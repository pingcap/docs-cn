---
title: PingCAP Clinic 快速上手
summary: 说明在 TiUP 部署的集群中，如何使用 Clinic 收集数据并上传到 Clinic Server 进行诊断。
---
-
# PingCAP Clinic 快速上手

本文介绍如何快速使用 PingCAP Clinic 诊断服务（以下简称为 PingCAP Clinic）进行诊断数据的收集、上传和分析。

> **注意：**
>
> - 本指南中的数据采集和上传的方式仅适用于 TiUP 部署的集群。
> - 通过 PingCAP Clinic 在 TiDB 集群中采集并上传到 Clinic Server 的数据**仅**用于诊断和分析集群问题。

## 注册并登录 Clinic Server

用户可以通过 TiDB 社区帐号登录 PingCAP Clinic 服务，进入[ Clinic 登录页面](https://clinic.pingcap.com/clinic/#/login)，选择 “Sign in with AskTUG” ，进入社区帐号登录界面。若您还没有 TiDB 社区帐号，可以在登录界面进行注册。

## 创建组织并获取上传 Token

用户第一次登录成功后，需要创建组织。根据页面提示输入组织名称，即可创建。创建成功后进入组织页面，用户可以在组织界面上直接上传 Diag 客户端采集的诊断数据，也可以获取 Token 后通过 Diag 客户端的命令行或接口上传。

### 获取客户端上传 Token （推荐方式）
点击页面上的上传图标，选择“Get Access Token For Diag Tool” ，在弹出窗口中复制并保存 Token 信息。

> **注意：**
>
> - Token 用于 Diag 客户端上传数据时进行用户认证，保证数据上传到用户创建的组织下，保证数据的安全隔离。
> - Token 内容只在创建时展示，如果用户丢失 Token 信息，可以删除老 Token，重新创建。

### 网页直接上传诊断数据
点击页面上的上传图标，选择“Diag Package (.diag) Upload” ，选择本地的 Diag 数据文件上传。

> **注意：**
>
> - 只支持上传客户端 Diag v0.7.0 及以上版本采集及使用 Package 命令打包后的文件。
> - 文件大小不能超过 10GB。

## 采集并上传数据 

- 适用场景：远程定位集群问题，当集群出现问题，需要远程咨询 PingCAP 技术支持时，你可以先使用 Diag 采集诊断数据，然后将其数据上传到 Clinic Server，最后把数据链接提供给技术支持人员，协助远程定位集群问题。

1. 安装 Diag 。
    如果你的中控机上已经安装了 TiUP，可以使用以下命令一键安装 Diag：

    {{< copyable "shell-regular" >}}

    ```bash
    tiup install diag
    ```

    若已安装了 Diag，你可以通过以下命令，将本地的 Diag 一键升级至最新版本：

    {{< copyable "shell-regular" >}}

    ```bash
    tiup update diag
    ```

    设置 Diag 的上传 Token

    {{< copyable "shell-regular" >}}

    ```bash
    tiup diag config --token=${token-value}
    ```

2. 运行 Diag 采集诊断数据。

    例如，如需采集从当前时间的 4 小时前到 2 小时前的诊断数据，可以运行以下命令：

    {{< copyable "shell-regular" >}}

    ```bash
    tiup diag collect ${cluster-name} -f="-4h" -t="-2h"
    ```
    > **注意：**
    >
    > 更多数据采集参数的说明可以参看[使用 TiDB Clinic](/clinic/clinic-user-guide-for-tiup.md)。

3. 上传数据到 Clinic Server

    如果你的集群所在的网络可以访问互联网，你可以直接通过以下命令上传在上一步中收集的数据包文件夹：

    {{< copyable "shell-regular" >}}

    ```bash
    tiup diag upload ${filepath}
    ```

    输出结果示例如下：

    {{< copyable "shell-regular" >}}

    ```bash
    [root@Copy-of-VM-EE-CentOS76-v1 qiaodan]# tiup diag upload /home/qiaodan/diag-fNTnz5MGhr6
    Starting component `diag`: /root/.tiup/components/diag/v0.5.1/diag upload /home/qiaodan/diag-fNTnz5MGhr6
    Completed!
    Download URL: "https://clinic.pingcap.com/clinic/#/orgs/75/clusters/7055188676317281573 "
    ```

    完成上传后，你可以打开 `Download URL` 中的数据访问链接进行数据查看，也可以将链接发给与你对接的 PingCAP 技术支持人员，后者协助远程定位集群问题。

    > **注意：**
    >
    > 如果你所在的集群无法访问互联网，需要通过先打包后上传的方式进行上传，相关说明可以参看[使用 TiDB Clinic](/clinic/clinic-user-guide-for-tiup.md)。

## 通过 Clinic Server 查看并分析诊断数据

诊断数据上传后，你可以在 Clinic Server 上直接查看到以下诊断数据内容：
- 集群名称
- 集群拓扑信息
- 诊断数据包中的日志内容
- 基于诊断数据包中的 metrics 信息重建的 Grafana Dashboard 