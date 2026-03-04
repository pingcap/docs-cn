---
title: Soft Delete 表
summary: 介绍 Soft Delete 表（SOFTDELETE）的创建方式、语义转换、数据恢复、后台清理任务与限制。
---

# Soft Delete 表

Soft Delete（软删除）表通过隐藏列 `_tidb_softdelete_time` 记录删除标记，并通过语义转换将 `DELETE` 重写为“标记删除”，从而实现更长时间的数据保留与可恢复能力。

> **说明：**
>
> Active-Active 场景中 Soft Delete 表是冲突解决与删除同步的重要基础能力。Active-Active 表的创建方式与隐藏列含义请参阅 [Active-Active 表](/active-active-table.md)。

## 创建 Soft Delete 表

Soft Delete 表通过表选项 `SOFTDELETE=RETENTION ...` 启用，也可以通过数据库选项统一启用以便继承。

### 通过数据库选项统一启用（推荐）

```sql
CREATE DATABASE sd_example SOFTDELETE=RETENTION 7 DAY;

USE sd_example;
CREATE TABLE message (
    id INT PRIMARY KEY,
    text VARCHAR(10)
);
```

### 在建表时单独启用

```sql
CREATE TABLE message (
    id INT PRIMARY KEY,
    text VARCHAR(10)
) SOFTDELETE=RETENTION 7 DAY;
```

### 调整 Soft Delete 相关选项

你可以通过 `ALTER TABLE` 调整 `SOFTDELETE` 的保留期，或配置软删除后台清理任务的开关与执行间隔：

```sql
-- 调整保留期
ALTER TABLE message SOFTDELETE=RETENTION 14 DAY;

-- 配置清理任务开关与执行间隔（例如 '24h'、'30m'）
ALTER TABLE message SOFTDELETE_JOB_ENABLE='ON' SOFTDELETE_JOB_INTERVAL='24h';
```

## 软删除语义与数据恢复

启用软删除后，TiDB 会为表增加隐藏列 `_tidb_softdelete_time`，并通过系统变量 [`tidb_translate_softdelete_sql`](/system-variables.md#tidb_translate_softdelete_sql) 控制软删除语义：

- 当 `tidb_translate_softdelete_sql=ON`（默认）时：
    - `DELETE` 会被重写为更新 `_tidb_softdelete_time`（标记为软删除）。
    - `SELECT` 会自动过滤软删除数据。
    - 查询中不能显式引用 `_tidb_softdelete_time`。
- 当 `tidb_translate_softdelete_sql=OFF` 时：
    - 软删除数据不会被自动过滤，你可以查询或写入 `_tidb_softdelete_time`。

> **注意：**
>
> 不要在 `tidb_translate_softdelete_sql=OFF` 的情况下对启用 `SOFTDELETE` 的表执行 `DELETE` 操作。
>
> - 对 Soft Delete 表来说，这可能会绕过软删除语义，导致数据被物理删除。
> - 在 Active-Active 场景中，这还可能造成双向同步的不一致。更多信息请参阅 [Active-Active 表](/active-active-table.md)。

### 通过 EXPLAIN 查看 DML 改写

当 `tidb_translate_softdelete_sql=ON` 时，你可以通过 `EXPLAIN` 观察到 TiDB 对软删除表 DML 的改写：

插入（`INSERT`）：

```sql
EXPLAIN INSERT INTO message (id, text) VALUES (1, 'hello');
```

```text
+----------+---------+------+---------------+----------------------------------------------------------------------------------+
| id       | estRows | task | access object | operator info                                                                    |
+----------+---------+------+---------------+----------------------------------------------------------------------------------+
| Insert_1 | N/A     | root |               | ReplaceConflictIfExpr: not(isnull(sd_example.message._tidb_softdelete_time)) |
+----------+---------+------+---------------+----------------------------------------------------------------------------------+
```

其中 `ReplaceConflictIfExpr` 表示 `INSERT` 在软删除表上会额外处理“主键冲突但该行已软删除”的情况，从而符合软删除语义。

更新（`UPDATE`）：

```sql
EXPLAIN UPDATE message SET text='world' WHERE id=1;
```

```text
+---------------------+---------+------+---------------+------------------------------------------------------+
| id                  | estRows | task | access object | operator info                                        |
+---------------------+---------+------+---------------+------------------------------------------------------+
| Update_4            | N/A     | root |               | N/A                                                  |
| └─Selection_7       | 0.00    | root |               | isnull(sd_example.message._tidb_softdelete_time) |
|   └─Point_Get_6     | 1.00    | root | table:message | handle:1                                             |
+---------------------+---------+------+---------------+------------------------------------------------------+
```

其中 `Selection` 节点会追加 `isnull(_tidb_softdelete_time)` 过滤条件，确保 `UPDATE` 只作用于未软删除的数据。

删除（`DELETE`）：

```sql
EXPLAIN DELETE FROM message WHERE id=1;
```

```text
+---------------------+---------+------+---------------+------------------------------------------------------+
| id                  | estRows | task | access object | operator info                                        |
+---------------------+---------+------+---------------+------------------------------------------------------+
| Update_4            | N/A     | root |               | N/A                                                  |
| └─Selection_7       | 0.00    | root |               | isnull(sd_example.message._tidb_softdelete_time) |
|   └─Point_Get_6     | 1.00    | root | table:message | handle:1                                             |
+---------------------+---------+------+---------------+------------------------------------------------------+
```

`DELETE` 的执行计划会显示为 `Update`，表示 `DELETE` 会被改写为更新 `_tidb_softdelete_time`（软删除标记），而非物理删除。

### 软删除与恢复示例

下面示例展示 `DELETE` 执行软删除后的效果，以及如何通过 `RECOVER VALUES` 恢复数据：

```sql
DROP TABLE IF EXISTS message_recover;
CREATE TABLE message_recover (
    id INT PRIMARY KEY,
    text VARCHAR(10)
) SOFTDELETE=RETENTION 7 DAY;

INSERT INTO message_recover VALUES (1,'hello');
DELETE FROM message_recover WHERE id=1;

-- 关闭语义转换，仅用于查看内部隐藏列（不要在 OFF 时执行 DELETE）
SET @@tidb_translate_softdelete_sql=OFF;
SELECT id, text, _tidb_softdelete_time FROM message_recover;

SET @@tidb_translate_softdelete_sql=ON;
RECOVER VALUES FROM message_recover WHERE id = 1;
SELECT * FROM message_recover;
```

软删除数据在保留期到期后，会由后台清理任务执行物理删除（Hard Delete）。你可以通过全局变量 [`tidb_softdelete_job_enable`](/system-variables.md#tidb_softdelete_job_enable) 控制是否调度该清理任务。

## 监控与排查

- `INFORMATION_SCHEMA.TIDB_SOFTDELETE_TABLE_STATS` 用于查看 Soft Delete 表的行数估算与软删除行数估算（依赖统计信息）。

## 使用限制

- Soft Delete 表当前不支持 `UNIQUE` 索引（包括 `ADD UNIQUE INDEX` 与 `CREATE UNIQUE INDEX`）。
- Soft Delete 表不支持外键（`FOREIGN KEY`）。
- Soft Delete 表不支持多表 `DELETE ... JOIN ...` 等涉及多表的 `DELETE` 语句。
- Soft Delete 表不支持临时表（`TEMPORARY TABLE` / `GLOBAL TEMPORARY TABLE`）。
- 不支持通过 DDL 删除、重命名或修改 `_tidb_softdelete_time` 等内部隐藏列。

