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
    > The access key used must be granted permissions to control resources.

- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/#install-kubectl) >= 1.12
- [helm](https://github.com/helm/helm/blob/master/docs/install.md#installing-the-helm-client) >= 2.9.1 and <= 2.11.0
- [jq](https://stedolan.github.io/jq/download/) >= 1.6
- [terraform](https://learn.hashicorp.com/terraform/getting-started/install.html) 0.11.*

### Privileges

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

## Overview

The default setup creates:

- A new VPC
- An ECS instance as the bastion machine
- A managed ACK (Alibaba Cloud Kubernetes) cluster with the following ECS instance worker nodes:

    - An auto-scaling group of 2 * instances (2c2g) as ACK mandatory workers for system service like CoreDNS
    - An auto-scaling group of 3 * `ecs.i2.xlarge` instances for PD
    - An auto-scaling group of 3 * `ecs.i2.2xlarge` instances for TiKV
    - An auto-scaling group of 2 * instances (16c32g) for TiDB
    - An auto-scaling group of 1 * instance (4c8g) for monitoring components

In addition, the monitoring node mounts a 500GB cloud disk as data volume. All the instances except ACK mandatory workers span in multiple available zones to provide cross-AZ high availability.

The auto-scaling group ensures the desired number of healthy instances, so the cluster can auto-recover from node failure or even available zone failure.

## Deploy

Configure the target region and credential (you can also set these variables in `terraform` command prompt):

{{< copyable "shell-regular" >}}

```shell
export TF_VAR_ALICLOUD_REGION=<YOUR_REGION> && \
export TF_VAR_ALICLOUD_ACCESS_KEY=<YOUR_ACCESS_KEY> && \
export TF_VAR_ALICLOUD_SECRET_KEY=<YOUR_SECRET_KEY>
```

The `variables.tf` file contains default settings of variables used for deploying the cluster, you can change it or use `-var` option to override a specific variable to fit your need.

Use the following commands to set up the cluster.

Get the code from Github:

{{< copyable "shell-regular" >}}

```shell
git clone --depth=1 https://github.com/pingcap/tidb-operator && \
cd tidb-operator/deploy/aliyun
```

Apply the configs, note that you must answer "yes" to `terraform apply` to continue:

{{< copyable "shell-regular" >}}

```shell
terraform init
```

{{< copyable "shell-regular" >}}

```shell
terraform apply
```

If you get an error while running `terraform apply`, fix the error (for example, lack of permission) according to the description and run `terraform apply` again.

`terraform apply` takes 5 to 10 minutes to create the whole stack, once complete, basic cluster information is printed:

```
Apply complete! Resources: 3 added, 0 changed, 1 destroyed.

Outputs:

bastion_ip = 1.2.3.4
bastion_key_file = /root/tidb-operator/deploy/aliyun/credentials/tidb-cluster-bastion-key.pem
cluster_id = ca57c6071f31f458da66965ceddd1c31b
kubeconfig_file = /root/tidb-operator/deploy/aliyun/.terraform/modules/a2078f76522ae433133fc16e24bd21ae/kubeconfig_tidb-cluster
monitor_endpoint = 1.2.3.4:3000
region = cn-hangzhou
tidb_port = 4000
tidb_slb_ip = 192.168.5.53
tidb_version = v3.0.0-rc.1
vpc_id = vpc-bp16wcbu0xhbg833fymmc
worker_key_file = /root/tidb-operator/deploy/aliyun/credentials/tidb-cluster-node-key.pem
```

> **Note:**
>
> You can use the `terraform output` command to get the output again.

You can then interact with the ACK cluster using `kubectl` and `helm` (`cluster_name` is `tidb-cluster` by default):

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

You can connect the TiDB cluster via the bastion instance, all necessary information are in the output printed after installation is finished (replace the `<>` parts with values from the output):

{{< copyable "shell-regular" >}}

```shell
ssh -i credentials/<cluster_name>-bastion-key.pem root@<bastion_ip>
```

{{< copyable "shell-regular" >}}

```shell
mysql -h <tidb_slb_ip> -P <tidb_port> -u root
```

## Monitor

Visit `<monitor_endpoint>` to view the grafana dashboards. You can find this information in the output of installation.

The initial login credentials are:

- User: admin
- Password: admin

> **Warning:**
>
> It is strongly recommended to set `monitor_slb_network_type` to `intranet` in `variables.tf` for security if you already have a VPN connecting to your VPC or plan to setup one.

## Upgrade

To upgrade TiDB cluster, modify `tidb_version` variable to a higher version in `variables.tf` and run `terraform apply`.

This may take a while to complete, watch the process using command:

{{< copyable "shell-regular" >}}

```shell
kubectl get pods --namespace tidb -o wide --watch
```

## Scale

To scale the TiDB cluster, modify `tikv_count` or `tidb_count` to your desired numbers, and then run `terraform apply`.

## Customize

By default, the terraform script will create a new VPC. You can use an existing VPC by setting `vpc_id` to use an existing VPC. Note that kubernetes node will only be created in available zones that has vswitch existed when using existing VPC.

An ecs instance is also created by default as bastion machine to connect to the created TiDB cluster, because the TiDB service is only exposed to intranet. The bastion instance has mysql-cli and sysbench installed that helps you use and test TiDB.

If you don't have to access TiDB from internet, you could disable the creation of bastion instance by setting `create_bastion` to false in `variables.tf`

The worker node instance types are also configurable, there are two ways to configure that:

1. by specifying instance type id
2. by specifying capacity like instance cpu count and memory size

Because the Alibaba Cloud offers different instance types in different region, it is recommended to specify the capacity instead of certain type. You can configure these in the `variables.tf`, note that instance type overrides capacity configurations.

There is an exception for PD and TiKV instances, because PD and TiKV required local SSD, so you cannot specify instance types for them. Instead, you can choose the type family among `ecs.i1`,`ecs.i2` and `ecs.i2g`, which has one or more local NVMe SSD, and select a certain type in the type family by specifying `instance_memory_size`.

For more customization options, please refer to `variables.tf`.

## Destroy

It may take some while to finish destroying the cluster.

{{< copyable "shell-regular" >}}

```shell
terraform destroy
```

Alibaba cloud terraform provider does not handle kubernetes creation error properly, which causes an error when destroying. In that case, you can remove the kubernetes resource from the local state manually and proceed to destroy the rest resources:

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
> You have to manually delete the cloud disk used by monitoring node in Aliyun's console after destroying if you don't need it anymore.

## Limitations

You cannot change pod cidr, service cidr and worker instance types once the cluster is created.
