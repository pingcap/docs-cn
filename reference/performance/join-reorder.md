---
title: TiDB 当前的 Join Reorder 算法简介
category: reference
---

# Join Reorder

在实际的的业务场景中，多个表的 Join 语句是非常常见的。而 Join 的执行效果会和各个表参与 Join 的顺序有关系。如 `select * from t, t1, t2 where t.a=t1.a and t2.a=t1.a`，这个 SQL 中可能的执行顺序有`t 和 t1 先做 Join，然后再和 t2 做 Join`以及`t1 和 t2 先做 Join，然后再和 t 做 Join` 两种情况。根据 `t` 和 `t2` 的数据量及数据分布，这两种执行顺序会有不同的性能表现。

因此需要优化器实现一种决定 Join 顺序的算法。目前 TiDB 中的算法是贪心算法。

# 贪心算法简介

以三个表 `t1, t2, t3` 的 Join 为例。首先我们会从拿到所有参与 Join 的节点，将他们按照行数多少从少到多排序

![pic1](/media/join-reorder-1.png)

之后我们选定其中最小的表。和其他两个表一次做 Join，看输出的结果集大小，选择更小的一侧作为选择。

![pic2](/media/join-reorder-2.png)

然后进入下一轮的选择，如果这时是四个表那么就是继续比较输出结果集的大小进行选择。这里只有三个表，因此就直接得到了最终的 Join 结果。

![pic3](/media/join-reorder-3.png)

这个就是当前 TiDB 中使用的 Join reorder 算法。

# 限制

当前的 Join Reorder 算法存在如下限制

- 目前并不支持 Outer Join 的 Join Reorder
- 受结果集的计算算法所限并不会保证一定会选到合适的 Join order

目前 TiDB 中支持使用 `STRAIGHT_JOIN` 语法来强制指定一种 Join 顺序，参见[语法元素说明](/reference/sql/statements/select.md#语法元素说明)。
