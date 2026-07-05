# Pentaminos 8x8

Interface web pour trouver des solutions de pentaminos sur un echiquier 8x8.

Le plateau contient 64 cases. Les 12 pentaminos couvrent 60 cases au total, donc l'application permet de choisir exactement 4 cases noires avant de lancer la recherche.

## Utilisation

Ouvrir `index.html` dans un navigateur, puis :

1. Choisir 4 cases noires sur l'echiquier.
2. Cliquer sur `Calculer`.
3. Naviguer entre les solutions avec `Precedente` et `Suivante`.

Le bouton `Coins` selectionne automatiquement `A1`, `A8`, `H1` et `H8`.

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
