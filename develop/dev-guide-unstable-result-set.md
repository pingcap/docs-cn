---
title: 不稳定结果集
summary: 了解如何处理不稳定结果集错误。
---

# 不稳定结果集

本文档介绍如何解决不稳定结果集错误。

## GROUP BY

为了方便使用，MySQL "扩展"了 `GROUP BY` 语法，允许 `SELECT` 子句引用未在 `GROUP BY` 子句中声明的非聚合字段，即 `NON-FULL GROUP BY` 语法。在其他数据库中，这被视为语法**_错误_**，因为它会导致不稳定的结果集。

例如，你有两个表：

- `stu_info` 存储学生信息
- `stu_score` 存储学生考试成绩

然后你可以编写如下 SQL 查询语句：

```sql
SELECT
    `a`.`class`,
    `a`.`stuname`,
    max( `b`.`courscore` )
FROM
    `stu_info` `a`
    JOIN `stu_score` `b` ON `a`.`stuno` = `b`.`stuno`
GROUP BY
    `a`.`class`,
    `a`.`stuname`
ORDER BY
    `a`.`class`,
    `a`.`stuname`;
```

结果：

```sql
+------------+--------------+------------------+
| class      | stuname      | max(b.courscore) |
+------------+--------------+------------------+
| 2018_CS_01 | MonkeyDLuffy |             95.5 |
| 2018_CS_03 | PatrickStar  |             99.0 |
| 2018_CS_03 | SpongeBob    |             95.0 |
+------------+--------------+------------------+
3 rows in set (0.00 sec)
```

`a`.`class` 和 `a`.`stuname` 字段在 `GROUP BY` 语句中指定，选择的列是 `a`.`class`、`a`.`stuname` 和 `b`.`courscore`。唯一不在 `GROUP BY` 条件中的列 `b`.`courscore` 也使用 `max()` 函数指定了唯一值。这个 SQL 语句只有**_一个_**满足条件的结果，没有任何歧义，这就是所谓的 `FULL GROUP BY` 语法。

下面是一个 `NON-FULL GROUP BY` 语法的反例。例如，在这两个表中，编写以下 SQL 查询（在 `GROUP BY` 中删除 `a`.`stuname`）。

```sql
SELECT
    `a`.`class`,
    `a`.`stuname`,
    max( `b`.`courscore` )
FROM
    `stu_info` `a`
    JOIN `stu_score` `b` ON `a`.`stuno` = `b`.`stuno`
GROUP BY
    `a`.`class`
ORDER BY
    `a`.`class`,
    `a`.`stuname`;
```

这时会返回两个匹配此 SQL 的值。

第一个返回值：

```sql
+------------+--------------+------------------------+
| class      | stuname      | max( `b`.`courscore` ) |
+------------+--------------+------------------------+
| 2018_CS_01 | MonkeyDLuffy |                   95.5 |
| 2018_CS_03 | PatrickStar  |                   99.0 |
+------------+--------------+------------------------+
```

第二个返回值：

```sql
+------------+--------------+------------------+
| class      | stuname      | max(b.courscore) |
+------------+--------------+------------------+
| 2018_CS_01 | MonkeyDLuffy |             95.5 |
| 2018_CS_03 | SpongeBob    |             99.0 |
+------------+--------------+------------------+
```

出现两个结果是因为你在 SQL 中**_没有_**指定如何获取 `a`.`stuname` 字段的值，而这两个结果都满足 SQL 语义。这导致了不稳定的结果集。因此，如果你想保证 `GROUP BY` 语句结果集的稳定性，请使用 `FULL GROUP BY` 语法。

MySQL 提供了 `sql_mode` 开关 `ONLY_FULL_GROUP_BY` 来控制是否检查 `FULL GROUP BY` 语法。TiDB 也兼容这个 `sql_mode` 开关。

