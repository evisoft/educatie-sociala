# Manual EPS clasa a IX-a — plan de implementare

> **Pentru agenți executanți:** SUB-SKILL OBLIGATORIU: folosiți `superpowers:subagent-driven-development` (recomandat) sau `superpowers:executing-plans` pentru a implementa acest plan sarcină cu sarcină. Pașii folosesc sintaxa cu casete (`- [ ]`) pentru urmărire.

**Scop:** Un manual pentru elev la *Educație pentru societate*, clasa a IX-a (Republica Moldova) — 34 de lecții în Markdown, conforme curriculumului MECC 2018, cu portofoliul *Dosarul meu de cetățean* ca fir roșu.

**Arhitectură:** Un fișier Markdown per lecție, fiecare cu antet YAML care declară ce acoperă (competențe, descriptori, conținuturi curriculare, fișe de portofoliu). Trei scripturi Python citesc aceste antete și verifică automat, la orice moment, dacă manualul acoperă integral curriculumul, dacă toți cei 40 de descriptori ai clasei a IX-a sunt observabili undeva și dacă volumul lecțiilor stă în limite. Scripturile se scriu **înaintea** conținutului și eșuează până când lecțiile există — este ciclul roșu-verde aplicat unui manual.

**Stiva tehnică:** Markdown; Python 3.12 + PyYAML (deja instalate) pentru verificări; `pdftotext` pentru citirea documentelor normative din `curriculum/`; git.

## Constrângeri globale

Se aplică fiecărei sarcini din plan, fără excepție.

- **Sursa normativă:** Curriculum EPS clasele V–IX, Chișinău 2018, Ordinul MECC nr. 1124 din 20.07.2018. Textul integral: `curriculum/eps_gimnaziu_2018-08-14_curriculum_ghid.txt`.
- **Descriptorii clasei a IX-a:** 40, Tabelul nr. 5 din `curriculum/metodologie_evaluare_descriptori_eps.txt`, liniile 809–901.
- **Fidelitatea față de textul oficial.** Transcrierea este fidelă ca sens și formulare. Documentele ministerului conțin erori de tipar și de scanare (*roluluii*, *instumente*, *influenta*, sedile în loc de virgule); acestea **se corectează**, iar fiecare corectură se consemnează în nota din capul fișierului `verificare/referinta.yaml`. Nicio reformulare, scurtare sau „îmbunătățire" de conținut nu este permisă — doar erori evidente de tipar și normalizarea capitalizării titlurilor.
- **Repartizarea orelor:** 8 + 8 + 11 + 7 = 34. Lecțiile numerotate 0–33.
- **Nicio sursă inventată.** Fiecare sursă din „Dosar de lucru" este reală, cu link și dată de accesare, centralizată în `manual/anexe/surse-si-bibliografie.md`. Artefactele construite pentru lecție (postare fictivă, anunț fabricat) se marchează explicit cu `> **Material construit pentru această lecție.**`.
- **Depersonalizare.** Fără nume de partide sau politicieni în activitate. Se analizează mecanismul, nu persoana.
- **Zero morală explicită.** Manualul pune faptele și întrebarea; concluzia o scrie elevul.
- **Adresare cu „tu"**, la prezent, fraze scurte.
- **Română cu diacritice**, normă academică (*sunt*, *î* din *i*).
- **Fără note, fără teste-grilă.** Curriculumul interzice notarea la această disciplină.
- **Volume:** lecție de conținut 1100–1400 cuvinte; lecție de reflecție 500–700; pas de șantier 600–900; deschidere de unitate ~300.
- **Ora are 45 de minute.** Fiecare segment cronometrat al lecției își declară minutele în text, iar suma lor nu depășește 45 pentru o oră (90 pentru două ore, 135 pentru trei). Se bugetează **tot**, inclusiv ce pare gratuit: prezentarea produselor de grup, trecerea de la lucrul individual la cel în grup, citirea casetelor. O lecție care nu încape în oră îl obligă pe profesor să taie ceva — iar primul lucru tăiat e întotdeauna reflecția, adică exact partea care nu se poate tăia.
- **Lucrul elevului ≥ expunerea, măsurat în minute.** Timpul de expunere nu depășește timpul de lucru efectiv. Măsura e timpul, nu numărul de cuvinte: un dosar de lucru se descrie în trei rânduri și cere douăzeci de minute de analizat, iar o sarcină explicată prolix nu devine prin asta muncă.
- **Lasă aer în oră.** Totalul de 45 de minute e plafonul, nu ținta. Scrie lecțiile la **42–44 de minute**, ca profesorul să aibă marjă pentru ce se lungește la clasă. O lecție bugetată la fix 45 scoate reflecția din oră la prima întârziere.
- **Commit după fiecare sarcină.** Mesaj în română, la imperativ.
- **Procedura standard de lecție** — cei șase pași pe care îi urmează fiecare sarcină din fazele 2–5 sunt enunțați o singură dată, la începutul FAZEI 2. Dacă execuți o sarcină izolat, citește-i acolo înainte de a începe.

---

## Harta fișierelor

```
verificare/
  referinta.yaml          sursa de adevăr: 9 unități de competențe, 18 unități de conținut, 40 descriptori
  fm.py                   citirea antetelor YAML din fișierele de lecție (folosit de celelalte)
  trasabilitate.py        verifică acoperirea curriculumului
  descriptori.py          verifică acoperirea celor 40 de descriptori
  volum.py                verifică volumul pe rubrici
  ruleaza-tot.sh          rulează toate trei

docs/verificare/          rapoartele generate (regenerabile, urmărite în git)

manual/
  00-cuvant-catre-elev.md
  00-cuprins.md
  _template-lectie.md     modelul de la care pleacă fiecare lecție de conținut
  u1-cultura-mediatica/   u1-deschidere.md, l00…l07
  u2-amenintari/          u2-deschidere.md, l08…l15
  u3-santier-integritate/ u3-deschidere.md, p01…p11
  u4-cetatenia-activa/    u4-deschidere.md, l27…l33
  anexe/
    dosarul-meu-de-cetatean.md
    descriptori-clasa-9.md
    glosar.md
    surse-si-bibliografie.md
```

**Responsabilități.** `verificare/` nu știe nimic despre conținut — citește doar antete și numără cuvinte. `manual/anexe/` conține tot ce se repetă (fișe, descriptori, glosar), ca lecțiile să trimită la el în loc să-l dubleze. Fiecare lecție este autonomă: se poate rescrie fără a atinge alta.

---

# FAZA 0 — Infrastructura de verificare

## Sarcina 1: Fișierul de referință și cititorul de antete

**Fișiere:**
- Creează: `verificare/referinta.yaml`
- Creează: `verificare/fm.py`
- Creează: `verificare/test_fm.py`

**Interfețe:**
- Produce: `fm.citeste(cale) -> dict` (antetul YAML al unui fișier, `{}` dacă lipsește); `fm.corp(cale) -> str` (textul de după antet); `fm.toate_lectiile(radacina="manual") -> list[tuple[Path, dict]]`.

- [ ] **Pasul 1: Scrie testul care eșuează**

`verificare/test_fm.py`:

```python
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
```

- [ ] **Pasul 2: Rulează testul, confirmă că eșuează**

Rulează: `python3 verificare/test_fm.py`
Așteptat: `ModuleNotFoundError: No module named 'fm'`

- [ ] **Pasul 3: Scrie `verificare/fm.py`**

```python
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
    return yaml.safe_load(antet) or {} if antet.strip() else {}

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
```

- [ ] **Pasul 4: Rulează testul, confirmă că trece**

Rulează: `python3 verificare/test_fm.py`
Așteptat: `OK — 3 teste trecute`

- [ ] **Pasul 5: Scrie `verificare/referinta.yaml`**

Sursa de adevăr a întregului manual. Transcrisă din curriculum (`curriculum/eps_gimnaziu_2018-08-14_curriculum_ghid.txt`, liniile 570–632) și din Tabelul nr. 5 al metodologiei (`curriculum/metodologie_evaluare_descriptori_eps.txt`, liniile 809–901).

