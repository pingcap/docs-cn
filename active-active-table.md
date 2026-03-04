---
title: Active-Active 表
summary: 介绍 Active-Active 表在 TiDB 层面的作用、创建方式、相关系统变量与限制。
---

# Active-Active 表

Active-Active 表是 TiDB 为 Active-Active（双活）同步场景提供的表能力。它通过隐藏列记录写入时间戳，并结合软删除（`SOFTDELETE`）机制，为多集群多写场景下的冲突解决（Last Write Wins，LWW）提供基础能力。

> **说明：**
>
> 本文档仅介绍 Active-Active 表在 TiDB 层如何创建和使用。如何配置 TiCDC 进行双向同步请参阅相关文档。

## 使用前提

- 你需要部署多个 TiDB 集群，并在集群间部署 TiCDC 同步链路（用于跨集群同步变更）。
- 你需要确保各集群的 PD 生成的时间戳在全局范围内可比较且不会冲突。为此，需要为每个集群配置 PD 的 `tso-max-index` 与 `tso-unique-index`（详见 [PD 配置文件](/pd-configuration-file.md#tso-max-index) 和 [PD 配置文件](/pd-configuration-file.md#tso-unique-index)）。
- 建议为各集群配置 NTP 等时间同步机制，避免因时钟漂移导致事务提交失败或等待时间过长。

> **注意：**
>
> Active-Active 同步不提供跨集群的全局事务一致性，属于最终一致性方案。对于同一行的并发写入可能产生“丢失更新”等现象，请谨慎评估业务适用性。

## 创建 Active-Active 表

Active-Active 表通过表选项 `ACTIVE_ACTIVE='ON'` 启用，并且**必须同时启用软删除**（`SOFTDELETE=RETENTION ...`）。`SOFTDELETE` 选项仅支持 `RETENTION ...` 或 `'OFF'`，不支持 `'ON'`。

### 通过数据库选项统一启用（推荐）

你可以在创建数据库时启用 `ACTIVE_ACTIVE` 与 `SOFTDELETE`，该数据库下新创建的表会自动继承这些选项：

```sql
CREATE DATABASE aa_example ACTIVE_ACTIVE='ON' SOFTDELETE=RETENTION 7 DAY;

USE aa_example;
CREATE TABLE message (
    id INT PRIMARY KEY,
    text VARCHAR(10)
);
```

通过 `SHOW CREATE TABLE` 可以看到这些选项会以注释形式展示（用于 MySQL 兼容），例如：

```sql
SHOW CREATE TABLE message\G
```

示例输出如下（内容会包含 `/*T![active_active] ACTIVE_ACTIVE='ON' */`、`/*T![softdelete] SOFTDELETE=RETENTION 7 DAY */` 等片段）：

```text
*************************** 1. row ***************************
       Table: message
Create Table: CREATE TABLE `message` (
  `id` int NOT NULL,
  `text` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin /*T![active_active] ACTIVE_ACTIVE='ON' */ /*T![softdelete] SOFTDELETE=RETENTION 7 DAY */ /*T![softdelete] SOFTDELETE_JOB_ENABLE='ON' */ /*T![softdelete] SOFTDELETE_JOB_INTERVAL='24h' */
```

### 在建表时单独启用

你也可以在建表时直接指定选项：

```sql
CREATE TABLE message (
    id INT PRIMARY KEY,
    text VARCHAR(10)
) ACTIVE_ACTIVE='ON' SOFTDELETE=RETENTION 7 DAY;
```

### Soft Delete 相关配置

Active-Active 表同时也是 Soft Delete 表。如何配置 `SOFTDELETE` 的保留期、后台清理任务开关与执行间隔，请参阅 [Soft Delete 表](/soft-delete-table.md#调整-soft-delete-相关选项)。

> **注意：**
>
> Active-Active 表不支持将 `SOFTDELETE` 设置为 `'OFF'`，否则会报错。

## 隐藏列与冲突解决（LWW）

启用 Active-Active 后，TiDB 会为表增加一个隐藏列 `_tidb_origin_ts`，用于记录该行数据在上游集群的原始提交时间戳（TiCDC 写入下游时填充）。当 `_tidb_origin_ts` 为 `NULL` 时表示该行由本地事务写入；当 `_tidb_origin_ts` 不为 `NULL` 时表示该行由上游变更同步而来。

同时，TiDB 提供一个只读列 `_tidb_commit_ts` 用于查询该行在本地集群的提交时间戳。`_tidb_commit_ts` 不属于真实表结构，不能用于 `ADD COLUMN`、`ADD INDEX` 等 DDL。

在冲突处理时，可以用如下表达式表示一行数据用于 LWW 冲突解决的时间戳：

```sql
IFNULL(_tidb_origin_ts, _tidb_commit_ts)
```

示例：

```sql
DROP TABLE IF EXISTS message_lww;
CREATE TABLE message_lww (
    id INT PRIMARY KEY,
    text VARCHAR(10)
) ACTIVE_ACTIVE='ON' SOFTDELETE=RETENTION 7 DAY;

INSERT INTO message_lww VALUES (1, 'local'), (2, 'up');

-- 为了展示效果，这里通过手动写入 _tidb_origin_ts 来模拟 TiCDC 在下游写入时填充该列。正式环境下不建议修改 _tidb_origin_ts 列，否则可能导致 Active-Active 同步结果不一致。
UPDATE message_lww SET _tidb_origin_ts=464677399908313272 WHERE id=2;

SELECT
    id,
    _tidb_origin_ts,
    _tidb_commit_ts,
    IFNULL(_tidb_origin_ts, _tidb_commit_ts) AS lww_ts
FROM message_lww
ORDER BY id;
```

```text
+----+--------------------+--------------------+--------------------+
| id | _tidb_origin_ts    | _tidb_commit_ts    | lww_ts             |
+----+--------------------+--------------------+--------------------+
| 1  | <null>             | 464677389206814721 | 464677389206814721 |
| 2  | 464677399908313272 | 464677437959045121 | 464677399908313272 |
+----+--------------------+--------------------+--------------------+
```

- `id=1`：`_tidb_origin_ts` 为 `NULL`，表示该行由本地事务写入，此时 `lww_ts` 取值来自 `_tidb_commit_ts`。
- `id=2`：`_tidb_origin_ts` 不为 `NULL`，表示该行由上游变更同步而来，此时 `lww_ts` 取值来自 `_tidb_origin_ts`。

### 本地写入覆盖上游写入时的行为

当你在本地集群对一行“来自上游”的数据执行写入（例如 `UPDATE`）时，TiDB 会把这次写入视为本地写入，并将该行的 `_tidb_origin_ts` 重置为 `NULL`。同时，本地事务的提交时间戳会保证大于该行的“LWW 时间戳”（即更新前的 `IFNULL(_tidb_origin_ts, _tidb_commit_ts)`），以避免旧写入覆盖新写入。若本地 PD 分配的 TSO 落后于该行的“LWW 时间戳”，事务提交可能会短暂等待重试；在时钟漂移较大时，事务也可能失败。

示例（继续使用上一节的 `message_lww`）：

```sql
SELECT id, text, _tidb_origin_ts FROM message_lww ORDER BY id;

UPDATE message_lww SET text='local2' WHERE id=2;

SELECT id, text, _tidb_origin_ts FROM message_lww ORDER BY id;
```

```text
+----+-------+--------------------+
| id | text  | _tidb_origin_ts    |
+----+-------+--------------------+
|  1 | local |               NULL |
|  2 | up    | 464677399908313272 |
+----+-------+--------------------+
+----+--------+-----------------+
| id | text   | _tidb_origin_ts |
+----+--------+-----------------+
|  1 | local  |            NULL |
|  2 | local2 |            NULL |
+----+--------+-----------------+
```

> **注意：**
>
> 不建议业务显式修改 `_tidb_origin_ts`，否则可能导致 Active-Active 同步结果不一致。

## Soft Delete（必需）

Active-Active 表必须同时启用 Soft Delete。Soft Delete 表的语义（DML 改写、`RECOVER VALUES` 数据恢复、后台清理任务等）请参阅 [Soft Delete 表](/soft-delete-table.md)。

> **注意：**
>
> 不要在 `tidb_translate_softdelete_sql=OFF` 的情况下对启用 `SOFTDELETE` 的表执行 `DELETE` 操作，否则可能会造成 Active-Active 同步的不一致。更多信息请参阅 [Soft Delete 表](/soft-delete-table.md#软删除语义与数据恢复)。

## 监控与排查

- 只读 SESSION 变量 [`tidb_cdc_active_active_sync_stats`](/system-variables.md#tidb_cdc_active_active_sync_stats) 仅供 TiCDC 读取，用于获取 Active-Active 同步的冲突跳过统计信息。
- Soft Delete 表的统计信息（`INFORMATION_SCHEMA.TIDB_SOFTDELETE_TABLE_STATS`）详见 [Soft Delete 表](/soft-delete-table.md#监控与排查)。

## 使用限制

- Active-Active 表必须同时启用 `SOFTDELETE`。
- Active-Active 表必须显式指定主键。
- Active-Active 表（Soft Delete 表）当前不支持 `UNIQUE` 索引（包括 `ADD UNIQUE INDEX` 与 `CREATE UNIQUE INDEX`）。
- Active-Active 表不支持外键（`FOREIGN KEY`）。
- Active-Active 表不支持临时表（`TEMPORARY TABLE` / `GLOBAL TEMPORARY TABLE`）。
- 目前不支持通过 `ALTER TABLE` 修改表的 `ACTIVE_ACTIVE` 启用状态。
- 不支持通过 DDL 删除、重命名或修改 `_tidb_origin_ts`、`_tidb_softdelete_time` 等内部隐藏列。
- Active-Active 表同时适用 Soft Delete 表的其他限制，详见 [Soft Delete 表](/soft-delete-table.md#使用限制)。