```sql
mysql> select a.class, a.stuname, max(b.courscore) from stu_info a join stu_score b on a.stuno=b.stuno group by a.class order by a.class, a.stuname;
+------------+--------------+------------------+
| class      | stuname      | max(b.courscore) |
+------------+--------------+------------------+
| 2018_CS_01 | MonkeyDLuffy |             95.5 |
| 2018_CS_03 | PatrickStar  |             99.0 |
+------------+--------------+------------------+
2 rows in set (0.01 sec)

mysql> set @@sql_mode='STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION,ONLY_FULL_GROUP_BY';
Query OK, 0 rows affected (0.01 sec)

mysql> select a.class, a.stuname, max(b.courscore) from stu_info a join stu_score b on a.stuno=b.stuno group by a.class order by a.class, a.stuname;
ERROR 1055 (42000): Expression #2 of ORDER BY is not in GROUP BY clause and contains nonaggregated column '' which is not functionally dependent on columns in GROUP BY clause; this is incompatible with sql_mode=only_full_group_by
```

**运行结果**：上面的例子展示了设置 `sql_mode` 为 `ONLY_FULL_GROUP_BY` 时的效果。

## ORDER BY

在 SQL 语义中，只有使用 `ORDER BY` 语法才能保证结果集按顺序输出。对于单实例数据库，由于数据存储在一台服务器上，在没有数据重组的情况下，多次执行的结果通常是稳定的。某些数据库（特别是 MySQL InnoDB 存储引擎）甚至可以按主键或索引顺序输出结果集。

作为分布式数据库，TiDB 将数据存储在多个服务器上。此外，TiDB 层不缓存数据页，因此没有 `ORDER BY` 的 SQL 语句的结果集顺序容易被感知为不稳定。要输出有序的结果集，需要在 `ORDER BY` 子句中明确添加排序字段，这符合 SQL 语义。

在下面的例子中，只在 `ORDER BY` 子句中添加了一个字段，TiDB 只按该字段对结果进行排序。

```sql
mysql> select a.class, a.stuname, b.course, b.courscore from stu_info a join stu_score b on a.stuno=b.stuno order by a.class;
+------------+--------------+-------------------------+-----------+
| class      | stuname      | course                  | courscore |
+------------+--------------+-------------------------+-----------+
| 2018_CS_01 | MonkeyDLuffy | PrinciplesofDatabase    |      60.5 |
| 2018_CS_01 | MonkeyDLuffy | English                 |      43.0 |
| 2018_CS_01 | MonkeyDLuffy | OpSwimming              |      67.0 |
| 2018_CS_01 | MonkeyDLuffy | OpFencing               |      76.0 |
| 2018_CS_01 | MonkeyDLuffy | FundamentalsofCompiling |      88.0 |
| 2018_CS_01 | MonkeyDLuffy | OperatingSystem         |      90.5 |
| 2018_CS_01 | MonkeyDLuffy | PrincipleofStatistics   |      69.0 |
| 2018_CS_01 | MonkeyDLuffy | ProbabilityTheory       |      76.0 |
| 2018_CS_01 | MonkeyDLuffy | Physics                 |      63.5 |
| 2018_CS_01 | MonkeyDLuffy | AdvancedMathematics     |      95.5 |
| 2018_CS_01 | MonkeyDLuffy | LinearAlgebra           |      92.5 |
| 2018_CS_01 | MonkeyDLuffy | DiscreteMathematics     |      89.0 |
| 2018_CS_03 | SpongeBob    | PrinciplesofDatabase    |      88.0 |
| 2018_CS_03 | SpongeBob    | English                 |      79.0 |
| 2018_CS_03 | SpongeBob    | OpBasketball            |      92.0 |
| 2018_CS_03 | SpongeBob    | OpTennis                |      94.0 |
| 2018_CS_03 | PatrickStar  | LinearAlgebra           |       6.5 |
| 2018_CS_03 | PatrickStar  | AdvancedMathematics     |       5.0 |
| 2018_CS_03 | SpongeBob    | DiscreteMathematics     |      72.0 |
| 2018_CS_03 | PatrickStar  | ProbabilityTheory       |      12.0 |
| 2018_CS_03 | PatrickStar  | PrincipleofStatistics   |      20.0 |
| 2018_CS_03 | PatrickStar  | OperatingSystem         |      36.0 |
| 2018_CS_03 | PatrickStar  | FundamentalsofCompiling |       2.0 |
| 2018_CS_03 | PatrickStar  | DiscreteMathematics     |      14.0 |
| 2018_CS_03 | PatrickStar  | PrinciplesofDatabase    |       9.0 |
| 2018_CS_03 | PatrickStar  | English                 |      60.0 |
| 2018_CS_03 | PatrickStar  | OpTableTennis           |      12.0 |
| 2018_CS_03 | PatrickStar  | OpPiano                 |      99.0 |
| 2018_CS_03 | SpongeBob    | FundamentalsofCompiling |      43.0 |
| 2018_CS_03 | SpongeBob    | OperatingSystem         |      95.0 |
| 2018_CS_03 | SpongeBob    | PrincipleofStatistics   |      90.0 |
| 2018_CS_03 | SpongeBob    | ProbabilityTheory       |      87.0 |
| 2018_CS_03 | SpongeBob    | Physics                 |      65.0 |
| 2018_CS_03 | SpongeBob    | AdvancedMathematics     |      55.0 |
| 2018_CS_03 | SpongeBob    | LinearAlgebra           |      60.5 |
| 2018_CS_03 | PatrickStar  | Physics                 |       6.0 |
+------------+--------------+-------------------------+-----------+
36 rows in set (0.01 sec)

```

