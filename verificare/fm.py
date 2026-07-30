"""Citirea antetelor YAML din fișierele manualului."""
from pathlib import Path
import yaml

SEPARATOR = "---"

def _imparte(text):
    if not text.startswith(SEPARATOR):
        return "", text
    rest = text[len(SEPARATOR):]
    capat = rest.find("\n" + SEPARATOR)
    if capat == -1:
        return "", text
    return rest[:capat], rest[capat + len(SEPARATOR) + 1:]

def citeste(cale):
    antet, _ = _imparte(Path(cale).read_text(encoding="utf-8"))
    if not antet.strip():
        return {}
    incarcat = yaml.safe_load(antet)
    return incarcat if isinstance(incarcat, dict) else {}

def corp(cale):
    _, c = _imparte(Path(cale).read_text(encoding="utf-8"))
    return c

def toate_fisierele(radacina="manual"):
    """Toate fișierele manualului care au antet cu `tip` (inclusiv deschideri și anexe).

    Fișierele al căror nume începe cu `_` sunt unelte de lucru, nu părți din manual
    (modelul de lecție, de pildă). Ele nu se numără nicăieri.
    """
    rezultat = []
    for p in sorted(Path(radacina).rglob("*.md")):
        if p.name.startswith("_"):
            continue
        a = citeste(p)
        if "tip" in a:
            rezultat.append((p, a))
    return rezultat

def toate_lectiile(radacina="manual"):
    """Doar lecțiile și pașii de șantier — cele care consumă ore și acoperă curriculum."""
    return [(p, a) for p, a in toate_fisierele(radacina) if "lectie" in a or "pas" in a]
