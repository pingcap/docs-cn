---
title: 谓词下推
summary: 介绍 TiDB 的一个逻辑优化规则——谓词下推（Predicate Push Down，PPD）。
---

# 谓词下推（PPD）

本文介绍 TiDB 的一个逻辑优化规则——谓词下推（Predicate Push Down，PPD）。本文旨在帮助你理解谓词下推以及了解其适用和不适用的场景。

PPD 将选择算子尽可能下推到数据源，以尽早完成数据过滤，这可以显著降低数据传输或计算的成本。

## 示例

以下案例描述了 PPD 的优化。案例 1、2 和 3 是 PPD 适用的场景，案例 4、5 和 6 是 PPD 不适用的场景。

### 案例 1：将谓词下推到存储层

```sql
create table t(id int primary key, a int);
explain select * from t where a < 1;
+-------------------------+----------+-----------+---------------+--------------------------------+
| id                      | estRows  | task      | access object | operator info                  |
+-------------------------+----------+-----------+---------------+--------------------------------+
| TableReader_7           | 3323.33  | root      |               | data:Selection_6               |
| └─Selection_6           | 3323.33  | cop[tikv] |               | lt(test.t.a, 1)                |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo |
+-------------------------+----------+-----------+---------------+--------------------------------+
3 rows in set (0.00 sec)
```

在这个查询中，将谓词 `a < 1` 下推到 TiKV 层进行数据过滤可以减少网络传输的开销。

### 案例 2：将谓词下推到存储层

```sql
create table t(id int primary key, a int not null);
explain select * from t where a < substring('123', 1, 1);
+-------------------------+----------+-----------+---------------+--------------------------------+
| id                      | estRows  | task      | access object | operator info                  |
+-------------------------+----------+-----------+---------------+--------------------------------+
| TableReader_7           | 3323.33  | root      |               | data:Selection_6               |
| └─Selection_6           | 3323.33  | cop[tikv] |               | lt(test.t.a, 1)                |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo |
+-------------------------+----------+-----------+---------------+--------------------------------+
```

这个查询与案例 1 的执行计划相同，因为谓词 `a < substring('123', 1, 1)` 中 `substring` 的输入参数都是常量，所以可以提前计算。然后谓词被简化为等价的谓词 `a < 1`。之后，TiDB 可以将 `a < 1` 下推到 TiKV。

### 案例 3：将谓词下推到连接算子之下

```sql
create table t(id int primary key, a int not null);
create table s(id int primary key, a int not null);
explain select * from t join s on t.a = s.a where t.a < 1;
+------------------------------+----------+-----------+---------------+--------------------------------------------+
| id                           | estRows  | task      | access object | operator info                              |
+------------------------------+----------+-----------+---------------+--------------------------------------------+
| HashJoin_8                   | 4154.17  | root      |               | inner join, equal:[eq(test.t.a, test.s.a)] |
| ├─TableReader_15(Build)      | 3323.33  | root      |               | data:Selection_14                          |
| │ └─Selection_14             | 3323.33  | cop[tikv] |               | lt(test.s.a, 1)                            |
| │   └─TableFullScan_13       | 10000.00 | cop[tikv] | table:s       | keep order:false, stats:pseudo             |
| └─TableReader_12(Probe)      | 3323.33  | root      |               | data:Selection_11                          |
|   └─Selection_11             | 3323.33  | cop[tikv] |               | lt(test.t.a, 1)                            |
|     └─TableFullScan_10       | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo             |
+------------------------------+----------+-----------+---------------+--------------------------------------------+
7 rows in set (0.00 sec)
```

在这个查询中，谓词 `t.a < 1` 被下推到连接之下以提前过滤，这可以减少连接的计算开销。

此外，这条 SQL 语句执行了一个内连接，`ON` 条件是 `t.a = s.a`。可以从 `t.a < 1` 推导出谓词 `s.a < 1` 并将其下推到连接算子之下的 `s` 表。过滤 `s` 表可以进一步减少连接的计算开销。

### 案例 4：存储层不支持的谓词无法下推

