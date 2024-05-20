---
title: Join Reorder 算法简介
aliases: ['/docs-cn/dev/join-reorder/','/docs-cn/dev/reference/performance/join-reorder/']
summary: Join Reorder 算法决定了多表 Join 的顺序，影响执行效率。TiDB 中有贪心算法和动态规划算法两种实现。贪心算法选择行数最小的表与其他表做 Join，直到所有节点完成 Join。动态规划算法枚举所有可能的 Join 顺序，选择最优的。算法受系统变量控制，且存在一些限制，如无法保证一定选到合适的 Join 顺序。
---

# Join Reorder 算法简介

在实际的业务场景中，多个表的 Join 语句是很常见的，而 Join 的执行效率和各个表参与 Join 的顺序有关系。如 `select * from t1, t2, t3 where t1.a=t2.a and t3.a=t2.a`，这个 SQL 中可能的执行顺序有“t1 和 t2 先做 Join，然后再和 t3 做 Join”以及“t2 和 t3 先做 Join，然后再和 t1 做 Join”两种情况。根据 `t1` 和 `t3` 的数据量及数据分布，这两种执行顺序会有不同的性能表现。

因此优化器需要实现一种决定 Join 顺序的算法。目前 TiDB 中存在两种 Join Reorder 算法，贪心算法和动态规划算法。

- Join Reorder 贪心算法：在所有参与 Join 的节点中，选择行数最小的表与其他各表分别做一次 Join 的结果估算，然后选择其中结果最小的一对进行 Join，再继续这个过程进入下一轮的选择和 Join，直到所有的节点都完成 Join。
- Join Reorder 动态规划算法：在所有参与 Join 的节点中，枚举所有可能的 Join 顺序，然后选择最优的 Join 顺序。

## Join Reorder 贪心算法实例

以三个表 t1、t2、t3 的 Join 为例。首先获取所有参与 Join 的节点，将所有节点按照行数多少，从少到多进行排序。

![join-reorder-1](/media/join-reorder-1.png)

之后选定其中最小的表，将其与其他两个表分别做一次 Join，观察输出的结果集大小，选择其中结果更小的一对。

![join-reorder-2](/media/join-reorder-2.png)

然后进入下一轮的选择，如果这时是四个表，那么就继续比较输出结果集的大小，进行选择。这里只有三个表，因此就直接得到了最终的 Join 结果。

![join-reorder-3](/media/join-reorder-3.png)

## Join Reorder 动态规划算法实例

仍然以上述例子为例。动态规划算法会枚举所有的可能性，因此相对贪心算法必须从 `t1` 表开始枚举，动态规划算法可以枚举如下的 Join 顺序。

![join-reorder-4](/media/join-reorder-4.png)

当该选择比贪心算法更优时，动态规划算法便可以选择到更优的 Join 顺序。

相应地，因为会枚举所有的可能性，动态规划算法会消耗更多的时间，也会更容易受统计信息影响。

## Join Reorder 算法的控制

目前 Join Reorder 算法由变量 [`tidb_opt_join_reorder_threshold`](/system-variables.md#tidb_opt_join_reorder_threshold) 控制，当参与 Join Reorder 的节点个数大于该阈值时选择贪心算法，反之选择动态规划算法。

## Join Reorder 算法限制

当前的 Join Reorder 算法存在如下限制：

- 受结果集的计算算法所限并不会保证一定会选到合适的 Join order
- 是否启用 Outer Join 的 Join Reorder 功能由系统变量 [`tidb_enable_outer_join_reorder`](/system-variables.md#tidb_enable_outer_join_reorder-从-v610-版本开始引入) 控制。
- 目前动态规划算法无法进行 Outer Join 的 Join Reorder。

目前 TiDB 中支持使用 `STRAIGHT_JOIN` 语法来强制指定一种 Join 顺序，参见[语法元素说明](/sql-statements/sql-statement-select.md#语法元素说明)。
