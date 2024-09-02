## How to monitor Kubernetes with Prometheus

1.  Forse (according to copilot & https://github.com/prometheus-community/helm-charts/tree/main/charts/prometheus ) va messo in iris-k9s-prova.yml il "annotations: prometheus.io/scrape: "true" prometheus.io/port: "5000" per dire a prometheus di raccogliere i dati dal pod.

Cioè: 
"apiVersion: apps/v1
kind: Deployment
metadata:
  name: iris
spec:
  selector:
    matchLabels:
      app: iris
  replicas: 2
  template:
    metadata:
      labels:
        app: iris
      annotations:
        prometheus.io/scrape: "true" #per dire a Prometheus di raccogliere metriche da questo pod.
        prometheus.io/port: "5000"  #specifica la porta su cui deve raccogliere le metriche. 
    spec:
      containers:
      - name: iris
        image: nicolacucina/iris-prova:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 5000

2. Allora si dovrebbe controllare che il file prometheus.yml sia configurato per raccogliere metriche dai pod annotati. Del tipo: 

global:
  scrape_interval: 15s # Intervallo di raccolta delle metriche

scrape_configs:
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]  #Filtra i pod che hanno l'annotazione prometheus.io/scrape impostata su true.

        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_port]  #Sostituisce l'indirizzo di destinazione con il valore dell'annotazione prometheus.io/port.

        action: replace
        target_label: __address__
        regex: (.*)
        replacement: $1
      - source_labels: [__meta_kubernetes_pod_name]
        target_label: pod

3. Allora fai apply "kubectl apply -f iris-k8s-prova.yml"
