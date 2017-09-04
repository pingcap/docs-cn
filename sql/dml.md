---
title: 数据操作语言
category: user guide
---

# TiDB 数据操作语言

数据操作语言（Data Manipulation Language， DML）用于帮助用户实现对数据库的基本操作，比如查询、写入、删除和修改数据库中的数据。

TiDB 支持的数据操作语言包括 Select ，Insert, Delete, Update，和 Replace。

## Table of Contents
+ [Select 语句](#select-语句)
+ [Insert 语句](#insert-语句)
+ Delete 语句
+ Update 语句
+ Replace 语句

## Select 语句

Select 语句用于从数据库中查询数据。

### 语法定义

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

### 语法元素说明

|语法元素 | 说明|
|-------- | -----------|
|`ALL、DISTINCT、DISTINCTROW` | 查询结果集中可能会包含重复值。指定 DISTINCT/DISTINCTROW 则在查询结果中过滤掉重复的行；指定 ALL 则列出所有的行。默认为 ALL。|
|`HIGH_PRIORITY` | 该语句为高优先级语句，TiDB 在执行阶段会优先处理这条语句|
|`SQL_CACHE、SQL_NO_CACHE、SQL_CALC_FOUND_ROWS` | TiDB 出于兼容性解析这三个语法，但是不做任何处理|
|`select_expr` | 投影操作列表，一般包括列名、表达式，或者是用 '*' 表示全部列|
|`From table_references` | 表示数据来源，数据来源可以是一个表（select * from t;）或者是多个表 (select * from t1 join t2;) 或者是0个表 (select 1+1;)|
|`WHERE where_condition` | Where 子句用于设置过滤条件，查询结果中只会包含满足条件的数据|
|`GROUP BY` | GroupBy 子句用于对查询结果集进行分组|
|`HAVING where_condition` | Having 子句与 Where 子句作用类似，Having 子句可以让过滤 GroupBy 后的各种数据，Where 子句用于在聚合前过滤记录。|
|`ORDER BY` | OrderBy 子句用于指定结果排序顺序，可以按照列、表达式或者是 select_expr 列表中某个位置的字段进行排序。|
|`LIMIT` | Limit 子句用于限制结果条数。Limit 接受一个或两个数字参数，如果只有一个参数，那么表示返回数据的最大行数；如果是两个参数，那么第一个参数表示返回数据的第一行的偏移量（第一行数据的偏移量是 0），第二个参数指定返回数据的最大条目数。|
|`FOR UPDATE` | 对查询结果集所有数据上读锁，以监测其他事务对这些的并发修改。TiDB 使用[乐观事务模型](https://github.com/pingcap/docs-cn/blob/master/op-guide/mysql-compatibility.md#事务)在语句执行期间不会检测锁冲突，在事务的提交阶段才会检测事务冲突，如果执行 Select For Update 期间，有其他事务修改相关的数据，那么包含 Select For Update 语句的事务会提交失败。|
|`LOCK IN SHARE MODE` | TiDB 出于兼容性解析这个语法，但是不做任何处理|

# Insert 语句

Insert 语句用于向数据库中插入数据，TiDB 兼容 MySQL Insert 语句的所有语法。

## 语法定义

```sql
InsertStatement:
INSERT [LOW_PRIORITY | DELAYED | HIGH_PRIORITY] [IGNORE]
    [INTO] tbl_name
    insert_values
    [ON DUPLICATE KEY UPDATE assignment_list]

insert_values:
    [(col_name [, col_name] ...)]
    {VALUES | VALUE} (expr_list) [, (expr_list)] ...
|   SET assignment_list
|   [(col_name [, col_name] ...)]
    SELECT ...

expr_list:
    expr [, expr] ...

assignment:
    col_name = expr

assignment_list:
    assignment [, assignment] ...
```

## 语法元素说明

|语法元素 | 说明|
|-------- | -----------|
|`LOW_PRIORITY` | 该语句为低优先级语句，TiDB 在执行阶段会降低这条语句的优先级|
|`DELAYED` | TiDB 出于兼容性解析这个语法，但是不做任何处理|
|`HIGH_PRIORITY` | 该语句为高优先级语句，TiDB 在执行阶段会优先处理这条语句|
|`IGNORE` | 如果发生 Uniq Key 冲突，则忽略插入的数据，不报错|
|`tbl_name` | 要插入的表名|
|`insert_values` | 待插入的数据，下面一节会详细描述|
|`ON DUPLICATE KEY UPDATE assignment_list` | 如果发生 Uniq Key 冲突，则舍弃要插入的数据，改用 assignment_list 更新已存在的行|

### insert_values

待插入的数据集，可以用以下三种方式指定：

* Value List

将被插入的数据值写入列表中，例如：

```sql
CREATE TABLE tbl_name (
    a int,
    b int,
    c int
);
INSERT INTO tbl_name VALUES(1,2,3),(4,5,6),(7,8,9);
```

上面的例子中，`(1,2,3),(4,5,6),(7,8,9)` 即为 Value List，其中每个括号内部的数据表示一行数据，这个例子中插入了三行数据。Insert 语句也可以只给部分列插入数据，这种情况下，需要在 Value List 之前加上 ColumnName List，如：


```sql
INSERT INTO tbl_name (a,c) VALUES(1,2),(4,5),(7,8);
```

上面的例子中，每行数据只指定了 a 和 c 这两列的值，b 列的值会设为 Null。

* Assignment List

通过赋值列表指定插入的数据，例如：

```sql
INSERT INTO tbl_name a=1, b=2, c=3;
```

这种方式每次只能插入一行数据，每列的值通过赋值列表制定。

* Select Statement

待插入的数据集是通过一个 Select 语句获取，要插入的列是通过 Select 语句的 Schema 获得。例如：
```sql
CREATE TABLE tbl_name1 (
    a int,
    b int,
    c int
);
INSERT INTO tbl_name SELECT * from tbl_name1;
```

上面的例子中，从 `tbl_name1` 中查询出数据，插入 `tbl_name` 中。