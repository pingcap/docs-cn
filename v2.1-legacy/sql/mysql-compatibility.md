---
title: 与 MySQL 兼容性对比
category: compatibility
---

# 与 MySQL 兼容性对比

TiDB 支持包括跨行事务、JOIN 及子查询在内的绝大多数 MySQL 5.7 的语法，用户可以直接使用现有的 MySQL 客户端连接。如果现有的业务已经基于 MySQL 开发，大多数情况不需要修改代码即可直接替换单机的 MySQL。

包括现有的大多数 MySQL 运维工具（如 PHPMyAdmin, Navicat, MySQL Workbench 等），以及备份恢复工具（如 mysqldump, mydumper/myloader）等都可以直接使用。

不过一些特性由于在分布式环境下没法很好的实现，目前暂时不支持或者是表现与 MySQL 有差异。

一些 MySQL 语法在 TiDB 中可以解析通过，但是不会做任何后续的处理，例如 Create Table 语句中 `Engine` 以及 `Partition` 选项，都是解析并忽略。更多兼容性差异请参考具体的文档。

## 不支持的特性

* 存储过程与函数
* 视图
* 触发器
* 事件
* 自定义函数
* 外键约束
* 全文函数与索引
* 空间函数与索引
* 非 `utf8` 字符集
* `BINARY` 之外的排序规则
* 增加主键
* 删除主键
* SYS schema
* MySQL 追踪优化器
* XML 函数
* X Protocol
* Savepoints
* 列级权限
* `CREATE TABLE tblName AS SELECT stmt` 语法
* `CREATE TEMPORARY TABLE` 语法
* `XA` 语法（TiDB 内部使用两阶段提交，但并没有通过 SQL 接口公开）

## 与 MySQL 有差异的特性

### 自增 ID

TiDB 的自增 ID (Auto Increment ID) 只保证自增且唯一，并不保证连续分配。TiDB 目前采用批量分配的方式，所以如果在多台 TiDB 上同时插入数据，分配的自增 ID 会不连续。

在集群中有多个 tidb-server 实例时，如果表结构中有自增 ID，建议不要混用缺省值和自定义值，否则在如下情况下会遇到问题。

假设有这样一个带有自增 ID 的表：

```sql
create table t(id int unique key auto_increment, c int);
```

TiDB 实现自增 ID 的原理是每个 tidb-server 实例缓存一段 ID 值用于分配（目前会缓存 30000 个 ID），用完这段值再去取下一段。

假设集群中有两个 tidb-server 实例 A 和 B（A 缓存 [1,30000] 的自增 ID，B 缓存 [30001,60000] 的自增 ID），依次执行如下操作：

1. 客户端向 B 插入一条将 `id` 设置为 1 的语句 `insert into t values (1, 1)`，并执行成功。
2. 客户端向 A 发送 Insert 语句 `insert into t (c) (1)`，这条语句中没有指定 `id` 的值，所以会由 A 分配，当前 A 缓存了 [1, 30000] 这段 ID，所以会分配 1 为自增 ID 的值，并把本地计数器加 1。而此时数据库中已经存在 `id` 为 1 的数据，最终返回 `Duplicated Error` 错误。

### Performance schema