```yaml
unitati_de_competente:
  UC1: Identificarea surselor de informare despre probleme de interes civic.
  UC2: Argumentarea rolului mass-mediei în societatea democratică.
  UC3: Caracterizarea principiilor și valorilor democratice ca bază a funcționării societății contemporane.
  UC4: Exprimarea poziției civice, neacceptând comportamente care contravin principiilor democrației.
  UC5: Determinarea modalităților de implicare activă în instituția de învățământ prin intermediul organelor care îi reprezintă.
  UC6: Evaluarea evenimentelor de actualitate prin prisma funcționării instituțiilor statului.
  UC7: Exprimarea interesului pentru participare la procesul decizional în clasă/școală.
  UC8: Analiza critică a problemelor de integritate în societate.
  UC9: Susținerea principiilor democrației, justiției, echității și a statului de drept.

unitati_de_continut:
  C1: Informarea din diverse surse
  C2: Inteligența mediatică
  C3: Știri veridice/știrile false
  C4: Propagandă și manipulare
  C5: Cultura mediatică în contextul provocărilor sociale
  C6: Apatia cetățeanului de a se implica la viața publică
  C7: Corupție vs integritate
  C8: Traficul de ființe umane
  C9: Viziunile radicaliste
  C10: Populismul
  C11: Șovinism, naționalism vs patriotism
  C12: "Învățarea bazată pe proiect: Elaborarea Codului de integritate al cetățeanului"
  C13: Spiritul civic. Voluntariatul
  C14: Cetățeanul – comunitatea locală/națională
  C15: Cetățeanul Republicii Moldova, al Europei, al lumii
  C16: Mecanismele participării civice, politice
  C17: Pluralism și consens în luarea deciziilor
  C18: Modalități și instrumente de contribuție la procesul decizional în școală și comunitate

descriptori:
  1: Susține că drepturile omului trebuie întotdeauna protejate și respectate
  2: Apără ideea că nimeni nu va fi supus torturii, unei pedepse sau unui tratament inuman sau degradant
  3: Promovează ideea că trebuie să fim toleranți față de credințele diferite pe care le au alte persoane în societate
  4: Exprimă părerea că diversitatea culturală dintr-o societate trebuie să fie valorizată și apreciată
  5: Exprimă părerea că toate persoanele și instituțiile trebuie să se supună și să răspundă în fața legii
  6: Exprimă părerea că trebuie să existe măsuri eficace pentru prevenirea și combaterea tuturor formelor de corupție
  7: Manifestă interes pentru a învăța despre credințele, valorile, tradițiile și viziunile asupra lumii ale altor persoane
  8: Profită de oportunitățile de a întâlni oameni noi
  9: Exprimă respect față de alte persoane ca ființe umane egale
  10: Exprimă atitudini de respect față de persoanele care sunt diferite de sine
  11: Exprimă că este dispus(ă) să se ofere voluntar pentru a-i ajuta pe oamenii din comunitate
  12: Exercită obligațiile și responsabilitățile aferente cetățeniei active la nivel local, național sau global
  13: Își asumă răspunderea pentru propriul comportament
  14: Își realizează sarcinile cât de bine poate
  15: Exprimă încredere în propria abilitate de a înțelege diferite lucruri
  16: Exprimă încredere în propria abilitate de a alege metode potrivite pentru realizarea sarcinilor
  17: Dă dovadă că își poate suspenda temporar judecățile referitoare la alte persoane
  18: Lucrează bine în circumstanțe imprevizibile
  19: Caută să clarifice noile informații întrebând alte persoane atunci când e nevoie
  20: Poate alege materiale, resurse și activități de învățare în mod independent
  21: Poate identifica asemănări și deosebiri între informațiile noi și ceea ce e deja cunoscut
  22: Poate analiza puncte de vedere alternative
  23: Ascultă cu atenție diferite păreri
  24: Acordă o atenție deosebită comportamentului celorlalte persoane
  25: Exprimă compasiune pentru o altă persoană care se simte rănită sau supărată
  26: Când vorbește cu cineva, încearcă să înțeleagă ce simte
  27: Dă dovadă de flexibilitate când se confruntă cu obstacole
  28: Își poate ajusta modul obișnuit de gândire în funcție de nevoi și circumstanțe
  29: Își poate transmite mesajul către ceilalți
  30: Pune întrebări pentru a se implica în conversații
  31: Își împărtășește propriile idei și resurse cu ceilalți
  32: Acceptă responsabilitatea comună pentru munca în colaborare
  33: Poate comunica cu părțile conflictuale în mod respectuos
  34: Poate aborda persoanele implicate într-un conflict într-un mod adecvat
  35: Poate descrie propriile sale motivații
  36: Poate reflecta în mod critic asupra propriilor valori și credințe
  37: Poate explica felul în care tonul vocii, contactul vizual și limbajul corporal pot ajuta comunicarea
  38: Poate reflecta în mod critic asupra felului în care diferiți interlocutori pot percepe sensuri diferite din aceeași informație
  39: Poate descrie diferitele modalități prin care cetățenii pot influența politicile
  40: Poate explica felul în care oamenii se pot proteja și apăra de propagandă

volume:
  continut:  {min: 1100, max: 1400}
  reflectie: {min: 500,  max: 700}
  santier:   {min: 600,  max: 900}
  deschidere: {min: 200, max: 400}

# Tipuri care nu se verifică pe volum (anexele au lungime liberă).
ignora_volum: [anexa]
```

**Lecțiile de două sau trei ore** își declară propriile limite în antet, prin `volum_min` și
`volum_max`; `volum.py` le respectă în locul intervalului standard. Nu există „abatere acceptată
manual" — orice abatere raportată este o abatere reală.

- [ ] **Pasul 6: Verifică faptul că referința se încarcă**

Rulează: `python3 -c "import yaml;r=yaml.safe_load(open('verificare/referinta.yaml',encoding='utf-8'));print(len(r['unitati_de_competente']),len(r['unitati_de_continut']),len(r['descriptori']))"`
Așteptat: `9 18 40`

- [ ] **Pasul 7: Commit**

```bash
git add verificare/
git commit -m "Adaugă referința curriculară și cititorul de antete"
```

---

## Sarcina 2: Verificarea trasabilității curriculare

**Fișiere:**
- Creează: `verificare/trasabilitate.py`
- Creează: `docs/verificare/.gitkeep`

**Interfețe:**
- Consumă: `fm.toate_lectiile()`, `verificare/referinta.yaml`
- Produce: raportul `docs/verificare/trasabilitate.md`; cod de ieșire 1 dacă rămâne ceva neacoperit.

- [ ] **Pasul 1: Rulează verificarea înainte de a o scrie — trebuie să nu existe**

Rulează: `python3 verificare/trasabilitate.py`
Așteptat: `python3: can't open file ... No such file or directory`

- [ ] **Pasul 2: Scrie `verificare/trasabilitate.py`**

```python
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
```

- [ ] **Pasul 3: Rulează, confirmă că eșuează corect (manualul nu există încă)**

Rulează: `mkdir -p manual && python3 verificare/trasabilitate.py; echo "cod ieșire: $?"`
Așteptat: `Fișiere: 0 | ore: 0 | neacoperit: 27 | coduri necunoscute: 0` și `cod ieșire: 1`

Cele 27 de elemente neacoperite sunt 9 unități de competențe + 18 unități de conținut.

Acesta este starea „roșu" a manualului. Va deveni verde abia la ultima lecție scrisă.

- [ ] **Pasul 4: Commit**

```bash
touch docs/verificare/.gitkeep
git add verificare/trasabilitate.py docs/verificare/.gitkeep docs/verificare/trasabilitate.md
git commit -m "Adaugă verificarea trasabilității curriculare"
```

---

## Sarcina 3: Verificarea descriptorilor și a volumului

**Fișiere:**
- Creează: `verificare/descriptori.py`
- Creează: `verificare/volum.py`
- Creează: `verificare/ruleaza-tot.sh`

**Interfețe:**
- Consumă: `fm.toate_lectiile()`, `fm.corp()`, `verificare/referinta.yaml`
- Produce: `docs/verificare/descriptori.md`, `docs/verificare/volum.md`

- [ ] **Pasul 1: Scrie `verificare/descriptori.py`**

```python
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
```

- [ ] **Pasul 2: Scrie `verificare/volum.py`**

```python
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
```

- [ ] **Pasul 3: Scrie `verificare/ruleaza-tot.sh`**

```bash
#!/usr/bin/env bash
# Rulează toate verificările. Cod de ieșire 0 doar dacă toate trec.
set -u
cd "$(dirname "$0")/.."
esec=0
for v in trasabilitate descriptori volum; do
  echo "── $v ──"
  python3 "verificare/$v.py" || esec=1
done
python3 verificare/test_fm.py || esec=1
exit $esec
```

- [ ] **Pasul 4: Rulează totul, confirmă starea „roșu"**

Rulează: `chmod +x verificare/ruleaza-tot.sh && ./verificare/ruleaza-tot.sh; echo "cod ieșire: $?"`
Așteptat: `Descriptori acoperiți: 0/40`, `Abateri de volum: 0`, `OK — 3 teste trecute`, `cod ieșire: 1`

- [ ] **Pasul 5: Commit**

```bash
git add verificare/ docs/verificare/
git commit -m "Adaugă verificarea descriptorilor și a volumului"
```

---

# FAZA 1 — Anexele-schelet

Se scriu întâi, fiindcă de ele atârnă fiecare lecție.

## Sarcina 4: Anexa cu descriptorii clasei a IX-a

**Fișiere:**
- Creează: `manual/anexe/descriptori-clasa-9.md`

**Interfețe:**
- Produce: ancore Markdown `#d1` … `#d40`, către care trimit lecțiile din rubrica *Reflecție*.

- [ ] **Pasul 1: Extrage textul oficial al celor 40 de descriptori**

Rulează: `sed -n '809,901p' curriculum/metodologie_evaluare_descriptori_eps.txt`
Verifică fiecare descriptor față de `verificare/referinta.yaml` — trebuie să fie identici cuvânt cu cuvânt.

- [ ] **Pasul 2: Scrie anexa**

Tabel cu patru coloane: **#**, **Descriptorul oficial** (citat exact, pentru profesor), **Cum sună pentru mine** (reformulare la persoana I, pentru elev), **Unde arăt asta** (fișele din dosar — se completează pe măsură ce lecțiile se scriu; la această sarcină rămâne coloana pregătită, cu liniuță).

Reformularea la persoana I este esențială: elevul se autoevaluează pe ea, nu pe limbajul administrativ. Exemple obligatorii:

| # | Oficial | Cum sună pentru mine |
|---|---|---|
| 6 | Exprimă părerea că trebuie să existe măsuri eficace pentru prevenirea și combaterea tuturor formelor de corupție | Pot spune de ce corupția strică viața tuturor, nu doar a celor prinși |
| 22 | Poate analiza puncte de vedere alternative | Pot explica un punct de vedere cu care nu sunt de acord, fără să-l caricaturizez |
| 39 | Poate descrie diferitele modalități prin care cetățenii pot influența politicile | Știu cel puțin trei căi prin care un om ca mine poate schimba o decizie |
| 40 | Poate explica felul în care oamenii se pot proteja și apăra de propagandă | Pot arăta cuiva cum să verifice o știre înainte s-o creadă |

Antet YAML: `tip: anexa` (fără câmpul `lectie`, ca să nu fie numărat de `trasabilitate.py`).

