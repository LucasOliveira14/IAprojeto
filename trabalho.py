import pandas as pd # type: ignore

data = pd.read_csv('ml-100k/u.data', sep='\t', names=['user_id', 'item_id', 'rating', 'timestamp'])

print(data.head())

print(data.info())


ratings_count = data.groupby('item_id')['rating'].count().reset_index()
ratings_count.columns = ['item_id', 'ratings_count']


data = data.merge(ratings_count, on='item_id')

print(data.head())


mean_ratings = data.groupby('item_id')['rating'].mean().reset_index()
mean_ratings.columns = ['item_id', 'mean_rating']


data = data.merge(mean_ratings, on='item_id')


print(data.head())


def recommend_movies(user_id, n_recommendations=5):
    user_ratings = data[data['user_id'] == user_id]
    user_ratings = user_ratings.sort_values(by='mean_rating', ascending=False)
    recommendations = user_ratings.head(n_recommendations)
    return recommendations


recommendations = recommend_movies(1)
print(recommendations)
# Verificar dados ausentes
print(data.isnull().sum())

# Análise exploratória dos dados
print(data.describe())

# Codificar variáveis categóricas (se houver)
# Exemplo: data = pd.get_dummies(data, columns=['genre'])

# Divisão dos dados em conjuntos de treinamento e teste
from sklearn.model_selection import train_test_split # type: ignore

train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)
print("Tamanho do conjunto de treinamento:", len(train_data))
print("Tamanho do conjunto de teste:", len(test_data))
# Calcular a média das avaliações por filme
mean_ratings = train_data.groupby('item_id')['rating'].mean().reset_index()
mean_ratings.columns = ['item_id', 'mean_rating']

# Adicionar a média das avaliações ao DataFrame original
train_data = train_data.merge(mean_ratings, on='item_id')

# Visualizar as primeiras linhas dos dados após adicionar as médias de avaliações
print(train_data.head())

# Função para recomendar filmes com base na média das avaliações
def recommend_movies(user_id, n_recommendations=5):
    user_ratings = train_data[train_data['user_id'] == user_id]
    user_ratings = user_ratings.sort_values(by='mean_rating', ascending=False)
    recommendations = user_ratings.head(n_recommendations)
    return recommendations

# Exemplo de recomendação para o usuário de ID 1
recommendations = recommend_movies(1)
print(recommendations)
from sklearn.metrics import mean_squared_error # type: ignore
import numpy as np # type: ignore

# Calcular as previsões do modelo (usando a média das avaliações)
predictions = test_data.merge(mean_ratings, on='item_id')['mean_rating']

# Calcular o erro quadrático médio (RMSE)
rmse = np.sqrt(mean_squared_error(test_data['rating'], predictions))
print("RMSE do modelo:", rmse)
# Exemplo de recomendação para o usuário de ID 1
recommendations = recommend_movies(1)
print(recommendations)

