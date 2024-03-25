#!/usr/bin/python3
""" Starts a Flask web application """
from flask import Flask

# Create a Flask web application
app = Flask(__name__)

# Define routes


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """returns Hello HBNB!"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """returns HBNB"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def cisfun(text):
    """display “C ” followed by the value of the text variable"""
    return 'C ' + text.replace('_', ' ')


# Run the Flask app


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
