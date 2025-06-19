---
title: SQL
summary: 了解 TiDB 的 SQL 概念。
---

# SQL

TiDB 高度兼容 MySQL 协议以及 MySQL 5.7 和 MySQL 8.0 的常用功能和语法。MySQL 的生态工具（PHPMyAdmin、Navicat、MySQL Workbench、DBeaver 和[更多](https://docs.pingcap.com/tidb/v7.2/dev-guide-third-party-support#gui)）和 MySQL 客户端都可以用于 TiDB。

然而，TiDB 不支持 MySQL 的某些功能。这可能是因为现在有更好的方法来解决问题（比如使用 JSON 而不是 XML 函数），或者是当前需求相对于所需努力较小（比如存储过程和函数）。此外，某些功能在分布式系统中可能难以实现。更多信息，请参见 [MySQL 兼容性](/mysql-compatibility.md)。

## SQL 语句

SQL 语句是 SQL（结构化查询语言）中由标识符、参数、变量、数据类型和保留的 SQL 关键字组成的命令或指令。它指示数据库执行特定操作，如检索、修改或管理数据和数据库结构。

TiDB 使用的 SQL 语句旨在遵循 ISO/IEC SQL 标准，必要时为 MySQL 和 TiDB 特定语句提供扩展。

SQL 根据其功能分为以下 4 种类型：

- DDL（数据定义语言）：用于定义数据库对象，包括数据库、表、视图和索引。有关 TiDB 中的 DDL 语句，请参见[架构管理/数据定义语句 (DDL)](/sql-statements/sql-statement-overview.md#schema-management--data-definition-statements-ddl)。

- DML（数据操作语言）：用于操作应用程序相关的记录。有关 TiDB 中的 DML 语句，请参见[数据操作语句 (DML)](/sql-statements/sql-statement-overview.md#data-manipulation-statements-dml)。

- DQL（数据查询语言）：用于在条件过滤后查询记录。

- DCL（数据控制语言）：用于定义访问权限和安全级别。

要了解 TiDB 中 SQL 语句的概览，请参见 [SQL 语句概览](/sql-statements/sql-statement-overview.md)。

## SQL 模式

TiDB 服务器在不同的 SQL 模式下运行，并针对不同的客户端应用这些模式。SQL 模式定义了 TiDB 支持的 SQL 语法以及要执行的数据验证检查类型。

更多信息，请参见 [SQL 模式](/sql-mode.md)。

## 行 ID 生成属性

TiDB 提供三个 SQL 属性来优化行 ID 生成和数据分布。

- AUTO_INCREMENT

- AUTO_RANDOM

- SHARD_ROW_ID_BITS

### AUTO_INCREMENT

`AUTO_INCREMENT` 是一个列属性，用于自动填充默认列值。当 `INSERT` 语句没有为 `AUTO_INCREMENT` 列指定值时，系统会自动为该列分配值。

出于性能考虑，`AUTO_INCREMENT` 数值会批量分配（默认为 3 万个）给每个 TiDB 服务器。这意味着虽然 `AUTO_INCREMENT` 数值保证是唯一的，但分配给 `INSERT` 语句的值只在每个 TiDB 服务器基础上是单调的。

如果你希望 `AUTO_INCREMENT` 数值在所有 TiDB 服务器上都是单调的，并且你的 TiDB 版本是 v6.5.0 或更高版本，建议启用 [MySQL 兼容模式](/auto-increment.md#mysql-compatibility-mode)。

更多信息，请参见 [AUTO_INCREMENT](/auto-increment.md)。

### AUTO_RANDOM

`AUTO_RANDOM` 是一个列属性，用于自动为 `BIGINT` 列分配值。自动分配的值是随机且唯一的。由于 `AUTO_RANDOM` 的值是随机且唯一的，`AUTO_RANDOM` 经常用来代替 [`AUTO_INCREMENT`](/auto-increment.md)，以避免因 TiDB 分配连续 ID 而导致单个存储节点出现写入热点。

由于 `AUTO_RANDOM` 的值是随机且唯一的，`AUTO_RANDOM` 经常用来代替 [`AUTO_INCREMENT`](/auto-increment.md)，以避免因 TiDB 分配连续 ID 而导致单个存储节点出现写入热点。如果当前的 `AUTO_INCREMENT` 列是主键且类型为 `BIGINT`，你可以执行 `ALTER TABLE t MODIFY COLUMN id BIGINT AUTO_RANDOM(5);` 语句将其从 `AUTO_INCREMENT` 切换为 `AUTO_RANDOM`。

更多信息，请参见 [AUTO_RANDOM](/auto-random.md)。

### SHARD_ROW_ID_BITS

对于没有聚簇主键或没有主键的表，TiDB 使用隐式自增行 ID。当执行大量 `INSERT` 操作时，数据会写入单个 Region，导致写入热点。

为了缓解热点问题，你可以配置 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)。行 ID 会被分散，数据会写入多个不同的 Region。

## 关键字

关键字是在 SQL 语句中具有特殊含义的词，如 `SELECT`、`UPDATE` 和 `DELETE`。

- 其中一些可以直接用作标识符，这些被称为非保留关键字。

- 有些在用作标识符之前需要特殊处理，这些被称为保留关键字。

然而，一些非保留关键字可能仍需要特殊处理。建议你将它们视为保留关键字。

更多信息，请参见[关键字](/keywords.md)。

## 用户定义变量

TiDB 允许你设置和读取用户定义变量。用户定义变量的格式是 `@var_name`。组成 `var_name` 的字符可以是任何可以组成标识符的字符，包括数字 `0-9`、字母 `a-zA-Z`、下划线 `_`、美元符号 `$` 和 UTF-8 字符。此外，还包括英文句点 `.`。用户定义变量不区分大小写。

用户定义变量是会话特定的，这意味着一个客户端连接定义的用户变量不能被其他客户端连接看到或使用。

更多信息，请参见[用户定义变量](/user-defined-variables.md)。

## 元数据锁

在 TiDB 中，元数据锁是一种用于在在线架构变更期间管理表元数据变更的机制。当事务开始时，它会锁定当前元数据的快照。如果在事务期间元数据发生变化，TiDB 会抛出"Information schema is changed"错误，防止事务提交。元数据锁通过优先处理 DML 来协调数据操作语言（DML）和数据定义语言（DDL）操作，确保使用过时元数据的进行中 DML 事务在应用新的 DDL 更改之前提交，从而最小化错误并维护数据一致性。

更多信息，请参见[元数据锁](/metadata-lock.md)。
