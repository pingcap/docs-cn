---
title: 数据操作语言
category: reference
aliases: ['/docs-cn/sql/dml/']
---

# TiDB 数据操作语言

数据操作语言 (Data Manipulation Language, DML) 用于帮助用户实现对数据库的基本操作，比如查询、写入、删除和修改数据库中的数据。

TiDB 支持的数据操作语言包括 Select，Insert，Delete，Update 和 Replace。

## Select 语句

Select 语句用于从数据库中查询数据。

### 语法定义

```sql
SELECT
    [ALL | DISTINCT | DISTINCTROW ]
      [HIGH_PRIORITY]
      [STRAIGHT_JOIN]
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

|语法元素 | 说明 |
| --------------------- | -------------------------------------------------- |
|`ALL`、`DISTINCT`、`DISTINCTROW` | 查询结果集中可能会包含重复值。指定 DISTINCT/DISTINCTROW 则在查询结果中过滤掉重复的行；指定 ALL 则列出所有的行。默认为 ALL。|
|`HIGH_PRIORITY` | 该语句为高优先级语句，TiDB 在执行阶段会优先处理这条语句|
|`SQL_CALC_FOUND_ROWS` | TiDB 出于兼容性解析这个语法，但是不做任何处理|
|`SQL_CACHE`、`SQL_NO_CACHE` | 是否把请求结果缓存到 TiKV (RocksDB) 的 `BlockCache` 中。对于一次性的大数据量的查询，比如 `count(*)` 查询，为了避免冲掉 `BlockCache` 中用户的热点数据，建议填上 `SQL_NO_CACHE` |
|`STRAIGHT_JOIN`|`STRAIGHT_JOIN` 会强制优化器按照 `FROM` 子句中所使用的表的顺序做联合查询。当优化器选择的 Join 顺序并不优秀时，你可以使用这个语法来加速查询的执行|
|`select_expr` | 投影操作列表，一般包括列名、表达式，或者是用 '\*' 表示全部列|
|`FROM table_references` | 表示数据来源，数据来源可以是一个表（`select * from t;`）或者是多个表 (`select * from t1 join t2;`) 或者是0个表 (`select 1+1 from dual;`, 等价于 `select 1+1;`)|
|`WHERE where_condition` | Where 子句用于设置过滤条件，查询结果中只会包含满足条件的数据|
|`GROUP BY` | GroupBy 子句用于对查询结果集进行分组|
|`HAVING where_condition` | Having 子句与 Where 子句作用类似，Having 子句可以让过滤 GroupBy 后的各种数据，Where 子句用于在聚合前过滤记录。|
|`ORDER BY` | OrderBy 子句用于指定结果排序顺序，可以按照列、表达式或者是 `select_expr` 列表中某个位置的字段进行排序。|
|`LIMIT` | Limit 子句用于限制结果条数。Limit 接受一个或两个数字参数，如果只有一个参数，那么表示返回数据的最大行数；如果是两个参数，那么第一个参数表示返回数据的第一行的偏移量（第一行数据的偏移量是 0），第二个参数指定返回数据的最大条目数。|
|`FOR UPDATE` | 对查询结果集所有行上锁（对于在查询条件内，但是不在结果集的行，将不会加锁，如事务启动后由其他事务写入的行），以监测其他事务对这些的并发修改。TiDB 使用[乐观事务模型](/dev/reference/transactions/transaction-model.md#事务模型)在语句执行期间不会检测锁，因此，不会像 PostgreSQL 之类的数据库一样，在当前事务结束前阻止其他事务执行 UPDATE、DELETE 和 SELECT FOR UPDATE。在事务的提交阶段 SELECT FOR UPDATE 读到的行，也会进行两阶段提交，因此，它们也可以参与事务冲突检测。如发生写入冲突，那么包含 SELECT FOR UPDATE 语句的事务会提交失败。如果没有冲突，事务将成功提交，当提交结束时，这些被加锁的行，会产生一个新版本，可以让其他尚未提交的事务，在将来提交时发现写入冲突。|
|`LOCK IN SHARE MODE` | TiDB 出于兼容性解析这个语法，但是不做任何处理|

## Insert 语句

Insert 语句用于向数据库中插入数据，TiDB 兼容 MySQL Insert 语句的所有语法。

### 语法定义

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

### 语法元素说明

| 语法元素 | 说明 |
| -------------- | --------------------------------------------------------- |
| `LOW_PRIORITY` | 该语句为低优先级语句，TiDB 在执行阶段会降低这条语句的优先级 |
| `DELAYED` | TiDB 出于兼容性解析这个语法，但是不做任何处理 |
| `HIGH_PRIORITY` | 该语句为高优先级语句，TiDB 在执行阶段会优先处理这条语句|
| `IGNORE` | 如果发生 Uniq Key 冲突，则忽略插入的数据，不报错 |
| `tbl_name` | 要插入的表名 |
| `insert_values` | 待插入的数据，下面一节会详细描述 |
| `ON DUPLICATE KEY UPDATE assignment_list` | 如果发生 Uniq Key 冲突，则舍弃要插入的数据，改用 assignment_list 更新已存在的行 |

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
INSERT INTO tbl_name SET a=1, b=2, c=3;
```

