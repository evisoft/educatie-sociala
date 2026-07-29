import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import descriptori

# ── competenta_pentru ───────────────────────────────────────────────────────

def test_competenta_pentru_descriptori_impari_si_pari():
    # Fiecare pereche (2k-1, 2k) duce la competența k.
    assert descriptori.competenta_pentru(19) == 10
    assert descriptori.competenta_pentru(20) == 10
    assert descriptori.competenta_pentru(21) == 11
    assert descriptori.competenta_pentru(22) == 11
    assert descriptori.competenta_pentru(1) == 1
    assert descriptori.competenta_pentru(40) == 20

def test_competente_asteptate_e_o_multime_sortata_fara_dubluri():
    assert descriptori.competente_asteptate([19, 21, 22]) == [10, 11]
    assert descriptori.competente_asteptate([15, 20, 35]) == [8, 10, 18]
    assert descriptori.competente_asteptate([]) == []

# ── verifica_competente ─────────────────────────────────────────────────────

def test_verifica_competente_trece_cand_corespund():
    antet = {"competente": [10, 11], "descriptori": [19, 21, 22]}
    assert descriptori.verifica_competente(antet) is None

def test_verifica_competente_trece_indiferent_de_ordine():
    antet = {"competente": [11, 10], "descriptori": [22, 19, 21]}
    assert descriptori.verifica_competente(antet) is None

def test_verifica_competente_semnaleaza_nepotrivirea():
    # Eroarea reală din antetul lecției 1: [11, 20] în loc de [10, 11].
    antet = {"competente": [11, 20], "descriptori": [19, 21, 22]}
    rezultat = descriptori.verifica_competente(antet)
    assert rezultat == ([11, 20], [10, 11])

def test_verifica_competente_semnaleaza_lista_goala_cand_lipseste():
    antet = {"descriptori": [19, 21, 22]}
    rezultat = descriptori.verifica_competente(antet)
    assert rezultat == ([], [10, 11])

# ── main() pe lecția 0 și lecția 1 din manual ───────────────────────────────

def test_lectiile_din_manual_au_competente_corecte():
    """Antetele reale trebuie să treacă validarea — inclusiv l00 și l01."""
    radacina = Path(__file__).resolve().parent.parent / "manual"
    abateri = []
    for cale, antet in descriptori.fm.toate_lectiile(radacina):
        rezultat = descriptori.verifica_competente(antet)
        if rezultat is not None:
            abateri.append((cale.name, rezultat))
    assert abateri == [], f"Antete cu competențe greșite: {abateri}"

if __name__ == "__main__":
    test_competenta_pentru_descriptori_impari_si_pari()
    test_competente_asteptate_e_o_multime_sortata_fara_dubluri()
    test_verifica_competente_trece_cand_corespund()
    test_verifica_competente_trece_indiferent_de_ordine()
    test_verifica_competente_semnaleaza_nepotrivirea()
    test_verifica_competente_semnaleaza_lista_goala_cand_lipseste()
    test_lectiile_din_manual_au_competente_corecte()
    print("OK — 7 teste trecute")
