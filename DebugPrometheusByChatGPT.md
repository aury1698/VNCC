Nonostante i passaggi che hai seguito siano corretti, sembra che Prometheus non riesca a connettersi all'endpoint delle metriche del tuo servizio. L'errore "connection refused" indica che qualcosa non sta esponendo correttamente le metriche sulla porta che hai specificato (6002) o che il pod non è accessibile da Prometheus.

Vediamo insieme le possibili cause e soluzioni.

### Possibili cause e soluzioni:

1. **Il container non espone correttamente la porta 8081 per le metriche**:
   - Il tuo Watchdog sta esponendo le metriche su `8081` (come hai verificato con il comando `curl localhost:6002/metrics`), ma potrebbe esserci un problema con la configurazione del servizio Kubernetes che reindirizza il traffico verso la porta del container.
   - Verifica che il servizio `iris-metrics-service` sia effettivamente in ascolto sulla porta `6002` e che la stia mappando correttamente a `8081`.

   **Comando di verifica:**
   `kubectl get svc iris-metrics-service -o yaml`

   Controlla che l'output mostri che la porta `6002` del servizio mappa correttamente alla porta `8081` del container.

   Se non vedi anomalie, prova a verificare la connettività all'interno del cluster con un `port-forward`:
   `kubectl port-forward svc/iris-metrics-service 6002:8081`
   E poi prova:
   `curl localhost:6002/metrics`

   Questo ti permetterà di confermare se effettivamente il servizio espone correttamente le metriche.

2. **Accesso ai servizi interni da parte di Prometheus**:
   - Verifica che il servizio di Prometheus riesca ad accedere ai pod Kubernetes.
   - Assicurati che il `ClusterRole` che hai creato conceda correttamente i permessi a Prometheus di accedere ai pod e ai loro endpoint. La parte relativa alle `nonResourceURLs` potrebbe non essere necessaria, ma il resto sembra a posto. Se questo non funziona, potresti provare a espandere la definizione del ClusterRole.

   **Controlla i log di Prometheus** per eventuali errori:
   `kubectl logs -l app=prometheus -n monitoring`

   I log ti diranno se ci sono ulteriori errori nella configurazione di scraping.

3. **Annotazioni non corrette o errate**:
   - Controlla nuovamente le annotazioni nel deployment del servizio `iris`. Le annotazioni devono corrispondere correttamente all'endpoint e alla porta dove Prometheus fa lo scraping.
   
   L'annotazione dovrebbe essere simile a:
   `yaml`
   `prometheus.io/scrape: "true"`
   `prometheus.io/port: "6002"`

4. **Problemi con il DNS Kubernetes o networking**:
   - Potrebbe esserci un problema di networking all'interno del cluster. Prova a verificare la connettività tra il pod di Prometheus e il pod `iris` utilizzando un container di debug.

   **Comando per avviare un container di debug**:
   `kubectl run -i --tty --rm debug --image=busybox --restart=Never -- sh`

   Dal container di debug, prova a fare un ping o una richiesta HTTP all'indirizzo del pod `iris` sulla porta `6002`.

5. **Verifica del deployment e stato dei pod**:
   - Controlla lo stato dei pod del tuo servizio `iris` per assicurarti che siano in esecuzione correttamente e che non abbiano errori.
   `kubectl get pods -l app=iris`
   `kubectl describe pod <nome-pod>`

6. **Logs del servizio Iris**:
   - Controlla anche i log del pod `iris` per vedere se ci sono errori relativi alla connessione o all'esposizione delle metriche:
   `kubectl logs <nome-pod-iris>`

### Riassumendo:
- Verifica che il servizio stia esponendo correttamente le metriche su `6002`.
- Assicurati che Prometheus abbia i permessi necessari per raccogliere le metriche.
- Controlla i log di Prometheus e del servizio Iris per eventuali errori di connessione.

