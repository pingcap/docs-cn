---
title: Insert 语句
category: user guide
---

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
