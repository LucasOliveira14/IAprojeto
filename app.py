from flask import Flask, request, render_template # type: ignore
import pandas as pd # type: ignore

app = Flask(__name__)


data = pd.read_csv('ml-100k/u.data', sep='\t', names=['user_id', 'item_id', 'rating', 'timestamp'])
mean_ratings = data.groupby('item_id')['rating'].mean().reset_index()
mean_ratings.columns = ['item_id', 'mean_rating']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommendations', methods=['POST'])
def recommendations():
    user_id = int(request.form['user_id'])
    user_ratings = data[data['user_id'] == user_id]
    user_ratings = user_ratings.merge(mean_ratings, on='item_id')
    user_ratings = user_ratings.sort_values(by='mean_rating', ascending=False)
    recommendations = user_ratings.head(5)['item_id'].tolist()
    return render_template('recommendations.html', user_id=user_id, recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
