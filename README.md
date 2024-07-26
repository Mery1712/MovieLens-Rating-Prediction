# MovieLens Rating Prediction

Ce projet vise à prédire les notes des utilisateurs pour les films dans le jeu de données MovieLens. Nous avons utilisé des techniques de prétraitement des données, d'exploration de données, de visualisation, ainsi que des modèles de régression pour accomplir cette tâche.

## Table des Matières

- [Introduction](#introduction)
- [Données](#données)
- [Exploration et Visualisation des Données](#exploration-et-visualisation-des-données)
- [Prétraitement des Données](#prétraitement-des-données)
- [Modélisation](#modélisation)
- [Évaluation du Modèle](#évaluation-du-modèle)
- [Conclusion](#conclusion)
- [Installation et Exécution](#installation-et-exécution)

## Introduction

Ce projet utilise les données MovieLens 10M pour prédire les évaluations des utilisateurs pour différents films. Nous avons exploré les données, effectué des visualisations pour comprendre les distributions et les relations, et appliqué plusieurs techniques de modélisation pour prédire les notes des films.

## Données

Le jeu de données MovieLens 10M est téléchargé à partir de [GroupLens](https://grouplens.org/datasets/movielens/). Il contient des informations sur les évaluations des films par les utilisateurs, ainsi que des métadonnées sur les films.

## Exploration et Visualisation des Données

Nous avons exploré les données pour comprendre les distributions des notes, les genres de films les plus populaires, et les relations entre les différentes caractéristiques. Nous avons utilisé des bibliothèques comme `seaborn` et `matplotlib` pour visualiser les distributions des notes, le nombre de films par genre, et la moyenne des notes par genre. Une matrice de corrélation a également été générée pour examiner les relations entre les variables numériques.

## Prétraitement des Données

Le prétraitement a inclus :
- **Extraction de l'année de sortie des films** à partir des titres.
- **Calcul des statistiques des utilisateurs et des films**, comme la moyenne des notes et le nombre d'évaluations.
- **Encodage des genres** de films sous forme de variables binaires.
- **Normalisation** des caractéristiques numériques pour la modélisation.

## Modélisation

Nous avons utilisé plusieurs modèles de régression pour prédire les notes des utilisateurs, notamment :
- **Ridge Regression** : Un modèle de régression linéaire avec régularisation L2.
- **Lasso Regression** : Un modèle de régression linéaire avec régularisation L1.

## Évaluation du Modèle

L'évaluation des modèles a été réalisée en utilisant la **Racine de l'Erreur Quadratique Moyenne (RMSE)** pour mesurer la précision des prédictions. Le modèle Ridge Regression a obtenu un RMSE de `0.8709949207384642`, et le modèle Lasso Regression a obtenu un RMSE de `0.882027854939268`.

## Conclusion

Ce projet a montré comment utiliser des techniques de prétraitement des données, d'exploration et de modélisation pour prédire les notes des films. Les résultats montrent l'importance du choix des caractéristiques et des modèles dans le cadre de la prédiction de notes de films.

## Installation et Exécution

### Prérequis

- Python 3.x
- Bibliothèques : `pandas`, `numpy`, `scikit-learn`, `seaborn`, `matplotlib`, `requests`, `zipfile`

### Instructions

1. Clonez le dépôt : 
   ```bash
   git clone https://github.com/votre_nom_de_utilisateur/nom_du_projet.git
