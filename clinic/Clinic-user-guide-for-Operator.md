---
title: Operator 环境下的 Clinic 操作手册
summary: 在 Operator 部署的集群上如何使用 Clinic 工具进行数据采集和快速检查
---

# Operator 环境下的 Clinic 操作手册

> **注意：**
>
> 本文档只针对 Operator 部署的集群。Clinic 工具暂时不支持开启了 TLS 加密的集群和 Ansible 部署的集群。

在 Operator 部署的集群中， Clinic Diag 数据采集工具需要部署为一个独立的 pod。本文介绍如何通过 kubectl 命令创建并部署 Diag pod ，然后通过 API 调用继续数据采集和快速检查。

## 工具安装
### manifest 说明
使用下面 的 yaml 文件为 manifest 模板，按照后续的说明修改其中的关键参数为实际值。manifest 模版包括以下三个文件：
- diag.yaml
- rbac.yaml
- cert.yaml

在 diag.yaml 中, 需要将文件中的用户名和密码配置修改为真实的用户名和密码。目前 Clinic 在 Beta 受邀测试使用阶段，请联系与您对接的 PingCAP 技术人员或者联系 clinic-trail@pingcap.com 获取试用账号。

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

其中：
- CLINIC_USERNAME 为上传所需的用户名。
- CLINIC_PASSWORD 为上传所需的密码。
- 模板中使用的镜像地址为 https://drive.google.com/file/d/1sNRQDFhKgi_Gl6wPt7dHbQLuQXbd03YW/view?usp=sharing 。


在 rbac.yaml 中，需要将 ${namespace} 占位符修改为部署 TiDB Operator 所在的 namespace 名称（通常为 tidb-admin）
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

对于 cert.yaml ，默认无需修改。如需更换上传前对压缩包加密所使用的证书，可编辑 cert.yaml 替换证书内容。

### 部署 diag pod

编辑修改 manifest 文件完成后，使用 kubectl 命令将其应用到 Kubernetes 集群中以实际创建 diag pod：

{{< copyable "shell-regular" >}}

```bash
kubectl apply -n ${namespace} -f manifest
```
- 其中 ${namespace} 替换为 TiDB Operator 所在的 namespace 名称（通常为 tidb-admin, 下同）

### 查看 diag pod 的运行状态
使用以下命令查看名为 diag-collector-xxx 的 pod, 待其状态变为 Running 后进行下一步操作。
{{< copyable "shell-regular" >}}

```bash
kubectl get pod --all-namespaces | grep diag
tidb-admin   diag-collector-69bf78478c-d24sn        1/1   Running      0     2m16s
```

- 如果状态一直不能变成 running ，可查看该 Pod 日志确认是否有报错。



