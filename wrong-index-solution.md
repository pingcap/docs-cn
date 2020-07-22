---
title: Wrong Index Solution
summary: Learn how to solve the wrong index issue.
---

# Wrong Index Solution

If you find that the execution speed of some query does not reach the expectation, the optimizer might choose the wrong index to run the query.

You can first view the [health state of tables](/statistics.md#health-state-of-tables) in the statistics, and then solve this issue according to the different health states.

## Low health state

The low health state means TiDB has not performed the`ANALYZE` statement for a long time. You can update the statistics by running the `ANALYZE` command. After the update, if the optimizer still uses the wrong index, refer to the next section.

## Near 100% health state

The near 100% health state suggests that the `ANALYZE` statement is just completed or was completed a short time ago. In this case, the wrong index issue might be related to TiDB's estimation logic for the number of rows.

For equivalence queries, the cause might be [Count-Min Sketch](/statistics.md#count-min-sketch). You can check whether Count-Min Sketch is the cause and take corresponding solutions. 

If the cause above does not apply to your problem, you can force-select indexes by using the `USE_INDEX` or `use index` optimzer hint (see [USE_INDEX](/optimizer-hints.md#use_indext1_name-idx1_name--idx2_name-) for details). Also, you can change the query behavior by using [SQL Plan Management](/sql-plan-management.md) in a non-intrusive way.

## Other situations

Apart from the aforementioned situations, the wrong index issue might also be caused by data updates which renders all the indexes no longer applicable. In such cases, you need to perform analysis on the conditions and data distribution to see whether new indexes can speed up the query. If so, you can add new indexes by running the [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) command.