```sql
create table t(id int primary key, a varchar(10) not null);
desc select * from t where truncate(a, " ") = '1';
+-------------------------+----------+-----------+---------------+---------------------------------------------------+
| id                      | estRows  | task      | access object | operator info                                     |
+-------------------------+----------+-----------+---------------+---------------------------------------------------+
| Selection_5             | 8000.00  | root      |               | eq(truncate(cast(test.t.a, double BINARY), 0), 1) |
| └─TableReader_7         | 10000.00 | root      |               | data:TableFullScan_6                              |
|   └─TableFullScan_6     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo                    |
+-------------------------+----------+-----------+---------------+---------------------------------------------------+
```

在这个查询中，有一个谓词 `truncate(a, " ") = '1'`。

从 `explain` 结果可以看出，该谓词没有被下推到 TiKV 进行计算。这是因为 TiKV 协处理器不支持内置函数 `truncate`。

### 案例 5：外连接内表上的谓词不能下推

```sql
create table t(id int primary key, a int not null);
create table s(id int primary key, a int not null);
explain select * from t left join s on t.a = s.a where s.a is null;
+-------------------------------+----------+-----------+---------------+-------------------------------------------------+
| id                            | estRows  | task      | access object | operator info                                   |
+-------------------------------+----------+-----------+---------------+-------------------------------------------------+
| Selection_7                   | 10000.00 | root      |               | isnull(test.s.a)                                |
| └─HashJoin_8                  | 12500.00 | root      |               | left outer join, equal:[eq(test.t.a, test.s.a)] |
|   ├─TableReader_13(Build)     | 10000.00 | root      |               | data:TableFullScan_12                           |
|   │ └─TableFullScan_12        | 10000.00 | cop[tikv] | table:s       | keep order:false, stats:pseudo                  |
|   └─TableReader_11(Probe)     | 10000.00 | root      |               | data:TableFullScan_10                           |
|     └─TableFullScan_10        | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo                  |
+-------------------------------+----------+-----------+---------------+-------------------------------------------------+
6 rows in set (0.00 sec)
```

在这个查询中，内表 `s` 上有一个谓词 `s.a is null`。

从 `explain` 结果可以看出，该谓词没有被下推到连接算子之下。这是因为当 `on` 条件不满足时，外连接会用 `NULL` 值填充内表，而谓词 `s.a is null` 用于在连接之后过滤结果。如果将其下推到连接之下的内表，执行计划就不等价于原始计划了。

### 案例 6：包含用户变量的谓词不能下推

```sql
create table t(id int primary key, a char);
set @a = 1;
explain select * from t where a < @a;
+-------------------------+----------+-----------+---------------+--------------------------------+
| id                      | estRows  | task      | access object | operator info                  |
+-------------------------+----------+-----------+---------------+--------------------------------+
| Selection_5             | 8000.00  | root      |               | lt(test.t.a, getvar("a"))      |
| └─TableReader_7         | 10000.00 | root      |               | data:TableFullScan_6           |
|   └─TableFullScan_6     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo |
+-------------------------+----------+-----------+---------------+--------------------------------+
3 rows in set (0.00 sec)
```

在这个查询中，表 `t` 上有一个谓词 `a < @a`。谓词中的 `@a` 是一个用户变量。

从 `explain` 结果可以看出，该谓词不像案例 2 那样被简化为 `a < 1` 并下推到 TiKV。这是因为用户变量 `@a` 的值可能在计算过程中发生变化，而 TiKV 无法感知这些变化。所以 TiDB 不会将 `@a` 替换为 `1`，也不会将其下推到 TiKV。

下面是一个帮助理解的示例：

```sql
create table t(id int primary key, a int);
insert into t values(1, 1), (2,2);
set @a = 1;
select id, a, @a:=@a+1 from t where a = @a;
+----+------+----------+
| id | a    | @a:=@a+1 |
+----+------+----------+
|  1 |    1 | 2        |
|  2 |    2 | 3        |
+----+------+----------+
2 rows in set (0.00 sec)
```

从这个查询可以看出，`@a` 的值会在查询过程中发生变化。所以如果将 `a = @a` 替换为 `a = 1` 并下推到 TiKV，就不是一个等价的执行计划了。
