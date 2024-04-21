from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# The API key
API_KEY = "123123test"


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/')
def welcome():
    return 'Welcome'


@app.route('/hello')
def hello_world():
    return 'Hello World'


@app.route('/shutdown', methods=['POST'])
def shutdown():
    # Get the API key from the request header
    auth_header = request.headers.get('Authorization')
    print("auth header: " , auth_header)

    # Check if authorization header is present and valid
    if not auth_header or auth_header != f"Bearer {API_KEY}":
        return jsonify({'error': 'Invalid API key'}), 401  # Unauthorized

    shutdown_server()
    return 'Server shutting down...'


if __name__ == '__main__':
    app.run()
