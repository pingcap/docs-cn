---
title: 使用逻辑导入模式
summary: 了解在 TiDB Lightning 的逻辑导入模式下，如何编写数据导入任务的配置文件，如何进行性能调优等。
---

# 使用逻辑导入模式

本文档介绍如何编写[逻辑导入模式](/tidb-lightning/tidb-lightning-logical-import-mode.md)的配置文件，如何进行性能调优等内容。

## 配置及使用

可以通过以下配置文件使用逻辑导入模式执行数据导入：

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
# 本地源数据目录或外部存储 URI。关于外部存储 URI 详情可参考 https://docs.pingcap.com/zh/tidb/v6.6/backup-and-restore-storages#uri-%E6%A0%BC%E5%BC%8F。
data-source-dir = "/data/my_database"

[tikv-importer]
# 导入模式配置，设为 tidb 即使用逻辑导入模式
backend = "tidb"

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

TiDB Lightning 的完整配置文件可参考[完整配置及命令行参数](/tidb-lightning/tidb-lightning-configuration.md)。

## 冲突数据检测

冲突数据是指两条或两条以上记录中存在主键或唯一键列数据重复。TiDB Lightning 的逻辑导入模式通过 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 配置冲突数据的处理行为，使用不同的 SQL 语句进行导入。

| 策略 | 冲突时默认行为                     | 对应 SQL 语句 |
|:---|:----------------------------|:---|
| `"replace"` | 新数据替代旧数据                    | `REPLACE INTO ...` |
| `"ignore"` | 保留旧数据，忽略新数据                 | `INSERT IGNORE INTO ...` |
| `"error"` | 遇到冲突数据时终止导入                        | `INSERT INTO ...` |
| `""` | 会被转换为 `"error"`，遇到冲突数据时终止导入 | 无 |

配置为 `"error"` 时，由冲突数据引发的错误将直接导致导入任务终止。配置为 `"replace"` 或 `"ignore"` 时，可以通过进一步配置 [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 控制冲突数据的上限。默认值为 `9223372036854775807`，意味着几乎能容忍全部错误。

配置为 `"ignore"` 时，冲突数据可以被记录到下游的 `conflict_records` 表中，详见[可容忍错误](/tidb-lightning/tidb-lightning-error-resolution.md)功能介绍。此时可以通过配置 [`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 控制记录上限，超出上限的冲突数据会被跳过导入而不再记录。默认值为 `100`。

## 性能调优

- TiDB Lightning 的逻辑导入模式性能很大程度上取决于目标 TiDB 集群的写入性能，当遇到性能瓶颈时可参考 TiDB 相关[性能优化文档](/best-practices/high-concurrency-best-practices.md)。

- 如果发现目标 TiDB 集群的的写入尚未达到瓶颈，可以考虑增加 Lightning 配置中 `region-concurrency` 的值。`region-concurrency` 默认值为 CPU 核数，其含义在物理导入模式和逻辑导入模式下有所不同，逻辑导入模式的 `region-concurrency` 表示写入并发数。配置示例：

    ```toml
    [lightning]
    region-concurrency = 32
    ```

- 调整目标 TiDB 集群的 [`raftstore.apply-pool-size`](/tikv-configuration-file.md#apply-pool-size) 和 [`raftstore.store-pool-size`](/tikv-configuration-file.md#store-pool-size) 参数也可能提升导入速度。