Performance schema 表在 TiDB 中返回结果为空。TiDB 使用 [Prometheus 和 Grafana](https://pingcap.com/docs/op-guide/monitor/#use-prometheus-and-grafana) 来监测性能指标。

### 内建函数

TiDB 支持常用的 MySQL 内建函数，但是不是所有的函数都已经支持，具体请参考[语法文档](https://pingcap.github.io/sqlgram/#FunctionCallKeyword)。

### DDL

TiDB 实现了 F1 的异步 Schema 变更算法，DDL 执行过程中不会阻塞线上的 DML 操作。目前已经支持的 DDL 包括：

+ Create Database
+ Drop Database
+ Create Table
+ Drop Table
+ Add Index
+ Drop Index
+ Add Column
+ Drop Column
+ Alter Column
+ Change Column
+ Modify Column
+ Truncate Table
+ Rename Table
+ Create Table Like

以上语句还有一些支持不完善的地方，具体包括如下：

+ Add/Drop primary key 操作目前不支持。
+ Add Index/Column 操作不支持同时创建多个索引或列。
+ Drop Column 操作不支持删除的列为主键列或索引列。
+ Add Column 操作不支持同时将新添加的列设为主键或唯一索引，也不支持将此列设成 auto_increment 属性。
+ Change/Modify Column 操作目前支持部分语法，细节如下：
    - 在修改类型方面，只支持整数类型之间修改，字符串类型之间修改和 Blob 类型之间的修改，且只能使原类型长度变长。此外，不能改变列的 unsigned/charset/collate 属性。这里的类型分类如下：
        * 具体支持的整型类型有：TinyInt，SmallInt，MediumInt，Int，BigInt。
        * 具体支持的字符串类型有：Char，Varchar，Text，TinyText，MediumText，LongText。
        * 具体支持的 Blob 类型有：Blob，TinyBlob，MediumBlob，LongBlob。
    - 在修改类型定义方面，支持的包括 default value，comment，null，not null 和 OnUpdate。
    - 支持 LOCK [=] {DEFAULT|NONE|SHARED|EXCLUSIVE} 语法，但是不做任何事情（pass through）。
    - 不支持对enum类型的列进行修改

### 事务模型

TiDB 使用乐观事务模型，在执行 `Update`、`Insert`、`Delete` 等语句时，只有在提交过程中才会检查写写冲突，而不是像 MySQL 一样使用行锁来避免写写冲突。类似的，诸如 `GET_LOCK()` 和 `RELEASE_LOCK()` 等函数以及 `SELECT .. FOR UPDATE` 之类的语句在 TiDB 和 MySQL 中的执行方式并不相同。所以业务端在执行 SQL 语句后，需要注意检查 commit 的返回值，即使执行时没有出错，commit 的时候也可能会出错。

### 大事务

由于 TiDB 分布式两阶段提交的要求，修改数据的大事务可能会出现一些问题。因此，TiDB 特意对事务大小设置了一些限制以减少这种影响：

* 每个键值对不超过 6MB
* 键值对的总数不超过 300,000
* 键值对的总大小不超过 100MB

### 小事务

由于 TiDB 中的每个事务都需要跟 PD leader 进行两次 round trip，TiDB 中的小事务相比于 MySQL 中的小事务延迟更高。以如下的 query 为例，用显式事务代替 `auto_commit`，可优化该 query 的性能。

```sql
# 使用 auto_commit 的原始版本
UPDATE my_table SET a='new_value' WHERE id = 1; 
UPDATE my_table SET a='newer_value' WHERE id = 2;
UPDATE my_table SET a='newest_value' WHERE id = 3;

# 优化后的版本
START TRANSACTION;
UPDATE my_table SET a='new_value' WHERE id = 1; 
UPDATE my_table SET a='newer_value' WHERE id = 2;
UPDATE my_table SET a='newest_value' WHERE id = 3;
COMMIT;
```

### 单线程的 workload

由于 TiDB 中的 workload 是分布式的，TiDB 中单线程的 workload 性能相比于单实例部署的 MySQL 较低。这与 TiDB 中的小事务延迟较高的情況类似。

### Load data

+  语法：

    ```sql
    LOAD DATA LOCAL INFILE 'file_name' INTO TABLE table_name
        {FIELDS | COLUMNS} TERMINATED BY 'string' ENCLOSED BY 'char' ESCAPED BY 'char'
        LINES STARTING BY 'string' TERMINATED BY 'string'
        IGNORE n LINES
        (col_name ...);
    ```

    其中 ESCAPED BY 目前只支持 '/\/\'。

+   事务的处理：

    TiDB 在执行 load data 时，默认每 2 万行记录作为一个事务进行持久化存储。如果一次 load data 操作插入的数据超过 2 万行，那么会分为多个事务进行提交。如果某个事务出错，这个事务会提交失败，但它前面的事务仍然会提交成功，在这种情况下一次 load data 操作会有部分数据插入成功，部分数据插入失败。而 MySQL 中会将一次 load data 操作视为一个事务，如果其中发生失败情况，将会导致整个 load data 操作失败。

### 存储引擎

出于兼容性原因，TiDB 支持使用备用存储引擎创建表的语法。元数据命令将表描述为 InnoDB 存储引擎：

```sql
mysql> CREATE TABLE t1 (a INT) ENGINE=MyISAM;
Query OK, 0 rows affected (0.14 sec)
 mysql> SHOW CREATE TABLE t1\G
*************************** 1. row ***************************
       Table: t1
Create Table: CREATE TABLE `t1` (
  `a` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
1 row in set (0.00 sec)
```

从架构上讲，TiDB 确实支持类似 MySQL 的存储引擎抽象，在启动 TiDB（通常是 `tikv`）时 [`--store`](../sql/server-command-option.md#--store) 选项指定的引擎中创建用户表。

### SQL 模式

TiDB 支持 MySQL 5.7 中 **绝大多数的 SQL 模式**，以下几种模式除外：

- TiDB 暂不支持 `ALLOW_INVALID_DATES` 模式。详情参见 [TiDB #8263](https://github.com/pingcap/tidb/issues/8263)。
- TiDB 不支持兼容模式（例如 `ORACLE` 和 `POSTGRESQL`）。MySQL 5.7 已弃用兼容模式，MySQL 8.0 已移除兼容模式。
- TiDB 中的 `ONLY_FULL_GROUP_BY` 与 MySQL 5.7 相比有细微的 [语义差别](../sql/aggregate-group-by-functions.md#与-mysql-的区别)，此问题日后将予以解决。
- `NO_DIR_IN_CREATE` 和 `NO_ENGINE_SUBSTITUTION` 这两种 SQL 模式用于解决兼容问题，但并不适用于 TiDB。

### EXPLAIN

TiDB 的 `EXPLAIN` 命令返回的查询执行计划的输出与 MySQL 不同。更多内容参见 [理解 TiDB 执行计划](../sql/understanding-the-query-execution-plan.md)。

### 默认设置的区别

+ 默认字符集不同：
    + TiDB 中为 `utf8`，相当于 MySQL 的 `utf8mb4`
    + MySQL 5.7 中为 `latin1`，但在 MySQL 8.0 中修改为 `utf8mb4`
+ 默认排序规则不同：
    + MySQL 5.7 中使用 `latin1_swedish_ci`
    + TiDB 使用 `binary`
+ 默认 SQL mode 不同：
    + TiDB 中为 `STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION`
    + MySQL 中为 `ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION`
+ `lower_case_table_names` 的默认值不同：
    + TiDB 中该值默认为 2，并且目前 TiDB 只支持设置该值为 2
    + MySQL 中默认设置：
        + Linux 系统中该值为 0
        + Windows 系统中该值为 1
        + macOS 系统中该值为 2
+ `explicit_defaults_for_timestamp` 的默认值不同：
    + TiDB 中该值默认为 `ON`，并且目前 TiDB 只支持设置该值为 `ON`
    + MySQL 中默认设置：
        + MySQL 5.7：`OFF`
        + MySQL 8.0：`ON`
