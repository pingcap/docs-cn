---
title: SQL 开发规范
summary: TiDB 的 SQL 开发规范。
aliases: ['/zh/tidb/dev/sql-development-specification']
---

# SQL 开发规范

本章将介绍一些使用 SQL 的一般化开发规范。

## 建表删表规范

- 基本原则：表的建立在遵循表命名规范前提下，建议业务应用内部封装建表删表语句增加判断逻辑，防止业务流程异常中断。
- 详细说明：`create table if not exists table_name` 或者 `drop table if exists table_name` 语句建议增加 if 判断，避免应用侧由于 SQL 命令运行异常造成的异常中断。

## SELECT \* 使用规范

- 基本原则：避免使用 SELECT \* 进行查询。
- 详细说明：按需求选择合适的字段列，避免盲目地 SELECT \* 读取全部字段，因为其会消耗网络带宽。考虑将被查询的字段也加入到索引中，以有效利用覆盖索引功能。

## 字段上使用函数规范

- 基本原则：在取出字段上可以使用相关函数,但是在 Where 条件中的过滤条件字段上避免使用任何函数,包括数据类型转换函数，以避免索引失效。或者可以考虑使用表达式索引功能。
- 详细说明：

    不推荐的写法：

    {{< copyable "sql" >}}

    ```sql
    SELECT gmt_create
    FROM ...
    WHERE DATE_FORMAT(gmt_create, '%Y%m%d %H:%i:%s') = '20090101 00:00:00'
    ```

    推荐的写法：

    {{< copyable "sql" >}}

    ```sql
    SELECT DATE_FORMAT(gmt_create，'%Y%m%d %H:%i:%s')
    FROM ...
    WHERE gmt_create = str_to_date('20090101 00:00:00', '%Y%m%d %H:%i:%s')
    ```

## 其他规范

- WHERE 条件中不要在索引列上进行数学运算或函数运算。
- 用 in/union 替换 or，并注意 in 的个数小于 300。
- 避免使用 %前缀进行模糊前缀查询。
- 如应用使用 Multi Statements 执行 SQL，即将多个 SQL 使用分号连接，一次性地发给客户端执行，TiDB 只会返回第一个 SQL 的执行结果。
- 当使用表达式时，检查其是否支持计算下推到存储层的功能 (TiKV、TiFlash)，否则应有预期在 TiDB 层需要消耗更多内存、甚至 OOM。计算下推到存储层的功能列表如下：
    - [TiFlash 支持的计算下推清单](/tiflash/tiflash-supported-pushdown-calculations.md)。
    - [下推到 TiKV 的表达式列表](/functions-and-operators/expressions-pushed-down.md#下推到-tikv-的表达式列表)。
    - [谓词下推](/predicate-push-down.md#谓词下推)。
