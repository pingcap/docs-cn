---
title: DEADLOCKS
summary: 了解 `DEADLOCKS` INFORMATION_SCHEMA 表。
---

# DEADLOCKS

`DEADLOCKS` 表显示当前 TiDB 节点上最近发生的几次死锁错误的信息。

```sql
USE INFORMATION_SCHEMA;
DESC deadlocks;
```

输出结果如下：

```sql
+-------------------------+---------------------+------+------+---------+-------+
| Field                   | Type                | Null | Key  | Default | Extra |
+-------------------------+---------------------+------+------+---------+-------+
| DEADLOCK_ID             | bigint(21)          | NO   |      | NULL    |       |
| OCCUR_TIME              | timestamp(6)        | YES  |      | NULL    |       |
| RETRYABLE               | tinyint(1)          | NO   |      | NULL    |       |
| TRY_LOCK_TRX_ID         | bigint(21) unsigned | NO   |      | NULL    |       |
| CURRENT_SQL_DIGEST      | varchar(64)         | YES  |      | NULL    |       |
| CURRENT_SQL_DIGEST_TEXT | text                | YES  |      | NULL    |       |
| KEY                     | text                | YES  |      | NULL    |       |
| KEY_INFO                | text                | YES  |      | NULL    |       |
| TRX_HOLDING_LOCK        | bigint(21) unsigned | NO   |      | NULL    |       |
+-------------------------+---------------------+------+------+---------+-------+
```

`DEADLOCKS` 表使用多行来显示同一个死锁事件，每一行显示死锁事件中涉及的其中一个事务的信息。如果 TiDB 节点记录了多个死锁错误，则使用 `DEADLOCK_ID` 列来区分每个错误。相同的 `DEADLOCK_ID` 表示同一个死锁事件。注意，`DEADLOCK_ID` **不保证全局唯一性且不会被持久化**，它仅用于在同一个结果集中表示同一个死锁事件。

`DEADLOCKS` 表中各列字段的含义如下：

