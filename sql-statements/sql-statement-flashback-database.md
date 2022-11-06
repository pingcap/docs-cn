---
title: FLASHBACK DATABASE
summary: TiDB 数据库中 FLASHBACK DATABASE 的使用概况。
---

# FLASHBACK TABLE

在 TiDB 6.4 中，引入了 `FLASHBACK TABLE` 语法，其功能是在 Garbage Collection (GC) life time 时间内，可以用 `FLASHBACK DATABASE` 语句来恢复被 `DROP` 删除的数据库以及数据。

可以使用系统变量 [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-从-v50-版本开始引入) 配置数据的历史版本的保留时间（默认值是 `10m0s`）。可以使用以下 SQL 语句查询当前的 `safePoint`，即 GC 已经清理到的时间点：

{{< copyable "sql" >}}

  ```sql
  SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point';
  ```

只要被 `DROP` 数据库是在 `tikv_gc_safe_point` 时间之后，都能用 `FLASHBACK DATABASE` 语法来恢复。

## 语法

{{< copyable "sql" >}}

```sql
FLASHBACK DATABASE DBName [TO newDBName]
```

### 语法图

```ebnf+diagram
FlashbackDatabaseStmt ::=
    'FLASHBACK' DatabaseSym DBName FlashbackToNewName

FlashbackToNewName ::=
    ( 'TO' Identifier )?
```

## 注意事项

如果删除了一个数据库并过了 GC lifetime，就不能再用 `FLASHBACK DATABASE` 语句来恢复被删除的数据了，否则会返回错误，错误类似于 `ERROR 1105 (HY000): Can't find dropped database 'test' in GC safe point 2022-11-06 16:10:10 +0800 CST`。

不能用 `FLASHBACK DATABASE` 多次恢复同一个被删除的数据库，因为 `FLASHBACK DATABASE` 所恢复数据库的 schema ID 还是被删除数据库的 schema ID，而 TiDB 要求所有还存在的数据库 schema ID 必须全局唯一。

在开启 TiDB Binlog 时使用 `FLASHBACK DATABASE` 需要注意以下情况：

* 下游从集群也支持 `FLASHBACK DATABASE`
* 从集群的 GC lifetime 一定要长于主集群的 GC lifetime。上下游同步存在的延迟可能也会造成下游恢复数据失败。

如果 Binlog 同步出错，则需要在 Binlog 过滤掉该数据库，同时手动全量重新导入该数据库的数据。

## 示例

- 恢复被 `DROP` 删除的 `test` 数据库：

    {{< copyable "sql" >}}

    ```sql
    DROP DATABASE test;
    ```

    {{< copyable "sql" >}}

    ```sql
    FLASHBACK DATABASE test;
    ```

- 恢复被 `DROP` 删除的 `test` 数据库并重命名为 `test1`：

    {{< copyable "sql" >}}

    ```sql
    DROP DATABASE test;
    ```

    {{< copyable "sql" >}}

    ```sql
    FLASHBACK DATABASE test to test1;
    ```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。
