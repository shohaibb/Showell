from flask import Flask, render_template
from algorithms.algorithm1 import my_algorithm_function
from api_clients.database_client import fetch_data_from_db
from api_clients.external_api_client import fetch_api_data

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/browse')
def browse():
    return render_template('browse.html')

if __name__ == '__main__':
    app.run(debug=True)