Text introductiv, ~150 de cuvinte, care îi explică elevului: la această disciplină nu se pun note; cei 40 de descriptori acoperă 20 de competențe, câte doi de fiecare, iar cei doi sunt **căi alternative** — îți ajunge unul singur ca să arăți că ai competența; la sfârșitul anului se numără **câte competențe din 20** ai format, iar de acolo rezultă calificativul (16–20 foarte bine, 11–15 bine, 5–10 suficient); dosarul este locul unde le arăți.

Această regulă vine din Metodologia de evaluare prin descriptori, pct. 28–32, și trebuie respectată exact — nu se numără descriptorii bifați din 40.

- [ ] **Pasul 3: Verifică**

Rulează: `python3 -c "
import re,yaml
t=open('manual/anexe/descriptori-clasa-9.md',encoding='utf-8').read()
r=yaml.safe_load(open('verificare/referinta.yaml',encoding='utf-8'))['descriptori']
lipsa=[n for n,x in r.items() if x not in t]
print('descriptori cu text lipsă sau modificat:', lipsa or 'niciunul')
"`
Așteptat: `descriptori cu text lipsă sau modificat: niciunul`

- [ ] **Pasul 4: Commit**

```bash
git add manual/anexe/descriptori-clasa-9.md
git commit -m "Adaugă anexa cu cei 40 de descriptori ai clasei a IX-a"
```

---

## Sarcina 5: Anexa „Dosarul meu de cetățean"

**Fișiere:**
- Creează: `manual/anexe/dosarul-meu-de-cetatean.md`

**Interfețe:**
- Produce: ancorele `#f1` … `#f23`, către care trimite rubrica *Dosarul meu de cetățean* din fiecare lecție.

- [ ] **Pasul 1: Scrie deschiderea dosarului (~250 de cuvinte)**

I se explică elevului, cu „tu": ce este dosarul, de ce îl ține el și nu profesorul, ce se întâmplă cu el la sfârșitul anului, și că fișele F9 și F11 vor fi materia primă din care echipa lui va scrie Codul de integritate. F21 nu intră aici: ea se completează abia la lecțiile 29–31, după ce Codul e gata, și are alt rol — oglinda de după, în care elevul află pe ce ușă ar putea intra, în realitate, documentul pe care l-a produs. Fără limbaj administrativ — nu „portofoliu de evaluare", ci „dosarul tău".

- [ ] **Pasul 2: Scrie cele 23 de fișe**

Fiecare fișă: titlu, lecția din care provine, **ce conține** (2–3 rânduri), **spațiul de completat** (tabel, listă de întrebări sau machetă concretă — nu doar o instrucțiune), și subsolul cu descriptorii pe care îi face vizibili.

| Fișa | Titlu | Din lecția |
|---|---|---|
| F1 | Harta surselor mele | 1 |
| F2 | Anatomia unui mesaj de propagandă | 2–3 |
| F3 | Jurnalul de verificare (3 știri) | 4 |
| F4 | Ce nu ajunge știre | 5 |
| F5 | Regulile mele de igienă informațională | 6 |
| F6 | Termometrul democrației | 8 |
| F7 | Disecția unui discurs | 9–10 |
| F8 | Scara radicalizării | 11 |
| F9 | Harta integrității în comunitatea mea | 12 |
| F10 | Semnele de alarmă — fișă de siguranță | 13 |
| F11 | Ce s-a decis fără mine anul acesta | 14 |
| F12 | Întrebarea de cercetare a echipei | pasul 1 |
| F13 | Instrumentul de culegere | pasul 2 |
| F14 | Datele brute | pasul 3 |
| F15 | Ce ne spun datele | pasul 4 |
| F16 | Codul, versiunea 1 | pașii 5–6 |
| F17 | Feedback din audiere | pasul 10 |
| F18 | Codul, versiunea finală | pasul 10 |
| F19 | Profilul meu de voluntar | 27 |
| F20 | Cercurile mele de apartenență | 28 |
| F21 | Harta deciziei în școala mea | 29–31 |
| F22 | Angajamentul meu pe trei luni | 29–31 |
| F23 | Scrisoare către mine, cel din clasa a V-a | 33 |

**F10 are un regim special.** Este fișă de siguranță, nu de reflecție: conține semnele de alarmă ale unei oferte de muncă înșelătoare, întrebările pe care le pune cineva înainte să plece, și **numerele reale de ajutor**, cu instituția care le deține. La această sarcină se lasă marcajul `> [DE VERIFICAT ÎNAINTE DE PUBLICARE: numerele și instituțiile]` — se completează la Sarcina 19, când se scrie lecția 13, după verificarea la sursă.

- [ ] **Pasul 3: Verifică ancorele**

Rulează: `grep -c '^### F' manual/anexe/dosarul-meu-de-cetatean.md`
Așteptat: `23`

- [ ] **Pasul 4: Commit**

```bash
git add manual/anexe/dosarul-meu-de-cetatean.md
git commit -m "Adaugă structura Dosarului meu de cetățean (23 de fișe)"
```

---

## Sarcina 6: Modelul de lecție

**Fișiere:**
- Creează: `manual/_template-lectie.md`

Toate sarcinile de lecție care urmează pornesc de la acest fișier. El nu este un placeholder: este artefactul real pe care se calchiază cele 34 de lecții.

- [ ] **Pasul 1: Scrie modelul**

```markdown
---
unitate: 0
lectie: 0
tip: continut            # continut | reflectie | santier | deschidere | anexa
titlu: ""
ore: 1
competente: []           # numere din cele 20 de competențe CDC
descriptori: []          # numere din cei 40 de descriptori ai clasei a IX-a
unitati_competenta: []   # coduri UC1…UC9 din verificare/referinta.yaml
continut_curricular: []  # coduri C1…C18 din verificare/referinta.yaml
fise: []                 # F1…F23
---

# Lecția N. Titlul

> **Întrebarea lecției:** …

## Deschidere

*(80–120 de cuvinte. O situație, trei titluri, o fotografie, o cifră care nu se potrivește. Fără explicații — doar întrebarea.)*

## De reținut

*(400–600 de cuvinte. Noțiunile și mecanismul. Nu concluzia morală.)*

> **Cuvinte de care ai nevoie**
> **termen** — definiție scurtă.

## Dosar de lucru

**Sursa A.** …
*(sursă reală: publicație, titlu, link, data accesării — sau, dacă e artefact construit: `> **Material construit pentru această lecție.**`)*

**Grila de analiză**

| Întrebare | Sursa A | Sursa B |
|---|---|---|

## Sarcină de grup

*(15–20 de minute. Produs concret, roluri distribuite. Nu „discutați despre", ci „produceți X".)*

## Dosarul meu de cetățean

Completează [Fișa FN — Titlu](../anexe/dosarul-meu-de-cetatean.md#fn).

## Reflecție

1. …
2. …

**Autoevaluare:** [descriptorii N, M](../anexe/descriptori-clasa-9.md#dn).
```

**Convenția de nume:** fișierele din `manual/` al căror nume începe cu `_` sunt unelte de lucru, nu părți din manual. `fm.toate_fisierele()` le sare, deci modelul nu e numărat nici ca lecție, nici la ore, nici la volum. Fără această regulă, manualul n-ar putea ajunge niciodată la 34 de ore fix.

- [ ] **Pasul 2: Verifică faptul că modelul se parsează**

Rulează: `python3 -c "import sys;sys.path.insert(0,'verificare');import fm;print(fm.citeste('manual/_template-lectie.md'))"`
Așteptat: un dicționar cu cheile `unitate`, `lectie`, `tip`, `titlu`, `ore`, `competente`, `descriptori`, `unitati_competenta`, `continut_curricular`, `fise`.

- [ ] **Pasul 3: Commit**

```bash
git add manual/_template-lectie.md
git commit -m "Adaugă modelul de lecție"
```

---

# FAZA 2 — Unitatea I. Cultura mediatică (8 ore)

**Procedura pentru fiecare lecție din fazele 2–5**, identică:

1. Copiază `manual/_template-lectie.md` la calea indicată.
2. Completează antetul YAML **exact** cum e dat în sarcină.
3. Rulează `python3 verificare/trasabilitate.py` — numărul de „neacoperit" trebuie să scadă. Aceasta este verificarea roșu→verde a lecției.
4. Caută și **verifică efectiv** sursele (deschide linkurile, confirmă cifrele). Adaugă-le în `manual/anexe/surse-si-bibliografie.md`.
5. Scrie conținutul, respectând volumele.
6. Rulează `./verificare/ruleaza-tot.sh` — volumul lecției trebuie să iasă „bine".
7. Commit.

## Sarcina 7: Deschiderea unității I și lecția 0

**Fișiere:**
- Creează: `manual/u1-cultura-mediatica/u1-deschidere.md`
- Creează: `manual/u1-cultura-mediatica/l00-deschidere-an.md`

**Antet — deschiderea de unitate:**
```yaml
unitate: 1
tip: deschidere
titlu: "Cultura mediatică"
```
Întrebarea mare a unității: *Cum știu că ceea ce citesc e adevărat?* Ce va ști și ce va produce elevul la finalul celor opt ore. Fișele F1–F5. ~300 de cuvinte.

**Antet — lecția 0:**
```yaml
unitate: 1
lectie: 0
tip: continut
titlu: "Ce facem anul acesta și ce e Dosarul meu de cetățean"
ore: 1
competente: [8, 10, 18]
descriptori: [15, 20, 35]
unitati_competenta: []
continut_curricular: []
fise: []
```

Lecția 0 **nu declară** unități de competențe sau de conținut: e o oră de deschidere, nu predă *Informarea din diverse surse*. UC1 și C1 sunt acoperite de lecția 1, care chiar le predă. O acoperire declarată acolo unde nu se învață nimic face trasabilitatea decorativă.

