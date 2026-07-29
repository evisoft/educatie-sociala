#!/usr/bin/env python3
"""Verifică dacă toți cei 40 de descriptori ai clasei a IX-a sunt observabili undeva.

Verifică și o a doua regulă, încrucișată: cei 40 de descriptori formează 20 de
competențe, câte doi descriptori pentru fiecare (descriptorul `d` aparține
competenței `(d + 1) // 2`). Câmpul `competente` din antetul unei lecții trebuie
să fie exact mulțimea competențelor cărora le aparțin descriptorii declarați în
`descriptori` — nici mai multe, nici mai puține. O nepotrivire aici a scăpat de
trei ori vigilenței omului, ceea ce înseamnă că regula trebuie apărată de un
script, nu de atenția cuiva.
"""
import sys
from pathlib import Path
import yaml
sys.path.insert(0, str(Path(__file__).parent))
import fm

RADACINA = Path(__file__).resolve().parent.parent
REF = yaml.safe_load((RADACINA / "verificare/referinta.yaml").read_text(encoding="utf-8"))
IESIRE = RADACINA / "docs/verificare/descriptori.md"

def competenta_pentru(descriptor):
    """Numărul competenței căreia îi aparține un descriptor (doi descriptori pe competență)."""
    return (descriptor + 1) // 2

def competente_asteptate(descriptori):
    """Mulțimea (sortată) a competențelor la care duc descriptorii dați."""
    return sorted({competenta_pentru(d) for d in descriptori})

def verifica_competente(antet):
    """None dacă `competente` declarate corespund descriptorilor; altfel (declarate, așteptate)."""
    declarate = sorted(antet.get("competente", []))
    asteptate = competente_asteptate(antet.get("descriptori", []))
    return None if declarate == asteptate else (declarate, asteptate)

def main():
    lectii = fm.toate_lectiile(RADACINA / "manual")
    unde = {}
    abateri_competente = []
    for cale, antet in lectii:
        eticheta = f"l{antet.get('lectie', antet.get('pas'))}"
        for d in antet.get("descriptori", []):
            unde.setdefault(d, []).append(eticheta)
        rezultat = verifica_competente(antet)
        if rezultat is not None:
            declarate, asteptate = rezultat
            abateri_competente.append((cale.relative_to(RADACINA), declarate, asteptate))

    randuri = ["# Acoperirea descriptorilor — clasa a IX-a", "",
               "| # | Descriptor | Observabil în |", "|---|---|---|"]
    neacoperiti = []
    for numar, text in REF["descriptori"].items():
        locuri = unde.get(numar, [])
        if not locuri:
            neacoperiti.append(numar)
        randuri.append(f"| {numar} | {text} | {', '.join(locuri) or '**NEACOPERIT**'} |")

    invalizi = [d for d in unde if d not in REF["descriptori"]]
    rezumat = [f"Acoperiți: **{40 - len(neacoperiti)}/40**.", ""]
    if neacoperiti:
        rezumat += [f"Neacoperiți: {', '.join(str(x) for x in neacoperiti)}", ""]
    if invalizi:
        rezumat += [f"Numere invalide în antete: {', '.join(str(x) for x in invalizi)}", ""]

    sectiune_competente = ["", "## Competențe declarate vs. competențe așteptate", ""]
    if abateri_competente:
        sectiune_competente += ["| Fișier | Declarate | Așteptate |", "|---|---|---|"]
        sectiune_competente += [
            f"| {cale} | {declarate} | {asteptate} |"
            for cale, declarate, asteptate in abateri_competente
        ]
    else:
        sectiune_competente += ["Toate lecțiile: `competente` corespunde exact competențelor descriptorilor declarați."]

    IESIRE.parent.mkdir(parents=True, exist_ok=True)
    IESIRE.write_text(
        "\n".join(randuri[:2] + rezumat + randuri[2:] + sectiune_competente) + "\n",
        encoding="utf-8",
    )
    print(f"Descriptori acoperiți: {40 - len(neacoperiti)}/40 | invalizi: {len(invalizi)} | abateri de competențe: {len(abateri_competente)}")
    for cale, declarate, asteptate in abateri_competente:
        print(f"  - {cale}: declarat {declarate}, așteptat {asteptate}")
    return 1 if (neacoperiti or invalizi or abateri_competente) else 0

if __name__ == "__main__":
    sys.exit(main())
