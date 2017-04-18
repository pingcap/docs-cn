---
title: 与 MySQL 兼容性对比
category: compatibility
---

# 与 MySQL 兼容性对比

TiDB 支持包括跨行事务，JOIN 及子查询在内的绝大多数 MySQL 的语法，用户可以直接使用现有的 MySQL 客户端连接。如果现有的业务已经基于 MySQL 开发，大多数情况不需要修改代码即可直接替换单机的 MySQL。

包括现有的大多数 MySQL 运维工具（如 PHPMyAdmin, Navicat, MySQL Workbench 等），以及备份恢复工具（如 mysqldump, mydumper/myloader）等都可以直接使用。

不过一些特性由于在分布式环境下没法很好的实现，目前暂时不支持或者是表现与 MySQL 有差异。

## 不支持的特性

* 存储过程
* 视图
* 触发器
* 自定义函数
* 外键约束
* 全文索引
* 空间索引
* 非 UTF8 字符集
* Json 类型

## 与 MySQL 有差异的特性
### 自增 ID
TiDB 的自增 ID (Auto Increment ID) 只保证自增且唯一，并不保证连续分配。TiDB 目前采用批量分配的方式，所以如果在多台 TiDB 上同时插入数据，分配的自增 ID 会不连续。

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
+ Crete Table Like

以上语句还有一些支持不完善的地方，具体包括如下：

+ Add Index/Column 操作不支持同时创建多个索引或列。
+ Drop Column 操作不支持删除的列为主键列或索引列。
+ Add Column 操作不支持同时将新添加的列设为主键或唯一索引，也不支持将此列设成 auto_increment 属性。
+ Change/Modify Column 操作目前支持部分语法，细节如下：
	- 在修改类型方面，只支持整数类型之间修改，字符串类型之间修改和 Blob 类型之间的修改，且只能使原类型长度变长。此外，不能改变列的 unsigned/charset/collate 属性。这里的类型分类如下：
	    * 具体支持的整型类型有：TinyInt，SmallInt，MediumInt，Int，BigInt。
	    * 具体支持的字符串类型有：Char，Varchar，Text，TinyText，MediumText，LongText。
	    * 具体支持的 Blob 类型有：Blob，TinyBlob，MediumBlob，LongBlob。
	- 在修改类型定义方面，支持的包括 default value，comment，null，not null 和 OnUpdate，但是不支持从 null 到 not null 的修改。
	- 在关键字方面，不支持 First/After 关键字。

### 事务
TiDB 使用乐观事务模型，在执行 Update、Insert、Delete 等语句时，只有在提交过程中才会检查写写冲突，而不是像 MySQL 一样使用行锁来避免写写冲突。所以业务端在执行 SQL 语句后，需要注意检查 commit 的返回值，即使执行时没有出错，commit的时候也可能会出错。

### Load data
TiDB 在执行 load data 时，默认每 2 万行记录作为一个事务进行持久化存储。如果一次 load data 操作插入的数据超过 2 万行，那么会分为多个事务进行提交。如果某个事务出错，这个事务会提交失败，但它前面的事务仍然会提交成功，在这种情况下一次 load data 操作会有部分数据插入成功，部分数据插入失败。而 MySQL 中会将一次 load data 操作视为一个事务，如果其中发生失败情况，将会导致整个 load data 操作失败。
