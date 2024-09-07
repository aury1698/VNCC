import pickle
import requests
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
    foo = req.split(';')
    username = foo[0]
    password = foo[1]

    data = {
        'username': username,
        'password': password
    }

    result = requests.post('http://'+str(cluster_ip)+':6002/user', json=data)

    return result.text
    