import os
import psutil
import numpy as np

p = psutil.Process(os.getpid())

counter = 0
while True:
    if counter % 1000 == 0:
        print(p.cpu_percent())
    counter += 1
    a = np.random.rand(100, 100)
    b = np.random.rand(100, 100)
    c = np.dot(a, b)
    np.linalg.inv(c)
