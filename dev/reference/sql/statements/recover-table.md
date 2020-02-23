---
title: RECOVER TABLE
category: reference
---

# RECOVER TABLE

`RECOVER TABLE` 的功能是恢复被删除的表及其数据。在 `DROP TABLE` 后，在 GC life time 时间内，可以用 `RECOVER TABLE` 语句恢复被删除的表以及其数据。

## 语法

{{< copyable "sql" >}}

```sql
RECOVER TABLE table_name
```

{{< copyable "sql" >}}

```sql
RECOVER TABLE BY JOB ddl_job_id
```

## 注意事项

如果删除表后并过了 GC lifetime，就不能再用 `RECOVER TABLE` 来恢复被删除的表了，执行 `RECOVER TABLE` 语句会返回类似错误：`snapshot is older than GC safe point 2019-07-10 13:45:57 +0800 CST`。

对于 3.0.0 及之后的 TiDB 版本，不推荐在使用 TiDB Binlog 的情况下使用 `RECOVER TABLE` 功能。

TiDB Binlog 在 3.0.1 支持 `RECOVER TABLE` 后，可在下面的情况下使用 `RECOVER TABLE`：

* 3.0.1+ 版本的 TiDB Binlog
* 主从集群都使用 TiDB 3.0
* 从集群 GC lifetime 一定要长于主集群（不过由于上下游同步的延迟，可能也会造成下游 recover 失败）

### TiDB Binlog 同步错误处理

当使用 TiDB Binlog 同步工具时，上游 TiDB 使用 `RECOVER TABLE` 后，TiDB Binlog 可能会因为下面几个原因造成同步中断：

* 下游数据库不支持 `RECOVER TABLE` 语句。类似错误：`check the manual that corresponds to your MySQL server version for the right syntax to use near 'RECOVER TABLE table_name'`。

* 上下游数据库的 GC lifetime 不一样。类似错误：`snapshot is older than GC safe point 2019-07-10 13:45:57 +0800 CST`。

* 上下游数据库的同步延迟。类似错误：`snapshot is older than GC safe point 2019-07-10 13:45:57 +0800 CST`。

只能通过重新[全量导入被删除的表](/dev/how-to/migrate/overview.md#mysql-数据的全量迁移)来恢复 TiDB Binlog 的数据同步。

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

    根据表名恢复被删除的表需满足以下条件：

    - 最近 DDL JOB 历史中找到的第一个 `DROP TABLE` 操作，且
    - `DROP TABLE` 所删除的表的名称与 `RECOVER TABLE` 语句指定表名相同

- 根据删除表时的 DDL JOB ID 恢复被删除的表。

    如果第一次删除表 t 后，又新建了一个表 t，然后又把新建的表 t 删除了，此时如果想恢复最开始删除的表 t, 就需要用到指定 DDL JOB ID 的语法了。

    {{< copyable "sql" >}}

    ```sql
    DROP TABLE t;
    ```

    {{< copyable "sql" >}}

    ```sql
    ADMIN SHOW DDL JOBS 1;
    ```

    上面这个语句用来查找删除表 t 时的 DDL JOB ID，这里是 53：

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

    根据删除表时的 DDL JOB ID 恢复被删除的表，会直接用 DDL JOB ID 找到被删除表进行恢复。如果指定的 DDL JOB ID 的 DDL JOB 不是 `DROP TABLE` 类型，会报错。

## 原理

TiDB 在删除表时，实际上只删除了表的元信息，并将需要删除的表数据（行数据和索引数据）写一条数据到 `mysql.gc_delete_range` 表。TiDB 后台的 GC Worker 会定期从 `mysql.gc_delete_range` 表中取出超过 GC lifetime 相关范围的 key 进行删除。

所以，RECOVER TABLE 只需要在 GC Worker 还没删除表数据前，恢复表的元信息并删除 `mysql.gc_delete_range` 表中相应的行记录就可以了。恢复表的元信息可以用 TiDB 的快照读实现。具体的快照读内容可以参考[读取历史数据](/dev/how-to/get-started/read-historical-data.md)文档。

TiDB 中表的恢复是通过快照读获取表的元信息后，再走一次类似于 `CREATE TABLE` 的建表流程，所以 `RECOVER TABLE` 实际上也是一种 DDL。
