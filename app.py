import sys
import os
from flask import Flask, render_template

# Add the current directory to the Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import functions from your project modules
# from algorithms.classification_algorithm import my_algorithm_function
# from api_clients.database_client import fetch_data_from_db
# from api_clients.external_api_client import fetch_api_data

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/browse')
def browse():
    return render_template('browse.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
