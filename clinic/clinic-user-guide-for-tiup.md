---
title: 使用 Clinic
summary: 详细介绍在使用 TiUP 部署的集群上如何通过 Clinic 诊断服务远程定位集群问题和本地快速检查集群状态。
---

# 使用 Clinic

对于使用 TiUP 部署的 TiDB 集群和 DM 集群，Clinic 诊断服务可以通过 Clinic Diag 工具与 Clinic Server 云服务实现远程定位集群问题和本地快速检查集群状态。

> **注意：**
>
> - Clinic 诊断服务目前处于 Beta 受邀测试使用阶段，不建议在生产场景中直接使用。
> - Clinic 诊断服务暂时**不支持**对开启了 TLS 加密的集群和使用 TiDB Ansible 部署的集群进行数据采集。

## 使用场景

- [远程定位集群问题](#远程定位集群问题)：

    - 当集群出现问题，需要远程咨询 PingCAP 技术支持时，你可以先使用 Clinic Diag 工具采集诊断数据，将其数据上传到 Clinic Server 后，把数据链接提供给技术支持人员，协助远程定位集群问题。

    > **注意：**
    >
    > - 目前 Clinic 处于 Beta 受邀测试使用阶段，如需使用 Diag 将数据上传到 Clinic Server，请联系与你对接的 PingCAP 技术人员获取试用账号。
    > - Clinic Beta 版本的 Server 端功能暂未开放给外部用户使用。当你将采集好的数据上传到 Clinic Server 并获取了数据链接后，只有经过授权的 PingCAP 技术支持人员可以访问其链接并查看数据。

    - 当集群出现问题，但无法马上进行问题分析时，你可以使用 Diag 工具采集数据后先将其保存下来，用于自己后期再进行问题分析。

- [本地快速检查集群状态](#本地快速检查集群状态)：

    即使集群可以正常运行，也需要定期检查集群是否有潜在的稳定性风险。Clinic 提供的本地快速诊断功能，用于检查集群潜在的健康风险。目前 Clinic Beta 版本主要提供对集群配置项的合理性检查，用于发现不合理的配置，并提供修改建议。

## 准备工作

如果你的中控机上已经安装了 TiUP，可以使用以下命令一键安装 Clinic Diag 工具：

{{< copyable "shell-regular" >}}

```bash
tiup install diag
```

若已安装了 Diag，也可以通过以下命令，将本地的 Diag 一键升级至最新版本：

{{< copyable "shell-regular" >}}

```bash
tiup update diag
```

> **注意：**
>
> - 对于离线集群，需要离线部署 Diag 工具。具体方法，可以参照[离线部署 TiUP 组件：方式 2](/production-deployment-using-tiup.md#离线部署)。
> - Clinic Diag 工具处于 Beta 阶段，暂未包含在 TiDB 官方下载页面中的 TiDB Server 离线镜像包中。

## 远程定位集群问题

Clinic Diag 工具可以快速抓取 TiDB 集群的诊断数据，其中包括监控数据、配置信息等。

### 第 1 步：确定需要采集的数据

如需查看 Clinic Diag 支持采集的数据的详细列表，请参阅 [Clinic 数据采集说明](/clinic/clinic-data-instruction-for-tiup.md)。建议收集完整的监控数据、配置信息等数据，有助于提升后续诊断效率。

### 第 2 步：采集数据

你可以使用 Clinic Diag 采集使用 TiUP 部署的 TiDB 集群和 DM 集群的数据，具体方法如下：

#### 采集 TiDB 集群的数据

1. 运行 Diag 数据采集命令。

    例如，如需采集从当前时间的 4 小时前到 2 小时前的诊断数据，可以运行以下命令：

    {{< copyable "shell-regular" >}}

    ```bash
    tiup diag collect <cluster-name> -f="-4h" -t="-2h"
    ```

    使用参数说明：

    - `-f/--from`：指定采集时间的起始点。如果不指定该参数，默认起始点为当前时间的 2 小时前。如需修改时区，可通过 `-f="12:30 +0900"` 的语法。如果该参数中未指定时区信息，如 `+0800`，则默认时区为 UTC。
    -`-t/--to`：指定采集时间的结束点。如果不指定该参数，默认结束点为当前时刻。如需修改时区，可通过 `-f="12:30 +0900"` 的语法。如果该参数中未指定时区信息，如 `+0800`，则默认时区为 UTC。

    > **提示：**
    >
    > 除了指定采集时间，你还可以使用 Diag 指定更多参数。如需查看完整参数，请使用 `tiup diag collect -h` 命令。
    >
    > - `-l`：传输文件时的带宽限制，单位为 Kbit/s, 默认值为 `100000`（即 scp 的 `-l` 参数）。
    > - `-N/--node`：支持只收集指定节点的数据，格式为 `ip:port`。
    > - `--include`：只收集特定类型的数据，可选值为 `system`，`monitor`，`log`，`config`，`db_vars`。
    > - `--exclude`：不收集特定类型的数据，可选值为 `system`，`monitor`，`log`，`config`，`db_vars`。

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
    tiup diag collectdm <cluster-name> -f="-4h" -t="-2h"
    ```

    如需了解在上述命令中使用的参数说明或需查看使用 Diag 工具时会使用的其他参数，请参阅 [Diag 工具相关参数说明](#采集-TiDB-集群的数据)。

2. 如果确认要开始采集数据，请输入 `Y`。

    采集数据需要一定的时间，具体所需时间与需要收集的数据量有关。例如，在测试环境中收集 1 GB 数据，大概需要 10 分钟。

    采集完成后，Diag 会提示采集数据所在的文件夹路径。例如：

    {{< copyable "shell-regular" >}}

    ```bash
    Collected data are stored in /home/qiaodan/diag-fNTnz5MGhr6
    ```

### 第 3 步：本地查看数据（可选步骤）

已收集的数据会根据其数据来源存储于独立的子目录中，这些子目录以机器名和端口号来命名。每个节点的配置、日志等文件的存放位置与在真实服务器中存放的相对路径相同，其中：

- 基础的系统和硬件信息： 位于 `insight.json`
- 系统 `/etc/security/limits.conf` 中的内容：位于 `limits.conf`
- 内核参数列表：位于 `sysctl.conf`
- 内核日志：位于 `dmesg.log`
- 采集时的网络连接情况：位于 `ss.txt`
- 配置数据：位于每节点目录下的 `config.json`
- 集群本身的元信息：位于 `meta.yaml`（此文件位于采集数据存储目录的顶层）
- 监控数据：位于 `/monitor` 文件目录。默认经过压缩，无法直接查看。如需直接查看监控指标的 JSON 文件内容，可在采集时通过 `--compress-metrics=false` 参数禁用压缩。

### 第 4 步：上传数据

如需将集群诊断数据提供给 PingCAP 技术支持人员，请将数据上传到 Clinic Server，然后再将数据链接发送给技术支持人员。Clinic Server 为 Clinic 诊断服务的云服务，可提供安全的诊断数据存储和共享。

根据集群的网络连接情况，你可以选择以下上传方式之一：

- 如果集群所在的网络可以直接连接 Clinic Server，可以[通过上传命令直接上传数据](#方式-1直接上传)。
- 如果集群所在的网络无法直接连接 Clinic Server，需要[打包后再上传数据](#方式-2打包后上传)。

#### 方式 1：直接上传

当集群所在的网络可以直接连接 Clinic Server 时，可以直接通过以下命令上传在[第 2 步](#第-2-步采集数据)中收集的数据包文件夹：

{{< copyable "shell-regular" >}}

```bash
 tiup diag upload <filepath> -u=username -p='password'
 ```

> **注意：**
>
> 目前 Clinic 在 Beta 受邀测试使用阶段，请联系与你对接的 PingCAP 技术人员获取试用账号。

输出结果示例如下：

{{< copyable "shell-regular" >}}

```bash
[root@Copy-of-VM-EE-CentOS76-v1 qiaodan]# tiup diag upload /home/qiaodan/diag-fNTnz5MGhr6
Starting component `diag`: /root/.tiup/components/diag/v0.5.1/diag upload /home/qiaodan/diag-fNTnz5MGhr6
Enter Username: username
Enter Password: >>>>>>>>>>>>>>>>>>>>>>>>>>>>>><>>>>>>>>>
Completed!
Download URL: "https://clinic.pingcap.com:4433/diag/files?uuid=52679daa98304e43-82efa642ce241f81-8694e4a10c5736ce"
```

完成上传后，你需要将 `Download URL` 中的数据访问链接发给与你对接的 PingCAP 技术支持人员。

> **注意：**
>
> 目前 Clinic Server 的数据访问链接只对 PingCAP 技术支持人员开放，上传数据的外部用户暂时无法打开该链接。

#### 方式 2：打包后上传

如果是离线部署的集群，由于其所在的网络无法直接连接 Clinic Server，需要先在内网打包数据后，再将其发送到网络连通的设备上进行上传。具体操作方法如下：

1. 压缩并加密在[第 2 步](#第2步采集数据)采集的数据包：

    {{< copyable "shell-regular" >}}

    ```bash
    tiup diag package <filepath>
    ```

    打包时，Diag 会同时对数据进行加密和压缩。在测试环境中，800 MB 数据压缩后变为 57 MB。示例输出如下：

    ```bash
    Starting component `diag`: /root/.tiup/components/diag/v0.5.1/diag package diag-fNTnz5MGhr6
    packaged data set saved to /home/qiaodan/diag-fNTnz5MGhr6.diag
    ```

    通过上面的 `package` 命令完成打包后，数据为 `.diag` 格式，只有上传到 Clinic Server 后才能解密查看。如需直接转发已收集的数据，而不在 Clinic Server 中查看，可以自行压缩后转发。

2. 在可以连通 Clinic Server 的网络环境下上传压缩包。

    {{< copyable "shell-regular" >}}

    ```bash
    tiup diag upload filepath -u=username -p='password'
    ```

    > **注意：**
    >
    > 目前 Clinic 在 Beta 受邀测试使用阶段，请联系与你对接的 PingCAP 技术人员获取试用账号。

    输出结果示例如下：

    {{< copyable "shell-regular" >}}

    ```bash
    [root@Copy-of-VM-EE-CentOS76-v1 qiaodan]# tiup diag upload /home/qiaodan/diag-fNTnz5MGhr6
    Starting component `diag`: /root/.tiup/components/diag/v0.5.1/diag upload /home/qiaodan/diag-fNTnz5MGhr6
    Enter Username: username
    Enter Password: >>>>>>>>>>>>>>>>>>>>>>>>>>>>>><>>>>>>>>>
    Completed!
    Download URL: "https://clinic.pingcap.com:4433/diag/files?uuid=52679daa98304e43-82efa642ce241f81-8694e4a10c5736ce"
    ```

    完成上传后，你需要将 `Download URL` 中的数据访问链接发给与你对接的 PingCAP 技术支持人员。

    > **注意：**
    >
    > 目前 Clinic Server 的数据访问链接只对 PingCAP 技术支持人员开放，上传数据的外部用户暂时无法打开该链接。

## 本地快速检查集群状态

你可以使用 Clinic Diag 工具对集群的健康状态进行快速诊断。即使集群可以正常运行，也需要定期检查集群是否有潜在的稳定性风险。目前 Clinic Beta 版本主要提供对集群配置项的合理性检查，用于发现不合理的配置，并提供修改建议。

1. 采集配置数据。

    {{< copyable "shell-regular" >}}

    ```bash
    tiup diag collect <cluster-name> --include="config"
    ```

    配置文件数据较小，采集后会默认存放至当前路径下。在测试环境中，对于一个 18 个节点的集群，配置文件数据量小于 10 KB。

2. 诊断配置数据。

    {{< copyable "shell-regular" >}}

    ```bash
    tiup diag check <subdir-in-output-data>
    ```

    其中，`<sudir-in-output-data>` 为采集数据的存放路径，其中包含 `meta.yaml` 文件。

3. 查看诊断结果。

    诊断结果会在命令行中返回，示例如下：

    {{< copyable "shell-regular" >}}

    ```bash
    Starting component `diag`: /root/.tiup/components/diag/v0.5.1/diag check diag-fNTnz5MGhr6

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

    #### 诊断结果文档的保存路径 Rule Name: tidb-max-days
    - RuleID: 100
    - Variation: TidbConfig.log.file.max-days
    - For more information, please visit: https://s.tidb.io/msmo6awg
    - Check Result:
      TidbConfig_172.16.7.87:4000   TidbConfig.log.file.max-days:0   warning
      TidbConfig_172.16.7.86:4000   TidbConfig.log.file.max-days:0   warning
      TidbConfig_172.16.7.179:4000   TidbConfig.log.file.max-days:0   warning

    Result report and record are saved at diag-fNTnz5MGhr6/report-220125153215
    ```

    在上述示例的诊断结果信息（第 3 部分）中，对于每条发现的配置问题，Diag 都会提供对应的知识库链接，以便查看详细的配置建议。在上面示例中，相关链接为 `https://s.tidb.io/msmo6awg`。

## 常见问题

1. 如果数据上传失败了，可以重新上传吗？

    数据上传支持断点上传，如果失败了，可以直接再次上传。

2. 数据上传后，无法打开返回的数据访问链接，怎么办？

    Clinic 诊断服务目前在 Beta 试用阶段，数据访问链接未对外部用户开放，只有经授权的 PingCAP 内部技术支持人员能打开链接并查看数据。

3. 上传到 Clinic Server 的数据后会保存多久？

    在对应的技术支持 Case 关闭后，PingCAP 会在 90 天内对相关数据进行永久删除或匿名化处理。