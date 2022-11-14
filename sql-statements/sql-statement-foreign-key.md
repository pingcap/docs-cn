---
title: FOREIGN KEY
summary: TiDB 数据库中 FOREIGN KEY 的使用概况。
---

# FOREIGN KEY

外键是 TiDB 从 v6.6.0 开始支持的**实验特性**，允许跨表交叉引用相关数据，以及外键约束，有助于保持相关数据的一致性。

外键是在子表中定义的，语法如下：

```sql
[CONSTRAINT identifier] FOREIGN KEY
    [identifier] (col_name, ...)
    REFERENCES tbl_name (col_name,...)
    [ON DELETE reference_option]
    [ON UPDATE reference_option]

reference_option:
    RESTRICT | CASCADE | SET NULL | NO ACTION | SET DEFAULT
```

> **警告：**
> 
> 由于外键还是实验特性，所有并没有默认开启该功能，需要手动设置以下变量后打开该功能：
> `set @@global.tidb_enable_foreign_key=1;`
> 另一个和外键相关的变量 `foreign_key_checks` 的默认值目前是 0，如要使用外键的约束检查和级联行为，也需要手动设置该变量的值为 1：
> `set @@foreign_key_checks=1;`

## 命名

外键的命名规则如下：

- 如果有定义 `CONSTRAINT identifier`，就用这个定义的名称。
- 如果没有定义 `CONSTRAINT identifier`，但有定义 `FOREIGN KEY identifier`，就用这个定义的名称。
- 如果 `CONSTRAINT identifier` 和 `FOREIGN KEY identifier` 都没有指定名称，则自动生成一个名称，例如 `fk_1`、`fk_2`、`fk_3` 等，以此类推。
- 名称在当前表的所有外键中必须是唯一的，否则创建时会报错：`ERROR 1826: Duplicate foreign key constraint name 'fk'`。

## 条件和限制

外键有以下条件和限制：

- 父表和子表都不能是临时表。
- 创建外键时，需要用户对父表有 `REFERENCES` 权限。
- 父表和子表中外键引用的 `Column` 必须是相同的数据类型，例如 `INTEGER` 和 `DECIMAL` 的大小和精度也必须相同，`String` 类型的长度，字符集（charset）和排序规则（collation）也必须相同。
- 外键中的 `Column` 引用不能是它自己。
- 外键中的 `Column` 和引用的父表中的 `Column` 都必须有对应的索引，索引中的 `Column` 顺序必须和外键的 `Column` 顺序一样，这样在执行外键约束检查时可以用索引而避免用全表扫。创建外键时如果父表中没有对应的外键索引，则会报错：`ERROR 1822: Failed to add the foreign key constraint. Missing index for constraint 'fk' in the referenced table 't'`。创建外键时如果子表中没有对应的索引，则会自动创建一个索引，索引名和外键名一样。
- 不支持在 `BLOB` 和 `TEXT` 类型的 `Column` 上创建外键。
- 不支持在分区表上创建外键。
- 不支持在 `VIRTUAL GENERATED COLUMN` 上创建外键。

## 引用操作

当 `UPDATE` 或 `DELETE` 操作影响父表中的外键值时，其在子表中相匹配的外键值取决于外键定义中 `ON UPDATE` 和 `ON DELETE` 定义的引用操作，引用操作包括：

- `CASCADE`：当 `UPDATE` 或 `DELETE` 父表中的行数据时，自动级联更新或删除子表中的匹配行数据。级联操作会用深度优先方式执行。
- `SET NULL`：当 `UPDATE` 或 `DELETE` 父表中的行数据时，自动将子表中匹配的外键列数据设置为 `NULL`。
- `RESTRICT`：如果子表中存在外键匹配的行数据，则拒绝 `UPDATE` 或 `DELETE` 父表的操作。
- `NO ACTION`：行为和 `RESTRICT` 一样。
- `SET DEFAULT`：行为和 `RESTRICT` 一样。

如果父表中没有匹配的外键值，则拒绝 `INSERT` 或 `UPDATE` 子表的操作。

如果外键定义中没有指定 `ON DELETE` 或者 `ON UPDATE`，则默认的行为是 `NO ACTION`。

如果外键是定义在 `STORED GENERATED COLUMN` 上的，则不支持使用 `CASCADE`，`SET NULL` 和 `SET DEFAULT` 引用操作。

## 外键使用示例

下面的示例通过单列外键关联父表和子表：

{{< copyable "sql" >}}

```sql
CREATE TABLE parent (
    id INT KEY
);

CREATE TABLE child (
    id INT,
    pid INT,
    INDEX idx_pid (pid),
    FOREIGN KEY (pid) REFERENCES parent(id) ON DELETE CASCADE
);
```

