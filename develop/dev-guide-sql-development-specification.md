---
title: SQL 开发规范
summary: 了解 TiDB 的 SQL 开发规范。
---

# SQL 开发规范

本文介绍使用 SQL 时的一些通用开发规范。

## 创建和删除表

- 基本原则：在遵循表命名规范的前提下，建议应用程序内部封装表的创建和删除语句，并添加判断逻辑，以防止业务流程异常中断。
- 详细说明：建议使用 `create table if not exists table_name` 或 `drop table if exists table_name` 语句添加 `if` 判断，以避免应用程序端 SQL 命令运行异常导致的中断。

## `SELECT *` 的使用

- 基本原则：避免使用 `SELECT *` 进行查询。
- 详细说明：根据需要选择适当的列，避免使用 `SELECT *` 读取所有字段，因为这样的操作会消耗网络带宽。考虑将查询的字段添加到索引中，以有效利用覆盖索引。

## 在字段上使用函数

- 基本原则：可以在查询的字段上使用相关函数。为避免索引失效，不要在 `WHERE` 子句的过滤字段上使用任何函数，包括数据类型转换函数。你可以考虑使用表达式索引。
- 详细说明：

    不推荐：

    {{< copyable "sql" >}}

    ```sql
    SELECT gmt_create
    FROM ...
    WHERE DATE_FORMAT(gmt_create, '%Y%m%d %H:%i:%s') = '20090101 00:00:00'
    ```

    推荐：

    {{< copyable "sql" >}}

    ```sql
    SELECT DATE_FORMAT(gmt_create, '%Y%m%d %H:%i:%s')
    FROM ...
    WHERE gmt_create = str_to_date('20090101 00:00:00', '%Y%m%d %H:%i:%s')
    ```

## 其他规范

- 不要在 `WHERE` 条件中对索引列进行数学运算或函数运算。
- 用 `IN` 或 `UNION` 替代 `OR`。`IN` 的数量必须小于 `300`。
- 避免使用 `%` 前缀进行模糊前缀查询。
- 如果应用程序使用 **Multi Statements** 执行 SQL，即多个 SQL 用分号连接并一次性发送到客户端执行，TiDB 只返回第一个 SQL 的执行结果。
- 使用表达式时，检查表达式是否支持计算下推到存储层（TiKV 或 TiFlash）。如果不支持，你应该预期 TiDB 层会有更多的内存消耗，甚至可能出现 OOM。可以下推到存储层的计算包括：
    - [TiFlash 支持的下推计算](/tiflash/tiflash-supported-pushdown-calculations.md)。
    - [TiKV - 下推表达式列表](/functions-and-operators/expressions-pushed-down.md)。
    - [谓词下推](/predicate-push-down.md)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
