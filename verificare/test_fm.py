import subprocess, sys, tempfile
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

if __name__ == "__main__":
    test_citeste_antetul(); test_corpul_exclude_antetul(); test_fisier_fara_antet_da_dict_gol()
    print("OK — 3 teste trecute")
