---
title: 使用 PingCAP Clinic
summary: 详细介绍在使用 TiUP 部署的集群上如何通过 PingCAP Clinic 诊断服务远程定位集群问题和本地快速检查集群状态。
---

# 使用 PingCAP Clinic

对于使用 TiUP 部署的 TiDB 集群和 DM 集群，PingCAP Clinic 诊断服务（以下简称为 PingCAP Clinic）可以通过 Diag 诊断客户端（以下简称为 Diag）与 [Clinic Server 云诊断平台](https://clinic.pingcap.com.cn)（以下简称为 Clinic Server）实现远程定位集群问题和本地快速检查集群状态。

目前，PingCAP Clinic 诊断服务处于 Technical Preview 阶段。

> **注意：**
>
> PingCAP Clinic 暂时**不支持**对使用 TiDB Ansible 部署的集群进行数据采集。

## 使用场景

- [远程定位集群问题](#远程定位集群问题)

    - 当集群出现问题，需要远程咨询 PingCAP 技术支持时，你可以先使用 Diag 采集诊断数据，然后将其数据上传到 Clinic Server，最后把数据链接提供给技术支持人员，协助远程定位集群问题。
    - 当集群出现问题，但无法马上进行问题分析时，你可以先使用 Diag 采集数据，并将其数据保存下来，用于自己后期进行问题分析。

- [本地快速检查集群状态](#本地快速检查集群状态)

    即使集群可以正常运行，也需要定期检查集群是否有潜在的稳定性风险。PingCAP Clinic 提供的本地快速诊断功能，用于检查集群潜在的健康风险。目前 PingCAP Clinic Technical Preview 版本主要对集群配置项提供合理性检查，用于发现不合理的配置，并提供修改建议。

## 准备工作

### 第 1 步：安装数据采集组件

为采集诊断数据，你需要安装 Diag。

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

> **注意：**
>
> - 对于离线集群，你需要离线部署 Diag 诊断客户端。具体方法，请参照[离线部署 TiUP 组件：方式 2](/production-deployment-using-tiup.md#离线部署)。
> - Diag 诊断客户端**仅**包含在 v6.0.0 及后续版本的 TiDB Server 离线镜像包中。

### 第 2 步：准备数据上传环境

1. 获取 Token：

    为上传采集到的数据，你需要在 Clinic Server 获取 Token 后，在 Diag 中设置 Token。上传数据时，你需要通过 Token 在 Diag 上进行进行用户认证，以保证数据上传的数据能够被安全地隔离。获取一个 Token 后，你可以重复使用该 Token，具体获取方法如下：

    登录 [Clinic Server](https://clinic.pingcap.com.cn)（页面名为 PingCAP Clinic），进入【XXX页面名称】页面【XXX 方向，比如右上侧】的上传图标后，选择 "Get Access Token For Diag Tool"，在弹出窗口（如图）中复制并保存 Token 信息。

    ![Token 示例](/media/clinic-get-token.png)

    > **注意：**
    >
    > - 登录 Clinic Server 页面时，你需要使用 TiDB 社区 AskTUG 的账号。如果你之前没有登录过该页面且为在 Clinic Server 中未设置过组织 (form)，请执行 [快速上手指南：准备数据上传环境](/clinic/quick-start-with-clinic.md#第-2-步-准备数据上传环境)中的相关步骤。
    > - 你**只能**在创建 Token 时看到 Token 信息。如果丢失了 Token 信息，你可以删除旧 Token 后重新创建。

2. 在 Diag 中设置 Token：

    {{< copyable "shell-regular" >}}

    ```bash
    tiup diag config clinic.token ${token-value}
    ```

## 远程定位集群问题

你可以使用 Diag 快速抓取 TiDB 集群和 DM 集群的诊断数据，其中包括监控数据、配置信息等。

### 第 1 步：确定需要采集的数据

如需查看 Diag 支持采集的数据的详细列表，请参阅 [PingCAP Clinic 数据采集说明](/clinic/clinic-data-instruction-for-tiup.md)。

建议收集监控数据、配置信息等全量诊断数据，有助于提升后续诊断效率。具体方法，请参考 [采集 TiDB 集群的数据](采集-TiDB-集群的数据]。

### 第 2 步：采集数据

你可以使用 Diag 采集使用 TiUP 部署的 TiDB 集群和 DM 集群的数据。

#### 采集 TiDB 集群的数据

1. 运行 Diag 数据采集命令。

    例如，如需采集从当前时间的 4 小时前到 2 小时前的诊断数据，可以运行以下命令：

    {{< copyable "shell-regular" >}}

    ```bash
    tiup diag collect ${cluster-name} -f="-4h" -t="-2h"
    ```

    采集参数说明：

    - `-f/--from`：指定采集时间的起始点。如果不指定该参数，默认起始点为当前时间的 2 小时前。如需修改时区，可使用 `-f="12:30 +0800"` 语法。如果没有在该参数中指定时区信息，如 `+0800`，则默认时区为 UTC。
    - `-t/--to`：指定采集时间的结束点。如果不指定该参数，默认结束点为当前时刻。如需修改时区，可使用 `-f="12:30 +0800"` 语法。如果没有在该参数中指定时区信息，如 `+0800`，则默认时区为 UTC。

    参数使用提示：

    除了指定采集时间，你还可以使用 Diag 指定更多参数。如需查看所有参数，请使用 `tiup diag collect -h` 命令。

    > **注意：**
    >
    > - Diag 默认**不收集**系统变量数据 (`db_vars`)。如需收集该数据，你需要额外提供开启了系统变量可读权限的数据库用户名和密码。
    > - Diag 默认**不收集**性能数据 (`perf`)和 debug 数据 (`debug`)。
    > - 如需收集全量诊断数据，可以使用命令 `tiup diag collect <cluster-name> --include="system,monitor,log,config,db_vars,perf,debug"`。

    - `-l`：传输文件时的带宽限制，单位为 Kbit/s, 默认值为 `100000`（即 scp 的 `-l` 参数）。
    - `-N/--node`：支持只收集指定节点的数据，格式为 `ip:port`。
    - `--include`：只收集特定类型的数据，可选值为 `system`，`monitor`，`log`，`config`，`db_vars`。如需同时列出多种类型的数据，你可以使用逗号 `,` 来分割不同的数据类型。
    - `--exclude`：不收集特定类型的数据，可选值为 `system`，`monitor`，`log`，`config`，`db_vars`。如需同时列出多种类型的数据，你可以使用逗号 `,` 来分割不同的数据类型。

    运行 Diag 数据采集命令后，Diag 不会立即开始采集数据，而会在输出中提供预估数据量大小和数据存储路径，并询问你是否进行数据收集。例如：

    {{< copyable "shell-regular" >}}

    ```bash
    Estimated size of data to collect:
    Host               Size       Target
    ----               ----       ------
    172.16.7.129:9090  43.57 MB   1775 metrics, compressed
    172.16.7.87        0 B        /tidb-deploy/tidb-4000/log/tidb_stderr.log
    ... ...
    172.16.7.179       325 B      /tidb-deploy/tikv-20160/conf/tikv.toml
    Total              2.01 GB    (inaccurate)
    These data will be stored in /home/qiaodan/diag-fNTnz5MGhr6
    Do you want to continue? [y/N]: (default=N)
    ```

2. 如果确认要开始采集数据，请输入 `Y`。

    采集数据需要一定的时间，具体所需时间与需要收集的数据量有关。例如，在测试环境中收集 1 GB 数据，大概需要 10 分钟。

    采集完成后，Diag 会提示采集数据所在的文件夹路径。例如：

    {{< copyable "shell-regular" >}}

    ```bash
    Collected data are stored in /home/qiaodan/diag-fNTnz5MGhr6
    ```

#### 采集 DM 集群的数据

1. 运行 Diag 数据采集命令。

    例如，如需采集从当前时间的 4 小时前到 2 小时前的诊断数据，可以运行以下命令：

    {{< copyable "shell-regular" >}}

    ```bash
    tiup diag collectdm ${cluster-name} -f="-4h" -t="-2h"
    ```

    如需了解在上述命令中使用的参数说明或需要查看使用 Diag 工具时会使用的其他参数，请参考[采集 TiDB 集群的数据](#采集-tidb-集群的数据)。

    运行 Diag 数据采集命令后，Diag 不会立即开始采集数据，而会在输出中提供预估数据量大小和数据存储路径，并询问你是否进行数据收集。

2. 如果确认要开始采集数据，请输入 `Y`。

    采集数据需要一定的时间，具体所需时间与需要收集的数据量有关。例如，在测试环境中收集 1 GB 数据，大概需要 10 分钟。

    采集完成后，Diag 会提示采集数据所在的文件夹路径。例如：

    {{< copyable "shell-regular" >}}

    ```bash
    Collected data are stored in /home/qiaodan/diag-fNTnz5MGhr6
    ```

### 第 3 步：本地查看数据（可选步骤）

已收集的数据会根据其数据来源存储于独立的子目录中，这些子目录以机器名和端口号来命名。每个节点的配置、日志等文件的存放位置与在真实服务器中存放的相对路径相同，其中：

- 系统和硬件的基础信息：位于 `insight.json`
- 系统 `/etc/security/limits.conf` 中的内容：位于 `limits.conf`
- 内核参数列表：位于 `sysctl.conf`
- 内核日志：位于 `dmesg.log`
- 采集时的网络连接情况：位于 `ss.txt`
- 配置数据：位于每节点目录下的 `config.json`
- 集群本身的元信息：位于 `meta.yaml`（此文件位于采集数据存储目录的顶层）
- 监控数据：位于 `/monitor` 文件目录。默认经过压缩，无法直接查看。如需直接查看监控指标的 JSON 文件内容，可在采集时通过 `--compress-metrics=false` 参数禁用压缩。

### 第 4 步：上传数据

如需将集群诊断数据提供给 PingCAP 技术支持人员，请先将数据上传到 Clinic Server 后，再把获取到的数据访问链接发送给技术支持人员。Clinic Server 为 PingCAP Clinic 的云服务，可提供安全的诊断数据存储和共享。

根据集群的网络连接情况，你可以选择以下上传方式之一：

- 方式 1：如果集群所在的网络能访问互联网，你可以[通过上传命令直接上传数据](#方式-1直接上传)。
- 方式 2：如果集群所在的网络不能访问互联网，你需要[打包后再上传数据](#方式-2打包后上传)。

> **注意：**
>
> 如果在上传前没有配置 Token，Diag 会提示上传失败，并提醒你设置 Token。关于 Token 获取方法，请参考[准备数据上传环境（第 2 步）](#第-2-步准备数据上传环境)。

#### 方式 1：直接上传

如果你的集群所在的网络可以访问互联网，你可以直接通过以下命令上传在[第 2 步：采集数据](#第-2-步采集数据)中收集的数据包文件夹：

{{< copyable "shell-regular" >}}

```bash
 tiup diag upload
 ```

输出结果示例如下：

{{< copyable "shell-regular" >}}

```bash
[root@Copy-of-VM-EE-CentOS76-v1 qiaodan]# tiup diag upload /home/qiaodan/diag-fNTnz5MGhr6
Starting component `diag`: /root/.tiup/components/diag/v0.7.0/diag upload /home/qiaodan/diag-fNTnz5MGhr6
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><>>>>>>>>>
Completed!
Download URL: "https://clinic.pingcap.com.cn/portal/#/orgs/4/clusters/XXXX"
```

完成上传后，你可以打开 `Download URL` 中的数据访问链接进行数据查看，也可以将 `Download URL` 中的数据访问链接发给与你对接的 PingCAP 技术支持人员。

#### 方式 2：打包后上传

如果你的集群所在的网络无法访问互联网，你需要先在内网打包数据后，再将其数据包发送到网络连通的设备上进行上传。具体操作方法如下：

1. 打包在[第 2 步：采集数据](#第-2-步采集数据)中采集的数据，并对其数据包进行压缩和加密：

    {{< copyable "shell-regular" >}}

    ```bash
    tiup diag package ${filepath}
    ```

    打包时，Diag 会同时对数据进行压缩和加密。在测试环境中，800 MB 数据压缩后变为 57 MB。示例输出如下：

    ```bash
    Starting component `diag`: /root/.tiup/components/diag/v0.7.0/diag package diag-fNTnz5MGhr6
    packaged data set saved to /home/qiaodan/diag-fNTnz5MGhr6.diag
    ```

    完成打包后，数据包为 `.diag` 格式。只有上传到 Clinic Server 后，该数据包才能被解密并查看。如需直接转发已收集的数据，而不在 Clinic Server 中查看，你可以自行压缩后转发数据。

2. 使用可以访问互联网的机器上传数据压缩包。

    {{< copyable "shell-regular" >}}

    ```bash
    tiup diag upload ${filepath}
    ```

    输出结果示例如下：

    {{< copyable "shell-regular" >}}

    ```bash
    [root@Copy-of-VM-EE-CentOS76-v1 qiaodan]# tiup diag upload /home/qiaodan/diag-fNTnz5MGhr6
    Starting component `diag`: /root/.tiup/components/diag/v0.7.0/diag upload /home/qiaodan/diag-fNTnz5MGhr6
    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>><>>>>>>>>>
    Completed!
    Download URL: "https://clinic.pingcap.com.cn/portal/#/orgs/4/clusters/XXXX"
    ```

3. 完成上传后，你可以打开 `Download URL` 中的数据访问链接，在 Clinic Server 页面进行数据查看，也可以将 `Download URL` 中的数据访问链接发给与你对接的 PingCAP 技术支持人员。

## 本地快速检查集群状态

你可以使用 Diag 对集群状态进行快速诊断。即使集群可以正常运行，也需要定期检查集群是否有潜在的稳定性风险。目前 PingCAP Clinic Technical Preview 版本主要提供对集群配置项的合理性检查，用于发现不合理的配置，并提供修改建议。

1. 采集配置数据：

    {{< copyable "shell-regular" >}}

    ```bash
    tiup diag collect ${cluster-name} --include="config"
    ```

    配置文件数据较小，采集后会默认存放至当前路径下。在测试环境中，对于一个 18 个节点的集群，配置文件数据量小于 10 KB。

2. 诊断配置数据：

    {{< copyable "shell-regular" >}}

    ```bash
    tiup diag check ${subdir-in-output-data}
    ```

    其中，`${subdir-in-output-data}` 为采集数据的存放路径，其路径中存放 `meta.yaml` 文件。

3. 查看诊断结果：

    诊断结果会在命令行中返回，示例如下：

    {{< copyable "shell-regular" >}}

    ```bash
    Starting component `diag`: /root/.tiup/components/diag/v0.7.0/diag check diag-fNTnz5MGhr6

    # 诊断结果
    lili 2022-01-24T09:33:57+08:00

    ## 1. 诊断集群名称等基础信息
    - Cluster ID: 7047403704292855808
    - Cluster Name: lili
    - Cluster Version: v5.3.0

    ## 2. 诊断数据来源信息
    - Sample ID: fNTnz5MGhr6
    - Sampling Date: 2022-01-24T09:33:57+08:00
    - Sample Content:: [system monitor log config]

    ## 3. 诊断结果信息，包括发现的可能的配置问题
    In this inspection, 22 rules were executed.

    The results of **1** rules were abnormal and needed to be further discussed with support team.

    The following is the details of the abnormalities.

    ### 诊断结果摘要
    The configuration rules are all derived from PingCAP’s OnCall Service.

    If the results of the configuration rules are found to be abnormal, they may cause the cluster to fail.

    There were **1** abnormal results.

    #### 诊断结果文档的保存路径
    Rule Name: tidb-max-days
    - RuleID: 100
    - Variation: TidbConfig.log.file.max-days
    - For more information, please visit: https://s.tidb.io/msmo6awg
    - Check Result:
      TidbConfig_172.16.7.87:4000   TidbConfig.log.file.max-days:0   warning
      TidbConfig_172.16.7.86:4000   TidbConfig.log.file.max-days:0   warning
      TidbConfig_172.16.7.179:4000   TidbConfig.log.file.max-days:0   warning

    Result report and record are saved at diag-fNTnz5MGhr6/report-220125153215
    ```

    在上述示例诊断结果信息的最后一部分（即 '#### 诊断结果文档的保存路径'）中，对于被发现的每一条潜在的配置问题，Diag 都会提供对应的知识库链接，以便查看详细的配置建议。在上面示例中，相关链接为 `https://s.tidb.io/msmo6awg`。

## 常见问题

1. 如果数据上传失败了，可以重新上传吗？

    可以。数据上传支持断点上传，如果上传失败了，可以直接再次上传。

2. 数据上传后，无法打开返回的数据访问链接，怎么办？

    你可以先尝试登录 Clinic Server 页面。如果登录后依然无法打开链接，请确认你是否拥有访问该数据的权限。如果没有权限，你需要联系数据所有人给你添加权限后，重新登录 Clinic Server 并访问数据链接。

3. 上传到 Clinic Server 的数据后会保存多久？

    在对应的技术支持 Case 关闭后，PingCAP 会在 90 天内对相关数据进行永久删除或匿名化处理。