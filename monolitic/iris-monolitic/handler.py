import pickle
import requests
import numpy as np
import requests
from kubernetes import client, config
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

config.load_incluster_config()
api = client.CoreV1Api()
service = api.read_namespaced_service(name="iris-server-service", namespace="default")
print(service.spec.cluster_ip)
cluster_ip = service.spec.cluster_ip

def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    foo = req.split(';')
    username = foo[0]
    password = foo[1]
    type = foo[2]
    model_input_data = foo[3]

    login_data = {
        'username': username,
        'password': password
    }

    result = requests.post('http://' + str(cluster_ip) + ':6002/user', json=login_data)
    if result.text == 'token':
        counter = 0
        while counter < 500:
            counter += 1
            a = np.random.rand(500,500)
            b = np.random.rand(500,500)
            c = np.dot(a,b)
            d = np.linalg.inv(c)
        X, y = load_iris(return_X_y=True)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = LogisticRegression(max_iter=200)
        model.fit(X_train, y_train)
        model_bytes = pickle.dumps(model)
        result = requests.post('http://' + str(cluster_ip) + ':6002/model', data=model_bytes)
        if result.status_code >= 200 and result.status_code < 300:
            print('Modello salvato')
            request = requests.get('http://'+cluster_ip+':6002/default')
            model_bytes = request.content
            default = pickle.loads(model_bytes) 
            # Convertiamo l'input in un array numpy (modifica questo in base al tuo modello)
            input_data = np.array([float(i) for i in model_input_data.split(',')]).reshape(1, -1)
            # Facciamo la predizione
            prediction = default.predict(input_data)
            # Restituiamo il risultato come stringa
            result = "Predizione:" + str(prediction[0])
            return result
        else:
            request = requests.get('http://'+cluster_ip+':6002/model')
            model_bytes = request.content
            custom = pickle.loads(model_bytes)
            # Convertiamo l'input in un array numpy (modifica questo in base al tuo modello)
            input_data = np.array([float(i) for i in model_input_data.split(',')]).reshape(1, -1)
            # Facciamo la predizione
            prediction = custom.predict(input_data)
            # Restituiamo il risultato come stringa
            result = "Predizione:" + str(prediction[0])
            return result
    else:
        return 'errore di autenticazione'
        
    
