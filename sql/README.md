---
title: TiDB 用户文档
category: user guide
---

# TiDB 用户文档

TiDB 支持 SQL92 标准并兼容 MySQL 语法，为了帮您更好地使用 TiDB, 该文档沿用了 MySQL 大部分的文档结构，
同时针对 TiDB 特有的功能作了详细的描述。

Table of Contents

+ TiDB 数据库管理
    - [TiDB 服务](tidb-server.md)
    - [TiDB 数据目录](tidb-server.md#tidb-数据目录)
    - [TiDB 系统数据库](system-database.md)
    - [TiDB 专用系统变量和语法](tidb-specific.md)
    - [TiDB 服务器日志文件](tidb-server.md#tidb-服务器日志文件)
+ TiDB 安全
    - [TiDB 访问权限管理](privilege.md)
    - [TiDB 用户账户管理](user-account-management.md)
    - [使用加密连接](encrypted-connections.md)
+ 优化
    - [理解 TiDB 执行计划](understanding-the-query-execution-plan.md)
    - [统计信息简介](statistics.md)
+ 语言结构
    + 字面值
        - [字符串字面值](literal-value-string-literals.md)
        - [数字字面值](literal-value-numeric-literals.md)
        - [NULL 值](literal-value-null-values.md)
        - [十六进制字面值](literal-value-hex-decimal.md)
        - [date 和 time 字面值](literal-value-date-and-time-literals.md)
        - [布尔值](literal-value-boolean.md)
        - [bit-val 字面值](literal-value-bit-value.md)
    - [数据库、表、索引、列和别名](schema-object-names.md)
    - [关键字和保留字](keywords-and-reserved-words.md)
    - [用户变量](user-defined-variables.md)
    - [表达式语法](expression-syntax.md)
    - [注释语法](comment-syntax.md)
+ 字符集和时区支持
    - [字符集支持](character-set-support.md)
    - [字符集配置](character-set-configuration.md)
    - [时区支持](time-zone.md)
+ 数据类型
    - [数值类型](datatype.md#数值类型)
    - 日期和时间类型
    - [字符串类型](datatype.md#字符串类型)
    - JSON 数据类型
    - [数据类型默认值](datatype.md#数据类型的默认值)
    - 数据类型存储需求
    - 选择正确的列类型
+ 函数和操作符
    - 函数和操作符概述
    - [表达式求值的类型转换](type-conversion-in-expression-evaluation.md)
    - [操作符](operators.md)
    - [控制流程函数](control-flow-functions.md)
    - [字符串函数](string-functions.md)
    - [数值函数与操作符](numeric-functions-and-operators.md)
    - [日期和时间函数](date-and-time-functions.md)
    - [位函数和操作符](bit-functions-and-operators.md)
    - [Cast 函数和操作符](cast-functions-and-operators.md)
    - [加密和压缩函数](encryption-and-compression-functions.md)
    - 信息函数
    - [JSON 函数](json-functions.md)
    - [信息函数](information-functions.md)
    - 全局事务 ID 函数
    - [GROUP BY 聚合函数](aggregate-group-by-functions.md)
    - [其他函数](miscellaneous-functions.md)
    - [精度数学](precision-math.md)
+ SQL 语句语法
    - [数据定义语句(DDL)](ddl.md)
    - [数据操作语句(DML)](dml.md)
    - [事务语句](transaction.md)
    - Prepared SQL 语句语法
    - [数据库管理语句](admin.md)
    - 实用工具语句
    - [TiDB SQL 语法图](https://pingcap.github.io/sqlgram/)
- [文档型数据库](json-functions-generated-column.md)
+ 连接器和 API
+ [错误码与故障诊断](error.md)