Câmpul `competente` listează competențele cărora le aparțin descriptorii declarați: descriptorul 15 e al competenței 8, 20 al competenței 10, 35 al competenței 18.

Conținut: reflecție asupra a ce a rămas din clasa a VIII-a (activitatea *Cele patru cadrane*, din Ghidul profesorului); prezentarea celor patru unități; **prezentarea dosarului** — ce e, de ce îl ține el, ce se întâmplă cu el la final; citirea împreună a câtorva descriptori din anexă, în varianta „cum sună pentru mine".

- [ ] **Pasul 1:** Creează cele două fișiere din model, cu antetele de mai sus.
- [ ] **Pasul 2:** Rulează `python3 verificare/trasabilitate.py`. Așteptat: `Fișiere: 1 | ore: 1 | neacoperit: 27` — lecția 0 nu acoperă nimic din curriculum, și e corect așa. (Deschiderea de unitate nu are câmpul `lectie`, deci nu e numărată aici — dar `volum.py` o verifică.)
- [ ] **Pasul 3:** Scrie conținutul ambelor fișiere.
- [ ] **Pasul 4:** Rulează `./verificare/ruleaza-tot.sh`. Volumul ambelor fișiere: „bine".
- [ ] **Pasul 5:** Commit: `git add manual/u1-cultura-mediatica/ && git commit -m "Adaugă deschiderea unității I și lecția 0"`

---

## Sarcina 8: Lecția 1 — De unde aflu ce se întâmplă

**Fișier:** `manual/u1-cultura-mediatica/l01-surse-de-informare.md`

```yaml
unitate: 1
lectie: 1
tip: continut
titlu: "De unde aflu ce se întâmplă. Sursele mele de informare"
ore: 1
competente: [11, 20]
descriptori: [19, 21, 22]
unitati_competenta: [UC1, UC2]
continut_curricular: [C1, C2]
fise: [F1]
```

**Întrebarea lecției:** De unde aflu, de fapt, ce se întâmplă în lume — și cine a ales asta pentru mine?

**Deschidere:** elevul își reconstituie ultimele trei lucruri pe care le-a aflat azi și de unde. Aproape sigur: dintr-un feed algoritmic. Întrebarea: cine a decis ce vezi?

**De reținut:** tipuri de surse (media instituțională, rețele sociale, mesagerie, gura lumii); ce înseamnă redacție, verificare, răspundere editorială; ce este un algoritm de recomandare și de ce nu-ți arată „tot"; diferența dintre a fi informat și a fi expus.

**Surse de găsit și verificat:**
- Un fragment din **Codul serviciilor media audiovizuale al RM (nr. 174/2018)** privind obligațiile de informare corectă — găsește articolul exact pe `legis.md` și citează-l verbatim, cu numărul articolului.
- Datele cele mai recente ale unui **barometru de opinie publică** din RM privind sursele de informare ale populației (IPP publică periodic) — cifră exactă, an, link, dată de accesare.
- Captura unui feed (artefact construit — marchează-l ca atare).

**Sarcină de grup:** fiecare grup primește același eveniment relatat de trei tipuri de surse și completează cine spune ce, ce lipsește din fiecare.

**F1 — Harta surselor mele:** inventarul propriu, pe o săptămână, cu coloană „cine răspunde dacă e greșit".

- [ ] **Pasul 1:** Creează fișierul cu antetul de mai sus.
- [ ] **Pasul 2:** `python3 verificare/trasabilitate.py` → `neacoperit: 23`.
- [ ] **Pasul 3:** Găsește și verifică sursele; adaugă-le în `manual/anexe/surse-si-bibliografie.md`.
- [ ] **Pasul 4:** Scrie lecția.
- [ ] **Pasul 5:** `./verificare/ruleaza-tot.sh` → volum „bine".
- [ ] **Pasul 6:** Commit: `git commit -am "Adaugă lecția 1 — sursele de informare"`

---

## Sarcina 9: Lecțiile 2–3 — Propaganda și manipularea

**Fișier:** `manual/u1-cultura-mediatica/l02-03-propaganda-manipulare.md`

```yaml
unitate: 1
lectie: 2
tip: continut
titlu: "Propaganda și manipularea"
ore: 2
competente: [11, 19, 20]
descriptori: [22, 38, 40]
unitati_competenta: [UC2, UC6]
continut_curricular: [C4, C5]
fise: [F2]
```



**Întrebarea lecției:** Cum arată un mesaj construit ca să mă facă să simt ceva anume?

**De reținut:** definiția propagandei (mesaj construit pentru a obține adeziune, nu pentru a informa); tehnicile — apel la frică, dușmanul comun, repetiția, falsa alternativă, autoritatea fabricată, whataboutism-ul; diferența dintre propagandă, publicitate și jurnalism; de ce propaganda funcționează mai bine când confirmă ce credeai deja.

**Studiul de caz central: dezinformarea legată de războiul din Ucraina și de spațiul media rusesc.** Se lucrează pe **narative documentate**, nu pe apartenență lingvistică. Surse de găsit:
- rapoarte publice ale **stopfals.md / Asociația Presei Independente** privind narative de dezinformare identificate în spațiul informațional din RM — citează narativul și raportul, cu link și dată;
- decizii publice ale **Consiliului Audiovizualului al RM** privind încălcarea obligației de informare corectă — număr de decizie, dată, link.

> Nicio formulare care să asocieze propaganda cu limba vorbită de elevi. Se analizează tehnica, nu vorbitorul. Lecția trebuie să funcționeze la fel de bine pentru un elev vorbitor de rusă.

**Sarcină de grup (ora 2):** fiecare grup primește același eveniment banal și îl transformă într-un reportaj de propagandă, folosind trei tehnici la alegere; celelalte grupuri identifică tehnicile.

**F2 — Anatomia unui mesaj de propagandă:** grila cu tehnicile, aplicată pe un mesaj găsit de elev.

- [ ] **Pasul 1:** Creează fișierul cu antetul de mai sus.
- [ ] **Pasul 2:** `python3 verificare/trasabilitate.py` → `neacoperit: 20`.
- [ ] **Pasul 3:** Găsește și verifică sursele; adaugă-le în bibliografie.
- [ ] **Pasul 4:** Scrie lecția (2200–2800 de cuvinte).
- [ ] **Pasul 5:** `./verificare/ruleaza-tot.sh`; verifică raportul de descriptori — 40 trebuie să apară acum acoperit.
- [ ] **Pasul 6:** Commit: `git commit -am "Adaugă lecțiile 2-3 — propaganda și manipularea"`

---

## Sarcina 10: Lecția 4 — Știri veridice, știri false

**Fișier:** `manual/u1-cultura-mediatica/l04-stiri-veridice-false.md`

```yaml
unitate: 1
lectie: 4
tip: continut
titlu: "Știri veridice, știri false"
ore: 1
competente: [11, 20]
descriptori: [21, 22, 40]
unitati_competenta: [UC1, UC2]
continut_curricular: [C3]
fise: [F3]
```

**Întrebarea lecției:** Cum verific o știre în cinci minute, cu telefonul din mână?

**De reținut:** ce face o știre verificabilă — sursa, data, autorul, dovada; diferența dintre eroare, exagerare și minciună deliberată; ce este clickbait-ul; de ce o știre falsă circulă mai repede decât dezmințirea ei.

**Dosar de lucru:** același subiect în trei forme — postare pe rețea (artefact construit, marcat), articol de presă (real, cu link), comunicatul instituției (real). Grila de verificare în șase întrebări.

**Sarcină de grup:** fiecare grup primește o știre și o clasează: veridică / parțial adevărată / falsă, cu argumentul scris.

**F3 — Jurnalul de verificare:** trei știri verificate de elev, cu traseul verificării.

- [ ] **Pasul 1:** Creează fișierul cu antetul de mai sus.
- [ ] **Pasul 2:** `python3 verificare/trasabilitate.py` → `neacoperit: 19`.
- [ ] **Pasul 3:** Găsește și verifică sursele.
- [ ] **Pasul 4:** Scrie lecția.
- [ ] **Pasul 5:** `./verificare/ruleaza-tot.sh`.
- [ ] **Pasul 6:** Commit: `git commit -am "Adaugă lecția 4 — știri veridice și știri false"`

---

## Sarcina 11: Lecția 5 — Cetățeanul în fața mass-mediei

**Fișier:** `manual/u1-cultura-mediatica/l05-cetateanul-si-massmedia.md`

```yaml
unitate: 1
lectie: 5
tip: continut
titlu: "Cetățeanul în fața mass-mediei"
ore: 1
competente: [7, 11, 20]
descriptori: [13, 22, 24]
unitati_competenta: [UC2, UC6]
continut_curricular: [C2, C5]
fise: [F4]
```

**Întrebarea lecției:** Ce nu ajunge niciodată știre — și de ce contează asta?

**De reținut:** ce face un subiect „demn de știre" și ce rămâne pe dinafară; responsabilitatea celui care distribuie, nu doar a celui care publică; dreptul la replică și la viață privată; ce poate face un cetățean când o publicație greșește (autosesizare, petiție la Consiliul Audiovizualului, drept la replică).

**Surse de găsit:** procedura reală de sesizare a Consiliului Audiovizualului al RM (de pe site-ul instituției, cu link și dată); un cod deontologic al jurnalistului din RM (Consiliul de Presă) — fragment citat exact.

**Sarcină de grup:** grupurile inventariază, timp de 10 minute, ce s-a întâmplat în ultima lună în localitatea lor și nu a ajuns în nicio știre; formulează un subiect de reportaj.

**F4 — Ce nu ajunge știre.**

- [ ] **Pasul 1–6:** Aceeași procedură. După pasul 2, așteptat: `neacoperit: 19`.
- [ ] Commit: `git commit -am "Adaugă lecția 5 — cetățeanul în fața mass-mediei"`

