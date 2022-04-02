---
title: PingCAP Clinic 快速上手
summary: 了解如何使用 PingCAP Clinic 诊断服务快速采集、上传、查看集群诊断数据。
---

# PingCAP Clinic 快速上手指南

本指南介绍如何使用 PingCAP Clinic 诊断服务（以下简称为 PingCAP Clinic）快速采集、上传、查看集群诊断数据。

PingCAP Clinic 由 Diag 客户端（以下简称为 Diag）和 [Clinic Server 云服务平台](https://clinic.pingcap.com.cn)（以下简称为 Clinic Server）组成。关于 Diag 和 Clinic Server 的详细介绍，请参考 [PingCAP Clinic 诊断服务简介](/clinic/clinic-introduction.md)。

当集群出现问题，需要远程咨询 PingCAP 技术支持时，为了提高定位和解决问题的效率，你可以使用 Diag 采集诊断数据，上传数据到 Clinic Server 并获取数据链接，然后将数据链接提供给技术支持人员。

PingCAP Clinic 目前处于 Technical Preview 阶段。

> **注意：**
>
> - 本指南提供的采集和上传数据的方式仅适用于使用 [TiUP 部署](/production-deployment-using-tiup.md)的集群。
> - 通过 PingCAP Clinic 采集和上传的数据**仅**用于定位和诊断集群问题。

## 准备工作

在开始体验 PingCAP Clinic 功能之前，你需要先安装数据采集组件 Diag 并准备数据上传环境。

1. 在安装了 TiUP 的中控机上，一键安装 Diag：

    {{< copyable "shell-regular" >}}

    ```bash
    tiup install diag
    ```

2. 登录 [Clinic Server](https://clinic.pingcap.com.cn)，选择 **Sign in with AskTUG** 进入 TiDB 社区 AskTUG 的登录界面。如果你尚未注册 AskTUG 帐号，可以在该界面进行注册。

3. 在 Clinic Server 中，依据页面提示创建组织 (Organization)。组织是一系列 TiDB 集群的集合。你可以在所创建的组织上上传诊断数据。

4. 获取用于上传数据的 Access Token（以下简称为 Token）。使用 Diag 上传数据时，你需要通过 Token 进行用户认证，以保证数据上传到组织后被安全地隔离。获取一个 Token 后，你可以重复使用该 Token，具体获取方法如下：

    点击 Cluster 页面右下角的图标，选择 **Get Access Token For Diag Tool**，在弹出窗口中点击 **+** 符号获取 Token 后，复制并保存 Token 信息。

    ![Token 示例](/media/clinic-get-token.png)

    > **注意：**
    >
    > - 为了确保数据的安全性，TiDB 只在创建 Token 时显示 Token 信息。如果丢失了 Token 信息，你可以删除旧 Token 后重新创建。
    > - 该 Token 只用于数据上传，访问数据时不需要使用 Token。

5. 在 Diag 中设置 Token：

    {{< copyable "shell-regular" >}}

    ```bash
    tiup diag config clinic.token ${token-value}
    ```

## 体验步骤

1. 运行 Diag，采集诊断数据。

    例如，如需采集从当前时间的 4 小时前到 2 小时前的诊断数据，可以运行以下命令：

    {{< copyable "shell-regular" >}}

    ```bash
    tiup diag collect ${cluster-name} -f="-4h" -t="-2h"
    ```

    运行 Diag 数据采集命令后，Diag 不会立即开始采集数据，而会在输出中提供预估数据量大小和数据存储路径，并询问你是否进行数据收集。如果确认要开始采集数据，请输入 `Y`。

    采集完成后，Diag 会提示采集数据所在的文件夹路径。

2. 将采集到的数据上传到 Clinic Server。

    > **注意：**
    >
    > 上传数据（数据包文件夹）的大小不得超过 10 GB，否则会导致上传失败。

    - 如果你的集群所在的网络可以访问互联网，你可以通过以下命令上传已采集的数据包文件夹：

        {{< copyable "shell-regular" >}}

        ```bash
        tiup diag upload ${filepath}
        ```

        输出结果示例如下：

        {{< copyable "shell-regular" >}}

        ```bash
        Completed!
        Download URL: "https://clinic.pingcap.com/clinic/#/orgs/75/clusters/7055188676317281573 "
        ```

        > **注意：**
        >
        > 使用该方式进行上传时，你需要使用 Diag v0.7.0 及以上版本。Diag 会在运行时提示版本信息。如果你早期安装过 v0.7.0 之前版本的 Diag，你可以通过 `tiup update diag` 命令将其一键升级至最新版。

    - 如果你所在的集群无法访问互联网，需要先打包数据后进行上传。具体步骤，请参阅[上传方式 2：打包后上传](/clinic/clinic-user-guide-for-tiup.md#方式-2打包后上传)。

3. 完成数据上传后，通过上传输出结果中的 `Download URL` 获取诊断数据的链接。

    诊断数据默认包括集群名称、集群拓扑信息、诊断数据包中的日志内容和基于诊断数据包中的 metrics 信息重建的 Grafana Dashboard 信息。

    你可以通过这些数据自己查找并诊断集群问题，或者，你也可以将链接发给与你对接的 PingCAP 技术支持人员，以协助远程定位集群问题。

## 探索更多

- [PingCAP Clinic 诊断服务简介](/clinic/clinic-introduction.md)
- [使用 PingCAP Clinic](/clinic/clinic-user-guide-for-tiup.md)
- [PingCAP Clinic 数据采集说明](/clinic/clinic-data-instruction-for-tiup.md)