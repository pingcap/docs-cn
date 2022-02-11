---
title: TiUP 环境的 Clinic 操作手册
summary: 在 TiUP 部署的集群上如何使用 Clinic 工具进行数据采集和快速检查
---

# TiUP 环境的 Clinic 诊断服务操作手册

对于使用 TiUP 部署的集群，Clinic 诊断服务可以通过 Clinic Diag 工具与 Clinic Server 云服务对该集群进行数据采集和集群快速诊断。

> **注意：**
>
> 本文档**仅**适用于使用 TiUP 部署的集群。如需查看适用于使用 TiDB Operator 部署的集群，请参阅[Operator 环境的 Clinic 操作手册](clinic/clinic-user-guide-for-operator.md)。
> Clinic 诊断服务暂时不支持对开启了 TLS 加密的集群和使用 TiDB Ansible 部署的集群进行数据采集。


## 工具安装
在安装有 TiUP 的中控机上，执行以下命令安装工具：
{{< copyable "shell-regular" >}}

```bash
tiup install diag 
```

若已安装 TiUP，可以将其直接升级至最新版本：

{{< copyable "shell-regular" >}}

```bash
tiup update diag
```

> **注意：**
>
> 对于离线集群，需要离线部署 Diag 工具。具体的离线部署办法，可以参照[离线部署 TiUP 组件](/production-deployment-using-tiup.md)。
> Diag 工具暂不属于正式功能，该工具不包含在 TiDB 官方下载页面中的 TiDB Server 离线镜像包中。

## 使用 Clinic Diag 工具采集诊断数据

Clinic 提供 TiDB 集群诊断数据快速抓取的方法，可以抓取监控数据、日志、配置信息等。适于在以下场景中使用：

- 遇到问题咨询 PingCAP 技术支持，需要提供诊断数据协助定位问题。
- 保留诊断数据做后期分析。

### 第一步：确定需要采集的数据
Clinic Diag 支持采集的详细数据列表在[Clinic 数据采集说明 - TiUP 环境](/clinic/clinic-data-instruction-for-tiup.md)，建议收集完整的监控数据、日志、配置信息等数据，有助于提升后续诊断效率。  

### 第二步：采集数据
Clinic Diag 支持采集 TiDB 集群和 DM 集群的数据，将分别进行介绍。

#### TiDB 集群数据采集操作步骤
一条命令收集从4小时前到2小时前的诊断数据：

{{< copyable "shell-regular" >}}

```bash
tiup diag collect <cluster-name> -f="-4h" -t="-2h"
```
采集过程中会先预估数据量大小，并询问用户是否进行数据收集，示例如下：
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
用户输入“Y” 后，开始数据采集。采集数据需要一定的时间，所需时间与收集的数据量有关，测试环境中收集 1GB 数据，大概需要 10 分钟。
采集完成后，会提示采集数据所在的文件夹路径，示例如下：
{{< copyable "shell-regular" >}}

```bash
Collected data are stored in /home/qiaodan/diag-fNTnz5MGhr6
```

采集参数说明：
- -f/--from: 采集时间起始点，默认为当前时刻的2小时前，如果不带时区（+0800）默认为 UTC， 也支持 -f="-4h" 这种格式，指定收集数据开始时间为4小时前。
  - 可通过形如 +0800 的语法指定时区，如 -f="12:30 +0900"。
- -t/--to: 采集时间结束点，默认为当前时刻，如果不带时区（+0800）默认为 UTC，也支持 -t="-2h" 这种格式，指定收集结束时间为2小时前。
  - 可通过形如 +0800 的语法指定时区，如 -t="12:30 +0900"。
- -l: 传输文件时的带宽限制，单位 Kbit/s, 默认为 100000 (即 scp 的 -l 参数)。
- -N/--node : 支持只收集直接节点的数据，格式[ip:port] 。
- --include : 只收集某类型的数据，支持[system, monitor, log, config, db_vars]
- --exclude : 不收集某类型的数据，支持[system, monitor, log, config, db_vars]。

> **注意：**
> db_vars （系统变量）数据收集需要额外提供系统变量可读权限数据库访问的用户名和密码，默认不收集此项。
> 如果需要收集包括系统变量在内的全量诊断数据，可使用以下命令。
> {{< copyable "shell-regular" >}}
> 
> ```bash
> tiup diag collect <cluster-name> --include="system,monitor,log,config,db_vars"
> ```

- 更多参数也可以通过命令查看
  {{< copyable "shell-regular" >}}
  ```bash
  tiup diag collect -h 
  ```

### DM 集群数据采集操作步骤
一条命令收集从4小时前到2小时前的诊断数据：

{{< copyable "shell-regular" >}}

```bash
tiup diag collectdm <cluster-name> -f="-4h" -t="-2h"
```
{{< copyable "shell-regular" >}}

