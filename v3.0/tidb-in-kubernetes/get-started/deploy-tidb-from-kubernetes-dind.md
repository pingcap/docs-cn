---
title: Deploy TiDB in Kubernetes Using DinD
summary: Learn how to quickly deploy a TiDB cluster in Kubernetes Using DinD.
category: how-to
---

# Deploy TiDB in Kubernetes Using DinD

This document describes how to deploy a TiDB cluster in Kubernetes on your laptop (Linux or macOS) for development or testing.

[Docker in Docker](https://hub.docker.com/_/docker/) (DinD) runs Docker containers as virtual machines, and runs another layer of Docker containers inside the first. [kubeadm-dind-cluster](https://github.com/kubernetes-sigs/kubeadm-dind-cluster) uses DinD to run Kubernetes clusters inside Docker containers. TiDB Operator uses a modified DinD script to manage the DinD Kubernetes cluster.

## Prerequisites

Before deployment, make sure the following requirements are satisfied:

- Resources requirement: CPU 2+, Memory 4G+

    > **Note:**
    >
    > For macOS, you need to allocate 2+ CPU and 4G+ Memory to Docker. For details, see [Docker for Mac configuration](https://docs.docker.com/docker-for-mac/#advanced).

- [Docker](https://docs.docker.com/install/): version >= 17.03

    > **Note:**
    >
    > - [Legacy Docker Toolbox](https://docs.docker.com/toolbox/toolbox_install_mac/) users must migrate to [Docker for Mac](https://store.docker.com/editions/community/docker-ce-desktop-mac) by uninstalling Legacy Docker Toolbox and installing Docker for Mac, because DinD cannot run on Docker Toolbox or Docker Machine.
    > - `kubeadm` validates the installed Docker version during installation. If you are using Docker later than 18.06, there will be warning messages in installation. The cluster might still be able to work normally, but it is recommended to use a Docker version between 17.03 and 18.06 for better compatibility. You can find older versions of docker [here](https://download.docker.com/).

- [Helm Client](https://github.com/helm/helm/blob/master/docs/install.md#installing-the-helm-client): version >= 2.9.0 and < 3.0.0
- [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl): 1.10 at least, 1.13 or later recommended

    > **Note:**
    >
    > The output might vary slightly for different versions of `kubectl`.

- For Linux users, `kubeadm` might produce warning messages during the installation process if you are using kernel 5.x or later versions. The cluster might still be able to work normally, but it is recommended to use kernel version 3.10+ or 4.x for better compatibility.

- `root` permissions are required to operate on the Docker daemon.

- Supported filesystem

    For Linux users, if the host machine uses an XFS filesystem (default in CentOS 7), it must be formatted with `ftype=1` to enable the `d_type` support, see [Docker's documentation](https://docs.docker.com/storage/storagedriver/overlayfs-driver/) for more details.

    You can check if your filesystem supports `d_type` using the `xfs_info / | grep ftype` command, where `/` is the data directory of your installed Docker daemon.

    If your root directory `/` uses XFS without the `d_type` support, but there is another partition does, or is using another filesystem, you can also change the data directory of Docker to use that partition.

    Assume a supported filesystem is mounted at path `/data`, use the following instructions to let Docker use it.

    Create a new directory for docker data storage:

    {{< copyable "shell-regular" >}}

    ```shell
    mkdir -p /data/docker
    ```

    Stop docker daemon:

    {{< copyable "shell-regular" >}}

    ```shell
    systemctl stop docker.service
    ```

    Make sure the `systemd` directory exist:

    {{< copyable "shell-regular" >}}

    ```shell
    mkdir -p /etc/systemd/system/docker.service.d/
    ```

    Overwrite config:

    {{< copyable "shell-regular" >}}

    ```shell
    cat << EOF > /etc/systemd/system/docker.service.d/docker-storage.conf
    [Service]
    ExecStart=
    ExecStart=/usr/bin/dockerd --data-root /data/docker -H fd:// --containerd=/run/containerd/containerd.sock
    EOF
    ```

    Restart docker daemon:

    {{< copyable "shell-regular" >}}

    ```shell
    systemctl daemon-reload && \
    systemctl start docker.service
    ```

## Step 1: Deploy a Kubernetes cluster using DinD

First, make sure that the docker daemon is running, and you can install and set up a Kubernetes cluster (version 1.12) using DinD for TiDB Operator with the script in our repository. Follow the steps below:

Clone the code:

{{< copyable "shell-regular" >}}

```shell
git clone --depth=1 https://github.com/pingcap/tidb-operator
```

Set up the cluster:

{{< copyable "shell-regular" >}}

```shell
cd tidb-operator && \
manifests/local-dind/dind-cluster-v1.12.sh up
```

If the cluster fails to pull Docker images during setup, you can set the environment variable `KUBE_REPO_PREFIX` to `uhub.ucloud.cn/pingcap` before running the script `dind-cluster-v1.12.sh` as follows (the Docker images are pulled from [UCloud Docker Registry](https://docs.ucloud.cn/compute/uhub/index) instead):

{{< copyable "shell-regular" >}}

```shell
KUBE_REPO_PREFIX=uhub.ucloud.cn/pingcap manifests/local-dind/dind-cluster-v1.12.sh up
```

An alternative solution is to configure HTTP proxies in DinD:

{{< copyable "shell-regular" >}}

```shell
export DIND_HTTP_PROXY=http://<ip>:<port> && \
export DIND_HTTPS_PROXY=http://<ip>:<port>
```

Export whitelist internal domains and IP addresses:

{{< copyable "shell-regular" >}}

```shell
export DIND_NO_PROXY=.svc,.local,127.0.0.1,0,1,2,3,4,5,6,7,8,9
```

{{< copyable "shell-regular" >}}

```shell
manifests/local-dind/dind-cluster-v1.12.sh up
```

There might be some warnings during the process due to various settings and environment of your system, but the command should exit without any error. You can verify whether the K8s cluster is up and running by using the following commands.

Get the cluster information:

{{< copyable "shell-regular" >}}

```shell
kubectl cluster-info
```

```
Kubernetes master is running at http://127.0.0.1:8080
KubeDNS is running at http://127.0.0.1:8080/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
kubernetes-dashboard is running at http://127.0.0.1:8080/api/v1/namespaces/kube-system/services/kubernetes-dashboard/proxy
```

List host nodes (they are docker containers in the DinD installation) in the cluster:

{{< copyable "shell-regular" >}}

```shell
kubectl get nodes -o wide
```

```
NAME          STATUS   ROLES    AGE     VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE                       KERNEL-VERSION               CONTAINER-RUNTIME
kube-master   Ready    master   11m     v1.12.5   10.192.0.2    <none>        Debian GNU/Linux 9 (stretch)   3.10.0-957.12.1.el7.x86_64   docker://18.9.0
kube-node-1   Ready    <none>   9m32s   v1.12.5   10.192.0.3    <none>        Debian GNU/Linux 9 (stretch)   3.10.0-957.12.1.el7.x86_64   docker://18.9.0
kube-node-2   Ready    <none>   9m32s   v1.12.5   10.192.0.4    <none>        Debian GNU/Linux 9 (stretch)   3.10.0-957.12.1.el7.x86_64   docker://18.9.0
kube-node-3   Ready    <none>   9m32s   v1.12.5   10.192.0.5    <none>        Debian GNU/Linux 9 (stretch)   3.10.0-957.12.1.el7.x86_64   docker://18.9.0
```

## Step 2: Install TiDB Operator in the DinD Kubernetes cluster

> **Note:**
>
> <chartVersion> will be used in the rest of the document to represent the chart version, e.g. `v1.0.0-rc.1`.

Once the K8s cluster is up and running, we can add chart repo and install TiDB Operator into it using `helm`:

1. Add the Helm chart repo:

    {{< copyable "shell-regular" >}}

    ```shell
    helm repo add pingcap https://charts.pingcap.org/ && \
    helm repo list && \
    helm repo update && \
    helm search tidb-cluster -l && \
    helm search tidb-operator -l
    ```

2. Install TiDB operator:

    {{< copyable "shell-regular" >}}

    ```shell
    helm install pingcap/tidb-operator --name=tidb-operator --namespace=tidb-admin --set scheduler.kubeSchedulerImageName=mirantis/hypokube --set scheduler.kubeSchedulerImageTag=final --version=<chartVersion>
    ```

3. Wait a few minutes until TiDB Operator is running:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl get pods --namespace tidb-admin -l app.kubernetes.io/instance=tidb-operator
    ```

    ```
    NAME                                       READY     STATUS    RESTARTS   AGE
    tidb-controller-manager-5cd94748c7-jlvfs   1/1       Running   0          1m
    tidb-scheduler-56757c896c-clzdg            2/2       Running   0          1m
    ```

## Step 3: Deploy a TiDB cluster in the DinD Kubernetes cluster

By using `helm` along with TiDB Operator, we can easily set up a TiDB cluster:

{{< copyable "shell-regular" >}}

```shell
helm install pingcap/tidb-cluster --name=demo --namespace=tidb --version=<chartVersion>
```

Wait a few minutes for all TiDB components to be created and ready:

{{< copyable "shell-regular" >}}

```shell
kubectl get pods --namespace tidb -l app.kubernetes.io/instance=demo -o wide --watch
```

> **Note:**
>
> You can use `Ctrl + C` to exit watch mode.

Get basic information of the TiDB cluster:

{{< copyable "shell-regular" >}}

```shell
kubectl get tidbcluster -n tidb
```

```
NAME   PD                       STORAGE   READY   DESIRE   TIKV                       STORAGE   READY   DESIRE   TIDB                       READY   DESIRE
demo   pingcap/pd:v3.0.0-rc.1   1Gi       3       3        pingcap/tikv:v3.0.0-rc.1   10Gi      3       3        pingcap/tidb:v3.0.0-rc.1   2       2
```

{{< copyable "shell-regular" >}}

```shell
kubectl get statefulset -n tidb
```

```
NAME        DESIRED   CURRENT   AGE
demo-pd     3         3         1m
demo-tidb   2         2         1m
demo-tikv   3         3         1m
```

{{< copyable "shell-regular" >}}

```shell
kubectl get service -n tidb
```

```
NAME              TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                          AGE
demo-discovery    ClusterIP   10.96.146.139    <none>        10261/TCP                        1m
demo-grafana      NodePort    10.111.80.73     <none>        3000:32503/TCP                   1m
demo-pd           ClusterIP   10.110.192.154   <none>        2379/TCP                         1m
demo-pd-peer      ClusterIP   None             <none>        2380/TCP                         1m
demo-prometheus   NodePort    10.104.97.84     <none>        9090:32448/TCP                   1m
demo-tidb         NodePort    10.102.165.13    <none>        4000:32714/TCP,10080:32680/TCP   1m
demo-tidb-peer    ClusterIP   None             <none>        10080/TCP                        1m
demo-tikv-peer    ClusterIP   None             <none>        20160/TCP                        1m
```

{{< copyable "shell-regular" >}}

```shell
kubectl get configmap -n tidb
```

```
NAME                              DATA   AGE
demo-monitor                      5      1m
demo-monitor-dashboard-extra-v3   2      1m
demo-monitor-dashboard-v2         5      1m
demo-monitor-dashboard-v3         5      1m
demo-pd                           2      1m
demo-tidb                         2      1m
demo-tikv                         2      1m
```

{{< copyable "shell-regular" >}}

```shell
kubectl get pod -n tidb
```

```
NAME                              READY     STATUS      RESTARTS   AGE
demo-discovery-649c7bcbdc-t5r2k   1/1       Running     0          1m
demo-monitor-58745cf54f-gb8kd     2/2       Running     0          1m
demo-pd-0                         1/1       Running     0          1m
demo-pd-1                         1/1       Running     0          1m
demo-pd-2                         1/1       Running     0          1m
demo-tidb-0                       1/1       Running     0          1m
demo-tidb-1                       1/1       Running     0          1m
demo-tikv-0                       1/1       Running     0          1m
demo-tikv-1                       1/1       Running     0          1m
demo-tikv-2                       1/1       Running     0          1m
```

## Access the database and monitor dashboards

To access the TiDB cluster, use `kubectl port-forward` to expose services to the host. The port number used in command are in `<host machine port>:<k8s service port>` format.

> **Note:**
>
> If you are deploying DinD on a remote machine rather than a local PC, there might be problems accessing "localhost" of that remote system. When you use `kubectl` 1.13 or later, you can expose the port on `0.0.0.0` instead of the default `127.0.0.1` by adding `--address 0.0.0.0` to the `kubectl port-forward` command.

- Access TiDB using the MySQL client

    Before you start testing your TiDB cluster, make sure you have installed a MySQL client.

    1. Use `kubectl` to forward the host machine port to the TiDB service port:

        {{< copyable "shell-regular" >}}

        ```shell
        kubectl port-forward svc/demo-tidb 4000:4000 --namespace=tidb
        ```

        > **Note:**
        >
        > If the proxy is set up sucessfully, it will print something like `Forwarding from 0.0.0.0:4000 -> 4000`. After testing, press `Ctrl + C` to stop the proxy and exit.

    2. To connect to TiDB using the MySQL client, open a new terminal tab or window and run the following command:

        {{< copyable "shell-regular" >}}

        ```shell
        mysql -h 127.0.0.1 -P 4000 -u root
        ```

- View the monitor dashboards

    1. Use `kubectl` to forward the host machine port to the Grafana service port:

        {{< copyable "shell-regular" >}}

        ```shell
        kubectl port-forward svc/demo-grafana 3000:3000 --namespace=tidb
        ```

        > **Note:**
        >
        > If the proxy is set up sucessfully, it will print something like `Forwarding from 0.0.0.0:3000 -> 3000`. After testing, press `Ctrl + C` to stop the proxy and exit.

    2. Then, open your web browser at http://localhost:3000 to access the Grafana monitoring interface.

        * Default username: admin
        * Default password: admin

- Permanent remote access

    Although this is a very simple demo cluster and does not apply to actual use scenarios, it is useful if the cluster can be accessed remotely without using `kubectl port-forward`, which might require an open terminal.

    TiDB, Prometheus, and Grafana are exposed as `NodePort` Services by default, so it is possible to set up a reverse proxy for them, as below:

    1. Find their listing port numbers using the following command:

        {{< copyable "shell-regular" >}}

        ```shell
        kubectl get service -n tidb | grep NodePort
        ```

        ```
        demo-grafana      NodePort    10.111.80.73     <none>        3000:32503/TCP                   1m
        demo-prometheus   NodePort    10.104.97.84     <none>        9090:32448/TCP                   1m
        demo-tidb         NodePort    10.102.165.13    <none>        4000:32714/TCP,10080:32680/TCP   1m
        ```

        In this sample output, the ports are: 32503 for Grafana, 32448 for Prometheus, and 32714 for TiDB.

    2. Find the host IP addresses of the cluster.

        DinD is a K8s cluster running inside Docker containers, so services expose ports to the containers' address, instead of the real host machine. We can find the IP addresses of Docker containers by using the following command:

        {{< copyable "shell-regular" >}}

        ```shell
        kubectl get nodes -o yaml | grep address
        ```

        ```
        addresses:
        - address: 10.192.0.2
        - address: kube-master
        addresses:
        - address: 10.192.0.3
        - address: kube-node-1
        addresses:
        - address: 10.192.0.4
        - address: kube-node-2
        addresses:
        - address: 10.192.0.5
        - address: kube-node-3
        ```

        Use the IP addresses for reverse proxy.

    3. Set up a reverse proxy.

        Either (or all) of the container IPs can be used as the upstream for a reverse proxy. You can use any reverse proxy server that supports TCP (for TiDB) or HTTP (for Grafana and Prometheus) to provide remote access. HAProxy and NGINX are two common choices.

## Scale the TiDB cluster

You can scale out or scale in the TiDB cluster simply by modifying the number of `replicas`.

1. Get the values.yaml of the current tidb-cluster chart:

    {{< copyable "shell-regular" >}}

    ```shell
    mkdir -p /home/tidb/demo && \
    helm inspect values pingcap/tidb-cluster --version=<chartVersion> > /home/tidb/demo/values-demo.yaml
    ```

2. Edit the `/home/tidb/demo/values-demo.yaml` file with your preferred text editor.

    For example, to scale out the cluster, you can modify the number of TiKV `replicas` from 3 to 5, or the number of TiDB `replicas` from 2 to 3.

3. Run the following command to apply the changes:

    {{< copyable "shell-regular" >}}

    ```shell
    helm upgrade demo pingcap/tidb-cluster --namespace=tidb -f /home/tidb/demo/values-demo.yaml --version=<chartVersion>
    ```
> **Note:**
>
> If you need to scale in TiKV, the consumed time depends on the volume of your existing data, because the data needs to be migrated safely.

Use `kubectl get pod -n tidb` to verify the number of each compoments equal to values in the `/home/tidb/demo/values-demo.yaml` file, and all pods are in `Running` state.

## Upgrade the TiDB cluster

1. Edit the `/home/tidb/demo/values-demo.yaml` file with your preferred text editor.

    For example, change the version of PD/TiKV/TiDB `image` to `v3.0.0-rc.2`.

2. Run the following command to apply the changes:

    {{< copyable "shell-regular" >}}

    ```shell
    helm upgrade demo pingcap/tidb-cluster --namespace=tidb -f /home/tidb/demo/values-demo.yaml --version=<chartVersion>
    ```

Use `kubectl get pod -n tidb` to verify whether all pods are in the `Running` state. Then you can connect to the database and use `tidb_version()` function to verify the version:

{{< copyable "sql" >}}

```sql
select tidb_version();
```

```
*************************** 1. row ***************************
tidb_version(): Release Version: v3.0.0-rc.2
Git Commit Hash: 06f3f63d5a87e7f0436c0618cf524fea7172eb93
Git Branch: HEAD
UTC Build Time: 2019-05-28 12:48:52
GoVersion: go version go1.12 linux/amd64
Race Enabled: false
TiKV Min Version: 2.1.0-alpha.1-ff3dd160846b7d1aed9079c389fc188f7f5ea13e
Check Table Before Drop: false
1 row in set (0.001 sec)
```

## Destroy the TiDB cluster

When you finish your test, use the following command to destroy the TiDB cluster:

{{< copyable "shell-regular" >}}

```shell
helm delete demo --purge
```

> **Note:**
>
> This only deletes the running pods and other resources. The data is persisted.

If you do not need the data anymore, run the following commands to clean up the data. 

{{< copyable "shell-regular" >}}

```shell
kubectl get pv -l app.kubernetes.io/namespace=tidb -o name | xargs -I {} kubectl patch {} -p '{"spec":{"persistentVolumeReclaimPolicy":"Delete"}}'
```

{{< copyable "shell-regular" >}}

```shell
kubectl delete pvc --namespace tidb --all
```

## Stop and Re-start the Kubernetes cluster

* If you want to stop the DinD Kubernetes cluster, run the following command:

    {{< copyable "shell-regular" >}}

    ```shell
    manifests/local-dind/dind-cluster-v1.12.sh stop
    ```

    You can use `docker ps` to verify that there is no docker container running.

* If you want to restart the DinD Kubernetes after you stop it, run the following command:

    {{< copyable "shell-regular" >}}

    ```shell
    manifests/local-dind/dind-cluster-v1.12.sh start
    ```

## Destroy the DinD Kubernetes cluster

If you want to clean up the DinD Kubernetes cluster, run the following commands:

{{< copyable "shell-regular" >}}

```shell
manifests/local-dind/dind-cluster-v1.12.sh clean && \
sudo rm -rf data/kube-node-*
```

> **Warning:**
>
> You must clean the data after you destroy the DinD Kubernetes cluster, otherwise the TiDB cluster would fail to start when you try to bring up a new cluster again.
