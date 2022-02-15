---
title: Operator 环境的 Clinic 诊断服务操作手册
summary: 详细介绍在使用 TiDB Operator 部署的集群上如何通过 Clinic Diag 工具进行数据采集和快速检查。
---

# Operator 环境的 Clinic 诊断服务操作手册

对于使用 TiDB Operator 部署的集群，Clinic 诊断服务可以通过 Clinic Diag 工具与 Clinic Server 云服务对该集群进行数据采集和集群快速诊断。

> **注意：**
>
> 本文档**仅**适用于使用 TiDB Operator 部署的集群。如需查看适用于使用 TiUP 部署的集群，请参阅 [TiUP 环境的 Clinic 操作手册](clinic/clinic-user-guide-for-tiup.md)。
> Clinic 诊断服务暂时**不支持**对开启了 TLS 加密的集群和使用 TiDB Ansible 部署的集群进行数据采集。

对于使用 TiDB Operator 部署的集群，Clinic Diag 需要部署为一个独立的 Pod。本文介绍如何使用 kubectl 命令创建并部署 Diag pod 后，通过 API 调用继续数据采集和快速检查。

## 使用场景

通过 Clinic 诊断服务的 Diag 工具，你可以方便快速地获取诊断数据，为集群进行基础的诊断：

- [使用 Clinic Diag 工具采集诊断数据](#使用-clinic-diag-工具采集诊断数据)
- [使用 Clinic Diag 工具快速诊断集群](#使用-clinic-diag-工具快速诊断集群)

## Clinic Diag 工具安装

本节详细介绍了安装 Clinic Diag 工具的步骤。

### 第 1 步：编辑 MANIFEST 文件

安装 Clinic Diag 工具时，可以使用以下 3 个 yaml 文件模板为 MANIFEST 文件：

- `diag.yaml`
- `rbac.yaml`
- `cert.yaml`

使用文件模板时，请按照下文中的具体说明将文件的关键参数修改为实际值。

#### `diag.yaml` 文件

在使用 `diag.yaml` 文件模板时，需要将文件中的用户名和密码修改为真实的用户名和密码。

在该模板中使用的镜像地址为 `https://drive.google.com/file/d/1sNRQDFhKgi_Gl6wPt7dHbQLuQXbd03YW/view?usp=sharing`。

> **注意：**
>
> 目前 Clinic 在 Beta 受邀测试使用阶段，请联系与你对接的 PingCAP 技术人员获取试用账号。

{{< copyable "shell-regular" >}}

```bash
  env:
        - name: NAMESPACE
          valueFrom:
            fieldRef:
              apiVersion: v1
              fieldPath: metadata.namespace
        - name: CLINIC_USERNAME
          value: "username"
        - name: CLINIC_PASSWORD
          value: "password
```

参数说明：
- `CLINIC_USERNAME`：上传所需的用户名
- `CLINIC_PASSWORD`：上传所需的密码

#### `rbac.yaml` 文件

在使用以下的 `rbac.yaml` 模板时，需要把 `${namespace}` 占位符修改为部署 TiDB Operator 所在的 `namespace` 名称（通常为 tidb-admin）。

{{< copyable "shell-regular" >}}

```bash
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: diag
subjects:
- kind: ServiceAccount
  namespace: ${namespace}
  name: pingcap-clinic
roleRef:
  kind: Role
  name: pingcap-clinic
  apiGroup: rbac.authorization.k8s.io
```

#### `cert.yaml ` 文件

该文件的内容默认无需修改。如需更换上传前对压缩包加密所使用的证书，可在该文件中替换证书内容。

### 第 2 步：部署 Diag Pod

编写 MANIFEST 文件后，通过使用 `kubectl` 命令把该文件应用到 Kubernetes 集群来实际创建 Diag Pod：

{{< copyable "shell-regular" >}}

```bash
kubectl apply -n ${namespace} -f manifest
```

其中，`${namespace}` 应替换为 TiDB Operator 所在的 `namespace` 名称，该名称通常为 `tidb-admin`。

### 第 3 步：查看 Diag Pod 的运行状态

使用以下命令，查看名为 `diag-collector-xxx` 的 Pod。

待其状态变为 Running 后，再进行下一步操作。如果状态一直不能变成 Running，可查看该 Pod 日志确认是否有报错。

{{< copyable "shell-regular" >}}

```bash
kubectl get pod --all-namespaces | grep diag
tidb-admin   diag-collector-69bf78478c-d24sn        1/1   Running      0     2m16s
```

## 使用 Clinic Diag 工具采集诊断数据

Clinic Diag 工具可以快速抓取 TiDB 集群的诊断数据，其中包括监控数据、配置信息等。

### 使用场景：

以下场景适用于使用 Clinic Diag 工具采集诊断数据：

- 当集群出现问题，要咨询 PingCAP 技术支持时，需要提供集群诊断数据，协助技术支持人员定位问题。
- 保留集群诊断数据，进行后期分析。

> **注意：**
>
> 对于使用 TiDB Operator 部署的集群，暂不支持收集日志、配置文件、系统硬件信息等诊断数据。

### 第 1 步：确定需要采集的数据

如需查看 Clinic Diag 支持采集的数据详细列表，请参阅 [Clinic 数据采集说明 - Operator 环境](clinic/clinic-data-instruction-for-operator.md)。建议采集完整的监控数据、配置信息等数据，以便提升诊断效率。

### 第 2 步：采集数据

Clinic Diag 工具的各项操作均会通过 API 完成。

- 如需查看完整的 API 定义文档，可访问节点 `http://${host}:${port}/api/v1`。

- 如需查看节点 IP，可使用以下命令：

    {{< copyable "shell-regular" >}}

    ```bash
    kubectl get node | grep node
    ```

- 如需查看 `diag-collector service` 的端口号，可使用以下命令：

    {{< copyable "shell-regular" >}}

    ```bash
    kubectl get service -n tidb-admin
    NAME                 TYPE           CLUSTER-IP           EXTERNAL-IP   PORT(S)              AGE
    diag-collector   NodePort   10.111.143.227   <none>            4917:31917/TCP   18m
    ```

    - 从 Kubernetes 集群外访问该 Service 的端口为 `31917`。
    - 该 Service 类型为 NodePort。你可以通过 Kubernetes 集群中任一宿主机的 IP 地址 `${host}` 和端口号 `${port}` 访问该服务。

#### 1. 发起采集数据请求

通过 API 请求发起一次数据采集任务：

{{< copyable "shell-regular" >}}

```bash
curl -s http://${host}:${port}/api/v1/collectors -X POST -d '{"clusterName": "${cluster-name}","namespace": "${cluster-namespace}","from": "2022-02-08 12:00 +0800","to": "2022-02-08 18:00 +0800"}'
```

API 调用参数说明：

- `clusterName`：TiDB 集群名称
- `namespace`：TiDB 集群所在的 `namespace 名称`（不是 TiDB Operator 所在的 `namespace`）
- `from` 和 `to`：分别为采集的起止时间。`+0800` 代表时区，支持的时间格式如下：

 {{< copyable "shell-regular" >}}

  ```bash
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

  {{< copyable "shell-regular" >}}

  ```bash
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
- `status` 为此任务的当前状态，`accepted` 代表采集任务进入队列。

> **注意：**
>
> 返回命令结果只代表数据采集任务已经开始，并不表示采集已完成。要了解采集是否全部完成，需要通过下一步操作来查看采集任务的状态。

#### 2. 查看采集数据任务状态

通过 API 请求，获取采集任务的状态：

{{< copyable "shell-regular" >}}

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
    
{{< copyable "shell-regular" >}}

```bash
curl -s http://${host}:${port}/api/v1/data/${id}
{
        "clusterName": "${cluster-namespace}/${cluster-name}",
        "date": "2021-12-10T10:10:54Z",
        "id": "fMcXDZ4hNzs",
        "size": 1788980746
}
```

通过本命令，**只能**查看数据集的文件包大小，不能查看具体数据。如需查看数据内容，请参阅[可选操作：本地查看数据](/clinic-user-guide-for-operator.md#可选操作本地查看数据)。

### 第 3 步：上传数据集

把诊断数据提供给 PingCAP 技术支持人员时，需要将数据上传到 Clinic Server，然后将其数据链接发送给技术支持人员。Clinic Server 为 Clinic 诊断服务的云服务，可提供更安全的诊断数据存储和共享。

#### 1. 发起上传任务

通过 API 请求打包并上传收集完成的数据集：

 {{< copyable "shell-regular" >}}

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

{{< copyable "shell-regular" >}}

```bash
curl -s http://${host}:${port}/api/v1/data/${id}/upload
{
        "date": "2021-12-10T10:23:36Z",
        "id": "fMcXDZ4hNzs",
        "result": "\"https://clinic.pingcap.com:4433/diag/files?uuid=ac6083f81cddf15f-34e3b09da42f74ec-ec4177dce5f3fc70\"",
        "status": "finished"
}
```

如果状态变为 `finished`，则表示打包与上传均已完成。此时，`result` 表示 Clinic Server 查看此数据集的链接，即需要发给 PingCAP 技术支持人员的数据访问链接。目前 Clinic Server 的数据访问链接只对 PingCAP 技术支持人员开放，上传数据的外部用户暂时无法打开该链接。

### 可选操作：本地查看数据

采集完成的数据会保存在 Pod 的 `/diag-${id}` 目录中，可以通过以下方法进入 Pod 查看此数据：

#### 1. 获取 `diag-collector-pod-name`

{{< copyable "shell-regular" >}}

```bash
kubectl get pod --all-namespaces  | grep diag
tidb-admin      diag-collector-69bf78478c-nvt47               1/1     Running            0          19h
```

其中，Diag Pod 的名称为 `diag-collector-69bf78478c-nvt47`，其所在的 `namespace` 为 `tidb-admin`。

#### 2. 进入 Pod 并查看数据

{{< copyable "shell-regular" >}}

```bash
kubectl exec -n ${namespace} ${diag-collector-pod-name}  -it -- sh
/ # cd diag-${id}
```

其中，`${namespace}` 需要替换为 TiDB Operator 所在的 `namespace` 名称（通常为 `tidb-admin`）。

## 使用 Clinic Diag 工具快速诊断集群

Clinic 诊断服务支持对集群的健康状态进行快速地诊断，主要支持检查配置项内容，快速发现不合理的配置项。

### 使用步骤

本节详细介绍通过 Clinic 诊断服务快速诊断使用 TiDB Operator 部署的集群的具体方法。

第 1 步：采集数据

有关采集数据具体方法，可参考[使用 Clinic Diag 工具采集诊断数据](#第2步采集数据)。

第 2 步：快速诊断

通过 API 请求，在本地对集群进行快速诊断：

{{< copyable "shell-regular" >}}

```bash
curl -s http://${host}:${port}/api/v1/data/${id}/check -XPOST -d '{"types": ["config"]}'
```

其中，`id` 为采集数据任务的 ID 编号，在上述例子中为 `fMcXDZ4hNzs`。

请求结果中会列出已发现的配置风险内容和建议配置的知识库链接，具体示例如下：

{{< copyable "shell-regular" >}}

```bash
stdout:
# Check Result Report
basic 2022-02-07T12:00:00+08:00

## 1. Cluster Information
- Cluster ID: 7039963340562527412
- Cluster Name: basic
- Cluster Version: v5.4.0

## 2. Sample Information
- Sample ID: fPrz0RnDxRn
- Sampling Date: 2022-02-07T12:00:00+08:00
- Sample Content:: [monitor config]

## 3. Main results and abnormalities
In this inspection, 21 rules were executed.
The results of **3** rules were abnormal and needed to be further discussed with support team.
The following is the details of the abnormalities.

### Configuration Summary
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

在上述示例中，
    - 第一部分为诊断集群名称等基础信息。
    - 第二部分为断数据来源信息。
    - 第三部分展示诊断结果信息，包括发现的可能的配置问题。对于每条发现的配置问题，都提供知识库链接，以便查看详细的配置建议。
    - 最后一行为诊断结果文档的保存路径。

## 常见问题

1. 如果数据上传失败了，可以重新上传吗？

    数据上传支持断点上传，如果失败了，可以直接再次上传。

2. 数据上传后，用户无法打开返回的数据访问链接，怎么办？

    Clinic 诊断服务目前在 Beta 试用阶段，数据访问链接未对外部用户开放，只有经授权的 PingCAP 内部技术支持人员能打开链接并查看数据。

3. 上传到 Clinic Server 的数据后会保存多久？

    在对应的技术支持 Case 关闭后，PingCAP 会在 90 天内对相关数据进行永久删除或匿名化处理。
