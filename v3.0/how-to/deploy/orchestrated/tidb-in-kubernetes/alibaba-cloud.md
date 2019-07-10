---
title: 在阿里云上部署 TiDB 集群
category: how-to
aliases: ['/docs-cn/v3.0/how-to/deploy/orchestrated/alibaba-cloud/']
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
    - 属于一个伸缩组的 2 台 ECS 实例（2 核 2G）托管版 Kubernetes 的默认伸缩组中必须至少有两台实例，用于承载整个的系统服务，例如 CoreDNS
    - 属于一个伸缩组的 3 台 `ecs.i2.xlarge` 实例，用于部署 PD
    - 属于一个伸缩组的 3 台 `ecs.i2.2xlarge` 实例，用于部署 TiKV
    - 属于一个伸缩组的 2 台 ECS 实例（16 核 32G）用于部署 TiDB
    - 属于一个伸缩组的 1 台 ECS 实例（4 核 8G）用于部署监控组件
    - 一块 500GB 的云盘用作监控数据存储

除了默认伸缩组之外的其它所有实例都是跨可用区部署的。而伸缩组 (Auto-scaling Group) 能够保证集群的健康实例数等于期望数值。因此，当发生节点故障甚至可用区故障时，伸缩组能够自动为我们创建新实例来确保服务可用性。

## 安装部署

1. 设置目标 Region 和阿里云密钥（也可以在运行 `terraform` 命令时根据命令提示输入）：

    ```shell
    export TF_VAR_ALICLOUD_REGION=<YOUR_REGION>
    export TF_VAR_ALICLOUD_ACCESS_KEY=<YOUR_ACCESS_KEY>
    export TF_VAR_ALICLOUD_SECRET_KEY=<YOUR_SECRET_KEY>
    ```

    用于部署集群的各变量的默认值存储在 `variables.tf` 文件中，如需定制可以修改此文件或在安装时通过 `-var` 参数覆盖。

2. 使用 Terraform 进行安装：

    ```shell
    $ git clone --depth=1 https://github.com/pingcap/tidb-operator
    $ cd tidb-operator/deploy/aliyun
    $ terraform init
    $ terraform apply
    ```

    假如在运行 `terraform apply` 时出现报错，可根据报错信息（例如缺少权限）进行修复后再次运行 `terraform apply`。

    整个安装过程大约需要 5 至 10 分钟，安装完成后会输出集群的关键信息（想要重新查看这些信息，可以运行 `terraform output`）：

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

3. 用 `kubectl` 或 `helm` 对集群进行操作（其中 `cluster_name` 默认值为 `tidb-cluster`）：

    ```shell
    $ export KUBECONFIG=$PWD/credentials/kubeconfig_<cluster_name>
    $ kubectl version
    $ helm ls
    ```

## 连接数据库

通过堡垒机可连接 TiDB 集群进行测试，相关信息在安装完成后的输出中均可找到：

```shell
$ ssh -i credentials/<cluster_name>-bastion-key.pem root@<bastion_ip>
$ mysql -h <tidb_slb_ip> -P <tidb_port> -u root
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

```
kubectl get pods --namespace tidb -o wide --watch
```

## TiDB 集群水平伸缩

按需修改 `variables.tf` 中的 `tikv_count` 和 `tidb_count` 数值，再次运行 `terraform apply` 即可完成 TiDB 集群的水平伸缩。

## 销毁集群

```shell
$ terraform destroy
```

假如 Kubernetes 集群没有创建成功，那么在 destroy 时会出现报错，无法进行正常清理。此时需要手动将 kubernetes 资源从本地状态中移除：

```shell
$ terraform state list
$ terraform state rm module.ack.alicloud_cs_managed_kubernetes.k8s
```

销毁集群操作需要执行较长时间。

> **注意：**
>
> 监控组件挂载的云盘需要在阿里云管理控制台中手动删除。

## 自定义集群

默认配置下，Terraform 脚本会创建一个新的 VPC，假如要使用现有的 VPC，可以在 `variable.tf` 中设置 `vpc_id`。注意，当使用现有 VPC 时，没有设置 vswitch 的可用区将不会部署 Kubernetes 节点。

出于安全考虑，TiDB 服务的 SLB 只对内网暴露，因此默认配置下还会创建一台堡垒机用于运维操作。堡垒机上还会安装 mysql-cli 和 sysbench 以便于使用和测试。假如不需要堡垒机，可以设置 `variables.tf` 中的 `create_bastion` 参数来关闭。

实例的规格可以通过两种方式进行定义：

1. 通过声明实例规格名；
2. 通过声明实例的配置，例如 CPU 核数和内存大小。

由于阿里云在不同地域会提供不同的规格类型，并且部分规格有售罄的情况，我们推荐使用第二种办法来定义更通用的实例规格。你可以在 `variables.tf` 中找到相关的配置项。

特殊地，由于 PD 和 TiKV 节点强需求本地 SSD 存储，脚本中不允许直接声明 PD 和 TiKV 的规格名，你可以通过设置 `*_instance_type_family` 来选择 PD 或 TiKV 的规格族（只能在三个拥有本地 SSD 的规格族中选择），再通过内存大小来筛选符合需求的型号。

更多自定义配置相关的内容，请直接参考项目中的 `variables.tf` 文件。

## 使用限制

目前，pod cidr，service cid 和节点型号等配置在集群创建后均无法修改。
