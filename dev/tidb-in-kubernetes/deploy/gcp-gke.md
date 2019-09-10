---
title: 在 GCP GKE 上部署 TiDB 集群
category: how-to
---

# 在 GCP GKE 上部署 TiDB 集群

本文介绍了如何使用个人电脑（Linux 或 macOS 系统）在 GCP GKE 上部署 TiDB 集群。

> **警告：**
>
> 当前多磁盘聚合功能[存在一些已知问题](https://github.com/pingcap/tidb-operator/issues/684)，不建议在生产环境中每节点配置一块以上磁盘。我们正在修复此问题。

## 环境准备

部署前，确认已安装以下软件：

* Git
* [Google Cloud SDK](https://cloud.google.com/sdk/install)
* [Terraform](https://www.terraform.io/downloads.html) >= 0.12
* [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/#install-kubectl) >= 1.14
* [Helm](https://github.com/helm/helm/blob/master/docs/install.md#installing-the-helm-client) >= 2.9.0 且 < 3.0.0
* [jq](https://stedolan.github.io/jq/download/)

## 配置

为保证部署顺利，需要提前进行一些配置。在开始配置 Google Cloud SDK、API、Terraform 前，先下载以下资源：

{{< copyable "shell-regular" >}}

```bash
git clone --depth=1 https://github.com/pingcap/tidb-operator && \
cd tidb-operator/deploy/gcp
```

### 配置 Google Cloud SDK

安装 Google Cloud SDK 后，需要执行 `gcloud init` 进行[初始化](https://cloud.google.com/sdk/docs/initializing)。

### 配置 API

如果使用的 GCP 项目是新项目，确保以下 API 已启用：

{{< copyable "shell-regular" >}}

```bash
gcloud services enable cloudresourcemanager.googleapis.com \
    cloudbilling.googleapis.com cloud services enable iam.googleapis.com \
    compute.googleapis.com container.googleapis.com
```

### 配置 Terraform

执行 Terraform 脚本需要设置 3 个环境变量。你可以等 Terraform 提示再输入，也可以提前在 `.tfvars` 文件中定义变量。所需的 3 个环境变量如下：

+ `GCP_CREDENTIALS_PATH`：GCP 证书文件路径。

    - 建议另建一个服务账号给 Terraform 使用，参考[创建与管理服务账号文档](https://cloud.google.com/iam/docs/creating-managing-service-accounts)。`./create-service-account.sh` 会创建最低权限的服务账号。

    - 参考[服务账号密钥文档](https://cloud.google.com/iam/docs/creating-managing-service-account-keys)来创建服务账号密钥。下面脚本中的步骤详细说明了如何使用 `deploy/gcp` 目录中提供的脚本执行此操作。或者，如果自己创建服务账号和密钥，可以在创建时选择 `JSON` 类型的密钥。下载的包含私钥的 `JSON` 文件即所需的证书文件。

+ `GCP_REGION`：创建资源所在的区域，例如：`us-west1`。
+ `GCP_PROJECT`：GCP 项目的名称。

要使用上述 3 个环境变量配置 Terraform，可执行以下脚本：

{{< copyable "shell-regular" >}}

```bash
# 将 GCP_REGION 替换为你的 GCP Region。
echo GCP_REGION=\"us-west1\" >> terraform.tfvars
```

{{< copyable "shell-regular" >}}

```bash
# 将 GCP_PROJECT 替换为你的 GCP 项目名称，确保连接的是正确的 GCP 项目。
echo "GCP_PROJECT=\"$(gcloud config get-value project)\"" >> terraform.tfvars
```

{{< copyable "shell-regular" >}}

```bash
# 为 Terraform 创建一个有限权限的服务账号，并设置证书路径。
./create-service-account.sh
```

Terraform 自动加载和填充匹配 `terraform.tfvars` 或 `*.auto.tfvars` 文件的变量。相关详细信息，请参阅 [Terraform 文档](https://learn.hashicorp.com/terraform/getting-started/variables.html)。上述脚本会使用 `GCP_REGION` 和 `GCP_PROJECT` 填充 `terraform.tfvars` 文件，使用 `GCP_CREDENTIALS_PATH` 填充 `credentials.auto.tfvars` 文件。

## 部署集群

在部署集群前，需要先确定实例类型。

- 如果只是想试一下 TiDB，又不想花费太高成本，可以采用轻量级的配置：

    {{< copyable "shell-regular" >}}

    ```bash
    cat small.tfvars >> terraform.tfvars
    ```

- 如果要对生产环境的部署进行 benchmark 测试，则建议采用生产级的配置：

    {{< copyable "shell-regular" >}}

    ```bash
    cat prod.tfvars >> terraform.tfvars
    ```

`prod.tfvars` 会默认创建一个新的 VPC，两个子网和一个 f1-micro 实例作为堡垒机，以及使用以下实例类型作为工作节点的 GKE 集群：

* 3 台 n1-standard-4 实例：部署 PD
* 3 台 n1-highmem-8 实例：部署 TiKV
* 3 台 n1-standard-16 实例：部署 TiDB
* 3 台 n1-standard-2 实例：部署监控组件

> **注意：**
>
> 工作节点的数量取决于指定 Region 中可用区的数量。大部分 Region 有 3 个可用区，但是 us-central1 有 4 个可用区。参考 [Regions and Zones](https://cloud.google.com/compute/docs/regions-zones/) 查看更多信息。参考[自定义](#自定义)部分来自定义区域集群的节点池。

如上所述，生产环境的部署需要 91 个 CPU，超过了 GCP 项目的默认配额。可以参考[配额](https://cloud.google.com/compute/quotas)来增加项目配额。扩容同样需要更多 CPU。

所有配置现已完成，可以启动脚本来部署 TiDB 集群：

{{< copyable "shell-regular" >}}

```bash
terraform init
```

{{< copyable "shell-regular" >}}

```bash
terraform apply
```

> **注意：**
>
> 如果未提前设置上文所述的 3 个环境变量，执行 `terraform apply` 过程中会有提示出现，要求对 3 个变量进行设置。详情请参考[配置 Terraform](#配置-terraform)。

整个过程可能至少需要 10 分钟。`terraform apply` 执行成功后，会输出类似如下的信息:

```
Apply complete! Resources: 23 added, 0 changed, 0 destroyed.

Outputs:

how_to_connect_to_default_cluster_tidb_from_bastion = mysql -h 172.31.252.20 -P 4000 -u root
how_to_ssh_to_bastion = gcloud compute ssh tidb-cluster-bastion --zone us-west1-b
how_to_set_reclaim_policy_of_pv_for_default_tidb_cluster_to_delete = kubectl --kubeconfig /.../credentials/kubeconfig_tidb-cluster get pvc -n tidb-cluster -o jsonpath='{.items[*].spec.volumeName}'|fmt -1 | xargs -I {} kubectl --kubeconfig /.../credentials/kubeconfig_tidb-cluster patch pv {} -p '{"spec":{"persistentVolumeReclaimPolicy":"Delete"}}'
kubeconfig_file = ./credentials/kubeconfig_tidb-cluster
monitor_lb_ip = 35.227.134.146
monitor_port = 3000
region = us-west1
tidb_version = v3.0.1
```

## 访问数据库

`terraform apply` 运行完成后，可先通过 `ssh` 远程连接到堡垒机，再通过 MySQL 客户端来访问 TiDB 集群。所需命令如下（用上面的输出信息替换 `<>` 部分内容）：

{{< copyable "shell-regular" >}}

```bash
gcloud compute ssh <gke-cluster-name>-bastion --zone <zone>
```

{{< copyable "shell-regular" >}}

```bash
mysql -h <tidb_ilb_ip> -P 4000 -u root
```

> **注意：**
>
> 通过 MySQL 连接 TiDB 前，需要先安装 MySQL 客户端。

## 与集群交互

你可以通过 `kubectl` 和 `helm` 使用 kubeconfig 文件 `credentials/kubeconfig_<cluster_name>` 和 GKE 集群交互。交互方式主要有以下两种：

- 指定 `--kubeconfig` 参数：

    {{< copyable "shell-regular" >}}

    ```bash
    kubectl --kubeconfig credentials/kubeconfig_<cluster_name> get po -n tidb
    ```

    ```bash
    # --kubeconfig 参数需要 helm 2.10.0+
    helm --kubeconfig credentials/kubeconfig_<cluster_name> ls
    ```

- 设置 `KUBECONFIG` 环境变量：

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

> **注意：**
>
> `cluster_name` 默认为 `my-cluster`，可以通过 `variables.tf` 修改。

## 升级 TiDB 集群

要升级 TiDB 集群，可编辑 `variables.tf` 文件，将 `tidb_version` 变量的值修改为更高版本，然后运行 `terraform apply`。

例如，要将 TiDB 集群升级到 3.0.0-rc.2，可修改 `tidb_version` 为 `v3.0.0-rc.2`：

```
variable "tidb_version" {
  description = "TiDB version"
  default     = "v3.0.0-rc.2"
}
```

升级过程会持续一段时间。你可以通过以下命令来持续观察升级进度：

{{< copyable "shell-regular" >}}

```bash
kubectl --kubeconfig credentials/kubeconfig_<cluster_name> get po -n tidb --watch
```

然后你可以[访问数据库](#访问数据库)并通过 `tidb_version()` 确认集群是否升级成功：

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

## 管理多个 TiDB 集群

一个 `tidb-cluster` 模块的实例对应一个 GKE 集群中的 TiDB 集群。要添加一个新的 TiDB 集群，可以编辑 `tidbclusters.tf` 文件来添加一个 `tidb-cluster` 模块的新实例。例如：

{{< copyable "" >}}

```hcl
module "example-tidb-cluster" {
  providers = {
    helm = "helm.gke"
  }
  source                     = "../modules/gcp/tidb-cluster"
  gcp_project                = "gcp-project-name"
  gke_cluster_location       = "us-west1"
  gke_cluster_name           = "gke-cluster-name"
  cluster_name               = "example-tidb-cluster"
  cluster_version            = "v3.0.1"
  kubeconfig_path            = module.tidb-operator.kubeconfig_path
  tidb_cluster_chart_version = "v1.0.0"
  pd_instance_type           = "n1-standard-1"
  tikv_instance_type         = "n1-standard-4"
  tidb_instance_type         = "n1-standard-2"
  monitor_instance_type      = "n1-standard-1"
  pd_node_count              = 1
  tikv_node_count            = 2
  tidb_node_count            = 1
  monitor_node_count         = 1
}
```

> **注意：**
>
> - 每个集群的 `cluster_name` 必须是唯一的。
> - 为任一组件实际创建的总节点数等于配置文件中的节点数乘以该 Region 中可用区的个数。

你可以通过 `kubectl` 获取创建的 TiDB 集群和监控组件的地址。如果你希望 Terraform 脚本打印此信息，可在 `outputs.tf` 中添加一个 `output` 配置项，如下所示：

{{< copyable "" >}}

```hcl
output "how_to_connect_to_example_tidb_cluster_from_bastion" {
  value = module.example-tidb-cluster.how_to_connect_to_tidb_from_bastion
}
```

上述配置可使该脚本打印出用于连接 TiDB 集群的命令，该集群即刚刚从堡垒机实例创建的集群。

## 扩容

若要扩容 TiDB 集群，可按需修改 `variables.tf` 文件中的 `tikv_count`、`tidb_count` 变量，然后运行 `terraform apply`。

> **注意：**
>
> 由于缩容过程中无法确定哪个节点会被删除，因此目前不支持集群缩容。

扩容过程会持续几分钟，你可以通过以下命令来持续观察进度：

{{< copyable "shell-regular" >}}

```
kubectl --kubeconfig credentials/kubeconfig_<gke_cluster_name> get po -n <tidb_cluster_name> --watch
```

例如，可以将 `tidb_count` 从 1 改为 2 来扩容 TiDB：

```hcl
variable "tidb_count" {
  description = "Number of TiDB nodes per availability zone"
  default     = 2
}
```

> **注意：**
>
> 增加节点数量会在每个可用区都增加节点。

## 自定义

你可以更改 `variables.tf` 中的默认值，例如集群名称和镜像版本等，但更建议在 `terraform.tfvars` 文件或其它相关文件中来指定值。

### 自定义 GCP 资源

GCP 允许 `n1-standard-1` 或者更大的实例类型挂载本地 SSD，这提供了更好的自定义特性。

### 自定义 TiDB 参数配置

Terraform 脚本为 GKE 中的 TiDB 集群提供了默认设置。你也可以在 `tidbclusters.tf` 中为每个 TiDB 集群指定一个覆盖文件 - `values.yaml`。此文件中的值会覆盖默认设置。

例如，集群默认使用 `gcp/tidb-cluster` 模块中的 `default.yaml` 作为覆盖文件，并在此文件中启用了 ConfigMap rollout 功能。

在 GKE 中，某些值不支持在 `values.yaml` 中自定义，例如群集版本、副本、节点选择器和 taints。这些变量由 Terraform 控制，以确保基础架构和 TiDB 集群一致。如果要自定义这些变量，可以直接在 `tidbclusters.tf` 文件中编辑每个 `tidb-cluster` 模块的变量。

### 自定义 TiDB Operator

如果要自定义 TiDB Operator，可以使用 `override_values` 变量来指定 Helm `values.yaml` 文件。该变量可以传递给 `tidb-cluster` 模块。

{{< copyable "" >}}

```
variable "override_values" {
  value = file("/path/to/values_file.yaml")
}
```

### 自定义节点池

集群是按区域 (regional) 而非按可用区 (zonal) 来创建的。也就是说，GKE 向每个可用区复制相同的节点池，以实现更高的可用性。但对于 Grafana 这样的监控服务来说，通常没有必要维护相同的可用性。你可以通过 `gcloud` 手动删除节点。

> **注意：**
>
> GKE 节点池通过实例组管理。如果你使用 `gcloud compute instances delete` 命令删除某个节点，GKE 会自动重新创建节点并将其添加到集群。

如果你需要从监控节点池中删掉一个节点，可采用如下步骤：

1. 获取托管的实例组和所在可用区。

    {{< copyable "shell-regular" >}}

    ```bash
    gcloud compute instance-groups managed list | grep monitor
    ```

    输出结果类似：

    ```
    gke-tidb-monitor-pool-08578e18-grp  us-west1-b  zone   gke-tidb-monitor-pool-08578e18  0     0            gke-tidb-monitor-pool-08578e18  no
    gke-tidb-monitor-pool-7e31100f-grp  us-west1-c  zone   gke-tidb-monitor-pool-7e31100f  1     1            gke-tidb-monitor-pool-7e31100f  no
    gke-tidb-monitor-pool-78a961e5-grp  us-west1-a  zone   gke-tidb-monitor-pool-78a961e5  1     1            gke-tidb-monitor-pool-78a961e5  no
    ```

    第一列是托管的实例组，第二列是所在可用区。

2. 获取实例组中的实例名字。

    {{< copyable "shell-regular" >}}

    ```bash
    gcloud compute instance-groups managed list-instances <the-name-of-the-managed-instance-group> --zone <zone>
    ```

    示例：

    {{< copyable "shell-regular" >}}

    ```bash
    gcloud compute instance-groups managed list-instances gke-tidb-monitor-pool-08578e18-grp --zone us-west1-b
    ```

    输出结果类似：

    ```
    NAME                                       ZONE        STATUS   ACTION  INSTANCE_TEMPLATE                     VERSION_NAME  LAST_ERROR
    gke-tidb-monitor-pool-08578e18-c7vd  us-west1-b  RUNNING  NONE    gke-tidb-monitor-pool-08578e18
    ```

3. 通过指定托管的实例组和实例的名称来删掉该实例。

    例如：

    {{< copyable "shell-regular" >}}

    ```bash
    gcloud compute instance-groups managed delete-instances gke-tidb-monitor-pool-08578e18-grp --instances=gke-tidb-monitor-pool-08578e18-c7vd --zone us-west1-b
    ```

## 销毁集群

可以通过如下命令销毁集群：

{{< copyable "shell-regular" >}}

```bash
terraform destroy
```

> **注意：**
>
> 在执行 `terraform destroy` 过程中，可能发生错误：`Error reading Container Cluster "tidb": Cluster "tidb" has status "RECONCILING" with message""`。当 GCP 升级 Kubernetes master 节点时会出现该问题。一旦问题出现，就无法删除集群，需要等待 GCP 升级结束，再次执行 `terraform destroy`。

### 删除磁盘

如果你不再需要之前的数据，并且想要删除正在使用的磁盘，有以下两种方法可以完成此操作：

- 手动删除：在 Google Cloud Console 中删除磁盘，或使用 `gcloud` 命令行工具执行删除操作。

- 在执行 `terraform destroy` 之前将 Kubernetes 的 PV (Persistent Volume) 回收策略设置为 `Delete`，具体操作为在 `terraform destroy` 之前运行以下 `kubectl`命令：

    {{< copyable "shell-regular" >}}

    ```bash
    kubectl --kubeconfig /path/to/kubeconfig/file get pvc -n namespace-of-tidb-cluster -o jsonpath='{.items[*].spec.volumeName}'|fmt -1 | xargs -I {} kubectl --kubeconfig /path/to/kubeconfig/file patch pv {} -p '{"spec":{"persistentVolumeReclaimPolicy":"Delete"}}'
    ```

    上述命令将获取 TiDB 集群命名空间中的 PVC (Persistent Volume Claim)，并将 PV 的回收策略设置为 `Delete`。在执行 `terraform destroy` 过程中删除 PVC 时，也会将磁盘删除。

    下面是一个名为 `change-pv-reclaimpolicy.sh` 的脚本。相对于仓库根目录来说，它在 `deploy/gcp` 中简化了上述过程。

    {{< copyable "shell-regular" >}}

    ```bash
    ./change-pv-reclaimpolicy.sh /path/to/kubeconfig/file <tidb-cluster-namespace>
    ```

## 管理多个 Kubernetes 集群

本节介绍管理多个 Kubernetes 集群的最佳实践，其中每个 Kubernetes 集群都安装了一个或多个 TiDB 集群。

在 TiDB 的案例中，Terraform 模块通常结合了几个子模块：

- `tidb-operator`：为 TiDB 集群提供 [Kubernetes Control Plane](https://kubernetes.io/docs/concepts/#kubernetes-control-plane)。
- `tidb-cluster`：在目标 Kubernetes 集群中创建资源池并部署 TiDB 集群。
- 一个 `vpc` 模块，一个 `bastion` 模块和一个 `project-credentials` 模块：专门用于 GKE 上的 TiDB 集群。

管理多个 Kubernetes 集群的最佳实践有以下两点：

1. 为每个 Kubernetes 集群创建一个新目录；
2. 根据具体需求，使用 Terraform 脚本将上述模块进行组合。

如果采用了最佳实践，集群中的 Terraform 状态不会相互干扰，并且扩展起来很方便。示例如下：

{{< copyable "shell-regular" >}}

```shell
# 假设已在项目根目录
mkdir -p deploy/gcp-staging
vim deploy/gcp-staging/main.tf
```

`deploy/gcp-staging/main.tf` 中的内容类似：

```hcl
provider "google" {
  credentials = file(var.GCP_CREDENTIALS_PATH)
  region      = var.GCP_REGION
  project     = var.GCP_PROJECT
}

// required for taints on node pools
provider "google-beta" {
  credentials = file(var.GCP_CREDENTIALS_PATH)
  region      = var.GCP_REGION
  project     = var.GCP_PROJECT
}

locals {
  gke_name        = "another-gke-name"
  credential_path = "${path.cwd}/credentials"
  kubeconfig      = "${local.credential_path}/kubeconfig_${var.gke_name}"
}


module "project-credentials" {
  source = "../modules/gcp/project-credentials"

  path = local.credential_path
}

module "vpc" {
  source              = "../modules/gcp/vpc"
  create_vpc          = true
  gcp_project         = var.GCP_PROJECT
  gcp_region          = var.GCP_REGION
  vpc_name            = "${locals.gke_name}-vpc-network"
  private_subnet_name = "${locals.gke_name}-private-subnet"
  public_subnet_name  = "${locals.gke_name}-public-subnet"
}

module "tidb-operator" {
  source                = "../modules/gcp/tidb-operator"
  gke_name              = locals.gke_name
  vpc_name              = module.vpc.vpc_name
  subnetwork_name       = module.vpc.private_subnetwork_name
  gcp_project           = var.GCP_PROJECT
  gcp_region            = var.GCP_REGION
  kubeconfig_path       = local.kubeconfig
  tidb_operator_version = "v1.0.0"
}

module "bastion" {
  source             = "../modules/gcp/bastion"
  vpc_name           = module.vpc.vpc_name
  public_subnet_name = module.vpc.public_subnetwork_name
  gcp_project        = var.GCP_PROJECT
  bastion_name       = "${locals.gke_name}-tidb-bastion"
}

# HACK: 强制使 Helm 依赖 GKE 集群
data "local_file" "kubeconfig" {
  depends_on = [module.tidb-operator.cluster_id]
  filename   = module.tidb-operator.kubeconfig_path
}
resource "local_file" "kubeconfig" {
  depends_on = [module.tidb-operator.cluster_id]
  content    = data.local_file.kubeconfig.content
  filename   = module.tidb-operator.kubeconfig_path
}

provider "helm" {
  alias          = "gke"
  insecure       = true
  install_tiller = false
  kubernetes {
    config_path = local_file.kubeconfig.filename
  }
}
module "tidb-cluster-a" {
  providers = {
    helm = "helm.gke"
  }
  source                     = "../modules/gcp/tidb-cluster"
  gcp_project                = var.GCP_PROJECT
  gke_cluster_location       = var.GCP_REGION
  gke_cluster_name           = locals.gke_name
  cluster_name               = "tidb-cluster-a"
  cluster_version            = "v3.0.1"
  kubeconfig_path            = module.tidb-operator.kubeconfig_path
  tidb_cluster_chart_version = "v1.0.0"
  pd_instance_type           = "n1-standard-1"
  tikv_instance_type         = "n1-standard-4"
  tidb_instance_type         = "n1-standard-2"
  monitor_instance_type      = "n1-standard-1"
}

module "tidb-cluster-b" {
  providers = {
    helm = "helm.gke"
  }
  source                     = "../modules/gcp/tidb-cluster"
  gcp_project                = var.GCP_PROJECT
  gke_cluster_location       = var.GCP_REGION
  gke_cluster_name           = locals.gke_name
  cluster_name               = "tidb-cluster-b"
  cluster_version            = "v3.0.1"
  kubeconfig_path            = module.tidb-operator.kubeconfig_path
  tidb_cluster_chart_version = "v1.0.0"
  pd_instance_type           = "n1-standard-1"
  tikv_instance_type         = "n1-standard-4"
  tidb_instance_type         = "n1-standard-2"
  monitor_instance_type      = "n1-standard-1"
}

output "how_to_ssh_to_bastion" {
  value= module.bastion.how_to_ssh_to_bastion
}

output "connect_to_tidb_cluster_a_from_bastion" {
  value = module.tidb-cluster-a.how_to_connect_to_default_cluster_tidb_from_bastion
}

output "connect_to_tidb_cluster_b_from_bastion" {
  value = module.tidb-cluster-b.how_to_connect_to_default_cluster_tidb_from_bastion
}

```

如上述代码所示，你可以在每个模块调用中省略几个参数，因为有合理的默认值，并且可以轻松地自定义配置。例如，如果你不需要调用堡垒模块，将其删除即可。

如果要自定义每个字段，可使用以下三种方法中的一种：

- 参考默认的 Terraform 模块。
- 参考每个模块的 `variables.tf` 文件来了解所有可用参数。
- 将这些模块集成到自己的 Terraform 工作流中。如果你熟悉 Terraform，这是推荐的做法。

> **注意：**
>
> - 创建新目录时，请注意其与 Terraform 模块的相对路径，这会影响模块调用期间的 `source` 参数。
> - 如果要在 tidb-operator 项目之外使用这些模块，务必确保复制整个 `modules` 目录并保持目录中每个模块的相对路径不变。
> - 由于 Terraform 的限制[（参见 hashicorp/terraform＃2430）](https://github.com/hashicorp/terraform/issues/2430#issuecomment-370685911)，上面的示例需要手动编写代码对 Helm provider 进行处理。建议将其保存在自己的 Terraform 脚本中。
>
>     如果你不愿意编写 Terraform 代码，还可以复制 `deploy/gcp` 目录来创建新的 Kubernetes 集群。但需要注意，当 Terraform 状态已存在于本地时，无法复制已被执行 `terraform apply` 命令的目录。在这种情况下，建议在复制目录之前克隆新的仓库。
