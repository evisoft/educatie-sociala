#!/usr/bin/env python3
"""Bugetul de timp al lecțiilor: minutele declarate față de 45 × ore, plus regula lucru ≥ expunere.

Convenția de marcare, documentată în `manual/_template-lectie.md`:
fiecare segment cronometrat își declară durata **pe un rând propriu**, sub forma

    ⏱ 7 min

Rândul propriu e obligatoriu: altfel, o lecție care citează convenția în text
(`⏱ 7 min` inline) și-ar umfla bugetul.

Se bugetează și ce pare gratuit: prezentarea produselor, trecerea de la lucrul
individual la cel în grup, citirea casetelor. O lecție fără niciun segment
cronometrat este semnalată, nu trecută tăcut.

Fiecare segment intră într-una din trei categorii, după rubrica în care se află
(vezi `RUBRICI`): „De reținut” e expunere, „Dosar de lucru” și „Sarcină de grup”
sunt lucru al elevului, restul rubricilor sunt neutre. O rubrică poate contrazice
implicitul printr-un comentariu HTML, invizibil în pagina tipărită:

    ⏱ 3 min <!-- expunere -->

Lista rubricilor este **închisă**: orice titlu de nivel 2 care nu se află în ea
e semnalat ca abatere. Un titlu scris altfel („De reţinut”, cu ț cu sedilă, sau
„Sarcina de grup”) ar dezactiva tăcut clasificarea — mai bine un fals-pozitiv
care se repară decât o regulă care tace. O rubrică nouă se adaugă aici deliberat.

Reguli verificate:
  1. suma minutelor declarate nu trece de 45 × `ore`;
  2. suma nu coboară sub 90% din buget (ora rămasă goală e tot o eroare de proiectare);
  3. expunerea nu depășește lucrul elevului;
  4. fiecare lecție are cel puțin un segment cronometrat și `ore` în antet;
  5. toate rubricile de nivel 2 sunt cunoscute.
Ținta e 42–44 de minute pentru o oră: 45 e plafonul, nu obiectivul, așa că
egalitatea cu bugetul primește o stare distinctă, „fără marjă”.
"""
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import fm

RADACINA = Path(__file__).resolve().parent.parent
IESIRE = RADACINA / "docs/verificare/minute.md"
MINUTE_PE_ORA = 45
PRAG_MINIM = 0.9
MARCAJ = re.compile(r"^⏱[ \t]*(\d+)[ \t]*min[ \t]*(?:<!--[ \t]*(expunere|lucru)[ \t]*-->)?[ \t]*$", re.M)
RUBRICA = re.compile(r"^##[ \t]+(.+?)[ \t]*$", re.M)
RUBRICI = {
    "Deschidere": "neutru",
    "De reținut": "expunere",
    "Dosar de lucru": "lucru",
    "Sarcină de grup": "lucru",
    "Dosarul meu de cetățean": "neutru",
    "Reflecție": "neutru",
}

def segmente(text):
    """(segmente, rubrici_necunoscute); un segment e (minute, categorie)."""
    fara_cod = re.sub(r"```.*?```", " ", text, flags=re.S)
    bucati = RUBRICA.split(fara_cod)
    gasite = [(int(m), e or "neutru") for m, e in MARCAJ.findall(bucati[0])]
    necunoscute = []
    for i in range(1, len(bucati), 2):
        titlu, corp = bucati[i], bucati[i + 1]
        if titlu not in RUBRICI:
            necunoscute.append(titlu)
        categorie = RUBRICI.get(titlu, "neutru")
        gasite += [(int(m), e or categorie) for m, e in MARCAJ.findall(corp)]
    return gasite, necunoscute

def evalueaza(antet, corp):
    """(segmente, minute, expunere, lucru, buget, probleme, stare)."""
    segs, necunoscute = segmente(corp)
    total = sum(m for m, _ in segs)
    expunere = sum(m for m, c in segs if c == "expunere")
    lucru = sum(m for m, c in segs if c == "lucru")
    ore = antet.get("ore")
    buget = MINUTE_PE_ORA * (ore or 0)
    probleme = []
    if ore is None:
        probleme.append("**`ore` lipsește din antet**")
    elif ore == 0:
        probleme.append("**`ore: 0` declarat în antet**")
    elif not segs:
        probleme.append("**niciun segment cronometrat**")
    elif total > buget:
        probleme.append(f"**depășire cu {total - buget} min**")
    elif total < PRAG_MINIM * buget:
        probleme.append(f"**subbugetat: {total} din {buget} min**")
    if segs and expunere > lucru:
        probleme.append(f"**expunere > lucru cu {expunere - lucru} min**")
    for titlu in necunoscute:
        probleme.append(f"**rubrică necunoscută: {titlu}**")
    if probleme:
        stare = "; ".join(probleme)
    elif total == buget:
        stare = "fără marjă"
    else:
        stare = f"bine ({buget - total} min liberi)"
    return segs, total, expunere, lucru, buget, probleme, stare

def main():
    randuri = ["# Bugetul de timp al lecțiilor", "",
               f"Un segment se declară cu marcajul `⏱ N min`, pe rând propriu. Bugetul e {MINUTE_PE_ORA} de minute pentru fiecare oră din antet, iar ținta e 42–44 dintr-o oră: 45 e plafonul, nu obiectivul.",
               "Expunerea („De reținut” și segmentele marcate `<!-- expunere -->`) nu depășește lucrul elevului („Dosar de lucru”, „Sarcină de grup” și segmentele marcate `<!-- lucru -->`).", "",
               "| Fișier | Ore | Segmente | Minute | Buget | Expunere | Lucru | Stare |", "|---|---|---|---|---|---|---|---|"]
    abateri = 0
    for cale, antet in fm.toate_lectiile(RADACINA / "manual"):
        segs, total, expunere, lucru, buget, probleme, stare = evalueaza(antet, fm.corp(cale))
        abateri += 1 if probleme else 0
        randuri.append(f"| {cale.relative_to(RADACINA)} | {antet.get('ore', '—')} | {len(segs)} | {total} | {buget} | {expunere} | {lucru} | {stare} |")

    IESIRE.parent.mkdir(parents=True, exist_ok=True)
    IESIRE.write_text("\n".join(randuri) + "\n", encoding="utf-8")
    print(f"Abateri de timp: {abateri}")
    print(f"Raport: {IESIRE.relative_to(RADACINA)}")
    return 1 if abateri else 0

if __name__ == "__main__":
    sys.exit(main())
