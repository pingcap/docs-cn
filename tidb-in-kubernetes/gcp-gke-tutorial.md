# 在 GCP GKE 上部署 TiDB Operator 和 TiDB 集群

本文档描述如何使用个人电脑 (Linux or macOS) 在 GCP GKE 上部署 TiDB Operator 和 TiDB 集群用于开发或者测试。

## 环境需求

部署之前请确认满足以下软件需求:

* [Google Cloud SDK](https://cloud.google.com/sdk/install)
* [terraform](https://www.terraform.io/downloads.html) >= 0.12
* [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/#install-kubectl) >= 1.14
* [helm](https://github.com/helm/helm/blob/master/docs/install.md#installing-the-helm-client) >= 2.9.0 and < 3.0.0
* [jq](https://stedolan.github.io/jq/download/)

## 配置

为保证顺利部署，需要进行一些配置。

### 配置 Google Cloud SDK

安装 Google Cloud SDK 后，需要执行 `gcloud init` 进行 [初始化](https://cloud.google.com/sdk/docs/initializing)。

### 配置 APIs

如果使用的 GCP 项目是新项目，请启用相关的 APIs：

```bash
gcloud services enable cloudresourcemanager.googleapis.com && \
gcloud services enable cloudbilling.googleapis.com && \
gcloud services enable iam.googleapis.com && \
gcloud services enable compute.googleapis.com && \
gcloud services enable container.googleapis.com
```

### 配置 Terraform

Terraform 脚本执行需要 3 个环境变量，你可以等 Terraform 提示你输入或者提前 `export`。需要的 3 个环境变量如下：

* `TF_VAR_GCP_CREDENTIALS_PATH`: GCP 证书文件路径
    - 建议给 Terraform 新建服务账号使用，参考 [服务账号](https://cloud.google.com/iam/docs/creating-managing-service-accounts) 创建服务账号并给它授予 `Project Editor` 权限。
    - 参考 [服务账号密钥](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) 创建服务账号密钥，创建过程中选择 `JSON` 类型密钥，创建完成后，自动下载的 `JSON` 文件就是需要的证书文件。
* `TF_VAR_GCP_REGION`: 创建资源的区域，比如: `us-west1`。
* `TF_VAR_GCP_PROJECT`: GCP 项目。

你可以在终端中设置这 3 个环境变量：

```bash
# 替换下面信息为正确的信息
export TF_VAR_GCP_CREDENTIALS_PATH="/Path/to/my-project.json"
export TF_VAR_GCP_REGION="us-west1"
export TF_VAR_GCP_PROJECT="my-project"
```

也可以将上面的命令追加到 `~/.bash_profile` 这样下次登录会自动 `export`。

## 部署

默认部署会创建一个新的 VPC，两个子网，一个 f1-micro 实例作为堡垒机，和包含如下实例作为工作节点的 GKE 集群：

* 3 台 n1-standard-4 实例，部署 PD
* 3 台 n1-highmem-8 实例，部署 TiKV
* 3 台 n1-standard-16 实例，部署 TiDB
* 3 台 n1-standard-2 实例，部署监控组件

> **注意**: 工作节点的数量取决于指定 region 中可用区的数量，大部分 region 有 3 个可用区，但是 us-central1 有 4 个。参考 [Regions and Zones](https://cloud.google.com/compute/docs/regions-zones/) 获取更多信息，参考 [自定义](#自定义) 部分自定义区域集群的节点池。

如上所述，默认部署需要 91 个 CPU，超过了 GCP 项目的默认配额，可以参考 [配额](https://cloud.google.com/compute/quotas) 增加项目配额。如果你要扩容，同样需要更多的 CPU。

现在你已经配置好所有信息，你可以启动脚本，部署 TiDB 集群：

```bash
git clone --depth=1 https://github.com/pingcap/tidb-operator
cd tidb-operator/deploy/gcp
terraform init
terraform apply
```

如果你之前没有 `export` 那 3 个环境变量，执行 `terraform apply` 过程中会提示你设置，详情请参考 [配置 Terraform](#配置-terraform)。

整个过程可能需要 10 分钟甚至更长时间。`terraform apply` 执行成功后，会输出类似如下信息:

```
Apply complete! Resources: 17 added, 0 changed, 0 destroyed.

Outputs:

cluster_id = my-cluster
cluster_name = my-cluster
how_to_connect_to_mysql_from_bastion = mysql -h 172.31.252.20 -P 4000 -u root
how_to_ssh_to_bastion = gcloud compute ssh bastion --zone us-west1-b
kubeconfig_file = ./credentials/kubeconfig_my-cluster
monitor_ilb_ip = 35.227.134.146
monitor_port = 3000
region = us-west1
tidb_ilb_ip = 172.31.252.20
tidb_port = 4000
tidb_version = v3.0.0-rc.1
```

## 访问数据库

要访问部署的 TiDB 集群，通过下面命令，首先 `ssh` 到堡垒机，然后通过 MySQL client（用上面输出的信息替换 `<>` 部分内容) 访问 TiDB：

```bash
gcloud compute ssh bastion --zone <zone>
mysql -h <tidb_ilb_ip> -P 4000 -u root
```

## 集群交互

你可以通过 `kubectl` 和 `helm` 使用 kubeconfig 文件 `credentials/kubeconfig_<cluster_name>` 和 GKE 集群交互。`cluster_name` 默认为 `my-cluster`，可以通过 `variables.tf` 修改。

```bash
# 指定 --kubeconfig 参数
kubectl --kubeconfig credentials/kubeconfig_<cluster_name> get po -n tidb
helm --kubeconfig credentials/kubeconfig_<cluster_name> ls

# 或者设置 KUBECONFIG 环境变量
export KUBECONFIG=$PWD/credentials/kubeconfig_<cluster_name>
kubectl get po -n tidb
helm ls
```

# 升级 TiDB 集群

编辑 `variables.tf` 文件，修改 `tidb_version` 变量到更高版本，然后运行 `terraform apply` 就可以升级 TiDB 集群。

比如，要升级 TiDB 集群到 3.0.0-rc.2，修改 `tidb_version` 为 `v3.0.0-rc.2`：

```
variable "tidb_version" {
  description = "TiDB version"
  default     = "v3.0.0-rc.2"
}
```

升级过程会持续一段时间，你可以通过命令持续观察升级进度: `kubectl --kubeconfig credentials/kubeconfig_<cluster_name> get po -n tidb --watch`。

然后你可以 [访问数据库](#访问数据库) 并通过 `tidb_version()` 确认集群是否升级成功:

```sql
MySQL [(none)]> select tidb_version();
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

## 扩容

按需修改 `variables.tf` 文件中的 `tikv_count`，`tikv_replica_count`，`tidb_count` 和 `tidb_replica_count` 变量，然后运行 `terraform apply` 升级 TiDB 集群。

由于缩容过程中无法确定哪个节点会被删除，因此目前不支持集群缩容。扩容过程会持续几分钟，你可以通过命令持续观察进度: `kubectl --kubeconfig credentials/kubeconfig_<cluster_name> get po -n tidb --watch`。

比如，可以将 `tidb_count` 从 1 改为 2 扩容 TiDB:

```
variable "tidb_count" {
  description = "Number of TiDB nodes per availability zone"
  default     = 2
}
```

> **注意**: 增加节点数量会在每个可用区都增加节点。

## 自定义

你可以按需修改 `variables.tf` 文件中的默认值，比如集群名称和镜像版本等。

### 自定义 GCP 资源

GCP 允许 `n1-standard-1` 或者更大的实例类型挂载本地 SSD，这提供了更好的自定义特性。

### 自定义 TiDB 参数配置

目前，暴露出来可以自定义修改的 TiDB 参数并不多。但是你可以在部署集群之前，修改 `templates/tidb-cluster-values.yaml.tpl` 文件中的配置。如果集群已经在运行，每次修改 `templates/tidb-cluster-values.yaml.tpl` 文件中的配置都需要执行 `terraform apply`，并手动删除 Pod(s)。

### 自定义节点池

集群是按区域创建的，而不是按可用区，也就是说 GKE 在区域内每个可用区创建同样的节点池，这是为了达到更高的可用性，但是对于监控服务，比如 Grafana，就没有太大必要。你可以通过 `gcloud` 手动删除节点。

> **注意**: GKE 节点池通过实例组管理，如果你通过 `gcloud compute instances delete` 删除某个节点，GKE 会自动重新创建节点并加到集群。

假如你需要从监控节点池中删掉一个节点，首先:

```bash
gcloud compute instance-groups managed list | grep monitor
```

结果类似下面输出:

```bash
gke-my-cluster-monitor-pool-08578e18-grp  us-west1-b  zone   gke-my-cluster-monitor-pool-08578e18  0     0            gke-my-cluster-monitor-pool-08578e18  no
gke-my-cluster-monitor-pool-7e31100f-grp  us-west1-c  zone   gke-my-cluster-monitor-pool-7e31100f  1     1            gke-my-cluster-monitor-pool-7e31100f  no
gke-my-cluster-monitor-pool-78a961e5-grp  us-west1-a  zone   gke-my-cluster-monitor-pool-78a961e5  1     1            gke-my-cluster-monitor-pool-78a961e5  no
```

第一列是托管的实例组，第二列是所在可用区。你还需要获取实例组中的实例名字：

```bash
gcloud compute instance-groups managed list-instances <the-name-of-the-managed-instance-group> --zone <zone>
```

示例:

```bash
$ gcloud compute instance-groups managed list-instances gke-my-cluster-monitor-pool-08578e18-grp --zone us-west1-b

NAME                                       ZONE        STATUS   ACTION  INSTANCE_TEMPLATE                     VERSION_NAME  LAST_ERROR
gke-my-cluster-monitor-pool-08578e18-c7vd  us-west1-b  RUNNING  NONE    gke-my-cluster-monitor-pool-08578e18
```

现在你可以通过指定托管的实例组和实例的名称删掉这个实例：

```bash
gcloud compute instance-groups managed delete-instances gke-my-cluster-monitor-pool-08578e18-grp --instances=gke-my-cluster-monitor-pool-08578e18-c7vd --zone us-west1-b
```

## 销毁集群

可以通过如下命令销毁集群:

```bash
terraform destroy
```

如果你不再需要之前的数据，执行完 `terraform destroy` 后，你可以通过 Google Cloud 控制台或者 `gcloud` 删除磁盘。

> **注意**: 执行 `terraform destroy` 过程中，可能发生如下错误： `Error reading Container Cluster "my-cluster": Cluster "my-cluster" has status "RECONCILING" with message""`。当 GCP 升级 kubernetes master 节点时，会出现这个问题。当这个问题出现，集群无法删除，需要等待 GCP 升级结束，再次执行 `terraform destroy`。


## 更多信息

请参考 [operation guide](./operation-guide.md)。
