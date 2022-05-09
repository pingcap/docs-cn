---
title: 在 Operator 部署环境使用 PingCAP Clinic 诊断服务
summary: 详细介绍在使用 TiDB Operator 部署的集群上如何通过 PingCAP Clinic 诊断服务进行数据采集和快速检查。
---

# 在 Operator 部署环境使用 PingCAP Clinic 诊断服务

对于使用 TiDB Operator 部署的 TiDB 集群，PingCAP Clinic 诊断服务（以下简称为 PingCAP Clinic）可以通过 Diag 诊断客户端（以下简称为 Diag）与 Clinic Server 云诊断平台（以下简称为 Clinic Server）实现远程定位集群问题和本地快速检查集群状态。

> **注意：**
>
> 本文档**仅**适用于使用 TiDB Operator 部署的集群。如需查看适用于使用 TiUP 部署的集群，请参阅 [TiUP 环境的 Clinic 操作手册](/clinic/clinic-user-guide-for-tiup.md)。
>
> PingCAP Clinic 暂时**不支持**对 TiDB Ansible 部署的集群进行数据采集。

对于使用 TiDB Operator 部署的集群，Diag 需要部署为一个独立的 Pod。本文介绍如何使用 `kubectl` 命令创建并部署 Diag Pod 后，通过 API 调用继续数据采集和快速检查。

## 使用场景

通过 PingCAP Clinic 的 Diag 客户端，你可以方便快速地获取诊断数据，为集群进行基础的诊断：

