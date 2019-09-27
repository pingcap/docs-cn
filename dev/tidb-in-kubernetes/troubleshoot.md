---
title: Troubleshoot TiDB in Kubernetes
summary: Learn how to diagnose and resolve issues when you use TiDB in Kubernetes.
category: how-to
---

# Troubleshoot TiDB in Kubernetes

This document describes some common issues and solutions when you use a TiDB cluster in Kubernetes.

## Use the diagnostic mode

When a Pod is in the `CrashLoopBackoff` state, the containers in the Pod quit continually. As a result, you cannot use `kubectl exec` or `tkctl debug` normally, making it inconvenient to diagnose issues.

To solve this problem, TiDB in Kubernetes provides the Pod diagnostic mode for PD, TiKV, and TiDB components. In this mode, the containers in the Pod hang directly after starting, and will not get into a state of repeated crash. Then you can use `kubectl exec` or `tkctl debug` to connect to the Pod containers for diagnosis.

To use the diagnostic mode for troubleshooting:

1. Add an annotation to the Pod to be diagnosed:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl annotate pod <pod-name> -n <namespace> runmode=debug
    ```

    The next time the container in the Pod is restarted, it detects this annotation and enters the diagnostic mode.

2. Wait for the Pod to enter the Running state.

    {{< copyable "shell-regular" >}}

    ```shell
    watch kubectl get pod <pod-name> -n <namespace>
    ```

3. Start the diagnosis.

    Here's an example of using `kubectl exec` to get into the container for diagnosis:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl exec -it <pod-name> -n <namespace> -- /bin/sh
    ```

4. After finishing the diagnosis and resolving the problem, delete the Pod.

    ```shell
    kubectl delete pod <pod-name> -n <namespace>
    ```

    After the Pod is rebuilt, it automatically returns to the normal mode.

## Recover the cluster after accidental deletion

TiDB Operator uses PV (Persistent Volume) and PVC (Persistent Volume Claim) to store persistent data. If you accidentally delete a cluster using `helm delete`, the PV/PVC objects and data are still retained to ensure data safety.

To restore the cluster at this time, use the `helm install` command to create a cluster with the same name. The retained PV/PVC and data are reused.

{{< copyable "shell-regular" >}}

```shell
helm install pingcap/tidb-cluster -n <release-name> --namespace=<namespace> --version=<chart_version> -f values.yaml
```

## Pod is not created normally

After creating a cluster using `helm install`, if the Pod is not created, you can diagnose it using the following commands:

{{< copyable "shell-regular" >}}

```shell
kubectl get tidbclusters -n <namespace>
kubectl get statefulsets -n <namespace>
kubectl describe statefulsets -n <namespace> <release-name>-pd
```

## Network connection failure between Pods

In a TiDB cluster, you can access most Pods by using the Pod's domain name (allocated by the Headless Service). The exception is when TiDB Operator collects the cluster information or issues control commands, it accesses the PD (Placement Driver) cluster using the `service-name` of the PD service.

When you find some network connection issues between Pods from the log or monitoring metrics, or you find the network connection between Pods might be abnormal according to the problematic condition, you can follow the following process to diagnose and narrow down the problem:

