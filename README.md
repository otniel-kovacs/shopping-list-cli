

# Shopping List CLI

Aplicație CLI pentru gestionarea unei liste de cumpărături, în JSON.

## Autor
- **Nume:** Otniel Kovacs
- **Grupă:** [2.1]
- **Email:** [otniel.kovacs@student.upt.ro]
- **An academic:** 2025–2026

## Cerințe sistem
- Python 3.10+ (testat cu 3.12)
- Docker

## Rulare locală
```bash

# Ajutor
python -m src.main help

# Adaugă articole
python -m src.main add "mere" 5 2.5 "fructe"
python -python -m src.main add "lapte" 2 7.9 "lactate"

# Listează (sortare după preț)
python -m src.main list --sort price


## Rulare cu Docker

Imaginea Docker este disponibilă public pe Docker Hub:

https://hub.docker.com/r/smithoty25/shopping-list-cli

Rulare rapidă:

```bash
docker pull smithoty25/shopping-list-cli
docker run --rm smithoty25/shopping-list-cli help

