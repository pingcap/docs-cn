---
title: Select 语句
category: user guide
---

# Select 语句

Select 语句用于从数据库中查询数据。

## 语法定义

```sql
SELECT
    [ALL | DISTINCT | DISTINCTROW ]
      [HIGH_PRIORITY]
      [SQL_CACHE | SQL_NO_CACHE] [SQL_CALC_FOUND_ROWS]
    select_expr [, select_expr ...]
    [FROM table_references
    [WHERE where_condition]
    [GROUP BY {col_name | expr | position}
      [ASC | DESC], ...]
    [HAVING where_condition]
    [ORDER BY {col_name | expr | position}
      [ASC | DESC], ...]
    [LIMIT {[offset,] row_count | row_count OFFSET offset}]
    [FOR UPDATE | LOCK IN SHARE MODE]]
```

## 语法元素说明

|语法元素 | 说明|
|-------- | -----------|
|ALL、DISTINCT、DISTINCTROW | 查询结果集中可能会包含重复值。指定 DISTINCT/DISTINCTROW 则在查询结果中过滤掉重复的行；指定 ALL 则列出所有的行。默认为 ALL。|
|HIGH_PRIORITY | 该语句为高优先级语句，TiDB 在执行阶段会优先处理这条语句|
|SQL_CACHE、SQL_NO_CACHE、SQL_CALC_FOUND_ROWS | TiDB 出于兼容性解析这三个语法，但是不做任何处理|
|select_expr | 投影操作列表，一般包括列名、表达式，或者是用 '*' 表示全部列|
|From table_references | 表示数据来源，数据来源可以是一个表（select * from t;）或者是多个表 (select * from t1 join t2;) 或者是0个表 (select 1+1;)|
|WHERE where_condition | Where 子句用于设置过滤条件，查询结果中只会包含满足条件的数据|
|GROUP BY | GroupBy 子句用于对查询结果集进行分组|
|HAVING where_condition | Having 子句与 Where 子句作用类似，Having 子句可以让过滤 GroupBy 后的各种数据，Where 子句用于在聚合前过滤记录。|
|ORDER BY | OrderBy 子句用于指定结果排序顺序，可以按照列、表达式或者是 select_expr 列表中某个位置的字段进行排序。|
|LIMIT | Limit 子句用于限制结果条数。Limit 接受一个或两个数字参数，如果只有一个参数，那么表示返回数据的最大行数；如果是两个参数，那么第一个参数表示返回数据的第一行的偏移量（第一行数据的偏移量是 0），第二个参数指定返回数据的最大条目数。|
|FOR UPDATE | 对查询结果集所有数据上读锁，以监测其他事务对这些的并发修改。TiDB 使用[乐观事务模型](https://github.com/pingcap/docs-cn/blob/master/op-guide/mysql-compatibility.md#事务)在语句执行期间不会检测锁冲突，在事务的提交阶段才会检测事务冲突，如果执行 Select For Update 期间，有其他事务修改相关的数据，那么包含 Select For Update 语句的事务会提交失败。|
|LOCK IN SHARE MODE | TiDB 出于兼容性解析这个语法，但是不做任何处理|