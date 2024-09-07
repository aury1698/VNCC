import pickle
import numpy as np
import requests
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from kubernetes import client, config

# Da usare dentro a kubernetes
# config.load_kube_config()
# Da usare con openfaas
config.load_incluster_config()
api = client.CoreV1Api()
service = api.read_namespaced_service(name="iris-server-service", namespace="default")
print('Service IP:', service.spec.cluster_ip)
cluster_ip = service.spec.cluster_ip

def handle(req):
    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)
    model_bytes = pickle.dumps(model)
    # cambiare localhost con pinata
    # requests.post('http://localhost:6001/model', data=model_bytes)
    result = requests.post('http://'+cluster_ip+':6002/model', data=model_bytes)
    if result.status_code >= 200 and result.status_code < 300:
        # print("Modello salvato.")
        return "Modello salvato."
    else:
        # print("Errore:", result.text)
        return "Errore:"+result.text
    