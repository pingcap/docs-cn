---
title: 视图
aliases: ['/docs-cn/dev/views/','/docs-cn/dev/reference/sql/view/']
---

# 视图

TiDB 支持视图，视图是一张虚拟表，该虚拟表的结构由创建视图时的 `SELECT` 语句定义。使用视图一方面可以对用户只暴露安全的字段及数据，进而保证底层表的敏感字段及数据的安全。另一方面，将频繁出现的复杂查询定义为视图，可以使复杂查询更加简单便捷。

## 查询视图

查询一个视图和查询一张普通表类似。但是 TiDB 在真正执行查询视图时，会将视图展开成创建视图时定义的 `SELECT` 语句，进而执行展开后的查询语句。

## 查看视图的相关信息

通过以下方式，可以查看 view 相关的信息。

### 使用 `SHOW CREATE TABLE view_name` 或 `SHOW CREATE VIEW view_name` 语句

示例：

{{< copyable "sql" >}}

```sql
show create view v;
```

使用该语句可以查看 view 对应的创建语句，及创建 view 时对应的 `character_set_client` 及 `collation_connection` 系统变量值。

```sql
+------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------+----------------------+
| View | Create View                                                                                                                                                         | character_set_client | collation_connection |
+------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------+----------------------+
| v    | CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`127.0.0.1` SQL SECURITY DEFINER VIEW `v` (`a`) AS SELECT `s`.`a` FROM `test`.`t` LEFT JOIN `test`.`s` ON `t`.`a`=`s`.`a` | utf8                 | utf8_general_ci      |
+------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------+----------------------+
1 row in set (0.00 sec)
```

### 查询 `INFORMATION_SCHEMA.VIEWS` 表

示例：

{{< copyable "sql" >}}

```sql
select * from information_schema.views;
```

通过查询该表可以查看 view 的相关元信息，如 `TABLE_CATALOG`、`TABLE_SCHEMA`、`TABLE_NAME`、`VIEW_DEFINITION`、`CHECK_OPTION`、`IS_UPDATABLE`、`DEFINER`、`SECURITY_TYPE`、`CHARACTER_SET_CLIENT`、`COLLATION_CONNECTION` 等。

```sql
+---------------+--------------+------------+------------------------------------------------------------------------+--------------+--------------+----------------+---------------+----------------------+----------------------+
| TABLE_CATALOG | TABLE_SCHEMA | TABLE_NAME | VIEW_DEFINITION                                                        | CHECK_OPTION | IS_UPDATABLE | DEFINER        | SECURITY_TYPE | CHARACTER_SET_CLIENT | COLLATION_CONNECTION |
+---------------+--------------+------------+------------------------------------------------------------------------+--------------+--------------+----------------+---------------+----------------------+----------------------+
| def           | test         | v          | SELECT `s`.`a` FROM `test`.`t` LEFT JOIN `test`.`s` ON `t`.`a`=`s`.`a` | CASCADED     | NO           | root@127.0.0.1 | DEFINER       | utf8                 | utf8_general_ci      |
+---------------+--------------+------------+------------------------------------------------------------------------+--------------+--------------+----------------+---------------+----------------------+----------------------+
1 row in set (0.00 sec)
```

### 查询 HTTP API

示例：

{{< copyable "" >}}

```
curl http://127.0.0.1:10080/schema/test/v
```

通过访问 `http://{TiDBIP}:10080/schema/{db}/{view}` 可以得到对应 view 的所有元信息。

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

以下例子将创建一个视图，并在该视图上进行查询，最后删除该视图。

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

## 局限性

目前 TiDB 中的视图有以下局限性：

- 不支持物化视图。
- TiDB 中视图为只读视图，不支持对视图进行 `UPDATE`、`INSERT`、`DELETE`、`TRUNCATE` 等写入操作。
- 对已创建的视图仅支持 `DROP` 的 DDL 操作，即 `DROP [VIEW | TABLE]`。

## 扩展阅读

- [创建视图](/sql-statements/sql-statement-create-view.md)
- [删除视图](/sql-statements/sql-statement-drop-view.md)
