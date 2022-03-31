---
title: PingCAP Clinic 快速上手
summary: 本文介绍如何快速上手体验 PingCAP Clinic 诊断服务，包括在使用 TiUP 部署的集群上通过 Diag 客户端采集数据的方法、使用 Diag 客户端将采集到的数据上传到 Clinic Server 云平台的方法，以及在 Clinic Server 上查看采集到的数据的方法。
---

# PingCAP Clinic 快速上手指南

本指南介绍在使用 TiUP 部署的集群上如何快速上手体验 PingCAP Clinic 诊断服务（以下简称为 PingCAP Clinic），包括采集、上传和查看诊断数据的方法。

当集群出现问题，需要远程咨询 PingCAP 技术支持时，为了协助技术人员远程定位集群问题，以提高定位问题的效率，你可以先使用 Diag 客户端（以下简称为 Diag）采集诊断数据，然后使用 Diag 将该数据上传到 [Clinic Server 云服务平台]((https://clinic.pingcap.com.cn))（以下简称为 Clinic Server）并获取数据链接，最后把其数据链接提供给技术支持人员。有关 Diag 和 Clinic Server 的介绍可以参考 [PingCAP Clinic 组件](/clinic/clinic-introduction.md)。

PingCAP Clinic 诊断服务目前处于 Technical Preview 阶段。

> **注意：**
>
> - 本指南提供的采集和上传数据的方式仅适用于使用 TiUP 部署的集群。
> - 通过 PingCAP Clinic 采集和上传的数据**仅**用于定位和诊断集群问题。

## 准备工作

在开始体验 PingCAP Clinic 功能之前，你需要先安装 Diag 并准备数据上传环境。

### 第 1 步：安装数据采集组件

为采集诊断数据，你需要使用 Diag。

- 如果你的中控机上已经安装了 TiUP，可以使用以下命令一键安装 Diag：

    {{< copyable "shell-regular" >}}

    ```bash
    tiup install diag
    ```

- 若已安装了 Diag，你可以通过以下命令，将本地的 Diag 一键升级至最新版本：

    {{< copyable "shell-regular" >}}

    ```bash
    tiup update diag
    ```

### 第 2 步：准备数据上传环境

1. 登录 Clinic Server。访问 [Clinic Server](https://clinic.pingcap.com.cn)（页面名为 PingCAP Clinic），选择 **Sign in with AskTUG** 进入 TiDB 社区帐号 AskTUG 的登录界面。如果你尚未注册 AskTUG 帐号，可以在该界面进行注册。

2. 创建组织 (form)。第一次成功登录到 Clinic Server 后，你需要创建组织。根据【XXX页面名称】上的提示输入组织名称即可创建组织。组织是一系列 TiDB 集群的集合。创建组织后，你可以在组织上上传集群的诊断数据。

3. 获取 Token。成功创建组织后，你获取用于上传数据的 Upload Token（以下简称为 Token）。使用 Diag 上传数据时，你需要通过 Token 进行用户认证，以保证数据上传到组织后被安全地隔离。获取一个 Token 后，你可以重复使用该 Token，具体获取方法如下：

    点击【XXX页面名称，比如，首页】页面【XXX 方向，比如右上侧】的上传图标，选择 "Get Access Token For Diag Tool"，在弹出窗口（如图）中复制并保存 Token 信息。

    ![Token 示例](/media/clinic-get-token.png)

    > **注意：**
    >
    > - 你只能在创建 Token 时看到 Token 信息。如果丢失了 Token 信息，你可以删除旧 Token 后重新创建。
    > - 该 Token 只用于数据上传，访问数据时不需要使用 Token。

4. 上传 Token。为使用已创建的 Token，你需要通过以下命令在 Diag 中设置 Token：

    {{< copyable "shell-regular" >}}

    ```bash
    tiup diag config clinic.token ${token-value}
    ```

## 体验步骤

1. 采集数据：运行 Diag

    例如，如需采集从当前时间的 4 小时前到 2 小时前的诊断数据，可以运行以下命令：

    {{< copyable "shell-regular" >}}

    ```bash
    tiup diag collect ${cluster-name} -f="-4h" -t="-2h"
    ```

    运行 Diag 数据采集命令后，Diag 不会立即开始采集数据，而会在输出中提供预估数据量大小和数据存储路径，并询问你是否进行数据收集。如果确认要开始采集数据，请输入 `Y`。

    采集完成后，Diag 会提示采集数据所在的文件夹路径。

2. 上传数据：将诊断数据上传到 Clinic Server

    - 如果你的集群所在的网络可以访问互联网，你可以直接通过以下命令上传已采集的数据包文件夹：

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

        > **注意：**
        >
        > - 使用该方式进行上传时，你需要使用 Diag v0.7.0 及以上版本。
        > - 数据包文件夹的大小不得超过 10 GB。

    - 如果你所在的集群无法访问互联网，需要先打包数据后进行上传。具体内容，请参阅[上传方式 2：打包后上传](/clinic/clinic-user-guide-for-tiup.md#方式-2打包后上传)。

3. 访问数据：打开数据链接。

    完成数据上传后，你可以打开命令返回结果中 `Download URL` 部分的数据访问链接。打开链接后，你可以查看已上传的诊断数据，具体内容包括集群名称、集群拓扑信息、诊断数据包中的日志内容和基于诊断数据包中的 metrics 信息重建的 Grafana Dashboard。

    你可以使用功能该数据自己查找并诊断集群问题，或者，你也可以将链接发给与你对接的 PingCAP 技术支持人员，以协助远程定位集群问题。

## 探索更多

- [PingCAP Clinic 诊断服务简介](/clinic/clinic-introduction.md)
- [使用 PingCAP Clinic](/clinic/clinic-user-guide-for-tiup.md)
- [PingCAP Clinic 数据采集说明](/clinic/clinic-data-instruction-for-tiup.md)