```bash
Collected data are stored in /home/qiaodan/diag-fNTnz5MGhr6
```
采集过程中会先预估数据量大小，并询问用户是否进行数据收集。用户输入“Y” 后，开始数据采集。采集数据需要一定的时间，所需时间与收集的数据量有关，测试环境中收集 1GB 数据，大概需要 10 分钟。
采集完成后，会提示采集数据所在的文件夹路径。

采集参数说明：
- -f/--from: 采集时间起始点，默认为当前时刻的2小时前，如果不带时区（+0800）默认为 UTC， 也支持 -f="-4h" 这种格式，指定收集数据开始时间为4小时前。
  - 可通过形如 +0800 的语法指定时区，如 -f="12:30 +0900"。
- -t/--to: 采集时间结束点，默认为当前时刻，如果不带时区（+0800）默认为 UTC，也支持 -t="-2h" 这种格式，指定收集结束时间为2小时前。
  - 可通过形如 +0800 的语法指定时区，如 -t="12:30 +0900"。
- -l: 传输文件时的带宽限制，单位 Kbit/s, 默认为 100000 (即 scp 的 -l 参数)。
- -R/--role : 只收集某种组件的数据，支持[dm-master，dm-worker]。
- -N/--node : 支持只收集直接节点的数据，格式[ip:port] 。
- --include : 只收集某类型的数据，支持[system, monitor, log, config]
- --exclude : 不收集某类型的数据，支持[system, monitor, log, config]。
- 更多参数也可以通过命令查看
  {{< copyable "shell-regular" >}}
  ```bash
  tiup diag collect -h 
  ```

### 第三步：上传数据
用户需要将诊断数据提供给 PingCAP 技术支持人员时，需要将数据上传到 Clinic Server ，然后将数据链接发送给技术支持人员。 Clinic Server 提供更安全的诊断数据存储和共享。
对于集群可以连接外网的场景和离线部署的集群，分别提供不同的上传方式。

#### 直接上传
适用场景：集群所在的网络可以直接连接 Clinic Server 
操作方式：
对于在第二步收集的数据包文件夹，直接执行上传命令如下：

 {{< copyable "shell-regular" >}}
```bash
 tiup diag upload <filepath> -u=username -p='password'
 ```

{{< copyable "shell-regular" >}}
```bash
[root@Copy-of-VM-EE-CentOS76-v1 qiaodan]# tiup diag upload /home/qiaodan/diag-fNTnz5MGhr6
Starting component `diag`: /root/.tiup/components/diag/v0.5.1/diag upload /home/qiaodan/diag-fNTnz5MGhr6
Enter Username: username
Enter Password: >>>>>>>>>>>>>>>>>>>>>>>>>>>>>><>>>>>>>>>
Completed!
Download URL: "https://clinic.pingcap.com:4433/diag/files?uuid=52679daa98304e43-82efa642ce241f81-8694e4a10c5736ce"
```
  - 上传需要提供用户名和密码，目前 Clinic 在 Beta 受邀测试使用阶段，请联系与您对接的 PingCAP 技术人员或者联系 clinic-trail@pingcap.com 获取试用账号。
  - 上传完成后返回数据访问链接，请将 `Download URL` 中的数据访问链接发给 PingCAP 技术支持人员。目前 Clinic Server 的数据访问链接只对 PingCAP 技术支持人员开放，上传数据的外部用户暂时无法打开该链接。
  

#### 先打包后上传
适用场景：集群是离线部署，所在的网络无法直接连接 Clinic Server ，需要先在内网打包，然后发送到网络连通的设备上进行上传。
操作方式：
1. 先使用 Package 命令对第二步收集的数据包进行压缩和加密，然后将压缩后的文件传到非隔离网络。
 {{< copyable "shell-regular" >}}
```bash
tiup diag package <filepath>
```
 {{< copyable "shell-regular" >}}
```bash
Starting component `diag`: /root/.tiup/components/diag/v0.5.1/diag package diag-fNTnz5MGhr6
packaged data set saved to /home/qiaodan/diag-fNTnz5MGhr6.diag
```
  - 打包时会同时进行加密和压缩。测试环境中 800MB 数据压缩后变为 57MB。
  - 打包后文件将会是 xxxx.diag，是可以被正常上传的，不需要进行额外处理。
  - 如果用户想直接转发收集的数据并不在 Clinic Server 查看，可以自行压缩转发。 `Package` 命令压缩后的数据包必须上传到 Clinic Server 后才能解密查看。

2. 在可以连通 Clinic Server 的网络环境下上传压缩包：
 {{< copyable "shell-regular" >}}
