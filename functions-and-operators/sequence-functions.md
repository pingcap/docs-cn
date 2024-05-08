---
title: 序列函数
summary: 了解 TiDB 中的序列函数。
---

# 序列函数

TiDB 中的序列函数用于返回或设置使用 [`CREATE SEQUENCE`](/sql-statements/sql-statement-create-sequence.md) 语句创建的序列对象的值。

| 函数名称 | 功能描述 |
| :-------- | :-------------------------- |
| `NEXTVAL()` 或 `NEXT VALUE FOR` | 返回序列的下一个值 |
| `SETVAL()` | 设置序列的当前值 |
| `LASTVAL()` | 返回序列中最近一个使用过的值 |

## MySQL 兼容性

根据 [ISO/IEC 9075-2](https://www.iso.org/standard/76584.html)，MySQL 不支持创建和操作序列的函数和语句。
