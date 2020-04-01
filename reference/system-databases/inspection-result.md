---
title: INSPECTION_RESULT
category: reference
---

# INSPECTION_RESULT

TiDB 内置了一些诊断规则，用于检测系统中的故障以及隐患。

该诊断功能可以帮助用户快速发现问题，减少用户的重复性手动工作。可使用 `select * from information_schema.inspection_result` 语句来触发内部诊断。

诊断结果表 `information_schema.inspection_result` 的表结构如下：

{{< copyable "sql" >}}

```sql
mysql> desc inspection_result;
```

```
+-----------+--------------+------+------+---------+-------+
| Field     | Type         | Null | Key  | Default | Extra |
+-----------+--------------+------+------+---------+-------+
| RULE      | varchar(64)  | YES  |      | NULL    |       |
| ITEM      | varchar(64)  | YES  |      | NULL    |       |
| TYPE      | varchar(64)  | YES  |      | NULL    |       |
| INSTANCE  | varchar(64)  | YES  |      | NULL    |       |
| VALUE     | varchar(64)  | YES  |      | NULL    |       |
| REFERENCE | varchar(64)  | YES  |      | NULL    |       |
| SEVERITY  | varchar(64)  | YES  |      | NULL    |       |
| DETAILS   | varchar(256) | YES  |      | NULL    |       |
+-----------+--------------+------+------+---------+-------+
8 rows in set (0.00 sec)
```

字段解释：

* `RULE`：诊断规则，目前实现了以下规则：
    * `config`：配置一致性检测。如果同一个配置在不同节点不一致，会生成 `warning` 诊断结果。
    * `version`：版本一致性检测。如果同一类型的节点版本不同，会生成 `critical` 诊断结果。
    * `current-load`：如果当前系统负载太高，会生成对应的 `warning` 诊断结果。
    * `critical-error`：系统各个模块定义了严重的错误，如果某一个严重错误在对应时间段内超过阈值，会生成 `warning` 诊断结果。
    * `threshold-check`：诊断系统会对大量指标进行阈值判断，如果超过阈值会生成对应的诊断信息。
* `ITEM`：每一个规则会对不同的项进行诊断，该字段表示对应规则下面的具体诊断项。
* `TYPE`：诊断的实例类型，可取值为 `tidb`，`pd` 或 `tikv`。
* `INSTANCE`：诊断的具体实例。
* `VALUE`：针对这个诊断项得到的值。
* `REFERENCE`：针对这个诊断项的参考值（阈值）。如果 `VALUE` 和阈值相差较大，就会产生对应的结果。
* `SEVERITY`：严重程度，`warning` 或 `critical`。
* `DETAILS`：诊断的详细信息，可能包含进一步调查的 SQL 或文档链接。

诊断模块内部包含一系列的规则，这些规则会通过查询已有的监控表和集群信息表，对结果和预先设定的阈值进行对比。如果结果超过阈值或低于阈值将生成 `warning` 或 `critical` 的结果，并在 `details` 列中提供相应信息。

查询已有的诊断规则:

{{< copyable "sql" >}}

```sql
mysql> select * from inspection_rules where type='inspection';
```

```
+-----------------+------------+---------+
| NAME            | TYPE       | COMMENT |
+-----------------+------------+---------+
| config          | inspection |         |
| version         | inspection |         |
| current-load    | inspection |         |
| critical-error  | inspection |         |
| threshold-check | inspection |         |
+-----------------+------------+---------+
5 rows in set (0.00 sec)
```