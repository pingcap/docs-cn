---
title: TiDB Lightning 导入模式
summary: 了解使用 TiDB Lightning 导入数据时，如何选择不同的后端。
---

# TiDB Lightning 导入模式

TiDB Lightning 目前支持两种导入模式，即[后端](/tidb-lightning/tidb-lightning-glossary.md#backend)。不同的后端决定 TiDB Lightning 如何将数据导入到目标 TiDB 集群。

- **Local-backend**：TiDB Lightning 首先将数据编码成键值对并排序存储在本地临时目录，然后将这些键值对上传到各个 TiKV 节点，最后调用 TiKV Ingest 接口将数据插入到 TiKV 的 RocksDB 中。如果用于初始化导入，请优先考虑使用 Local-backend 模式，其拥有较高的导入速度。

- **TiDB-backend**：TiDB Lightning 先将数据编码成 SQL，然后直接运行这些 SQL 语句进行数据导入。如果需要导入的集群为生产环境线上集群，或需要导入的目标表中已包含有数据，则应使用 TiDB-backend 模式。

| 后端 | Local-backend | TiDB-backend |
|:---|:---|:---|
| 速度 | 快 (≈ 500 GB/小时) | 慢 (≈ 50 GB/小时) |
| 资源使用率 | 高 | 低 |
| 占用网络带宽 | 高 | 低 |
| 导入时是否满足 ACID | 否 | 是 |
| 目标表 | 必须为空 |  可以不为空 |
| 支持 TiDB 集群版本 | >= v4.0.0| 全部 |
| 导入期间是否允许 TiDB 对外提供服务 | 否 | 是 |

> **注意：**
>
> - 请勿使用 local-backend 模式向已经投入生产的 TiDB 集群导入数据，这将对在线业务产生严重影响。
>
> - 默认情况下，不应同时启动多个 TiDB Lightning 实例向同一 TiDB 集群导入数据，而应考虑使用[并行导入](/tidb-lightning/tidb-lightning-distributed-import.md)特性。
>
> - 使用多个 TiDB Lightning 向同一目标导入时，请勿混用不同的 backend，例如，不可同时使用 Local-backend 和 TiDB-backend 导入同一 TiDB 集群。

## Local-backend

自 TiDB 4.0.3 版本起，TiDB Lightning 引入了 Local-backend 特性。该特性支持导入数据到 v4.0.0 以上的 TiDB 集群。

### 配置说明与示例

```toml
[Lightning]

# 指定用于存储执行结果的数据库。如果不希望创建此 schema，需要将该值设置为空字符串。
# task-info-schema-name = 'lightning_task_info'

[tikv-importer]
backend = "local"

# 当后端模式为 'local' 时，设置是否检测和解决冲突的记录（唯一键冲突）。
# 目前支持三种解决方法：
#  - none: 不检测冲突记录。该模式是三种模式中性能最佳的，但是可能会导致目的 TiDB 中出现数据不一致的情况。
#  - record: 仅将冲突记录添加到目的 TiDB 中的 `lightning_task_info.conflict_error_v1` 表中。注意，该方法要求目的 TiKV 的版本为 v5.2.0 或更新版本。如果版本过低，则会启用下面的 'none' 模式。
#  - remove: 记录所有的冲突记录，和 'record' 模式相似。但是会删除所有的冲突记录，以确保目的 TiDB 中的数据状态保持一致。
# duplicate-resolution = 'none'

# 当后端是 “local” 时，本地进行 KV 排序的路径。建议使用 SSD 高性能介质，且与 `data-source-dir` 所在分属不同的存储介质，可有效提升导入性能。
# sorted-kv-dir 空间至少需要上游最大表的容量，若空间不足将导致导入失败。
sorted-kv-dir = ""

# 当后端是 “local” 时，TiKV 写入 KV 数据的并发度。当 TiDB Lightning 和 TiKV 直接网络传输速度超过万兆的时候，可以适当增加这个值。
# range-concurrency = 16
# 当后端是 “local” 时，一次请求中发送的 KV 数量。
# send-kv-pairs = 32768

[tidb]
# 目标集群的信息。tidb-server 的地址，填一个即可。
host = "172.16.31.1"
port = 4000
user = "root"
# 设置连接 TiDB 的密码，可为明文或 Base64 编码。
password = ""
# 当后端模式为 'local' 时必填，表结构信息需从 TiDB 的“status-port”获取。
status-port = 10080
# 当后端模式为 'local' 时必填，pd-server 的地址，填一个即可。
pd-addr = "172.16.31.4:2379"
```

### 解决冲突记录

`duplicate-resolution` 配置提供了三种策略处理可能存在的冲突数据。

- none: 默认值。不检测冲突记录。该模式是三种模式中性能最佳的，但是可能会导致目的 TiDB 中出现数据索引不一致的情况。
- record: 仅将冲突记录添加到目的 TiDB 中的 `lightning_task_info.conflict_error_v1` 表中。注意，该方法要求目的 TiKV 的版本为 v5.2.0 或更新版本。如果版本过低，则会启用 'none' 模式。
- remove: 记录所有的冲突记录，和 'record' 模式相似。但是会删除所有的冲突记录，以确保目的 TiDB 中的数据索引保持一致。

以上三种模式中，如果不确定数据源是否存在冲突数据，推荐使用 `remove` 方式。`none` 和 `record` 方式由于不会移除目标表的冲突数据，意味着 TiDB Lightning 生成的唯一索引与数据可能不一致。

## TiDB-backend

### 配置说明与示例

```toml

[tikv-importer]
# 后端模式，对于 TiDB-backend 请设置为 “tidb”
backend = "tidb"

# 对于插入冲突数据时执行的操作：
# - replace：新数据替代已有数据
# - ignore：保留已有数据，忽略新数据
# - error：中止导入并报错
# on-duplicate = "replace"
```

### 解决冲突记录

TiDB-backend 支持导入到已填充的表（非空表）。但是，新数据可能会与旧数据的唯一键冲突。使用 `on-duplicate` 配置采取不同的冲突解决策略：

| 设置 | 冲突时默认行为 | 对应 SQL 语句 |
|:---|:---|:---|
| `replace` | 新数据替代旧数据 | `REPLACE INTO ...` |
| `ignore` | 保留旧数据，忽略新数据 | `INSERT IGNORE INTO ...` |
| `error` | 中止导入 | `INSERT INTO ...` |

## 更多

- [并行导入](/tidb-lightning/tidb-lightning-distributed-import.md)
