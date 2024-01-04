import pickle
from flask import Flask, render_template, request
import requests
import pandas as pd

app = Flask(__name__)

api_key = "ee9f3a88b8fefdd8e45003d761f77468"
api = "https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US"

def fetch_poster(movie_id):
    response = requests.get(api.format(movie_id, api_key))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie, movies, similarity):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movie_posters

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        selected_movie_name = request.form['selected_movie']
        movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
        movies = pd.DataFrame(movies_dict)
        similarity = pickle.load(open('similarity.pkl', 'rb'))

        recommended_movies, recommended_movie_posters = recommend(selected_movie_name, movies, similarity)

        # Add TMDb links for recommended movies
        recommended_movie_links = []
        for movie in recommended_movies:
            response = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie}&language=en-US")
            data = response.json()
            if data['results']:
                movie_id = data['results'][0]['id']
                movie_link = f"https://www.themoviedb.org/movie/{movie_id}"
                recommended_movie_links.append(movie_link)
            else:
                recommended_movie_links.append("#")  # Placeholder link if information is not available

        return render_template('index.html', 
                               movie_list=movies['title'].values,
                               recommended_movies=recommended_movies, 
                               recommended_movie_posters=recommended_movie_posters,
                               recommended_movie_links=recommended_movie_links)

    else:
        movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
        movies = pd.DataFrame(movies_dict)

        return render_template('index.html', movie_list=movies['title'].values)

if __name__ == '__main__':
    app.run(debug=True)