当 `ORDER BY` 值相同时，结果是不稳定的。为了减少随机性，`ORDER BY` 值应该是唯一的。如果无法保证唯一性，则需要添加更多的 `ORDER BY` 字段，直到 `ORDER BY` 中的 `ORDER BY` 字段组合是唯一的，这样结果才会稳定。

## GROUP_CONCAT() 中未使用 ORDER BY 导致结果集不稳定

由于 TiDB 从存储层并行读取数据，因此没有 `ORDER BY` 的 `GROUP_CONCAT()` 返回的结果集顺序容易被感知为不稳定。

要让 `GROUP_CONCAT()` 按顺序获取结果集输出，需要在 `ORDER BY` 子句中添加排序字段，这符合 SQL 语义。在下面的例子中，没有 `ORDER BY` 的拼接 `customer_id` 的 `GROUP_CONCAT()` 导致了不稳定的结果集。

1. 不包含 `ORDER BY`

    第一次查询：

    {{< copyable "sql" >}}

    ```sql
    mysql>  select GROUP_CONCAT( customer_id SEPARATOR ',' ) FROM customer where customer_id like '200002%';
    +-------------------------------------------------------------------------+
    | GROUP_CONCAT(customer_id  SEPARATOR ',')                                |
    +-------------------------------------------------------------------------+
    | 20000200992,20000200993,20000200994,20000200995,20000200996,20000200... |
    +-------------------------------------------------------------------------+
    ```

    第二次查询：

    {{< copyable "sql" >}}

    ```sql
    mysql>  select GROUP_CONCAT( customer_id SEPARATOR ',' ) FROM customer where customer_id like '200002%';
    +-------------------------------------------------------------------------+
    | GROUP_CONCAT(customer_id  SEPARATOR ',')                                |
    +-------------------------------------------------------------------------+
    | 20000203040,20000203041,20000203042,20000203043,20000203044,20000203... |
    +-------------------------------------------------------------------------+
    ```

2. 包含 `ORDER BY`

    第一次查询：

    {{< copyable "sql" >}}

    ```sql
    mysql>  select GROUP_CONCAT( customer_id order by customer_id SEPARATOR ',' ) FROM customer where customer_id like '200002%';
    +-------------------------------------------------------------------------+
    | GROUP_CONCAT(customer_id  SEPARATOR ',')                                |
    +-------------------------------------------------------------------------+
    | 20000200000,20000200001,20000200002,20000200003,20000200004,20000200... |
    +-------------------------------------------------------------------------+
    ```

    第二次查询：

    {{< copyable "sql" >}}

    ```sql
    mysql>  select GROUP_CONCAT( customer_id order by customer_id SEPARATOR ',' ) FROM customer where customer_id like '200002%';
    +-------------------------------------------------------------------------+
    | GROUP_CONCAT(customer_id  SEPARATOR ',')                                |
    +-------------------------------------------------------------------------+
    | 20000200000,20000200001,20000200002,20000200003,20000200004,20000200... |
    +-------------------------------------------------------------------------+
    ```

## SELECT * FROM T LIMIT N 的不稳定结果

返回的结果与存储节点（TiKV）上的数据分布有关。如果执行多次查询，存储节点（TiKV）的不同存储单元（Region）返回结果的速度不同，这可能导致不稳定的结果。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
