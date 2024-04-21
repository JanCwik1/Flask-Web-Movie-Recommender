from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
import os
from fake_useragent import UserAgent
import random

app = Flask(__name__)

def get_random_index(array):
  """Generates a random integer between 0 (inclusive) and the length of the array (exclusive)."""
  if not array:
    raise ValueError("Array cannot be empty")
  return random.randrange(len(array))

# The API key
API_KEY = "123123test"
ua = UserAgent()

imdb_website_top = "https://www.imdb.com/chart/top/"
headers = {'User-Agent': ua.chrome}  # Example using fake-useragent
imbd_req = requests.get(imdb_website_top, headers=headers)

if imbd_req.status_code == 200:
  soup = BeautifulSoup(imbd_req.text, 'html.parser')
  # Process the parsed content using BeautifulSoup
else:
  print(f"Error: Failed to retrieve data. Status code: {imbd_req.status_code}")

movie_entries = soup.find_all('h3', class_='ipc-title__text')  # Original selector

init1 = soup.find('div', attrs={"data-testid": "chart-layout-main-column"})
init1 = init1.find_all('h3', attrs={"class": "ipc-title__text"})
best_movies_text = []

for x in init1:
    movie_text = x.get_text()
    best_movies_text.append(movie_text)

@app.route('/')
def welcome():
    return 'Welcome'

@app.route('/hello')
def hello_world():
    return 'Hello World'

@app.route('/random_movie')
def random_movie():
    random_index = get_random_index(best_movies_text)
    random_element = best_movies_text[random_index]
    return f'You should check out: {random_element}'

@app.route('/shutdown', methods=['POST'])
def shutdown():
    # Get the API key from the request header
    auth_header = request.headers.get('Authorization')
    print("auth header: " , auth_header)

    # Check if authorization header is present and valid
    if not auth_header or auth_header != f"Bearer {API_KEY}":
        return jsonify({'error': 'Invalid API key'}), 401  # Unauthorized

    def shutdown_app():
        app.logger.info('Stopping application...')
        app.jinja_env.cache = {}  # Clear Jinja template cache (optional)
        # Aadd other cleanup tasks here (closing databases, connections, etc.)
        os._exit(0)  # Exit the process

    with app.app_context():
        shutdown_app()
    return 'Server shutting down...'

if __name__ == '__main__':
    app.run()