这种方式每次只能插入一行数据，每列的值通过赋值列表指定。

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

## Delete 语句

Delete 语句用于删除数据库中的数据，TiDB 兼容 MySQL Delete 语句除 PARTITION 之外的所有语法。Delete 语句主要分为单表删除和多表删除两种，下面分开描述。

### 单表删除

这种语法用于删除的数据只会涉及一个表的情况。

### 语法定义

```sql
DELETE [LOW_PRIORITY] [QUICK] [IGNORE] FROM tbl_name
    [WHERE where_condition]
    [ORDER BY ...]
    [LIMIT row_count]
```

### 多表删除

这种语法用于删除的数据会涉及多张表的情况。一共有两种写法：

```sql
DELETE [LOW_PRIORITY] [QUICK] [IGNORE]
    tbl_name[.*] [, tbl_name[.*]] ...
    FROM table_references
    [WHERE where_condition]

DELETE [LOW_PRIORITY] [QUICK] [IGNORE]
    FROM tbl_name[.*] [, tbl_name[.*]] ...
    USING table_references
    [WHERE where_condition]
```

删除多个表的数据的时候，可以用这两种语法。这两种写法都可以指定从多个表查询数据，但只删除其中一些表的数据。在第一种语法中，只会删除 `FROM` 关键字之前的 Table 列表中所列 Table 的表中的数据。对于第二种写法，只会删除 `FROM` 之后 `USING` 之前的 Table 列表中的所列 Table 中的数据。

### 语法元素说明

| 语法元素 | 说明 |
| -------------- | --------------------------------------------------------- |
| `LOW_PRIORITY` | 该语句为低优先级语句，TiDB 在执行阶段会降低这条语句的优先级 |
| `QUICK` | TiDB 出于兼容性解析这个语法，但是不做任何处理 |
| `IGNORE` | TiDB 出于兼容性解析这个语法，但是不做任何处理|
| `tbl_name` | 要删除数据的表名 |
| `WHERE where_condition` | Where 表达式，只删除满足表达式的那些行 |
| `ORDER BY` | 对待删除数据集进行排序 |
| `LIMIT row_count` | 只对待删除数据集中排序前 row_count 行的内容进行删除 |

## Update 语句

Update 语句用于更新表中的数据。

### 语法定义

Update 语句一共有两种语法，分别用于更新单表数据和多表数据。

### 单表 Update

```sql
UPDATE [LOW_PRIORITY] [IGNORE] table_reference
    SET assignment_list
    [WHERE where_condition]
    [ORDER BY ...]
    [LIMIT row_count]

assignment:
    col_name = value

assignment_list:
    assignment [, assignment] ...
```

单表 Update 语句会更新 Table 中现有行的指定列。`SET assignment_list` 指定了要更新的列名，以及要赋予地新值。 Where/OrderBy/Limit 子句一起用于从 Table 中查询出待更新的数据。

### 多表 Update

```sql
UPDATE [LOW_PRIORITY] [IGNORE] table_references
    SET assignment_list
    [WHERE where_condition]
```

多表更新语句用于将 `table_references` 中满足 Where 子句的数据地指定列赋予新的值。

### 语法元素说明

| 语法元素 | 说明 |
| -------------- | --------------------------------------------------------- |
| `LOW_PRIORITY` | 该语句为低优先级语句，TiDB 在执行阶段会降低这条语句的优先级 |
| `IGNORE` | TiDB 出于兼容性解析这个语法，但是不做任何处理|
| `table_reference` | 待更新的 Table 名称 |
| `table_references` | 待更新的 Table 名称列表 |
| `SET assignment_list` | 待更新的列名以及目标值 |
| `WHERE where_condition` | Where 表达式，只更新满足表达式的那些行 |
| `ORDER BY` | 对待更新数据集进行排序 |
| `LIMIT row_count` | 只对待更新数据集中排序前 row_count 行的内容进行更新 |

## Replace 语句

Replace 语句是 MySQL 对标准 SQL 语法的扩展，其行为和 Insert 语句一样，但是当现有数据中有和待插入数据在 PRIMARY KEY 或者 UNIQUE KEY 冲突的情况下，会先删除旧数据，再插入新数据。

### 语法定义

```sql
REPLACE [LOW_PRIORITY | DELAYED]
    [INTO] tbl_name
    [(col_name [, col_name] ...)]
    {VALUES | VALUE} (value_list) [, (value_list)] ...

REPLACE [LOW_PRIORITY | DELAYED]
    [INTO] tbl_name
    SET assignment_list

REPLACE [LOW_PRIORITY | DELAYED]
    [INTO] tbl_name
    [(col_name [, col_name] ...)]
    SELECT ...
```

### 语法元素说明

| 语法元素 | 说明 |
| -------------- | --------------------------------------------------------- |
| `LOW_PRIORITY` | 该语句为低优先级语句，TiDB 在执行阶段会降低这条语句的优先级 |
| `DELAYED` | TiDB 出于兼容性解析这个语法，但是不做任何处理|
| `tbl_name` | 待更新的 Table 名称 |
| `value_list` | 待插入的数据 |
| `SET assignment_list` | 待更新的列名以及目标值 |
| `SELECT ...` | 待插入的数据集，该数据集来自于一个 `Select` 语句 |
