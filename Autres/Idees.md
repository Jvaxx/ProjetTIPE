# Idées:

## Réalisation du radio-goniomètre:

+ Mesure de la différence de phase par multiplicateur ou additionneur?
+ Quels AO utiliser pour la simulation avec PGB suffisant?

## Complexification du projet:

#### Detection 3D: correlation de données (en simulation)

**Objectifs**:

Utiliser 2 radio-goniomètres (donc 6 antennes) dans 2 plans différents pour
localiser la source dans l'espace

**Réalisation**:

Simulation sur python des données théoriques recues par chaque antennes pour une
source située en tous points de l'espace:

Pour une source située en coordonnées sphériques suivantes: **(r, theta, phi)**,
on simule la différence de phase sur chacune des 6 antennes

| Theata \ Phi|      1°             |  2°      | 3°       | etc...   |
|-------------|:-------------------:|:--------:|:--------:|:--------:|
| **1°**      |  [1, 2, 3, 4, 5, 6] | [......] | [......] | [......] |
| **2°**      |  [1, 2, 3, 4, 5, 6] | [......] | [......] | [......] |
| **3°**      |  [1, 2, 3, 4, 5, 6] | [......] | [......] | [......] |
| **etc...**  |  [......]           | [......] | [......] | [......] |

Les listes des différences de phase sont uniques (sauf pour les points situés sur l'axe
theta=180° et theta=0°)

Ensuite, les données reelles reçues sont comparées à cette table et on en déduit les
valeurs de theta et de phi, on obtient donc la direction de la source en 3D.


#### Prise en compte des ondes réfléchies
Exemple: Sauvetage en montagne, réfléxion des ondes sur les parois, comment éviter
ce phénomène

#### Triangulation du signal en direct
Réalisation en continu des mesures de direction tout en déplaçant l'appareil.
Connaisant les différentes positions du radiogoniomètre, on triangule la position
de la source.