1. Confirm that the endpoints of the Service and Headless Service are normal:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl -n <namespace> get endpoints <release-name>-pd
    kubectl -n <namespace> get endpoints <release-name>-tidb
    kubectl -n <namespace> get endpoints <release-name>-pd-peer
    kubectl -n <namespace> get endpoints <release-name>-tikv-peer
    kubectl -n <namespace> get endpoints <release-name>-tidb-peer
    ```

    The `ENDPOINTS` field shown in the above command should be a comma-separated list of `cluster_ip:port`. If the field is empty or incorrect, check the health of the Pod and whether `kube-controller-manager` is working properly.

2. Enter the Pod's Network Namespace to diagnose network problems:

    {{< copyable "shell-regular" >}}

    ```shell
    tkctl debug -n <namespace> <pod-name>
    ```

    After the remote shell is started, use the `dig` command to diagnose the DNS resolution. If the DNS resolution is abnormal, refer to [Debugging DNS Resolution](https://kubernetes.io/docs/tasks/administer-cluster/dns-debugging-resolution/) for troubleshooting.

    {{< copyable "shell-regular" >}}

    ```shell
    dig <HOSTNAME>
    ```

    Use the `ping` command to diagnose the connection with the destination IP (the ClusterIP resolved using `dig`):

    {{< copyable "shell-regular" >}}

    ```shell
    ping <TARGET_IP>
    ```

    - If the `ping` check fails, refer to [Debugging Kubernetes Networking](https://www.praqma.com/stories/debugging-kubernetes-networking/) for troubleshooting.

    - If the `ping` check succeeds, continue to check whether the target port is open by using `telnet`:

        {{< copyable "shell-regular" >}}

        ```shell
        telnet <target_ip> <target_port>
        ```

        If the `telnet` check fails, check whether the port corresponding to the Pod is correctly exposed and whether the applied port is correctly configured:

        {{< copyable "shell-regular" >}}

        ```shell
        # Checks whether the ports are consistent.
        kubectl -n <namespace> get po <pod-name> -ojson | jq '.spec.containers[].ports[].containerPort'

        # Checks whether the application is correctly configured to serve the specified port.
        # The default port of PD is 2379 when not configured.
        kubectl -n <namespace> -it exec <pod-name> -- cat /etc/pd/pd.toml | grep client-urls
        # The default port of PD is 20160 when not configured.
        kubectl -n <namespace> -it exec <pod-name> -- cat /etc/tikv/tikv.toml | grep addr
        # The default port of TiDB is 4000 when not configured.
        kubectl -n <namespace> -it exec <pod-name> -- cat /etc/tidb/tidb.toml | grep port
        ```

## The Pod is in the Pending state

The Pending state of a Pod is usually caused by conditions of insufficient resources, such as:

- The `StorageClass` of the PVC used by PD, TiKV, Monitor Pod does not exist or the PV is insufficient.
- No nodes in the Kubernetes cluster can satisfy the CPU or memory applied by the Pod

You can check the specific reason for Pending by using the `kubectl describe pod` command:

{{< copyable "shell-regular" >}}

```shell
kubectl describe po -n <namespace> <pod-name>
```

- If the CPU or memory resources are insufficient, you can lower the CPU or memory resources requested by the corresponding component for scheduling, or add a new Kubernetes node.

- If the `StorageClass` of the PVC cannot be found, delete the TiDB Pod and the corresponding PVC. Then, in the `values.yaml` file, change `storageClassName` to the name of the `StorageClass` available in the cluster. Run the following command to get the `StorageClass` available in the cluster:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl get storageclass
    ```

- If a `StorageClass` exists in the cluster but the available PV is insufficient, you need to add PV resources correspondingly. For Local PV, you can expand it by referring to [Local PV Configuration](/dev/tidb-in-kubernetes/reference/configuration/local-pv.md).

## The Pod is in the `CrashLoopBackOff` state

A Pod in the `CrashLoopBackOff` state means that the container in the Pod repeatedly aborts, in the loop of abort - restart by `kubelet` - abort. There are many potential causes of `CrashLoopBackOff`. In this case, the most effective way to locate it is to view the log of the Pod container:

{{< copyable "shell-regular" >}}

```shell
kubectl -n <namespace> logs -f <pod-name>
```

If the log fails to help diagnose the problem, you can add the `-p` parameter to output the log information when the container was last started:

{{< copyable "shell-regular" >}}

```shell
kubectl -n <namespace> logs -p <pod-name>
```

