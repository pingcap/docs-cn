---
title: 系统变量
category: reference
aliases: ['/docs-cn/dev/reference/configuration/tidb-server/mysql-variables/']
---

# 系统变量

MySQL 系统变量 (System Variables) 是一些系统参数，用于调整数据库运行时的行为，根据变量的作用范围分为全局范围有效（Global Scope）以及会话级别有效（Session Scope）。TiDB 支持 MySQL5.7 的所有系统变量，大部分变量仅仅是为了兼容性而支持，不会影响运行时行为。

## 设置系统变量

通过 [`SET` 语句](/sql-statements/sql-statement-admin.md#set-语句)可以修改系统变量的值。进行修改时，还要考虑变量可修改的范围，不是所有的变量都能在全局/会话范围内进行修改。具体的可修改范围参考 [MySQL 动态变量文档](https://dev.mysql.com/doc/refman/5.7/en/dynamic-system-variables.html)。

### 全局范围值

* 在变量名前加 `GLOBAL` 关键词或者是使用 `@@global.` 作为修饰符:

    {{< copyable "sql" >}}

    ```sql
    SET GLOBAL autocommit = 1;
    ```

    {{< copyable "sql" >}}

    ```sql
    SET @@global.autocommit = 1;
    ```
  
> **注意：**
>
> 在分布式 TiDB 中，`GLOBAL` 变量的设置会持久化到存储层中，单个 TiDB 实例每 2 秒会主动进行一次全变量的获取并形成 `gvc` (global variables cache) 缓存，该缓存有效时间最多可持续 2 秒。在设置 `GLOBAL` 变量之后，为了保证新会话的有效性，请确保两个操作之间的间隔大于 2 秒。相关细节可以查看 [Issue #14531](https://github.com/pingcap/tidb/issues/14531)。

### 会话范围值

* 在变量名前加 `SESSION` 关键词或者是使用 `@@session.` 作为修饰符，或者是不加任何修饰符:

    {{< copyable "sql" >}}

    ```sql
    SET SESSION autocommit = 1;
    ```

    {{< copyable "sql" >}}

    ```sql
    SET @@session.autocommit = 1;
    ```

    {{< copyable "sql" >}}

    ```sql
    SET @@autocommit = 1;
    ```

* `LOCAL` 以及 `@@local.` 是 `SESSION` 以及 `@@session.` 的同义词

### 系统变量的作用机制

* 会话范围的系统变量仅仅会在创建会话时才会根据全局范围系统变量初始化自己的值。更改全局范围的系统变量不会改变已经创建的会话正在使用的系统变量的值。

    {{< copyable "sql" >}}

    ```sql
    SELECT @@GLOBAL.autocommit;
    ```

    ```
    +---------------------+
    | @@GLOBAL.autocommit |
    +---------------------+
    | ON                  |
    +---------------------+
    1 row in set (0.00 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    SELECT @@SESSION.autocommit;
    ```

    ```
    +----------------------+
    | @@SESSION.autocommit |
    +----------------------+
    | ON                   |
    +----------------------+
    1 row in set (0.00 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    SET GLOBAL autocommit = OFF;
    ```

    ```
    Query OK, 0 rows affected (0.01 sec)
    ```

    会话范围的系统变量不会改变，会话中执行的事务依旧是以自动提交的形式来进行：

    {{< copyable "sql" >}}

    ```sql
    SELECT @@SESSION.autocommit;
    ```

    ```
    +----------------------+
    | @@SESSION.autocommit |
    +----------------------+
    | ON                   |
    +----------------------+
    1 row in set (0.00 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    SELECT @@GLOBAL.autocommit;
    ```

    ```
    +---------------------+
    | @@GLOBAL.autocommit |
    +---------------------+
    | OFF                 |
    +---------------------+
    1 row in set (0.00 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    exit
    ```

    ```
    Bye
    ```

    {{< copyable "shell-regular" >}}

    ```shell
    mysql -h 127.0.0.1 -P 4000 -u root -D test
    ```

    ```
    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 3
    Server version: 5.7.25-TiDB-None MySQL Community Server (Apache License 2.0)

    Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

    Oracle is a registered trademark of Oracle Corporation and/or its
    affiliates. Other names may be trademarks of their respective
    owners.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

    mysql>
    ```

    新建的会话会使用新的全局变量：

    ```sql
    SELECT @@SESSION.autocommit;
    ```

    ```
    +----------------------+
    | @@SESSION.autocommit |
    +----------------------+
    | OFF                  |
    +----------------------+
    1 row in set (0.00 sec)
    ```

## TiDB 支持的 MySQL 系统变量

下列系统变量是 TiDB 真正支持并且行为和 MySQL 一致：

| 变量名 | 作用域 | 说明 |
| ---------------- | -------- | -------------------------------------------------- |
| autocommit | GLOBAL \| SESSION | 是否自动 Commit 事务 |
| sql_mode | GLOBAL \| SESSION | 支持部分 MySQL SQL mode，|
| time_zone | GLOBAL \| SESSION | 数据库所使用的时区 |
| tx_isolation | GLOBAL \| SESSION | 事务隔离级别 |
| max\_execution\_time | GLOBAL \| SESSION | 语句超时时间，单位为毫秒 |
| innodb\_lock\_wait\_timeout | GLOBAL \| SESSION | 悲观事务语句等锁时间，单位为秒 |
| windowing\_use\_high\_precision | GLOBAL \| SESSION | 计算窗口函数时采用高精度模式，默认值为 1 |
| sql\_select\_limit | GLOBAL \| SESSION | SELECT 语句返回的最大行数，默认值为 `2^64 - 1` |

> **注意：**
>
> `max_execution_time` 目前对所有类型的 `statement` 生效，并非只对 `SELECT` 语句生效。实际精度在 100ms 级别，而非更准确的毫秒级别。

## TiDB 特有的系统变量

参见 [TiDB 专用系统变量](/tidb-specific-system-variables.md)。
