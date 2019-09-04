---
title: Deploy TiDB in the Minikube Cluster
summary: Learn how to deploy TiDB in the minikube cluster.
category: how-to
aliases: ['/docs/v3.0/how-to/get-started/deploy-tidb-from-kubernetes-minikube/']
---

# Deploy TiDB in the Minikube Cluster

This document describes how to deploy a TiDB cluster in the [minikube](https://kubernetes.io/docs/setup/minikube/) cluster.

> **Warning:**
>
> This is for testing only. DO NOT USE in production!

## Start a Kubernetes cluster with minikube

[Minikube](https://kubernetes.io/docs/setup/minikube/) can start a local Kubernetes cluster inside a VM on your laptop. It works on macOS, Linux, and Windows.

> **Note:**
>
> Although Minikube supports `--vm-driver=none` that uses host docker instead of VM, it is not fully tested with TiDB Operator and may not work. If you want to try TiDB Operator on a system without virtualization support (e.g., on a VPS), you might consider using [DinD](/v3.0/tidb-in-kubernetes/get-started/deploy-tidb-from-kubernetes-dind.md) instead.

### Install minikube and start a Kubernetes cluster

See [Installing Minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/) to install minikube (1.0.0+) on your machine.

After you installed minikube, you can run the following command to start a Kubernetes cluster.

```shell
minikube start
```

For Chinese mainland users, you may use local gcr.io mirrors such as `registry.cn-hangzhou.aliyuncs.com/google_containers`.

```shell
minikube start --image-repository registry.cn-hangzhou.aliyuncs.com/google_containers
```

Or you can configure HTTP/HTTPS proxy environments in your Docker:

```shell
# change 127.0.0.1:1086 to your http/https proxy server IP:PORT
minikube start --docker-env https_proxy=http://127.0.0.1:1086 \
  --docker-env http_proxy=http://127.0.0.1:1086
```

> **Note:**
>
> As minikube is running with VMs (default), the `127.0.0.1` is the VM itself, you might want to use your real IP address of the host machine in some cases.

See [minikube setup](https://kubernetes.io/docs/setup/minikube/) for more options to configure your virtual machine and Kubernetes cluster.

### Install kubectl to access the cluster

The Kubernetes command-line tool, [kubectl](https://kubernetes.io/docs/user-guide/kubectl/), allows you to run commands against Kubernetes clusters.

Install kubectl according to the instructions in [Install and Set Up kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/).

After kubectl is installed, test your minikube Kubernetes cluster:

```shell
kubectl cluster-info
```

## Install TiDB Operator and run a TiDB cluster

### Install helm

Helm is the package manager for Kubernetes and is what allows us to install all of the distributed components of TiDB in a single step. Helm requires both a server-side and a client-side component to be installed.

```shell
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get | bash
```

Install helm tiller:

```shell
helm init
```

If you have limited access to gcr.io, you can try a mirror. For example:

```shell
helm init --upgrade --tiller-image registry.cn-hangzhou.aliyuncs.com/google_containers/tiller:$(helm version --client --short | grep -P -o 'v\d+\.\d+\.\d')
```

Once it is installed, running `helm version` returns both the client and server version. For example:

```shell
$ helm version
Client: &version.Version{SemVer:"v2.13.1",
GitCommit:"618447cbf203d147601b4b9bd7f8c37a5d39fbb4", GitTreeState:"clean"}
Server: &version.Version{SemVer:"v2.13.1",
GitCommit:"618447cbf203d147601b4b9bd7f8c37a5d39fbb4", GitTreeState:"clean"}
```

If it shows only the client version, `helm` cannot yet connect to the server. Use `kubectl` to see if any tiller pods are running.

```shell
kubectl -n kube-system get pods -l app=helm
```

### Add Helm repo

Helm repo (`https://charts.pingcap.org/`) houses PingCAP managed charts, such as tidb-operator, tidb-cluster and tidb-backup, etc. Add and check the repo with following commands:

```shell
helm repo add pingcap https://charts.pingcap.org/
helm repo list
```

Then you can check the avaliable charts:

```shell
helm repo update
helm search tidb-cluster -l
helm search tidb-operator -l
```

### Install TiDB Operator in the Kubernetes cluster

> **Note:**
>
> <chartVersion> will be used in the rest of the document to represent the chart version, e.g. `v1.0.0`.

Clone tidb-operator repository:

```shell
git clone --depth=1 https://github.com/pingcap/tidb-operator
cd tidb-operator
kubectl apply -f ./manifests/crd.yaml
helm install pingcap/tidb-operator --name tidb-operator --namespace tidb-admin --version=<chartVersion>
```

Now, you can watch the operator come up using the following command:

```shell
kubectl get pods --namespace tidb-admin -o wide --watch
```

> **Note:**
>
> For Mac OS, if you are prompted "watch: command not found", you need to install the `watch` command using `brew install watch`. The same applies to other `watch` commands in this document.

If you have limited access to gcr.io (pods failed with ErrImagePull), you can try a mirror of kube-scheduler image. You can upgrade tidb-operator like this:

```shell
helm upgrade tidb-operator pingcap/tidb-operator --namespace tidb-admin --set \
  scheduler.kubeSchedulerImageName=registry.cn-hangzhou.aliyuncs.com/google_containers/kube-scheduler --version=<chartVersion>
```

When you see both tidb-scheduler and tidb-controller-manager are running, you can process to launch a TiDB cluster!

### Launch a TiDB cluster

To launch a TiDB cluster, use the following command:

```shell
helm install pingcap/tidb-cluster --name demo --set \
  schedulerName=default-scheduler,pd.storageClassName=standard,tikv.storageClassName=standard,pd.replicas=1,tikv.replicas=1,tidb.replicas=1 --version=<chartVersion>
```

You can watch the cluster up and running using:

```shell
kubectl get pods --namespace default -l app.kubernetes.io/instance=demo -o wide --watch
```

Use Ctrl+C to quit the watch mode.

### Test a TiDB cluster

Before you start testing your TiDB cluster, make sure you have installed a MySQL client. Note that there can be a small delay between the time when the pod is up and running, and when the service is available. You can watch the list of available services with:

```shell
kubectl get svc --watch
```

When you see `demo-tidb` appear, it's ready to connect to TiDB server.

To connect your MySQL client to the TiDB server, take the following steps:

1. Forward a local port to the TiDB port.

    ```shell
    kubectl port-forward svc/demo-tidb 4000:4000
    ```

2. In another terminal window, connect the TiDB server with a MySQL client:

    ```shell
    mysql -h 127.0.0.1 -P 4000 -uroot
    ```

    Or you can run a SQL command directly:

    ```shell
    mysql -h 127.0.0.1 -P 4000 -uroot -e 'select tidb_version();'
    ```

### Monitor TiDB cluster

To monitor the status of the TiDB cluster, take the following steps.

1. Forward a local port to the Grafana port.

    ```shell
    kubectl port-forward svc/demo-grafana 3000:3000
    ```

2. Open your browser, and access Grafana at `http://localhost:3000`.

    Alternatively, Minikube provides `minikube service` that exposes Grafana as a service for you to access more conveniently.

    ```shell
    minikube service demo-grafana
    ```

    And it will automatically set up the proxy and open the browser for Grafana.

### Delete TiDB cluster

Use the following commands to delete the demo cluster:

```shell
helm delete --purge demo

# update reclaim policy of PVs used by demo to Delete
kubectl get pv -l app.kubernetes.io/instance=demo -o name | xargs -I {} kubectl patch {} -p '{"spec":{"persistentVolumeReclaimPolicy":"Delete"}}'

# delete PVCs
kubectl delete pvc -l app.kubernetes.io/managed-by=tidb-operator
```

## FAQs

### TiDB cluster in minikube is not responding or responds slow

The minikube VM is configured by default to only use 2048MB of memory and 2 CPUs. You can allocate more resources during `minikube start` using the `--memory` and `--cpus` flag. Note that you'll need to recreate minikube VM for this to take effect.

```shell
minikube delete
minikube start --cpus 4 --memory 4096 ...
```
