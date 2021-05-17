---
title: TiDB Lightning 导入模式
summary: 了解 TiDB 不同导入模式。
aliases: ['/docs-cn/stable/tidb-lightning/tidb-lightning-backends/','/docs-cn/v4.0/tidb-lightning/tidb-lightning-backends/','/docs-cn/stable/reference/tools/tidb-lightning/tidb-backend/','/zh/tidb/stable/tidb-lightning-tidb-backend','/docs-cn/stable/tidb-lightning/tidb-lightning-tidb-backend/','/zh/tidb/v4.0/tidb-lightning-tidb-backend']
---

# TiDB Lightning 后端

TiDB Lightning 的[后端](/tidb-lightning/tidb-lightning-glossary.md#backend)决定 `tidb-lightning` 组件将如何把将数据导入到目标集群中。目前，TiDB Lightning 支持以下后端：

+ [Importer-backend](#tidb-lightning-importer-backend)（默认）
+ [Local-backend](#tidb-lightning-local-backend)
+ [TiDB-backend](#tidb-lightning-tidb-backend)

以上几种后端导入数据的区别如下：

* **Importer-backend**：`tidb-lightning` 先将 SQL 或 CSV 数据编码成键值对，由 `tikv-importer` 对写入的键值对进行排序，然后把这些键值对 Ingest 到 TiKV 节点中。

* **Local-backend**：`tidb-lightning` 先将数据编码成键值对并排序存储在本地临时目录，然后将这些键值对以 SST 文件的形式上传到各个 TiKV 节点，然后由 TiKV 将这些 SST 文件 Ingest 到集群中。和 `Importer-backend` 原理相同，不过不依赖额外的 `tikv-importer` 组件。

* **TiDB-backend**：`tidb-lightning` 先将数据编码成 `INSERT` 语句，然后直接在 TiDB 节点上运行这些 SQL 语句进行数据导入。

| 后端 | Local-backend | Importer-backend | TiDB-backend |
|:---|:---|:---|:---|
| 速度 | 快 (~500 GB/小时) | 快 (~400 GB/小时) | 慢 (~50 GB/小时) |
| 资源使用率 | 高 | 高 | 低 |
| 占用网络带宽 | 高 | 中  | 低 |
| 导入时是否满足 ACID | 否 | 否 | 是 |
| 目标表 | 必须为空 | 必须为空 | 可以不为空 |
| 额外组件 | 无 | `tikv-importer` | 无 |
| 支持 TiDB 集群版本 | >= v4.0.0 | 全部 | 全部 |

## 如何选择后端模式

- 如果导入的目标集群为 v4.0 或以上版本，请优先考虑使用 Local-backend 模式。Local-backend 部署更简单并且性能也较其他两个模式更高
- 如果目标集群为 v3.x 或以下，则建议使用 Importer-backend 模式
- 如果需要导入的集群为生产环境线上集群，或需要导入的表中已包含有数据，则最好使用 TiDB-backend 模式

## TiDB Lightning Local-backend

自 TiDB 4.0.3 版本起，TiDB Lightning 引入了 Local-backend 特性。该特性支持导入数据到 v4.0.0 以上的 TiDB 集群。

### 部署和配置 TiDB Lightning

TiDB Lightning Local-backend 模式的部署方法见 [TiDB Lightning 部署与执行](/tidb-lightning/deploy-tidb-lightning.md)。

## TiDB Lightning TiDB-backend

### 部署和配置 TiDB Lightning

使用 TiDB-backend 时，你无需部署 `tikv-importer`。与[标准部署过程](/tidb-lightning/deploy-tidb-lightning.md)相比，部署 TiDB-backend 时有如下不同：

* 可以跳过所有涉及 `tikv-importer` 的步骤。
* 必须更改相应配置申明使用的是 TiDB-backend。

#### 硬件需求

使用 TiDB-backend 时， TiDB Lightning 的速度仅受限于 TiDB 执行 SQL 语句的速度。因此，即使是低配的机器也足够发挥出最佳性能。推荐的硬件配置如下：

* 16 逻辑核 CPU
* 足够储存整个数据源的 SSD 硬盘，读取速度越快越好
* 千兆网卡

#### 使用 TiDB Ansible 部署

1. `inventory.ini` 文件中，`[importer_server]` 部分可以留空。

    ```ini
    ...

    [importer_server]
    # keep empty

    [lightning_server]
    192.168.20.10

    ...
    ```

2. 忽略 `group_vars/all.yml` 文件中 `tikv_importer_port` 部分的设置，`group_vars/importer_server.yml` 文件也不需要修改。但是你需要在 `conf/tidb-lightning.yml` 文件中将 `backend` 设置更改为 `tidb`。

    ```yaml
    ...
    tikv_importer:
        backend: "tidb"   # <-- 改成 “tidb”
    ...
    ```

3. 启动、部署集群。

4. 为 TiDB Lightning 挂载数据源。

5. 启动 `tidb-lightning`。

#### 手动部署

手动部署时，你无需下载和配置 `tikv-importer`，TiDB Lightning 可[在此下载](/download-ecosystem-tools.md#tidb-lightning)。

在运行 `tidb-lightning` 之前，在配置文件中加上如下几行：

```toml
[tikv-importer]
backend = "tidb"
```

或者在用命令行启动 `tidb-lightning` 时，传入参数 `--backend tidb`。

### 冲突解决

TiDB-backend 支持导入到已填充的表（非空表）。但是，新数据可能会与旧数据的唯一键冲突。你可以通过使用如下任务配置来控制遇到冲突时的默认行为：

```toml
[tikv-importer]
backend = "tidb"
on-duplicate = "replace" # 或者 “error”、“ignore”
```

| 设置 | 冲突时默认行为 | 对应 SQL 语句 |
|:---|:---|:---|
| replace | 新数据替代旧数据 | `REPLACE INTO ...` |
| ignore | 保留旧数据，忽略新数据 | `INSERT IGNORE INTO ...` |
| error | 中止导入 | `INSERT INTO ...` |

### 从 Loader 迁移到 TiDB Lightning TiDB-backend

当需要将数据导入到 TiDB 集群时，TiDB Lightning TiDB-backend 可以完全取代 [Loader](/loader-overview.md)。下表说明了如何将 [Loader](/loader-overview.md) 的配置迁移到 [TiDB Lightning 配置](/tidb-lightning/tidb-lightning-configuration.md)中：

<table>
<thead><tr><th>Loader</th><th>TiDB Lightning</th></tr></thead>
<tbody>
<tr><td>

```toml
# 日志级别
log-level = "info"
# 日志的输出目录
log-file = "loader.log"
# Prometheus
status-addr = ":8272"
# 线程数
pool-size = 16
```

</td><td>

```toml
[lightning]
# 日志级别
level = "info"
# 日志的输出目录。如果未指定该位置目录，默认为执行命令的所在目录。
file = "tidb-lightning.log"
# Prometheus
pprof-port = 8289
# 并发度 (最好使用默认设置)
#region-concurrency = 16
```

</td></tr>
<tr><td>

```toml
# 断点数据库名
checkpoint-schema = "tidb_loader"
```

</td><td>

```toml
[checkpoint]
# 断点存储
enable = true
schema = "tidb_lightning_checkpoint"
# 断点默认存储在本地的文件系统，这样更高效。但你也可以
# 选择将断点存储在目标数据库中，设置如下：
# driver = "mysql"
```

</td></tr>
<tr><td>

```toml
```

</td><td>

```toml
[tikv-importer]
# 使用 TiDB-backend
backend = "tidb"
```

</td></tr>
<tr><td>

```toml
# 数据源目录
dir = "/data/export/"
```

</td><td>

```toml
[mydumper]
# 数据源目录
data-source-dir = "/data/export"
```

</td></tr>

<tr><td>

```toml
[db]
# TiDB 连接参数
host = "127.0.0.1"
port = 4000
user = "root"
password = ""
#sql-mode = ""
```

</td><td>

```toml
[tidb]
# TiDB 连接参数
host = "127.0.0.1"
port = 4000
# 在 tidb-backend 模式下，该参数为非必要参数
# status-port = 10080
user = "root"
password = ""
#sql-mode = ""
```

</td></tr>
<tr><td>

```toml
# [[route-rules]]
# Table routes
# schema-pattern = "shard_db_*"
# table-pattern = "shard_table_*"
# target-schema = "shard_db"
# target-table = "shard_table"
```

</td><td>

```toml
# [[routes]]
# Table routes
# schema-pattern = "shard_db_*"
# table-pattern = "shard_table_*"
# target-schema = "shard_db"
# target-table = "shard_table"
```

</td></tr>
</tbody>
</table>

## TiDB Lightning Importer-backend

### 部署 Importer-backend

本节介绍 TiDB Lightning 使用 Importer 模式的两种部署方式：[使用 TiDB Ansible 部署](#使用-tidb-ansible-部署-tidb-lightning)和[手动部署](#手动部署-tidb-lightning)。

#### 硬件需求

`tidb-lightning` 和 `tikv-importer` 这两个组件皆为资源密集程序，建议各自单独部署。

为了优化效能，建议硬件配置如下：

- `tidb-lightning`

    - 32+ 逻辑核 CPU
    - 足够储存整个数据源的 SSD 硬盘，读取速度越快越好
    - 使用万兆网卡，带宽需 300 MB/s 以上
    - 运行过程默认会占满 CPU资源，因此建议将 `tidb-lightning` 部署到一台单独的机器上。条件不允许的情况下可以和其他组件（比如 `tidb-server`）部署在同一台机器上，然后通过配置 `region-concurrency` 限制 `tidb-lightning` 使用 CPU 资源。

- `tikv-importer`

    - 32+ 逻辑核 CPU
    - 40 GB+ 内存
    - 1 TB+ SSD 硬盘，IOPS 越高越好（要求 ≥8000）
        * 硬盘必须大于最大的 N 个表的大小总和，其中 `N` = `max(index-concurrency, table-concurrency)`。
    - 使用万兆网卡，带宽需 300 MB/s 以上
    - 运行过程中 CPU、I/O 和网络带宽资源都可能占满，建议单独部署。

如果机器充裕的话，可以部署多套 `tidb-lightning` + `tikv-importer`，然后将源数据以表为粒度进行切分，并发导入。

#### 使用 TiDB Ansible 部署 TiDB Lightning

TiDB Lightning 可随 TiDB 集群一起用 [TiDB Ansible 部署](/online-deployment-using-ansible.md)。

1. 编辑 `inventory.ini`，分别配置一个 IP 来部署 `tidb-lightning` 和 `tikv-importer`。

    ```ini
    ...

    [importer_server]
    192.168.20.9

    [lightning_server]
    192.168.20.10

    ...
    ```

2. 修改 `group_vars/*.yml` 的变量配置这两个工具。

    - `group_vars/all.yml`

        ```yaml
        ...
        # tikv-importer 的监听端口。需对 tidb-lightning 服务器开放。
        tikv_importer_port: 8287
        ...
        ```

    - `group_vars/lightning_server.yml`

        ```yaml
        ---
        dummy:

        # 提供监控告警的端口。需对监控服务器 (monitoring_server) 开放。
        tidb_lightning_pprof_port: 8289

        # 获取数据源（Mydumper SQL dump 或 CSV）的路径。
        data_source_dir: "{{ deploy_dir }}/mydumper"
        ```

    - `group_vars/importer_server.yml`

        ```yaml
        ---
        dummy:

        # 储存引擎文件的路径。需存放在空间足够大的分区。
        import_dir: "{{ deploy_dir }}/data.import"
        ```

3. 开始部署。

    {{< copyable "shell-regular" >}}

    ```sh
    ansible-playbook bootstrap.yml &&
    ansible-playbook deploy.yml
    ```

4. 将数据源写入 `data_source_dir` 指定的路径。

5. 登录 `tikv-importer` 的服务器，并执行以下命令来启动 Importer。

    {{< copyable "shell-regular" >}}

    ```sh
    scripts/start_importer.sh
    ```

6. 登录 `tidb-lightning` 的服务器，并执行以下命令来启动 Lightning，开始导入过程。

    {{< copyable "shell-regular" >}}

    ```sh
    scripts/start_lightning.sh
    ```

7. 完成后，在 `tikv-importer` 的服务器执行 `scripts/stop_importer.sh` 来关闭 Importer。

#### 手动部署 TiDB Lightning

##### 第 1 步：部署 TiDB 集群

在开始数据导入之前，需先部署一套要进行导入的 TiDB 集群 (版本要求 2.0.9 以上)，建议使用最新版。部署方法可参考 [使用 TiUP 部署 TiDB 集群](/production-deployment-using-tiup.md)。

##### 第 2 步：下载 TiDB Lightning 安装包

在[工具下载](/download-ecosystem-tools.md#tidb-lightning)页面下载 TiDB Lightning 安装包（需选择与 TiDB 集群相同的版本）。

##### 第 3 步：启动 `tikv-importer`

1. 从安装包上传 `bin/tikv-importer`。

2. 配置 `tikv-importer.toml`。

    ```toml
    # TiKV Importer 配置文件模版

    # 日志文件。
    log-file = "tikv-importer.log"
    # 日志等级：trace、debug、info、warn、error、off。
    log-level = "info"

    # 状态服务器的监听地址。
    status-server-address = "0.0.0.0:8286"

    [server]
    # tikv-importer 监听的地址，tidb-lightning 需要连到这个地址进行数据写入。
    addr = "0.0.0.0:8287"

    [metric]
    # 给 Prometheus 客户端的推送任务名称。
    job = "tikv-importer"
    # 给 Prometheus 客户端的推送间隔。
    interval = "15s"
    # Prometheus Pushgateway 地址。
    address = ""

    [import]
    # 存储引擎文档 (engine file) 的文件夹路径。
    import-dir = "/mnt/ssd/data.import/"
    ```

    上面仅列出了 `tikv-importer` 的基本配置。完整配置请参考[`tikv-importer` 配置说明](/tidb-lightning/tidb-lightning-configuration.md#tikv-importer)。

3. 运行 `tikv-importer`。

    {{< copyable "shell-regular" >}}

    ```sh
    nohup ./tikv-importer -C tikv-importer.toml > nohup.out &
    ```

##### 第 4 步：启动 `tidb-lightning`

1. 从安装包上传 `bin/tidb-lightning` 及 `bin/tidb-lightning-ctl`。

2. 将数据源写入到同样的机器。

3. 配置 `tidb-lightning.toml`。对于没有出现在下述模版中的配置，TiDB Lightning 给出配置错误的提醒并退出。

    ```toml
    [lightning]

    # 转换数据的并发数，默认为逻辑 CPU 数量，不需要配置。
    # 混合部署的情况下可以配置为逻辑 CPU 的 75% 大小。
    # region-concurrency =

    # 日志
    level = "info"
    file = "tidb-lightning.log"

    [tikv-importer]
    # tikv-importer 的监听地址，需改成 tikv-importer 服务器的实际地址。
    addr = "172.16.31.10:8287"

    [mydumper]
    # Mydumper 源数据目录。
    data-source-dir = "/data/my_database"

    [tidb]
    # 目标集群的信息。tidb-server 的监听地址，填一个即可。
    host = "172.16.31.1"
    port = 4000
    user = "root"
    password = ""
    # 表架构信息在从 TiDB 的“状态端口”获取。
    status-port = 10080
    ```

    上面仅列出了 `tidb-lightning` 的基本配置信息。完整配置信息请参考[`tidb-lightning` 配置说明](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-全局配置)。

4. 运行 `tidb-lightning`。如果直接在命令行中用 `nohup` 启动程序，可能会因为 SIGHUP 信号而退出，建议把 `nohup` 放到脚本里面，如：

    {{< copyable "shell-regular" >}}

    ```sh
    #!/bin/bash
    nohup ./tidb-lightning -config tidb-lightning.toml > nohup.out &
    ```
