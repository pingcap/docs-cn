---
title: TiDB Lightning Local&TiDB-Backend
summary: 了解 TiDB Lightning Local&TiDB-backend。
category: reference
aliases: ['/docs-cn/dev/reference/tools/tidb-lightning/backends/']
---

# Lightning Backends Overview

TiDB Lightning 的后端决定 `tidb-lightning` 将如何把将数据导入到目标集群中。目前，TiDB Lightning 支持 Importer-backend（默认）、Local-backend 和 TiDB-backend 三种后端，它们导入数据的区别如下：

* **Importer-backend**：`tidb-lightning` 先将 SQL 或 CSV 数据编码成键值对，由 `tikv-importer` 对写入的键值对进行排序，然后把这些键值对 Ingest 到 TiKV 节点中。(只支持 v4.0.0 以上的 TiDB 集群)

* **Local-backend**: 和 Importer-backend 类似， `tidb-lightning` 先将数据编码成键值对并排序存储在本地临时目录，
然后批量将这些键值对写到各个 TiKV 节点，然后由 TiKV 将它们 Ingest 到集群中。

* **TiDB-backend**：`tidb-lightning` 先将数据编码成 `INSERT` 语句，然后直接在 TiDB 节点上运行这些 SQL 语句进行数据导入。

| 后端 | Local-backend | Importer-backend | TiDB-backend |
|:---|:---|:---|:---|
| 速度 | 快 (~500 GB/小时) | 快 (~500 GB/小时) | 慢 (~50 GB/小时) |
| 资源使用率 | 高 | 高 | 低 |
| 占用网络带宽 | 高 | 中  | 低 |
| 导入时是否满足 ACID | 否 | 否 | 是 |
| 目标表 | 必须为空 | 必须为空 | 可以不为空 |
| 额外组件 | 无 | TiKV Importer | 无 |
| 支持 TiDB 集群版本 | >= v4.0.0 | 全部 | 全部 |


# TiDB Lightning Local-Backend

NOTE: Local-Backend 只支持 v4.0.0 以上的集群

## 部署 Local-backend

使用 Local-backend 时，无需部署 `tikv-importer`。与[标准部署过程](/tidb-lightning/deploy-tidb-lightning.md)相比，部署 TiDB-backend 时有如下不同：

* 可以跳过所有涉及 `tikv-importer` 的步骤。
* 必须更改相应配置申明使用的是 Local-backend。
* 必须指定本地的临时路径用于存储排序后的键值对数据

### 硬件需求

使用 Local-backend 的 TiDB Lightning 为资源密集型程序，同时需要比较多网络带宽：

* 32+ 逻辑核 CPU
* 20G+ 内存
* 足够储存整个数据源的 SSD 硬盘，读取速度越快越好
* 使用万兆网卡，推荐带宽在 1 GB/s 以上

### 使用 TiDB Ansible 部署

1. `inventory.ini` 文件中，`[importer_server]` 部分可以留空。

    ```ini
    ...

    [importer_server]
    # keep empty

    [lightning_server]
    192.168.20.10

    ...
    ```

2. 忽略 `group_vars/all.yml` 文件中 `tikv_importer_port` 部分的设置，`group_vars/importer_server.yml` 文件也不需要修改。但是你需要在 `conf/tidb-lightning.yml` 文件中将 `backend` 设置更改为 `local`。同时增加 设置`sorted-kv-dir`，值为一个可用的本地磁盘的路径，对应的路径必须不存在或为空文件夹。

    ```yaml
    ...
    tikv_importer:
        backend: "local"   # <-- 改成 local
        sorted-kv-dir: "/tmp/sorted-kv"     # <-- 设置为本地磁盘的路径，对应的磁盘需要有足够大的存储空间
    ...
    ```

3. 启动、部署集群。

4. 为 TiDB Lightning 挂载数据源。

5. 启动 `tidb-lightning`。

### 手动部署

手动部署时，你无需下载和配置 `tikv-importer`，TiDB Lightning 可[在此下载](/download-ecosystem-tools.md#tidb-lightning)。

在运行 `tidb-lightning` 之前，在配置文件中加上如下几行：

```toml
[tikv-importer]
backend = "tidb"
sorted-kv-dir = "/tmp/sorted-kv"     # <-- 设置为本地磁盘的路径，对应的磁盘需要有足够大的存储空间
```

或者在用命令行启动 `tidb-lightning` 时，传入参数 `--backend local`。




# TiDB Lightning TiDB-Backend


## 部署 TiDB-backend

使用 TiDB-backend 时，你无需部署 `tikv-importer`。与[标准部署过程](/tidb-lightning/deploy-tidb-lightning.md)相比，部署 TiDB-backend 时有如下不同：

* 可以跳过所有涉及 `tikv-importer` 的步骤。
* 必须更改相应配置申明使用的是 TiDB-backend。

### 硬件需求

使用 TiDB-backend 时， TiDB Lightning 的速度仅受限于 TiDB 执行 SQL 语句的速度。因此，即使是低配的机器也足够发挥出最佳性能。推荐的硬件配置如下：

* 16 逻辑核 CPU
* 足够储存整个数据源的 SSD 硬盘，读取速度越快越好
* 千兆网卡

### 使用 TiDB Ansible 部署

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

### 手动部署

手动部署时，你无需下载和配置 `tikv-importer`，TiDB Lightning 可[在此下载](/download-ecosystem-tools.md#tidb-lightning)。

在运行 `tidb-lightning` 之前，在配置文件中加上如下几行：

```toml
[tikv-importer]
backend = "tidb"
```

或者在用命令行启动 `tidb-lightning` 时，传入参数 `--backend tidb`。

## 冲突解决

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

## 从 Loader 迁移到 TiDB Lightning TiDB-backend

TiDB Lightning TiDB-backend 可以完全取代 [Loader](/loader-overview.md)。下表说明了如何将 [Loader](/loader-overview.md) 的配置迁移到 [TiDB Lightning 配置](/tidb-lightning/tidb-lightning-configuration.md)中：

<table align="left">
<thead><tr><th>Loader</th><th>TiDB Lightning</th></tr></thead>
<tbody>
<tr><td>

```toml
# 日志
log-level = "info"
log-file = "loader.log"
# Prometheus
status-addr = ":8272"
# 线程数
pool-size = 16
```

</td><td>

```toml
[lightning]
# 日志
level = "info"
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
status-port = 10080  # <- 必须有的参数
user = "root"
password = ""
#sql-mode = ""
```

</td></tr>
<tr><td>

```toml
# [[route-rules]]
# Table routes
# pattern-schema = "shard_db_*"
# pattern-table = "shard_table_*"
# target-schema = "shard_db"
# target-table = "shard_table"
```

</td><td>

```toml
# [[routes]]
# Table routes
# pattern-schema = "shard_db_*"
# pattern-table = "shard_table_*"
# target-schema = "shard_db"
# target-table = "shard_table"
```

</td></tr>
</tbody>
</table>
