---
title: TiCDC Active-Active 双向同步
summary: 介绍 Active-Active 场景下 TiCDC Changefeed 与 TiDB/PD 的关键配置、以及 DDL 的操作建议。
---

# TiCDC Active-Active 双向同步

TiCDC 支持在双向复制（BDR）的基础上启用 Active-Active（双活）同步模式。在该模式下，TiCDC 会把上游变更转换为带冲突解决逻辑的 SQL 写入下游 TiDB，并基于 Last Write Wins（LWW）策略处理多集群多写导致的写入冲突。

> **说明：**
>
> Active-Active 同步属于最终一致性方案，不提供跨集群的全局事务一致性。Active-Active 表在 TiDB 层的创建方式与隐藏列含义请参阅 [Active-Active 表](/active-active-table.md)，Soft Delete 机制（`SOFTDELETE`、`RECOVER VALUES`、清理任务等）请参阅 [Soft Delete 表](/soft-delete-table.md)。

## 部署 Active-Active 同步

本节按推荐的部署顺序介绍 Active-Active 双向同步的关键配置与操作，并提供最小可跑通的示例。

### 1. 部署两个 TiDB 集群与 TiCDC

你需要至少两个 TiDB 集群（记为集群 A、集群 B），并在各集群部署 TiCDC，用于建立双向同步链路（A→B 与 B→A）。TiCDC 部署方式可参考 [部署 TiCDC](/ticdc/deploy-ticdc.md)。

### 2. 配置并部署 PD（确保跨集群 TSO 可比较）

