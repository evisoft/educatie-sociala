#!/usr/bin/env python3
"""Verifică dacă lecțiile încap în oră: minutele declarate față de 45 × ore.

Convenția de marcare, documentată în `manual/_template-lectie.md`:
fiecare segment cronometrat își declară durata pe un rând propriu, sub forma

    ⏱ 7 min

Se bugetează și ce pare gratuit: prezentarea produselor, trecerea de la lucrul
individual la cel în grup, citirea casetelor. O lecție fără niciun segment
cronometrat este semnalată, nu trecută tăcut.
"""
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import fm

RADACINA = Path(__file__).resolve().parent.parent
IESIRE = RADACINA / "docs/verificare/minute.md"
MINUTE_PE_ORA = 45
MARCAJ = re.compile(r"⏱\s*(\d+)\s*min")

def segmente(text):
    fara_cod = re.sub(r"```.*?```", " ", text, flags=re.S)
    return [int(x) for x in MARCAJ.findall(fara_cod)]

def main():
    randuri = ["# Bugetul de minute al lecțiilor", "",
               f"Un segment se declară cu marcajul `⏱ N min`. Bugetul e {MINUTE_PE_ORA} de minute pentru fiecare oră din antet.", "",
               "| Fișier | Ore | Segmente | Minute declarate | Buget | Stare |", "|---|---|---|---|---|---|"]
    abateri = 0
    for cale, antet in fm.toate_lectiile(RADACINA / "manual"):
        ore = antet.get("ore", 0)
        segs = segmente(fm.corp(cale))
        total = sum(segs)
        buget = MINUTE_PE_ORA * ore
        if not ore:
            stare = "**ore nedeclarate în antet**"; abateri += 1
        elif not segs:
            stare = "**niciun segment cronometrat**"; abateri += 1
        elif total > buget:
            stare = f"**depășire cu {total - buget} min**"; abateri += 1
        else:
            stare = "bine" if total == buget else f"bine ({buget - total} min liberi)"
        randuri.append(f"| {cale.relative_to(RADACINA)} | {ore} | {len(segs)} | {total} | {buget} | {stare} |")

    IESIRE.parent.mkdir(parents=True, exist_ok=True)
    IESIRE.write_text("\n".join(randuri) + "\n", encoding="utf-8")
    print(f"Abateri de minute: {abateri}")
    print(f"Raport: {IESIRE.relative_to(RADACINA)}")
    return 1 if abateri else 0

if __name__ == "__main__":
    sys.exit(main())
