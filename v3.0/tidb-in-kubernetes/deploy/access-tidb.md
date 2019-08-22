---
title: Access the TiDB Cluster in Kubernetes
summary: Learn how to access the TiDB cluster in Kubernetes.
category: how-to
aliases: ['/docs/v3.0/how-to/deploy/orchestrated/tidb-in-kubernetes/access-tidb/','/docs/v3.0/how-to/deploy/tidb-in-kubernetes/access-tidb/']
---

# Access the TiDB Cluster in Kubernetes

This document describes how to access the TiDB cluster in Kubernetes.

+ To access the TiDB cluster within a Kubernetes cluster, use the TiDB service domain name `<release-name>-tidb.<namespace>`.
+ To access the TiDB cluster outside a Kubernetes cluster, expose the TiDB service port by editing the `tidb.service` field configuration in the `values.yaml` file of the `tidb-cluster` Helm chart.

    {{< copyable "" >}}

    ```yaml
    tidb:
    service:
        type: NodePort
        # externalTrafficPolicy: Cluster
        # annotations:
        # cloud.google.com/load-balancer-type: Internal
    ```

## NodePort

If there is no LoadBalancer, expose the TiDB service port in the following two modes of NodePort:

- `externalTrafficPolicy=Cluster`: All machines in the Kubernetes cluster assign a NodePort to TiDB Pod, which is the default mode.

    When using the `Cluster` mode, you can access the TiDB service by using the IP address of any machine plus a same port. If there is no TiDB Pod on the machine, the corresponding request is forwarded to the machine with a TiDB Pod.

    > **Note:**
    >
    > In this mode, the request's source IP obtained by the TiDB server is the node IP, not the real client's source IP. Therefore, the access control based on the client's source IP is not available in this mode.

- `externalTrafficPolicy=Local`: Only those machines that runs TiDB assign NodePort to TiDB Pod so that you can access local TiDB instances.

    When you use the `Local` mode, it is recommended to enable the `StableScheduling` feature of `tidb-scheduler`. `tidb-scheduler` tries to schedule the newly added TiDB instances to the existing machines during the upgrade process. With such scheduling, client outside the Kubernetes cluster does not need to upgrade configuration after TiDB is restarted.

### View the IP/PORT exposed in NodePort mode

To view the Node Port assigned by Service, run the following commands to obtain the Service object of TiDB:

{{< copyable "shell-regular" >}}

```shell
namespace=<your-tidb-namesapce>
```

{{< copyable "shell-regular" >}}

```shell
release=<your-tidb-release-name>
```

{{< copyable "shell-regular" >}}

```shell
kubectl -n <namespace> get svc <release-name>-tidb -ojsonpath="{.spec.ports[?(@.name=='mysql-client')].nodePort}{'\n'}"
```

To check you can access TiDB services by using the IP of what nodes, see the following two cases:

- When `externalTrafficPolicy` is configured as `Cluster`, you can use the IP of any node to access TiDB services.
- When `externalTrafficPolicy` is configured as `Local`, use the following commands to get the nodes where the TiDB instance of a specified cluster is located:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl -n <namespace> get pods -l "app.kubernetes.io/component=tidb,app.kubernetes.io/instance=<release-name>" -ojsonpath="{range .items[*]}{.spec.nodeName}{'\n'}{end}"
    ```

## LoadBalancer

If Kubernetes is run in an environment with LoadBalancer, such as GCP/AWS platform, it is recommended to use the LoadBalancer feature of these cloud platforms by setting `tidb.service.type=LoadBalancer`.

See [Kubernetes Service Documentation](https://kubernetes.io/docs/concepts/services-networking/service/) to know more about the features of Service and what LoadBalancer in the cloud platform supports.
