# the server must listen for POST requests to store a model and GET requests to return a model
import os
import sys
import pickle
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

with open('model.pkl' , 'rb') as f:
    model = pickle.load(f)

@app.route('/model', methods=['POST'])
def store_model():
    try:
        model = pickle.loads(request.data)
        return "Modello salvato."
    except Exception as e:
        return str(e)

@app.route('/model', methods=['GET'])
def get_model():
    try:
        return pickle.dumps(model)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6001)
