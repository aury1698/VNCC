import pickle
import numpy as np
import requests
from kubernetes import client, config

config.load_incluster_config()
api = client.CoreV1Api()
service = api.read_namespaced_service(name="iris-server-service", namespace="default")
print('Service IP:', service.spec.cluster_ip)
cluster_ip = service.spec.cluster_ip

with open('model.pkl', 'rb') as f:
    default = pickle.load(f)

def handle(req):
    try:
        foo = req.split(';')
        type = foo[0]
        data = foo[1]
        if type == 'default':
            print('default model') 
            # Convertiamo l'input in un array numpy (modifica questo in base al tuo modello)
            input_data = np.array([float(i) for i in data.split(',')]).reshape(1, -1)
            # Facciamo la predizione
            prediction = default.predict(input_data)
            # Restituiamo il risultato come stringa
            result = "Predizione:" + str(prediction[0])
            return result
        elif type == 'custom':
            print('custom model')
            # cambiare localhost con pinata
            # model_bytes = requests.get('http://localhost:6001/model')
            request = requests.get('http://'+cluster_ip+':6002/model')
            model_bytes = request.content
            custom = pickle.loads(model_bytes)
            # Convertiamo l'input in un array numpy (modifica questo in base al tuo modello)
            input_data = np.array([float(i) for i in data.split(',')]).reshape(1, -1)
            # Facciamo la predizione
            prediction = custom.predict(input_data)
            # Restituiamo il risultato come stringa
            result = "Predizione:" + str(prediction[0])
            return result
        else:
            return "Invalid type"
    except Exception as e:
        return str(e)
