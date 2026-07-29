#!/usr/bin/env python3
"""Bugetul de timp al lecțiilor: minutele declarate față de 45 × ore, plus regula lucru ≥ expunere.

Convenția de marcare, documentată în `manual/_template-lectie.md`:
fiecare segment cronometrat își declară durata pe un rând propriu, sub forma

    ⏱ 7 min

Se bugetează și ce pare gratuit: prezentarea produselor, trecerea de la lucrul
individual la cel în grup, citirea casetelor. O lecție fără niciun segment
cronometrat este semnalată, nu trecută tăcut.

Fiecare segment intră într-una din trei categorii, după rubrica în care se află:
„De reținut" e expunere; „Dosar de lucru" și „Sarcină de grup" sunt lucru al
elevului; restul rubricilor sunt neutre. O rubrică poate contrazice implicitul
marcând segmentul: `⏱ 3 min (expunere)` sau `⏱ 5 min (lucru)` — folosit acolo
unde, de pildă, rubrica „Dosarul meu de cetățean" prezintă ceva, în loc să pună
elevul la treabă. Regula: expunerea nu depășește lucrul.
"""
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import fm

RADACINA = Path(__file__).resolve().parent.parent
IESIRE = RADACINA / "docs/verificare/minute.md"
MINUTE_PE_ORA = 45
MARCAJ = re.compile(r"⏱\s*(\d+)\s*min(?:\s*\((expunere|lucru)\))?")
IMPLICIT = {"De reținut": "expunere", "Dosar de lucru": "lucru", "Sarcină de grup": "lucru"}

def segmente(text):
    """[(minute, categorie)] — categoria: expunere, lucru sau neutru."""
    fara_cod = re.sub(r"```.*?```", " ", text, flags=re.S)
    gasite, rubrica = [], ""
    for bucata in re.split(r"\n##\s+", "\n" + fara_cod):
        titlu = bucata.split("\n", 1)[0].strip()
        rubrica = IMPLICIT.get(titlu, "neutru")
        for minute, eticheta in MARCAJ.findall(bucata):
            gasite.append((int(minute), eticheta or rubrica))
    return gasite

def main():
    randuri = ["# Bugetul de timp al lecțiilor", "",
               f"Un segment se declară cu marcajul `⏱ N min`. Bugetul e {MINUTE_PE_ORA} de minute pentru fiecare oră din antet.",
               "Expunerea („De reținut” și segmentele marcate `(expunere)`) nu depășește lucrul elevului („Dosar de lucru”, „Sarcină de grup” și segmentele marcate `(lucru)`).", "",
               "| Fișier | Ore | Segmente | Minute | Buget | Expunere | Lucru | Stare |", "|---|---|---|---|---|---|---|---|"]
    abateri = 0
    for cale, antet in fm.toate_lectiile(RADACINA / "manual"):
        ore = antet.get("ore", 0)
        segs = segmente(fm.corp(cale))
        total = sum(m for m, _ in segs)
        expunere = sum(m for m, c in segs if c == "expunere")
        lucru = sum(m for m, c in segs if c == "lucru")
        buget = MINUTE_PE_ORA * ore
        probleme = []
        if not ore:
            probleme.append("**ore nedeclarate în antet**")
        elif not segs:
            probleme.append("**niciun segment cronometrat**")
        elif total > buget:
            probleme.append(f"**depășire cu {total - buget} min**")
        if segs and expunere > lucru:
            probleme.append(f"**expunere > lucru cu {expunere - lucru} min**")
        if probleme:
            abateri += 1
            stare = "; ".join(probleme)
        else:
            stare = "bine" if total == buget else f"bine ({buget - total} min liberi)"
        randuri.append(f"| {cale.relative_to(RADACINA)} | {ore} | {len(segs)} | {total} | {buget} | {expunere} | {lucru} | {stare} |")

    IESIRE.parent.mkdir(parents=True, exist_ok=True)
    IESIRE.write_text("\n".join(randuri) + "\n", encoding="utf-8")
    print(f"Abateri de timp: {abateri}")
    print(f"Raport: {IESIRE.relative_to(RADACINA)}")
    return 1 if abateri else 0

if __name__ == "__main__":
    sys.exit(main())
