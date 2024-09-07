1. Come calcolare CPU usage & metrics in kubernetes

- https://signoz.io/guides/-how-to-calculate-containers-cpu-usage-in-kubernetes-with-prometheus-as-monitoring/

- https://last9.io/blog/guide-to-prometheus-query-language/ Guida per scrivere le query

- https://www.youtube.com/watch?v=hfKASyWzOIs dal minuto 14 fa vedere le query.

- https://devopscube.com/setup-prometheus-monitoring-on-kubernetes/  stesso concetto di query

- meno utile forse ma fatto bene: https://www.youtube.com/watch?v=fzny5uUaAeY

2. Le metriche su CPU e RAM per OpenFaas sono solo per la Pro Edition?

- Ho cercato ovunque ma non c'è risposta se NON nella documentazione, e pare che sì, sia così ma si possono vedere altre metriche tipo quante volte viene invocata una funzione o per quanti secondi viene eseguita etc.
- Addirittura ChatGPT dice "Se hai bisogno di monitorare le risorse come CPU e RAM nella versione gratuita, potresti considerare di fare monitoraggio a livello di Kubernetes usando Prometheus Node Exporter o Grafana o altre metriche di Kubernetes per monitorare l'uso delle risorse dei pod che eseguono le funzioni OpenFaaS."

A questo proposito, se usassimo grafana dice di fare: 
Sì, **Grafana** è incluso con OpenFaaS, e puoi utilizzarlo per monitorare le metriche dei tuoi servizi e funzioni OpenFaaS, anche nella versione gratuita. Se Grafana è già configurato, puoi aggiungere un **datasource Kubernetes** per visualizzare le metriche di CPU e RAM dei pod che eseguono le funzioni OpenFaaS.

### Passi per configurare Grafana con un datasource Kubernetes:

-- **Accedi a Grafana**:
   Se non l'hai già fatto, puoi esporre il servizio Grafana tramite port-forwarding. Per esempio:
   ```bash
   kubectl port-forward -n openfaas svc/grafana 3000:80
   ```
   Poi accedi a Grafana tramite `http://localhost:3000` nel browser.

-- **Aggiungi il datasource Kubernetes in Grafana**:
   Una volta dentro Grafana:
   - Vai su **Configuration** (icona dell'ingranaggio) → **Data Sources**.
   - Clicca su **Add data source**.
   - Cerca e seleziona **Prometheus** come tipo di datasource.
   
-- **Configura Prometheus come datasource**:
   Nella schermata di configurazione del datasource:
   - Imposta l'URL del **Prometheus server** che OpenFaaS utilizza. Di solito l'URL è qualcosa come `http://prometheus.openfaas.svc.cluster.local:9090`, se Prometheus è già configurato all'interno di OpenFaaS.
   - Salva la configurazione.

-- **Importa una dashboard per Kubernetes**:
   Dopo aver configurato Prometheus come datasource, puoi importare una dashboard per monitorare le metriche di Kubernetes, inclusi CPU, RAM e altre risorse:
   - Vai su **Create** → **Import**.
   - Cerca una dashboard preesistente per Kubernetes nel [Grafana Marketplace](https://grafana.com/grafana/dashboards/), come la dashboard **Kubernetes Cluster Monitoring** (ID 6417) o **Node Exporter Full** (ID 1860).
   - Inserisci l'ID della dashboard e clicca su **Load**.
   - Seleziona il datasource appena configurato (Prometheus) e importa la dashboard.

-- **Visualizza le metriche di CPU e RAM dei pod OpenFaaS**:
   Dopo aver importato la dashboard, dovresti vedere le metriche relative a CPU, RAM, rete e altro per i pod di Kubernetes, inclusi i pod OpenFaaS.

### Nota importante:
Poiché OpenFaaS utilizza Kubernetes per eseguire le funzioni, monitorando i **pod Kubernetes** otterrai le metriche delle risorse utilizzate da ogni funzione. Anche se non hai la versione Pro di OpenFaaS, puoi ottenere queste metriche a livello del pod tramite Kubernetes e visualizzarle in Grafana.

### Conclusione:
Sì, puoi utilizzare **Grafana incluso in OpenFaaS** per monitorare le metriche di CPU e RAM configurando un datasource Prometheus che monitora Kubernetes. Questo ti permetterà di accedere alle metriche sui pod delle funzioni OpenFaaS senza dover passare alla versione Pro.

3. Grafana è necessario?

- Pare di no, Prometheus dà dei grafici semplici pare anche per CPU. 

4. Ma se volessimo usare Grafana, uno per tutti o tutti per uno?

- Grafana è in grado di gestire più datasources, quindi non è necessario avere due istanze separate di Grafana. Puoi configurare due datasources distinti nella stessa istanza di Grafana:

Datasource 1: Prometheus che hai installato manualmente per Kubernetes.
Datasource 2: Prometheus già integrato con OpenFaaS.

Per farlo: In Grafana, vai su Configuration → Data Sources.
Aggiungi il primo datasource, che sarà quello di Prometheus per Kubernetes (il Prometheus che hai installato).
Poi, aggiungi il secondo datasource, che sarà Prometheus per OpenFaaS (già integrato).
Quando configuri i dashboard, puoi scegliere di utilizzare uno dei due datasource a seconda di cosa vuoi monitorare (Kubernetes monolitico o OpenFaaS serverless).

- Forse molto utile: https://medium.com/israeli-tech-radar/one-grafana-dashboard-with-multiple-prometheus-datasources-394a04ae4050

-Guida ufficiale Grafana per impostare Prometheus come Datasource : https://grafana.com/docs/grafana/latest/datasources/prometheus/configure-prometheus-data-source/

- Forse utile: https://stackoverflow.com/questions/63349357/how-to-configure-a-grafana-dashboard-for-multiple-prometheus-datasources


