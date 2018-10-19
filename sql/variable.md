---
title: 系统变量
category: user guide
---

# 系统变量

MySQL 系统变量 (System Variables) 是一些系统参数，用于调整数据库运行时的行为，根据变量的作用范围分为全局范围有效（Global Scope）以及会话级别有效（Session Scope）。TiDB 支持 MySQL5.7 的所有系统变量，大部分变量仅仅是为了兼容性而支持，不会影响运行时行为。

## 设置系统变量

通过 [`SET` 语句](../sql/admin.md#set-语句)可以修改系统变量的值。进行修改时，还要考虑变量可修改的范围，不是所有的变量都能在全局/会话范围内进行修改。具体的可修改范围参考 [MySQL 动态变量文档](https://dev.mysql.com/doc/refman/5.7/en/dynamic-system-variables.html)。

### 全局范围值

* 在变量名前加 `GLOBAL` 关键词或者是使用 `@@global.` 作为修饰符:

```sql
SET GLOBAL autocommit = 1;
SET @@global.autocommit = 1;
```

### 会话范围值

* 在变量名前加 `SESSION` 关键词或者是使用 `@@session.` 作为修饰符，或者是不加任何修饰符:

```sql
SET SESSION autocommit = 1;
SET @@session.autocommit = 1;
SET @@autocommit = 1;
```

* `LOCAL` 以及 `@@local.` 是 `SESSION` 以及 `@@session.` 的同义词

## TiDB 支持的 MySQL 系统变量

下列系统变量是 TiDB 真正支持并且行为和 MySQL 一致：

| 变量名 | 作用域 | 说明 |
| ---------------- | -------- | -------------------------------------------------- |
| autocommit | GLOBAL \| SESSION | 是否自动 Commit 事务 |
| sql_mode | GLOBAL \| SESSION | 支持部分 MySQL SQL mode，|
| time_zone | GLOBAL \| SESSION | 数据库所使用的时区 |
| tx_isolation | GLOBAL \| SESSION | 事务隔离级别 |

## TiDB 特有的系统变量

参见 [TiDB 专用系统变量](../sql/tidb-specific.md#tidb-专用系统变量和语法)。