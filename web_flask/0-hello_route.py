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

# Run the Flask app


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
