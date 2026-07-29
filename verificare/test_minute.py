import contextlib, io, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import minute

STANDARD = [
    ("Deschidere", "⏱ 3 min\n\nO situație."),
    ("De reținut", "⏱ 7 min\n\nMecanismul."),
    ("Dosar de lucru", "⏱ 6 min\n\nSursa A.\n\n⏱ 4 min\n\nÎn grupuri."),
    ("Sarcină de grup", "⏱ 15 min\n\nProdusul.\n\n⏱ 3 min\n\nPrezentarea."),
    ("Dosarul meu de cetățean", "⏱ 2 min <!-- expunere -->\n\nFișa."),
    ("Reflecție", "⏱ 3 min\n\nÎntrebări."),
]

def lectie(rubrici=None, ore=1):
    """(antet, corp) — o lecție construită din perechi (titlu, conținut)."""
    corp = "\n# Lecția N. Titlu\n\n> **Întrebarea lecției:** …\n"
    for titlu, continut in (STANDARD if rubrici is None else rubrici):
        corp += f"\n## {titlu}\n\n{continut}\n"
    return {"ore": ore}, corp

def toate_rubricile(inlocuiri):
    """STANDARD, cu conținutul unor rubrici înlocuit — ca restul anatomiei să nu zgomote testul."""
    return [(t, inlocuiri.get(t, c)) for t, c in STANDARD]

# ── bugetul ──────────────────────────────────────────────────────────────────

def test_lectie_de_o_ora_in_buget():
    r = minute.evalueaza(*lectie())
    assert (r.minute, r.buget) == (43, 45)
    assert (r.expunere, r.lucru) == (9, 28)
    assert r.probleme == []
    assert r.stare == "bine (2 min liberi)"

def test_lectie_de_doua_ore_are_buget_de_90():
    r = minute.evalueaza(*lectie(toate_rubricile({"Sarcină de grup": "⏱ 60 min\n\nX."}), ore=2))
    assert (r.buget, r.minute) == (90, 85)
    assert r.probleme == []

def test_lectie_de_trei_ore_are_buget_de_135():
    r = minute.evalueaza(*lectie(toate_rubricile({"Sarcină de grup": "⏱ 105 min\n\nX."}), ore=3))
    assert (r.buget, r.minute) == (135, 130)
    assert r.probleme == []

def test_depasirea_e_semnalata():
    r = minute.evalueaza(*lectie(toate_rubricile({"Sarcină de grup": "⏱ 25 min\n\nX."})))
    assert r.minute == 50
    assert any("depășire cu 5 min" in p for p in r.probleme), r.probleme

def test_bugetul_exact_are_stare_fara_marja():
    r = minute.evalueaza(*lectie(toate_rubricile({"Sarcină de grup": "⏱ 20 min\n\nX."})))
    assert (r.minute, r.probleme) == (45, [])
    assert r.stare == "fără marjă"

def test_pragul_de_jos_la_limita():
    """40,5 = 90% din 45: 41 trece, 40 nu."""
    peste = minute.evalueaza(*lectie(toate_rubricile({"Sarcină de grup": "⏱ 16 min\n\nX."})))
    sub = minute.evalueaza(*lectie(toate_rubricile({"Sarcină de grup": "⏱ 15 min\n\nX."})))
    assert (peste.minute, peste.probleme) == (41, [])
    assert sub.minute == 40
    assert any("subbugetat: 40 din 45 min" in p for p in sub.probleme), sub.probleme

def test_subbugetarea_grosolana_e_semnalata():
    rubrici = [(t, c if t == "Deschidere" else c.replace("⏱", "ceas")) for t, c in STANDARD]
    r = minute.evalueaza(*lectie(rubrici))
    assert r.minute == 3
    assert any("subbugetat: 3 din 45 min" in p for p in r.probleme), r.probleme

def test_fara_niciun_marcaj_e_semnalata():
    r = minute.evalueaza(*lectie([(t, "Text fără marcaj.") for t, _ in STANDARD]))
    assert r.minute == 0
    assert any("niciun segment" in p for p in r.probleme), r.probleme

def test_ore_lipsa_ore_zero_si_ore_text():
    _, corp = lectie()
    fara = minute.evalueaza({}, corp).probleme
    zero = minute.evalueaza({"ore": 0}, corp).probleme
    text = minute.evalueaza({"ore": "1"}, corp).probleme
    assert any("`ore` lipsește" in p for p in fara), fara
    assert any("`ore: 0` declarat" in p for p in zero), zero
    assert any("nu e număr întreg" in p for p in text), text

# ── expunere / lucru ─────────────────────────────────────────────────────────

def test_expunerea_nu_depaseste_lucrul():
    r = minute.evalueaza(*lectie(toate_rubricile(
        {"De reținut": "⏱ 30 min\n\nX.", "Sarcină de grup": "⏱ 4 min\n\nY."})))
    assert (r.expunere, r.lucru) == (32, 14)
    assert any("expunere > lucru cu 18 min" in p for p in r.probleme), r.probleme

def test_eticheta_explicita_contrazice_implicitul():
    """Cazul e asimetric intenționat: dacă eticheta e ignorată sau inversată, sumele se schimbă."""
    rubrici = toate_rubricile({
        "De reținut": "⏱ 10 min <!-- lucru -->",
        "Dosar de lucru": "⏱ 6 min",
        "Sarcină de grup": "⏱ 4 min <!-- expunere -->",
        "Dosarul meu de cetățean": "⏱ 2 min",
    })
    r = minute.evalueaza(*lectie(rubrici))
    assert r.segmente == [(3, "neutru"), (10, "lucru"), (6, "lucru"),
                          (4, "expunere"), (2, "neutru"), (3, "neutru")], r.segmente
    assert (r.expunere, r.lucru) == (4, 16)

