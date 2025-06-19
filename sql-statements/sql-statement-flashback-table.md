---
title: FLASHBACK TABLE
summary: 了解如何使用 `FLASHBACK TABLE` 语句恢复表。
---

# FLASHBACK TABLE

`FLASHBACK TABLE` 语法自 TiDB 4.0 引入。你可以使用 `FLASHBACK TABLE` 语句在垃圾回收（GC）生命周期内恢复被 `DROP` 或 `TRUNCATE` 操作删除的表和数据。

系统变量 [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)（默认值：`10m0s`）定义了行的早期版本的保留时间。可以通过以下查询获取垃圾回收已执行到的当前 `safePoint`：

{{< copyable "sql" >}}

```sql
SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point';
```

只要表是在 `tikv_gc_safe_point` 时间之后被 `DROP` 或 `TRUNCATE` 语句删除的，你就可以使用 `FLASHBACK TABLE` 语句恢复该表。

## 语法

{{< copyable "sql" >}}

```sql
FLASHBACK TABLE table_name [TO other_table_name]
```

## 语法图

```ebnf+diagram
FlashbackTableStmt ::=
    'FLASHBACK' 'TABLE' TableName FlashbackToNewName

TableName ::=
    Identifier ( '.' Identifier )?

FlashbackToNewName ::=
    ( 'TO' Identifier )?
```

## 注意事项

如果表被删除且 GC 生命周期已过，则无法再使用 `FLASHBACK TABLE` 语句恢复已删除的数据。否则，将返回类似 `Can't find dropped / truncated table 't' in GC safe point 2020-03-16 16:34:52 +0800 CST` 的错误。

当启用 TiDB Binlog 并使用 `FLASHBACK TABLE` 语句时，请注意以下条件和要求：

* 下游从集群也必须支持 `FLASHBACK TABLE`。
* 从集群的 GC 生命周期必须长于主集群。
* 上下游之间的复制延迟也可能导致无法将数据恢复到下游。
* 如果 TiDB Binlog 在复制表时发生错误，你需要在 TiDB Binlog 中过滤该表，并手动导入该表的所有数据。

## 示例

- 恢复被 `DROP` 操作删除的表数据：

    {{< copyable "sql" >}}

    ```sql
    DROP TABLE t;
    ```

    {{< copyable "sql" >}}

    ```sql
    FLASHBACK TABLE t;
    ```

- 恢复被 `TRUNCATE` 操作删除的表数据。由于被截断的表 `t` 仍然存在，你需要将要恢复的表 `t` 重命名。否则，由于表 `t` 已存在，将返回错误。

    {{< copyable "sql" >}}

    ```sql
    TRUNCATE TABLE t;
    ```

    {{< copyable "sql" >}}

    ```sql
    FLASHBACK TABLE t TO t1;
    ```

## 实现原理

删除表时，TiDB 只删除表元数据，并将要删除的表数据（行数据和索引数据）写入 `mysql.gc_delete_range` 表。TiDB 后台的 GC Worker 会定期从 `mysql.gc_delete_range` 表中删除超过 GC 生命周期的键。

因此，要恢复表，你只需要在 GC Worker 删除表数据之前恢复表元数据并删除 `mysql.gc_delete_range` 表中的相应行记录。你可以使用 TiDB 的快照读取来恢复表元数据。有关快照读取的详细信息，请参阅[读取历史数据](/read-historical-data.md)。

以下是 `FLASHBACK TABLE t TO t1` 的工作过程：

1. TiDB 搜索最近的 DDL 历史作业，并定位表 `t` 上第一个 `DROP TABLE` 或 `truncate table` 类型的 DDL 操作。如果 TiDB 无法定位到一个，则返回错误。
2. TiDB 检查 DDL 作业的开始时间是否在 `tikv_gc_safe_point` 之前。如果在 `tikv_gc_safe_point` 之前，则表示被 `DROP` 或 `TRUNCATE` 操作删除的表已被 GC 清理，并返回错误。
3. TiDB 使用 DDL 作业的开始时间作为快照来读取历史数据和读取表元数据。
4. TiDB 删除 `mysql.gc_delete_range` 中与表 `t` 相关的 GC 任务。
5. TiDB 将表元数据中的 `name` 更改为 `t1`，并使用此元数据创建新表。请注意，只更改表名而不更改表 ID。表 ID 与之前删除的表 `t` 的 ID 相同。

从上述过程可以看出，TiDB 始终对表的元数据进行操作，而表的用户数据从未被修改。恢复的表 `t1` 与之前删除的表 `t` 具有相同的 ID，因此 `t1` 可以读取 `t` 的用户数据。

> **注意：**
>
> 你不能使用 `FLASHBACK` 语句多次恢复同一个已删除的表，因为恢复的表的 ID 与已删除表的 ID 相同，而 TiDB 要求所有现有表必须具有全局唯一的表 ID。

`FLASHBACK TABLE` 操作是通过 TiDB 通过快照读取获取表元数据，然后经过类似于 `CREATE TABLE` 的表创建过程来完成的。因此，`FLASHBACK TABLE` 本质上是一种 DDL 操作。

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。
