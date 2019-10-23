---
title: 在 AWS EKS 上部署 TiDB 集群
category: how-to
aliases: ['/docs-cn/v3.0/how-to/deploy/tidb-in-kubernetes/aws-eks/','/docs-cn/v3.0/how-to/deploy/orchestrated/aws-eks/']
---

# 在 AWS EKS 上部署 TiDB 集群

本文介绍了如何使用个人电脑（Linux 或 macOS 系统）在 AWS EKS (Elastic Kubernetes Service) 上部署 TiDB 集群。

## 环境配置准备

部署前，请确认已安装以下软件并完成配置：

* [awscli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) >= 1.16.73，控制 AWS 资源

    要与 AWS 交互，必须[配置 `awscli`](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)。最快的方式是使用 `aws configure` 命令:

    {{< copyable "shell-regular" >}}

    ``` shell
    aws configure
    ```

    替换下面的 AWS Access Key ID 和 AWS Secret Access Key：

    ```
    AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
    AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
    Default region name [None]: us-west-2
    Default output format [None]: json
    ```

    > **注意：**
    >
    > Access key 必须至少具有以下权限：创建 VPC、创建 EBS、创建 EC2 和创建 Role。

* [terraform](https://learn.hashicorp.com/terraform/getting-started/install.html)
* [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/#install-kubectl) >= 1.11
* [helm](https://github.com/helm/helm/blob/master/docs/install.md#installing-the-helm-client) >= 2.9.0 且 < 3.0.0
* [jq](https://stedolan.github.io/jq/download/)
* [aws-iam-authenticator](https://docs.aws.amazon.com/eks/latest/userguide/install-aws-iam-authenticator.html)，AWS 权限鉴定工具，确保安装在 `PATH` 路径下。

    最简单的安装方法是下载编译好的二进制文件 `aws-iam-authenticator`，如下所示。

    Linux 用户下载二进制文件：

    {{< copyable "shell-regular" >}}

    ``` shell
    curl -o aws-iam-authenticator https://amazon-eks.s3-us-west-2.amazonaws.com/1.12.7/2019-03-27/bin/linux/amd64/aws-iam-authenticator
    ```

    macOS 用户下载二进制文件：

    {{< copyable "shell-regular" >}}

    ``` shell
    curl -o aws-iam-authenticator https://amazon-eks.s3-us-west-2.amazonaws.com/1.12.7/2019-03-27/bin/darwin/amd64/aws-iam-authenticator
    ```

    二进制文件下载完成后，执行以下操作：

    {{< copyable "shell-regular" >}}

    ``` shell
    chmod +x ./aws-iam-authenticator && \
    sudo mv ./aws-iam-authenticator /usr/local/bin/aws-iam-authenticator
    ```

## 部署集群

默认部署会创建一个新的 VPC、一个 t2.micro 实例作为堡垒机，并包含以下 ec2 实例作为工作节点的 EKS 集群：

* 3 台 m5.xlarge 实例，部署 PD
* 3 台 c5d.4xlarge 实例，部署 TiKV
* 2 台 c5.4xlarge 实例，部署 TiDB
* 1 台 c5.2xlarge 实例，部署监控组件

使用如下命令部署集群。

从 Github 克隆代码并进入指定路径：

{{< copyable "shell-regular" >}}

``` shell
git clone --depth=1 https://github.com/pingcap/tidb-operator && \
cd tidb-operator/deploy/aws
```

使用 `terraform` 命令初始化并部署集群：

{{< copyable "shell-regular" >}}

``` shell
terraform init
```

{{< copyable "shell-regular" >}}

``` shell
terraform apply
```

> **注意：**
>
> `terraform apply` 过程中必须输入 "yes" 才能继续。

整个过程可能至少需要 10 分钟。`terraform apply` 执行成功后，控制台会输出类似如下的信息：

```
Apply complete! Resources: 67 added，0 changed，0 destroyed.

Outputs:

bastion_ip = [
  "34.219.204.217",
]
default-cluster_monitor-dns = a82db513ba84511e9af170283460e413-1838961480.us-west-2.elb.amazonaws.com
default-cluster_tidb-dns = a82df6d13a84511e9af170283460e413-d3ce3b9335901d8c.elb.us-west-2.amazonaws.com
eks_endpoint = https://9A9A5ABB8303DDD35C0C2835A1801723.yl4.us-west-2.eks.amazonaws.com
eks_version = 1.12
kubeconfig_filename = credentials/kubeconfig_my-cluster
region = us-west-21
```

你可以通过 `terraform output` 命令再次获取上面的输出信息。

> **注意：**
>
> 1.14 版本以前的 EKS 不支持自动开启 NLB 跨可用区负载均衡，因此默认配置下 会出现各台 TiDB 实例压力不均衡额状况。生产环境下，强烈建议参考 [AWS 官方文档](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/enable-disable-crosszone-lb.html#enable-cross-zone)手动开启 NLB 的跨可用区负载均衡。

## 访问数据库

`terraform apply` 完成后，可先通过 `ssh` 远程连接到堡垒机，再通过 MySQL client 来访问 TiDB 集群。

所需命令如下（用上面的输出信息替换 `<>` 部分内容)：

{{< copyable "shell-regular" >}}

```shell
ssh -i credentials/<eks_name>.pem centos@<bastion_ip>
```

{{< copyable "shell-regular" >}}

```shell
mysql -h <tidb_dns> -P 4000 -u root
```

`eks_name` 默认为 `my-cluster`。如果 DNS 名字无法解析，请耐心等待几分钟。

你还可以通过 `kubectl` 和 `helm` 命令使用 kubeconfig 文件 `credentials/kubeconfig_<eks_name>` 和 EKS 集群交互，主要有两种方式，如下所示。

- 指定 --kubeconfig 参数：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl --kubeconfig credentials/kubeconfig_<eks_name> get po -n <default_cluster_name>
    ```

    {{< copyable "shell-regular" >}}

    ```shell
    helm --kubeconfig credentials/kubeconfig_<eks_name> ls
    ```

- 或者，设置 KUBECONFIG 环境变量：

    {{< copyable "shell-regular" >}}

    ```shell
    export KUBECONFIG=$PWD/credentials/kubeconfig_<eks_name>
    ```

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl get po -n <default_cluster_name>
    ```

    {{< copyable "shell-regular" >}}

    ```shell
    helm ls
    ```

## Grafana 监控

你可以通过浏览器访问 `<monitor-dns>:3000` 地址查看 Grafana 监控指标。

Grafana 默认登录信息：

- 用户名：admin
- 密码：admin

## 升级 TiDB 集群

要升级 TiDB 集群，可编辑 `variables.tf` 文件，修改 `default_cluster_version` 变量到更高版本，然后运行 `terraform apply`。

例如，要升级 TiDB 集群到 3.0.1，则修改 `default_cluster_version` 为 `v3.0.1`：

```hcl
variable "default_cluster_version" {
  default = "v3.0.1"
}
```

> **注意：**
>
> 升级过程会持续一段时间，你可以通过 `kubectl --kubeconfig credentials/kubeconfig_<cluster_name> get po -n <default_cluster_name> --watch` 命令持续观察升级进度。

## 扩容 TiDB 集群

若要扩容 TiDB 集群，可按需修改 `variables.tf` 文件中的 `default_cluster_tikv_count` 或者 `default_cluster_tidb_count` 变量，然后运行 `terraform apply`。

例如，可以将 `default_cluster_tidb_count` 从 2 改为 4 以扩容 TiDB：

```hcl
 variable "default_cluster_tidb_count" {
   default = 4
 }
```

> **注意：**
>
> - 由于缩容过程中无法确定会缩掉哪个节点，目前还不支持 TiDB 集群的缩容。
> - 扩容过程会持续几分钟，你可以通过 `kubectl --kubeconfig credentials/kubeconfig_<eks_name> get po -n <default_cluster_name> --watch` 命令持续观察进度。

## 自定义

你可以按需修改 `variables.tf` 文件中的默认值，例如集群名称和镜像版本等。

### 自定义 AWS 相关的资源

默认情况下 terraform 脚本会新建 VPC。你也可以通过设置 `create_vpc` 为 `false`，并指定 `vpc_id`、`private_subnet_ids` 和 `public_subnet_ids` 变量为已有的 VPC id、subnet ids 来使用现有的网络。

> **注意：**
>
> - 由于 AWS 和 Terraform 的限制，还不支持复用已有 EKS 集群的 VPC 和 subnets，所以请确保只在你手动创建 VPC 的情况下修改该参数；
> - EKS Node 上的 CNI 插件会为每个节点预留一部分 IP 资源，因此 IP 消耗较大，在手动创建 VPC 时，建议将每个 subnet 的掩码长度设置在 18~20 以确保 IP 资源充足，或参考 [EKS CNI 插件文档](https://github.com/aws/amazon-vpc-cni-k8s#cni-configuration-variables)将节点预留的 IP 资源数调低。

由于 TiDB 服务通过 [Internal Elastic Load Balancer](https://aws.amazon.com/blogs/aws/internal-elastic-load-balancers/) 暴露，默认情况下，会创建一个 Amazon EC2 实例作为堡垒机，访问创建的 TiDB 集群。堡垒机上预装了 MySQL 和 Sysbench，所以你可以通过 SSH 方式登陆到堡垒机后通过 ELB 访问 TiDB。如果你的 VPC 中已经有了类似的 EC2 实例，你可以通过设置 `create_bastion` 为 `false` 禁掉堡垒机的创建。

TiDB 版本和组件数量也可以在 `variables.tf` 中修改，你可以按照自己的需求配置。

目前，由于 PD 和 TiKV 依赖 [NVMe SSD 实例存储卷](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ssd-instance-store.html)，TiDB 集群组件的实例类型不能修改。

### 自定义 TiDB 参数配置

Terraform 脚本中为运行在 EKS 上的 TiDB 集群提供了合理的默认配置。有自定义需求时，你可以在 `clusters.tf` 中通过 `override_values` 参数为每个 TiDB 集群指定一个 `values.yaml` 文件来自定义集群参数配置。

作为例子，默认集群使用了 `./default-cluster.yaml` 作为 `values.yaml` 配置文件，并在配置中打开了"配置文件滚动更新"特性。

值得注意的是，在 EKS 上部分配置项无法在 `values.yaml` 中进行修改，包括集群版本、副本数、`NodeSelector` 以及 `Tolerations`。`NodeSelector` 和 `Tolerations` 由 Terraform 直接管理以确保基础设施与 TiDB 集群之间的一致性。集群版本和副本数可以通过 `cluster.tf` 文件中的 `tidb-cluster` module 参数来修改。

> **注意：**
>
> 自定义 `values.yaml` 配置文件中，不建议包含如下配置（`tidb-cluster` module 默认固定配置）：

```
pd:
  storageClassName: ebs-gp2
tikv:
  stroageClassName: local-storage
tidb:
  service:
    type: LoadBalancer
    annotations:
      service.beta.kubernetes.io/aws-load-balancer-internal: '0.0.0.0/0'
      service.beta.kubernetes.io/aws-load-balancer-type: nlb
      service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: >'true'
  separateSlowLog: true
monitor:
  storage: 100Gi
  storageClassName: ebs-gp2
  persistent: true
  grafana:
    config:
      GF_AUTH_ANONYMOUS_ENABLED: "true"
    service:
      type: LoadBalancer
```

### 自定义 TiDB Operator

你可以通过 `variables.tf` 中的 `operator_values` 参数传入自定义的 `values.yaml` 内容来配置 TiDB Operator。示例如下：

```hcl
variable "operator_values" {
  description = "The helm values file for TiDB Operator, path is relative to current working dir"
  default     = "./operator_values.yaml"
}
```

## 管理多个 TiDB 集群

一个 `tidb-cluster` 模块的实例对应一个 TiDB 集群，你可以通过编辑 `clusters.tf` 添加新的 `tidb-cluster` 模块实例来新增 TiDB 集群，示例如下：

```hcl
module example-cluster {
  source = "../modules/aws/tidb-cluster"
  
  # The target EKS, required
  eks = local.eks
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

> **注意：**
>
> `cluster_name` 必须是唯一的。

你可以通过 `kubectl` 获取新集群的监控系统地址与 TiDB 地址。假如你希望让 Terraform 脚本输出这些地址，可以通过在 `outputs.tf` 中增加相关的输出项实现：

```hcl
output "example-cluster_tidb-hostname" {
  value = module.example-cluster.tidb_hostname
}

output "example-cluster_monitor-hostname" {
  value = module.example-cluster.monitor_hostname
}
```

修改完成后，执行 `terraform init` 和 `terraform apply` 创建集群。

最后，只要移除 `tidb-cluster` 模块调用，对应的 TiDB 集群就会被销毁，EC2 资源也会随之释放。

## 销毁集群

可以通过如下命令销毁集群：

{{< copyable "shell-regular" >}}

```shell
terraform destroy
```

> **注意：**
>
> * 该操作会销毁 EKS 集群以及部署在该 EKS 集群上的所有 TiDB 集群。
> * 如果你不再需要存储卷中的数据，在执行 `terraform destroy` 后，你需要在 AWS 控制台手动删除 EBS 卷。

## 管理多个 Kubernetes 集群

本节详细介绍了如何管理多个 Kubernetes 集群（EKS），并在每个集群上部署一个或更多 TiDB 集群。

上述文档中介绍的 Terraform 脚本组合了多个 Terraform 模块：

- `tidb-operator` 模块，用于创建 EKS 集群并在 EKS 集群上安装配置 [TiDB Operator](/dev/tidb-in-kubernetes/deploy/tidb-operator.md)。
- `tidb-cluster` 模块，用于创建 TiDB 集群所需的资源池并部署 TiDB 集群。
- EKS 上的 TiDB 集群专用的 `vpc` 模块、`key-pair`模块和`bastion` 模块

管理多个 Kubernetes 集群的最佳实践是为每个 Kubernetes 集群创建一个单独的目录，并在新目录中自行组合上述 Terraform 模块。这种方式能够保证多个集群间的 Terraform 状态不会互相影响，也便于自由定制和扩展。下面是一个例子：

{{< copyable "shell-regular" >}}

```shell
mkdir -p deploy/aws-staging
vim deploy/aws-staging/main.tf
```

`deploy/aws-staging/main.tf` 的内容可以是：

```hcl
provider "aws" {
  region = "us-west-1"
}

# 创建一个 ssh key，用于登录堡垒机和 Kubernetes 节点
module "key-pair" {
  source = "../modules/aws/key-pair"

  name = "another-eks-cluster"
  path = "${path.cwd}/credentials/"
}

# 创建一个新的 VPC
module "vpc" {
  source = "../modules/aws/vpc"

  vpc_name = "another-eks-cluster"
}

# 在上面的 VPC 中创建一个 EKS 并部署 tidb-operator
module "tidb-operator" {
  source = "../modules/aws/tidb-operator"

  eks_name           = "another-eks-cluster"
  config_output_path = "credentials/"
  subnets            = module.vpc.private_subnets
  vpc_id             = module.vpc.vpc_id
  ssh_key_name       = module.key-pair.key_name
}

# 特殊处理，确保 helm 操作在 EKS 创建完毕后进行
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

# 在上面的 EKS 集群上创建一个 TiDB 集群
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

# 在上面的 EKS 集群上创建另一个 TiDB 集群
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

# 创建一台堡垒机
module "bastion" {
  source = "../modules/aws/bastion"

  bastion_name             = "another-eks-cluster-bastion"
  key_name                 = module.key-pair.key_name
  public_subnets           = module.vpc.public_subnets
  vpc_id                   = module.vpc.vpc_id
  target_security_group_id = module.tidb-operator.eks.worker_security_group_id
  enable_ssh_to_workers    = true
}

# 输出 tidb-cluster-a 的 TiDB 服务地址
output "cluster-a_tidb-dns" {
  description = "tidb service endpoints"
  value       = module.tidb-cluster-a.tidb_hostname
}

# 输出 tidb-cluster-b 的监控地址
output "cluster-b_monitor-dns" {
  description = "tidb service endpoint"
  value       = module.tidb-cluster-b.monitor_hostname
}

# 输出堡垒机 IP
output "bastion_ip" {
  description = "Bastion IP address"
  value       = module.bastion.bastion_ip
}
```

上面的例子很容易进行定制，比如，假如你不需要堡垒机，便可以删去对 `bastion` 模块的调用。同时，项目中提供的 Terraform 模块均设置了合理的默认值，因此在调用这些 Terraform 模块时，你可以略去大部分的参数。

你可以参考默认的 Terraform 脚本来定制每个模块的参数，也可以参考每个模块的 `variables.tf` 文件来了解所有可配置的参数。

另外，这些 Terraform 模块可以很容易地集成到你自己的 Terraform 工作流中。假如你对 Terraform 非常熟悉，这也是我们推荐的一种使用方式。

> **注意：**
>
> * 由于 Terraform 本身的限制（[hashicorp/terraform#2430](https://github.com/hashicorp/terraform/issues/2430#issuecomment-370685911)），在你自己的 Terraform 脚本中，也需要保留上述例子中对 `helm provider` 的特殊处理。
> * 创建新目录时，需要注意与 Terraform 模块之间的相对路径，这会影响调用模块时的 `source` 参数。
> * 假如你想在 tidb-operator 项目之外使用这些模块，你需要确保 `modules` 目录中的所有模块的相对路径保持不变。

假如你不想自己写 Terraform 代码，也可以直接拷贝 `deploy/aws` 目录来创建新的 Kubernetes 集群。但要注意不能拷贝已经运行过 `terraform apply` 的目录（已经有 Terraform 的本地状态）。这种情况下，推荐在拷贝前克隆一个新的仓库。