---

## Sarcina 12: Lecția 6 — Cum mă apăr

**Fișier:** `manual/u1-cultura-mediatica/l06-cum-ma-apar.md`

```yaml
unitate: 1
lectie: 6
tip: continut
titlu: "Cum mă apăr: verificare, surse, gândire lentă"
ore: 1
competente: [11, 18, 20]
descriptori: [22, 36, 40]
unitati_competenta: [UC1, UC2]
continut_curricular: [C2, C5]
fise: [F5]
```

**Întrebarea lecției:** Ce fac, concret, când un mesaj mă face să simt imediat furie sau frică?

**De reținut:** de ce emoția puternică e semnalul de alarmă, nu dovada; teoriile conspirației — de ce sunt atrăgătoare (explică tot, nu se pot infirma, dau senzația de a fi printre puținii care știu); tehnici practice: căutarea inversă a imaginii, verificarea datei, căutarea sursei primare, regula celor două surse independente; gândirea lentă ca deprindere, nu ca talent.

**Sarcină de grup:** fiecare grup redactează trei reguli de igienă informațională pentru un elev de clasa a V-a; clasa alege regulile care intră în lista comună.

**F5 — Regulile mele de igienă informațională.**

- [ ] **Pasul 1–6:** Aceeași procedură. După pasul 2, așteptat: `neacoperit: 19` (fără scădere — conținuturile C2 și C5 sunt deja acoperite; asta e corect și așteptat).
- [ ] Commit: `git commit -am "Adaugă lecția 6 — cum mă apăr de manipulare"`

---

## Sarcina 13: Lecția 7 — Reflecție asupra unității I

**Fișier:** `manual/u1-cultura-mediatica/l07-reflectie.md`

```yaml
unitate: 1
lectie: 7
tip: reflectie
titlu: "Reflecție asupra unității"
ore: 1
competente: [10, 18]
descriptori: [15, 35, 36]
unitati_competenta: [UC1]
continut_curricular: [C5]
fise: []
```

**Structură** (500–700 de cuvinte, nu cele șapte rubrici): recitirea fișelor F1–F5; harta mentală *Ce știu acum despre informație și nu știam în septembrie*; trei întrebări de bilanț; grila de autoevaluare pe descriptorii unității (15, 19, 20, 21, 22, 24, 35, 36, 38, 40) — elevul bifează ce poate arăta și **indică unde**, în dosar.

- [ ] **Pasul 1:** Creează fișierul cu antetul de mai sus.
- [ ] **Pasul 2:** `python3 verificare/volum.py` → lecția apare cu tipul `reflectie` și intervalul 500–700.
- [ ] **Pasul 3:** Scrie lecția.
- [ ] **Pasul 4:** `./verificare/ruleaza-tot.sh`.
- [ ] **Pasul 5:** Commit: `git commit -am "Adaugă lecția 7 — reflecție asupra unității I"`

---

## Sarcina 14: Poarta de calitate a unității I

Prima unitate întreagă e scrisă. Aici se validează anatomia **înainte** de a o repeta de încă 26 de ori.

- [ ] **Pasul 1: Rulează toate verificările**

Rulează: `./verificare/ruleaza-tot.sh`
Așteptat: 7 fișiere de lecție, 8 ore, conținuturile C1–C5 acoperite, volumele „bine".

- [ ] **Pasul 2: Verificarea limbii**

Trece fiecare fișier din `manual/u1-cultura-mediatica/` prin skill-ul `profesor-roman`. Corectează ce semnalează.

- [ ] **Pasul 3: Verificarea surselor**

Deschide fiecare link din `manual/anexe/surse-si-bibliografie.md`. Confirmă că pagina există, că textul citat apare acolo și că cifrele coincid. Orice sursă care nu trece: se înlocuiește sau se elimină, și lecția se ajustează.

- [ ] **Pasul 4: Citire ca elev**

Citește cele 8 lecții cap-coadă și verifică: apare undeva o concluzie morală pe care ar fi trebuit s-o formuleze elevul? Există vreo sarcină formulată ca „discutați despre"? Există vreo lecție în care „De reținut" a crescut pe seama „Dosarului de lucru"? Corectează.

- [ ] **Pasul 5: Decizia asupra anatomiei**

Dacă cele șapte rubrici s-au dovedit strâmte sau prea largi, **acum** se modifică `manual/_template-lectie.md` și volumele din `verificare/referinta.yaml`, și se retușează unitatea I. După acest punct, anatomia este înghețată.

- [ ] **Pasul 6: Commit**

```bash
git add -A
git commit -m "Închide unitatea I: verificări, corecturi de limbă, validarea surselor"
```

---

# FAZA 3 — Unitatea II. Amenințări la adresa democrației (8 ore)

Aceeași procedură în șase pași ca la faza 2, pentru fiecare lecție.

## Sarcina 15: Deschiderea unității II și lecția 8 — Democrația și cultura democratică

**Fișiere:** `manual/u2-amenintari/u2-deschidere.md`, `manual/u2-amenintari/l08-democratia.md`

Deschiderea de unitate: întrebarea mare *Ce slăbește o democrație din interior?*; fișele F6–F11; ~300 de cuvinte.

```yaml
unitate: 2
lectie: 8
tip: continut
titlu: "Democrația și cultura democratică"
ore: 1
competente: [3, 11, 20]
descriptori: [5, 9, 22]
unitati_competenta: [UC3, UC9]
continut_curricular: [C6]
fise: [F6]
```

**Întrebarea lecției:** Ce trebuie să existe într-o țară ca să spunem că e democratică — pe lângă alegeri?

**De reținut:** alegeri libere, separația puterilor, supremația legii, presă liberă, drepturi ale minorității, societate civilă; distincția dintre **instituții** democratice și **cultură** democratică (ce fac oamenii zilnic); de ce democrația se poate goli pe dinăuntru păstrând forma.

**Surse:** Constituția RM, titlul I — articolele privind statul de drept și pluralismul politic, citate exact, cu numărul articolului (`legis.md`). Un indice internațional public de măsurare a democrației, cu poziția RM, anul și metodologia numite explicit.

**F6 — Termometrul democrației:** criteriile, aplicate de elev pe o situație din școala lui.

- [ ] **Pașii 1–6:** procedura standard. După pasul 2, așteptat: `neacoperit: 16`.
- [ ] Commit: `git commit -am "Adaugă deschiderea unității II și lecția 8"`

---

## Sarcina 16: Lecțiile 9–10 — Populism, naționalism, șovinism

**Fișier:** `manual/u2-amenintari/l09-10-populism-nationalism.md`

```yaml
unitate: 2
lectie: 9
tip: continut
titlu: "Populism, naționalism, șovinism — și ce e, de fapt, patriotismul"
ore: 2
volum_min: 2200
volum_max: 2800
competente: [2, 4, 11]
descriptori: [4, 7, 10, 17, 22]
unitati_competenta: [UC3, UC4, UC6]
continut_curricular: [C10, C11]
fise: [F7]
```

Volum: 2200–2800 de cuvinte.

**Întrebarea lecției:** Când iubirea de țară devine ură de altul?

**De reținut:** anatomia discursului populist — „poporul curat" contra „elitei corupte", soluția simplă la problema complexă, ostilitatea față de instituțiile care limitează puterea; distincția patriotism / naționalism / șovinism, cu exemple de comportament, nu de etichetă; de ce populismul câștigă când instituțiile chiar au dezamăgit — fără a-l scuza.

**Regula de aur a acestei lecții:** patriotismul **nu** se prezintă ca versiunea „bună" a naționalismului într-un tabel moralizator. Se dau comportamente concrete și elevul le clasează singur.

**Surse:** un discurs public real, depersonalizat (fără autor numit), din care se extrag structurile; un fragment din Constituția RM privind interzicerea instigării la ură (articol exact).

**Sarcină de grup (ora 2):** grupurile primesc șase enunțuri despre țară și le așază pe o axă de la „mă face să vreau să construiesc ceva" la „mă face să vreau să resping pe cineva"; argumentează plasarea.

**F7 — Disecția unui discurs.**

- [ ] **Pașii 1–6:** procedura standard. După pasul 2, așteptat: `neacoperit: 13`.
- [ ] Commit: `git commit -am "Adaugă lecțiile 9-10 — populism, naționalism, șovinism"`

---

## Sarcina 17: Lecția 11 — Viziunile radicaliste

**Fișier:** `manual/u2-amenintari/l11-viziuni-radicaliste.md`

```yaml
unitate: 2
lectie: 11
tip: continut
titlu: "Viziunile radicaliste"
ore: 1
competente: [1, 5, 11]
descriptori: [1, 2, 9, 22]
unitati_competenta: [UC4, UC9]
continut_curricular: [C9]
fise: [F8]
```

**Întrebarea lecției:** Cum ajunge cineva să creadă că violența e singura soluție?

**De reținut:** radicalizarea ca proces, nu ca trăsătură de caracter — nemulțumire reală → explicație simplă → comunitate care o confirmă → dușman identificat → izolarea de restul → justificarea violenței; rolul mediului online în accelerarea traseului; ce oprește procesul (relații în afara grupului, întrebări la care grupul nu răspunde).

**Protocol de siguranță:** fără detalii operaționale, fără propagandă reproduce, fără nume de grupări. Lecția se încheie cu ce poate face un elev care observă un prieten alunecând — nu cu frica.

**Sarcină de grup:** grupurile reconstituie traseul unui personaj fictiv pe cele șase trepte și identifică, la fiecare treaptă, ce l-ar fi putut opri.

**F8 — Scara radicalizării.**

- [ ] **Pașii 1–6:** procedura standard. După pasul 2, așteptat: `neacoperit: 12`.
- [ ] Commit: `git commit -am "Adaugă lecția 11 — viziunile radicaliste"`