## 使用概述
Clinic 工具主要用于以下两个场景，方便用户快速获取诊断数据和做基础集群诊断：
- [使用 Clinic diag 工具采集诊断数据](/clinic-uyser-guide-for-operator.md#使用-clinic-diag-工具采集诊断数据)
- [使用 Clinic diag 工具快速诊断集群](/clinic-uyser-guide-for-operator.md#使用-clinic-diag-工具快速诊断集群)

## 使用 Clinic diag 工具采集诊断数据

Clinic 提供 TiDB 集群诊断数据快速抓取的方法，可以抓取监控数据、配置信息等。适于在以下场景中使用：

- 遇到问题咨询 PingCAP 技术支持，需要提供诊断数据协助定位问题。
- 保留诊断数据做后期分析。

> **注意：**
>
> 对于 Operator 集群，暂不支持收集日志、配置文件、系统硬件信息等诊断数据。

### 第一步：确定需要采集的数据
Clinic 支持采集的详细数据列表在[Clinic 数据采集说明 - Operator 环境]()，建议收集完整的监控数据、配置信息等数据，有助于提升后续诊断效率。  

### 第二步：采集数据

#### API 调用说明
Clinic Diag 的各项操作均通过 API 完成，访问节点 http://${host}:${port}/api/v1 可查看完整的 API 定义文档。

可通过以下命令查看节点 IP ：
{{< copyable "shell-regular" >}}

```bash
kubectl get node | grep node
```

通过以下命令查看 diag-collector service 的端口号：
{{< copyable "shell-regular" >}}

```bash
kubectl get service -n tidb-admin
NAME                 TYPE           CLUSTER-IP           EXTERNAL-IP   PORT(S)              AGE
diag-collector   NodePort   10.111.143.227   <none>            4917:31917/TCP   18m
```
- 在上述例子中，从 Kubernetes 集群外访问该 Service 的端口为 31917.
- 该 Service 类型为 NodePort, 可通过 Kubernetes 集群中任一宿主机的 IP 地址 ${host} 和端口号 ${port} 进行访问。

#### 发起采集数据请求
通过 API 请求发起一次数据采集任务：
{{< copyable "shell-regular" >}}

```bash
curl -s http://${host}:${port}/api/v1/collectors -X POST -d '{"clusterName": "${cluster-name}","namespace": "${cluster-namespace}","from": "2021-12-08 12:00 +0800","to": "2021-12-08 18:00 +0800"}'
```
API 调用参数说明：
- clusterName 为 TiDB 集群名称
- namespace 为 TiDB 集群所在的 namespace 名称（不是 TiDB Operator 所在的 namespace）
- from 和 to 分别为采集的起止时间，“+0800” 代表时区。


请求响应：
{{< copyable "shell-regular" >}}

```bash
        "clusterName": "${cluster-namespace}/${cluster-name}",
        "collectors": [
            "config",
            "monitor"
        ],
        "date": "2021-12-10T10:10:54Z",
        "from": "2021-12-08 12:00 +0800",
        "id": "fMcXDZ4hNzs",
        "status": "accepted",
        "to": "2021-12-08 18:00 +0800"

```
API 返回信息说明：
- date 为采集任务发起的时间。
- id 为此任务的 ID 编号，在之后的操作中都将使用此 ID 来唯一定位到此次任务。
- status 为此任务的当前状态，accepted 代表采集任务进入队列。

> **注意：**
>
> 收到响应只代表数据采集任务开始，并不是已经采集完成，需要通过下一章节的获取采集状态操作了解是否采集完成。

#### 查看采集数据任务状态
通过 API 请求获取采集任务的状态：

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

说明：
- 请求中的 id 为任务的 ID 编号，在上述例子中为 fMcXDZ4hNzs。
- 响应格式与发起采集任务的接口响应格式相同。
- 待该任务的状态变为 “finished” 即表示采集已完成。

#### 查看采集的数据集信息

在采集任务完成后，可以通过 API 请求获取数据集的采集时间和数据大小信息：
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

说明：本接口只能查看数据集的文件包大小，不能查看具体数据，如需查看数据内容，请参考[可选操作：本地查看数据](/clinic-uyser-guide-for-operator.md#可选操作：本地查看数据)。

### 第三步：上传数据集
用户需要将诊断数据提供给 PingCAP 技术支持人员时，需要将数据上传到 Clinic Server ，然后将数据链接发送给技术支持人员。 Clinic Server 提供更安全的诊断数据存储和共享。

#### 发起上传任务
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
说明：收到响应只代表数据上传任务开始，并不是已经上传完成，需要通过后续介绍的查看上传任务状态接口了解上传任务是否完成。

#### 查看上传任务状态
通过 API 请求查看上传任务的状态：
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
说明： 
- 待状态变为 “finished” 后表示打包与上传均已完成，此时 “result” 中的内容即为 Clinic Server 查看此数据集的链接。
- 请将 result 中的数据访问链接发给 PingCAP 技术支持人员。目前 Clinic Server 的数据访问链接只对 PingCAP 技术支持人员开放，上传数据的外部用户暂时无法打开该链接。
  
### 可选操作：本地查看数据

采集完成的数据会保存在 pod 的 /diag-${id} 目录中，可以通过以下方法进入 pod 进行查看：

（1）获取 diag-collector-pod-name

{{< copyable "shell-regular" >}}

```bash
kubectl get pod -n  ${namespace}   | grep diag
```

（2）进入 Pod
{{< copyable "shell-regular" >}}

```bash
kubectl exec -n ${namespace} ${diag-collector-pod-name}  -it -- sh
```
其中
- ${namespace} 替换为 TiDB Operator 所在的 namespace 名称（通常为 tidb-admin, 下同）

（3）查看数据
{{< copyable "shell-regular" >}}

```bash
 ~ cd /diag-${id}
```

# 使用 Clinic 工具快速诊断集群

Clinic 工具支持对集群的健康状态进行快速的诊断，目前版本主要支持配置项内容检查，快速发现不合理的配置项。

### 使用步骤
第一步：采集数据
采集数据方法可参考[使用 Clinic diag 工具采集诊断数据](/clinic-uyser-guide-for-operator.md#使用-clinic-diag-工具采集诊断数据)内容，进行数据采集。

第二步：快速诊断

通过 API 请求在本地进行快速诊断：

{{< copyable "shell-regular" >}}

```bash
curl -s http://${host}:${port}/api/v1/data/${id}/check -XPOST -d '{"types": ["config"]}'
```
其中：
- 请求中的 id 为采集数据任务的 ID 编号，在上述例子中为 fMcXDZ4hNzs。