```bash
tiup diag upload filepath -u=username -p='password'
```
{{< copyable "shell-regular" >}}
```bash
[root@Copy-of-VM-EE-CentOS76-v1 qiaodan]# tiup diag upload /home/qiaodan/diag-fNTnz5MGhr6
Starting component `diag`: /root/.tiup/components/diag/v0.5.1/diag upload /home/qiaodan/diag-fNTnz5MGhr6
Enter Username: username
Enter Password: >>>>>>>>>>>>>>>>>>>>>>>>>>>>>><>>>>>>>>>
Completed!
Download URL: "https://clinic.pingcap.com:4433/diag/files?uuid=52679daa98304e43-82efa642ce241f81-8694e4a10c5736ce"
```
  - 上传需要提供用户名和密码，目前 Clinic 在 Beta 受邀测试使用阶段，请联系与您对接的 PingCAP 技术人员或者联系 clinic-trail@pingcap.com 获取试用账号。
  - 上传完成后返回数据访问链接，请将 `Download URL` 中的数据访问链接发给 PingCAP 技术支持人员。目前 Clinic Server 的数据访问链接只对 PingCAP 技术支持人员开放，上传数据的外部用户暂时无法打开该链接。

### 可选操作：本地查看数据
所有收集到的数据被按来源存储在以机器名和端口号命名的独立子目录中，对每个节点，其中的配置、日志等文件均按照其在真实服务器上相同的相对路径存放。
其中：
- 基础的系统和硬件信息在 `insight.json` 中
- 系统 `/etc/security/limits.conf` 中的内容在 `limits.conf` 中
- 内核参数列表在 `sysctl.conf` 中
- 内核日志在 `dmesg.log` 中
- 采集当时的网络连接情况在 `ss.txt` 中
- 配置数据在每节点目录下的 `config.json` 中
- 集群本身的元信息在 `meta.yaml` 中，此文件位于采集数据存储目录的顶层。
- 监控数据在 `/monitor` 文件目录中，默认经过压缩，无法直接查看，如需直接查看监控指标的 JSON 文件内容，可在采集时通过 `--compress-metrics=false` 参数禁用压缩。

## 使用 Clinic Diag 工具快速诊断集群

Clinic Diag 工具支持对集群的健康状态进行快速的诊断，目前版本主要支持配置项内容检查，快速发现不合理的配置项。

### 使用步骤
（1）采集配置数据 
 {{< copyable "shell-regular" >}}
```bash
tiup diag collect <cluster-name> --include="config" 
```
- 默认的采集数据会放到当前路径下。配置文件数据较小，测试环境 18 节点集群数据量小于 10KB。

（2）对配置数据进行诊断
 {{< copyable "shell-regular" >}}
```bash
tiup diag check <subdir-in-output-data> 
```
- <sudir-in-output-data>  是用 `diag collect` 命令收集数据后包含 `meta.yaml` 的目录 。

### 诊断输出示例：
诊断结果会在命令行返回，示例如下：
 {{< copyable "shell-regular" >}}
```bash
Starting component `diag`: /root/.tiup/components/diag/v0.5.1/diag check diag-fNTnz5MGhr6
# Check Result Report
lili 2022-01-24T09:33:57+08:00

## 1. Cluster Information
- Cluster ID: 7047403704292855808
- Cluster Name: lili
- Cluster Version: v5.3.0

## 2. Sample Information
- Sample ID: fNTnz5MGhr6
- Sampling Date: 2022-01-24T09:33:57+08:00
- Sample Content:: [system monitor log config]

## 3. Main results and abnormalities
In this inspection, 22 rules were executed.
The results of **1** rules were abnormal and needed to be further discussed with support team.
The following is the details of the abnormalities.

### Configuration Summary
The configuration rules are all derived from PingCAP’s OnCall Service.
If the results of the configuration rules are found to be abnormal, they may cause the cluster to fail.
There were **1** abnormal results.

#### Rule Name: tidb-max-days
- RuleID: 100
- Variation: TidbConfig.log.file.max-days
- For more information, please visit: https://s.tidb.io/msmo6awg
- Check Result: 
  TidbConfig_172.16.7.87:4000   TidbConfig.log.file.max-days:0   warning  
  TidbConfig_172.16.7.86:4000   TidbConfig.log.file.max-days:0   warning  
  TidbConfig_172.16.7.179:4000   TidbConfig.log.file.max-days:0   warning  

Result report and record are saved at diag-fNTnz5MGhr6/report-220125153215
```
说明：
- 第一部分展示诊断集群名称等基础信息。
- 第二部分展示诊断数据来源信息。
- 第三部分展示诊断结果信息，包括发现的可能的配置问题。对于每条发现的配置问题，都提供知识库链接，用户可以打开链接查看详细的配置建议。在上面示例中，相关链接为：https://s.tidb.io/msmo6awg 。
- 最后一行展示诊断结果文档的保存路径。

## 常见问题

1. 上传失败可以重新上传么？

  回答： 工具上传支持断点上传，如果失败了，可以直接再次上传。

2. 上传后返回的数据访问链接用户无法打开，怎么办？

  回答： Clinic 诊断服务目前在 Beta 试用阶段，数据访问链接未开放给外部用户，只有经授权的 PingCAP 内部技术支持人员能打开查看数据。

3. 数据上传 Clinic Server 后会保存多久？

  回答：数据将在对应的技术支持 Case 关闭后90天内永久删除或匿名化处理。


