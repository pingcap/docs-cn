---
title: Deploy TiDB on Alibaba Cloud Kubernetes
summary: Learn how to deploy a TiDB cluster on Alibaba Cloud Kubernetes.
category: how-to
---

# Deploy TiDB on Alibaba Cloud Kubernetes

This document describes how to deploy a TiDB cluster on Alibaba Cloud Kubernetes with your laptop (Linux or macOS) for development or testing.

## Prerequisites

- [aliyun-cli](https://github.com/aliyun/aliyun-cli) >= 3.0.15 and [configure aliyun-cli](https://www.alibabacloud.com/help/doc-detail/90766.htm?spm=a2c63.l28256.a3.4.7b52a893EFVglq)

    > **Note:**
    >
    > The access key must be granted permissions to control the corresponding resources.

- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/#install-kubectl) >= 1.12
- [helm](https://github.com/helm/helm/blob/master/docs/install.md#installing-the-helm-client) >= 2.9.1 and <= 2.11.0
- [jq](https://stedolan.github.io/jq/download/) >= 1.6
- [terraform](https://learn.hashicorp.com/terraform/getting-started/install.html) 0.11.*

You can use [Cloud Shell](https://shell.aliyun.com) of Alibaba Cloud to perform operations. All the tools have been pre-installed and configured in the Cloud Shell of Alibaba Cloud.

### Required privileges

To deploy a TiDB cluster, make sure you have the following privileges:

- AliyunECSFullAccess
- AliyunESSFullAccess
- AliyunVPCFullAccess
- AliyunSLBFullAccess
- AliyunCSFullAccess
- AliyunEIPFullAccess
- AliyunECIFullAccess
- AliyunVPNGatewayFullAccess
- AliyunNATGatewayFullAccess

## Overview of things to create

In the default configuration, you will create:

- A new VPC
- An ECS instance as the bastion machine
- A managed ACK (Alibaba Cloud Kubernetes) cluster with the following ECS instance worker nodes:

    - An auto-scaling group of 2 * instances (2 cores, 2 GB RAM) as ACK mandatory workers for the system service like CoreDNS
    - An auto-scaling group of 3 * `ecs.g5.large` instances for deploying the PD cluster
    - An auto-scaling group of 3 * `ecs.i2.2xlarge` instances for deploying the TiKV cluster
    - An auto-scaling group of 2 * `ecs.c5.4xlarge` instances for deploying the TiDB cluster
    - An auto-scaling group of 1 * `ecs.c5.xlarge` instance for deploying monitoring components
    - A 100 GB cloud disk used to store monitoring data

All the instances except ACK mandatory workers are deployed across availability zones (AZs) to provide cross-AZ high availability. The auto-scaling group ensures the desired number of healthy instances, so the cluster can auto-recover from node failure or even AZ failure.

## Deploy

1. Configure the target Region and Alibaba Cloud key (you can also set these variables in the `terraform` command prompt):

    {{< copyable "shell-regular" >}}

    ```shell
    export TF_VAR_ALICLOUD_REGION=<YOUR_REGION> && \
    export TF_VAR_ALICLOUD_ACCESS_KEY=<YOUR_ACCESS_KEY> && \
    export TF_VAR_ALICLOUD_SECRET_KEY=<YOUR_SECRET_KEY>
    ```

    The `variables.tf` file contains default settings of variables used for deploying the cluster. You can change it or use the `-var` option to override a specific variable to fit your need.

2. Use Terraform to set up the cluster.

    {{< copyable "shell-regular" >}}

    ```shell
    git clone --depth=1 https://github.com/pingcap/tidb-operator && \
    cd tidb-operator/deploy/aliyun
    ```

    Note that you must answer "yes" to `terraform apply` to continue:

    {{< copyable "shell-regular" >}}

    ```shell
    terraform init
    ```

    {{< copyable "shell-regular" >}}

    ```shell
    terraform apply
    ```

    If you get an error while running `terraform apply`, fix the error (for example, lack of permission) according to the error description and run `terraform apply` again.

    It takes 5 to 10 minutes to create the whole stack using `terraform apply`. Once installation is complete, the basic cluster information is printed:

    ```
    Apply complete! Resources: 3 added, 0 changed, 1 destroyed.

    Outputs:

    bastion_ip = 47.96.174.214
    cluster_id = c2d9b20854a194f158ef2bc8ea946f20e

    kubeconfig_file = /tidb-operator/deploy/aliyun/credentials/kubeconfig
    monitor_endpoint = 121.199.195.236:3000
    region = cn-hangzhou
    ssh_key_file = /tidb-operator/deploy/aliyun/credentials/my-cluster-keyZ.pem
    tidb_endpoint = 172.21.5.171:4000
    tidb_version = v3.0.0
    vpc_id = vpc-bp1v8i5rwsc7yh8dwyep5
    ```

    > **Note:**
    >
    > You can use the `terraform output` command to get the output again.

3. You can then interact with the ACK cluster using `kubectl` or `helm` (`cluster_name` is `tidb-cluster` by default):

    {{< copyable "shell-regular" >}}

    ```shell
    export KUBECONFIG=$PWD/credentials/kubeconfig_<cluster_name>
    ```

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl version
    ```

    {{< copyable "shell-regular" >}}

    ```shell
    helm ls
    ```

## Access the database

You can connect the TiDB cluster via the bastion instance. All necessary information is in the output printed after installation is finished (replace the `<>` parts with values from the output):

{{< copyable "shell-regular" >}}

```shell
ssh -i credentials/<cluster_name>-bastion-key.pem root@<bastion_ip>
```

{{< copyable "shell-regular" >}}

```shell
mysql -h <tidb_slb_ip> -P <tidb_port> -u root
```

## Monitor

Visit `<monitor_endpoint>` to view the Grafana dashboards. You can find this information in the output of installation.

The initial login user account and password:

- User: admin
- Password: admin

> **Warning:**
>
> It is strongly recommended to set `monitor_slb_network_type` to `intranet` in `variables.tf` for security if you already have a VPN connecting to your VPC or plan to set up one.

## Upgrade

To upgrade the TiDB cluster, set the `tidb_version` variable to a higher version in `variables.tf` and run `terraform apply`.

This may take a while to complete. You can watch the process using the following command:

{{< copyable "shell-regular" >}}

```shell
kubectl get pods --namespace tidb -o wide --watch
```

## Scale

To scale the TiDB cluster, modify `tikv_count` or `tidb_count` to your desired numbers, and then run `terraform apply`.

## Configure

### Configure TiDB Operator

You can adjust the `variables.tf` settings to configure TiDB Operator. Note that the `operator_helm_values` configuration item can provide a customized `values.yaml` configuration file for TiDB Operator. For example,

```hcl
variable "operator_helm_values" {
  default = file("my-operator-values.yaml")
}
```

In the default configuration, the Terraform script creates a new VPC. To use the existing VPC, set `vpc_id` in `variable.tf`. In this case, Kubernetes nodes are not deployed in AZs with vswitch not configured.

### Configure the TiDB cluster

`./my-cluster.yaml` is the `values.yaml` configuration file in the TiDB cluster. You can configure the TiDB cluster by modifying this file. For supported configuration items, see [Configure the TiDB cluster in Kubernetes](/dev/tidb-in-kubernetes/reference/configuration/tidb-cluster.md).

## Manage multiple TiDB clusters

To manage multiple TiDB clusters in a single Kubernetes cluster, you need to edit `./main.tf` and add the `tidb-cluster` declaration based on your needs. For example:

```hcl
module "tidb-cluster-dev" {
  source = "../modules/aliyun/tidb-cluster"
  providers = {
    helm = helm.default
  }

  cluster_name = "dev-cluster"
  ack          = module.tidb-operator

  pd_count                   = 1
  tikv_count                 = 1
  tidb_count                 = 1
  override_values            = file("dev-cluster.yaml")
}

module "tidb-cluster-staging" {
  source = "../modules/aliyun/tidb-cluster"
  providers = {
    helm = helm.default
  }

  cluster_name = "staging-cluster"
  ack          = module.tidb-operator

  pd_count                   = 3
  tikv_count                 = 3
  tidb_count                 = 2
  override_values            = file("staging-cluster.yaml")
}
```

> **Note:**
>
> You need to set a unique `cluster_name` for each TiDB cluster.

All the configurable parameters in `tidb-cluster` are as follows:

| Parameter | Description | Default value |
| :----- | :---- | :----- |
| `ack` | The structure that enwraps the target Kubernetes cluster information (required) | `nil` |
| `cluster_name` | The TiDB cluster name (required and unique) | `nil` |
| `tidb_version` | The TiDB cluster version | `v3.0.0` |
| `tidb_cluster_chart_version` | `tidb-cluster` helm chart version | `v1.0.0` |
| `pd_count` | The number of PD nodes | 3 |
| `pd_instance_type` | The PD instance type | `ecs.g5.large` |
| `tikv_count` | The number of TiKV nodes | 3 |
| `tikv_instance_type` | The TiKV instance type | `ecs.i2.2xlarge` |
| `tidb_count` | The number of TiDB nodes | 2 |
| `tidb_instance_type` | The TiDB instance type | `ecs.c5.4xlarge` |
| `monitor_instance_type` | The instance type of monitoring components | `ecs.c5.xlarge` |
| `override_values` | The `values.yaml` configuration file of the TiDB cluster. You can read it using the `file()` function | `nil` |
| `local_exec_interpreter` | The interpreter that executes the command line instruction | `["/bin/sh", "-c"]` |

## Manage multiple Kubernetes clusters

It is recommended to use a separate Terraform module to manage a specific Kubernetes cluster. (A Terraform module is a directory that contains the `.tf` script.)

`deploy/aliyun` combines multiple reusable Terraform scripts in `deploy/modules`. To manage multiple clusters, perform the following operations in the root directory of the `tidb-operator` project:

1. Create a directory for each cluster. For example:

    {{< copyable "shell-regular" >}}

    ```shell
    mkdir -p deploy/aliyun-staging
    ```

2. Refer to `main.tf` in `deploy/aliyun` and write your own script. For example:

    ```hcl
    provider "alicloud" {
        region     = <YOUR_REGION>
        access_key = <YOUR_ACCESS_KEY>
        secret_key = <YOUR_SECRET_KEY>
    }

    module "tidb-operator" {
        source     = "../modules/aliyun/tidb-operator"

        region          = <YOUR_REGION>
        access_key      = <YOUR_ACCESS_KEY>
        secret_key      = <YOUR_SECRET_KEY>
        cluster_name    = "example-cluster"
        key_file        = "ssh-key.pem"
        kubeconfig_file = "kubeconfig"
    }

    provider "helm" {
        alias    = "default"
        insecure = true
        install_tiller = false
        kubernetes {
            config_path = module.tidb-operator.kubeconfig_filename
        }
    }

    module "tidb-cluster" {
        source = "../modules/aliyun/tidb-cluster"
        providers = {
            helm = helm.default
        }

        cluster_name = "example-cluster"
        ack          = module.tidb-operator
    }

    module "bastion" {
        source = "../modules/aliyun/bastion"

        bastion_name             = "example-bastion"
        key_name                 = module.tidb-operator.key_name
        vpc_id                   = module.tidb-operator.vpc_id
        vswitch_id               = module.tidb-operator.vswitch_ids[0]
        enable_ssh_to_worker     = true
        worker_security_group_id = module.tidb-operator.security_group_id
    }
    ```

You can customize this script. For example, you can remove the `module "bastion"` declaration if you do not need the bastion machine.

> **Note:**
>
> You can copy the `deploy/aliyun` directory. But you cannot copy a directory on which the `terraform apply` operation is currently performed. In this case, it is recommended to clone the repository again and then copy it.

## Destroy

It may take a long time to finish destroying the cluster.

{{< copyable "shell-regular" >}}

```shell
terraform destroy
```

If you fail to create a Kubernetes cluster, an error is reported and you cannot clean the cluster normally when you try to destroy the cluster. In this case, you need to manually remove the Kubernetes resources from the local state and proceed to destroy the rest resources:

{{< copyable "shell-regular" >}}

```shell
terraform state list
```

{{< copyable "shell-regular" >}}

```shell
terraform state rm module.ack.alicloud_cs_managed_kubernetes.k8s
```

> **Note:**
>
> You have to manually delete the cloud disk used by monitoring node in the Alibaba Cloud console after destroying if you do not need it anymore.

## Limitation

You cannot change `pod cidr`, `service cidr` and worker instance types once the cluster is created.
