---
title: TiDB 基本功能
summary: 了解 TiDB 的基本功能。
aliases: ['/docs-cn/dev/basic-features/']
---

# TiDB 基本功能

本文详细介绍 TiDB 具备的基本功能。

## 数据类型

- 数值类型：BIT、BOOL|BOOLEAN、SMALLINT、MEDIUMINT、INT|INTEGER、BIGINT、FLOAT、DOUBLE、DECIMAL。

- 日期和时间类型：DATE、TIME、DATETIME、TIMESTAMP、YEAR。

- 字符串类型：CHAR、VARCHAR、TEXT、TINYTEXT、MEDIUMTEXT、LONGTEXT、BINARY、VARBINARY、BLOB、TINYBLOB、MEDIUMBLOB、LONGBLOB、ENUM、SET。

- JSON 类型。

## 运算符

- 算术运算符、位运算符、比较运算符、逻辑运算符、日期和时间运算符等。

## 字符集及排序规则 

- 字符集：UTF8、UTF8MB4、BINARY、ASCII、LATIN1。

- 排序规则：UTF8MB4_GENERAL_CI、UTF8MB4_UNICODE_CI、UTF8MB4_GENERAL_BIN、UTF8_GENERAL_CI、UTF8_UNICODE_CI、UTF8_GENERAL_BIN、BINARY。

## 函数

- 控制流函数、字符串函数、日期和时间函数、位函数、数据类型转换函数、数据加解密函数、压缩和解压函数、信息函数、JSON 函数、聚合函数、窗口函数等。

## SQL 语句

- 完全支持标准的 Data Definition Language (DDL) 语句，例如：CREATE、DROP、ALTER、RENAME、TRUNCATE 等。

- 完全支持标准的 Data Manipulation Language (DML) 语句，例如：INSERT、REPLACE、SELECT、Subqueries、UPDATE、LOAD DATA 等。

- 完全支持标准的 Transactional and Locking 语句，例如：START TRANSACTION、COMMIT、ROLLBACK、SET TRANSACTION 等。

- 完全支持标准的 Database Administration 语句，例如：SHOW、SET 等。

- 完全支持标准的 Utility 语句，例如：DESCRIBE、EXPLAIN、USE 等。

- 完全支持 SQL GROUP BY 和 ORDER BY 子语句。

- 完全支持标准 SQL 语法的 LEFT OUTER JOIN 和 RIGHT OUTER JOIN。

- 完全支持标准 SQL 要求的表和列别名。

## 分区表

- 支持 Range 分区。

- 支持 Hash 分区。

## 视图

- 支持普通视图。

## 约束

- 支持非空约束。

- 支持主键约束。

- 支持唯一约束。

## 安全

- 支持基于 RBAC (role-based access control) 的权限管理。

- 支持密码管理。

- 支持通信、数据加密。

- 支持 IP 白名单。

- 支持审计功能。

## 工具

- 支持快速备份功能。

- 支持通过工具从 MySQL 迁移数据到 TiDB。

- 支持通过工具部署、运维 TiDB。
