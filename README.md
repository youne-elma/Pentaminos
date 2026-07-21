# Pentaminos

Interface web pour trouver des solutions de pentaminos.

La page d'accueil `index.html` propose deux modes :

- `Pentaminos Extreme` : solveur 8x8 historique dans `normal.html`.
- `Pentaminos Easy pro` : variante 7x5 dans `new-pentomino.html`.

## Pentaminos Extreme

Le mode normal utilise un echiquier 8x8.

Le plateau contient 64 cases. Les 12 pentaminos couvrent 60 cases au total, donc l'application permet de choisir exactement 4 cases noires avant de lancer la recherche.

## Utilisation

Ouvrir `normal.html` dans un navigateur, puis :

1. Choisir 4 cases noires sur l'echiquier.
2. Cliquer sur `Calculer`.
3. Naviguer entre les solutions avec `Precedente` et `Suivante`.

Le bouton `Coins` selectionne automatiquement `A1`, `A8`, `H1` et `H8`.

## Pentaminos Easy pro

Le nouveau mode utilise un echiquier 7x5, de `A` a `G` et de `1` a `5`.

Les cases `D5`, `E5`, `F5` et `G5` sont deja bloquees. Il faut ensuite choisir une seule case inconnue et exactement 6 pieces parmi les 12 pentominos avant de lancer la recherche.

## Version console

Le fichier `pentomino_solver.py` contient aussi un solveur en ligne de commande :

```powershell
python .\pentomino_solver.py --limit 1 --coords
```

Pour compter toutes les solutions du cas avec les quatre coins vides :

```powershell
python .\pentomino_solver.py --limit 0
```

## GitHub Pages

Ce projet est compatible avec GitHub Pages tel quel : la page principale est `index.html` a la racine du depot.
