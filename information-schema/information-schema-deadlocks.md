---
title: DEADLOCKS
summary: 了解 information_schema 表 `DEADLOCKS`。
---

# DEADLOCKS

`DEADLOCKS` 表提供当前 TiDB 节点上最近发生的若干次死锁错误的信息。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC deadlocks;
```

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

`DEADLOCKS` 表中需要用多行来表示同一个死锁事件，每行显示参与死锁的其中一个事务的信息。当该 TiDB 节点记录了多次死锁错误时，需要按照 `DEADLOCK_ID` 列来区分，相同的 `DEADLOCK_ID` 表示同一个死锁事件。需要注意，`DEADLOCK_ID` **并不保证全局唯一，也不会持久化**，因而其只能在同一个结果集里表示同一个死锁事件。

`DEADLOCKS` 表中各列的字段含义如下：

* `DEADLOCK_ID`：死锁事件的 ID。当表内存在多次死锁错误的信息时，需要使用该列来区分属于不同死锁错误的行。
* `OCCUR_TIME`：发生该次死锁错误的时间。
* `RETRYABLE`：该次死锁错误是否可重试。关于可重试的死锁错误的说明，参见[可重试的死锁错误](#可重试的死锁错误)小节。
* `TRY_LOCK_TRX_ID`：试图上锁的事务 ID，即事务的 `start_ts`。
* `CURRENT_SQL_DIGEST`：试图上锁的事务中当前正在执行的 SQL 语句的 Digest。
* `CURRENT_SQL_DIGEST_TEXT`：试图上锁的事务中当前正在执行的 SQL 语句的归一化形式。
* `KEY`：该事务试图上锁、但是被阻塞的 key，以十六进制编码的形式显示。
* `KEY_INFO`：对 `KEY` 进行解读得出的一些详细信息，详见 [KEY_INFO](#key_info)。。
* `TRX_HOLDING_LOCK`：该 key 上当前持锁并导致阻塞的事务 ID，即事务的 `start_ts`。

要调整 `DEADLOCKS` 表中可以容纳的死锁事件数量，可通过 TiDB 配置文件中的 [`pessimistic-txn.deadlock-history-capacity`](/tidb-configuration-file.md#deadlock-history-capacity) 配置项进行调整，默认容纳最近 10 次死锁错误的信息。


> **注意：**
>
> * 仅拥有 [PROCESS](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_process) 权限的用户可以查询该表。
> * `CURRENT_SQL_DIGEST` 列中的信息（SQL Digest）为 SQL 语句进行归一化后计算得到的 hash。`CURRENT_SQL_DIGEST_TEXT` 列中的信息为内部从 Statements Summary 系列表中查询得到，因而存在内部查询不到对应语句的可能性。关于 SQL Digest 和 Statements Summary 相关表的详细说明，请参阅[Statement Summary Tables](/statement-summary-tables.md)。

## `KEY_INFO`

`KEY_INFO` 列中展示了对 `KEY` 列中所给出的 key 的详细信息，以 JSON 格式给出。其包含的信息如下：

* `"db_id"`：该 key 所属的数据库（schema）的 ID。
* `"db_name"`：该 key 所属的数据库（schema）的名称。
* `"table_id"`：该 key 所属的表的 ID。
* `"table_name"`：该 key 所属的表的名称。
* `"handle_type"`：该 row key 的 handle 类型，其可能的值有：
  * `"int"`：handle 为 int 类型，即 handle 为 row id；
  * `"common"`：非 int64 类型的 handle，在启用 clustered index 时非 int 类型的主键会显示为此类型；
  * `"unknown"`：当前暂不支持的 handle 类型。
* `"partition_handle"`：是否为 partition handle。
* `"handle_value"`：handle 的值。
* `"index_id"`：该 index key 所属的 index id。
* `"index_name"`：该 index key 所属的 index 名称。
* `"index_values"`：该 index key 中的 index value。

其中，不适用或当前无法查询到的信息会被省略。比如，row key 的信息中不会包含 `index_id`、`index_name` 和 `index_values`，index key 不会包含 `handle_type` 和 `partition_handle`，已经被 drop 掉的表中的 key 的信息可能只有 `table_id` 等几个 ID。

## 可重试的死锁错误

> **注意：**
>
> `DEADLOCKS` 表中默认不收集可重试的死锁错误的信息。如果需要收集，可通过 TiDB 配置文件中的 [`pessimistic-txn.deadlock-history-collect-retryable`](/tidb-configuration-file.md#deadlock-history-collect-retryable) 配置项进行调整。

当事务 A 被另一个事务 B 已经持有的锁阻塞，而事务 B 直接或间接地被当前事务 A 持有的锁阻塞，将会引发一个死锁错误。这里：

+ 情况一：事务 B 可能（直接或间接地）被事务 A 开始后到被阻塞前这段时间内已经执行完成的语句产生的锁阻塞
+ 情况二：事务 B 也可能被事务 A 目前正在执行的语句阻塞

对于情况一，TiDB 将会向事务 A 的客户端报告死锁错误，并终止该事务；而对于情况二，事务 A 当前正在执行的语句将在 TiDB 内部被自动重试。例如，假设事务 A 执行了如下语句：

{{< copyable "sql" >}}

```sql
update t set v = v + 1 where id = 1 or id = 2;
```

事务 B 则先后执行如下两条语句：

{{< copyable "sql" >}}

```sql
update t set v = 4 where id = 2;
update t set v = 2 where id = 1;
```

那么如果事务 A 先后对 `id = 1` 和 `id = 2` 的两行分别上锁，且两个事务以如下时序运行：

1. 事务 A 对 `id = 1` 的行上锁
2. 事务 B 执行第一条语句并对 `id = 2` 的行上锁
3. 事务 B 执行第二条语句试图对 `id = 1` 的行上锁，被事务 A 阻塞
4. 事务 A 试图对 `id = 2` 的行上锁，被 B 阻塞，形成死锁

对于情况二，由于事务 A 阻塞其它事务的语句也是当前正在执行的语句，因而可以解除当前语句所上的悲观锁（使得事务 B 可以继续运行），并重试当前语句。TiDB 内部使用 key 的 hash 来判断是否属于这种情况。

当可重试的死锁发生时，内部自动重试并不会引起事务报错，因而对客户端透明，但是这种情况的频繁发生可能影响性能。当这种情况发生时，在 TiDB 的日志中可以观察到 `single statement deadlock, retry statement` 字样的日志。

## 示例 1

假设有如下表定义和初始数据：

{{< copyable "sql" >}}

```sql
create table t (id int primary key, v int);
insert into t values (1, 10), (2, 20);
```

使两个事务按如下顺序执行：

| 事务 1                               | 事务 2                               | 说明                 |
|--------------------------------------|--------------------------------------|----------------------|
| `update t set v = 11 where id = 1;`  |                                      |                      |
|                                      | `update t set v = 21 where id = 2;`  |                      |
| `update t set v = 12 where id = 2;`  |                                      | 事务 1 阻塞          |
|                                      | `update t set v = 22 where id = 1;`  | 事务 2 报出死锁错误  |

接下来，事务 2 将报出死锁错误。此时，查询 `DEADLOCKS` 表，将得到如下结果：

{{< copyable "sql" >}}

```sql
select * from information_schema.deadlocks;
```

```sql
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+-----------------------------------------+----------------------------------------+----------------------------------------------------------------------------------------------------+--------------------+
| DEADLOCK_ID | OCCUR_TIME                 | RETRYABLE | TRY_LOCK_TRX_ID    | CURRENT_SQL_DIGEST                                               | CURRENT_SQL_DIGEST_TEXT                 | KEY                                    | KEY_INFO                                                                                           | TRX_HOLDING_LOCK   |
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+-----------------------------------------+----------------------------------------+----------------------------------------------------------------------------------------------------+--------------------+
|           1 | 2021-08-05 11:09:03.230341 |         0 | 426812829645406216 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | update `t` set `v` = ? where `id` = ? ; | 7480000000000000355F728000000000000002 | {"db_id":1,"db_name":"test","table_id":53,"table_name":"t","handle_type":"int","handle_value":"2"} | 426812829645406217 |
|           1 | 2021-08-05 11:09:03.230341 |         0 | 426812829645406217 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | update `t` set `v` = ? where `id` = ? ; | 7480000000000000355F728000000000000001 | {"db_id":1,"db_name":"test","table_id":53,"table_name":"t","handle_type":"int","handle_value":"1"} | 426812829645406216 |
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+-----------------------------------------+----------------------------------------+----------------------------------------------------------------------------------------------------+--------------------+
```

该表中产生了两行数据，两行的 `DEADLOCK_ID` 字段皆为 1，表示这两行数据包含同一次死锁错误的信息。第一行显示 ID 为 `426812829645406216` 的事务，在 `"7480000000000000355F728000000000000002"` 这个 key 上，被 ID 为 `"426812829645406217"` 的事务阻塞了；第二行则显示 ID 为 `"426812829645406217"` 的事务在 `"7480000000000000355F728000000000000001"` 这个 key 上被 ID 为 `426812829645406216` 的事务阻塞了，构成了相互阻塞的状态，形成了死锁。

## 示例 2

假设查询 `DEADLOCKS` 表得到了如下结果集：

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

以上查询结果中的 `DEADLOCK_ID` 列表明，前两行共同表示一次死锁错误的信息，两条事务相互等待构成了死锁；而后三行共同表示另一次死锁信息，三个事务循环等待构成了死锁。

## CLUSTER_DEADLOCKS

`CLUSTER_DEADLOCKS` 表返回整个集群上每个 TiDB 节点中最近发生的数次死锁错误的信息，即将每个节点上的 `DEADLOCKS` 表内的信息合并在一起。`CLUSTER_DEADLOCKS` 还包含额外的 `INSTANCE` 列展示所属节点的 IP 地址和端口，用以区分不同的 TiDB 节点。

需要注意的是，由于 `DEADLOCK_ID` 并不保证全局唯一，所以在 `CLUSTER_DEADLOCKS` 表的查询结果中，需要 `INSTANCE` 和 `DEADLOCK_ID` 两个字段共同区分结果集中的不同死锁错误的信息。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC cluster_deadlocks;
```

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