Active-Active 场景要求不同集群的 PD 生成的时间戳在全局范围内可比较且不冲突。为此，需要在每个集群的 PD 配置中设置 `tso-max-index` 与 `tso-unique-index`（详见 [PD 配置文件](/pd-configuration-file.md#tso-max-index) 和 [PD 配置文件](/pd-configuration-file.md#tso-unique-index)）。

示例：两套集群时，可以将 `tso-max-index` 统一设置为 `2`，并为各集群分配不同的 `tso-unique-index`。

```toml
# 集群 A 的 pd.toml（示例）
tso-max-index = 2
tso-unique-index = 0

# 集群 B 的 pd.toml（示例）
tso-max-index = 2
tso-unique-index = 1
```

> **注意：**
>
> 建议为各集群配置 NTP 等时间同步机制，避免因时钟漂移导致事务提交失败或等待时间过长。

### 3. 在两侧创建 Active-Active 表（TiDB DDL）

Active-Active 同步要求需要双向复制的表必须启用 `ACTIVE_ACTIVE='ON'`，并且必须启用 Soft Delete（`SOFTDELETE=RETENTION ...`，详见 [Soft Delete 表](/soft-delete-table.md)）。你需要在两个集群上创建**同名同结构**的库表。

示例（在集群 A 与集群 B 上分别执行）：

```sql
CREATE DATABASE aa_example ACTIVE_ACTIVE='ON' SOFTDELETE=RETENTION 7 DAY;
USE aa_example;

CREATE TABLE message (
    id INT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name  VARCHAR(100)
);
```

更多 Active-Active 表的建表与隐藏列说明，参阅 [Active-Active 表](/active-active-table.md)。更多 Soft Delete 语义与数据恢复说明，参阅 [Soft Delete 表](/soft-delete-table.md)。

### 4. 创建双向 changefeed（A→B 与 B→A）

Active-Active 模式通过 changefeed 配置项 `enable-active-active` 启用，并且**要求同时启用** `bdr-mode`：

```toml
# changefeed.toml

# 启用双向复制（BDR）模式
bdr-mode = true

# 在 BDR 基础上启用 Active-Active（LWW）同步模式
enable-active-active = true
```

> **注意：**
>
> 如果 changefeed 需要同步 Active-Active 表，请确保已启用 `enable-active-active=true`。否则 TiCDC 可能无法按 Active-Active 的写入与冲突处理逻辑生成下游写入语句，进而导致同步任务异常。

然后分别创建两条 changefeed：

```shell
# 集群 A -> 集群 B
cdc cli changefeed create \
  --server=http://<cluster-a-cdc-host>:<cluster-a-cdc-port> \
  --changefeed-id="changefeed-ab" \
  --start-ts=<tso> \
  --sink-uri="tidb://root@<cluster-b-tidb-host>:<cluster-b-tidb-port>" \
  --config=changefeed.toml

# 集群 B -> 集群 A
cdc cli changefeed create \
  --server=http://<cluster-b-cdc-host>:<cluster-b-cdc-port> \
  --changefeed-id="changefeed-ba" \
  --start-ts=<tso> \
  --sink-uri="tidb://root@<cluster-a-tidb-host>:<cluster-a-tidb-port>" \
  --config=changefeed.toml
```

在创建 changefeed 前，建议确保两侧集群在某个时间点的数据处于一致状态。你可以根据实际需要使用 [Dumpling](/dumpling-overview.md) 与 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 等工具进行全量数据互导，再开启增量双向同步。

关于 `--start-ts` 的选择原则（例如双向复制时上下游如何各自选择起始 TSO），参阅 [TiCDC 双向复制](/ticdc/ticdc-bidirectional-replication.md#部署双向复制)。

### 5.（可选）调整 Active-Active 专用的 changefeed 参数

当 `enable-active-active=true` 且下游为 TiDB 时，TiCDC 会额外执行两类周期性操作：

- 维护下游的进度表，用于 Hard Delete 安全检查（默认每 `30m` 写入一次）。
- 读取下游 TiDB 的 `@@tidb_cdc_active_active_sync_stats` 以获取冲突统计（默认每 `1m` 读取一次）。

对应配置项如下：

```toml
# changefeed.toml

# 进度表更新间隔（默认 30m）
active-active-progress-interval = "30m"

# 读取 @@tidb_cdc_active_active_sync_stats 的间隔（默认 1m）
# 设置为 "0s" 可关闭冲突统计采集
active-active-sync-stats-interval = "1m"
```

`tidb_cdc_active_active_sync_stats` 系统变量仅用于 TiCDC 读取 Active-Active 同步的统计信息。详见 [`tidb_cdc_active_active_sync_stats`](/system-variables.md#tidb_cdc_active_active_sync_stats)。

> **注意：**
>
> - `enable-active-active` 仅支持 TiDB sink（`tidb://...`）以及 storage sink。
> - `enable-active-active` 与 redo log/consistency 特性不兼容。如需启用 Active-Active，请关闭 redo/consistency 相关配置。

## TiDB 侧相关行为与配置

### `tidb_translate_softdelete_sql`

Active-Active 表依赖 `_tidb_softdelete_time` 的语义以及 LWW 写入逻辑。TiCDC 在 Active-Active 模式下写入 TiDB 下游时，会在其连接会话中设置 `tidb_translate_softdelete_sql=OFF`，以便按需读写软删除隐藏列并执行冲突解决逻辑。

> **注意：**
>
> 不要在业务会话中将 [`tidb_translate_softdelete_sql`](/system-variables.md#tidb_translate_softdelete_sql) 设为 `OFF` 后再对启用 `SOFTDELETE` 的表执行 `DELETE`，否则可能会造成 Active-Active 同步的不一致。更多信息请参阅 [Soft Delete 表](/soft-delete-table.md) 和 [Active-Active 表](/active-active-table.md)。

### TiCDC 系统库 `tidb_cdc`

当 `enable-active-active=true` 且下游为 TiDB 时，TiCDC 会在下游创建系统库 `tidb_cdc`，并维护一张进度表 `ticdc_progress_table`，用于 Hard Delete 安全检查。

建议确保：

- 下游 TiDB 的 sink 用户具备创建数据库/表及写入 `tidb_cdc` 的权限。
- 不要将 `tidb_cdc.*` 纳入业务同步范围（TiCDC 会默认跳过该系统库）。

## DDL 操作建议

在 Active-Active 双向同步中，DDL 的处理方式与 TiCDC 双向复制（BDR）一致：需要通过 BDR role 来降低 DDL 冲突与循环复制风险。

### 可复制 DDL

对“可复制 DDL”，建议：

1. 选择一个集群作为 DDL 的唯一入口，设置为 `PRIMARY`：`ADMIN SET BDR ROLE PRIMARY;`
2. 其他集群设置为 `SECONDARY`：`ADMIN SET BDR ROLE SECONDARY;`
3. 只在 `PRIMARY` 集群执行可复制 DDL，TiCDC 会将其同步到 `SECONDARY` 集群。

可复制/不可复制 DDL 的划分以及具体操作步骤，详见 [TiCDC 双向复制](/ticdc/ticdc-bidirectional-replication.md#ddl-类别)。

### 不可复制 DDL

对“不可复制 DDL”，建议按以下流程降低不一致风险：

1. 对所有集群执行 `ADMIN UNSET BDR ROLE;`
2. 暂停相关表的业务写入，并等待增量同步追平
3. 在每个集群上分别执行 DDL
4. 恢复写入并重新设置 BDR role

详细步骤与注意事项，详见 [TiCDC 双向复制](/ticdc/ticdc-bidirectional-replication.md#不可复制的-ddl-的同步场景)。

### Active-Active 特有注意事项

- 需要双向同步的表应以 Active-Active 表形式创建，并保持各集群表结构与表选项一致。建表与选项说明详见 [Active-Active 表](/active-active-table.md)。
- 不支持通过 DDL 删除、重命名或修改 Active-Active 表的内部隐藏列（例如 `_tidb_origin_ts`、`_tidb_softdelete_time`），也不支持在建表后切换表的 `ACTIVE_ACTIVE` 启用状态。详见 [Active-Active 表](/active-active-table.md#使用限制)。
