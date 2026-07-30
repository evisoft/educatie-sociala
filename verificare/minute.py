#!/usr/bin/env python3
"""Bugetul de timp al lecțiilor: minutele declarate față de 45 × ore, plus regula lucru ≥ expunere.

Convenția de marcare, documentată în `manual/_template-lectie.md`:
fiecare segment cronometrat își declară durata **singur pe rândul lui**, sub forma

    ⏱ 7 min

Forma e canonică, nu orientativă. Orice rând care conține ceasul, dar nu se
parsează exact așa, e semnalat ca „marcaj nerecunoscut” — `- ⏱ 5 min` într-o
listă, `**⏱ 5 min**`, `⏱ 5 minute`, două marcaje pe același rând, un spațiu
insecabil după ceas sau o etichetă scrisă altfel. Un marcaj care nu se numără
și nu se plânge e o oră de 60 de minute care trece drept 45. Dacă o lecție are
nevoie să citeze convenția în text, o pune într-un bloc de cod: blocurile sunt
curățate înainte de scanare.

Se bugetează și ce pare gratuit: prezentarea produselor, trecerea de la lucrul
individual la cel în grup, citirea casetelor.

Fiecare segment intră într-una din trei categorii, după rubrica în care se află
(vezi `RUBRICI`): „De reținut” e expunere, „Dosar de lucru” și „Sarcină de grup”
sunt lucru al elevului, restul rubricilor sunt neutre. O rubrică poate contrazice
implicitul printr-un comentariu HTML, invizibil în pagina tipărită:

    ⏱ 3 min <!-- expunere -->

Lista rubricilor este **închisă** și **completă**: titlurile de nivel 2 sunt exact
cele șase de mai jos, toate, în ordinea din model. Un titlu scris altfel
(„De reţinut”, cu ț cu sedilă) sau o rubrică lipsă sunt abateri, nu tăceri.

Reguli verificate:
  1. suma minutelor declarate nu trece de 45 × `ore`;
  2. suma nu coboară sub 90% din buget (ora rămasă goală e tot o eroare de proiectare);
  3. expunerea nu depășește lucrul elevului;
  4. fiecare lecție are cel puțin un segment cronometrat și `ore` întreg în antet;
  5. rubricile sunt toate cele din model, o singură dată fiecare, în ordine;
  6. fiecare rând cu ceas e un marcaj canonic.
Ținta e 42–44 de minute pentru o oră: 45 e plafonul, nu obiectivul, așa că
egalitatea cu bugetul primește o stare distinctă, „fără marjă”.
"""
import re, sys
from pathlib import Path
from typing import NamedTuple
sys.path.insert(0, str(Path(__file__).parent))
import fm

RADACINA = Path(__file__).resolve().parent.parent
IESIRE = RADACINA / "docs/verificare/minute.md"
MINUTE_PE_ORA = 45
PRAG_MINIM = 0.9
CEAS = "⏱"
MARCAJ = re.compile(r"^⏱[ \t]*([1-9]\d*)[ \t]*min[ \t]*(?:<!--[ \t]*(expunere|lucru)[ \t]*-->)?[ \t]*$")
RUBRICA = re.compile(r"^##[ \t]+(.+?)[ \t]*$", re.M)
GARD = re.compile(r"^(```|~~~).*?^\1.*?$", re.M | re.S)
INDENTAT = re.compile(r"^(?: {4}|\t).*$", re.M)
RUBRICI = {
    "Deschidere": "neutru",
    "De reținut": "expunere",
    "Dosar de lucru": "lucru",
    "Sarcină de grup": "lucru",
    "Dosarul meu de cetățean": "neutru",
    "Reflecție": "neutru",
}

class Rezultat(NamedTuple):
    segmente: list      # [(minute, categorie)]
    minute: int
    expunere: int
    lucru: int
    buget: int
    probleme: list
    stare: str

def _curata(text):
    """Scoate blocurile de cod: gardurile ``` și ~~~ și liniile indentate cu patru spații."""
    return INDENTAT.sub(" ", GARD.sub(" ", text))

def _marcaje(bloc, categorie):
    """(segmente, rânduri cu ceas care nu se parsează)."""
    segmente, gresite = [], []
    for rand in bloc.splitlines():
        if CEAS not in rand:
            continue
        potrivire = MARCAJ.match(rand)
        if potrivire:
            minute, eticheta = potrivire.groups()
            segmente.append((int(minute), eticheta or categorie))
        else:
            gresite.append(rand.strip())
    return segmente, gresite

