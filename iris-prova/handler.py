# handler.py

import pickle
import numpy as np

# Carica il modello al momento del caricamento del modulo
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

def handle(req):
    # Qui supponiamo che `req` contenga una stringa che rappresenta l'input per la predizione
    try:
        # Convertiamo l'input in un array numpy (modifica questo in base al tuo modello)
        input_data = np.array([float(i) for i in req.split(',')]).reshape(1, -1)
        # Facciamo la predizione
        prediction = model.predict(input_data)
        # Restituiamo il risultato come stringa
        result = "Predizione:" + str(prediction[0])
        return result
    except Exception as e:
        return str(e)
