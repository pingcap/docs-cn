---
title: FLASHBACK DATABASE
summary: 了解在 TiDB 数据库中 FLASHBACK DATABASE 的用法。
---

# FLASHBACK DATABASE

TiDB v6.4.0 引入了 `FLASHBACK DATABASE` 语法。你可以使用 `FLASHBACK DATABASE` 来恢复在垃圾回收（GC）生命周期内被 `DROP` 语句删除的数据库及其数据。

你可以通过配置 [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) 系统变量来设置历史数据的保留时间。默认值为 `10m0s`。你可以使用以下 SQL 语句查询当前的 `safePoint`（即 GC 已执行到的时间点）：

```sql
SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point';
```

只要数据库是在 `tikv_gc_safe_point` 时间之后被 `DROP` 删除的，你就可以使用 `FLASHBACK DATABASE` 来恢复该数据库。

## 语法

```sql
FLASHBACK DATABASE DBName [TO newDBName]
```

### 语法概要

```ebnf+diagram
FlashbackDatabaseStmt ::=
    'FLASHBACK' DatabaseSym DBName FlashbackToNewName
FlashbackToNewName ::=
    ( 'TO' Identifier )?
```

## 注意事项

* 如果数据库是在 `tikv_gc_safe_point` 时间之前删除的，你将无法使用 `FLASHBACK DATABASE` 语句恢复数据。`FLASHBACK DATABASE` 语句会返回类似 `ERROR 1105 (HY000): Can't find dropped database 'test' in GC safe point 2022-11-06 16:10:10 +0800 CST` 的错误。

* 你不能使用 `FLASHBACK DATABASE` 语句多次恢复同一个数据库。因为通过 `FLASHBACK DATABASE` 恢复的数据库与原始数据库具有相同的 schema ID，多次恢复同一个数据库会导致 schema ID 重复。在 TiDB 中，数据库 schema ID 必须全局唯一。

* 当启用 TiDB Binlog 时，使用 `FLASHBACK DATABASE` 时需要注意以下几点：

    * 下游从库必须支持 `FLASHBACK DATABASE`。
    * 从库的 GC 生命周期必须长于主库。否则，上下游之间的延迟可能会导致下游数据恢复失败。
    * 如果 TiDB Binlog 复制遇到错误，你需要在 TiDB Binlog 中过滤掉该数据库，然后手动为该数据库导入完整数据。

## 示例

- 恢复被 `DROP` 删除的 `test` 数据库：

    ```sql
    DROP DATABASE test;
    ```

    ```sql
    FLASHBACK DATABASE test;
    ```

- 恢复被 `DROP` 删除的 `test` 数据库，并将其重命名为 `test1`：

    ```sql
    DROP DATABASE test;
    ```

    ```sql
    FLASHBACK DATABASE test TO test1;
    ```

## MySQL 兼容性

此语句是 TiDB 对 MySQL 语法的扩展。
