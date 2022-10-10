---
title: PingCAP Clinic 快速上手指南
summary: 了解如何使用 PingCAP Clinic 诊断服务快速采集、上传、查看集群诊断数据。
---

# PingCAP Clinic 快速上手指南

本指南介绍如何使用 PingCAP Clinic 诊断服务（以下简称为 PingCAP Clinic）快速采集、上传、查看集群诊断数据。

PingCAP Clinic 由 Diag 诊断客户端（以下简称为 Diag）和 Clinic Server 云服务平台（以下简称为 Clinic Server）组成。关于 Diag 和 Clinic Server 的详细介绍，请参考 [PingCAP Clinic 诊断服务简介](/clinic/clinic-introduction.md)。

## 使用场景

- 当集群出现问题，需要远程咨询 PingCAP 技术支持时，为了提高定位和解决问题的效率，你可以使用 Diag 采集诊断数据，上传数据到 Clinic Server 并获取数据链接，然后将数据链接提供给技术支持人员。
- 在集群正常运行时，需要检查集群的运行状态，你可以使用 Diag 采集诊断数据，上传数据到 Clinic Server 并查看 Health Report 的结果。

> **注意：**
>
> - 本文档提供的采集和上传数据的方式**仅**适用于使用 [TiUP 部署](/production-deployment-using-tiup.md)的集群。如需查看适用于使用 Operator 部署的集群，请参阅 [在 TiDB Operator 部署环境使用 PingCAP Clinic](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/clinic-user-guide)。
> - 通过 PingCAP Clinic 采集和上传的数据**仅**用于定位和诊断集群问题。

## 准备工作

在开始体验 PingCAP Clinic 功能之前，你需要先安装数据采集组件 Diag 并准备数据上传环境。

1. 在安装了 TiUP 的中控机上，一键安装 Diag：

    ```bash
    tiup install diag
    ```

