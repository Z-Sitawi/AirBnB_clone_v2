#!/usr/bin/python3
""" Starts a Flask web application """
from flask import Flask, render_template
from models import *
from models import storage

# Create a Flask web application
app = Flask(__name__)

# Define routes


@app.route('/states_list', strict_slashes=False)
def state_list():
    """Display an HTML page ith the states listed in alphabetical order"""
    states = sorted(list(storage.all("State").values()), key=lambda x: x.name)
    return render_template('7-state_list.html', states=states)


@app.teardown_appcontext
def teardown_appcontext():
    """Removes the current SQLAlchemy Session after each request"""
    storage.close()

# Run the Flask app


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
