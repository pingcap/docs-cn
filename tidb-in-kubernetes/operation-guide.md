---
title: TiDB Cluster Operation Guide
summary: TiDB Cluster Operation Guide
category: how-to
---
# TiDB Cluster Operation Guide

TiDB Operator can manage multiple clusters in the same Kubernetes cluster.

The following variables will be used in the rest of the document:

```shell
releaseName="demo"
namespace="tidb"
chartVersion="v1.0.0-beta.3"
```

## GKE

On GKE, local SSD volumes by default are limited to 375 GiB size and perform worse than persistent disk.

For proper performance, you must:

* install the Linux guest environment on the Ubuntu image or use a recent COS image
* make sure SSD is mounted with the `nobarrier` option.

We also have a [daemonset](https://raw.githubusercontent.com/pingcap/tidb-operator/master/manifests/gke/local-ssd-provision/local-ssd-provision.yaml) that

* fixes any performance issues
* remounts local SSD disks with a UUID for safety
* On Ubuntu combines all local SSD disks into one large disk with lvm tools.
* Run the local-volume-provisioner

The terraform deployment will automatically install that.

> **Note:**
>
> On Ubuntu this setup that combines local SSD assumes you are running only one process that needs local SSD per VM.

## Configuration

After Helm is deployed, get the values.yaml of current tidb-cluster chart:

{{< copyable "shell-regular" >}}

```shell
mkdir -p /home/tidb/${releaseName} && \
helm inspect values pingcap/tidb-cluster --version=${chartVersion} > /home/tidb/${releaseName}/values-${releaseName}.yaml
```
> **Note:** 
>
> The rest of the document will use `values.yaml` to reference `/home/tidb/${releaseName}/values-${releaseName}.yaml`

## Deploy TiDB cluster

After TiDB Operator and Helm are deployed correctly and configuration completed, TiDB cluster can be deployed using following command:

{{< copyable "shell-regular" >}}

```shell
helm install pingcap/tidb-cluster --name=${releaseName} --namespace=${namespace} --version=${chartVersion} -f /home/tidb/${releaseName}/values-${releaseName}.yaml
```

Check Pod status with following command:

{{< copyable "shell-regular" >}}

```shell
kubectl get po -n ${namespace} -l app.kubernetes.io/instance=${releaseName}
```

## Access TiDB cluster

By default TiDB service is exposed using [`NodePort`](https://kubernetes.io/docs/concepts/services-networking/service/#nodeport). You can modify it to `ClusterIP` which will disable access from outside of the cluster. Or modify it to [`LoadBalancer`](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer) if the underlining Kubernetes supports this kind of service.

{{< copyable "shell-regular" >}}

```shell
kubectl get svc -n ${namespace} # check the available services
```

By default the TiDB cluster has no root password set. Setting a password in helm is insecure. Instead you can set the name of a K8s secret as `tidb.passwordSecretName` in `values.yaml`. Note that this is only used to initialize users: once your tidb cluster is initialized you may delete the secret. The format of the secret is `user=password`, so you can set the root user password with:

{{< copyable "shell-regular" >}}

```shell
kubectl create namespace ${namespace} && \
kubectl create secret generic tidb-secret --from-literal=root=<root-password> --namespace=${namespace}
```

You can retrieve the password from the initialization `Secret`:

{{< copyable "shell-regular" >}}

```shell
PASSWORD=$(kubectl get secret -n ${namespace} tidb-secret -ojsonpath="{.data.root}" | base64 --decode) && \
echo ${PASSWORD}
```

* Access inside of the Kubernetes cluster

    When your application is deployed in the same Kubernetes cluster, you can access TiDB via domain name `demo-tidb.tidb.svc` with port `4000`. Here `demo` is the `releaseName`. And the latter `tidb` is the namespace you specified when using `helm install` to deploy TiDB cluster.

* Access outside of the Kubernetes cluster

    * Using kubectl portforward

        {{< copyable "shell-regular" >}}

        ```shell
        kubectl port-forward -n ${namespace} svc/${releaseName}-tidb 4000:4000 &>/tmp/portforward-tidb.log
        ```

        Access TiDB:

        {{< copyable "shell-regular" >}}
        
        ```shell
        mysql -h 127.0.0.1 -P 4000 -u root -p
        ```

    * Using LoadBalancer

        When you set `tidb.service.type` to `LoadBalancer` and the underlining Kubernetes support LoadBalancer, then a LoadBalancer will be created for TiDB service. You can access it via the external IP with port `4000`. Some cloud platforms support internal load balancer via service annotations, for example you can add annotation `cloud.google.com/load-balancer-type: Internal` to `tidb.service.annotations` to create an internal load balancer for TiDB on GKE.

    * Using NodePort

        You can access TiDB via any node's IP with tidb service node port. The node port is the port after `4000`, usually greater than `30000`.

## Scale TiDB cluster

TiDB Operator supports both horizontal and vertical scaling, but there are some caveats for storage vertical scaling.

* Kubernetes is v1.11 or later, please reference [the official blog](https://kubernetes.io/blog/2018/07/12/resizing-persistent-volumes-using-kubernetes/)
* Backend storage class supports resizing. (Currently only a limited of network storage class supports resizing)

When using local persistent volumes, even CPU and memory vertical scaling can cause problems because there may be not enough resources on the node.

Due to the above reasons, it's recommended to do horizontal scaling other than vertical scaling when workload increases.

### Horizontal scaling

To scale in/out TiDB cluster, just modify the `replicas` of PD, TiKV and TiDB in `values.yaml` file. And then run the following command:

{{< copyable "shell-regular" >}}

```shell
helm upgrade ${releaseName} pingcap/tidb-cluster --version=${chartVersion} -f /home/tidb/${releaseName}/values-${releaseName}.yaml
```

### Vertical scaling

To scale up/down TiDB cluster, modify the cpu/memory/storage limits and requests of PD, TiKV and TiDB in `values.yaml` file. And then run the same command as above.

> **Note:**
>
> See the above caveats of vertical scaling. Before [#35](https://github.com/pingcap/tidb-operator/issues/35) is fixed, you have to manually configure the block cache size for TiKV in `values.yaml`.

## Upgrade TiDB cluster

Upgrade TiDB cluster is similar to scale TiDB cluster, but by changing `image` of PD, TiKV and TiDB to different image versions in `values.yaml`. And then run the following command:

{{< copyable "shell-regular" >}}

```shell
helm upgrade ${releaseName} pingcap/tidb-cluster --version=${chartVersion} -f /home/tidb/${releaseName}/values-${releaseName}.yaml
```

For minor version upgrade, updating the `image` should be enough. When TiDB major version is out, the better way to update is to fetch the new values.yaml from new tidb-operator chart as described in the beginning and then merge the old values.yaml with new values.yaml. And then upgrade as above.

## Change TiDB cluster Configuration

Since `v1.0.0`, TiDB operator can perform rolling-update on configuration updates. This feature is disabled by default in favor of backward compatibility, you can enable it by setting `enableConfigMapRollout` to `true` in your helm values file.

> **Note:**
>
> Currently, changing PD's `scheduler` and `replication` configurations(`maxStoreDownTime` and `maxReplicas` in `values.yaml`, and all the configuration key under `[scheduler]` and `[replication]` section if you override the pd config file) after cluster creation has no effect. You have to configure these variables via `pd-ctl` after the cluster creation, see: [pd-ctl](https://pingcap.com/docs/dev/reference/tools/pd-control/)

> **WARN:**
>
> Changing this variable against a running cluster will trigger an rolling-update of PD/TiKV/TiDB pods even if there's no configuration change.

## Destroy TiDB cluster

To destroy TiDB cluster, run the following command:

{{< copyable "shell-regular" >}}

```shell
helm delete ${releaseName} --purge
```

The above command only delete the running pods, the data is persistent. If you do not need the data anymore, you can run the following command to clean the data:

{{< copyable "shell-regular" >}}

```shell
kubectl delete pvc -n ${namespace} -l app.kubernetes.io/instance=${releaseName},app.kubernetes.io/managed-by=tidb-operator && \
kubectl get pv -l app.kubernetes.io/namespace=${namespace},app.kubernetes.io/managed-by=tidb-operator,app.kubernetes.io/instance=${releaseName} -o name | xargs -I {} kubectl patch {} -p '{"spec":{"persistentVolumeReclaimPolicy":"Delete"}}'
```

> **Note:**
>
> The above command will delete the data permanently. Think twice before executing them.


## Monitor

TiDB cluster is monitored with Prometheus and Grafana. When TiDB cluster is created, a Prometheus and Grafana pod will be created and configured to scrape and visualize metrics.

By default the monitor data is not persistent, when the monitor pod is killed for some reason, the data will be lost. This can be avoided by specifying `monitor.persistent` to `true` in `values.yaml` file.

You can view the dashboard using `kubectl portforward`:

{{< copyable "shell-regular" >}}

```shell
kubectl port-forward -n ${namespace} svc/${releaseName}-grafana 3000:3000 &>/tmp/portforward-grafana.log
```

Then open your browser at http://localhost:3000 The default username and password are both `admin`

The Grafana service is exposed as `NodePort` by default, you can change it to `LoadBalancer` if the underlining Kubernetes has load balancer support. And then view the dashboard via load balancer endpoint.

## Backup and restore

TiDB Operator provides highly automated backup and recovery operations for a TiDB cluster. You can easily take full backup or setup incremental backup of a TiDB cluster, and restore the TiDB cluster when the cluster fails.

For detailed operation guides of backup and restore, refer to [Backup and Restore TiDB Cluster](./backup-restore.md).
