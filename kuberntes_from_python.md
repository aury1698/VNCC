Simply get the service and read its spec.cluster_ip property:

    from kubernetes import client, config
    config.load_kube_config()
    api = client.CoreV1Api()
    service = api.read_namespaced_service(name="kubernetes", namespace="default")
    print(service.spec.cluster_ip)
    # 10.100.0.1

