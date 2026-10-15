---
title: 在 TiDB 中存储 AI Agent Memory
summary: 了解如何使用 SQL 在一张 TiDB 表中存储 AI agent memory，并利用向量搜索、事务、按用户召回和自动过期功能。
---

# 在 TiDB 中存储 AI Agent Memory

一个能够跨会话记住用户的 AI agent，其 memory store 需要完成四件事：按语义查找记忆、按用户和类型缩小范围、在不留下半写入状态的情况下替换过时记忆，以及在记忆过期或用户提出要求时将其遗忘。在 TiDB 中，一张表和普通 SQL 就能覆盖这四种需求，因为向量搜索、二级索引、事务和行过期都位于同一个数据库中。

本文将逐步介绍这张表的设计。若要查看基于相同思路、使用 `pytidb` Python SDK 构建的完整聊天应用，请参见[AI Agent Memory 示例](/ai/guides/memory-with-pytidb.md)。

## 前提条件 {#prerequisites}

- 一个 {{{ .starter }}} 实例。你可以在 [TiDB Cloud](https://tidbcloud.com/free-trial) 上创建一个免费的 {{{ .starter }}} 实例。
- 一个已连接到该实例的 MySQL 客户端。在 [TiDB Cloud console](https://tidbcloud.com/) 中，进入 {{{ .starter }}} 实例的概览页面，然后点击 **Connect** 获取连接参数。

本文中的这些示例使用了 3 维向量，并手动指定其值，从而使 SQL 示例和查询结果更加容易理解。这些向量仅用于演示，不代表由嵌入模型生成的向量嵌入。在你的应用中，请将向量维度设置为嵌入模型的输出大小，例如 `VECTOR(1536)`，并使用该模型生成每个 embedding。

## 第 1 步：创建 memory 表 {#step-1-create-the-memory-table}

首先选择一个数据库。本示例使用每个 {{{ .starter }}} 实例都自带的 `test` 数据库：

```sql
USE test;

CREATE TABLE agent_memory (
    id          BIGINT PRIMARY KEY AUTO_RANDOM,
    user_id     VARCHAR(64) NOT NULL,
    kind        ENUM('fact', 'preference', 'episode') NOT NULL,
    content     TEXT NOT NULL,
    embedding   VECTOR(3) NOT NULL,
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    KEY idx_user (user_id, is_active),
    VECTOR INDEX idx_embedding ((VEC_COSINE_DISTANCE(embedding)))
) TTL = `created_at` + INTERVAL 90 DAY TTL_ENABLE = 'ON';
```

表中的每个部分都对应一种记忆操作：

- `embedding` 和向量索引 `idx_embedding` 用于按语义查找记忆。
- `user_id` 和 `kind` 用于将记忆限定到某个用户和某种类型。建立在 `(user_id, is_active)` 上的二级索引 `idx_user` 可以加快读取某个用户的活跃记忆。
- `is_active` 用于让过时记忆退役，而无需删除它。
- `TTL` 子句使 TiDB 自动清理已存储超过 90 天的记忆。过期记忆不一定会立即删除，因为 TTL 清理是周期性运行的。更多信息，请参见 [TTL (Time to Live)](/time-to-live.md)。

## 第 2 步：写入记忆 {#step-2-write-memories}

```sql
INSERT INTO agent_memory (user_id, kind, content, embedding) VALUES
  ('alice', 'fact',       'Alice is a data engineer at a fintech company.',    '[0.9, 0.1, 0.2]'),
  ('alice', 'preference', 'Alice prefers answers in Python.',                  '[0.2, 0.9, 0.1]'),
  ('alice', 'episode',    'Alice asked how to tune a slow join on 2026-10-01.', '[0.5, 0.4, 0.7]'),
  ('bob',   'fact',       'Bob runs a small online bookstore.',                '[0.8, 0.2, 0.3]'),
  ('bob',   'preference', 'Bob prefers short answers.',                        '[0.1, 0.8, 0.3]');
```

## 第 3 步：在事务中替换过时记忆 {#step-3-replace-an-outdated-memory-in-a-transaction}

当用户修改偏好时，在一个事务中让旧记忆退役并写入新记忆。事务可以确保读取方不会看到只完成一部分的替换结果。

为防止并发写入为同一用户创建多个活跃偏好，请按[为每个用户最多保留一个活跃偏好](#enforce-at-most-one-active-preference-per-user)中的说明添加唯一性约束。

```sql
BEGIN;
UPDATE agent_memory SET is_active = FALSE
 WHERE user_id = 'alice' AND kind = 'preference' AND is_active;
INSERT INTO agent_memory (user_id, kind, content, embedding)
VALUES ('alice', 'preference', 'Alice now prefers answers in Go.', '[0.25, 0.85, 0.15]');
COMMIT;
```

检查结果：

```sql
SELECT content, is_active FROM agent_memory
WHERE user_id = 'alice' AND kind = 'preference'
ORDER BY is_active DESC;
```

```
+----------------------------------+-----------+
| content                          | is_active |
+----------------------------------+-----------+
| Alice now prefers answers in Go. |         1 |
| Alice prefers answers in Python. |         0 |
+----------------------------------+-----------+
```

如果事务中的某条语句失败，例如某个值不符合其列定义，请执行 `ROLLBACK` 而不是 `COMMIT`。语句失败不会结束事务：已经成功的语句仍处于待提交状态，而如果执行 `COMMIT`，这些修改仍会被保存，例如导致用户的旧偏好已退役但新偏好没有写入。执行 `ROLLBACK` 后，记忆会保持原样。

### 为每个用户最多保留一个活跃偏好 {#enforce-at-most-one-active-preference-per-user}

事务可以保证每次替换的原子性，但并发写入仍可能为同一用户创建多个活跃偏好。例如，当当前不存在活跃偏好时，两个事务都可能各自更新 0 行、插入一条新偏好，并成功提交。

如果你的应用只允许每个用户有一个活跃偏好，请添加以下生成列和唯一索引。对于已有表，请先为每个用户停用或移除重复的活跃偏好。

```sql
ALTER TABLE agent_memory
ADD COLUMN active_preference_user VARCHAR(64)
GENERATED ALWAYS AS (
  CASE
    WHEN kind = 'preference' AND is_active THEN user_id
    ELSE NULL
  END
) VIRTUAL;

ALTER TABLE agent_memory
ADD UNIQUE KEY uk_active_preference (active_preference_user);
```

该生成列仅在活跃偏好行中包含 `user_id`。唯一索引可防止两行此类记录拥有相同的用户 ID。其他行在该列中为 `NULL`，因此该索引允许每个用户存在多个非活跃偏好、fact 和 episode。

添加唯一索引后，按上文所示，在单个事务中停用旧偏好并插入新偏好。即使在并发写入场景下，唯一索引也能强制执行这一限制。如果替换失败，请回滚事务。若要重试，请开启一个新事务，并重新执行 `UPDATE` 和 `INSERT`。

## 第 4 步：召回单个用户的记忆 {#step-4-recall-memories-for-one-user}

大多数 agent 请求只需要当前用户的记忆。先按用户过滤，再按与当前请求 embedding 的距离进行排序：

```sql
SELECT kind, content, VEC_COSINE_DISTANCE(embedding, '[0.2, 0.9, 0.2]') AS distance
FROM agent_memory
WHERE user_id = 'alice' AND is_active
ORDER BY distance
LIMIT 3;
```

```
+------------+----------------------------------------------------+-----------------------+
| kind       | content                                            | distance              |
+------------+----------------------------------------------------+-----------------------+
| preference | Alice now prefers answers in Go.                   | 0.0032403313698232683 |
| episode    | Alice asked how to tune a slow join on 2026-10-01. |    0.3295984359391211 |
| fact       | Alice is a data engineer at a fintech company.     |     0.645662235088144 |
+------------+----------------------------------------------------+-----------------------+
```

该查询不会使用向量索引，因为 `WHERE` 过滤会在最近邻搜索之前应用。它可以使用二级索引 `idx_user`，只读取该用户的活跃记忆，并为每条记录计算精确距离。结果是精确的；在使用二级索引时，其成本主要取决于匹配记忆的数量，而不需要全表扫描。对于按用户维度的 agent memory，这通常是正确的模式。

## 第 5 步：跨所有用户召回记忆 {#step-5-recall-memories-across-all-users}

某些功能需要搜索整张表，例如在应用已被授予权限可访问的记忆范围内，查找不同用户之间相似的历史对话。此时应先使用向量索引查找近似最近邻，再进行过滤。获取的候选项数量应多于最终所需数量，因为过滤可能会移除其中一部分。不过，即使候选集之外还存在更多匹配记忆，获取更多候选项也不能保证最终查询一定返回三条匹配结果：

```sql
SELECT * FROM (
  SELECT user_id, kind, content, is_active,
         VEC_COSINE_DISTANCE(embedding, '[0.85, 0.15, 0.25]') AS distance
  FROM agent_memory
  ORDER BY distance
  LIMIT 20
) t
WHERE is_active
ORDER BY distance
LIMIT 3;
```

```
+---------+---------+----------------------------------------------------+-----------+-----------------------+
| user_id | kind    | content                                            | is_active | distance              |
+---------+---------+----------------------------------------------------+-----------+-----------------------+
| alice   | fact    | Alice is a data engineer at a fintech company.     |         1 | 0.0040039807124229165 |
| bob     | fact    | Bob runs a small online bookstore.                 |         1 | 0.0044730676562374505 |
| alice   | episode | Alice asked how to tune a slow join on 2026-10-01. |         1 |     0.225803083881864 |
+---------+---------+----------------------------------------------------+-----------+-----------------------+
```

对该查询执行 `EXPLAIN` 以确认其使用了向量索引：当使用向量索引时，`operator info` 列会包含 `annIndex:`。如果表中只有少量行，优化器可能会改为从 TiKV 读取并跳过向量索引；随着表变大，优化器可能会根据查询及其成本估算选择向量索引。关于过滤条件的位置如何影响向量索引，请参见[在带过滤条件的查询中使用向量索引](/ai/reference/vector-search-index.md#use-the-vector-index-with-filters)。

## 第 6 步：遗忘记忆 {#step-6-forget-memories}

要删除 `agent_memory` 表中为某个用户存储的所有记忆，例如当用户要求被遗忘时，可按 `user_id` 删除：

```sql
DELETE FROM agent_memory WHERE user_id = 'bob';
```

超过 90 天的记忆会由第 1 步中的 `TTL` 子句自动删除。在 {{{ .starter }}} 中，过期行由后台 TTL 任务每 15 分钟清理一次，且 `TTL_JOB_INTERVAL` 是固定值，无法修改。若要立即在召回结果中排除过期记忆，请基于 `created_at` 进行过滤。在第 4 步的查询中，将 `AND created_at > NOW() - INTERVAL 90 DAY` 添加到 `WHERE` 子句中。在第 5 步的查询中，在子查询里选出 `created_at`，并在外层 `WHERE` 子句中与 `is_active` 一起对其进行过滤：

```sql
SELECT * FROM (
  SELECT user_id, kind, content, is_active, created_at,
         VEC_COSINE_DISTANCE(embedding, '[0.85, 0.15, 0.25]') AS distance
  FROM agent_memory
  ORDER BY distance
  LIMIT 20
) t
WHERE is_active AND created_at > NOW() - INTERVAL 90 DAY
ORDER BY distance
LIMIT 3;
```

不要将 `created_at` 过滤条件放在子查询内部。子查询内部的过滤会在最近邻搜索之前应用，因此不会使用向量索引。

> **Note:**
>
> 执行 `DELETE` 后，在垃圾回收移除旧行版本之前，仍然可以在短时间内通过 [stale read](/stale-read.md)（例如 `SELECT ... AS OF TIMESTAMP`）读取到已删除的行。TiDB 会至少保留旧版本到 [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) 所设置的时长，默认值为 10 分钟。

## 另请参阅 {#see-also}

- [AI Agent Memory 示例](/ai/guides/memory-with-pytidb.md)
- [向量搜索索引](/ai/reference/vector-search-index.md)
- [事务](/ai/guides/transactions.md)
- [TTL (Time to Live)](/time-to-live.md)