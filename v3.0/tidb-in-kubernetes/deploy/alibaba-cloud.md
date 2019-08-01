---
title: 在阿里云上部署 TiDB 集群
category: how-to
aliases: ['/docs-cn/V3.0/how-to/deploy/tidb-in-kubernetes/alibaba-cloud/']
---

# 在阿里云上部署 TiDB 集群

本文介绍了如何使用个人电脑（Linux 或 macOS 系统）在阿里云上部署 TiDB 集群。

## 环境需求

- [aliyun-cli](https://github.com/aliyun/aliyun-cli) >= 3.0.15 并且[配置 aliyun-cli](https://www.alibabacloud.com/help/doc-detail/90766.htm?spm=a2c63.l28256.a3.4.7b52a893EFVglq)

    > **注意：**
    >
    > Access Key 需要具有操作相应资源的权限。

- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/#install-kubectl) >= 1.12
- [helm](https://github.com/helm/helm/blob/master/docs/install.md#installing-the-helm-client) >= 2.9.1 且 <= 2.11.0
- [jq](https://stedolan.github.io/jq/download/) >= 1.6
- [terraform](https://learn.hashicorp.com/terraform/getting-started/install.html) 0.11.*

你可以使用阿里云的[云命令行](https://shell.aliyun.com)服务来进行操作，云命令行中已经预装并配置好了所有工具。

### 权限

完整部署集群需要具备以下权限：

- AliyunECSFullAccess
- AliyunESSFullAccess
- AliyunVPCFullAccess
- AliyunSLBFullAccess
- AliyunCSFullAccess
- AliyunEIPFullAccess
- AliyunECIFullAccess
- AliyunVPNGatewayFullAccess
- AliyunNATGatewayFullAccess

## 概览

默认配置下，会创建：

- 一个新的 VPC
- 一台 ECS 实例作为堡垒机
- 一个托管版 ACK（阿里云 Kubernetes）集群以及一系列 worker 节点：
    - 属于一个伸缩组的 2 台 ECS 实例（2 核 2 GB）托管版 Kubernetes 的默认伸缩组中必须至少有两台实例，用于承载整个的系统服务，例如 CoreDNS
    - 属于一个伸缩组的 3 台 `ecs.g5.large` 实例，用于部署 PD
    - 属于一个伸缩组的 3 台 `ecs.i2.2xlarge` 实例，用于部署 TiKV
    - 属于一个伸缩组的 2 台 `ecs.c5.4xlarge` 实例用于部署 TiDB
    - 属于一个伸缩组的 1 台 `ecs.c5.xlarge` 实例用于部署监控组件
    - 一块 100 GB 的云盘用作监控数据存储

除了默认伸缩组之外的其它所有实例都是跨可用区部署的。而伸缩组 (Auto-scaling Group) 能够保证集群的健康实例数等于期望数值。因此，当发生节点故障甚至可用区故障时，伸缩组能够自动为我们创建新实例来确保服务可用性。

## 安装部署

1. 设置目标 Region 和阿里云密钥（也可以在运行 `terraform` 命令时根据命令提示输入）：

    {{< copyable "shell-regular" >}}

    ```shell
    export TF_VAR_ALICLOUD_REGION=<YOUR_REGION> && \
    export TF_VAR_ALICLOUD_ACCESS_KEY=<YOUR_ACCESS_KEY> && \
    export TF_VAR_ALICLOUD_SECRET_KEY=<YOUR_SECRET_KEY>
    ```

    用于部署集群的各变量的默认值存储在 `variables.tf` 文件中，如需定制可以修改此文件或在安装时通过 `-var` 参数覆盖。

2. 使用 Terraform 进行安装：

    {{< copyable "shell-regular" >}}

    ```shell
    git clone --depth=1 https://github.com/pingcap/tidb-operator && \
    cd tidb-operator/deploy/aliyun
    ```

    {{< copyable "shell-regular" >}}

    ```shell
    terraform init
    ```

    `apply` 过程中需要输入 `yes` 来确认执行：

    {{< copyable "shell-regular" >}}

    ```shell
    terraform apply
    ```

    假如在运行 `terraform apply` 时出现报错，可根据报错信息（例如缺少权限）进行修复后再次运行 `terraform apply`。

    整个安装过程大约需要 5 至 10 分钟，安装完成后会输出集群的关键信息（想要重新查看这些信息，可以运行 `terraform output`）：

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

3. 用 `kubectl` 或 `helm` 对集群进行操作（其中 `cluster_name` 默认值为 `my-cluster`）：

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

## 连接数据库

通过堡垒机可连接 TiDB 集群进行测试，相关信息在安装完成后的输出中均可找到：

{{< copyable "shell-regular" >}}

```shell
ssh -i credentials/<cluster_name>-bastion-key.pem root@<bastion_ip>
```

{{< copyable "shell-regular" >}}

```shell
mysql -h <tidb_slb_ip> -P <tidb_port> -u root
```

## 监控

访问 `<monitor_endpoint>` 就可以查看相关的 Grafana 大盘。相关信息可在安装完成后的输出中找到。默认帐号密码为：

- 用户名：admin
- 密码：admin

> **警告：**
>
> 出于安全考虑，假如你已经或将要配置 VPN 用于访问 VPC，强烈建议将 `monitor_slb_network_type` 设置为 `intranet` 以禁止监控服务的公网访问。

## 升级 TiDB 集群

设置 `variables.tf` 中的 `tidb_version` 参数，并再次运行 `terraform apply` 即可完成升级。

升级操作可能会执行较长时间，可以通过以下命令来持续观察进度：

{{< copyable "shell-regular" >}}

```
kubectl get pods --namespace tidb -o wide --watch
```

## TiDB 集群水平伸缩

按需修改 `variables.tf` 中的 `tikv_count` 和 `tidb_count` 数值，再次运行 `terraform apply` 即可完成 TiDB 集群的水平伸缩。

## 销毁集群

{{< copyable "shell-regular" >}}

```shell
terraform destroy
```

假如 Kubernetes 集群没有创建成功，那么在 destroy 时会出现报错，无法进行正常清理。此时需要手动将 Kubernetes 资源从本地状态中移除：

{{< copyable "shell-regular" >}}

```shell
terraform state list
```

{{< copyable "shell-regular" >}}

```shell
terraform state rm module.ack.alicloud_cs_managed_kubernetes.k8s
```

销毁集群操作需要执行较长时间。

> **注意：**
>
> 监控组件挂载的云盘需要在阿里云管理控制台中手动删除。

## 配置

### 配置 TiDB Operator

通过调整 `variables.tf` 内的值来配置 TiDB Operator，大多数配置项均能按照 `variable` 的注释理解语义后进行修改。需要注意的是，`operator_helm_values` 配置项允许为 TiDB Operator 提供一个自定义的 `values.yaml` 配置文件，示例如下：

```hcl
variable "operator_helm_values" {
  default = file("my-operator-values.yaml")
}
```

同时，在默认配置下 Terraform 脚本会创建一个新的 VPC，假如要使用现有的 VPC，可以在 `variable.tf` 中设置 `vpc_id`。注意，当使用现有 VPC 时，没有设置 vswitch 的可用区将不会部署 Kubernetes 节点。

### 配置 TiDB 集群

TiDB 集群会使用 `./my-cluster.yaml` 作为集群的 `values.yaml` 配置文件，修改该文件即可配置 TiDB 集群。支持的配置项可参考 [Kubernetes 上的 TiDB 集群配置](/tidb-in-kubernetes/reference/configuration/tidb-cluster.md)。

## 管理多个 TiDB 集群

需要在一个 Kubernetes 集群下管理多个 TiDB 集群时，需要编辑 `./main.tf`，按实际需要新增 `tidb-cluster` 声明，示例如下：

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

注意，多个 TiDB 集群之间 `cluster_name` 必须保持唯一。下面是 `tidb-cluster` 模块的所有可配置参数：

| 参数名 | 说明 | 默认值 |
| :----- | :---- | :----- |
| `ack` | 封装目标 Kubernetes 集群信息的结构体，必填 | `nil` |
| `cluster_name` | TiDB 集群名，必填且必须唯一 | `nil` |
| `tidb_version` | TiDB 集群版本 | `v3.0.0` |
| `tidb_cluster_chart_version` | `tidb-cluster` helm chart 的版本 | `v1.0.0-beta.3` |
| `pd_count` | PD 节点数 | 3 |
| `pd_instance_type` | PD 实例类型 | `ecs.g5.large` |
| `tikv_count` | TiKV 节点数 | 3 |
| `tikv_instance_type` | TiKV 实例类型 | `ecs.i2.2xlarge` |
| `tidb_count` | TiDB 节点数 | 2 |
| `tidb_instance_type` | TiDB 实例类型 | `ecs.c5.4xlarge` |
| `monitor_instance_type` | 监控组件的实例类型 | `ecs.c5.xlarge` |
| `override_values` | TiDB 集群的 `values.yaml` 配置文件，通常通过 `file()` 函数从文件中读取 | `nil` |
| `local_exec_interpreter` | 执行命令行指令的解释器  | `["/bin/sh", "-c"]` |

## 管理多个 Kubernetes 集群

推荐针对每个 Kubernetes 集群都使用单独的 Terraform 模块进行管理（一个 Terraform Module 即一个包含 `.tf` 脚本的目录）。

`deploy/aliyun` 实际上是将 `deploy/modules` 中的数个可复用的 Terraform 脚本组合在了一起。当管理多个集群时（下面的操作在 `tidb-operator` 项目根目录下进行）：

1. 首先针对每个集群创建一个目录，如：

    {{< copyable "shell-regular" >}}

    ```shell
    mkdir -p deploy/aliyun-staging
    ```

2. 参考 `deploy/aliyun` 的 `main.tf`，编写自己的脚本，下面是一个简单的例子：

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

上面的脚本可以自由定制，比如，假如不需要堡垒机则可以移除 `module "bastion"` 相关声明。

你也可以直接拷贝 `deploy/aliyun` 目录，但要注意不能拷贝已经运行了 `terraform apply` 的目录，建议重新 clone 仓库再进行拷贝。

## 使用限制

目前，`pod cidr`，`service cidr` 和节点型号等配置在集群创建后均无法修改。
