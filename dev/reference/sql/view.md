---
title: 视图
category: reference
---

# 视图

TiDB 支持视图，视图是一张虚拟表，该虚拟表的结构由创建视图时的 `SELECT` 语句定义。使用视图一方面可以对用户只暴露安全的字段及数据，进而保证底层表的敏感字段及数据的安全。另一方面，将频繁出现的复杂查询定义为视图，可以使复杂查询更加简单便捷。

## 查询视图

查询一个视图和查询一张普通表类似。但是 TiDB 在真正执行查询视图时，会将视图展开成创建视图时定义的 `SELECT` 语句，进而执行展开后的查询语句。

## 样例

以下例子将创建一个视图，并在该视图上进行查询，最后删除该视图。

```sql
tidb> create table t(a int, b int);
Query OK, 0 rows affected (0.01 sec)

tidb> insert into t values(1, 1),(2,2),(3,3);
Query OK, 3 rows affected (0.00 sec)
Records: 3  Duplicates: 0  Warnings: 0

tidb> create table s(a int);
Query OK, 0 rows affected (0.01 sec)

tidb> insert into s values(2),(3);
Query OK, 2 rows affected (0.01 sec)
Records: 2  Duplicates: 0  Warnings: 0

tidb> create view v as select s.a from t left join s on t.a = s.a;
Query OK, 0 rows affected (0.01 sec)

tidb> select * from v;
+------+
| a    |
+------+
| NULL |
|    2 |
|    3 |
+------+
3 rows in set (0.00 sec)

tidb> drop view v;
Query OK, 0 rows affected (0.02 sec)
```

## 局限性

目前 TiDB 中的视图有以下局限性：

- 不支持物化视图。
- TiDB 中视图为只读视图，不支持对视图进行 `UPDATE`、`INSERT`、`DELETE` 等写入操作。
- 对已创建的视图仅支持一种 DDL 操作，即 `DROP [VIEW | TABLE]`。

## 扩展阅读

- [创建试图](/reference/sql/statements/create-view.md)
- [删除视图](/reference/sql/statements/drop-view.md)
