---
title: 结果集不稳定
---

# 结果集不稳定

## 1. group by

出于便捷的考量，MySQL “扩展” 了 group by 语法，使 select 子句可以引用未在 group by 子句中声明的非聚集字段，也就是 non-full group by 语法。在其他数据库中，这被认为是一种语法错误，因为这会导致结果集不稳定。

在下例的 3 条 SQL 语句中，第一条 SQL 使用了 full group by 语法 ，所有在 select 子句中引用的字段，都在 group by 子句中有所声明，所以它的结果集是稳定的，可以看到 class 与 stuname 的全部组合共有三种；第二条与第三条是同一个 SQL，但它在两次执行时得到了不同的结果，这条 SQL 的 group by 子句中仅声明了一个 class 字段，因此结果集只会针对 class 进行聚集，class 的唯一值有两个，也就是说结果集中只会包含两行数据，而 class 与 stuname 的全部组合共有三种，班级 2018_CS_03 有两位同学，每次执行时返回哪位同学是没有语义上的限制的，都是符合语义的结果。

```sql
mysql> select a.class, a.stuname, max(b.courscore) from stu_info a join stu_score b on a.stuno=b.stuno group by a.class, a.stuname order by a.class, a.stuname;
+------------+--------------+------------------+
| class      | stuname      | max(b.courscore) |
+------------+--------------+------------------+
| 2018_CS_01 | MonkeyDLuffy |             95.5 |
| 2018_CS_03 | PatrickStar  |             99.0 |
| 2018_CS_03 | SpongeBob    |             95.0 |
+------------+--------------+------------------+
3 rows in set (0.00 sec)

mysql> select a.class, a.stuname, max(b.courscore) from stu_info a join stu_score b on a.stuno=b.stuno group by a.class order by a.class, a.stuname;
+------------+--------------+------------------+
| class      | stuname      | max(b.courscore) |
+------------+--------------+------------------+
| 2018_CS_01 | MonkeyDLuffy |             95.5 |
| 2018_CS_03 | SpongeBob    |             99.0 |
+------------+--------------+------------------+
2 rows in set (0.01 sec)

mysql> select a.class, a.stuname, max(b.courscore) from stu_info a join stu_score b on a.stuno=b.stuno group by a.class order by a.class, a.stuname;
+------------+--------------+------------------+
| class      | stuname      | max(b.courscore) |
+------------+--------------+------------------+
| 2018_CS_01 | MonkeyDLuffy |             95.5 |
| 2018_CS_03 | PatrickStar  |             99.0 |
+------------+--------------+------------------+
2 rows in set (0.01 sec)

```

因此，想保障 group by 语句结果集的稳定，请使用 full group by 语法。

MySQL 提供了一个 SQL_MODE 开关 ONLY_FULL_GROUP_BY 来控制是否进行 full group by 语法的检查，TiDB 也兼容了这个 SQL_MODE 开关：

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

**说明**：上例为 sql_mode 设置了 ONLY_FULL_GROUP_BY 的效果

## 2. order by

在 SQL 的语义中，只有使用了 order by 语法才会保障结果集的顺序输出。而单机数据库由于数据都存储在一台服务器上，在不进行数据重组时，多次执行的结果往往是稳定的，有些数据库(尤其是 MySQL InnoDB 存储引擎)还会按照主键或索引的顺序进行结果集的输出。TiDB 是分布式数据库，数据被存储在多台服务器上，另外 TiDB 层不缓存数据页，因此不含 order by 的 SQL 语句的结果集展现顺序容易被感知到不稳定。想要按顺序输出的结果集，需明确地把要排序的字段添加到 order by 子句中，这符合 SQL 的语义。

在下面的案例中，用户只在 order by 子句中添加了一个字段，TiDB 只会按照这一个字段进行排序。

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

当遇到相同的 order by 值时，排序结果不稳定。为减少随机性，应当尽可能保持 order by 值的唯一性。不能保证唯一的继续加，保证 order by 的字段组合是唯一时，结果才能唯一。

## 3. 由于 group_concat() 中没有使用 order by 导致结果集不稳定

结果集不稳定是因为 TiDB 是并行地从存储层读取数据，所以 `group_concat()` 在不加 order by 的情况下得到的结果集展现顺序容易被感知到不稳定。

`group_concat()` 要获取到按顺序输出的结果集，需要把用于排序的字段添加到 order by 子句中，这样才符合 SQL 的语义。在下面的案例中，使用 `group_concat()` 不加 order by 的情况下拼接 customer_id ，造成结果集不稳定：

1. 不加 order by

   第一次查询：

   ```sql
   mysql>  select GROUP_CONCAT( customer_id SEPARATOR ',' ) FROM customer where customer_id like '200002%';
   +-------------------------------------------------------------------------+
   | GROUP_CONCAT(customer_id  SEPARATOR ',')                                |
   +-------------------------------------------------------------------------+
   | 20000200992,20000200993,20000200994,20000200995,20000200996,20000200... |
   +-------------------------------------------------------------------------+

   ```

   第二次查询：

   ```sql
   mysql>  select GROUP_CONCAT( customer_id SEPARATOR ',' ) FROM customer where customer_id like '200002%';
   +-------------------------------------------------------------------------+
   | GROUP_CONCAT(customer_id  SEPARATOR ',')                                |
   +-------------------------------------------------------------------------+
   | 20000203040,20000203041,20000203042,20000203043,20000203044,20000203... |
   +-------------------------------------------------------------------------+

   ```

2. 加 order by

   第一次查询：

   ```sql
   mysql>  select GROUP_CONCAT( customer_id order by customer_id SEPARATOR ',' ) FROM customer where customer_id like '200002%';
   +-------------------------------------------------------------------------+
   | GROUP_CONCAT(customer_id  SEPARATOR ',')                                |
   +-------------------------------------------------------------------------+
   | 20000200000,20000200001,20000200002,20000200003,20000200004,20000200... |
   +-------------------------------------------------------------------------+

   ```

   第二次查询：

   ```sql
   mysql>  select GROUP_CONCAT( customer_id order by customer_id SEPARATOR ',' ) FROM customer where customer_id like '200002%';
   +-------------------------------------------------------------------------+
   | GROUP_CONCAT(customer_id  SEPARATOR ',')                                |
   +-------------------------------------------------------------------------+
   | 20000200000,20000200001,20000200002,20000200003,20000200004,20000200... |
   +-------------------------------------------------------------------------+

   ```

## 4. select \* from t limit n 的结果不稳定

返回结果与数据在存储节点（TiKV）上的分布有关。如果进行了多次查询，存储节点（TiKV）不同存储单元（Region） 返回结果的速度不同，会造成结果不稳定。
