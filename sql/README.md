---
title: TiDB 用户文档
category: user guide
---

# TiDB 用户文档

TiDB 支持 SQL92 标准并兼容 MySQL 语法，为了帮您更好地使用 TiDB, 该文档沿用了 MySQL 大部分的文档结构，同时针对 TiDB 特有的功能作了详细的描述。

## Table of Contents

+ TiDB 数据库管理
	- TiDB 服务器和服务器启动脚本
	- TiDB 数据目录
	- TiDB 系统数据库
	- [TiDB 专用系统变量和语法](tidb-specific.md)
	- TiDB 服务器日志文件
+ TiDB 安全
	- [TiDB 访问权限管理](privilege.md)
	- TiDB 用户账户管理
	- 使用安全连接
+ 优化
+ 语言结构
    - 字面值
    - 数据库、表、索引、列和别名
    - 关键字和保留字
    - 用户变量
    - 表达式语法
    - 注释语法
+ 字符集和时区支持
	- 字符集支持
	- 字符集配置
	- 时区支持
+ 数据类型
	- 数值类型
	- 日期和时间类型
	- 字符串类型
	- JSON 数据类型
	- 数据类型默认值
	- 数据类型存储需求
	- 选择正确的列类型
	- 使用来自其他数据库引擎的数据类型
+ 函数和操作符
	- 函数和操作符概述
	- 表达式求值的类型转换
	- 操作符
	- 控制流程函数
	- 字符串函数
	- 数值函数与操作符
	- 日期和时间函数
	- Cast函数和操作符
	- 位函数和操作符
	- 加密和压缩函数
	- 信息函数
	- JSON 函数
	- 全局事务 ID 函数
	- GROUP BY 聚合函数
	- 其他函数
	- 精度数学
+ SQL 语句语法
	- 数据定义语句(DDL)
	- [数据操作语句(DML)](dml/README.md)
	- 事务语句
	- Prepared SQL 语句语法
	- 复合语句语法
	- 数据库管理语句
	- 实用工具语句
	- [TiDB SQL 语法图](https://pingcap.github.io/sqlgram/)
+ 文档数据库
+ 连接器和 API
+ 故障诊断
