# Monitoring

## Kubernetes Dashboard

Before setting up Prometheus for monitoring, it’s important to mention that Kubernetes comes with a default dashboard that can be used to monitor cluster performance, such as CPU and memory usage. However, in our case, the default Kubernetes dashboard didn’t display the required metrics properly, making it difficult to monitor our application.

## Prometheus
To address this issue, we decided to use Prometheus, as it's also integrated with OpenFaaS (with which we will be comparing resource usage between a monolithic Python application deployed on Kubernetes and the same application split into serverless functions). 
Prometheus offers a more flexible and robust way to collect and query metrics.

### Step 0: Getting the Prometheus Kubernetes Manifest Files
All the configuration files that are needed are hosted on Github. 
```sh
git clone https://github.com/techiescamp/kubernetes-prometheus
```

### Step 1: Create a Namespace
Create a dedicated Kubernetes namespace for all monitoring components. This is done so that all the Prometheus Kubernetes deployment objects will be installed in the same specific namespace.

Run the following command to create a new namespace called `monitoring`.
```sh
kubectl create namespace monitoring
```

### Step 2: Create a ClusterRole for RBAC policy
Prometheus uses Kubernetes APIs to read all the available metrics from nodes, pods, deployments... . For this reason, you need to create an RBAC policy with read access to the required API groups and bind the policy to the monitoring namespace.

Then create the role using the following command:

```sh
kubectl create -f prometheus\clusterRole.yaml
```

### Step 3: Create a Config Map To Externalize Prometheus Configurations

To facilitate easier management of Prometheus configurations and alert rules, you can use a Kubernetes ConfigMap. This approach allows you to update configurations without needing to rebuild the Prometheus image. 

The ConfigMap will mount the necessary configuration files into the `/etc/prometheus` directory of the Prometheus container, enabling dynamic discovery of pods and services within the Kubernetes cluster.

Create the ConfigMap in Kubernetes:

```sh
kubectl create -f prometheus\config-map.yaml
```

This command generates the configuration and alert rules needed for Prometheus to scrape metrics from your pods. The key scrape job, `kubernetes-pods`, allows Prometheus to discover metrics from pods annotated with `prometheus.io/scrape` and `prometheus.io/port`.

### Step 4: Annotate Your Services and Deployment for Prometheus Scraping
Since Prometheus expects to scrape metrics from specific sources, you need to add annotations to your deployment definitions so that Prometheus knows where to look for metrics within your pods.

The annotations need to be included in a specfic position in the yml, under the pod template in your deployment configuration: 

```sh

...
  template:
    metadata:
      labels:
        app: iris-monolitic
      annotations:
        prometheus.io/scrape: "true" # Indicates that Prometheus should scrape metrics from this pod.
        prometheus.io/port: "8081" # Specifies the port from which Prometheus should collect metrics.
    spec:
      containers:
      ....
        ports:
        - containerPort: 8080
        - containerPort: 8081
``` 


### Step 5: Create a Prometheus Deployment

The `prometheus\prometheus-deployment.yaml` mounts the Prometheus ConfigMap as files inside `/etc/prometheus`, as explained in the previous section. It is important to note that this deployment does not use persistent storage volumes for Prometheus storage, as this is a basic setup, while for production uses you should make sure to add persistent storage to the deployment.


###  Step 6: Connecting To Prometheus Dashboard 
 
With `kubectl port forwarding`, you can access a pod from your local workstation using a specified port on your localhost. 

First, get the Prometheus pod name with the following command:

```sh
kubectl get pods --namespace=monitoring
```

Execute the following command with your pod name to access Prometheus from localhost port <external-port>.

```sh
kubectl port-forward <prometheus-pod-name> <external-port>:9090 -n monitoring
```
Now, if you access `http://localhost:<external-port>` on your browser, you will get the Prometheus home page.

Otherwise, inside the `prometheus` folder the `prometheus-service.yaml` is included so that you don't have to run the `kubectl port-forward`  everytime you want to connect to the dashboard.

Once you have deployed the service, since this is a NodePort Service to connect to the dashboard you have to contact `https://<your-machine-IP:NodePort>`.

 Prometheus Dashboard, by navigating to Status --> Targets, you can see all the Kubernetes endpoints automatically connected to Prometheus through service discovery, as shown below.  
 
 
[!!!!! INSERIRE FOTO !!!!!]


Although Prometheus is now set up, we realized that understanding the default metrics from Prometheus can be challenging without an in-depth knowledge.
Additionally, writing custom queries in PromQL (Prometheus Query Language) can be time-consuming for beginners.

For these reasons, we chose to use Grafana,  a visualization tool that integrates seamlessly with Prometheus and provides a user-friendly interface with visual dashboards. Grafana simplifies the process of visualizing metrics with pre-built graphs and dashboards, without needing to write PromQL queries manually.


###  Step 7: Grafana

Install Grafana in the `monitoring` namespace (the same namespace where Prometheus was installed):

```sh 
kubectl -n monitoring run --image=stefanprodan/faas-grafana:4.6.3 --port=3000 grafana
1890  kubectl port-forward -n monitoring grafana 11111:3000
```

Access the Grafana dashboard by port-forwarding the Grafana service and logging in with the default credentials(user: `admin`, password: `admin`).
```sh
kubectl port-forward -n monitoring svc/grafana 3000:80
```
You can then access Grafana at `http://localhost:3000` and log in with the provided credentials.

Once logged into Grafana, follow these steps to configure Prometheus as your data source:
1. Go to **Configuration** → **Data Sources**.
2. Click on **Add data source** and select **Prometheus**.
3. Fill in the following details:
   - **Name**: Choose any name (e.g., `Prometheus`).
   - **Type**: Select **Prometheus**.
   - **URL**: Enter the Prometheus service URL. If you are using a NodePort service for Prometheus, as shown before, the URL would look like `http://<your-machine-IP>:<NodePort>`.
   - **Skip TLS Verification**: Check this option.
4. Click **Save & Test** to verify the connection. If the configuration is correct, you will see a success message.


Once the data source is configured, you can either create custom dashboards or import pre-built Kubernetes monitoring dashboards:


1. In the **Dashboards** section, click on **Import**.
2. Use the following ID to import a Kubernetes-specific dashboard from the Grafana community: **[315](https://grafana.com/grafana/dashboards/315)** (Kubernetes cluster monitoring dashboard).
3. Link the dashboard to the Prometheus data source you just created.
4. Once imported, you’ll be able to visualize all your Kubernetes metrics through this dashboard.








