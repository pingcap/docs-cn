---
title: RECOVER TABLE
summary: TiDB 数据库中 RECOVER TABLE 的使用概述。
---

# RECOVER TABLE

`RECOVER TABLE` 用于在执行 `DROP TABLE` 语句后的 GC（垃圾回收）生命周期内恢复已删除的表及其数据。

## 语法

{{< copyable "sql" >}}

```sql
RECOVER TABLE table_name;
```

{{< copyable "sql" >}}

```sql
RECOVER TABLE BY JOB JOB_ID;
```

## 语法图

```ebnf+diagram
RecoverTableStmt ::=
    'RECOVER' 'TABLE' ( 'BY' 'JOB' Int64Num | TableName Int64Num? )

TableName ::=
    Identifier ( '.' Identifier )?

Int64Num ::= NUM

NUM ::= intLit
```

> **注意：**
>
> + 如果表被删除且超出了 GC 生命周期，则无法使用 `RECOVER TABLE` 恢复该表。在这种情况下执行 `RECOVER TABLE` 会返回类似以下的错误：`snapshot is older than GC safe point 2019-07-10 13:45:57 +0800 CST`。
>
> + 如果 TiDB 版本是 3.0.0 或更高版本，不建议在使用 TiDB Binlog 时使用 `RECOVER TABLE`。
>
> + `RECOVER TABLE` 在 Binlog 3.0.1 版本中得到支持，因此你可以在以下三种情况下使用 `RECOVER TABLE`：
>
>     - Binlog 版本为 3.0.1 或更高版本。
>     - 上游集群和下游集群都使用 TiDB 3.0。
>     - 从集群的 GC 生命周期必须长于主集群。但是，由于上下游数据库之间的数据复制存在延迟，下游的数据恢复可能会失败。

<CustomContent platform="tidb">

**TiDB Binlog 复制期间的错误排查**

当你在 TiDB Binlog 复制期间在上游 TiDB 中使用 `RECOVER TABLE` 时，TiDB Binlog 可能会在以下三种情况下中断：

+ 下游数据库不支持 `RECOVER TABLE` 语句。错误示例：`check the manual that corresponds to your MySQL server version for the right syntax to use near 'RECOVER TABLE table_name'`。

+ 上游数据库和下游数据库之间的 GC 生命周期不一致。错误示例：`snapshot is older than GC safe point 2019-07-10 13:45:57 +0800 CST`。

+ 上游和下游数据库之间的复制存在延迟。错误示例：`snapshot is older than GC safe point 2019-07-10 13:45:57 +0800 CST`。

对于上述三种情况，你可以通过[对已删除表进行完整导入](/ecosystem-tool-user-guide.md#backup-and-restore---backup--restore-br)来恢复 TiDB Binlog 的数据复制。

</CustomContent>

## 示例

+ 根据表名恢复已删除的表。

    {{< copyable "sql" >}}

    ```sql
    DROP TABLE t;
    ```

    {{< copyable "sql" >}}

    ```sql
    RECOVER TABLE t;
    ```

    此方法会搜索最近的 DDL 作业历史记录，并定位第一个 `DROP TABLE` 类型的 DDL 操作，然后恢复与 `RECOVER TABLE` 语句中指定的表名相同的已删除表。

+ 根据表的 `DDL JOB ID` 恢复已删除的表。

    假设你删除了表 `t` 并创建了另一个 `t`，然后又删除了新创建的 `t`。如果你想恢复第一次删除的 `t`，则必须使用指定 `DDL JOB ID` 的方法。

    {{< copyable "sql" >}}

    ```sql
    DROP TABLE t;
    ```

    {{< copyable "sql" >}}

    ```sql
    ADMIN SHOW DDL JOBS 1;
    ```

    上面的第二条语句用于搜索删除 `t` 的表的 `DDL JOB ID`。在下面的示例中，ID 为 `53`。

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

    此方法通过 `DDL JOB ID` 恢复已删除的表。如果相应的 DDL 作业不是 `DROP TABLE` 类型，则会发生错误。

## 实现原理

当删除表时，TiDB 只删除表元数据，并将要删除的表数据（行数据和索引数据）写入 `mysql.gc_delete_range` 表。TiDB 后台的 GC Worker 会定期从 `mysql.gc_delete_range` 表中删除超过 GC 生命周期的键。

因此，要恢复表，你只需要在 GC Worker 删除表数据之前恢复表元数据并删除 `mysql.gc_delete_range` 表中的相应行记录。你可以使用 TiDB 的快照读取来恢复表元数据。详情请参考[读取历史数据](/read-historical-data.md)。

表恢复是通过 TiDB 通过快照读取获取表元数据，然后经过类似于 `CREATE TABLE` 的表创建过程来完成的。因此，`RECOVER TABLE` 本质上是一种 DDL 操作。

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。
