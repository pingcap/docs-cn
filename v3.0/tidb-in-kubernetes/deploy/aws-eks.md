---
title: Deploy TiDB on AWS EKS
summary: Learn how to deploy a TiDB cluster on AWS EKS.
category: how-to
aliases: ['/docs/v3.0/how-to/deploy/tidb-in-kubernetes/aws-eks/']
---

# Deploy TiDB on AWS EKS

This document describes how to deploy a TiDB cluster on AWS EKS with your laptop (Linux or macOS) for development or testing.

## Prerequisites

Before deploying a TiDB cluster on AWS EKS, make sure the following requirements are satisfied:

* [awscli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) >= 1.16.73, to control AWS resources

    You must [configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) `awscli` before it can interact with AWS. The fastest way is using the `aws configure` command:

    {{< copyable "shell-regular" >}}

    ```shell
    aws configure
    ```

    Replace AWS Access Key ID and AWS Secret Access Key with your own keys:

    ```
    AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
    AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
    Default region name [None]: us-west-2
    Default output format [None]: json
    ```

    > **Note:**
    >
    > The access key must have at least permissions to: create VPC, create EBS, create EC2 and create role.

* [terraform](https://learn.hashicorp.com/terraform/getting-started/install.html)
* [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/#install-kubectl) >= 1.11
* [helm](https://github.com/helm/helm/blob/master/docs/install.md#installing-the-helm-client) >= 2.9.0 and < 3.0.0
* [jq](https://stedolan.github.io/jq/download/)
* [aws-iam-authenticator](https://docs.aws.amazon.com/eks/latest/userguide/install-aws-iam-authenticator.html) installed in `PATH`, to authenticate with AWS

    The easiest way to install `aws-iam-authenticator` is to download the prebuilt binary as shown below:

    Download the binary for Linux:

    {{< copyable "shell-regular" >}}

    ```shell
    curl -o aws-iam-authenticator https://amazon-eks.s3-us-west-2.amazonaws.com/1.12.7/2019-03-27/bin/linux/amd64/aws-iam-authenticator
    ```

    Or, download binary for macOS:

    {{< copyable "shell-regular" >}}

    ```shell
    curl -o aws-iam-authenticator https://amazon-eks.s3-us-west-2.amazonaws.com/1.12.7/2019-03-27/bin/darwin/amd64/aws-iam-authenticator
    ```

    Then execute the following commands:

    {{< copyable "shell-regular" >}}

    ```shell
    chmod +x ./aws-iam-authenticator && \
    sudo mv ./aws-iam-authenticator /usr/local/bin/aws-iam-authenticator
    ```

## Deploy

The default setup creates a new VPC and a `t2.micro` instance as the bastion machine, and an EKS cluster with following Amazon EC2 instances as worker nodes:

* 3 m5.xlarge instances for PD
* 3 c5d.4xlarge instances for TiKV
* 2 c5.4xlarge instances for TiDB
* 1 c5.2xlarge instance for monitor

Use the following commands to set up the cluster.

Get the code from Github:

{{< copyable "shell-regular" >}}

```shell
git clone --depth=1 https://github.com/pingcap/tidb-operator && \
cd tidb-operator/deploy/aws
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

It might take 10 minutes or more to finish the process. After `terraform apply` is executed successfully, some useful information is printed to the console.

A successful deployment will give the output like:

```
Apply complete! Resources: 67 added, 0 changed, 0 destroyed.

Outputs:

bastion_ip = [
  "34.219.204.217",
]
default-cluster_monitor-dns = a82db513ba84511e9af170283460e413-1838961480.us-west-2.elb.amazonaws.com
default-cluster_tidb-dns = a82df6d13a84511e9af170283460e413-d3ce3b9335901d8c.elb.us-west-2.amazonaws.com
eks_endpoint = https://9A9A5ABB8303DDD35C0C2835A1801723.yl4.us-west-2.eks.amazonaws.com
eks_version = 1.12
kubeconfig_filename = credentials/kubeconfig_my-cluster
region = us-west-2
```

You can use the `terraform output` command to get the output again.

> **Note:**
>
> EKS versions earlier than 1.14 do not support auto enabling cross-zone load balancing via Network Load Balancer (NLB). Therefore, unbalanced pressure distributed among TiDB instances can be expected in default settings. It is strongly recommended that you refer to [AWS Documentation](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/enable-disable-crosszone-lb.html#enable-cross-zone) to manually enable cross-zone load balancing for a production environment.

## Access the database

To access the deployed TiDB cluster, use the following commands to first `ssh` into the bastion machine, and then connect it via MySQL client (replace the `<>` parts with values from the output):

{{< copyable "shell-regular" >}}

```shell
ssh -i credentials/<cluster_name>.pem centos@<bastion_ip>
```

{{< copyable "shell-regular" >}}

```shell
mysql -h <tidb_dns> -P <tidb_port> -u root
```

The default value of `cluster_name` is `my-cluster`. If the DNS name is not resolvable, be patient and wait a few minutes.

You can interact with the EKS cluster using `kubectl` and `helm` with the kubeconfig file `credentials/kubeconfig_<cluster_name>` in the following two ways.

- By specifying `--kubeconfig` argument:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl --kubeconfig credentials/kubeconfig_<cluster_name> get po -n tidb
    ```

    {{< copyable "shell-regular" >}}

    ```shell
    helm --kubeconfig credentials/kubeconfig_<cluster_name> ls
    ```

- Or by setting the `KUBECONFIG` environment variable:

    {{< copyable "shell-regular" >}}

    ```shell
    export KUBECONFIG=$PWD/credentials/kubeconfig_<cluster_name>
    ```

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl get po -n tidb
    ```

    {{< copyable "shell-regular" >}}

    ```shell
    helm ls
    ```

## Monitor

You can access the `monitor_endpoint` address (printed in outputs) using your web browser to view monitoring metrics.

The initial Grafana login credentials are:

- User: admin
- Password: admin

## Upgrade

To upgrade the TiDB cluster, edit the `variables.tf` file with your preferred text editor and modify the `tidb_version` variable to a higher version, and then run `terraform apply`.

For example, to upgrade the cluster to version 3.0.1, modify the `tidb_version` to `v3.0.1`:

```hcl
 variable "default_cluster_version" {
   description = "tidb cluster version"
   default = "v3.0.1"
 }
```

> **Note:**
>
> The upgrading doesn't finish immediately. You can watch the upgrading process by `kubectl --kubeconfig credentials/kubeconfig_<cluster_name> get po -n tidb --watch`.

## Scale

To scale the TiDB cluster, edit the `variables.tf` file with your preferred text editor and modify the `tikv_count` or `tidb_count` variable to your desired count, and then run `terraform apply`.

For example, to scale out the cluster, you can modify the number of TiDB instances from 2 to 4:

```hcl
 variable "default_cluster_tidb_count" {
   default = 4
 }
```

> **Note:**
>
> Currently, scaling in is NOT supported because we cannot determine which node to scale. Scaling out needs a few minutes to complete, you can watch the scaling out by `kubectl --kubeconfig credentials/kubeconfig_<cluster_name> get po -n tidb --watch`.

## Customize

You can change default values in `variables.tf` (such as the cluster name and image versions) as needed.

### Customize AWS related resources

By default, the terraform script will create a new VPC. You can use an existing VPC by setting `create_vpc` to `false` and specify your existing VPC id and subnet ids to `vpc_id`, `private_subnet_ids` and `public_subnet_ids` variables.

> **Note:**
>
> - Reusing VPC and subnets of an existing EKS cluster is not supported yet due to limitations of AWS and Terraform, so only change this option if you have to use a manually created VPC.
> - The CNI plug-in on the EKS Node reserves some IP resources for each node. When manually creating a VPC, it is recommended to set the subnet mask length to 18~20 to ensure sufficient IP resources, or configure the CNI plugin to reserver less IP resources according to [EKS CNI plugin documentation](https://github.com/aws/amazon-vpc-cni-k8s#cni-configuration-variables).

An Amazon EC2 instance is also created by default as the bastion machine to connect to the created TiDB cluster. This is because the TiDB service is exposed as an [Internal Elastic Load Balancer](https://aws.amazon.com/blogs/aws/internal-elastic-load-balancers/). The EC2 instance has MySQL and Sysbench pre-installed, so you can use SSH to log into the EC2 instance and connect to TiDB using the ELB endpoint. You can disable the bastion instance creation by setting `create_bastion` to `false` if you already have an EC2 instance in the VPC.

The TiDB version and the number of components are also configurable in `variables.tf`.  You can customize these variables to suit your needs.

Currently, the instance type of the TiDB cluster component is not configurable because PD and TiKV depend on [NVMe SSD instance store](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ssd-instance-store.html), and different instance types have different disks.

### Customize a TiDB cluster

The terraform scripts provide proper default settings for the TiDB cluster in EKS. You can specify an overriding values file - `values.yaml` in `clusters.tf` for each TiDB cluster. Values of this file will override the default settings.

For example, the default cluster uses `./default-cluster.yaml` as the overriding values file, and the ConfigMap rollout feature is enabled in this file.

In EKS, some values are not customizable in `values.yaml`, such as the cluster version, replicas, node selectors, and taints. These variables are controlled by Terraform to ensure consistency between the infrastructure and TiDB clusters. To customize these variables, you can edit the variables of each `./tidb-cluster` module in the `clusters.tf` file directly.

### Customize TiDB Operator

You can customize the TiDB operator by specifying a Helm values file through the `operator_values` variable in the `variables.tf` file. For example:

```hcl
variable "operator_values" {
  description = "The helm values of TiDB Operator"
  default     = file("operator_values.yaml")
}
```

## Manage multiple TiDB clusters

An instance of `./tidb-cluster` module corresponds to a TiDB cluster in the EKS cluster. If you want to add a new TiDB cluster, you can edit `./cluster.tf` and add a new instance of `./tidb-cluster` module:

```hcl
module example-cluster {
  source = "./tidb-cluster"

  # The target EKS, required
  eks_info = local.eks
  # The subnets of node pools of this TiDB cluster, required
  subnets = local.subnets
  # TiDB cluster name, required
  cluster_name    = "example-cluster"

  # Helm values file
  override_values = file("example-cluster.yaml")
  # TiDB cluster version
  cluster_version               = "v3.0.0"
  # SSH key of cluster nodes
  ssh_key_name                  = module.key-pair.key_name
  # PD replica number
  pd_count                      = 3
  # TiKV instance type
  pd_instance_type              = "t2.xlarge"
  # TiKV replica number
  tikv_count                    = 3
  # TiKV instance type
  tikv_instance_type            = "t2.xlarge"
  # The storage class used by TiKV, if the TiKV instance type do not have local SSD, you should change it to storage class
  # TiDB replica number
  tidb_count                    = 2
  # TiDB instance type
  tidb_instance_type            = "t2.xlarge"
  # Monitor instance type
  monitor_instance_type         = "t2.xlarge"
  # The version of tidb-cluster helm chart
  tidb_cluster_chart_version    = "v1.0.0"
}
```

> **Note:**
>
> The `cluster_name` of each cluster must be unique.

You can get the addresses for TiDB and the monitoring service of the created cluster via `kubectl`. If you want the Terraform script to print this information, you can add `output` sections in `outputs.tf`:

```hcl
output "example-cluster_tidb-hostname" {
  value = module.example-cluster.tidb_hostname
}

output "example-cluster_monitor-hostname" {
  value = module.example-cluster.monitor_hostname
}
```

## Destroy clusters

It may take some time to finish destroying the cluster.

{{< copyable "shell-regular" >}}

``` shell
terraform destroy
```

> **Note:**
>
> * This will destroy your EKS cluster along with all the TiDB clusters you deployed on it.
> * If you do not need the data on the volumes anymore, you have to manually delete the EBS volumes in AWS console after running `terraform destroy`.

## Manage multiple Kubernetes clusters

This section describes the best practice to manage multiple Kubernetes clusters, each with one or more TiDB clusters installed.

The Terraform module in our case typically combines several sub-modules:

- `tidb-operator`, that provisions the Kubernetes control plane for TiDB cluster
- `tidb-cluster`, that creates the resource pool in the target Kubernetes cluster and deploy the TiDB cluster
- A `VPC` module, a `bastion` module and a `key-pair` module that are dedicated to TiDB on AWS

The best practice for managing multiple Kubernetes clusters is creating a new directory for each of your Kubernetes clusters, and combine the above modules according to your needs via Terraform scripts, so that the Terraform states among clusters do not interfere with each other, and it is convenient to expand. Here's an example:

{{< copyable "shell-regular" >}}

```shell
# assume we are in the project root
mkdir -p deploy/aws-staging
vim deploy/aws-staging/main.tf
```

The content of `deploy/aws-staging/main.tf` could be:

```hcl
provider "aws" {
  region = "us-west-1"
}

# Creates an SSH key to log in the bastion and the Kubernetes node
module "key-pair" {
  source = "../modules/aws/key-pair"

  name = "another-eks-cluster"
  path = "${path.cwd}/credentials/"
}

# Provisions a VPC
module "vpc" {
  source = "../modules/aws/vpc"

  vpc_name = "another-eks-cluster"
}

# Provisions an EKS control plane with TiDB Operator installed
module "tidb-operator" {
  source = "../modules/aws/tidb-operator"

  eks_name           = "another-eks-cluster"
  config_output_path = "credentials/"
  subnets            = module.vpc.private_subnets
  vpc_id             = module.vpc.vpc_id
  ssh_key_name       = module.key-pair.key_name
}

# HACK: enforces Helm to depend on the EKS
resource "local_file" "kubeconfig" {
  depends_on        = [module.tidb-operator.eks]
  sensitive_content = module.tidb-operator.eks.kubeconfig
  filename          = module.tidb-operator.eks.kubeconfig_filename
}
provider "helm" {
  alias    = "eks"
  insecure = true
  install_tiller = false
  kubernetes {
    config_path = local_file.kubeconfig.filename
  }
}

# Provisions a TiDB cluster in the EKS cluster
module "tidb-cluster-a" {
  source = "../modules/aws/tidb-cluster"
  providers = {
    helm = "helm.eks"
  }

  cluster_name = "tidb-cluster-a"
  eks          = module.tidb-operator.eks
  ssh_key_name = module.key-pair.key_name
  subnets      = module.vpc.private_subnets
}

# Provisions another TiDB cluster in the EKS cluster
module "tidb-cluster-b" {
  source = "../modules/aws/tidb-cluster"
  providers = {
    helm = "helm.eks"
  }

  cluster_name = "tidb-cluster-b"
  eks          = module.tidb-operator.eks
  ssh_key_name = module.key-pair.key_name
  subnets      = module.vpc.private_subnets
}

# Provisions a bastion machine to access the TiDB service and worker nodes
module "bastion" {
  source = "../modules/aws/bastion"

  bastion_name             = "another-eks-cluster-bastion"
  key_name                 = module.key-pair.key_name
  public_subnets           = module.vpc.public_subnets
  vpc_id                   = module.vpc.vpc_id
  target_security_group_id = module.tidb-operator.eks.worker_security_group_id
  enable_ssh_to_workers    = true
}

# Prints the TiDB hostname of tidb-cluster-a
output "cluster-a_tidb-dns" {
  description = "tidb service endpoints"
  value       = module.tidb-cluster-a.tidb_hostname
}

# print the monitor hostname of tidb-cluster-b
output "cluster-b_monitor-dns" {
  description = "tidb service endpoint"
  value       = module.tidb-cluster-b.monitor_hostname
}

output "bastion_ip" {
  description = "Bastion IP address"
  value       = module.bastion.bastion_ip
}
```

As shown in the code above, you can omit most of the parameters in each of the module calls because there are reasonable defaults, and it is easy to customize the configuration. For example, just delete the bastion module call if you do not need it.

To customize each field, you can refer to the default Terraform module. Also, you can always refer to the `variables.tf` file of each module to learn about all the available parameters.

In addition, you can easily integrate these modules into your own Terraform workflow. If you are familiar with Terraform, this is our recommended way of use.

> **Note:**
>
> * When creating a new directory, please pay attention to its relative path to Terraform modules, which affects the `source` parameter during module calls.
> * If you want to use these modules outside the tidb-operator project, make sure you copy the whole `modules` directory and keep the relative path of each module inside the directory unchanged.
> * Due to limitation [hashicorp/terraform#2430](https://github.com/hashicorp/terraform/issues/2430#issuecomment-370685911) of Terraform, the hack processing of Helm provider is necessary in the above example. It is recommended that you keep it in your own Terraform scripts.

If you are unwilling to write Terraform code, you can also copy the `deploy/aws` directory to create new Kubernetes clusters. But note that you cannot copy a directory that you have already run `terraform apply` against, when the Terraform state already exists in local.  In this case, it is recommended to clone a new repository before copying the directory.
