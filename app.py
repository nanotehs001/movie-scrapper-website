from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Home route
@app.route('/')
def index():
    # Scrape movie data or display a form
    movies = scrape_movies()  # Your scrape function
    return render_template('index.html', movies=movies)

# Movie detail route
@app.route('/movie/<path:movie_url>')
def movie_detail(movie_url):
    full_movie_url = f'https://andydaytv.to{movie_url}'
    response = requests.get(full_movie_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Scrape specific movie details
    title = soup.select_one('.film-title').text
    poster_url = soup.select_one('.film-poster img')['src']
    description = soup.select_one('.description').text

    return render_template('movie_detail.html', title=title, poster_url=poster_url, description=description)

# Function to scrape movies for homepage
def scrape_movies():
    url = "https://andydaytv.to/home"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    movies = soup.select('.film-poster')
    movie_data = []

    for movie in movies:
        poster_url = movie.find('img')['data-src']
        movie_url = movie.find('a')['href']
        movie_data.append({'poster_url': poster_url, 'movie_url': movie_url})

    return movie_data

if __name__ == '__main__':
    app.run(debug=True)
