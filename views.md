---
title: 视图
summary: 了解如何在 TiDB 中使用视图。
---

# 视图

TiDB 支持视图。视图作为一个虚拟表，其架构由创建视图的 `SELECT` 语句定义。使用视图具有以下优点：

- 仅向用户公开安全的字段和数据，确保底层表中存储的敏感字段和数据的安全性。
- 将经常出现的复杂查询定义为视图，使复杂查询更简单和方便。

## 查询视图

查询视图与查询普通表类似。但是，当 TiDB 查询视图时，它实际上是在查询与该视图关联的 `SELECT` 语句。

## 显示元数据

要获取视图的元数据，可以选择以下任一方法。

### 使用 `SHOW CREATE TABLE view_name` 或 `SHOW CREATE VIEW view_name` 语句

使用示例：

{{< copyable "sql" >}}

```sql
show create view v;
```

此语句显示与此视图对应的 `CREATE VIEW` 语句，以及创建视图时 `character_set_client` 和 `collation_connection` 系统变量的值。

```sql
+------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------+----------------------+
| View | Create View                                                                                                                                                         | character_set_client | collation_connection |
+------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------+----------------------+
| v    | CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`127.0.0.1` SQL SECURITY DEFINER VIEW `v` (`a`) AS SELECT `s`.`a` FROM `test`.`t` LEFT JOIN `test`.`s` ON `t`.`a`=`s`.`a` | utf8                 | utf8_general_ci      |
+------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------+----------------------+
1 row in set (0.00 sec)
```

### 查询 `INFORMATION_SCHEMA.VIEWS` 表

使用示例：

{{< copyable "sql" >}}

```sql
select * from information_schema.views;
```

通过查询此表，你可以查看视图的相关元信息，如 `TABLE_CATALOG`、`TABLE_SCHEMA`、`TABLE_NAME`、`VIEW_DEFINITION`、`CHECK_OPTION`、`IS_UPDATABLE`、`DEFINER`、`SECURITY_TYPE`、`CHARACTER_SET_CLIENT` 和 `COLLATION_CONNECTION`。

```sql
+---------------+--------------+------------+------------------------------------------------------------------------+--------------+--------------+----------------+---------------+----------------------+----------------------+
| TABLE_CATALOG | TABLE_SCHEMA | TABLE_NAME | VIEW_DEFINITION                                                        | CHECK_OPTION | IS_UPDATABLE | DEFINER        | SECURITY_TYPE | CHARACTER_SET_CLIENT | COLLATION_CONNECTION |
+---------------+--------------+------------+------------------------------------------------------------------------+--------------+--------------+----------------+---------------+----------------------+----------------------+
| def           | test         | v          | SELECT `s`.`a` FROM `test`.`t` LEFT JOIN `test`.`s` ON `t`.`a`=`s`.`a` | CASCADED     | NO           | root@127.0.0.1 | DEFINER       | utf8                 | utf8_general_ci      |
+---------------+--------------+------------+------------------------------------------------------------------------+--------------+--------------+----------------+---------------+----------------------+----------------------+
1 row in set (0.00 sec)
```

### 使用 HTTP API

使用示例：

{{< copyable "" >}}

```sql
curl http://127.0.0.1:10080/schema/test/v
```

通过访问 `http://{TiDBIP}:10080/schema/{db}/{view}`，你可以获取视图的所有元数据。

```
{
 "id": 122,
 "name": {
  "O": "v",
  "L": "v"
 },
 "charset": "utf8",
 "collate": "utf8_general_ci",
 "cols": [
  {
   "id": 1,
   "name": {
    "O": "a",
    "L": "a"
   },
   "offset": 0,
   "origin_default": null,
   "default": null,
   "default_bit": null,
   "default_is_expr": false,
   "generated_expr_string": "",
   "generated_stored": false,
   "dependences": null,
   "type": {
    "Tp": 0,
    "Flag": 0,
    "Flen": 0,
    "Decimal": 0,
    "Charset": "",
    "Collate": "",
    "Elems": null
   },
   "state": 5,
   "comment": "",
   "hidden": false,
   "version": 0
  }
 ],
 "index_info": null,
 "fk_info": null,
 "state": 5,
 "pk_is_handle": false,
 "is_common_handle": false,
 "comment": "",
 "auto_inc_id": 0,
 "auto_id_cache": 0,
 "auto_rand_id": 0,
 "max_col_id": 1,
 "max_idx_id": 0,
 "update_timestamp": 416801600091455490,
 "ShardRowIDBits": 0,
 "max_shard_row_id_bits": 0,
 "auto_random_bits": 0,
 "pre_split_regions": 0,
 "partition": null,
 "compression": "",
 "view": {
  "view_algorithm": 0,
  "view_definer": {
   "Username": "root",
   "Hostname": "127.0.0.1",
   "CurrentUser": false,
   "AuthUsername": "root",
   "AuthHostname": "%"
  },
  "view_security": 0,
  "view_select": "SELECT `s`.`a` FROM `test`.`t` LEFT JOIN `test`.`s` ON `t`.`a`=`s`.`a`",
  "view_checkoption": 1,
  "view_cols": null
 },
 "sequence": null,
 "Lock": null,
 "version": 3,
 "tiflash_replica": null
}
```

## 示例

以下示例创建一个视图，查询此视图，并删除此视图：

{{< copyable "sql" >}}

```sql
create table t(a int, b int);
```

```
Query OK, 0 rows affected (0.01 sec)
```

{{< copyable "sql" >}}

```sql
insert into t values(1, 1),(2,2),(3,3);
```

```
Query OK, 3 rows affected (0.00 sec)
Records: 3  Duplicates: 0  Warnings: 0
```

{{< copyable "sql" >}}

```sql
create table s(a int);
```

```
Query OK, 0 rows affected (0.01 sec)
```

{{< copyable "sql" >}}

```sql
insert into s values(2),(3);
```

```
Query OK, 2 rows affected (0.01 sec)
Records: 2  Duplicates: 0  Warnings: 0
```

{{< copyable "sql" >}}

```sql
create view v as select s.a from t left join s on t.a = s.a;
```

```
Query OK, 0 rows affected (0.01 sec)
```

{{< copyable "sql" >}}

```sql
select * from v;
```

```
+------+
| a    |
+------+
| NULL |
|    2 |
|    3 |
+------+
3 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
drop view v;
```

```
Query OK, 0 rows affected (0.02 sec)
```

## 限制

目前，TiDB 中的视图有以下限制：

* 尚不支持物化视图。
* TiDB 中的视图是只读的，不支持 `UPDATE`、`INSERT`、`DELETE` 和 `TRUNCATE` 等写操作。
* 对于已创建的视图，唯一支持的 DDL 操作是 `DROP [VIEW | TABLE]`

## 另请参阅

- [CREATE VIEW](/sql-statements/sql-statement-create-view.md)
- [DROP VIEW](/sql-statements/sql-statement-drop-view.md)
