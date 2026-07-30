# Educație pentru societate — manual pentru clasa a IX-a

Manual pentru elev la disciplina *Educație pentru societate*, clasa a IX-a, învățământ gimnazial din
Republica Moldova. Resursă didactică deschisă, în lucru.

## De ce

La clasele VII–IX, Ministerul Educației nu a editat manual pentru elev la această disciplină. Există
doar *Ghidul profesorului*, construit pe activități. Elevul de clasa a IX-a nu are nimic în mână.

Manualul de față îi dă un text al lui, surse reale de analizat și un portofoliu — **Dosarul meu de
cetățean** — pe care îl construiește singur, lecție cu lecție, tot anul.

## Conformitate curriculară

Elaborat după **Curriculumul național, aria curriculară Științe socioumanistice, disciplina Educație
pentru societate, clasele V–IX** (Chișinău, 2018), aprobat prin **Ordinul MECC nr. 1124 din
20 iulie 2018**.

Competențele specifice sunt cele **20 de competențe pentru o cultură democratică** ale Consiliului
Europei. Evaluarea se face **prin descriptori**, nu prin note, conform *Metodologiei de evaluare prin
descriptori, clasele V–XII*.

**34 de ore**, patru unități de învățare:

| Unitatea | Ore |
|---|---|
| I. Cultura mediatică | 8 |
| II. Amenințări la adresa democrației | 8 |
| III. Șantierul: Codul de integritate al cetățeanului (învățare bazată pe proiect) | 11 |
| IV. Cetățenia activă. Voluntariatul | 7 |

> Curriculumul listează la unitatea II conținutul *Traficul de ființe umane*, dar Ghidul profesorului
> nu-i dedică nicio lecție. Manualul acoperă acest gol, cu o oră redistribuită din unitatea-proiect —
> redistribuire permisă explicit de curriculum.

## Structura repozitoriului

```
curriculum/   documentele normative (PDF + text extras) și rezumatul curricular
docs/         specificația de design, planul de implementare, rapoartele de verificare
verificare/   scripturile care verifică manualul
manual/       manualul propriu-zis, un fișier per lecție   (în lucru)
```

## Statut

| Etapă | Statut |
|---|---|
| Curricula găsită și analizată | gata |
| Specificație de design | gata — `docs/superpowers/specs/` |
| Plan de implementare | gata — 33 de sarcini, `docs/superpowers/plans/` |
| Infrastructura de verificare | gata — 4 scripturi, 33 de teste |
| Anexe: descriptorii și Dosarul | gata |
| Unitatea I. Cultura mediatică | 3 din 8 ore scrise |
| Unitățile II–IV | nu au început |

## Verificarea manualului

```
./verificare/ruleaza-tot.sh
```

Patru verificări, repetabile oricând, cu rapoarte în `docs/verificare/`:

- **trasabilitate** — fiecare unitate de competențe și de conținut din curriculum e acoperită de o
  lecție, iar orele însumează exact 34;
- **descriptori** — toți cei 40 de descriptori ai clasei a IX-a sunt observabili undeva, iar
  competențele declarate în antete corespund descriptorilor;
- **volum** — fiecare pagină stă în intervalul de cuvinte al tipului ei;
- **minute** — segmentele cronometrate ale unei lecții însumează cel mult 45 de minute pe oră, iar
  timpul de lucru al elevului depășește timpul de expunere.

Cât timp manualul e incomplet, `ruleaza-tot.sh` întoarce codul 1 și listează ce lipsește. Devine
verde abia când ultima lecție e scrisă.

## Documentele normative

Toate în `curriculum/`, descărcate de pe site-urile oficiale:

- *Curriculum EPS, clasele V–IX* (2018) + Ghidul de implementare
- *Ghidul profesorului, clasa a IX-a* — Consiliul Europei și MECC
- *Metodologia de evaluare prin descriptori, clasele V–XII* — conține cei 40 de descriptori ai clasei a IX-a
- *Metodologia de monitorizare a implementării* (2023)

## Licență

Conținutul original al manualului: CC BY-SA 4.0. Documentele din `curriculum/` sunt publicații
oficiale ale Ministerului Educației și Cercetării al Republicii Moldova și ale Consiliului Europei,
incluse aici doar ca referință.
