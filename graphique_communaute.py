#!/usr/bin/env python3
"""Trace le nombre de personnes présentes dans la communauté au fil du temps,
à partir des horodatages d'arrivée et de départ."""

import csv
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt

POPULATION_INITIALE = 32
DOSSIER = Path(__file__).parent
FICHIER_ARRIVEES = DOSSIER / "arrive.csv"
FICHIER_DEPARTS = DOSSIER / "departs.csv"


def lire_horodatages(fichier):
    with open(fichier, newline="") as f:
        lecteur = csv.DictReader(f)
        return [datetime.fromisoformat(ligne["date"]) for ligne in lecteur]


def main():
    arrivees = [(t, +1) for t in lire_horodatages(FICHIER_ARRIVEES)]
    departs = [(t, -1) for t in lire_horodatages(FICHIER_DEPARTS)]

    evenements = sorted(arrivees + departs, key=lambda e: e[0])

    dates = [evenements[0][0]] if evenements else []
    effectifs = [POPULATION_INITIALE]
    compte = POPULATION_INITIALE
    for temps, variation in evenements:
        compte += variation
        dates.append(temps)
        effectifs.append(compte)

    plt.figure(figsize=(14, 6))
    plt.step(dates, effectifs, where="post")
    plt.xlabel("Date")
    plt.ylabel("Nombre de personnes")
    plt.title("Nombre de personnes dans la communauté au fil du temps")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(DOSSIER / "communaute.png", dpi=150)
    plt.show()


if __name__ == "__main__":
    main()
