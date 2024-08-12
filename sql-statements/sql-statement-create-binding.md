---
title: CREATE [GLOBAL|SESSION] BINDING
summary: TiDB 数据库中 CREATE [GLOBAL|SESSION] BINDING 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-create-binding/']
---

# CREATE [GLOBAL|SESSION] BINDING

`CREATE [GLOBAL|SESSION] BINDING` 语句用于在 TiDB 中创建新的执行计划绑定。绑定可用于将优化器 Hint 插入语句中，而无需更改底层查询。

`BINDING` 语句可以在 `GLOBAL` 或者 `SESSION` 作用域内创建执行计划绑定。在不指定作用域时，默认的作用域为 `SESSION`。

被绑定的 SQL 语句会被参数化后存储到系统表中。在处理 SQL 查询时，只要参数化后的 SQL 语句和系统表中某个被绑定的 SQL 语句一致，并且系统变量 `tidb_use_plan_baselines` 的值为 `ON`（其默认值为 `ON`），即可使用相应的优化器 Hint。如果存在多个可匹配的执行计划，优化器会从中选择代价最小的一个进行绑定。更多信息，请参考[创建绑定](/sql-plan-management.md#创建绑定)。

## 语法图

```ebnf+diagram
CreateBindingStmt ::=
    'CREATE' GlobalScope 'BINDING' ( 'FOR' BindableStmt 'USING' BindableStmt
|   'FROM' 'HISTORY' 'USING' 'PLAN' 'DIGEST' StringLiteralOrUserVariableList )

GlobalScope ::=
    ( 'GLOBAL' | 'SESSION' )?

BindableStmt ::=
    ( SelectStmt | UpdateStmt | InsertIntoStmt | ReplaceIntoStmt | DeleteStmt )

StringLiteralOrUserVariableList ::=
    ( StringLitOrUserVariable | StringLiteralOrUserVariableList ',' StringLitOrUserVariable )

StringLiteralOrUserVariable ::=
    ( stringLiteral | UserVariable )
```

## 示例

你可以根据 SQL 或历史执行计划创建绑定。

根据历史执行计划创建绑定时，你需要指定 Plan Digest，既可以通过字符串字面量来指定，也可以通过字符串类型的用户变量来指定。你可以通过指定多个 Plan Digest 来同时为多个语句创建绑定，此时你可以指定多个字符串，同时每个字符串也可以包含多个 digest，字符串之间和 digest 之间均需使用逗号隔开。

下面的示例演示如何根据 SQL 创建绑定。

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (
    id INT NOT NULL PRIMARY KEY auto_increment,
    b INT NOT NULL,
    pad VARBINARY(255),
    INDEX(b)
   );
Query OK, 0 rows affected (0.07 sec)

INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM dual;
Query OK, 1 row affected (0.01 sec)
Records: 1  Duplicates: 0  Warnings: 0

INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
Query OK, 1 row affected (0.00 sec)
Records: 1  Duplicates: 0  Warnings: 0

INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
Query OK, 8 rows affected (0.00 sec)
Records: 8  Duplicates: 0  Warnings: 0

INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
Query OK, 1000 rows affected (0.04 sec)
Records: 1000  Duplicates: 0  Warnings: 0

INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
Query OK, 100000 rows affected (1.74 sec)
Records: 100000  Duplicates: 0  Warnings: 0

INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
Query OK, 100000 rows affected (2.15 sec)
Records: 100000  Duplicates: 0  Warnings: 0

INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
Query OK, 100000 rows affected (2.64 sec)
Records: 100000  Duplicates: 0  Warnings: 0

SELECT SLEEP(1);
+----------+
| SLEEP(1) |
+----------+
|        0 |
+----------+
1 row in set (1.00 sec)

ANALYZE TABLE t1;
Query OK, 0 rows affected (1.33 sec)

EXPLAIN ANALYZE SELECT * FROM t1 WHERE b = 123;
+-------------------------------+---------+---------+-----------+----------------------+---------------------------------------------------------------------------+-----------------------------------+----------------+------+
| id                            | estRows | actRows | task      | access object        | execution info                                                            | operator info                     | memory         | disk |
+-------------------------------+---------+---------+-----------+----------------------+---------------------------------------------------------------------------+-----------------------------------+----------------+------+
| IndexLookUp_10                | 583.00  | 297     | root      |                      | time:10.545072ms, loops:2, rpc num: 1, rpc time:398.359µs, proc keys:297  |                                   | 109.1484375 KB | N/A  |
| ├─IndexRangeScan_8(Build)     | 583.00  | 297     | cop[tikv] | table:t1, index:b(b) | time:0s, loops:4                                                          | range:[123,123], keep order:false | N/A            | N/A  |
| └─TableRowIDScan_9(Probe)     | 583.00  | 297     | cop[tikv] | table:t1             | time:12ms, loops:4                                                        | keep order:false                  | N/A            | N/A  |
+-------------------------------+---------+---------+-----------+----------------------+---------------------------------------------------------------------------+-----------------------------------+----------------+------+
3 rows in set (0.02 sec)

CREATE SESSION BINDING FOR
    SELECT * FROM t1 WHERE b = 123
   USING
    SELECT * FROM t1 IGNORE INDEX (b) WHERE b = 123;
Query OK, 0 rows affected (0.00 sec)

EXPLAIN ANALYZE  SELECT * FROM t1 WHERE b = 123;
+-------------------------+-----------+---------+-----------+---------------+--------------------------------------------------------------------------------+--------------------+---------------+------+
| id                      | estRows   | actRows | task      | access object | execution info                                                                 | operator info      | memory        | disk |
+-------------------------+-----------+---------+-----------+---------------+--------------------------------------------------------------------------------+--------------------+---------------+------+
| TableReader_7           | 583.00    | 297     | root      |               | time:222.32506ms, loops:2, rpc num: 1, rpc time:222.078952ms, proc keys:301010 | data:Selection_6   | 88.6640625 KB | N/A  |
| └─Selection_6           | 583.00    | 297     | cop[tikv] |               | time:224ms, loops:298                                                          | eq(test.t1.b, 123) | N/A           | N/A  |
|   └─TableFullScan_5     | 301010.00 | 301010  | cop[tikv] | table:t1      | time:220ms, loops:298                                                          | keep order:false   | N/A           | N/A  |
+-------------------------+-----------+---------+-----------+---------------+--------------------------------------------------------------------------------+--------------------+---------------+------+
3 rows in set (0.22 sec)

SHOW SESSION BINDINGS\G
*************************** 1. row ***************************
Original_sql: select * from t1 where b = ?
    Bind_sql: SELECT * FROM t1 IGNORE INDEX (b) WHERE b = 123
  Default_db: test
      Status: using
 Create_time: 2020-05-22 14:38:03.456
 Update_time: 2020-05-22 14:38:03.456
     Charset: utf8mb4
   Collation: utf8mb4_0900_ai_ci
1 row in set (0.00 sec)

DROP SESSION BINDING FOR SELECT * FROM t1 WHERE b = 123;
Query OK, 0 rows affected (0.00 sec)

EXPLAIN ANALYZE  SELECT * FROM t1 WHERE b = 123;
+-------------------------------+---------+---------+-----------+----------------------+-------------------------------------------------------------------------+-----------------------------------+----------------+------+
| id                            | estRows | actRows | task      | access object        | execution info                                                          | operator info                     | memory         | disk |
+-------------------------------+---------+---------+-----------+----------------------+-------------------------------------------------------------------------+-----------------------------------+----------------+------+
| IndexLookUp_10                | 583.00  | 297     | root      |                      | time:5.31206ms, loops:2, rpc num: 1, rpc time:665.927µs, proc keys:297  |                                   | 109.1484375 KB | N/A  |
| ├─IndexRangeScan_8(Build)     | 583.00  | 297     | cop[tikv] | table:t1, index:b(b) | time:0s, loops:4                                                        | range:[123,123], keep order:false | N/A            | N/A  |
| └─TableRowIDScan_9(Probe)     | 583.00  | 297     | cop[tikv] | table:t1             | time:0s, loops:4                                                        | keep order:false                  | N/A            | N/A  |
+-------------------------------+---------+---------+-----------+----------------------+-------------------------------------------------------------------------+-----------------------------------+----------------+------+
3 rows in set (0.01 sec)
```

下面的示例演示如何根据历史执行计划创建绑定。

```sql
USE test;
CREATE TABLE t1(a INT, b INT, c INT, INDEX ia(a));
CREATE TABLE t2(a INT, b INT, c INT, INDEX ia(a));
INSERT INTO t1 SELECT * FROM t2 WHERE a = 1;
SELECT @@LAST_PLAN_FROM_BINDING;
UPDATE /*+ INL_JOIN(t2) */ t1, t2 SET t1.a = 1 WHERE t1.b = t2.a;
SELECT @@LAST_PLAN_FROM_BINDING;
DELETE /*+ HASH_JOIN(t1) */ t1 FROM t1 JOIN t2 WHERE t1.b = t2.a;
SELECT @@LAST_PLAN_FROM_BINDING;
SELECT * FROM t1 WHERE t1.a IN (SELECT a FROM t2);
SELECT @@LAST_PLAN_FROM_BINDING;
```

方法一：

```sql
SELECT query_sample_text, stmt_type, table_names, plan_digest FROM information_schema.statements_summary_history WHERE table_names LIKE '%test.t1%' AND stmt_type != 'CreateTable';
CREATE GLOBAL BINDING FROM HISTORY USING PLAN DIGEST 'e72819cf99932f63a548156dbf433adda60e10337e89dcaa8638b4caf16f64d8,c291edc36b2482738d3389d335f37efc76290be2930330fe5034c5f4c42eeb36,8dc146249484f4a6ab219bfe9effa6b7a18aeed3764d49b610da61ac347ab914,73b2dec866595688ea416675f88ccb3456eb8e7443a79cd816695b688e07ac6b';
```

方法二：

```sql
SELECT @digests:=GROUP_CONCAT(plan_digest) FROM information_schema.statements_summary_history WHERE table_names LIKE '%test.t1%' AND stmt_type != 'CreateTable';
CREATE GLOBAL BINDING FROM HISTORY USING PLAN DIGEST @digests;
```

```sql
SHOW GLOBAL BINDINGS;
INSERT INTO t1 SELECT * FROM t2 WHERE a = 1;
SELECT @@LAST_PLAN_FROM_BINDING;
UPDATE t1, t2 SET t1.a = 1 WHERE t1.b = t2.a;
SELECT @@LAST_PLAN_FROM_BINDING;
DELETE t1 FROM t1 JOIN t2 WHERE t1.b = t2.a;
SELECT @@LAST_PLAN_FROM_BINDING;
SELECT * FROM t1 WHERE t1.a IN (SELECT a FROM t2);
SELECT @@LAST_PLAN_FROM_BINDING;
```

```sql
> CREATE TABLE t1(a INT, b INT, c INT, INDEX ia(a));
Query OK, 0 rows affected (0.048 sec)

> CREATE TABLE t2(a INT, b INT, c INT, INDEX ia(a));
Query OK, 0 rows affected (0.035 sec)

> INSERT INTO t1 SELECT * FROM t2 WHERE a = 1;
Query OK, 0 rows affected (0.002 sec)
Records: 0  Duplicates: 0  Warnings: 0

> SELECT @@LAST_PLAN_FROM_BINDING;
+--------------------------+
| @@LAST_PLAN_FROM_BINDING |
+--------------------------+
|                        0 |
+--------------------------+
1 row in set (0.001 sec)

> UPDATE /*+ INL_JOIN(t2) */ t1, t2 SET t1.a = 1 WHERE t1.b = t2.a;
Query OK, 0 rows affected (0.005 sec)
Rows matched: 0  Changed: 0  Warnings: 0

> SELECT @@LAST_PLAN_FROM_BINDING;
+--------------------------+
| @@LAST_PLAN_FROM_BINDING |
+--------------------------+
|                        0 |
+--------------------------+
1 row in set (0.000 sec)

> DELETE /*+ HASH_JOIN(t1) */ t1 FROM t1 JOIN t2 WHERE t1.b = t2.a;
Query OK, 0 rows affected (0.003 sec)

> SELECT @@LAST_PLAN_FROM_BINDING;
+--------------------------+
| @@LAST_PLAN_FROM_BINDING |
+--------------------------+
|                        0 |
+--------------------------+
1 row in set (0.000 sec)

> SELECT * FROM t1 WHERE t1.a IN (SELECT a FROM t2);
Empty set (0.002 sec)

> SELECT @@LAST_PLAN_FROM_BINDING;
+--------------------------+
| @@LAST_PLAN_FROM_BINDING |
+--------------------------+
|                        0 |
+--------------------------+
1 row in set (0.001 sec)

> SELECT @digests:=GROUP_CONCAT(plan_digest) FROM information_schema.statements_summary_history WHERE table_names LIKE '%test.t1%' AND stmt_type != 'CreateTable';
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| @digests:=GROUP_CONCAT(plan_digest)                                                                                                                                                                                                                                 |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 73b2dec866595688ea416675f88ccb3456eb8e7443a79cd816695b688e07ac6b,8dc146249484f4a6ab219bfe9effa6b7a18aeed3764d49b610da61ac347ab914,c291edc36b2482738d3389d335f37efc76290be2930330fe5034c5f4c42eeb36,e72819cf99932f63a548156dbf433adda60e10337e89dcaa8638b4caf16f64d8 |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.001 sec)

