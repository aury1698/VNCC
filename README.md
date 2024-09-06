# HOW TO INSTALL PROMETHEUS AND GRAFANA

## Installare helm se non presente e verifica la versione
`curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash`

`helm version`

## Aggiungere il repository di Helm per Prometheus
`helm repo add prometheus-community https://prometheus-community.github.io/helm-charts `

`helm repo update`

## Installare Prometheus e creare namespace "monitoring"
`helm install prometheus prometheus-community/prometheus --namespace monitoring --create-namespace`

## Verifica stato del pod prima di accedere a Prometheus per vedere se tutte le componenti sono "Running"
`kubectl get pods -n monitoring`

## Dal comando precedente mi sono accorta dei problemi con le componenti Server e AlertManager, se a te già funzionassero per assurdo salta i passaggi da qua in poi e salta a "Accesso a Prometheus"

## Controlla così i volumi persistenti:
`kubectl get pvc -n monitoring`

## Allora da qui i passaggi di questo tizio online che hanno funzionato: https://github.com/prometheus-community/helm-charts/issues/4040

## Intallare con helm lo storage persistente OpenEBS e metterlo nel namespace "openebs"
`helm repo add openebs https://openebs.github.io/openebs`

`helm repo update`

`helm install openebs --namespace openebs openebs/openebs --set engines.replicated.mayastor.enabled=false --create-namespace`

## Salvare il pvc (persistent volume) in uno yml per il PROMETHEUS SERVER (da fare uguale poi per Alert)
`kubectl get pvc prometheus-server -n monitoring -o yaml > prometheus-server-pvc.yaml`

## Modifica del file YAML del PVC per aggiungere una riga per settare lo storage (va inserito allo stesso livello gerarchico di resources & di volumeMode, in mezzo a loro, quindi subito SOPRA di "volumeMode: Filesystem"):

`storageClassName: openebs-hostpath`

## Eliminare il PVC esistente (pare  necessario perché non si può semplicemente modificare il storageClassName di un pvc esistente)
`kubectl delete pvc prometheus-server -n monitoring`

## Applicazione del PVC modificato: questo creerà un nuovo pvc che utilizza lo storage class OpenEBS.
`kubectl apply -f prometheus-server-pvc.yaml`

## Controllare che sia andato a buon fine, dovrebbe apparire che ora il prometheus-SERVER è "Bound"/ Active
`kubectl get pvc -n monitoring`

## Ripetere i 5 step precedenti (da "Salvare il pvc in uno yml...") ma stavolta per ALERT-MANAGER, del tipo il primo step sarà:
`kubectl get pvc storage-prometheus-alertmanager-0 -n monitoring -o yaml > storage-prometheus-alertmanager-pvc.yaml`

## Accesso a Prometheus (se tutte le componenti sono running obv)
`kubectl port-forward -n monitoring svc/prometheus-server 9090:80`

## Installare Grafana per la visualizzazione (nello stesso namespace)
`helm install grafana grafana/grafana --namespace monitoring`

## Accedere a Grafana con le credenziali mostrate nel terminale dopo l'istallazione (user: admin)
`kubectl port-forward -n monitoring svc/grafana 3000:80`

## NON ANCORA PROVATO:
Una volta dentro Grafana,  configurare un nuovo datasource per Prometheus (http://prometheus-server.monitoring.svc.cluster.local) e importare dashboard predefinite per Kubernetes disponibili nel marketplace di Grafana.


## DA QUI: 05/09/2024

Guida utile su Prometheus: https://devopscube.com/setup-prometheus-monitoring-on-kubernetes/

- (Posto quanto fatto nei passi sopra per istallare Prometheus) 
Basandomi su github copilot ma soprattutto sulla documentazione: https://github.com/prometheus-community/helm-charts/tree/main/charts/prometheus  nella sezione "Configuration":

1. Nel nostro servizio iris-k9s-prova.yml ho aggiunto "`annotations: prometheus.io/scrape: "true" prometheus.io/port: "6002`" per dire a prometheus di raccogliere i dati dal pod.
Cioè (con aggiunta del servizio iris-metrics-service"): 

apiVersion: v1
kind: Service
metadata:
  name: iris-service
spec:
  selector:
    app: iris
  ports:
  - protocol: "TCP"
    port: 6000
    targetPort: 8080
  type: LoadBalancer

---
apiVersion: v1
kind: Service
metadata:
  name: iris-metrics-service
spec:
  selector:
    app: iris
  ports:
  - protocol: "TCP"
    port: 6002  # Porta per le metriche
    targetPort: 8081  # Porta del container dove il watchdog espone le metriche
  type: LoadBalancer

---
apiVersion: apps/v1
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
        prometheus.io/scrape: "true"  # Indica a Prometheus di raccogliere le metriche
        prometheus.io/port: "6002"  # Porta da cui raccogliere le metriche
    spec:
      containers:
      - name: iris
        image: nicolacucina/iris-prova:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 8080  # Porta principale dell'applicazione
        - containerPort: 8081  # Porta dove il watchdog espone le metriche


2. Allora si dovrebbe controllare che il file "prometheus.yml" sia configurato per raccogliere metriche dai pod annotati. 
L' ho trovato dentro la famosa ConfigMap, con il comando "`kubectl get configmap prometheus-server -n monitoring -o yaml`" e ho visto che lo yml di prometheus sembra okay già di default, infatti al suo interno troviamo una sezione tipo: 

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

3. A questo punto ho avviato il service:
`kubectl apply -f iris-k8s-prova.yml`

4. Solo dopo ho creato un file "clusterRole.yml" seguendo il solito sito "https://devopscube.com/setup-prometheus-monitoring-on-kubernetes/" che appare così:

apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: prometheus
rules:
- apiGroups: [""]
  resources:
  - nodes
  - nodes/proxy
  - services
  - endpoints
  - pods
  verbs: ["get", "list", "watch"]
- apiGroups:
  - extensions
  resources:
  - ingresses
  verbs: ["get", "list", "watch"]
- nonResourceURLs: ["/metrics"]
  verbs: ["get"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: prometheus
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: prometheus
subjects:
- kind: ServiceAccount
  name: default
  namespace: monitoring

- E poi ho creato il ruolo con `kubectl create -f clusterRole.yml`