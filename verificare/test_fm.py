import sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import fm

EXEMPLU = """---
unitate: 1
lectie: 4
titlu: "Știri veridice, știri false"
competente: [11, 20]
descriptori: [21, 22, 40]
---

## Deschidere

Trei titluri.
"""

def test_citeste_antetul():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "l04.md"
        p.write_text(EXEMPLU, encoding="utf-8")
        a = fm.citeste(p)
        assert a["lectie"] == 4
        assert a["descriptori"] == [21, 22, 40]
        assert a["titlu"] == "Știri veridice, știri false"

def test_corpul_exclude_antetul():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "l04.md"
        p.write_text(EXEMPLU, encoding="utf-8")
        c = fm.corp(p)
        assert c.lstrip().startswith("## Deschidere")
        assert "unitate:" not in c

def test_fisier_fara_antet_da_dict_gol():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "x.md"
        p.write_text("# Doar text\n", encoding="utf-8")
        assert fm.citeste(p) == {}

LINIE_ORIZONTALA = """---

Text liber care conține cuvântul tip, dar nu este antet YAML.

---

## Restul textului
"""

def test_linie_orizontala_nu_e_antet():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "y.md"
        p.write_text(LINIE_ORIZONTALA, encoding="utf-8")
        assert fm.citeste(p) == {}
        assert p not in [cale for cale, _ in fm.toate_fisierele(radacina=d)]

def test_fisiere_cu_underscore_nu_se_numara():
    """Fișierele care încep cu _ sunt unelte de lucru și nu se numără în manual."""
    with tempfile.TemporaryDirectory() as d:
        # Fișier tool (nu se numără)
        p_tool = Path(d) / "_template.md"
        p_tool.write_text("""---
unitate: 0
lectie: 0
tip: continut
titlu: "Model"
ore: 1
competente: []
descriptori: []
unitati_competenta: []
continut_curricular: []
fise: []
---

# Model

Text
""", encoding="utf-8")

        # Fișier lecție obișnuit (se numără)
        p_lectie = Path(d) / "l01.md"
        p_lectie.write_text("""---
unitate: 1
lectie: 1
tip: continut
titlu: "Lecția 1"
ore: 1
competente: [1]
descriptori: [1]
unitati_competenta: []
continut_curricular: []
fise: []
---

# Lecția 1

Text
""", encoding="utf-8")

        # Verifică că doar l01.md apare în toate_fisierele
        fisiere = fm.toate_fisierele(radacina=d)
        cai = [p for p, _ in fisiere]
        assert p_lectie in cai, "Fișierul obișnuit trebuie inclus"
        assert p_tool not in cai, "Fișierul cu underscore trebuie exclus"

        # Verifică că doar l01.md apare în toate_lectiile
        lectii = fm.toate_lectiile(radacina=d)
        cai_lectii = [p for p, _ in lectii]
        assert p_lectie in cai_lectii, "Fișierul obișnuit trebuie inclus în lectii"
        assert p_tool not in cai_lectii, "Fișierul cu underscore trebuie exclus din lectii"

if __name__ == "__main__":
    test_citeste_antetul(); test_corpul_exclude_antetul(); test_fisier_fara_antet_da_dict_gol()
    test_linie_orizontala_nu_e_antet(); test_fisiere_cu_underscore_nu_se_numara()
    print("OK — 5 teste trecute")