> CREATE GLOBAL BINDING FROM HISTORY USING PLAN DIGEST @digests;
Query OK, 0 rows affected (0.060 sec)

> SHOW GLOBAL BINDINGS;
+----------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+-----------------+---------+------------------------------------------------------------------+------------------------------------------------------------------+
| Original_sql                                                                                 | Bind_sql                                                                                                                                                                                                                               | Default_db | Status  | Create_time             | Update_time             | Charset | Collation       | Source  | Sql_digest                                                       | Plan_digest                                                      |
+----------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+-----------------+---------+------------------------------------------------------------------+------------------------------------------------------------------+
| insert into `test` . `t1` select * from `test` . `t2` where `a` = ?                          | INSERT INTO `test`.`t1` SELECT /*+ use_index(@`sel_1` `test`.`t2` `ia`) no_order_index(@`sel_1` `test`.`t2` `ia`)*/ * FROM `test`.`t2` WHERE `a` = 1                                                                                   | test       | enabled | 2024-08-11 05:27:19.669 | 2024-08-11 05:27:19.669 | utf8    | utf8_general_ci | history | bd23e6af17e7b77b25383e50e258f0dece18583d19772f08caacb2021945a300 | e72819cf99932f63a548156dbf433adda60e10337e89dcaa8638b4caf16f64d8 |
| update ( `test` . `t1` ) join `test` . `t2` set `t1` . `a` = ? where `t1` . `b` = `t2` . `a` | UPDATE /*+ inl_join(`test`.`t2`) use_index(@`upd_1` `test`.`t1` ) use_index(@`upd_1` `test`.`t2` `ia`) no_order_index(@`upd_1` `test`.`t2` `ia`)*/ (`test`.`t1`) JOIN `test`.`t2` SET `t1`.`a`=1 WHERE `t1`.`b` = `t2`.`a`             | test       | enabled | 2024-08-11 05:27:19.667 | 2024-08-11 05:27:19.667 | utf8    | utf8_general_ci | history | 987e91af17eb40e36fecfc0634cce0b6a736de02bb009091810f932804fc02e9 | c291edc36b2482738d3389d335f37efc76290be2930330fe5034c5f4c42eeb36 |
| delete `test` . `t1` from `test` . `t1` join `test` . `t2` where `t1` . `b` = `t2` . `a`     | DELETE /*+ hash_join_build(`test`.`t2`) use_index(@`del_1` `test`.`t1` ) use_index(@`del_1` `test`.`t2` )*/ `test`.`t1` FROM `test`.`t1` JOIN `test`.`t2` WHERE `t1`.`b` = `t2`.`a`                                                    | test       | enabled | 2024-08-11 05:27:19.664 | 2024-08-11 05:27:19.664 | utf8    | utf8_general_ci | history | 70ef3d442d95c51020a76c7c86a3ab674258606d4dd24bbd16ac6f69d87a4316 | 8dc146249484f4a6ab219bfe9effa6b7a18aeed3764d49b610da61ac347ab914 |
| select * from `test` . `t1` where `t1` . `a` in ( select `a` from `test` . `t2` )            | SELECT /*+ use_index(@`sel_1` `test`.`t1` ) stream_agg(@`sel_2`) use_index(@`sel_2` `test`.`t2` `ia`) order_index(@`sel_2` `test`.`t2` `ia`) agg_to_cop(@`sel_2`)*/ * FROM `test`.`t1` WHERE `t1`.`a` IN (SELECT `a` FROM `test`.`t2`) | test       | enabled | 2024-08-11 05:27:19.649 | 2024-08-11 05:27:19.649 | utf8    | utf8_general_ci | history | b58508a5e29d7889adf98cad50343d7a575fd32ad55dbdaa88e14ecde54f3d93 | 73b2dec866595688ea416675f88ccb3456eb8e7443a79cd816695b688e07ac6b |
+----------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+-----------------+---------+------------------------------------------------------------------+------------------------------------------------------------------+
4 rows in set (0.001 sec)

