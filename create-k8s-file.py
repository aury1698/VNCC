import os

if __name__ == '__main__':
    name = "iris"
    image = "nicolacucina/iris-prova:latest"
    filename = name+"-k8s.yml"
    containerPort = 5000
    servicePort = 6000
    text = """apiVersion: v1
kind: Service
metadata:
  name: """+name+"""-service
spec:
  selector:
    app: """+name+"""
  ports:
  - protocol: "TCP"
    port: """+str(servicePort)+"""
    targetPort: """+str(containerPort)+"""
  type: LoadBalancer

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: """+name+"""
spec:
  selector:
    matchLabels:
      app: """+name+"""
  replicas: 2
  template:
    metadata:
      labels:
        app: """+name+"""
    spec:
      containers:
      - name: """+name+"""
        image: """+image+"""
        imagePullPolicy: Always
        ports:
        - containerPort: """+str(containerPort)
    print(text)
    
    with open(filename, "w") as f:
        f.write(text)
        