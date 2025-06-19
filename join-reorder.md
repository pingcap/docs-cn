---
title: Join Reorder 简介
summary: 在 TiDB 中使用 Join Reorder 算法进行多表连接。
---

# Join Reorder 简介

在实际应用场景中，多表连接是很常见的。连接的执行效率与各个表的连接顺序有关。

例如：

{{< copyable "sql" >}}

```sql
SELECT * FROM t1, t2, t3 WHERE t1.a=t2.a AND t3.a=t2.a;
```

在这个查询中，表可以按以下两种顺序进行连接：

- t1 与 t2 连接，然后与 t3 连接
- t2 与 t3 连接，然后与 t1 连接

由于 t1 和 t3 具有不同的数据量和分布，这两种执行顺序可能会表现出不同的性能。

因此，优化器需要一个算法来确定连接顺序。目前，TiDB 中使用以下两种 Join Reorder 算法：

- 贪心算法：在所有参与连接的节点中，TiDB 选择行数最少的表，估算它与其他每个表的连接结果，然后选择连接结果最小的一对。之后，TiDB 继续类似的过程，为下一轮选择和连接其他节点，直到所有节点都完成连接。
- 动态规划算法：在所有参与连接的节点中，TiDB 枚举所有可能的连接顺序，并选择最优的连接顺序。

## 示例：Join Reorder 的贪心算法

以前面的三个表（t1、t2 和 t3）为例。

首先，TiDB 获取所有参与连接操作的节点，并按行数升序排序。

![join-reorder-1](/media/join-reorder-1.png)

之后，选择行数最少的表，分别与其他两个表进行连接。通过比较输出结果集的大小，TiDB 选择结果集较小的一对。

![join-reorder-2](/media/join-reorder-2.png)

然后 TiDB 进入下一轮选择。如果你尝试连接四个表，TiDB 会继续比较输出结果集的大小，并选择结果集较小的一对。

在这个例子中只连接了三个表，所以 TiDB 得到最终的连接结果。

![join-reorder-3](/media/join-reorder-3.png)

## 示例：Join Reorder 的动态规划算法

再次以前面的三个表（t1、t2 和 t3）为例，动态规划算法可以枚举所有可能性。因此，与必须从 `t1` 表（行数最少的表）开始的贪心算法相比，动态规划算法可以枚举如下的连接顺序：

![join-reorder-4](/media/join-reorder-4.png)

当这个选择比贪心算法更好时，动态规划算法可以选择更好的连接顺序。

由于枚举了所有可能性，动态规划算法消耗更多时间，并且更容易受统计信息的影响。

## Join Reorder 算法的选择

TiDB Join Reorder 算法的选择由 [`tidb_opt_join_reorder_threshold`](/system-variables.md#tidb_opt_join_reorder_threshold) 变量控制。如果参与 Join Reorder 的节点数量大于此阈值，TiDB 使用贪心算法。否则，TiDB 使用动态规划算法。

## Join Reorder 算法的限制

当前的 Join Reorder 算法有以下限制：

- 受限于结果集的计算方法，该算法不能保证选择最优的连接顺序。
- Join Reorder 算法对外连接（Outer Join）的支持由 [`tidb_enable_outer_join_reorder`](/system-variables.md#tidb_enable_outer_join_reorder-new-in-v610) 系统变量控制。
- 目前，动态规划算法不能对外连接执行 Join Reorder。

目前，TiDB 支持使用 `STRAIGHT_JOIN` 语法来强制指定连接顺序。更多信息，请参考[语法元素说明](/sql-statements/sql-statement-select.md#description-of-the-syntax-elements)。
