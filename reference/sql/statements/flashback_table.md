---
title: FLASHBACK TABLE
category: reference
---

# FLASHBACK TABLE

在 Garbage Collection (GC) life time 时间内（参阅 [`tikv_gc_life_time`](/reference/garbage-collection/configuration/#tikv_gc_life_time)），可以用 `FLASHBACK TABLE` 语句来恢复被 `DROP` 或 `TRUNCATE` 删除的表以及数据。

## 语法

{{< copyable "sql" >}}

```sql
FLASHBACK TABLE table_name [TO other_table_name]
```

## 注意事项

如果删除了一张表并过了 GC life time，就不能再用 `FLASHBACK TABLE` 语句来恢复被删除的数据了，否则会返回错误，错误类似于 `snapshot is older than GC safe point 2020-02-27 13:45:57 +0800 CST`。

在开启 TiDB Binlog 时使用 `FLASHBACK TABLE` 需要注意一下情况：

* 下游从集群也支持 `FLASHBACK TABLE`
* 从集群 GC lifetime 一定要长于主集群（不过由于上下游同步的延迟，可能也会造成下游恢复数据失败）

## 示例

- 恢复被 `DROP` 的表数据。

    {{< copyable "sql" >}}

    ```sql
    DROP TABLE t;
    ```

    {{< copyable "sql" >}}

    ```sql
    FLASHBACK TABLE t;
    ```

- 恢复被 `TRUNCATE` 的表数据，由于被 `TRUNCATE` 的表还存在，所以需要重命名被恢复的表，否则会报错表 t 已存在。

    ```sql
    TRUNCATE TABLE t;
    ```

    {{< copyable "sql" >}}

    ```sql
    FLASHBACK TABLE t TO t1;
    ```

## 原理

TiDB 在删除表时，实际上只删除了表的元信息，并将需要删除的表数据（行数据和索引数据）写一条数据到 `mysql.gc_delete_range` 表。TiDB 后台的 GC Worker 会定期从 `mysql.gc_delete_range` 表中取出超过 GC lifetime 相关范围的 key 进行删除。

所以，`FLASHBACK TABLE` 只需要在 GC Worker 还没删除表数据前，恢复表的元信息并删除 `mysql.gc_delete_range` 表中相应的行记录就可以了。恢复表的元信息可以用 TiDB 的快照读实现。具体的快照读内容可以参考[读取历史数据](/how-to/get-started/read-historical-data.md)文档。

TiDB 中表的恢复是通过快照读获取表的元信息后，再走一次类似于 `CREATE TABLE` 的建表流程，所以 `FLASHBACK TABLE` 实际上也是一种 DDL。
