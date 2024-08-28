# training_script.py

import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

# Carichiamo un dataset di esempio (Iris)
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Alleniamo un modello di Logistic Regression
model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

# Salviamo il modello su un file
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Modello allenato e salvato in 'model.pkl'.")
