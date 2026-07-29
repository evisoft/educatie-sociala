import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import minute

def lectie(rubrici, ore=1):
    """Construiește corpul unei lecții din perechi (titlu, conținut)."""
    corp = "\n# Lecția N. Titlu\n\n> **Întrebarea lecției:** …\n"
    for titlu, continut in rubrici:
        corp += f"\n## {titlu}\n\n{continut}\n"
    return {"ore": ore}, corp

STANDARD = [
    ("Deschidere", "⏱ 3 min\n\nO situație."),
    ("De reținut", "⏱ 7 min\n\nMecanismul."),
    ("Dosar de lucru", "⏱ 6 min\n\nSursa A.\n\n⏱ 5 min\n\nÎn grupuri."),
    ("Sarcină de grup", "⏱ 15 min\n\nProdusul.\n\n⏱ 3 min\n\nPrezentarea."),
    ("Dosarul meu de cetățean", "⏱ 2 min <!-- expunere -->\n\nFișa."),
    ("Reflecție", "⏱ 3 min\n\nÎntrebări."),
]

def test_lectie_de_o_ora_in_buget():
    antet, corp = lectie(STANDARD)
    segs, total, expunere, lucru, buget, probleme, stare = minute.evalueaza(antet, corp)
    assert total == 44 and buget == 45, (total, buget)
    assert expunere == 9 and lucru == 29, (expunere, lucru)
    assert probleme == [], probleme
    assert stare == "bine (1 min liberi)"

def test_lectie_de_doua_ore_are_buget_de_90():
    rubrici = [(t, c.replace("⏱ 15 min", "⏱ 60 min")) for t, c in STANDARD]
    antet, corp = lectie(rubrici, ore=2)
    _, total, _, _, buget, probleme, _ = minute.evalueaza(antet, corp)
    assert buget == 90 and total == 89, (buget, total)
    assert probleme == [], probleme

def test_fara_niciun_marcaj_e_semnalata():
    antet, corp = lectie([(t, "Text fără marcaj.") for t, _ in STANDARD])
    _, total, _, _, _, probleme, _ = minute.evalueaza(antet, corp)
    assert total == 0
    assert any("niciun segment" in p for p in probleme), probleme

def test_titlu_de_rubrica_scris_gresit_e_semnalat():
    """„De reţinut" cu ț cu sedilă nu trebuie să dezactiveze tăcut clasificarea."""
    rubrici = [("De reţinut", "⏱ 30 min\n\nExpunere lungă."),
               ("Dosar de lucru", "⏱ 10 min\n\nLucru.")]
    antet, corp = lectie(rubrici)
    segs, total, expunere, lucru, _, probleme, _ = minute.evalueaza(antet, corp)
    assert total == 40
    assert any("rubrică necunoscută: De reţinut" in p for p in probleme), probleme
    # și, fiindcă rubrica nu e recunoscută, minutele ei nu se pot clasifica
    assert expunere == 0 and lucru == 10, (expunere, lucru)

def test_expunerea_nu_depaseste_lucrul():
    rubrici = [("De reținut", "⏱ 30 min\n\nExpunere."),
               ("Dosar de lucru", "⏱ 10 min\n\nLucru.")]
    antet, corp = lectie(rubrici)
    _, _, expunere, lucru, _, probleme, _ = minute.evalueaza(antet, corp)
    assert expunere == 30 and lucru == 10
    assert any("expunere > lucru cu 20 min" in p for p in probleme), probleme

def test_subbugetarea_grosolana_e_semnalata():
    antet, corp = lectie([("Deschidere", "⏱ 5 min\n\nAtât.")])
    _, total, _, _, _, probleme, _ = minute.evalueaza(antet, corp)
    assert total == 5
    assert any("subbugetat: 5 din 45 min" in p for p in probleme), probleme

def test_depasirea_e_semnalata():
    rubrici = [("De reținut", "⏱ 10 min\n\nX."), ("Sarcină de grup", "⏱ 40 min\n\nY.")]
    antet, corp = lectie(rubrici)
    _, total, _, _, _, probleme, _ = minute.evalueaza(antet, corp)
    assert total == 50
    assert any("depășire cu 5 min" in p for p in probleme), probleme

def test_bugetul_exact_are_stare_fara_marja():
    rubrici = [("De reținut", "⏱ 15 min\n\nX."), ("Sarcină de grup", "⏱ 30 min\n\nY.")]
    antet, corp = lectie(rubrici)
    _, total, _, _, _, probleme, stare = minute.evalueaza(antet, corp)
    assert total == 45 and probleme == []
    assert stare == "fără marjă", stare

def test_marcajul_inline_sau_in_cod_nu_se_numara():
    """Convenția cere marcajul pe rând propriu: citarea ei în text nu umflă bugetul."""
    rubrici = [("De reținut", "Scrii `⏱ 7 min` pe rând propriu. Vezi ⏱ 7 min în model.\n\n⏱ 7 min"),
               ("Dosar de lucru", "```\n⏱ 99 min\n```\n\n⏱ 35 min")]
    antet, corp = lectie(rubrici)
    segs, total, _, _, _, probleme, _ = minute.evalueaza(antet, corp)
    assert [m for m, _ in segs] == [7, 35], segs
    assert total == 42, total
    assert probleme == [], probleme

def test_eticheta_explicita_contrazice_implicitul():
    rubrici = [("De reținut", "⏱ 10 min <!-- lucru -->"),
               ("Sarcină de grup", "⏱ 10 min <!-- expunere -->"),
               ("Reflecție", "⏱ 20 min")]
    antet, corp = lectie(rubrici)
    _, _, expunere, lucru, _, _, _ = minute.evalueaza(antet, corp)
    assert expunere == 10 and lucru == 10, (expunere, lucru)

def test_ore_lipsa_si_ore_zero_dau_mesaje_diferite():
    _, corp = lectie(STANDARD)
    _, _, _, _, _, fara, _ = minute.evalueaza({}, corp)
    _, _, _, _, _, zero, _ = minute.evalueaza({"ore": 0}, corp)
    assert any("`ore` lipsește" in p for p in fara), fara
    assert any("`ore: 0` declarat" in p for p in zero), zero

TESTE = [v for k, v in sorted(globals().items()) if k.startswith("test_")]

if __name__ == "__main__":
    for t in TESTE:
        t()
    print(f"OK — {len(TESTE)} teste trecute")
