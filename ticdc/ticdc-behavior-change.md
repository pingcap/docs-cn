---
title: TiCDC 行为变更说明
summary: 介绍 TiCDC changefeed 的行为变更，说明变更原因以及影响范围。
---

# TiCDC 行为变更说明

## 将 `UPDATE` 事件拆分为 `DELETE` 和 `INSERT` 事件

### 含有单条 `UPDATE` 变更的事务拆分

从 v6.5.3、v7.1.1 和 v7.2.0 开始，使用非 MySQL Sink 时，对于仅包含一条 `UPDATE` 变更的事务，如果 `UPDATE` 事件的主键或者非空唯一索引的列值发生改变，TiCDC 会将该条事件拆分为 `DELETE` 和 `INSERT` 两条事件。详情见 GitHub issue [#9086](https://github.com/pingcap/tiflow/issues/9086)。

该变更主要为了解决如下问题：

* 在使用 CSV 和 AVRO 协议时，仅输出新值而不输出旧值。因此，当主键或者非空唯一索引的列值发生改变时，消费者只能接收到变化后的新值，无法得到旧值，导致无法处理变更前的值（例如删除旧值）。
* 在使用 Index value dispatcher 将数据按照 Key 分发到不同的 Kafka partition 时，下游的消费者组内多个消费者进程独立消费 Kafka Topic partition，由于消费进度不同，可能导致数据不一致的问题。

以如下 SQL 为例：

```sql
CREATE TABLE t (a INT PRIMARY KEY, b INT);
INSERT INTO t VALUES (1, 1);
UPDATE t SET a = 2 WHERE a = 1;
```

在上述示例中，主键 `a` 的值从 `1` 修改为 `2`。如果不将该 `UPDATE` 事件进行拆分：

* 在使用 CSV 和 AVRO 协议时，消费者仅能看到新值 `a = 2`，而无法得到旧值 `a = 1`。这可能导致下游消费者只插入了新值 `2`，而没有删除旧值 `1`。
* 在使用 Index value dispatcher 时，插入记录 `(1, 1)` 的事件可能被发送到 Partition 0，而变更事件 `(2, 1)` 可能被发送到 Partition 1。如果 Partition 1 的消费进度快于 Partition 0，则可能由于下游数据系统中找不到相应数据而导致出错。因此，TiCDC 会将该条 `UPDATE` 事件拆分为 `DELETE` 和 `INSERT` 两条事件，其中，删除记录 `(1, 1)` 被发送到 Partition 0，写入记录 `(2, 1)` 被发送到 Partition 1，以确保无论消费者的进度如何，事件都能被消费成功。

### 含有多条 `UPDATE` 变更的事务拆分

从 v6.5.4、v7.1.2 和 v7.4.0 开始，对于一个含有多条变更的事务，如果 `UPDATE` 事件的主键或者非空唯一索引的列值发生改变，TiCDC 会将该其拆分为 `DELETE` 和 `INSERT` 两条事件，并确保所有事件按照 `DELETE` 事件在 `INSERT` 事件之前的顺序进行排序。详情见 GitHub issue [#9430](https://github.com/pingcap/tiflow/issues/9430)。

该变更主要为了解决当使用 MySQL Sink 直接将这两条事件写入下游时，可能会出现主键或唯一键冲突的问题，从而导致 changefeed 报错。当使用 Kafka Sink 或其他 Sink 时，如果消费者需要将数据变更写入关系型数据库或进行类似操作，也可能遇到相同问题。

以如下 SQL 为例：

```sql
CREATE TABLE t (a INT PRIMARY KEY, b INT);
INSERT INTO t VALUES (1, 1);
INSERT INTO t VALUES (2, 2);

BEGIN;
UPDATE t SET a = 3 WHERE a = 1;
UPDATE t SET a = 1 WHERE a = 2;
UPDATE t SET a = 2 WHERE a = 3;
COMMIT;
```

在上述示例中，通过执行三条 SQL 语句对两行数据的主键进行交换，但 TiCDC 只会接收到两条 `UPDATE` 变更事件，即将主键 `a` 从 `1` 变更为 `2`，将主键 `a` 从 `2` 变更为 `1`，如果 MYSQL Sink 直接将这两条 `UPDATE` 事件写入下游，会出现主键冲突的问题，导致 changefeed 报错。

因此，TiCDC 会将这两条事件拆分为四条事件，即删除记录 `(1, 1)` 和 `(2, 2)` 以及写入记录 `(2, 1)` 和 `(1, 2)`。

### MySQL Sink

从 v7.5.2 开始，当使用 MySQL Sink 时，TiCDC 的任意节点在收到某张表的同步任务请求并开始向下游同步数据之前，会从 PD 获取当前的时间戳 `thresholdTS`，并根据时间戳的值决定是否拆分 `UPDATE` 事件：

- 对于含有单条或多条 `UPDATE` 变更的事务，如果该事务的 `commitTS` 小于 `thresholdTS`，在写入 Sorter 模块之前 TiCDC 会将每条 `UPDATE` 事件拆分为 `DELETE` 和 `INSERT` 两条事件。
- 对于事务的 `commitTS` 大于或等于 `thresholdTS` 的 `UPDATE` 事件，TiCDC 不会对其进行拆分。详情见 GitHub issue [#10918](https://github.com/pingcap/tiflow/issues/10918)。

该行为变更解决了由于 TiCDC 接收到的 `UPDATE` 事件顺序可能不正确，导致拆分后的 `DELETE` 和 `INSERT` 事件顺序也可能不正确，从而引发下游数据不一致的问题。

以如下 SQL 为例：

```sql
CREATE TABLE t (a INT PRIMARY KEY, b INT);
INSERT INTO t VALUES (1, 1);
INSERT INTO t VALUES (2, 2);

BEGIN;
UPDATE t SET a = 3 WHERE a = 2;
UPDATE t SET a = 2 WHERE a = 1;
COMMIT;
```

在该示例中，事务内的两条 `UPDATE` 语句的执行顺序有先后依赖关系，即先将主键 `a` 从 `2` 变更为 `3`，再将主键 `a` 从 `1` 变更为 `2`。执行完该事务后，上游数据库内的记录为 `(2, 1)` 和 `(3, 2)`。

但 TiCDC 内部收到的 `UPDATE` 事件顺序可能与上游事务内部实际的执行顺序不同，例如：

```sql
UPDATE t SET a = 2 WHERE a = 1;
UPDATE t SET a = 3 WHERE a = 2;
```

- 在引入该行为变更之前，TiCDC 会将这些 `UPDATE` 事件写入 Sorter 模块之后再将其拆分为 `DELETE` 和 `INSERT` 事件。拆分后下游实际执行的事件顺序如下：

    ```sql
    BEGIN;
    DELETE FROM t WHERE a = 1;
    REPLACE INTO t VALUES (2, 1);
    DELETE FROM t WHERE a = 2;
    REPLACE INTO t VALUES (3, 2);
    COMMIT;
    ```

    下游执行完该事务后，数据库内的记录为 `(3, 2)`，与上游数据库的记录（即 `(2, 1)` 和 `(3, 2)`）不同，即发生了数据不一致问题。

- 在引入该行为变更之后，如果该事务的 `commitTS` 小于对应表开始向下游同步数据时 TiCDC 获取的 `thresholdTS`，TiCDC 会在这些 `UPDATE` 事件写入 Sorter 模块之前将其拆分为 `DELETE` 和 `INSERT` 事件，经过 Sorter 排序后下游实际执行的事件顺序如下：

    ```sql
    BEGIN;
    DELETE FROM t WHERE a = 1;
    DELETE FROM t WHERE a = 2;
    REPLACE INTO t VALUES (2, 1);
    REPLACE INTO t VALUES (3, 2);
    COMMIT;
    ```

    下游执行完该事务后，下游数据库内的记录和上游数据库一样，都为 `(2, 1)` 和 `(3, 2)`，保证了数据一致性。

从该示例中可以看到，在写入 Sorter 模块之前将 `UPDATE` 事件拆分为 `DELETE` 和 `INSERT` 事件，可以保证拆分后所有的 `DELETE` 事件都在 `INSERT` 事件之前执行，这样无论 TiCDC 收到的 `UPDATE` 事件顺序，均可以保证数据一致性。

> **注意：**
>
> 该行为变更后，在使用 MySQL Sink 时，TiCDC 在大部分情况下都不会拆分 `UPDATE` 事件，因此 changefeed 在运行时可能会出现主键或唯一键冲突的问题。该问题会导致 changefeed 自动重启，重启后发生冲突的 `UPDATE` 事件会被拆分为 `DELETE` 和 `INSERT` 事件并写入 Sorter 模块中，此时可以确保同一事务内所有事件按照 `DELETE` 事件在 `INSERT` 事件之前的顺序进行排序，从而正确完成数据同步。
