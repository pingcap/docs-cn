---
title: Join Reorder 算法简介
---

# Join Reorder 算法简介

在实际的业务场景中，多个表的 Join 语句是很常见的，而 Join 的执行效率和各个表参与 Join 的顺序有关系。如 `select * from t1, t2, t3 where t1.a=t2.a and t3.a=t2.a`，这个 SQL 中可能的执行顺序有“t1 和 t2 先做 Join，然后再和 t3 做 Join”以及“t2 和 t3 先做 Join，然后再和 t1 做 Join”两种情况。根据 `t1` 和 `t3` 的数据量及数据分布，这两种执行顺序会有不同的性能表现。

因此优化器需要实现一种决定 Join 顺序的算法。目前 TiDB 中使用的算法是 Join Reorder 算法，又称贪心算法。

## Join Reorder 算法实例

以三个表 t1、t2、t3 的 Join 为例。首先获取所有参与 Join 的节点，将所有节点按照行数多少，从少到多进行排序。

![join-reorder-1](/media/join-reorder-1.png)

之后选定其中最小的表，将其与其他两个表分别做一次 Join，观察输出的结果集大小，选择其中结果更小的一对。

![join-reorder-2](/media/join-reorder-2.png)

然后进入下一轮的选择，如果这时是四个表，那么就继续比较输出结果集的大小，进行选择。这里只有三个表，因此就直接得到了最终的 Join 结果。

![join-reorder-3](/media/join-reorder-3.png)

以上就是当前 TiDB 中使用的 Join reorder 算法。

## Join reorder 算法限制

当前的 Join Reorder 算法存在如下限制

- 目前并不支持 Outer Join 的 Join Reorder
- 受结果集的计算算法所限并不会保证一定会选到合适的 Join order

目前 TiDB 中支持使用 `STRAIGHT_JOIN` 语法来强制指定一种 Join 顺序，参见[语法元素说明](/sql-statements/sql-statement-select.md#语法元素说明)。
