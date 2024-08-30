import pickle
import numpy as np
import requests
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

def handle(req):
    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)
    model_bytes = pickle.dumps(model)
    requests.post('http://localhost:6001/model', data=model_bytes)
    if result.status_code >= 200 and result.status_code < 300:
        # print("Modello salvato.")
        return "Modello salvato."
    else:
        # print("Errore:", result.text)
        return "Errore:"+result.text
    