- [使用 Clinic Diag 采集诊断数据](#使用-clinic-diag-采集诊断数据)
- [使用 Clinic Diag 快速诊断集群](#使用-clinic-diag-工具快速诊断集群)

## Clinic Diag 安装

本节详细介绍了安装 Clinic Diag 的步骤。

### 第 1 步：准备环境

Diag 部署前，请确认以下软件需求：

* Kubernetes v1.12 或者更高版本
* [TiDB Operator](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/tidb-operator-overview)
* [PersistentVolume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
* [RBAC](https://kubernetes.io/docs/admin/authorization/rbac)
* [Helm 3](https://helm.sh)

#### 安装 Helm

参考[使用 Helm](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/tidb-toolkit#%E4%BD%BF%E7%94%A8-helm) 安装 Helm 并配置 PingCAP 维护的 chart 仓库 `https://charts.pingcap.org/`。

```shell
helm search repo diag
NAME          CHART VERSION  APP VERSION  DESCRIPTION
pingcap/diag  v0.7.1         v0.7.1       Clinic Diag Helm chart for Kubernetes
```

#### 检查部署用户的权限

部署 Diag 所使用的用户需要具备创建以下类型 *Role* 和 *Cluster Role* 的权限：
*Role* 权限：
```
PolicyRule:
  Resources                               Non-Resource URLs  Resource Names  Verbs
  ---------                               -----------------  --------------  -----
  serviceaccounts                         []                 []              [get create delete]
  deployments.apps                        []                 []              [get create delete]
  rolebindings.rbac.authorization.k8s.io  []                 []              [get create delete]
  roles.rbac.authorization.k8s.io         []                 []              [get create delete]
  secrets                                 []                 []              [get list create delete]
  services                                []                 []              [get list create delete]
  pods                                    []                 []              [get list]
  tidbclusters.pingcap.com                []                 []              [get list]
  tidbmonitors.pingcap.com                []                 []              [get list]
```

*Cluster Role* 权限：
```
PolicyRule:
  Resources                                      Non-Resource URLs  Resource Names  Verbs
  ---------                                      -----------------  --------------  -----
  clusterrolebindings.rbac.authorization.k8s.io  []                 []              [get create delete]
  clusterroles.rbac.authorization.k8s.io         []                 []              [get create delete]
  pods                                           []                 []              [get list]
  secrets                                        []                 []              [get list]
  services                                       []                 []              [get list]
  tidbclusters.pingcap.com                       []                 []              [get list]
  tidbmonitors.pingcap.com                       []                 []              [get list]
```

> **注意：**
>
> - 如果集群情况可以满足最小权限部署的条件，可以使用更小的权限。详情见[最小权限部署](#第-3-步部署-clinic-diag-pod)。

可以通过以下步骤检查部署用户的权限：
（1）查看部署用户绑定的 Role 角色 和 clusterRole 角色：
```shell
kubectl describe rolebinding -n ${namespace} | grep ${user_name} -A 7
kubectl describe clusterrolebinding -n ${namespace} | grep ${user_name} -A 7
```

（2）查看对应角色具有的权限
```shell
kubectl describe role ${role_name} -n ${namespace}
kubectl describe clusterrole ${clusterrole_name} -n ${namespace}
```

### 第 2 步：登录 Clinic Server 获取 Access Token

Access Token（以下简称为 Token）用于 Diag 上传数据时的用户认证，保证数据上传到用户创建的组织下。需要注册登录 Clinic Server 后才能获取 Token。

#### 注册并登录 Clinic Server

登录 [Clinic Server](https://clinic.pingcap.com.cn/portal/#/login)，选择 **Sign in with AskTUG**，可以通过 TiDB 社区帐号登录 PingCAP Clinic 服务。若你还没有 TiDB 社区帐号，可以在登录界面进行注册。

#### 创建组织

用户第一次登录成功后，需要创建组织。根据页面提示输入组织名称，即可创建。创建成功后进入组织页面，可以获取 Token 后通过 Diag 的命令行或接口上传。

#### 获取客户端上传 Token

点击页面上的上传图标，选择 **Get Access Token For Diag Tool**，在弹出窗口中复制并保存 Token 信息。

![获取 token 截图](/media/clinic-get-token.png)

> **注意：**
>
> - 为了确保数据的安全性，TiDB 只在创建 Token 时显示 Token 信息。如果丢失了 Token 信息，你可以删除旧 Token 后重新创建。

### 第 3 步：部署 Diag Pod

根据集群的网络连接情况，你可以选择以下方式部署 Diag Pod：

- 在线快速部署：如果集群所在的网络能访问互联网，并且使用默认配置参数，推荐使用快速部署方式。
- 在线普通部署：如果集群所在的网络能访问互联网，需要自定义 Diag Pod 的配置参数，推荐使用在线普通部署方式。
- 离线部署：如果集群所在的网络不能访问互联网，可采用离线部署方式。
- 最小权限部署：如果目标集群所有节点都在同一个 namespace 可以将 Diag 部署到目标集群所在的 namespace，实现最小权限部署。

<SimpleTab>
<div label="在线快速部署">

1. 通过如下 `helm` 命令部署 Diag，从 Docker Hub 下载最新 Diag 镜像

    ```shell
    # namespace： 和 TiDB Operator 处于同一 namespace 中
    # diag.clinicToken: 请在 "https://clinic.pingcap.com.cn" 中登录并获取您的 Token。
    helm install --namespace tidb-admin diag-collector pingcap/diag --version v0.7.1 \
          --set diag.clinicToken=${clinic_token}
    ```

    > **注意：**
    >
    > 如果访问 Docker Hub 网速较慢，可以使用阿里云上的镜像：
    >
    > {{< copyable "shell-regular" >}}
    >
    > ```shell
    > helm install --namespace tidb-admin diag-collector pingcap/diag --version v0.7.1 \
    >     --set image.diagImage=registry.cn-beijing.aliyuncs.com/tidb/diag \
    >     --set diag.clinicToken= ${clinic_token}
    > ```

2. 部署成功后会输出以下结果：

    ```
    NAME: diag-collector
    LAST DEPLOYED: Tue Mar 15 13:00:44 2022
    NAMESPACE: tidb-admin
    STATUS: deployed
    REVISION: 1
    NOTES:
    Make sure diag-collector components are running:

      kubectl get pods --namespace tidb-admin -l app.kubernetes.io/instance=diag-collector
      kubectl get svc --namespace tidb-admin -l app.kubernetes.io/name=diag-collector
    ```

</div>
<div label="在线普通部署">

1. 获取你要部署的 Clinic Diag chart 中的 `values-diag-collector.yaml` 文件。

    ```shell
    mkdir -p ${HOME}/diag-collector && \
    helm inspect values pingcap/diag --version=${chart_version} > ${HOME}/diag-collector/values-diag-collector.yaml
    ```

    > **注意：**
    >
    > `${chart_version}` 在后续文档中代表 chart 版本，例如 `v0.7.1`，可以通过 `helm search repo -l diag` 查看当前支持的版本。

2. 配置 `values-diag-collector.yaml` 文件。

    将修改 `${HOME}/diag-collector/values-diag-collector.yaml` 文件设置你的 Access Token。

    其他项目例如：`limits`、`requests` 和 `volume`，请根据需要进行修改。

    > **注意：**
    >
    > - 请参照前文中[第 2 步：登录 Clinic Server 获取 Access Token](#第-2-步登录-clinic-server-获取-access-token)的内容获取 Token。
    > - 部署 `diag-collector`，会用到 `pingcap/diag` 镜像，如果无法从 Docker Hub 下载该镜像，可以修改 `${HOME}/diag-collector/values-diag-collector.yaml` 文件中的 `image.diagImage` 为 `registry.cn-beijing.aliyuncs.com/tidb/diag`。

3. 部署 Clinic Diag。

    ```shell
    helm install diag-collector pingcap/diag --namespace=tidb-admin --version=${chart_version} -f ${HOME}/diag-collector/values-diag-collector.yaml && \
    kubectl get pods --namespace tidb-admin -l app.kubernetes.io/instance=diag-collector
    ```

    > **注意：**
    >
    > - namespace 应设置为和 TiDB Operator 相同，若没有部署 TiDB Operator，请先部署 TiDB Operator 后再部署 Clinic Diag。

4. 【可选操作】设置持久化数据卷。

    本操作可以为 Diag 挂载数据卷，以提供持久化数据的能力。修改 `${HOME}/diag-collector/values-diag-collector.yaml` 文件，配置 `diag.volume` 字段可以选择需要的 volume，下面为使用 PVC、Host 类型的示例：

    ```
    # 使用 PVC 类型
    volume:
      persistentVolumeClaim:
        claimName: local-storage-diag
    ```

    ```
    # 使用 Host 类型
    volume:
      hostPath:
        path: /data/diag
    ```

    > **注意：**
    >
    > - 不支持多盘挂载
    > - 支持任意类型的 StorageClass

5. 【可选操作】升级 Clinic Diag。

    如果需要升级 Clinic Diag，请先修改 `${HOME}/diag-collector/values-diag-collector.yaml` 文件，然后执行下面的命令进行升级：

    ```shell
    helm upgrade diag-collector pingcap/diag --namespace=tidb-admin -f ${HOME}/diag-collector/values-diag-collector.yaml
    ```

</div>
<div label="离线部署">

如果服务器无法访问互联网，需要按照下面的步骤来离线安装 Clinic Diag：

1. 下载 Clinic Diag chart。

    如果服务器无法访问互联网，就无法通过配置 Helm repo 来安装 Clinic Diag 组件以及其他应用。这时，需要在能访问互联网的机器上下载集群安装需用到的 chart 文件，再拷贝到服务器上。

    通过以下命令，下载 Clinic Diag chart 文件：

    {{< copyable "shell-regular" >}}

    ```shell
    wget http://charts.pingcap.org/diag-v0.7.1.tgz
    ```

    将 `diag-v0.7.1.tgz` 文件拷贝到服务器上并解压到当前目录：

    {{< copyable "shell-regular" >}}

    ```shell
    tar zxvf diag-v0.7.1.tgz
    ```

2. 下载 Clinic Diag 运行所需的 Docker 镜像。

    需要在能访问互联网的机器上将 Clinic Diag 用到的 Docker 镜像下载下来并上传到服务器上，然后使用 `docker load` 将 Docker 镜像安装到服务器上。

    TiDB Operator 用到的 Docker 镜像为 `pingcap/diag:v0.7.1`，通过下面的命令将镜像下载下来：

    {{< copyable "shell-regular" >}}

    ```shell
    docker pull pingcap/diag:v0.7.1
    docker save -o diag-v0.7.1.tar pingcap/diag:v0.7.1
    ```

    接下来将这些 Docker 镜像上传到服务器上，并执行 `docker load` 将这些 Docker 镜像安装到服务器上：

    {{< copyable "shell-regular" >}}

    ```shell
    docker load -i diag-v0.7.1.tar
    ```

3. `values-diag-collector.yaml` 文件。

    修改 `${HOME}/diag-collector/values-diag-collector.yaml` 文件设置你的 Access Token。

    其他项目例如：`limits`、`requests` 和 `volume`，请根据需要进行修改。

    > **注意：**
    >
    > - 请参照前文中[第 2 步：登录 Clinic Server 获取 Access Token](#第-2-步-：-登录-clinic-server-获取-clinic-token)的内容获取 Token。
    > - 部署 `diag-collector` 会用到 `pingcap/diag` 镜像，如果无法从 Docker Hub 下载该镜像，可以修改 `${HOME}/diag-collector/values-diag-collector.yaml` 文件中的 `image.diagImage` 为 `registry.cn-beijing.aliyuncs.com/tidb/diag`。

4. 安装 Clinic Diag。

    使用下面的命令安装 Clinic Diag：

    {{< copyable "shell-regular" >}}

    ```shell
    helm install diag-collector ./diag --namespace=tidb-admin
    ```

    > **注意：**
    > `namespace` 应设置为和 TiDB Operator 相同，若没有部署 TiDB Operator，请先部署 TiDB Operator 后再部署 Clinic Diag。

5. 【可选操作】设置持久化数据卷。

    本操作可以为 Diag 挂载数据卷，以提供持久化数据的能力。修改 `${HOME}/diag-collector/values-diag-collector.yaml` 文件，配置 `diag.volume` 字段可以选择需要的 volume，下面为使用 PVC、Host 类型的示例：

    ```
    # 使用 PVC 类型
    volume:
      persistentVolumeClaim:
        claimName: local-storage-diag
    ```

    ```
    # 使用 Host 类型
    volume:
      hostPath:
        path: /data/diag
    ```

    > **注意：**
    >
    > - 不支持多盘挂载
    > - 支持任意类型的 StorageClass

</div>
<div label="最小权限部署">

> **注意：**
>
> - 本部署方式将 Diag 部署到目标集群所在的 namespace，Diag 只能采集 namespace 中的数据，不能进行跨 namespace 采集数据。

1. 确认部署用户的权限

    最小权限部署会在部署的 namespace 中创建具备以下权限的 Role，需要部署 Diag 所使用的用户在 namespace 中有创建该类型 *Role* 的权限。

    ```
    Resources                               Non-Resource URLs  Resource Names  Verbs
    ---------                               -----------------  --------------  -----
    serviceaccounts                         []                 []              [get create delete]
    deployments.apps                        []                 []              [get create delete]
    rolebindings.rbac.authorization.k8s.io  []                 []              [get create delete]
    roles.rbac.authorization.k8s.io         []                 []              [get create delete]
    secrets                                 []                 []              [get list create delete]
    services                                []                 []              [get list create delete]
    pods                                    []                 []              [get list]
    tidbclusters.pingcap.com                []                 []              [get list]
    tidbmonitors.pingcap.com                []                 []              [get list]
    ```

2. 通过如下 `helm` 命令部署 Clinic Diag，从 Docker Hub 下载最新 Diag 镜像

    {{< copyable "shell-regular" >}}

    ```shell
    helm install --namespace tidb-cluster diag-collector pingcap/diag --version v0.7.1 \
        --set diag.clinicToken=${clinic_token} \
        --set diag.clusterRoleEnabled=false
    ```

    > **注意：**
    >
    > - 如果集群未开启 TLS，可以设置 `diag.tlsEnabled=false`，此时创建的 Role 将不会带有 `secrets` 的 `get` 和 `list` 权限。
    >
    > {{< copyable "shell-regular" >}}
    >
    >  ```shell
    > helm install --namespace tidb-cluster diag-collector pingcap/diag --version v0.7.1 \
    >        --set diag.clinicToken=${clinic_token} \
    >        --set diag.tlsEnabled=false \
    >        --set diag.clusterRoleEnabled=false
    > ```
    >
    > - 如果访问 Docker Hub 网速较慢，可以使用阿里云上的镜像：
    >
    > {{< copyable "shell-regular" >}}
    >
    > ```shell
    > helm install --namespace tidb-cluster diag-collector pingcap/diag --version v0.7.1 \
    >      --set image.diagImage=registry.cn-beijing.aliyuncs.com/tidb/diag \
    >      --set diag.clinicToken= ${clinic_token} \
    >      --set diag.clusterRoleEnabled=false
    > ```

3. 部署成功后会输出以下结果：

    ```
    NAME: diag-collector
    LAST DEPLOYED: Tue Mar 15 13:00:44 2022
    NAMESPACE: tidb-cluster
    STATUS: deployed
    REVISION: 1
    NOTES:
    Make sure diag-collector components are running:
      kubectl get pods --namespace tidb-cluster -l app.kubernetes.io/instance=diag-collector
      kubectl get svc --namespace tidb-cluster -l app.kubernetes.io/name=diag-collector
    ```

</div>
</SimpleTab>

### 第 4 步：检查 Clinic Diag Pod 的运行状态

使用以下命令查询 Diag 状态：

{{< copyable "shell-regular" >}}

```shell
kubectl get pods --namespace tidb-admin -l app.kubernetes.io/instance=diag-collector
```

Pod 正常运行的输出如下：

```
NAME                             READY   STATUS    RESTARTS   AGE
diag-collector-5c9d8968c-clnfr   1/1     Running   0          89s
```

## 使用 Clinic Diag 采集诊断数据

Clinic Diag 可以快速抓取 TiDB 集群的诊断数据，其中包括监控数据、配置信息等。

### 使用场景

以下场景适用于使用 Clinic Diag 采集诊断数据：

- 当集群出现问题，要咨询 PingCAP 技术支持时，需要提供集群诊断数据，协助技术支持人员定位问题。
- 保留集群诊断数据，进行后期分析。

> **注意：**
>
> 对于使用 TiDB Operator 部署的集群，暂不支持收集日志、配置文件、系统硬件信息等诊断数据。

### 第 1 步：确定需要采集的数据

如需查看 Clinic Diag 支持采集的数据详细列表，请参阅 [Clinic 数据采集说明 - Operator 环境](https://clinic-docs.vercel.app/docs/getting-started/clinic-data-instruction-for-operator)。建议采集完整的监控数据，以便提升诊断效率。

### 第 2 步：采集数据

Clinic Diag 工具的各项操作均会通过 API 完成。

- 如需查看完整的 API 定义文档，可访问节点 `http://${host}:${port}/api/v1`。

- 如需查看节点 IP，可使用以下命令：

    {{< copyable "bash" >}}

    ```bash
    kubectl get node | grep node
    ```

- 如需查看 `diag-collector service` 的端口号，可使用以下命令：

    {{< copyable "bash" >}}

    ```bash
    kubectl get service -n tidb-admin
    ```

    输出示例为：

    ```
    NAME                 TYPE           CLUSTER-IP           EXTERNAL-IP   PORT(S)              AGE
    diag-collector   NodePort   10.111.143.227   <none>            4917:31917/TCP   18m
    ```

    在上述示例中：

    - 从 Kubernetes 集群外访问该 Service 的端口为 `31917`。
    - 该 Service 类型为 NodePort。你可以通过 Kubernetes 集群中任一宿主机的 IP 地址 `${host}` 和端口号 `${port}` 访问该服务。

#### 1. 发起采集数据请求

通过 API 请求发起一次数据采集任务：

```bash
curl -s http://${host}:${port}/api/v1/collectors -X POST -d '{"clusterName": "${cluster-name}","namespace": "${cluster-namespace}","from": "2022-02-08 12:00 +0800","to": "2022-02-08 18:00 +0800"}'
```

API 调用参数说明：

- `clusterName`：TiDB 集群名称。
- `namespace`：TiDB 集群所在的 `namespace 名称`（不是 TiDB Operator 所在的 `namespace`）。
- `collector`：可选参数，可配置需要采集的数据类型，支持 [monitor, config, perf]。若不配置该参数，默认采集 monitor 和 config 数据。
- `from` 和 `to`：分别为采集的起止时间。`+0800` 代表时区，支持的时间格式如下：

    ```
    "2006-01-02T15:04:05Z07:00"
    "2006-01-02T15:04:05.999999999Z07:00"
    "2006-01-02 15:04:05 -0700",
    "2006-01-02 15:04 -0700",
    "2006-01-02 15 -0700",
    "2006-01-02 -0700",
    "2006-01-02 15:04:05",
    "2006-01-02 15:04",
    "2006-01-02 15",
    "2006-01-02",
    ```

命令输出结果示例如下：

```
"clusterName": "${cluster-namespace}/${cluster-name}",
"collectors"            "config",
    "monitor"
],
"date": "2021-12-10T10:10:54Z",
"from": "2021-12-08 12:00 +0800",
"id": "fMcXDZ4hNzs",
"status": "accepted",
"to": "2021-12-08 18:00 +0800"
```

API 返回信息说明：

- `date`：采集任务发起的时间。
- `id`：此任务的 ID 编号。在之后的操作中，此 ID 为定位到此次任务的唯一信息。
- `status`：此任务的当前状态，`accepted` 代表采集任务进入队列。

> **注意：**
>
> 返回命令结果只代表数据采集任务已经开始，并不表示采集已完成。要了解采集是否全部完成，需要通过下一步操作来查看采集任务的状态。

#### 2. 查看采集数据任务状态

通过 API 请求，获取采集任务的状态：

```bash
curl -s http://${host}:${port}/api/v1/collectors/${id}
{
            "clusterName": "${cluster-namespace}/${cluster-name}",
        "collectors": [
            "config",
            "monitor"
        ],
        "date": "2021-12-10T10:10:54Z",
        "from": "2021-12-08 12:00 +0800",
        "id": "fMcXDZ4hNzs",
        "status": "finished",
        "to": "2021-12-08 18:00 +0800"
}
```

其中，`id` 为任务的 ID 编号，在上述例子中为 `fMcXDZ4hNzs`。该步骤命令返回格式与上一步（[发起采集数据请求](#发起采集数据请求)）的是相同的。

如果该任务的状态变为 `finished`，则表示数据采集已完成。

#### 3. 查看已采集的数据集信息

完成采集任务后，可以通过 API 请求来获取数据集的采集时间和数据大小信息：

```bash
curl -s http://${host}:${port}/api/v1/data/${id}
{
        "clusterName": "${cluster-namespace}/${cluster-name}",
        "date": "2021-12-10T10:10:54Z",
        "id": "fMcXDZ4hNzs",
        "size": 1788980746
}
```

通过本命令，**只能**查看数据集的文件包大小，不能查看具体数据。

### 第 3 步：上传数据集

把诊断数据提供给 PingCAP 技术支持人员时，需要将数据上传到 Clinic Server，然后将其数据链接发送给技术支持人员。Clinic Server 为 PingCAP Clinic 的云服务，可提供更安全的诊断数据存储和共享。

#### 1. 发起上传任务

通过 API 请求打包并上传收集完成的数据集：

```bash
curl -s http://${host}:${port}/api/v1/data/${id}/upload -XPOST
{
        "date": "2021-12-10T11:26:39Z",
        "id": "fMcXDZ4hNzs",
        "status": "accepted"
}
```

返回命令结果只代表上传任务开始已经开始，并不表示已完成上传。要了解上传任务是否完成，需要通过下一步操作来查看任务状态。

#### 2. 查看上传任务状态

通过 API 请求，查看上传任务的状态：

```bash
curl -s http://${host}:${port}/api/v1/data/${id}/upload
{
        "date": "2021-12-10T10:23:36Z",
        "id": "fMcXDZ4hNzs",
        "result": "\"https://clinic.pingcap.com:4433/diag/files?uuid=ac6083f81cddf15f-34e3b09da42f74ec-ec4177dce5f3fc70\"",
        "status": "finished"
}
```

如果状态变为 `finished`，则表示打包与上传均已完成。此时，`result` 表示 Clinic Server 查看此数据集的链接，即需要发给 PingCAP 技术支持人员的数据访问链接。

### 可选操作：本地查看数据

采集完成的数据会保存在 Pod 的 `/diag/collector/diag-${id}` 目录中，可以通过以下方法进入 Pod 查看此数据：

#### 1. 获取 `diag-collector-pod-name`

执行如下命令，获取 `diag-collector-pod-name`：

{{< copyable "bash" >}}

```bash
kubectl get pod --all-namespaces  | grep diag
```

输出结果示例：

```
tidb-admin      diag-collector-69bf78478c-nvt47               1/1     Running            0          19h
```

其中，Diag Pod 的名称为 `diag-collector-69bf78478c-nvt47`，其所在的 `namespace` 为 `tidb-admin`。

#### 2. 进入 Pod 并查看数据

{{< copyable "bash" >}}

```bash
kubectl exec -n ${namespace} ${diag-collector-pod-name}  -it -- sh
cd  /diag/collector/diag-${id}
```

其中，`${namespace}` 需要替换为 TiDB Operator 所在的 `namespace` 名称（通常为 `tidb-admin`）。

## 使用 Clinic Diag 工具快速诊断集群

PingCAP Clinic 支持对集群的健康状态进行快速地诊断，主要支持检查配置项内容，快速发现不合理的配置项。

### 使用步骤

本节详细介绍通过 PingCAP Clinic 快速诊断使用 TiDB Operator 部署的集群的具体方法。

1. 采集数据

    有关采集数据具体方法，可参考[使用 Clinic Diag 工具采集诊断数据](#第2步采集数据)。

2. 快速诊断

    通过 API 请求，在本地对集群进行快速诊断：

    {{< copyable "bash" >}}

    ```bash
    curl -s http://${host}:${port}/api/v1/data/${id}/check -XPOST -d '{"types": ["config"]}'
    ```

    其中，`id` 为采集数据任务的 ID 编号，在上述例子中为 `fMcXDZ4hNzs`。

    请求结果中会列出已发现的配置风险内容和建议配置的知识库链接，具体示例如下：

    ```
    # 诊断结果报告
    basic 2022-02-07T12:00:00+08:00

    ## 1. 诊断集群名称等基础信息
    - Cluster ID: 7039963340562527412
    - Cluster Name: basic
    - Cluster Version: v5.4.0

    ## 2. 诊断数据来源信息
    - Sample ID: fPrz0RnDxRn
    - Sampling Date: 2022-02-07T12:00:00+08:00
    - Sample Content:: [monitor config]

    ## 3. 诊断结果信息
    In this inspection, 21 rules were executed.
    The results of **3** rules were abnormal and needed to be further discussed with support team.
    The following is the details of the abnormalities.

    ### 配置规则
    The configuration rules are all derived from PingCAP’s OnCall Service.
    If the results of the configuration rules are found to be abnormal, they may cause the cluster to fail.
    There were **3** abnormal results.

    #### Rule Name: tidb-max-days
    - RuleID: 100
    - Variation: TidbConfig.log.file.max-days
    - For more information, please visit: https://s.tidb.io/msmo6awg
    - Check Result:
    TidbConfig_172.20.21.213:4000   TidbConfig.log.file.max-days:0   warning

    #### Rule Name: pdconfig-max-days
    - RuleID: 209
    - Variation: PdConfig.log.file.max-days
    - For more information, please visit: https://s.tidb.io/jkdqxudq
    - Check Result:
    PdConfig_172.20.22.100:2379   PdConfig.log.file.max-days:0   warning
    PdConfig_172.20.14.102:2379   PdConfig.log.file.max-days:0   warning
    PdConfig_172.20.15.222:2379   PdConfig.log.file.max-days:0   warning

    #### Rule Name: pdconfig-max-backups
    - RuleID: 210
    - Variation: PdConfig.log.file.max-backups
    - For more information, please visit: https://s.tidb.io/brd9zy53
    - Check Result:
    PdConfig_172.20.22.100:2379   PdConfig.log.file.max-backups:0   warning
    PdConfig_172.20.14.102:2379   PdConfig.log.file.max-backups:0   warning
    PdConfig_172.20.15.222:2379   PdConfig.log.file.max-backups:0   warning

    Result report and record are saved at /diag-fPrz0RnDxRn/report-220208030210
    ```

    上述示例中：

    - 第一部分为诊断集群名称等基础信息。
    - 第二部分为断数据来源信息。
    - 第三部分展示诊断结果信息，包括发现的可能的配置问题。对于每条发现的配置问题，都提供知识库链接，以便查看详细的配置建议。
    - 最后一行为诊断结果文档的保存路径。
