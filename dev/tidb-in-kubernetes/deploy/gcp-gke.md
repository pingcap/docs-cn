---
title: Deploy TiDB on GCP GKE
summary: Learn how to deploy a TiDB cluster on GCP GKE.
category: how-to
---

# Deploy TiDB on GCP GKE

This document describes how to deploy a TiDB cluster on GCP GKE with your laptop (Linux or macOS) for development or testing.

> **Warning:**
>
> The GKE support for multiple disks per node has [known issues](https://github.com/pingcap/tidb-operator/issues/684) that make it not ready for production usage. We are working to get GKE to resolve this issue.

## Prerequisites

First of all, make sure the following items are installed on your machine:

* git
* [Google Cloud SDK](https://cloud.google.com/sdk/install)
* [terraform](https://www.terraform.io/downloads.html) >= 0.12
* [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/#install-kubectl) >= 1.14
* [helm](https://github.com/helm/helm/blob/master/docs/install.md#installing-the-helm-client) >= 2.9.0 and < 3.0.0
* [jq](https://stedolan.github.io/jq/download/)

## Configure

Before deploying, you need to configure several items to guarantee a smooth deployment.
First download the source:

{{< copyable "shell-regular" >}}

```bash
git clone --depth=1 https://github.com/pingcap/tidb-operator && \
cd tidb-operator/deploy/gcp
```

### Configure Cloud SDK

After you install Google Cloud SDK, you need to run `gcloud init` to [perform initial setup tasks](https://cloud.google.com/sdk/docs/initializing).

### Configure APIs

If the GCP project is new, make sure the relevant APIs are enabled:

{{< copyable "shell-regular" >}}

```bash
gcloud services enable cloudresourcemanager.googleapis.com && \
gcloud services enable cloudbilling.googleapis.com && \
gcloud services enable iam.googleapis.com && \
gcloud services enable compute.googleapis.com && \
gcloud services enable container.googleapis.com
```

### Configure Terraform

The terraform script expects three environment variables. You can let Terraform prompt you for them, or `export` them in the `~/.bash_profile` file ahead of time. The required environment variables are:

* `TF_VAR_GCP_CREDENTIALS_PATH`: Path to a valid GCP credentials file.
    - It is recommended to create a new service account to be used by Terraform. See [this page](https://cloud.google.com/iam/docs/creating-managing-service-accounts) to create a service account and grant `Project Editor` role to it.
    - See [this page](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) to create service account keys, and choose `JSON` key type during creation. The downloaded `JSON` file that contains the private key is the credentials file you need.
* `TF_VAR_GCP_REGION`: The region to create the resources in, for example: `us-west1`.
* `TF_VAR_GCP_CREDENTIALS_PATH`: Path to a valid GCP credentials file.
    - It is recommended to create a new service account to be used by Terraform as shown in the below example.

Below we will set these environment variables

{{< copyable "shell-regular" >}}

```bash
# Replace the region with your GCP region and your GCP project name.
echo GCP_REGION=us-west1 >> terraform.tfvars
# First make sure you are connected to the correct project. gcloud config set project $PROJECT
echo "GCP_PROJECT=$(gcloud config get-value project)" >> terraform.tfvars
# Create a service account for terraform with restricted permissions and set the credentails path
./create-service-account.sh
```

## Deploy

You need to decide on instance types. If you just want to get a feel for a TiDB deployment and lower your cost, you can use the small settings.

{{< copyable "shell-regular" >}}

```bash
cat small.tfvars >> terraform.tfvars
```

{{< copyable "shell-regular" >}}

If you want to benchmark a production deployment, run:

```bash
cat prod.tfvars >> terraform.tfvars
```

The default setup creates a new VPC, two subnetworks, and an f1-micro instance as a bastion machine. The production setup is created with the following instance types as worker nodes:

* 3 n1-standard-4 instances for PD
* 3 n1-highmem-8 instances for TiKV
* 3 n1-standard-16 instances for TiDB
* 3 n1-standard-2 instances for monitor

> **Note:**
>
> The number of nodes created depends on how many availability zones there are in the chosen region. Most have 3 zones, but us-central1 has 4. See [Regions and Zones](https://cloud.google.com/compute/docs/regions-zones/) for more information and see the [Customize](#customize) section on how to customize node pools in a regional cluster.

The production setup, as listed above, requires at least 91 CPUs which exceed the default CPU quota of a GCP project. To increase your project's quota, follow the instructions [here](https://cloud.google.com/compute/quotas). You need more CPUs if you need to scale out.

Now that you have configured everything needed, you can launch the script to deploy the TiDB cluster:

{{< copyable "shell-regular" >}}

```bash
terraform init
```

{{< copyable "shell-regular" >}}

```bash
terraform apply
```

When you run `terraform apply`, you may be asked to set three environment variables if you have not exported them in advance. See [Configure Terraform](#configure-terraform) for details.

It might take 10 minutes or more to finish the process. A successful deployment gives the output like:

```
Apply complete! Resources: 17 added, 0 changed, 0 destroyed.

Outputs:

cluster_id = tidb
cluster_name = tidb
how_to_connect_to_mysql_from_bastion = mysql -h 172.31.252.20 -P 4000 -u root
how_to_ssh_to_bastion = gcloud compute ssh bastion --zone us-west1-b
kubeconfig_file = ./credentials/kubeconfig_tidb
monitor_ilb_ip = 35.227.134.146
monitor_port = 3000
region = us-west1
tidb_ilb_ip = 172.31.252.20
tidb_port = 4000
tidb_version = v3.0.0-rc.1
```

## Access the database

After `terraform apply` is successful, the TiDB cluster can be accessed by SSHing into the bastion machine and connecting via MySQL (Replace the `<>` parts with values from the output):

{{< copyable "shell-regular" >}}

```bash
gcloud compute ssh bastion --zone <zone>
```

{{< copyable "shell-regular" >}}

```bash
mysql -h <tidb_ilb_ip> -P 4000 -u root
```

> **Note:**
>
> You need to install the MySQL client before you connect to TiDB via MySQL.

## Interact with the cluster

You can interact with the cluster using `kubectl` and `helm` with the kubeconfig file `credentials/kubeconfig_<cluster_name>` as follows. The default `cluster_name` is `tidb`, which can be changed in `variables.tf`.

There are two ways to do this:

- By specifying --kubeconfig argument:

    {{< copyable "shell-regular" >}}

    ```bash
    kubectl --kubeconfig credentials/kubeconfig_<cluster_name> get po -n tidb
    ```

    {{< copyable "shell-regular" >}}

    ```bash
    helm --kubeconfig credentials/kubeconfig_<cluster_name> ls
    ```

- Or setting KUBECONFIG environment variable:

    {{< copyable "shell-regular" >}}

    ```bash
    export KUBECONFIG=$PWD/credentials/kubeconfig_<cluster_name>
    ```

    {{< copyable "shell-regular" >}}

    ```bash
    kubectl get po -n tidb
    ```

    {{< copyable "shell-regular" >}}

    ```bash
    helm ls
    ```

## Upgrade

To upgrade the TiDB cluster, modify the `tidb_version` variable to a higher version in the `variables.tf` file, and run `terraform apply`.

For example, to upgrade the cluster to the 3.0.0-rc.2 version, modify the `tidb_version` to `v3.0.0-rc.2`:

```
variable "tidb_version" {
  description = "TiDB version"
  default     = "v3.0.0-rc.2"
}
```

The upgrading does not finish immediately. You can run `kubectl --kubeconfig credentials/kubeconfig_<cluster_name> get po -n tidb --watch` to verify that all pods are in `Running` state. Then you can [access the database](#access-the-database) and use `tidb_version()` to see whether the cluster has been upgraded successfully:

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

## Scale

To scale the TiDB cluster, modify `tikv_count`, `tikv_replica_count`, `tidb_count`, and `tidb_replica_count` in the `variables.tf` file to your desired count, and run `terraform apply`.

Currently, scaling in is not supported since we cannot determine which node to remove. Scaling out needs a few minutes to complete, you can watch the scaling-out process by `kubectl --kubeconfig credentials/kubeconfig_<cluster_name> get po -n tidb --watch`.

For example, to scale out the cluster, you can modify the number of TiDB instances from 1 to 2:

```
variable "tidb_count" {
  description = "Number of TiDB nodes per availability zone"
  default     = 2
}
```

> **Note:**
>
> Incrementing the node count creates a node per GCP availability zone.

## Customize

You can change default values in `variables.tf` (such as the cluster name and the TiDB version) as needed.

### Customize GCP resources

GCP allows attaching a local SSD to any instance type that is `n1-standard-1` or greater. This allows for good customizability.

### Customize TiDB parameters

Currently, there are not too many parameters exposed to be customized. However, you can modify `templates/tidb-cluster-values.yaml.tpl` before deploying. If you modify it after the cluster is created and then run `terraform apply`, it can not take effect unless the pod(s) is manually deleted.

### Customize node pools

The cluster is created as a regional, as opposed to a zonal cluster. This means that GKE replicates node pools to each availability zone. This is desired to maintain high availability, however for the monitoring services, like Grafana, this is potentially unnecessary. It is possible to manually remove nodes if desired via `gcloud`.

> **Note:**
>
> GKE node pools are managed instance groups, so a node deleted by `gcloud compute instances delete` will be automatically recreated and added back to the cluster.

Suppose that you need to delete a node from the monitor pool. You can first do:

{{< copyable "shell-regular" >}}

```bash
gcloud compute instance-groups managed list | grep monitor
```

And the result will be something like this:

```
gke-tidb-monitor-pool-08578e18-grp  us-west1-b  zone   gke-tidb-monitor-pool-08578e18  0     0            gke-tidb-monitor-pool-08578e18  no
gke-tidb-monitor-pool-7e31100f-grp  us-west1-c  zone   gke-tidb-monitor-pool-7e31100f  1     1            gke-tidb-monitor-pool-7e31100f  no
gke-tidb-monitor-pool-78a961e5-grp  us-west1-a  zone   gke-tidb-monitor-pool-78a961e5  1     1            gke-tidb-monitor-pool-78a961e5  no
```

The first column is the name of the managed instance group, and the second column is the zone in which it was created. You also need the name of the instance in that group, and you can get it by running:

{{< copyable "shell-regular" >}}

```bash
gcloud compute instance-groups managed list-instances <the-name-of-the-managed-instance-group> --zone <zone>
```

For example:

{{< copyable "shell-regular" >}}

```bash
gcloud compute instance-groups managed list-instances gke-tidb-monitor-pool-08578e18-grp --zone us-west1-b
```

```
NAME                                       ZONE        STATUS   ACTION  INSTANCE_TEMPLATE                     VERSION_NAME  LAST_ERROR
gke-tidb-monitor-pool-08578e18-c7vd  us-west1-b  RUNNING  NONE    gke-tidb-monitor-pool-08578e18
```

Now you can delete the instance by specifying the name of the managed instance group and the name of the instance, for example:

{{< copyable "shell-regular" >}}

```bash
gcloud compute instance-groups managed delete-instances gke-tidb-monitor-pool-08578e18-grp --instances=gke-tidb-monitor-pool-08578e18-c7vd --zone us-west1-b
```

## Destroy

When you are done, the infrastructure can be torn down by running:

{{< copyable "shell-regular" >}}

```bash
terraform destroy
```

You have to manually delete disks in the Google Cloud Console, or with `gcloud` after running `terraform destroy` if you do not need the data anymore.

> **Note:**
>
> When `terraform destroy` is running, an error with the following message might occur: `Error reading Container Cluster "tidb": Cluster "tidb" has status "RECONCILING" with message""`. This happens when GCP is upgrading the kubernetes master node, which it does automatically at times. While this is happening, it is not possible to delete the cluster. When it is done, run `terraform destroy` again.