---

## Sarcina 18: Lecția 12 — Corupție și integritate

**Fișier:** `manual/u2-amenintari/l12-coruptie-integritate.md`

```yaml
unitate: 2
lectie: 12
tip: continut
titlu: "Corupție și integritate"
ore: 1
competente: [3, 7, 11]
descriptori: [5, 6, 13, 22]
unitati_competenta: [UC8, UC9]
continut_curricular: [C7]
fise: [F9]
```

**Întrebarea lecției:** Cine plătește, de fapt, când cineva „aranjează" ceva?

**De reținut:** formele corupției (mită, trafic de influență, favoritism, conflict de interese, „cadoul" care nu e cadou); de ce corupția mică o pregătește pe cea mare; ce înseamnă integritate ca deprindere zilnică; de ce „toți fac așa" este mecanismul care o susține.

**Surse:** legislația RM privind integritatea în sectorul public — articolele care definesc conflictul de interese și cadourile inadmisibile, citate exact (`legis.md`); datele publice ale unui barometru de percepție a corupției, cu anul și metodologia numite.

**Sarcină de grup:** patru situații ambigue din viața școlii; grupurile decid dacă e sau nu problemă de integritate și de ce. **Caseta *Aici nu există un singur răspuns* este obligatorie** — cel puțin una dintre situații trebuie să rămână genuin discutabilă.

**F9 — Harta integrității în comunitatea mea.** Fișă esențială: este una dintre cele trei surse de date pentru unitatea III. Elevul identifică locurile din comunitatea lui unde apar riscuri de integritate și cum se manifestă.

- [ ] **Pașii 1–6:** procedura standard. După pasul 2, așteptat: `neacoperit: 10`.
- [ ] Commit: `git commit -am "Adaugă lecția 12 — corupție și integritate"`

---

## Sarcina 19: Lecția 13 — Traficul de ființe umane

**Fișier:** `manual/u2-amenintari/l13-traficul-de-fiinte-umane.md`

Lecția care lipsește din Ghidul profesorului. Se scrie cu cea mai mare grijă din tot manualul.

```yaml
unitate: 2
lectie: 13
tip: continut
titlu: "Nimeni nu pleacă crezând că i se va întâmpla"
ore: 1
competente: [1, 3, 7, 11]
descriptori: [1, 2, 13, 25]
unitati_competenta: [UC4, UC9]
continut_curricular: [C8]
fise: [F10]
```

**Întrebarea lecției:** Cum ajunge un om, fără să fie răpit, să-și piardă libertatea?

**Deschidere:** anunțul de angajare prea bun ca să fie adevărat (artefact construit, marcat ca atare). *Ce te-ar face să spui „da"? Ce te-ar face să te oprești?*

**De reținut:** traficul nu începe cu un răpitor, ci cu o ofertă bună și o nevoie reală; cele trei elemente ale definiției juridice — acțiunea, mijlocul, scopul exploatării; de ce consimțământul inițial nu contează juridic; formele (muncă forțată, exploatare sexuală, cerșetorie organizată, prelevare de organe); cine e vulnerabil și de ce vulnerabilitatea nu e vină.

**Protocol obligatoriu:**
- fără detalii grafice, fără povești de victimizare spuse pentru efect;
- **nicio formulare care să pună vina pe victimă** — verifică fiecare frază din acest unghi;
- lecția se încheie cu ce se poate face concret, nu cu frica;
- se menționează explicit că victima nu e pedepsită pentru actele comise sub constrângere.

**Surse de găsit și verificat obligatoriu la sursă:**
- **Legea RM nr. 241/2005** privind prevenirea și combaterea traficului de ființe umane — definiția, citată exact, cu articolul (`legis.md`);
- **Codul penal al RM**, articolele privind traficul de ființe umane și traficul de copii — numerele exacte;
- datele publice ale **Centrului pentru combaterea traficului de persoane** sau ale raportului național anual — cifre cu an și link.

**Numerele de ajutor** (F10 și lecție): se preiau **de pe site-ul instituției care le deține**, se notează instituția lângă număr, iar în bibliografie se trece data verificării. **Nu se scriu din memorie.** Dacă un număr nu poate fi confirmat, nu intră în manual.

**Sarcină de grup:** grupurile primesc trei oferte de muncă în străinătate și formulează, pentru fiecare, cele cinci întrebări pe care le-ar pune înainte de plecare și cele trei verificări pe care le-ar face.

**F10 — Semnele de alarmă, fișă de siguranță:** semnele ofertei înșelătoare; ce verifici înainte să pleci (contract, angajator, adresă reală, cine știe unde ești); ce faci dacă ești deja acolo; numerele reale, cu instituția.

- [ ] **Pasul 1:** Creează fișierul cu antetul de mai sus.
- [ ] **Pasul 2:** `python3 verificare/trasabilitate.py` → `neacoperit: 9`. C8 apare acum acoperit — golul din Ghidul profesorului e închis.
- [ ] **Pasul 3:** Găsește textele de lege și confirmă numerele de articol la sursă.
- [ ] **Pasul 4:** Confirmă numerele de ajutor pe site-urile instituțiilor; completează F10 în `dosarul-meu-de-cetatean.md` și elimină marcajul `[DE VERIFICAT ÎNAINTE DE PUBLICARE]`.
- [ ] **Pasul 5:** Scrie lecția.
- [ ] **Pasul 6:** Recitire dedicată, doar pentru protocol: caută în text orice frază care ar putea fi citită ca vină pusă pe victimă. Rescrie.
- [ ] **Pasul 7:** `./verificare/ruleaza-tot.sh`.
- [ ] **Pasul 8:** Commit: `git commit -am "Adaugă lecția 13 — traficul de ființe umane (lecția lipsă din ghid)"`

---

## Sarcina 20: Lecția 14 — Apatia cetățeanului

**Fișier:** `manual/u2-amenintari/l14-apatia.md`

```yaml
unitate: 2
lectie: 14
tip: continut
titlu: "Apatia cetățeanului: costul neimplicării"
ore: 1
competente: [6, 8, 20]
descriptori: [12, 15, 39]
unitati_competenta: [UC4, UC6, UC7]
continut_curricular: [C6]
fise: [F11]
```

**Întrebarea lecției:** Ce se decide despre mine când eu nu sunt în sală?

**De reținut:** de ce oamenii nu se implică (senzația că nu contează, lipsa de timp, neîncrederea, costul personal); ce se întâmplă când o minoritate activă decide pentru o majoritate pasivă; votul ca instrument, nu ca ritual; formele de participare între alegeri (petiție, consultare publică, audiere, consiliul elevilor, ședința publică a consiliului local).

**Surse:** procedura reală de consultare publică a autorităților din RM (Legea privind transparența în procesul decizional — articolul exact); datele reale de prezență la ultimele alegeri locale din RM, pe grupa de vârstă tânără, cu sursa oficială.

**Sarcină de grup:** grupurile identifică o decizie luată în școală în ultimul an fără consultarea elevilor și reconstituie cine ar fi trebuit consultat, când și cum.

**F11 — Ce s-a decis fără mine anul acesta.** A doua fișă-sursă pentru unitatea III.

- [ ] **Pașii 1–6:** procedura standard. După pasul 2, așteptat: `neacoperit: 8`.
- [ ] Commit: `git commit -am "Adaugă lecția 14 — apatia cetățeanului"`

---

## Sarcina 21: Lecția 15 — Reflecție asupra unității II, și poarta de calitate

**Fișier:** `manual/u2-amenintari/l15-reflectie.md`

```yaml
unitate: 2
lectie: 15
tip: reflectie
titlu: "Reflecție asupra unității"
ore: 1
competente: [3, 18]
descriptori: [5, 6, 36]
unitati_competenta: [UC3, UC9]
continut_curricular: [C6]
fise: []
```

Recitirea fișelor F6–F11; harta mentală *Despre democrație*; bilanț; autoevaluare pe descriptorii unității.

- [ ] **Pasul 1:** Creează și scrie lecția (500–700 de cuvinte).
- [ ] **Pasul 2:** `./verificare/ruleaza-tot.sh`. Așteptat: 14 fișiere de lecție, 16 ore, conținuturile C1–C11 acoperite.
- [ ] **Pasul 3:** `profesor-roman` pe toate fișierele din `manual/u2-amenintari/`.
- [ ] **Pasul 4:** Verificarea la sursă a tuturor linkurilor și cifrelor adăugate la unitatea II. Atenție specială la lecția 13.
- [ ] **Pasul 5:** Citire ca elev: morală explicită? sarcini formulate ca „discutați despre"? Corectează.
- [ ] **Pasul 6:** Commit: `git add -A && git commit -m "Închide unitatea II: reflecție, verificări, corecturi"`

---

# FAZA 4 — Unitatea III. Șantierul integrității (11 ore)

Structură proprie: nu lecții, ci pași de proiect. Fiecare pas (`tip: santier`, 600–900 de cuvinte) conține: **întrebarea de cercetare a pasului**, **instrumentul gata de folosit**, **criteriile de calitate ale produsului**, **jurnalul de echipă** (ce am făcut, ce ne-a blocat, ce facem data viitoare).

Elevii intră în șantier cu fișele **F9** (harta integrității) și **F11** (ce s-a decis fără mine) deja completate. Pasul 1 începe de la ele.

## Sarcina 22: Deschiderea unității III și pașii 1–2

**Fișiere:** `manual/u3-santier-integritate/u3-deschidere.md`, `p01-integritatea-in-comunitate.md`, `p02-culegerea-de-informatii.md`

Deschiderea: ce este un șantier, ce se va produce (Codul de integritate al cetățeanului), cum se formează echipele, cum se împart rolurile, calendarul celor 11 ore. ~300 de cuvinte.

```yaml
# p01
unitate: 3
pas: 1
tip: santier
titlu: "Integritatea în comunitatea mea"
ore: 1
competente: [11, 16, 18]
descriptori: [21, 31, 35]
unitati_competenta: [UC8]
continut_curricular: [C12]
fise: [F12]
```
Pasul 1: echipele recitesc F9 și F11, aleg **o singură** problemă de integritate din comunitatea lor și o transformă în întrebare de cercetare. Criteriul de calitate: întrebarea trebuie să aibă un răspuns care se poate afla, nu unul care se poate presupune.

```yaml
# p02
unitate: 3
pas: 2
tip: santier
titlu: "Culegerea de informații"
ore: 1
competente: [10, 11, 16]
descriptori: [19, 20, 31]
unitati_competenta: [UC8]
continut_curricular: [C12]
fise: [F13]
```
Pasul 2: ce documente există deja (regulamente, hotărâri, rapoarte publice), cine poate fi întrebat, cum se cere o informație de interes public. Instrumentul: modelul de cerere de acces la informație, cu câmpurile de completat.

- [ ] **Pasul 1:** Creează cele trei fișiere cu antetele de mai sus.
- [ ] **Pasul 2:** `python3 verificare/trasabilitate.py` → C12 acoperit, `neacoperit: 7`.
- [ ] **Pasul 3:** Găsește procedura reală de acces la informație din RM (legea și articolul exact) pentru instrumentul de la pasul 2.
- [ ] **Pasul 4:** Scrie cele trei fișiere.
- [ ] **Pasul 5:** `./verificare/ruleaza-tot.sh`.
- [ ] **Pasul 6:** Commit: `git commit -am "Adaugă deschiderea șantierului și pașii 1-2"`

---

## Sarcina 23: Pașii 3–4 — Pregătirea studiului și analiza datelor

**Fișiere:** `p03-pregatirea-studiului.md`, `p04-analiza-datelor.md`

```yaml
# p03 — pas: 3, ore: 1, competente: [12, 15, 16], descriptori: [23, 29, 30, 32], fise: [F14]
# p04 — pas: 4, ore: 1, competente: [11, 14, 16], descriptori: [21, 22, 27], fise: [F15]
```
Ambele: `unitate: 3`, `tip: santier`, `unitati_competenta: [UC8]`, `continut_curricular: [C12]`.

Pasul 3 — instrumentul: chestionarul de 6–8 întrebări și grila de interviu, cu regulile lor (o întrebare = un lucru; fără întrebări care sugerează răspunsul; anonimatul respondentului). Pasul 4 — instrumentul: tabelul de sinteză, distincția între ce arată datele și ce credem noi despre ele.

- [ ] **Pașii 1–6:** procedura standard.
- [ ] Commit: `git commit -am "Adaugă pașii 3-4 ai șantierului"`

---

## Sarcina 24: Pașii 5–6 — Redactarea Codului de integritate

**Fișier:** `manual/u3-santier-integritate/p05-06-redactarea-codului.md`

```yaml
unitate: 3
pas: 5
tip: santier
titlu: "Redactarea Codului de integritate al cetățeanului"
ore: 2
volum_min: 1200
volum_max: 1800
competente: [3, 7, 16]
descriptori: [5, 6, 32]
unitati_competenta: [UC8, UC9]
continut_curricular: [C12]
fise: [F16]
```
Volum: 1200–1800 de cuvinte.

Structura Codului, cerută de curriculum: **principii, norme, drepturi și responsabilități**. Instrumentul: macheta Codului, cu exemple de formulare corectă și incorectă a unei norme (o normă spune ce face cineva, verificabil; nu ce simte). Criteriile de calitate: fiecare normă să se sprijine pe o dată culeasă la pașii 2–4.

- [ ] **Pașii 1–6:** procedura standard.
- [ ] Commit: `git commit -am "Adaugă pașii 5-6 — redactarea Codului de integritate"`

---

## Sarcina 25: Pașii 7–8 — Materialul de promovare

**Fișier:** `manual/u3-santier-integritate/p07-08-material-de-promovare.md`

```yaml
unitate: 3
pas: 7
tip: santier
titlu: "Materialul de promovare a Codului"
ore: 2
volum_min: 1200
volum_max: 1800
competente: [15, 16, 19]
descriptori: [29, 31, 37]
unitati_competenta: [UC8]
continut_curricular: [C12]
fise: []
```
Volum: 1200–1800 de cuvinte.

Aici se întoarce unitatea I: elevii au învățat cum se construiește un mesaj persuasiv — acum construiesc unul ei înșiși, onest. Instrumentul: grila mesajului (cui vorbesc, ce vreau să facă, ce dovadă am, ce nu am voie să exagerez). Formatele la alegere: afiș, spot de 30 de secunde, pliant.

**Legătura explicită cu lecțiile 2–3 este obligatorie:** aceleași tehnici, folosite cu răspundere. Caseta *Aici nu există un singur răspuns*: unde e granița dintre a convinge și a manipula?

- [ ] **Pașii 1–6:** procedura standard.
- [ ] Commit: `git commit -am "Adaugă pașii 7-8 — materialul de promovare"`

---

## Sarcina 26: Pașii 9–11 — Prezentarea, audierea, reflecția

**Fișiere:** `p09-pregatirea-prezentarii.md`, `p10-audierea-publica.md`, `p11-reflectie.md`

```yaml
# p09 — pas: 9,  ore: 1, tip: santier,   competente: [15, 19], descriptori: [29, 37], fise: []
# p10 — pas: 10, ore: 1, tip: santier,   competente: [12, 17, 23], descriptori: [23, 33, 34], fise: [F17, F18]
# p11 — pas: 11, ore: 1, tip: reflectie, competente: [18, 7],  descriptori: [13, 14, 36], fise: []
```
Toate: `unitate: 3`, `unitati_competenta: [UC8, UC9]`, `continut_curricular: [C12]`.

**Pasul 9** — pregătirea prezentării: comprimat la o oră (aici e ora cedată unității II). Instrumentul: structura în cinci minute — problema, ce am aflat, ce propunem, ce cerem de la voi.

**Pasul 10** — audierea publică: invitați reali (diriginte, administrație, consiliul elevilor, un părinte, un reprezentant al primăriei). Instrumentul: regulile audierii și fișa de consemnare a feedbackului. Aici se completează F17 (feedbackul primit) și F18 (Codul revizuit) — **revizuirea după feedback este obligatorie**, e caracteristica definitorie a învățării bazate pe proiect din curriculum.

**Pasul 11** — reflecție (500–700 de cuvinte): ce a mers, ce nu, ce ar face altfel echipa; ce a învățat fiecare despre sine lucrând în echipă.

- [ ] **Pașii 1–6:** procedura standard pentru toate trei fișierele.
- [ ] Commit: `git add -A && git commit -m "Adaugă pașii 9-11 și închide șantierul integrității"`

---

# FAZA 5 — Unitatea IV. Cetățenia activă. Voluntariatul (7 ore)

## Sarcina 27: Deschiderea unității IV și lecția 27 — Spiritul civic și voluntariatul

**Fișiere:** `manual/u4-cetatenia-activa/u4-deschidere.md`, `l27-spirit-civic.md`

Deschiderea: întrebarea mare *Ce pot face eu, de fapt?*; fișele F19–F23; ~300 de cuvinte.

```yaml
unitate: 4
lectie: 27
tip: continut
titlu: "Spiritul civic și voluntariatul"
ore: 1
competente: [6, 7, 13]
descriptori: [8, 11, 12, 25, 26]
unitati_competenta: [UC5]
continut_curricular: [C13]
fise: [F19]
```

**Întrebarea lecției:** De ce ar face cineva o muncă pentru care nu e plătit?

**De reținut:** ce e și ce nu e voluntariatul (nu e muncă gratuită pentru cineva care ar trebui să plătească); cadrul legal al voluntariatului în RM — contractul de voluntariat, carnetul, drepturile voluntarului; ce câștigă voluntarul; de unde începe cineva la 15 ani.

**Surse:** Legea voluntariatului din RM — articolele privind contractul și drepturile voluntarului, citate exact; o organizație reală din RM care primește voluntari minori, cu condițiile ei publice.

**F19 — Profilul meu de voluntar:** ce pot oferi, cât timp am, cui i-ar folosi.

- [ ] **Pașii 1–6:** procedura standard. După pasul 2, așteptat: `neacoperit: 5`.
- [ ] Commit: `git commit -am "Adaugă deschiderea unității IV și lecția 27"`

---

## Sarcina 28: Lecția 28 — Cetățean al comunității, al țării, al Europei, al lumii

**Fișier:** `manual/u4-cetatenia-activa/l28-cercuri-de-apartenenta.md`

```yaml
unitate: 4
lectie: 28
tip: continut
titlu: "Cetățean al comunității, al țării, al Europei, al lumii"
ore: 1
competente: [2, 4, 5, 20]
descriptori: [3, 4, 7, 10]
unitati_competenta: [UC5, UC6]
continut_curricular: [C14, C15]
fise: [F20]
```

**Întrebarea lecției:** Câte apartenențe încap într-un singur om?

**De reținut:** cetățenia ca statut juridic și ca practică; drepturile și obligațiile cetățeanului RM (Constituția, articolele exacte); ce înseamnă cetățenia europeană și ce nu înseamnă; apartenențele multiple ca normă, nu ca problemă — un om poate fi, simultan, dintr-un sat, dintr-o țară, dintr-o Europă și dintr-o limbă maternă diferită de a vecinului.

Aici se leagă explicit de unitatea II: apartenențele multiple sunt exact ce neagă șovinismul.

**F20 — Cercurile mele de apartenență.**

- [ ] **Pașii 1–6:** procedura standard. După pasul 2, așteptat: `neacoperit: 3`.
- [ ] Commit: `git commit -am "Adaugă lecția 28 — cercurile de apartenență"`

---

## Sarcina 29: Lecțiile 29–31 — Rolul meu într-o societate democratică

**Fișier:** `manual/u4-cetatenia-activa/l29-31-rolul-meu.md`

```yaml
unitate: 4
lectie: 29
tip: continut
titlu: "Rolul meu într-o societate democratică"
ore: 3
volum_min: 3300
volum_max: 4200
competente: [6, 8, 16, 17, 20]
descriptori: [12, 16, 18, 28, 32, 33, 39]
unitati_competenta: [UC5, UC6, UC7]
continut_curricular: [C16, C17, C18]
fise: [F21, F22]
```
Volum: 3300–4200 de cuvinte, structurat pe trei ore distincte, marcate în text.

**Ora 1 — mecanismele.** Cum se ia o decizie într-o școală, într-o primărie, într-un parlament. Cine are drept de inițiativă, unde intră cetățeanul, ce e o consultare publică. Instrument: harta deciziei. **F21 — Harta deciziei în școala mea.** Nu e materie primă pentru unitatea III — aceea s-a încheiat. E oglinda de după: elevul cartografiază mecanismul formal de decizie și descoperă abia acum pe ce ușă ar putea intra Codul pe care l-a scris deja. Textul lecției trebuie să facă explicit această legătură înapoi.

**Ora 2 — pluralism și consens.** De ce dezacordul e normal și necesar; diferența dintre compromis și consens; cum se conduce o discuție în care nu toată lumea vrea același lucru. Simulare: clasa ia o decizie reală care o privește, cu proceduri explicite.

**Ora 3 — instrumentele.** Petiția, demersul, propunerea de modificare a unui regulament, ședința consiliului elevilor. Fiecare cu macheta lui, gata de folosit. **F22 — Angajamentul meu pe trei luni:** o acțiune concretă, cu termen și cu primul pas scris.

**Surse:** regulamentul-tip de organizare a consiliului elevilor (document real al MEC sau al unei instituții, cu link); procedura reală de depunere a unei petiții către o autoritate din RM (legea și articolul).

- [ ] **Pașii 1–6:** procedura standard. După pasul 2, așteptat: `neacoperit: 0`. **Toate cele 18 unități de conținut și toate cele 9 unități de competențe sunt acum acoperite.**
- [ ] Commit: `git commit -am "Adaugă lecțiile 29-31 — rolul meu într-o societate democratică"`

---

## Sarcina 30: Lecțiile 32–33 — Reflecția finală

**Fișiere:** `manual/u4-cetatenia-activa/l32-reflectie.md`, `l33-recitirea-dosarului.md`

```yaml
# l32 — lectie: 32, tip: reflectie, ore: 1, competente: [6, 18], descriptori: [11, 12, 36], fise: []
# l33 — lectie: 33, tip: reflectie, ore: 1, competente: [18, 8], descriptori: [15, 35, 36], fise: [F23]
```
Ambele: `unitate: 4`, `unitati_competenta: [UC5]`, `continut_curricular: [C13]`.

**Lecția 32** — reflecție asupra unității IV: recitirea F19–F22; ce s-a schimbat în ce crede elevul că poate face.

**Lecția 33 — recitirea dosarului.** Nu doar a anului: a celor cinci ani de disciplină. Elevul își recitește tot dosarul, de la F1 la F22, și scrie **F23 — Scrisoare către mine, cel din clasa a V-a**: ce i-ar spune copilului care începea gimnaziul. Apoi trece ultima dată prin grila celor 40 de descriptori și marchează, pentru fiecare bifat, **unde anume** în dosar se vede.

Aceasta e ultima pagină a manualului. Nu conține concluzii ale autorului. Ultimul cuvânt e al elevului.

- [ ] **Pasul 1:** Creează și scrie ambele fișiere (500–700 de cuvinte fiecare).
- [ ] **Pasul 2:** Completează F23 în `manual/anexe/dosarul-meu-de-cetatean.md`.
- [ ] **Pasul 3:** `./verificare/ruleaza-tot.sh`. Așteptat: **28 de fișiere de lecție, 34 de ore, 0 neacoperit**.
- [ ] **Pasul 4:** Commit: `git add -A && git commit -m "Adaugă lecțiile 32-33 și închide manualul"`

---

# FAZA 6 — Aparatul și verificările finale

## Sarcina 31: Glosarul și bibliografia

**Fișiere:** `manual/anexe/glosar.md`, `manual/anexe/surse-si-bibliografie.md` (finalizare)

- [ ] **Pasul 1: Extrage toți termenii din casetele *Cuvinte de care ai nevoie***

Rulează: `grep -rh -A3 'Cuvinte de care ai nevoie' manual/ | grep '^> \*\*' | sort -u`

- [ ] **Pasul 2:** Scrie glosarul: fiecare termen, definiția scurtă (identică cu cea din lecție — orice divergență e o eroare de corectat în lecție), și lecția unde apare prima dată.
- [ ] **Pasul 3:** Finalizează bibliografia: grupată pe unități, fiecare intrare cu titlu, instituție, link, dată de accesare. Marchează cu `[de reînnoit]` sursele legate de evenimente în desfășurare.
- [ ] **Pasul 4:** Commit: `git add manual/anexe/ && git commit -m "Adaugă glosarul și finalizează bibliografia"`

---

## Sarcina 32: Cuvânt către elev și cuprins

**Fișiere:** `manual/00-cuvant-catre-elev.md`, `manual/00-cuprins.md`

- [ ] **Pasul 1:** Scrie *Cuvânt către elev* (~400 de cuvinte). Ce e cartea asta, de ce nu are note, de ce jumătate din ea o scrie el. Se scrie **la sfârșit**, nu la început — abia acum se știe ce a ieșit.
- [ ] **Pasul 2:** Generează cuprinsul din antete:

```bash
python3 -c "
import sys; sys.path.insert(0,'verificare'); import fm
for cale, a in fm.toate_lectiile('manual'):
    n = a.get('lectie', a.get('pas'))
    print(f\"| {n} | [{a['titlu']}]({cale.relative_to('manual')}) | {a.get('ore','')} |\")
"
```
- [ ] **Pasul 3:** Scrie `00-cuprins.md` cu cele patru unități, orele și trimiterile la anexe.
- [ ] **Pasul 4:** Commit: `git add manual/00-*.md && git commit -m "Adaugă cuvântul către elev și cuprinsul"`

---

## Sarcina 33: Verificarea finală

- [ ] **Pasul 1: Toate verificările automate**

Rulează: `./verificare/ruleaza-tot.sh; echo "cod ieșire: $?"`
Așteptat: `cod ieșire: 0` — 28 de fișiere de lecție, 34 de ore, 0 neacoperit, 40/40 descriptori, 0 abateri de volum.

- [ ] **Pasul 2: Limba**

`profesor-roman` pe fiecare fișier din `manual/` care nu a trecut încă prin el (unitățile III și IV, anexele).

- [ ] **Pasul 3: Ancorele interne**

Toate trimiterile către anexe trebuie să ajungă undeva. Ancorele se scriu cu ghilimele ASCII
(`<a id="f1"></a>`) și orice normalizare tipografică a ghilimelelor le poate strica **tăcut** — s-a
întâmplat o dată, la lecția 0, unde o corectură de ghilimele a transformat 63 de ancore în ținte
inexistente. Verifică programatic că fiecare `](...#ancora)` din `manual/` are un `id="ancora"`
corespunzător în fișierul-țintă, și că nicio ancoră nu folosește ghilimele tipografice.

- [ ] **Pasul 4: Toate linkurile externe**

```bash
grep -oh 'https\?://[^ )]*' -r manual/ | sort -u > /tmp/linkuri.txt
while read u; do printf '%s ' "$u"; curl -sS -o /dev/null -w '%{http_code}\n' --max-time 20 "$u" || echo EROARE; done < /tmp/linkuri.txt
```
Orice cod ≠ 200: sursa se înlocuiește sau se elimină, iar lecția se ajustează.

- [ ] **Pasul 4: Recitirea de protocol**

Lecțiile 11 și 13: încă o trecere, doar pentru vină pusă pe victimă și detalii inutile. Lecțiile 2–3 și 9–10: încă o trecere, doar pentru ca nicio formulare să nu lege propaganda de limba vorbită de elevi.

- [ ] **Pasul 5: Inventarul briefurilor de ilustrație**

```bash
grep -rn '\[ILUSTRAȚIE\]' manual/ | tee docs/verificare/ilustratii.md | wc -l
```
Lista completă a imaginilor de produs, cu lecția și descrierea. Aceasta e intrarea în etapa vizuală (skill `pictor`), care nu face parte din acest plan.

- [ ] **Pasul 6: Actualizează README**

Tabelul de statut: redactarea lecțiilor → gata; adaugă rezultatele verificărilor.

- [ ] **Pasul 7: Commit final**

```bash
git add -A
git commit -m "Verificare finală: 34 de lecții, 40/40 descriptori, curriculum acoperit integral"
git push
```

---

## Ce nu face acest plan

- **Imaginile.** Se produc după stabilizarea textului, pornind de la `docs/verificare/ilustratii.md`.
- **Conversia în .docx / HTML.** Sintaxa Markdown uniformă face conversia mecanică; se face la cerere.
- **Ghidul profesorului.** Poate fi derivat ulterior din manual, mult mai rapid decât dacă ar fi scris de la zero.
- **Adaptarea la un curriculum revizuit.** Dacă MEC publică versiunea nouă, se actualizează `verificare/referinta.yaml`; verificările vor arăta imediat, la rulare, ce lecții trebuie rescrise. Acesta este principalul câștig al infrastructurii din Faza 0.
