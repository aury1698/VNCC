# Setting up Prometheus on a Kubernetes cluster for monitoring the Kubernetes cluster.

## Step 0: Getting the Prometheus Kubernetes Manifest Files
All the configuration files that needed are hosted on Github. You can clone the repo using the following command.
```sh
git clone https://github.com/techiescamp/kubernetes-prometheus`
```

## Step 1: Create a Namespace
Create a dedicated Kubernetes namespace for all monitoring components. Without this, the Prometheus Kubernetes deployment objects will be installed in the default namespace.

Run the following command to create a new namespace called `monitoring`."
```sh
kubectl create namespace monitoring
```

## Step 2: Create a ClusterRole for RBAC policy
Prometheus uses Kubernetes APIs to read all the available metrics from nodes, pods, deployments, and so on. For this reason, you need to create an RBAC policy with read access to the required API groups and bind the policy to the monitoring namespace.

Create a file named `clusterRole.yaml`: you can find it in `prometheus\clusterRole.yaml`.


Then create the role using the following command:
```sh
kubectl create -f clusterRole.yaml
```

## Step 3: Create a Config Map To Externalize Prometheus Configurations

To facilitate easier management of Prometheus configurations and alert rules, you can use a Kubernetes ConfigMap. This approach allows you to update configurations without needing to rebuild the Prometheus image. 

The ConfigMap will mount the necessary configuration files into the `/etc/prometheus` directory of the Prometheus container, enabling dynamic discovery of pods and services within the Kubernetes cluster.

1. Create a file named `config-map.yaml` and populate it with the contents from this link: [config-map.yaml](https://raw.githubusercontent.com/bibinwilson/kubernetes-prometheus/master/config-map.yaml).

2. Execute the following command to create the ConfigMap in Kubernetes:

```sh
kubectl create -f config-map.yaml
```

This command generates the configuration and alert rules needed for Prometheus to scrape metrics from your pods. The key scrape job, `kubernetes-pods`, allows Prometheus to discover metrics from pods annotated with `prometheus.io/scrape` and `prometheus.io/port`.

## Step 4: Annotate Your Services and Deployment for Prometheus Scraping
Since Prometheus expects to scrape metrics from specific sources, you need to add annotations to your service and deployment definitions. This informs Prometheus where to look for metrics within your pods.

Update your `iris-k8s-monolitic.yml` file to include the following annotations under the pod template in your deployment configuration:

```sh
apiVersion: v1
kind: Service
metadata:
  name: iris-monolitic-user-service
spec:
  selector:
    app: iris-monolitic
  ports:
  - protocol: "TCP"
    port: 7500
    targetPort: 8080
  type: ClusterIP

---
apiVersion: v1
kind: Service
metadata:
  name: iris-monolitic-admin-service
spec:
  selector:
    app: iris-monolitic
  ports:
  - protocol: "TCP"
    port: 7501
    targetPort: 8081
  type: ClusterIP

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: iris-monolitic
spec:
  selector:
    matchLabels:
      app: iris-monolitic
  replicas: 1
  template:
    metadata:
      labels:
        app: iris-monolitic
      annotations:
        prometheus.io/scrape: "true" # Indicates that Prometheus should scrape metrics from this pod.
        prometheus.io/port: "8081" # Specifies the port from which Prometheus should collect metrics.
    spec:
      containers:
      - name: iris-monolitic
        image: nicolacucina/iris-monolitic:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 8080
        - containerPort: 8081
```
Your `prometheus.yml` file should already be configured to scrape metrics from the annotated pods. 

Finally, apply your updated configuration:
`kubectl apply -f iris-k8s-monolitic.yml`

## Step 5: Create a Prometheus Deployment

Create a file named `prometheus-deployment.yaml`: you can see its structure in `prometheus\prometheus-deployment.` of this project.

This configuration mounts the Prometheus ConfigMap as files inside /etc/prometheus, as explained in the previous section. It is important to note that this deployment does not use persistent storage volumes for Prometheus storage, as this is a basic setup.

 Then, create a deployment on monitoring namespace using the above file.
`kubectl create  -f prometheus-deployment.yaml`
You can check the created deployment using the following command:
 `kubectl get deployments --namespace=monitoring`

 ##  Step 6: Connecting To Prometheus Dashboard using Kubectl port forwarding
 
With `kubectl port forwarding`, you can access a pod from your local workstation using a specified port on your localhost. 

First, get the Prometheus pod name with the following command:

```sh
kubectl get pods --namespace=monitoring
```

Execute the following command with your pod name to access Prometheus from localhost port 8080.

```sh
kubectl port-forward <prometheus-pod-name> 8080:9090 -n monitoring
```
Now, if you access `http://localhost:8080` on your browser, you will get the Prometheus home page.

Once inside Prometheus Dashboard, by navigating to Status --> Targets, you can see all the Kubernetes endpoints automatically connected to Prometheus through service discovery, as shown below.  [INSERIRE FOTO]