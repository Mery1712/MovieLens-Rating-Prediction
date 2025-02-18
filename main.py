import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge, Lasso
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt
import os
import requests
import zipfile

# Téléchargement et extraction des données
zip_file = "ml-10M100K.zip"
ratings_file = "ml-10M100K/ratings.dat"
movies_file = "ml-10M100K/movies.dat"

# Télécharger le fichier si non présent
if not os.path.exists(zip_file):
    url = "https://files.grouplens.org/datasets/movielens/ml-10m.zip"
    r = requests.get(url)
    with open(zip_file, "wb") as f:
        f.write(r.content)

# Extraire les fichiers
with zipfile.ZipFile(zip_file, 'r') as zip_ref:
    zip_ref.extractall()

# Chargement des données
ratings = pd.read_csv(ratings_file, delimiter='::', engine='python',
                      names=['userId', 'movieId', 'rating', 'timestamp'])
movies = pd.read_csv(movies_file, delimiter='::', engine='python',
                     names=['movieId', 'title', 'genres'])

# Convertir les colonnes nécessaires en types appropriés
ratings['userId'] = ratings['userId'].astype(int)
ratings['movieId'] = ratings['movieId'].astype(int)
ratings['rating'] = ratings['rating'].astype(float)
ratings['timestamp'] = ratings['timestamp'].astype(int)
movies['movieId'] = movies['movieId'].astype(int)

# Fusion des données
movielens = pd.merge(ratings, movies, on='movieId')

# Division des données en ensembles edx et final_holdout_test
edx, temp = train_test_split(movielens, test_size=0.1, random_state=1)
final_holdout_test = temp[(temp['movieId'].isin(edx['movieId'])) & (temp['userId'].isin(edx['userId']))]
edx = pd.concat([edx, temp[~temp.index.isin(final_holdout_test.index)]])
del ratings, movies, temp

# Visualisation de la distribution des notes
plt.figure(figsize=(8, 5))
sns.histplot(movielens['rating'], bins=10, kde=False)
plt.title('Distribution des notes')
plt.xlabel('Note')
plt.ylabel('Nombre de votes')
plt.grid(True)
plt.show()

# Nombre de films par genre
genre_count = movielens['genres'].str.get_dummies(sep='|').sum().sort_values(ascending=False)
genre_count.plot(kind='bar', figsize=(12, 6))
plt.title('Nombre de films par genre')
plt.xlabel('Genre')
plt.ylabel('Nombre de films')
plt.grid(True)
plt.show()

# Moyenne des notes par genre
genre_avg_rating = movielens.groupby('genres')['rating'].mean().sort_values(ascending=False)
genre_avg_rating.plot(kind='bar', figsize=(12, 6))
plt.title('Moyenne des notes par genre')
plt.xlabel('Genre')
plt.ylabel('Moyenne des notes')
plt.grid(True)
plt.show()

# Extraction de l'année de sortie des films
def extract_year(title):
    year = title.strip()[-5:-1]
    if year.isdigit():
        return int(year)
    else:
        return pd.NA

movielens['release_year'] = movielens['title'].apply(extract_year)

# Statistiques utilisateur
user_stats = movielens.groupby('userId')['rating'].agg(['mean', 'count']).reset_index()
user_stats.columns = ['userId', 'user_mean_rating', 'user_rating_count']

# Statistiques des films
movie_stats = movielens.groupby('movieId')['rating'].agg(['mean', 'count']).reset_index()
movie_stats.columns = ['movieId', 'movie_mean_rating', 'movie_rating_count']

# Joindre ces statistiques à l'ensemble de données movielens
movielens = movielens.merge(user_stats, on='userId', how='left')
movielens = movielens.merge(movie_stats, on='movieId', how='left')

# Extraction des genres
unique_genres = set()
for genre_list in movielens['genres'].str.split('|'):
    unique_genres.update(genre_list)
unique_genres = list(unique_genres)

# Ajouter une colonne pour chaque genre
for genre in unique_genres:
    movielens[genre] = movielens['genres'].apply(lambda x: 1 if genre in x else 0)

# Supprimer les doublons pour obtenir une liste unique de films
unique_movies_with_genres = movielens[['movieId', 'title', 'genres'] + unique_genres].drop_duplicates(subset=['movieId', 'title'])

# Afficher les premières lignes du DataFrame unique
print(unique_movies_with_genres.head())

# Normalisation/Standardisation
columns_to_normalize = ['user_mean_rating', 'user_rating_count', 'movie_mean_rating', 'movie_rating_count']
scaler = StandardScaler()
movielens[columns_to_normalize] = scaler.fit_transform(movielens[columns_to_normalize])

# Matrice de corrélation des caractéristiques
numeric_features = movielens.select_dtypes(include=[np.number])
corr_matrix = numeric_features.corr()
plt.figure(figsize=(14, 10))
sns.set(style='white')
heatmap = sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm',
                      center=0, linewidths=0.5, linecolor='gray',
                      annot_kws={"size": 10}, cbar_kws={"shrink": .8})
plt.title('Matrice de Corrélation des Caractéristiques', size=16)
plt.xticks(rotation=45, ha='right', fontsize=12)
plt.yticks(rotation=0, fontsize=12)
plt.show()

# Sélection des caractéristiques pertinentes
X = movielens.drop(columns=['rating', 'title', 'genres', 'timestamp'])
y = movielens['rating']

# Séparer les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modélisation avec Ridge Regression
model = Ridge(alpha=1.0)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f'RMSE avec Ridge Regression: {rmse}')

# Modélisation avec Lasso Regression
lasso_model = Lasso(alpha=0.1)
lasso_model.fit(X_train, y_train)
y_pred = lasso_model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f'RMSE avec Lasso Regression: {rmse}')