# ── rubricile ────────────────────────────────────────────────────────────────

def test_titlu_de_rubrica_scris_gresit_e_semnalat():
    """„De reţinut", cu ț cu sedilă, nu trebuie să dezactiveze tăcut clasificarea."""
    rubrici = [("De reţinut" if t == "De reținut" else t, c) for t, c in STANDARD]
    r = minute.evalueaza(*lectie(rubrici))
    assert any("rubrică necunoscută: De reţinut" in p for p in r.probleme), r.probleme
    assert any("rubrică lipsă: De reținut" in p for p in r.probleme), r.probleme
    assert (r.expunere, r.lucru) == (2, 28), (r.expunere, r.lucru)

def test_rubrica_lipsa_e_semnalata():
    r = minute.evalueaza(*lectie([(t, c) for t, c in STANDARD if t != "Reflecție"]))
    assert any("rubrică lipsă: Reflecție" in p for p in r.probleme), r.probleme

def test_rubricile_in_alta_ordine_sunt_semnalate():
    rubrici = list(STANDARD)
    rubrici[1], rubrici[2] = rubrici[2], rubrici[1]
    r = minute.evalueaza(*lectie(rubrici))
    assert any("nu sunt în ordinea din model" in p for p in r.probleme), r.probleme

def test_rubrica_repetata_e_semnalata():
    r = minute.evalueaza(*lectie(STANDARD + [("Reflecție", "⏱ 1 min")]))
    assert any("rubrică repetată: Reflecție" in p for p in r.probleme), r.probleme

# ── marcajul ─────────────────────────────────────────────────────────────────

def test_marcajul_in_bloc_de_cod_nu_se_numara():
    for gard in ("```", "~~~"):
        rubrici = toate_rubricile({"De reținut": f"{gard}\n⏱ 99 min\n{gard}\n\n⏱ 7 min"})
        r = minute.evalueaza(*lectie(rubrici))
        assert r.minute == 43, (gard, r.minute)
        assert r.probleme == [], (gard, r.probleme)

def test_marcajul_in_cod_indentat_nu_se_numara():
    rubrici = toate_rubricile({"De reținut": "Exemplu:\n\n    ⏱ 99 min\n\n⏱ 7 min"})
    r = minute.evalueaza(*lectie(rubrici))
    assert r.minute == 43, r.minute
    assert r.probleme == [], r.probleme

def test_marcajele_necanonice_sunt_semnalate_nu_ignorate():
    """Fiecare formă de mai jos ar fi trecut tăcut, cu zero minute adunate."""
    for rand in ["- ⏱ 5 min", "**⏱ 5 min**", "⏱ 5 minute", "⏱ 5 min <!-- Expunere -->",
                 "⏱ 5 min <!-- lucru individual -->", "⏱ 5 min", "⏱ 2 min ⏱ 3 min",
                 "⏱ 5 min (expunere)", "text ⏱ 5 min", "⏱ 0 min"]:
        rubrici = toate_rubricile({"De reținut": f"{rand}\n\n⏱ 7 min"})
        r = minute.evalueaza(*lectie(rubrici))
        assert r.minute == 43, (rand, r.minute)
        assert any("marcaj nerecunoscut" in p for p in r.probleme), (rand, r.probleme)

def test_marcajul_canonic_accepta_eticheta_si_spatii():
    for rand in ["⏱ 7 min", "⏱  7  min", "⏱ 7 min <!-- expunere -->", "⏱ 7 min <!--lucru-->"]:
        rubrici = toate_rubricile({"De reținut": rand})
        r = minute.evalueaza(*lectie(rubrici))
        assert r.minute == 43, (rand, r.minute)

# ── raportul ─────────────────────────────────────────────────────────────────

ANTET = "---\nunitate: 1\nlectie: 1\ntip: continut\nore: 1\n---\n"

def _scrie(d, corp):
    radacina = Path(d) / "manual"
    radacina.mkdir()
    (radacina / "l01.md").write_text(ANTET + corp, encoding="utf-8")
    return radacina, Path(d) / "raport.md"

def test_main_numara_abaterile_si_intoarce_cod_1():
    _, corp = lectie([(t, c) for t, c in STANDARD if t != "Reflecție"])
    with tempfile.TemporaryDirectory() as d:
        radacina, iesire = _scrie(d, corp)
        with contextlib.redirect_stdout(io.StringIO()):
            cod = minute.main(radacina=radacina, iesire=iesire)
        assert cod == 1
        raport = iesire.read_text(encoding="utf-8")
        assert "rubrică lipsă: Reflecție" in raport
        assert "l01.md" in raport

def test_main_intoarce_0_pe_o_lectie_curata():
    _, corp = lectie()
    with tempfile.TemporaryDirectory() as d:
        radacina, iesire = _scrie(d, corp)
        with contextlib.redirect_stdout(io.StringIO()):
            cod = minute.main(radacina=radacina, iesire=iesire)
        assert cod == 0
        assert "bine (2 min liberi)" in iesire.read_text(encoding="utf-8")

TESTE = [v for k, v in sorted(globals().items()) if k.startswith("test_")]

if __name__ == "__main__":
    for t in TESTE:
        t()
    print(f"OK — {len(TESTE)} teste trecute")