下面是一个更复杂的示例，其中 `product_order` 表有 2 个外键分别引用其他两个表。一个外键引用 `product` 表中的两列索引。另一个引用 `customer` 表中的单列索引：

{{< copyable "sql" >}}

```sql
CREATE TABLE product (
    category INT NOT NULL, 
    id INT NOT NULL,
    price DECIMAL(20,10),
    PRIMARY KEY(category, id)
);

CREATE TABLE customer (
    id INT KEY
);

CREATE TABLE product_order (
    id INT NOT NULL AUTO_INCREMENT,
    product_category INT NOT NULL,
    product_id INT NOT NULL,
    customer_id INT NOT NULL,

    PRIMARY KEY(id),
    INDEX (product_category, product_id),
    INDEX (customer_id),

    FOREIGN KEY (product_category, product_id)
      REFERENCES product(category, id)
      ON UPDATE CASCADE ON DELETE RESTRICT,

    FOREIGN KEY (customer_id)
      REFERENCES customer(id)
);
```

## 新增外键约束

可以使用下面 `ALTER TABLE` 语句来新增一个外键约束：

```sql
ALTER TABLE table_name
    ADD [CONSTRAINT [identifier]] FOREIGN KEY
    [identifier] (col_name, ...)
    REFERENCES tbl_name (col_name,...)
    [ON DELETE reference_option]
    [ON UPDATE reference_option]
```

外键可以是自引用的（引用同一个表）。使用 ALTER TABLE 向表添加外键约束时，请先在外键引用的列上创建索引。

## 删除外键约束

可以使用下面 `ALTER TABLE` 语句来删除一个外键约束：

```sql
ALTER TABLE table_name DROP FOREIGN KEY fk_identifier;
```

如果外键约束在创建时定义了名称，则可以引用该名称来删除外键约束。否则约束名称是自动生成的，您可以使用 `SHOW CREATE TABLE` 查看外键名称：

```sql
mysql> SHOW CREATE TABLE child\G
*************************** 1. row ***************************
       Table: child
Create Table: CREATE TABLE `child` (
  `id` int(11) DEFAULT NULL,
  `pid` int(11) DEFAULT NULL,
  KEY `idx_pid` (`pid`),
  CONSTRAINT `fk_1` FOREIGN KEY (`pid`) REFERENCES `test`.`parent` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
```

## 外键约束检查

TiDB 支持是否开启外键约束检查，由系统变量 [`foreign_key_checks`](/system-variables.md#foreign_key_checks) 控制，其默认值是 `ON`，即开启外键约束检查，它有 `GLOBAL` 和 `SESSION` 两种作用域。在一般的操作中保持该变量开启来保证外键引用关系的完整性。

关闭 [`foreign_key_checks`](/system-variables.md#foreign_key_checks) 的作用如下：

- 当删除一个被外键引用的父表时，只有关闭外键约束检查时才能删除成功。
- 当给数据库导入数据时，创建表的顺序可能和外键依赖顺序不一样而导致创建表报错，只有关闭外键约束检查时才能创建表成功，另外，导入数据时关闭外键约束检查也能加快导数据的速度。
- 当给数据库导入数据时，如果先导入子表的数据会报错，只有关闭外键约束检查时才能成功先导入子表的数据。
- 执行有关外键的 `ALTER TABLE` 操作时，关于外键约束检查才能执行成功。

当关闭关键约束检查时，不会执行外键约束检查以及引用操作，但以下场景除外：

- `ALTER TABLE` 执行时如果导致外键的定义不正确，则依然会执行报错。
- 删除外键所需的索引时，需要先删除外键，否则删除外键会执行报错。
- 创建外键时，如果不符合外键的条件或限制，则依然会执行报错。

## 锁

在 `INSERT` 或者 `UPDATE` 子表时，外键约束会检查父表中是否存在对应的外键值，并对父表中的该行数据上锁，避免该外键值被其他操作删除，导致破坏外键约束。这里的上锁行为相当于对父表中外键值所在行做 `SELECT FOR UPDATE` 操作。因为 TiDB 目前暂不支持 `LOCK IN SHARE MODE`，所以如果在并发写入子表且引用的外键值大部分都一样时，可能会有比较严重的锁冲突，建议在大批量写入子表数据时，关闭 [`foreign_key_checks`](/system-variables.md#foreign_key_checks)。

## 外键的定义和元信息

可以使用 `SHOW CREATE TABLE` 语句查看外键的定义：

```sql
mysql> SHOW CREATE TABLE child\G
*************************** 1. row ***************************
       Table: child
Create Table: CREATE TABLE `child` (
  `id` int(11) DEFAULT NULL,
  `pid` int(11) DEFAULT NULL,
  KEY `idx_pid` (`pid`),
  CONSTRAINT `fk_1` FOREIGN KEY (`pid`) REFERENCES `test`.`parent` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
```