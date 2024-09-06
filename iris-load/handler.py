import numpy as np

def handle(req):
    counter = 0
    while counter < 500:
        counter += 1
        a = np.random.rand(500, 500)
        b = np.random.rand(500, 500)
        c = np.dot(a, b)
        d = np.linalg.inv(c)
    return 'finito'