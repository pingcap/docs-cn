---
title: Deploy TiDB to Kubernetes Locally
summary: Use TiDB Operator to quickly deploy a TiDB cluster on Kubernetes
category: how-to
aliases: ['/docs/op-guide/kubernetes-local/'] 
---

# Deploy TiDB to Kubernetes Locally

This document describes how to deploy a TiDB cluster to Kubernetes on your laptop (Linux or macOS) for development or testing.

[Docker in Docker](https://hub.docker.com/_/docker/) (DinD) runs Docker containers as virtual machines and runs another layer of Docker containers inside the first layer of Docker containers. [kubeadm-dind-cluster](https://github.com/kubernetes-sigs/kubeadm-dind-cluster) uses this technology to run the Kubernetes cluster in Docker containers. TiDB Operator uses a modified DinD script to manage the DinD Kubernetes cluster.

## Prerequisites

Before deploying a TiDB cluster to Kubernetes, make sure the following requirements are satisfied:

- Resources requirement: CPU 2+, Memory 4G+

    > **Note:**
    >
    > For macOS, you need to allocate 2+ CPU and 4G+ Memory to Docker. For details, see [Docker for Mac configuration](https://docs.docker.com/docker-for-mac/#advanced).

- [Docker](https://docs.docker.com/install/): 17.03 or later

    > **Note:**
    >
    > [Legacy Docker Toolbox](https://docs.docker.com/toolbox/toolbox_install_mac/) users must migrate to [Docker for Mac](https://store.docker.com/editions/community/docker-ce-desktop-mac) by uninstalling Legacy Docker Toolbox and installing Docker for Mac, because DinD cannot run on Docker Toolbox and Docker Machine.

- [Helm Client](https://github.com/helm/helm/blob/master/docs/install.md#installing-the-helm-client): 2.9.0 or later
- [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl): 1.10 or later

    > **Note:**
    >
    > The outputs of different versions of `kubectl` might be slightly different.

## Step 1: Deploy a Kubernetes cluster using DinD

```sh
$ git clone https://github.com/pingcap/tidb-operator
$ cd tidb-operator
$ manifests/local-dind/dind-cluster-v1.12.sh up
```

> **Note:**
>
> If the cluster fails to pull Docker images during the startup due to the firewall, you can set the environment variable `KUBE_REPO_PREFIX` to `uhub.ucloud.cn/pingcap` before running the script `dind-cluster-v1.12.sh` as follows (the Docker images used are pulled from [UCloud Docker Registry](https://docs.ucloud.cn/compute/uhub/index)):

```
$ KUBE_REPO_PREFIX=uhub.ucloud.cn/pingcap manifests/local-dind/dind-cluster-v1.12.sh up
```

## Step 2: Install TiDB Operator in the DinD Kubernetes cluster

Uncomment the `scheduler.kubeSchedulerImage` in `values.yaml`, set it to the same as your kubernetes cluster version.

```sh
$ kubectl apply -f manifests/crd.yaml

$ # This creates the custom resource for the cluster that the operator uses.
$ kubectl get customresourcedefinitions
NAME                             AGE
tidbclusters.pingcap.com         1m

$ # Install TiDB Operator into Kubernetes
$ helm install charts/tidb-operator --name=tidb-operator --namespace=tidb-admin

$ # wait operator running
$ kubectl get pods --namespace tidb-admin -l app.kubernetes.io/instance=tidb-operator
NAME                                       READY     STATUS    RESTARTS   AGE
tidb-controller-manager-5cd94748c7-jlvfs   1/1       Running   0          1m
tidb-scheduler-56757c896c-clzdg            2/2       Running   0          1m
```

## Step 3: Deploy a TiDB cluster in the DinD Kubernetes cluster

```sh
$ helm install charts/tidb-cluster --name=tidb-cluster --namespace=tidb
$ watch kubectl get pods --namespace tidb -l app.kubernetes.io/instance=tidb-cluster -o wide
$ # wait a few minutes to get all TiDB components created and ready

$ kubectl get tidbcluster -n tidb
NAME      AGE
demo      3m

$ kubectl get statefulset -n tidb
NAME        DESIRED   CURRENT   AGE
demo-pd     3         3         1m
demo-tidb   2         2         1m
demo-tikv   3         3         1m

$ kubectl get service -n tidb
NAME              TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                          AGE
demo-discovery    ClusterIP   10.96.146.139    <none>        10261/TCP                        1m
demo-grafana      NodePort    10.111.80.73     <none>        3000:32503/TCP                   1m
demo-pd           ClusterIP   10.110.192.154   <none>        2379/TCP                         1m
demo-pd-peer      ClusterIP   None             <none>        2380/TCP                         1m
demo-prometheus   NodePort    10.104.97.84     <none>        9090:32448/TCP                   1m
demo-tidb         NodePort    10.102.165.13    <none>        4000:32714/TCP,10080:32680/TCP   1m
demo-tidb-peer    ClusterIP   None             <none>        10080/TCP                        1m
demo-tikv-peer    ClusterIP   None             <none>        20160/TCP                        1m

$ kubectl get configmap -n tidb
NAME           DATA      AGE
demo-monitor   3         1m
demo-pd        2         1m
demo-tidb      2         1m
demo-tikv      2         1m

$ kubectl get pod -n tidb
NAME                              READY     STATUS      RESTARTS   AGE
demo-discovery-649c7bcbdc-t5r2k   2/2       Running     0          1m
demo-monitor-58745cf54f-gb8kd     2/2       Running     0          1m
demo-monitor-configurator-stvw6   0/1       Completed   0          1m
demo-pd-0                         1/1       Running     0          1m
demo-pd-1                         1/1       Running     0          1m
demo-pd-2                         1/1       Running     0          1m
demo-tidb-0                       1/1       Running     0          1m
demo-tidb-1                       1/1       Running     0          1m
demo-tikv-0                       2/2       Running     0          1m
demo-tikv-1                       2/2       Running     0          1m
demo-tikv-2                       2/2       Running     0          1m
```

To access the TiDB cluster, use `kubectl port-forward` to expose the services to host.

- Access TiDB using the MySQL client

    1. Use `kubectl` to forward the host machine port to the TiDB service port:

        ```sh
        $ kubectl port-forward svc/demo-tidb 4000:4000 --namespace=tidb
        ```

    2. To connect to TiDB using the MySQL client, open a new terminal tab or window and run the following command:

        ```sh
        $ mysql -h 127.0.0.1 -P 4000 -u root -p
        ```

- View the monitor dashboard

    1. Use `kubectl` to forward the host machine port to the Grafana service port:

        ```sh
        $ kubectl port-forward svc/demo-grafana 3000:3000 --namespace=tidb
        ```

    2. Open your web browser at http://localhost:3000 to access the Grafana monitoring interface.

        * Default username: admin
        * Default password: admin

## Scale the TiDB cluster

You can scale out or scale in the TiDB cluster simply by modifying the number of `replicas`.

1. Configure the `charts/tidb-cluster/values.yaml` file.

    For example, to scale out the cluster, you can modify the number of TiKV `replicas` from 3 to 5, or the number of TiDB `replicas` from 2 to 3.

2. Run the following command to apply the changes:

    ```sh
    helm upgrade tidb-cluster charts/tidb-cluster --namespace=tidb
    ```

> **Note:**
>
> If you need to scale in TiKV, the consumed time depends on the volume of your existing data, because the data needs to be migrated safely.

## Upgrade the TiDB cluster

1. Configure the `charts/tidb-cluster/values.yaml` file.

    For example, change the version of PD/TiKV/TiDB `image` to `v2.1.1`.

2. Run the following command to apply the changes:

    ```sh
    helm upgrade tidb-cluster charts/tidb-cluster --namespace=tidb
    ```

## Destroy the TiDB cluster

When you are done with your test, use the following command to destroy the TiDB cluster:

```sh
$ helm delete tidb-cluster --purge
```

> **Note:**
>
> This only deletes the running pods and other resources, the data is persisted. If you do not need the data anymore, run the following commands to clean up the data. (Be careful, this permanently deletes the data).

```sh
$ kubectl get pv -l app.kubernetes.io/namespace=tidb -o name | xargs -I {} kubectl patch {} -p '{"spec":{"persistentVolumeReclaimPolicy":"Delete"}}'
$ kubectl delete pvc --namespace tidb --all
```

## Stop and Re-start the Kubernetes cluster

* If you want to stop the DinD Kubernetes cluster, run the following command:

    ```sh
    $ manifests/local-dind/dind-cluster-v1.12.sh stop

    ```

* If you want to restart the DinD Kubernetes after you stop it, run the following command:

    ```
    $ manifests/local-dind/dind-cluster-v1.12.sh start
    ```

## Destroy the DinD Kubernetes cluster

If you want to clean up the DinD Kubernetes cluster and bring up a new cluster, run the following commands:

```sh
$ manifests/local-dind/dind-cluster-v1.12.sh clean
$ sudo rm -rf data/kube-node-*
$ manifests/local-dind/dind-cluster-v1.12.sh up
```

> **Warning:**
>
> You must clean the data after you destroy the DinD Kubernetes cluster, otherwise the TiDB cluster would fail to start when you bring it up again.
