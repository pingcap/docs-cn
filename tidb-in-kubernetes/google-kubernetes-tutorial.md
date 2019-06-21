---
title: Deploy TiDB to Kubernetes on Google Cloud
summary: Learn how to deploy TiDB on Google Cloud using Kubernetes.
category: how-to
---

# Deploy TiDB to Kubernetes on Google Cloud

This tutorial is designed to be [run in Google Cloud Shell](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/pingcap/tidb-operator&tutorial=docs/google-kubernetes-tutorial.md). It takes you through these steps:

- Launch a new 3-node Kubernetes cluster (optional)
- Install the Helm package manager for Kubernetes
- Deploy the TiDB Operator
- Deploy your first TiDB cluster
- Connect to the TiDB cluster
- Scale out the TiDB cluster
- Shut down the Kubernetes cluster (optional)

## Select a project

This tutorial launches a 3-node Kubernetes cluster of `n1-standard-1` machines. Pricing information can be [found here](https://cloud.google.com/compute/pricing).

Please select a project before proceeding:

```
<walkthrough-project-billing-setup key="project-id">
</walkthrough-project-billing-setup>
```

## Enable API access

This tutorial requires use of the Compute and Container APIs. Please enable them before proceeding:

```
<walkthrough-enable-apis apis="container.googleapis.com,compute.googleapis.com">
</walkthrough-enable-apis>
```

## Configure gcloud defaults

This step defaults gcloud to your preferred project and [zone](https://cloud.google.com/compute/docs/regions-zones/), which simplifies the commands used for the rest of this tutorial:

{{< copyable "shell-regular" >}}

```shell
gcloud config set project {{project-id}}
```

{{< copyable "shell-regular" >}}

```shell
gcloud config set compute/zone us-west1-a
```

## Launch a 3-node Kubernetes cluster

It's now time to launch a 3-node kubernetes cluster! The following command launches a 3-node cluster of `n1-standard-1` machines.

It takes a few minutes to complete:

{{< copyable "shell-regular" >}}

```shell
gcloud container clusters create tidb
```

Once the cluster has launched, set it to be the default:

{{< copyable "shell-regular" >}}

```shell
gcloud config set container/cluster tidb
```

The last step is to verify that `kubectl` can connect to the cluster, and all three machines are running:

{{< copyable "shell-regular" >}}

```shell
kubectl get nodes
```

If you see `Ready` for all nodes, congratulations! You've setup your first Kubernetes cluster.

## Install Helm

Helm is the package manager for Kubernetes, and is what allows us to install all of the distributed components of TiDB in a single step. Helm requires both a server-side and a client-side component to be installed.

Install `helm`:

{{< copyable "shell-regular" >}}

```shell
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get | bash
```

Copy `helm` to your `$HOME` directory so that it persists after the Cloud Shell reaches its idle timeout:

{{< copyable "shell-regular" >}}

```shell
mkdir -p ~/bin && \
cp /usr/local/bin/helm ~/bin && \
echo 'PATH="$PATH:$HOME/bin"' >> ~/.bashrc
```

Helm also needs a couple of permissions to work properly:

{{< copyable "shell-regular" >}}

```shell
kubectl apply -f ./manifests/tiller-rbac.yaml && \
helm init --service-account tiller --upgrade
```

It takes a minute for helm to initialize `tiller`, its server component:

{{< copyable "shell-regular" >}}

```shell
watch "kubectl get pods --namespace kube-system | grep tiller"
```

When you see `Running`, it's time to hit <kbd>Ctrl</kbd>+<kbd>C</kbd> and proceed to the next step!

## Add Helm repo

Helm repo (http://charts.pingcap.org/) houses PingCAP managed charts, such as tidb-operator, tidb-cluster and tidb-backup, etc. Add and check the repo with following commands:

{{< copyable "shell-regular" >}}

```shell
helm repo add pingcap http://charts.pingcap.org/ && \
helm repo list
```

Then you can check the available charts:

{{< copyable "shell-regular" >}}

```shell
helm repo update
```

{{< copyable "shell-regular" >}}

```shell
helm search tidb-cluster -l
```

{{< copyable "shell-regular" >}}

```shell
helm search tidb-operator -l
```

## Deploy TiDB Operator

Note that `${chartVersion}` is used in the rest of the document to represent the chart version, e.g. `v1.0.0-beta.3`.

The first TiDB component we are going to install is the TiDB Operator, using a Helm Chart. TiDB Operator is the management system that works with Kubernetes to bootstrap your TiDB cluster and keep it running. This step assumes you are in the `tidb-operator` working directory:

{{< copyable "shell-regular" >}}

```shell
kubectl apply -f ./manifests/crd.yaml && \
kubectl apply -f ./manifests/gke/persistent-disk.yml && \
helm install pingcap/tidb-operator -n tidb-admin --namespace=tidb-admin --version=${chartVersion}
```

We can watch the operator come up with:

{{< copyable "shell-regular" >}}

```shell
watch kubectl get pods --namespace tidb-admin -o wide
```

When you see both tidb-scheduler and tidb-controller-manager are `Running`, press <kbd>Ctrl</kbd>+<kbd>C</kbd> and proceed to launch a TiDB cluster!

## Deploy your first TiDB cluster

Now with a single command we can bring-up a full TiDB cluster:

{{< copyable "shell-regular" >}}

```shell
helm install pingcap/tidb-cluster -n demo --namespace=tidb --set pd.storageClassName=pd-ssd,tikv.storageClassName=pd-ssd --version=${chartVersion}
```

It takes a few minutes to launch. You can monitor the progress with:

{{< copyable "shell-regular" >}}

```shell
watch kubectl get pods --namespace tidb -o wide
```

The TiDB cluster includes 2 TiDB pods, 3 TiKV pods, and 3 PD pods. When you see all pods `Running`, it's time to <kbd>Ctrl</kbd>+<kbd>C</kbd> and proceed forward!

## Connect to the TiDB cluster

There can be a small delay between the pod being up and running, and the service being available. You can watch list services available with:

{{< copyable "shell-regular" >}}

```shell
watch "kubectl get svc -n tidb"
```

When you see `demo-tidb` appear, you can <kbd>Ctrl</kbd>+<kbd>C</kbd>. The service is ready to connect to!

To connect to TiDB within the Kubernetes cluster, you can establish a tunnel between the TiDB service and your Cloud Shell. This is recommended only for debugging purposes, because the tunnel will not automatically be transferred if your Cloud Shell restarts. To establish a tunnel:

{{< copyable "shell-regular" >}}

```shell
kubectl -n tidb port-forward svc/demo-tidb 4000:4000 &>/tmp/port-forward.log &
```

From your Cloud Shell:

{{< copyable "shell-regular" >}}

```shell
sudo apt-get install -y mysql-client && \
mysql -h 127.0.0.1 -u root -P 4000
```

Try out a MySQL command inside your MySQL terminal:

{{< copyable "sql" >}}

```sql
select tidb_version();
```

If you did not specify a password in helm, set one now:

{{< copyable "sql" >}}

```sql
SET PASSWORD FOR 'root'@'%' = '<change-to-your-password>';
```

> **Note:**
>
> This command contains some special characters which cannot be auto-populated in the google cloud shell tutorial, so you might need to copy and paste it into your console manually.

Congratulations, you are now up and running with a distributed TiDB database compatible with MySQL!

## Scale out the TiDB cluster

With a single command we can easily scale out the TiDB cluster. To scale out TiKV:

{{< copyable "shell-regular" >}}

```shell
helm upgrade demo pingcap/tidb-cluster --set pd.storageClassName=pd-ssd,tikv.storageClassName=pd-ssd,tikv.replicas=5 --version=${chartVersion}
```

Now the number of TiKV pods is increased from the default 3 to 5. You can check it with:

{{< copyable "shell-regular" >}}

```shell
kubectl get po -n tidb
```

## Accessing the Grafana dashboard

To access the Grafana dashboards, you can create a tunnel between the Grafana service and your shell.
To do so, use the following command:

{{< copyable "shell-regular" >}}

```shell
kubectl -n tidb port-forward svc/demo-grafana 3000:3000 &>/dev/null &
```

In Cloud Shell, click on the Web Preview button and enter 3000 for the port. This opens a new browser tab pointing to the Grafana dashboards. Alternatively, use the following URL https://ssh.cloud.google.com/devshell/proxy?port=3000 in a new tab or window.

If not using Cloud Shell, point a browser to `localhost:3000`.

## Destroy the TiDB cluster

When the TiDB cluster is not needed, you can delete it with the following command:

{{< copyable "shell-regular" >}}

```shell
helm delete demo --purge
```

The above commands only delete the running pods, the data is persistent. If you do not need the data anymore, you should run the following commands to clean the data and the dynamically created persistent disks:

{{< copyable "shell-regular" >}}

```shell
kubectl delete pvc -n tidb -l app.kubernetes.io/instance=demo,app.kubernetes.io/managed-by=tidb-operator && \
kubectl get pv -l app.kubernetes.io/namespace=tidb,app.kubernetes.io/managed-by=tidb-operator,app.kubernetes.io/instance=demo -o name | xargs -I {} kubectl patch {} -p '{"spec":{"persistentVolumeReclaimPolicy":"Delete"}}'
```

## Shut down the Kubernetes cluster

Once you have finished experimenting, you can delete the Kubernetes cluster with:

{{< copyable "shell-regular" >}}

```shell
gcloud container clusters delete tidb
```
