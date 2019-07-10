---
title: RECOVER TABLE
category: reference
---

# RECOVER TABLE

RECOVER TABLE 的功能是恢复被删除的表及其数据。在 DROP TABLE 后，在 GC life time 时间内，可以用 RECOVER TABLE 语句恢复被删除的表以及其数据。

## 语法

{{< copyable "sql" >}}

```sql
RECOVER TABLE table_name
```

{{< copyable "sql" >}}

```sql
RECOVER TABLE BY JOB ddl_job_id
```

## 示例

- 根据表名恢复被删除的表。

    {{< copyable "sql" >}}

    ```sql
    DROP TABLE t;
    ```

    {{< copyable "sql" >}}

    ```sql
    RECOVER TABLE t;
    ```

    根据表名恢复被删除的表，会找到最近历史 DDL JOB 中的第一个是 DROP TABLE 类型的 DDL 且 DROP TABLE 的表名等于 RECOVER TABLE 语句中指定的表名的表进行恢复。

- 根据删除表时的 DDL JOB ID 恢复被删除的表。

    {{< copyable "sql" >}}

    ```sql
    DROP TABLE t;
    ```

    {{< copyable "sql" >}}

    ```sql
    ADMIN SHOW DDL JOBS 1; -- 查找删除表 t 时的 DDL JOB ID，这里是 53。
    ```

    ```
    +--------+---------+------------+------------+--------------+-----------+----------+-----------+-----------------------------------+--------+
    | JOB_ID | DB_NAME | TABLE_NAME | JOB_TYPE   | SCHEMA_STATE | SCHEMA_ID | TABLE_ID | ROW_COUNT | START_TIME                        | STATE  |
    +--------+---------+------------+------------+--------------+-----------+----------+-----------+-----------------------------------+--------+
    | 53     | test    |            | drop table | none         | 1         | 41       | 0         | 2019-07-10 13:23:18.277 +0800 CST | synced |
    +--------+---------+------------+------------+--------------+-----------+----------+-----------+-----------------------------------+--------+
    ```

    {{< copyable "sql" >}}

    ```sql
    RECOVER TABLE BY JOB 53;
    ```

    根据删除表时的 DDL JOB ID 恢复被删除的表，会直接用 DDL JOB ID 找到被删除表进行恢复。如果指定的 DDL JOB ID 的 DDL JOB 不是 DROP TABLE 类型，会报错。

## 原理

TiDB 在删除表时，实际上只删除了表的元信息，并将需要删除的表数据（行数据和索引数据）写一条数据到 `mysql.gc_delete_range` 表。TiDB 后台的 GC Worker 会定期从 `mysql.gc_delete_range` 表中取出超过 GC life time 相关范围的 key 进行删除。

所以，RECOVER TABLE 只需要在 GC Worker 还没删除表数据前，恢复表的元信息并删除 `mysql.gc_delete_range` 表中相应的行记录就可以了。恢复表的元信息可以用 TiDB 的快照读实现。具体的快照读内容可以参考 [读取历史数据](/how-to/get-started/read-historical-data.md) 文档。

恢复表的元信息是通过快照读获取表的元信息后，再走一次类似于 CREATE TABLE 的建表流程，所以 RECOVER TABLE 实际上也是一种 DDL。

> **注意：**
>
> 如果删除表后并过了 GC life time，就不能再用 RECOVER TABLE 来恢复被删除的表了，执行 RECOVER TABLE 语句会返回类似错误：`snapshot is older than GC safe point 2019-07-10 13:45:57 +0800 CST`。

## 注意事项

如果 TiDB 有用类似 Binlog 的同步工具，上游 TiDB 使用 RECOVER TABLE 后，经过 Binlog 同步后下游可能会失败导致同步失败，失败可能有以下几个原因：

* 下游数据库不支持 RECOVER TABLE 语句。

* 上下游数据库的 GC life time 不一样。

* 上下游数据库的同步延迟。
