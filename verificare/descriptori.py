#!/usr/bin/env python3
"""Verifică dacă toți cei 40 de descriptori ai clasei a IX-a sunt observabili undeva."""
import sys
from pathlib import Path
import yaml
sys.path.insert(0, str(Path(__file__).parent))
import fm

RADACINA = Path(__file__).resolve().parent.parent
REF = yaml.safe_load((RADACINA / "verificare/referinta.yaml").read_text(encoding="utf-8"))
IESIRE = RADACINA / "docs/verificare/descriptori.md"

def main():
    lectii = fm.toate_lectiile(RADACINA / "manual")
    unde = {}
    for _, antet in lectii:
        eticheta = f"l{antet.get('lectie', antet.get('pas'))}"
        for d in antet.get("descriptori", []):
            unde.setdefault(d, []).append(eticheta)

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

    IESIRE.parent.mkdir(parents=True, exist_ok=True)
    IESIRE.write_text("\n".join(randuri[:2] + rezumat + randuri[2:]) + "\n", encoding="utf-8")
    print(f"Descriptori acoperiți: {40 - len(neacoperiti)}/40 | invalizi: {len(invalizi)}")
    return 1 if (neacoperiti or invalizi) else 0

if __name__ == "__main__":
    sys.exit(main())