After checking the error messages in the log, you can refer to [Cannot start `tidb-server`](/dev/how-to/troubleshoot/cluster-setup.md#cannot-start-tidb-server), [Cannot start `tikv-server`](/dev/how-to/troubleshoot/cluster-setup.md#cannot-start-tikv-server), and [Cannot start `pd-server`](/dev/how-to/troubleshoot/cluster-setup.md#cannot-start-pd-server) for further troubleshooting.

In addition, TiKV might also fail to start when `ulimit` is insufficient. In this case, you can modify the `/etc/security/limits.conf` file of the Kubernetes node to increase the `ulimit`:

```
root soft nofile 1000000
root hard nofile 1000000
root soft core unlimited
root soft stack 10240
```

If you cannot confirm the cause from the log and `ulimit` is also a normal value, troubleshoot it further by using [the diagnostic mode](#use-the-diagnostic-mode).

## Unable to access the TiDB service

If you cannot access the TiDB service, first check whether the TiDB service is deployed successfully using the following method:

1. Check whether all components of the cluster are up and the status of each component is `Running`.

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl get po -n <namespace>
    ```

2. Check the log of TiDB components to see whether errors are reported.

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl logs -f <tidb-pod-name> -n <namespace> -c tidb
    ```

If the cluster is successfully deployed, check the network using the following steps:

1. If you cannot access the TiDB service using `NodePort`, try to access the TiDB service using the service domain or `clusterIP` on the node. If the `serviceName` or `clusterIP` works, the network within the Kubernetes cluster is normal. Then the possible issues are as follows:

    - Network failure exists between the client and the node.
    - Check whether the `externalTrafficPolicy` attribute of the TiDB service is `Local`. If it is `Local`, you must access the client using the IP of the node where the TiDB Pod is located.

2. If you still cannot access the TiDB service using the service domain or `clusterIP`, connect using `<PodIP>:4000` on the TiDB service backend. If the `PodIP` works, you can confirm that the problem is in the connection between the service domain and `PodIP` or between `clusterIP` and `PodIP`. Check the following items:

    - Check whether the DNS service works well.

        {{< copyable "shell-regular" >}}

        ```shell
        kubectl get po -n kube-system -l k8s-app=kube-dns
        dig <tidb-service-domain>
        ```

    - Check whether `kube-proxy` on each node is working.

        {{< copyable "shell-regular" >}}

        ```shell
        kubectl get po -n kube-system -l k8s-app=kube-proxy
        ```

    - Check whether the TiDB service rule is correct in the `iptables` rules.

        {{< copyable "shell-regular" >}}

        ```shell
        iptables-save -t nat |grep <clusterIP>
        ```

    - Check whether the corresponding endpoint is correct.

3. If you cannot access the TiDB service even using `PodIP`, the problem is on the Pod level network. Check the following items:

    - Check whether the relevant route rules on the node are correct.
    - Check whether the network plugin service works well.
    - Refer to [network connection failure between Pods](#network-connection-failure-between-pods) section.

## TiKV Store is in `Tombstone` status abnormally

Normally, when a TiKV Pod is in a healthy state (`Running`), the corresponding TiKV store is also in a healthy state (`UP`). However, concurrent scale-in or scale-out on TiKV components might cause part of TiKV stores to fall into the `Tombstone` state abnormally. When this happens, try the following steps to fix it:

1. View the state of the TiKV store:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl get -n <namespace> tidbcluster <release-name> -ojson | jq '.status.tikv.stores'
    ```

2. View the state of the TiKV Pod:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl get -n <namespace> po -l app.kubernetes.io/component=tikv
    ```

3. Compare the state of the TiKV store with that of the Pod. If the store corresponding to a TiKV Pod is in the `Offline` state, it means the store is being taken offline abnormally. You can use the following commands to cancel the offline process and perform recovery operations:

    1. Open the connection to the PD service:

        {{< copyable "shell-regular" >}}

        ```shell
        kubectl port-forward -n <namespace> svc/<cluster-name>-pd <local-port>:2379 &>/tmp/portforward-pd.log &
        ```

    2. Bring online the corresponding store:

        {{< copyable "shell-regular" >}}

        ```shell
        curl -X POST http://127.0.0.1:2379/pd/api/v1/store/<store-id>/state?state=Up
        ```

4. If the TiKV store with the latest `lastHeartbeatTime` that corresponds to a Pod is in a `Tombstone` state, it means that the offline process is completed. At this time, you need to re-create the Pod and bind it with a new PV to perform recovery by taking the following steps:

    1. Set the `reclaimPolicy` value of the PV corresponding to the store to `Delete`:

        {{< copyable "shell-regular" >}}

        ```shell
        kubectl patch $(kubectl get pv -l app.kubernetes.io/instance=<release-name>,tidb.pingcap.com/store-id=<store-id> -o name) -p '{"spec":{"persistentVolumeReclaimPolicy":"Delete"}}
        ```

    2. Remove the PVC used by the Pod:

        {{< copyable "shell-regular" >}}

        ```shell
        kubectl delete -n <namespace> pvc tikv-<pod-name> --wait=false
        ```

    3. Remove the Pod, and wait for it to be re-created:

        {{< copyable "shell-regular" >}}

        ```shell
        kubectl delete -n <namespace> pod <pod-name>
        ```

    After the Pod is re-created, a new store is registered in the TiKV cluster. Then the recovery is completed.
