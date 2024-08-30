# HOW TO INSTALL PROMETHEUS AND GRAFANA

# Installare helm se non presente e verifica la versione
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
helm version

# Aggiungere il repository di Helm per Prometheus
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Installare Prometheus e creare namespace "monitoring"
helm install prometheus prometheus-community/prometheus --namespace monitoring --create-namespace

# Verifica stato del pod prima di accedere a Prometheus per vedere se tutte le componenti sono "Running"
kubectl get pods -n monitoring

# Dal comando precedente mi sono accorta dei problemi con le componenti Server e AlertManager, se a te già funzionassero per assurdo salta i passaggi da qua in poi e salta a "Accesso a Prometheus"

# Controlla così i volumi persistenti:
kubectl get pvc -n monitoring

# Allora da qui i passaggi di questo tizio online che hanno funzionato: https://github.com/prometheus-community/helm-charts/issues/4040

# Intallare con helm lo storage persistente OpenEBS e metterlo nel namespace "openebs"
helm repo add openebs https://openebs.github.io/openebs

helm repo update

helm install openebs --namespace openebs openebs/openebs --set engines.replicated.mayastor.enabled=false --create-namespace

# Salvare il pvc (persistent volume) in uno yml per il PROMETHEUS SERVER (da fare uguale poi per Alert)
kubectl get pvc prometheus-server -n monitoring -o yaml > prometheus-server-pvc.yaml

# Modifica del file YAML del PVC per aggiungere una riga per settare lo storage (va inserito allo stesso livello gerarchico di resources & di volumeMode, in mezzo a loro, quindi subito SOPRA di "volumeMode: Filesystem"):

storageClassName: openebs-hostpath

# Eliminare il PVC esistente (pare  necessario perché non si può semplicemente modificare il storageClassName di un pvc esistente)
kubectl delete pvc prometheus-server -n monitoring

# Applicazione del PVC modificato: questo creerà un nuovo pvc che utilizza lo storage class OpenEBS.
kubectl apply -f prometheus-server-pvc.yaml

# Controllare che sia andato a buon fine, dovrebbe apparire che ora il prometheus-SERVER è "Bound"/ Active
kubectl get pvc -n monitoring

# Ripetere i 5 step precedenti (da "Salvare il pvc in uno yml...") ma stavolta per ALERT-MANAGER, del tipo il primo step sarà:
kubectl get pvc storage-prometheus-alertmanager-0 -n monitoring -o yaml > storage-prometheus-alertmanager-pvc.yaml

# Accesso a Prometheus (se tutte le componenti sono running obv)
kubectl port-forward -n monitoring svc/prometheus-server 9090:80

# Installare Grafana per la visualizzazione (nello stesso namespace)
helm install grafana grafana/grafana --namespace monitoring

# Accedere a Grafana con le credenziali mostrate nel terminale dopo l'istallazione (user: admin)
kubectl port-forward -n monitoring svc/grafana 3000:80

# NON ANCORA PROVATO:
Una volta dentro Grafana,  configurare un nuovo datasource per Prometheus (http://prometheus-server.monitoring.svc.cluster.local) e importare dashboard predefinite per Kubernetes disponibili nel marketplace di Grafana.