* `DEADLOCK_ID`：死锁事件的 ID。当表中存在多个死锁错误时，可以使用此列来区分属于不同死锁错误的行。
* `OCCUR_TIME`：死锁错误发生的时间。
* `RETRYABLE`：死锁错误是否可以重试。关于可重试死锁错误的说明，请参见[可重试死锁错误](#可重试死锁错误)部分。
* `TRY_LOCK_TRX_ID`：尝试获取锁的事务 ID。此 ID 也是事务的 `start_ts`。
* `CURRENT_SQL_DIGEST`：获取锁事务中当前正在执行的 SQL 语句的摘要。
* `CURRENT_SQL_DIGEST_TEXT`：获取锁事务中当前正在执行的 SQL 语句的规范化形式。
* `KEY`：事务尝试锁定的被阻塞的键。此字段的值以十六进制字符串形式显示。
* `KEY_INFO`：`KEY` 的详细信息。参见 [`KEY_INFO`](#key_info) 部分。
* `TRX_HOLDING_LOCK`：当前持有该键的锁并导致阻塞的事务 ID。此 ID 也是事务的 `start_ts`。

<CustomContent platform="tidb">

要调整 `DEADLOCKS` 表中可以记录的最大死锁事件数，请在 TiDB 配置文件中调整 [`pessimistic-txn.deadlock-history-capacity`](/tidb-configuration-file.md#deadlock-history-capacity) 配置。默认情况下，表中记录最近 10 次死锁事件的信息。

</CustomContent>

<CustomContent platform="tidb-cloud">

`DEADLOCKS` 表中记录最近 10 次死锁事件的信息。

</CustomContent>

> **警告：**
>
> * 只有具有 [PROCESS](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_process) 权限的用户才能查询此表。
> * `CURRENT_SQL_DIGEST` 列中的信息（SQL 摘要）是从规范化 SQL 语句计算得出的哈希值。`CURRENT_SQL_DIGEST_TEXT` 列中的信息是从语句概要表内部查询的，因此可能找不到相应的语句。有关 SQL 摘要和语句概要表的详细说明，请参见[语句概要表](/statement-summary-tables.md)。

## `KEY_INFO`

`KEY_INFO` 列显示 `KEY` 列的详细信息。信息以 JSON 格式显示。各字段说明如下：

* `"db_id"`：键所属 schema 的 ID。
* `"db_name"`：键所属 schema 的名称。
* `"table_id"`：键所属表的 ID。
* `"table_name"`：键所属表的名称。
* `"partition_id"`：键所在分区的 ID。
* `"partition_name"`：键所在分区的名称。
* `"handle_type"`：行键（即存储一行数据的键）的句柄类型。可能的值如下：
    * `"int"`：句柄类型为 int，表示句柄是行 ID。
    * `"common"`：句柄类型不是 int64。这种类型在启用聚簇索引时的非整数主键中显示。
    * `"unknown"`：当前不支持的句柄类型。
* `"handle_value"`：句柄值。
* `"index_id"`：索引键（存储索引的键）所属的索引 ID。
* `"index_name"`：索引键所属的索引名称。
* `"index_values"`：索引键中的索引值。

在上述字段中，如果某个字段的信息不适用或当前不可用，则该字段在查询结果中会被省略。例如，行键信息不包含 `index_id`、`index_name` 和 `index_values`；索引键不包含 `handle_type` 和 `handle_value`；非分区表不显示 `partition_id` 和 `partition_name`；已删除表中的键信息无法获取 `table_name`、`db_id`、`db_name` 和 `index_name` 等 schema 信息，也无法区分该表是否为分区表。

> **注意：**
>
> 如果一个键来自启用了分区的表，并且在查询期间由于某些原因（例如，键所属的表已被删除）无法查询到该键所属的 schema 信息，则该键所属的分区的 ID 可能会出现在 `table_id` 字段中。这是因为 TiDB 对不同分区的键的编码方式与对几个独立表的键的编码方式相同。因此，当缺少 schema 信息时，TiDB 无法确认该键是属于非分区表还是属于某个表的一个分区。

## 可重试死锁错误

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 此部分不适用于 TiDB Cloud。

</CustomContent>

<CustomContent platform="tidb">

> **注意：**
>
> 默认情况下，`DEADLOCKS` 表不收集可重试死锁错误的信息。如果你希望表收集可重试死锁错误信息，可以在 TiDB 配置文件中调整 [`pessimistic-txn.deadlock-history-collect-retryable`](/tidb-configuration-file.md#deadlock-history-collect-retryable) 的值。

</CustomContent>

当事务 A 被事务 B 已持有的锁阻塞，而事务 B 又直接或间接地被当前事务 A 持有的锁阻塞时，就会发生死锁错误。在这个死锁中，可能存在两种情况：

+ 情况 1：事务 B 可能被事务 A 在开始后、被阻塞前执行的语句生成的锁（直接或间接）阻塞。
+ 情况 2：事务 B 也可能被事务 A 当前正在执行的语句阻塞。

在情况 1 中，TiDB 会向事务 A 的客户端报告死锁错误并终止事务。

在情况 2 中，TiDB 会自动重试事务 A 当前正在执行的语句。例如，假设事务 A 执行以下语句：

```sql
UPDATE t SET v = v + 1 WHERE id = 1 OR id = 2;
```

事务 B 依次执行以下两条语句：

```sql
UPDATE t SET v = 4 WHERE id = 2;
UPDATE t SET v = 2 WHERE id = 1;
```

然后，如果事务 A 锁定 `id = 1` 和 `id = 2` 的两行，并且两个事务按以下顺序运行：

1. 事务 A 锁定 `id = 1` 的行。
2. 事务 B 执行第一条语句并锁定 `id = 2` 的行。
3. 事务 B 执行第二条语句并尝试锁定 `id = 1` 的行，被事务 A 阻塞。
4. 事务 A 尝试锁定 `id = 2` 的行并被事务 B 阻塞，形成死锁。

对于这种情况，由于阻塞其他事务的事务 A 的语句也是当前正在执行的语句，因此可以解除当前语句的悲观锁（以便事务 B 可以继续运行），并重试当前语句。TiDB 内部使用键的哈希来判断是否属于这种情况。

当发生可重试死锁时，内部自动重试不会导致事务错误，因此对客户端是透明的。但是，如果这种情况频繁发生，可能会影响性能。发生这种情况时，你可以在 TiDB 日志中看到 `single statement deadlock, retry statement`。

## 示例 1

假设表定义和初始数据如下：

```sql
CREATE TABLE t (id int primary key, v int);
INSERT INTO t VALUES (1, 10), (2, 20);
```

两个事务按以下顺序执行：

| 事务 1                               | 事务 2                               | 说明                 |
|--------------------------------------|--------------------------------------|----------------------|
| `BEGIN;`                             |                                      |                      |
|                                      | `BEGIN;`                             |                      |
| `UPDATE t SET v = 11 WHERE id = 1;`  |                                      |                      |
|                                      | `UPDATE t SET v = 21 WHERE id = 2;`  |                      |
| `UPDATE t SET v = 12 WHERE id = 2;`  |                                      | 事务 1 被阻塞          |
|                                      | `UPDATE t SET v = 22 WHERE id = 1;`  | 事务 2 报告死锁错误  |

接下来，事务 2 报告死锁错误。此时，查询 `DEADLOCKS` 表：

```sql
SELECT * FROM INFORMATION_SCHEMA.DEADLOCKS;
```

预期输出如下：

```sql
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+-----------------------------------------+----------------------------------------+----------------------------------------------------------------------------------------------------+--------------------+
| DEADLOCK_ID | OCCUR_TIME                 | RETRYABLE | TRY_LOCK_TRX_ID    | CURRENT_SQL_DIGEST                                               | CURRENT_SQL_DIGEST_TEXT                 | KEY                                    | KEY_INFO                                                                                           | TRX_HOLDING_LOCK   |
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+-----------------------------------------+----------------------------------------+----------------------------------------------------------------------------------------------------+--------------------+
|           1 | 2021-08-05 11:09:03.230341 |         0 | 426812829645406216 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | update `t` set `v` = ? where `id` = ? ; | 7480000000000000355F728000000000000002 | {"db_id":1,"db_name":"test","table_id":53,"table_name":"t","handle_type":"int","handle_value":"2"} | 426812829645406217 |
|           1 | 2021-08-05 11:09:03.230341 |         0 | 426812829645406217 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | update `t` set `v` = ? where `id` = ? ; | 7480000000000000355F728000000000000001 | {"db_id":1,"db_name":"test","table_id":53,"table_name":"t","handle_type":"int","handle_value":"1"} | 426812829645406216 |
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+-----------------------------------------+----------------------------------------+----------------------------------------------------------------------------------------------------+--------------------+
```

在 `DEADLOCKS` 表中生成了两行数据。两行的 `DEADLOCK_ID` 字段都是 `1`，表示两行中的信息属于同一个死锁错误。第一行显示，在键 `"7480000000000000355F728000000000000002"` 上，ID 为 `"426812829645406216"` 的事务被 ID 为 `"426812829645406217"` 的事务阻塞。第二行显示，在键 `"7480000000000000355F728000000000000001"` 上，ID 为 `"426812829645406217"` 的事务被 ID 为 `426812829645406216` 的事务阻塞，这构成了互相阻塞，形成了死锁。

## 示例 2

假设你查询 `DEADLOCKS` 表，得到以下结果：

```sql
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+-----------------------------------------+----------------------------------------+----------------------------------------------------------------------------------------------------+--------------------+
| DEADLOCK_ID | OCCUR_TIME                 | RETRYABLE | TRY_LOCK_TRX_ID    | CURRENT_SQL_DIGEST                                               | CURRENT_SQL_DIGEST_TEXT                 | KEY                                    | KEY_INFO                                                                                           | TRX_HOLDING_LOCK   |
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+-----------------------------------------+----------------------------------------+----------------------------------------------------------------------------------------------------+--------------------+
|           1 | 2021-08-05 11:09:03.230341 |         0 | 426812829645406216 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | update `t` set `v` = ? where `id` = ? ; | 7480000000000000355F728000000000000002 | {"db_id":1,"db_name":"test","table_id":53,"table_name":"t","handle_type":"int","handle_value":"2"} | 426812829645406217 |
|           1 | 2021-08-05 11:09:03.230341 |         0 | 426812829645406217 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | update `t` set `v` = ? where `id` = ? ; | 7480000000000000355F728000000000000001 | {"db_id":1,"db_name":"test","table_id":53,"table_name":"t","handle_type":"int","handle_value":"1"} | 426812829645406216 |
|           2 | 2021-08-05 11:09:21.252154 |         0 | 426812832017809412 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | update `t` set `v` = ? where `id` = ? ; | 7480000000000000355F728000000000000002 | {"db_id":1,"db_name":"test","table_id":53,"table_name":"t","handle_type":"int","handle_value":"2"} | 426812832017809413 |
|           2 | 2021-08-05 11:09:21.252154 |         0 | 426812832017809413 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | update `t` set `v` = ? where `id` = ? ; | 7480000000000000355F728000000000000003 | {"db_id":1,"db_name":"test","table_id":53,"table_name":"t","handle_type":"int","handle_value":"3"} | 426812832017809414 |
|           2 | 2021-08-05 11:09:21.252154 |         0 | 426812832017809414 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | update `t` set `v` = ? where `id` = ? ; | 7480000000000000355F728000000000000001 | {"db_id":1,"db_name":"test","table_id":53,"table_name":"t","handle_type":"int","handle_value":"1"} | 426812832017809412 |
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+-----------------------------------------+----------------------------------------+----------------------------------------------------------------------------------------------------+--------------------+
```

上述查询结果中的 `DEADLOCK_ID` 列显示，前两行一起表示一个死锁错误的信息，两个相互等待的事务形成了死锁。接下来的三行一起表示另一个死锁错误的信息，三个循环等待的事务形成了死锁。

## CLUSTER_DEADLOCKS

`CLUSTER_DEADLOCKS` 表返回整个集群中每个 TiDB 节点上最近的死锁错误信息，这是每个节点上 `DEADLOCKS` 表信息的组合。`CLUSTER_DEADLOCKS` 还包括一个额外的 `INSTANCE` 列，用于显示节点的 IP 地址和端口，以区分不同的 TiDB 节点。

注意，由于 `DEADLOCK_ID` 不保证全局唯一性，在 `CLUSTER_DEADLOCKS` 表的查询结果中，你需要同时使用 `INSTANCE` 和 `DEADLOCK_ID` 来区分结果集中不同死锁错误的信息。

```sql
USE INFORMATION_SCHEMA;
DESC CLUSTER_DEADLOCKS;
```

输出结果如下：

```sql
+-------------------------+---------------------+------+------+---------+-------+
| Field                   | Type                | Null | Key  | Default | Extra |
+-------------------------+---------------------+------+------+---------+-------+
| INSTANCE                | varchar(64)         | YES  |      | NULL    |       |
| DEADLOCK_ID             | bigint(21)          | NO   |      | NULL    |       |
| OCCUR_TIME              | timestamp(6)        | YES  |      | NULL    |       |
| RETRYABLE               | tinyint(1)          | NO   |      | NULL    |       |
| TRY_LOCK_TRX_ID         | bigint(21) unsigned | NO   |      | NULL    |       |
| CURRENT_SQL_DIGEST      | varchar(64)         | YES  |      | NULL    |       |
| CURRENT_SQL_DIGEST_TEXT | text                | YES  |      | NULL    |       |
| KEY                     | text                | YES  |      | NULL    |       |
| KEY_INFO                | text                | YES  |      | NULL    |       |
| TRX_HOLDING_LOCK        | bigint(21) unsigned | NO   |      | NULL    |       |
+-------------------------+---------------------+------+------+---------+-------+
```