def scaneaza(corp):
    """(segmente, rubrici_gasite, marcaje_gresite)."""
    bucati = RUBRICA.split(_curata(corp))
    segmente, gresite = _marcaje(bucati[0], "neutru")
    rubrici = []
    for i in range(1, len(bucati), 2):
        titlu, bloc = bucati[i], bucati[i + 1]
        rubrici.append(titlu)
        s, g = _marcaje(bloc, RUBRICI.get(titlu, "neutru"))
        segmente += s
        gresite += g
    return segmente, rubrici, gresite

def _probleme_rubrici(rubrici):
    probleme = []
    cunoscute = [t for t in rubrici if t in RUBRICI]
    for titlu in rubrici:
        if titlu not in RUBRICI:
            probleme.append(f"**rubrică necunoscută: {titlu}**")
    for titlu in dict.fromkeys(cunoscute):
        if cunoscute.count(titlu) > 1:
            probleme.append(f"**rubrică repetată: {titlu}**")
    for titlu in RUBRICI:
        if titlu not in cunoscute:
            probleme.append(f"**rubrică lipsă: {titlu}**")
    fara_dubluri = list(dict.fromkeys(cunoscute))
    if fara_dubluri != [t for t in RUBRICI if t in fara_dubluri]:
        probleme.append("**rubricile nu sunt în ordinea din model**")
    return probleme

def evalueaza(antet, corp):
    segmente, rubrici, gresite = scaneaza(corp)
    total = sum(m for m, _ in segmente)
    expunere = sum(m for m, c in segmente if c == "expunere")
    lucru = sum(m for m, c in segmente if c == "lucru")
    ore = antet.get("ore")
    probleme = []
    if ore is None:
        probleme.append("**`ore` lipsește din antet**")
    elif not isinstance(ore, int) or isinstance(ore, bool):
        probleme.append(f"**`ore` nu e număr întreg: {ore!r}**")
    elif ore <= 0:
        probleme.append(f"**`ore: {ore}` declarat în antet**")
    elif not segmente:
        probleme.append("**niciun segment cronometrat**")
    buget = MINUTE_PE_ORA * ore if isinstance(ore, int) and not isinstance(ore, bool) and ore > 0 else 0
    if buget and segmente:
        if total > buget:
            probleme.append(f"**depășire cu {total - buget} min**")
        elif total < PRAG_MINIM * buget:
            probleme.append(f"**subbugetat: {total} din {buget} min**")
    if segmente and expunere > lucru:
        probleme.append(f"**expunere > lucru cu {expunere - lucru} min**")
    probleme += _probleme_rubrici(rubrici)
    for rand in gresite:
        probleme.append(f"**marcaj nerecunoscut: `{rand}`**")
    if probleme:
        stare = "; ".join(probleme)
    elif total == buget:
        stare = "fără marjă"
    else:
        stare = f"bine ({buget - total} min liberi)"
    return Rezultat(segmente, total, expunere, lucru, buget, probleme, stare)

def main(radacina=RADACINA / "manual", iesire=IESIRE):
    randuri = ["# Bugetul de timp al lecțiilor", "",
               f"Un segment se declară cu marcajul `⏱ N min`, singur pe rândul lui. Bugetul e {MINUTE_PE_ORA} de minute pentru fiecare oră din antet, iar ținta e 42–44 dintr-o oră: 45 e plafonul, nu obiectivul.",
               "Expunerea („De reținut” și segmentele marcate `<!-- expunere -->`) nu depășește lucrul elevului („Dosar de lucru”, „Sarcină de grup” și segmentele marcate `<!-- lucru -->`).", "",
               "| Fișier | Ore | Segmente | Minute | Buget | Expunere | Lucru | Stare |", "|---|---|---|---|---|---|---|---|"]
    abateri = 0
    for cale, antet in fm.toate_lectiile(radacina):
        r = evalueaza(antet, fm.corp(cale))
        abateri += 1 if r.probleme else 0
        nume = cale.relative_to(RADACINA) if RADACINA in cale.parents else cale.name
        randuri.append(f"| {nume} | {antet.get('ore', '—')} | {len(r.segmente)} | {r.minute} | {r.buget} | {r.expunere} | {r.lucru} | {r.stare} |")

    iesire.parent.mkdir(parents=True, exist_ok=True)
    iesire.write_text("\n".join(randuri) + "\n", encoding="utf-8")
    print(f"Abateri de timp: {abateri}")
    print(f"Raport: {iesire.relative_to(RADACINA) if RADACINA in iesire.parents else iesire}")
    return 1 if abateri else 0

if __name__ == "__main__":
    sys.exit(main())
