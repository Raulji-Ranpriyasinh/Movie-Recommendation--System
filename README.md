# Movie Recommendation Web App

This web application, built with Flask, provides personalized movie recommendations based on user selection. It utilizes the Flask framework, TMDB API (The Movie Database), and collaborative filtering for movie recommendations.

## Features

- **Browse Movies:** Explore a curated list of movies available in the application.
- **Get Recommendations:** Select a movie of interest to receive personalized movie recommendations.
- **Detailed Information:** View recommended movies with posters and links to additional information on TMDB.

## Files and Structure

- **app.py:** Main Flask application file.
- **movies_dict.pkl:** Pickled file containing movie data.
- **similarity.pkl:** Pickled file containing similarity data.
- **templates:** Directory containing HTML templates for the application.

## Acknowledgments

- Movie data is obtained from the TMDB API.
- The recommendation algorithm is based on collaborative filtering.
