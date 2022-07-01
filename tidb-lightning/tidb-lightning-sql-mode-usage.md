---
title: 使用 Logical Import Mode
---

# 使用 Logical Import Mode

本文档介绍如何编写 Logical Import Mode 的配置文件，如何进行性能调优等内容。

## 配置及使用

可以通过以下配置文件使用 Logical Import Mode 执行数据导入：

```toml
[lightning]
# 日志
level = "info"
file = "tidb-lightning.log"
max-size = 128 # MB
max-days = 28
max-backups = 14

# 启动之前检查集群是否满足最低需求。
check-requirements = true

[mydumper]
# 本地源数据目录或外部存储 URL
data-source-dir = "/data/my_database"

[tikv-importer]
# 导入模式配置，设为 tidb 即使用 Logical Import Mode
backend = "tidb"

# Logical Import Mode 插入重复数据时执行的操作。
# - replace：新数据替代已有数据
# - ignore：保留已有数据，忽略新数据
# - error：中止导入并报错
on-duplicate = "replace"

[tidb]
# 目标集群的信息。tidb-server 的地址，填一个即可。
host = "172.16.31.1"
port = 4000
user = "root"
# 设置连接 TiDB 的密码，可为明文或 Base64 编码。
password = ""
# tidb-lightning 引用了 TiDB 库，并生成产生一些日志。
# 设置 TiDB 库的日志等级。
log-level = "error"
```

Lightning 的完整配置文件可参考[完整配置及命令行参数](/tidb-lightning/tidb-lightning-configuration.md)。

## 冲突数据检测

冲突数据，即两条或两条以上的记录存在 PK/UK 列数据重复的情况。当数据源中的记录存在冲突数据，将导致该表真实总行数和使用唯一索引查询的总行数不一致的情况。Lightning 的 Logical Import Mode 通过 `on-duplicate` 配置冲突数据检测的策略，根据策略 Lightning 使用不同的 SQL 语句进行插入。

| 设置 | 冲突时默认行为 | 对应 SQL 语句 |
|:---|:---|:---|
| `replace` | 新数据替代旧数据 | `REPLACE INTO ...` |
| `ignore` | 保留旧数据，忽略新数据 | `INSERT IGNORE INTO ...` |
| `error` | 中止导入 | `INSERT INTO ...` |

## 性能调优

- Lightning Logical Import Mode 性能很大程度上取决于目标 TiDB 集群的写入性能，当遇到性能瓶颈时可参考 TiDB 相关[性能优化文档](/best-practices/high-concurrency-best-practices.md)

- 如果发现目标 TiDB 集群的的写入尚未达到瓶颈，可以考虑增加 Lightning 配置中 `region-concurrency` 的值。 `region-concurrency`默认值为 CPU 核数，其含义在 Physical Import Mode 和 Logical Import Mode 下有所不同，Logical Import Mode 的 `region-concurrency` 表示写入并发数。配置示例：

    ```toml
    [lightning]

    region-concurrency = 32
    ```

- 调整目标 TiDB 集群的[raftstore.apply-pool-size](/tikv-configuration-file.md#apply-pool-size)和[raftstore.store-pool-size](/tikv-configuration-file.md#store-pool-size)参数也可能提升导入速度。