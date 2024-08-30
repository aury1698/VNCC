import pickle
import numpy as np
import requests

with open('model.pkl', 'rb') as f:
    default = pickle.load(f)

def handle(req):
    try:
        foo = req.split(';')
        type = foo[0]
        data = foo[1]
        if type == 'default': 
            # Convertiamo l'input in un array numpy (modifica questo in base al tuo modello)
            input_data = np.array([float(i) for i in req.split(',')]).reshape(1, -1)
            # Facciamo la predizione
            prediction = default.predict(input_data)
            # Restituiamo il risultato come stringa
            result = "Predizione:" + str(prediction[0])
            return result
        elif type == 'custom':
            model_bytes = requests.get('http://localhost:6001/model')
            custom = pickle.loads(model_bytes)
            # Convertiamo l'input in un array numpy (modifica questo in base al tuo modello)
            input_data = np.array([float(i) for i in req.split(',')]).reshape(1, -1)
            # Facciamo la predizione
            prediction = custom.predict(input_data)
            # Restituiamo il risultato come stringa
            result = "Predizione:" + str(prediction[0])
            return
        else:
            return "Invalid type"
    except Exception as e:
        return str(e)
