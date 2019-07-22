---
title: 在 AWS EKS 上部署 TiDB 集群
category: how-to
aliases: ['/docs-cn/v3.0/how-to/deploy/orchestrated/aws-eks/']
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

* 3 台 m5d.xlarge 实例，部署 PD
* 3 台 i3.2xlarge 实例，部署 TiKV
* 2 台 c4.4xlarge 实例，部署 TiDB
* 1 台 c5.xlarge 实例，部署监控组件

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
    52.14.50.145
]
eks_endpoint = https://E10A1D0368FFD6E1E32E11573E5CE619.sk1.us-east-2.eks.amazonaws.com
eks_version = 1.12
monitor_endpoint = http://abd299cc47af411e98aae02938da0762-1989524000.us-east-2.elb.amazonaws.com:3000
region = us-east-2
tidb_dns = abd2e3f7c7af411e98aae02938da0762-17499b76b312be02.elb.us-east-2.amazonaws.com
tidb_port = 4000
tidb_version = v3.0.0-rc.1
```

> **注意：**
>
> 你可以通过 `terraform output` 命令再次获取上面的输出信息。

## 访问数据库

`terraform apply` 完成后，可先通过 `ssh` 远程连接到堡垒机，再通过 MySQL client 来访问 TiDB 集群。

所需命令如下（用上面的输出信息替换 `<>` 部分内容)：

{{< copyable "shell-regular" >}}

```shell
ssh -i credentials/k8s-prod-<cluster_name>.pem ec2-user@<bastion_ip>
```

{{< copyable "shell-regular" >}}

```shell
mysql -h <tidb_dns> -P <tidb_port> -u root
```

`cluster_name` 默认为 `my-cluster`。如果 DNS 名字无法解析，请耐心等待几分钟。

你还可以通过 `kubectl` 和 `helm` 命令使用 kubeconfig 文件 `credentials/kubeconfig_<cluster_name>` 和 EKS 集群交互，主要有两种方式，如下所示。

- 指定 --kubeconfig 参数：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl --kubeconfig credentials/kubeconfig_<cluster_name> get po -n tidb
    ```

    {{< copyable "shell-regular" >}}

    ```shell
    helm --kubeconfig credentials/kubeconfig_<cluster_name> ls
    ```

- 或者，设置 KUBECONFIG 环境变量：

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

## Grafana 监控

你可以通过浏览器访问 `monitor_endpoint` 地址查看 Grafana 监控指标。

Grafana 默认登录信息：

- 用户名：admin
- 密码：admin

## 升级 TiDB 集群

要升级 TiDB 集群，可编辑 `variables.tf` 文件，修改 `tidb_version` 变量到更高版本，然后运行 `terraform apply`。

例如，要升级 TiDB 集群到 3.0.0-rc.2，则修改 `tidb_version` 为 `v3.0.0-rc.2`：

```
 variable "tidb_version" {
   description = "tidb cluster version"
   default = "v3.0.0-rc.2"
 }
```

> **注意：**
>
> 升级过程会持续一段时间，你可以通过 `kubectl --kubeconfig credentials/kubeconfig_<cluster_name> get po -n tidb --watch` 命令持续观察升级进度。

## 扩容 TiDB 集群

若要扩容 TiDB 集群，可按需修改 `variables.tf` 文件中的 `tikv_count` 或者 `tidb_count` 变量，然后运行 `terraform apply`。

例如，可以将 `tidb_count` 从 2 改为 4 以扩容 TiDB：

```
 variable "tidb_count" {
   default = 4
 }
```

> **注意：**
>
> - 由于缩容过程中无法确定会缩掉哪个节点，目前还不支持 TiDB 集群的缩容。
> - 扩容过程会持续几分钟，你可以通过 `kubectl --kubeconfig credentials/kubeconfig_<cluster_name> get po -n tidb --watch` 命令持续观察进度。

## 自定义

你可以按需修改 `variables.tf` 文件中的默认值，例如集群名称和镜像版本等。

### 自定义 AWS 相关的资源

默认情况下 terraform 脚本会新建 VPC。你也可以通过设置 `create_vpc` 为 `false`，并指定 `vpc_id`、`private_subnet_ids` 和 `public_subnet_ids` 变量为已有的 VPC id、subnet ids 来使用现有的网络。

> **注意：**
>
> 由于 AWS 和 Terraform 的限制，还不支持复用已有 EKS 集群的 VPC 和 subnets，所以请确保只在你手动创建 VPC 的情况下修改该参数。

由于 TiDB 服务通过 [Internal Elastic Load Balancer](https://aws.amazon.com/blogs/aws/internal-elastic-load-balancers/) 暴露，默认情况下，会创建一个 ec2 实例作为堡垒机，访问创建的 TiDB 集群。堡垒机上预装了 MySQL 和 Sysbench，所以你可以 SSH 到堡垒机然后通过 ELB 访问 TiDB。如果你的 VPC 中已经有了类似的 ec2 实例，你可以通过设置 `create_bastion` 为 `false` 禁掉堡垒机的创建。

TiDB 版本和组件数量也可以在 `variables.tf` 中修改，你可以按照自己的需求配置。

目前，由于 PD 和 TiKV 依赖 [NVMe SSD 实例存储卷](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ssd-instance-store.html)，TiDB 集群组件的实例类型不能修改。

### 自定义 TiDB 参数配置

目前，支持自定义修改的 TiDB 参数并不多。有两种方式修改这些参数：

* 部署集群之前，你可以直接修改 `templates/tidb-cluster-values.yaml.tpl` 文件中的配置，然后部署集群。
* 如果集群已经在运行，每次修改 `templates/tidb-cluster-values.yaml.tpl` 文件中的配置都需要重新执行 `terraform apply`，并手动删除 Pod(s)，否则集群会一直使用旧的配置。

## 销毁集群

可以通过如下命令销毁集群：

{{< copyable "shell-regular" >}}

```shell
terraform destroy
```

> **注意：**
>
> 如果你不再需要存储卷中的数据，在执行 `terraform destroy` 后，你需要在 AWS 控制台手动删除 EBS 卷。