2. 登录 Clinic Server。

    <SimpleTab groupId="clinicServer">
    <div label="Clinic Server 中国区" value="clinic-cn">

    登录 [Clinic Server 中国区](https://clinic.pingcap.com.cn)，选择 **Sign in with AskTUG** 进入 TiDB 社区 AskTUG 的登录界面。如果你尚未注册 AskTUG 帐号，可以在该界面进行注册。

    </div>

    <div label="Clinic Server 美国区" value="clinic-us">

    登录 [Clinic Server 美国区](https://clinic.pingcap.com)，选择 **Sign in with TiDB Account** 进入 TiDB Cloud Account 的登录界面。如果你尚未注册 TiDB Cloud 帐号，可以在该界面进行注册。

    > **注意：**
    >
    > Clinic Server 只是通过 TiDB Cloud 账号进行 SSO 登录，并不要求用户必须使用 TiDB Cloud 服务。

    </div>
    </SimpleTab>

3. 在 Clinic Server 中，依据页面提示创建组织 (Organization)。组织是一系列 TiDB 集群的集合。你可以在所创建的组织上上传诊断数据。

4. 获取用于上传数据的 Access Token（以下简称为 Token）。使用 Diag 上传数据时，你需要通过 Token 进行用户认证，以保证数据上传到组织后被安全地隔离。获取一个 Token 后，你可以重复使用该 Token，具体获取方法如下：

    点击 Cluster 页面右下角的图标，选择 **Get Access Token For Diag Tool**，在弹出窗口中点击 **+** 符号获取 Token 后，复制并保存 Token 信息。

    ![Token 示例](/media/clinic-get-token.png)

    > **注意：**
    >
    > - 为了确保数据的安全性，TiDB 只在创建 Token 时显示 Token 信息。如果丢失了 Token 信息，你可以删除旧 Token 后重新创建。
    > - 该 Token 只用于数据上传，访问数据时不需要使用 Token。

5. 在 Diag 中设置 Token 和 `region`：

    - 设置 `clinic.token`：

        ```bash
        tiup diag config clinic.token ${token-value}
        ```

    - 设置 `clinic.region`：

        `region` 决定数据打包时使用的加密证书和上传的目标 Clinic Server 地址。参考以下命令，根据你的 Clinic Server 在 Diag 中设置 `clinic.region`。

        > **注意：**
        >
        > - Diag v0.9.0 及以后的版本支持自行设置 `region`。
        > - 对于 Diag v0.9.0 之前的版本，数据默认上传到中国区的 Clinic Server。
        > - 如果你的 Diag 是 v0.9.0 之前的版本，你可以通过 `tiup update diag` 命令将其升级至最新版后设置 `region`。

        <SimpleTab groupId="clinicServer">
        <div label="Clinic Server 中国区" value="clinic-cn">

        对于 Clinic Server 中国区，参考以下命令，将 `region` 设置为 `CN`：

        ```bash
        tiup diag config clinic.region CN
        ```

        </div>

        <div label="Clinic Server 美国区" value="clinic-us">

        对于 Clinic Server 美国区，参考以下命令，将 `region` 设置为 `US`：

        ```bash
        tiup diag config clinic.region US
        ```

        </div>
        </SimpleTab>

6. 开启日志脱敏配置（可选步骤）。

    TiDB 在提供详细的日志信息时可能会打印数据库的敏感信息（例如用户数据）。如果希望本地日志及上传到 Clinic Server 的日志中不带有敏感信息，你可以开启日志脱敏配置。具体操作请参考[日志脱敏](/log-redaction.md#tidb-组件日志脱敏)。

## 体验步骤

1. 运行 Diag，采集诊断数据。

    例如，如需采集从当前时间的 4 小时前到 2 小时前的诊断数据，可以运行以下命令：

    ```bash
    tiup diag collect ${cluster-name} -f="-4h" -t="-2h"
    ```

    运行 Diag 数据采集命令后，Diag 不会立即开始采集数据，而会在输出中提供预估数据量大小和数据存储路径，并询问你是否进行数据收集。如果确认要开始采集数据，请输入 `Y`。

    采集完成后，Diag 会提示采集数据所在的文件夹路径。

2. 将采集到的数据上传到 Clinic Server。

    > **注意：**
    >
    > 上传数据（数据包文件夹打包压缩后的文件）的大小不得超过 3 GB，否则会导致上传失败。

    - 如果你的集群所在的网络可以访问互联网，你可以通过以下命令上传已采集的数据包文件夹：

        ```bash
        tiup diag upload ${filepath}
        ```

        完成上传后，Diag 会提示诊断数据的下载路径 `Download URL`。

        > **注意：**
        >
        > 使用该方式进行上传时，你需要使用 Diag v0.9.0 及以上版本。Diag 会在运行时提示版本信息。如果你早期安装过 v0.9.0 之前版本的 Diag，你可以通过 `tiup update diag` 命令将其一键升级至最新版。

    - 如果你所在的集群无法访问互联网，需要先打包数据后进行上传。具体步骤，请参阅[上传方式 2：打包后上传](/clinic/clinic-user-guide-for-tiup.md#方式-2打包后上传)。

3. 完成数据上传后，通过上传输出结果中的 `Download URL` 获取诊断数据的链接。

    诊断数据默认包括集群名称、集群拓扑信息、诊断数据包中的日志内容和基于诊断数据包中的 metrics 信息重建的 Grafana Dashboard 信息。

    你可以通过这些数据自己查找并诊断集群问题，或者，你也可以将链接发给与你对接的 PingCAP 技术支持人员，以协助远程定位集群问题。

4. 查看 Health Report 结果。

    数据上传到 Clinic Server 后，后台将自动处理数据，在大概 5～15 分钟后生成 Health Report。用户可以打开诊断数据链接，点击下方的“Health Report”入口查看报告内容。

## 探索更多

- 在 TiUP 部署环境使用 PingCAP Clinic

    - [PingCAP Clinic 诊断服务简介](/clinic/clinic-introduction.md)
    - [使用 PingCAP Clinic 诊断集群](/clinic/clinic-user-guide-for-tiup.md)
    - [使用 PingCAP Clinic 生成诊断报告](/clinic/clinic-report.md)
    - [PingCAP Clinic 数据采集说明](/clinic/clinic-data-instruction-for-tiup.md)

- 在 TiDB Operator 部署环境使用 PingCAP Clinic

    - [使用 PingCAP Clinic](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/clinic-user-guide)
    - [PingCAP Clinic 数据采集说明](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/clinic-data-instruction)