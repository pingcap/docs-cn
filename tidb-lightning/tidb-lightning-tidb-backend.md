---
title: TiDB Lightning TiDB-Backend
summary: 了解 TiDB Lightning TiDB-backend。
aliases: ['/docs-cn/v3.0/tidb-lightning/tidb-lightning-tidb-backend/','/docs-cn/v3.0/reference/tools/tidb-lightning/tidb-backend/']
---

# TiDB Lightning TiDB-Backend

TiDB Lightning 的后端决定 `tidb-lightning` 将如何把将数据导入到目标集群中。目前，TiDB Lightning 支持 Importer-backend（默认）和 TiDB-backend 两种后端，两者导入数据的区别如下：

* **Importer-backend**：`tidb-lightning` 先将 SQL 或 CSV 数据编码成键值对，由 `tikv-importer` 对写入的键值对进行排序，然后把这些键值对 Ingest 到 TiKV 节点中。

* **TiDB-backend**：`tidb-lightning` 先将数据编码成 `INSERT` 语句，然后直接在 TiDB 节点上运行这些 SQL 语句进行数据导入。

| 后端 | Importer-backend | TiDB-backend |
|:---|:---|:---|
| 速度 | 快 (~300 GB/小时) | 慢 (~50 GB/小时) |
| 资源使用率 | 高 | 低 |
| 导入时是否满足 ACID | 否 | 是 |
| 目标表 | 必须为空 | 可以不为空 |

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
# schema-pattern = "shard_db_*"
# table-pattern = "shard_table_*"
# target-schema = "shard_db"
# target-table = "shard_table"
```

</td><td>

```toml
# [[routes]]
# schema-pattern = "shard_db_*"
# table-pattern = "shard_table_*"
# target-schema = "shard_db"
# target-table = "shard_table"
```

</td></tr>
</tbody>
</table>