> INSERT INTO t1 SELECT * FROM t2 WHERE a = 1;
Query OK, 0 rows affected (0.002 sec)
Records: 0  Duplicates: 0  Warnings: 0

> SELECT @@LAST_PLAN_FROM_BINDING;
+--------------------------+
| @@LAST_PLAN_FROM_BINDING |
+--------------------------+
|                        1 |
+--------------------------+
1 row in set (0.000 sec)

> UPDATE t1, t2 SET t1.a = 1 WHERE t1.b = t2.a;
Query OK, 0 rows affected (0.002 sec)
Rows matched: 0  Changed: 0  Warnings: 0

> SELECT @@LAST_PLAN_FROM_BINDING;
+--------------------------+
| @@LAST_PLAN_FROM_BINDING |
+--------------------------+
|                        1 |
+--------------------------+
1 row in set (0.000 sec)

> DELETE t1 FROM t1 JOIN t2 WHERE t1.b = t2.a;
Query OK, 0 rows affected (0.002 sec)

> SELECT @@LAST_PLAN_FROM_BINDING;
+--------------------------+
| @@LAST_PLAN_FROM_BINDING |
+--------------------------+
|                        1 |
+--------------------------+
1 row in set (0.000 sec)

> SELECT * FROM t1 WHERE t1.a IN (SELECT a FROM t2);
Empty set (0.002 sec)

> SELECT @@LAST_PLAN_FROM_BINDING;
+--------------------------+
| @@LAST_PLAN_FROM_BINDING |
+--------------------------+
|                        1 |
+--------------------------+
1 row in set (0.002 sec)
```

## MySQL 兼容性

`CREATE [GLOBAL|SESSION] BINDING` 语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [DROP [GLOBAL|SESSION] BINDING](/sql-statements/sql-statement-drop-binding.md)
* [SHOW [GLOBAL|SESSION] BINDINGS](/sql-statements/sql-statement-show-bindings.md)
* [ANALYZE](/sql-statements/sql-statement-analyze-table.md)
* [Optimizer Hints](/optimizer-hints.md)
* [执行计划管理 (SPM)](/sql-plan-management.md)
