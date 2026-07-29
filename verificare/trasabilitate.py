#!/usr/bin/env python3
"""Verifică dacă manualul acoperă integral curriculumul."""
import sys
from pathlib import Path
import yaml
sys.path.insert(0, str(Path(__file__).parent))
import fm

RADACINA = Path(__file__).resolve().parent.parent
REF = yaml.safe_load((RADACINA / "verificare/referinta.yaml").read_text(encoding="utf-8"))
IESIRE = RADACINA / "docs/verificare/trasabilitate.md"

def main():
    lectii = fm.toate_lectiile(RADACINA / "manual")
    acoperire = {"unitati_de_competente": {}, "unitati_de_continut": {}}
    for cale, antet in lectii:
        eticheta = f"l{antet.get('lectie', antet.get('pas'))}"
        for cheie, camp in (("unitati_de_competente", "unitati_competenta"),
                            ("unitati_de_continut", "continut_curricular")):
            for cod in antet.get(camp, []):
                acoperire[cheie].setdefault(cod, []).append(eticheta)

    randuri, lipsa, necunoscute = [], [], []
    for cheie, titlu in (("unitati_de_competente", "Unități de competențe"),
                         ("unitati_de_continut", "Unități de conținut")):
        randuri += [f"\n## {titlu}\n", "| Cod | Text | Acoperit în |", "|---|---|---|"]
        for cod, text in REF[cheie].items():
            unde = acoperire[cheie].get(cod, [])
            if not unde:
                lipsa.append(f"{cheie}:{cod}")
            randuri.append(f"| {cod} | {text} | {', '.join(unde) or '**LIPSĂ**'} |")
        for cod in acoperire[cheie]:
            if cod not in REF[cheie]:
                necunoscute.append(f"{cheie}:{cod}")

    ore = sum(a.get("ore", 0) for _, a in lectii)
    antet_raport = [
        "# Trasabilitate curriculară", "",
        f"Fișiere de lecție găsite: **{len(lectii)}**. Total ore declarate: **{ore}** (țintă: 34).", "",
    ]
    if lipsa:
        antet_raport += ["## Neacoperit", ""] + [f"- {x}" for x in lipsa] + [""]
    if necunoscute:
        antet_raport += ["## Coduri necunoscute în antete", ""] + [f"- {x}" for x in necunoscute] + [""]
    IESIRE.parent.mkdir(parents=True, exist_ok=True)
    IESIRE.write_text("\n".join(antet_raport + randuri) + "\n", encoding="utf-8")

    print(f"Fișiere: {len(lectii)} | ore: {ore} | neacoperit: {len(lipsa)} | coduri necunoscute: {len(necunoscute)}")
    print(f"Raport: {IESIRE.relative_to(RADACINA)}")
    return 1 if (lipsa or necunoscute or ore != 34) else 0

if __name__ == "__main__":
    sys.exit(main())
