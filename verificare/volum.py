#!/usr/bin/env python3
"""Numără cuvintele fiecărei lecții și semnalează abaterile de la volumele stabilite."""
import re, sys
from pathlib import Path
import yaml
sys.path.insert(0, str(Path(__file__).parent))
import fm

RADACINA = Path(__file__).resolve().parent.parent
REF = yaml.safe_load((RADACINA / "verificare/referinta.yaml").read_text(encoding="utf-8"))
IESIRE = RADACINA / "docs/verificare/volum.md"

def cuvinte(text):
    fara_cod = re.sub(r"```.*?```", " ", text, flags=re.S)
    return len(re.findall(r"[\wăâîșțĂÂÎȘȚ]+", fara_cod))

def main():
    randuri = ["# Volumul lecțiilor", "", "| Fișier | Tip | Cuvinte | Interval | Stare |", "|---|---|---|---|---|"]
    abateri = 0
    ignorate = set(REF.get("ignora_volum", []))
    for cale, antet in fm.toate_fisierele(RADACINA / "manual"):
        tip = antet.get("tip", "continut")
        if tip in ignorate:
            continue
        n = cuvinte(fm.corp(cale))
        # Lecțiile de 2–3 ore își declară propriile limite în antet. Declarate pe jumătate,
        # ele sunt o eroare de antet — nu un motiv de a reveni tăcut la intervalul standard.
        are_min, are_max = "volum_min" in antet, "volum_max" in antet
        if are_min != are_max:
            lipsa = "volum_max" if are_min else "volum_min"
            randuri.append(f"| {cale.relative_to(RADACINA)} | {tip} | {n} | — | antet incomplet: lipsește {lipsa} |")
            abateri += 1
            continue
        if are_min:
            limite = {"min": antet["volum_min"], "max": antet["volum_max"]}
        else:
            limite = REF["volume"].get(tip)
        if limite is None:
            stare, interval = "tip necunoscut", "—"
            abateri += 1
        else:
            interval = f"{limite['min']}–{limite['max']}"
            if n < limite["min"]:
                stare = "prea scurt"; abateri += 1
            elif n > limite["max"]:
                stare = "prea lung"; abateri += 1
            else:
                stare = "bine"
        randuri.append(f"| {cale.relative_to(RADACINA)} | {tip} | {n} | {interval} | {stare} |")

    IESIRE.parent.mkdir(parents=True, exist_ok=True)
    IESIRE.write_text("\n".join(randuri) + "\n", encoding="utf-8")
    print(f"Abateri de volum: {abateri}")
    return 1 if abateri else 0

if __name__ == "__main__":
    sys.exit(main())
