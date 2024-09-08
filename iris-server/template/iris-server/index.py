import os
import sys
import pickle
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

with open('model.pkl' , 'rb') as f:
    default = pickle.load(f)

user_list = [
    {
        'username': 'nicolacucina',
        'password': 'password'
    },
    {
        'username': 'auroratraversini',
        'password': 'wordpass'
    }
]

@app.route('/default', methods=['GET'])
def get_default():
    try:
        return pickle.dumps(default)
    except Exception as e:
        return str(e)

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

@app.route('/user', methods=['POST'])
def auth_user():
    try:
        data = request.get_json()
        for user in user_list:
            if data['username'] == user['username'] and data['password'] == user['password']:
                return 'token'
        return 'Invalid input'
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6001)
