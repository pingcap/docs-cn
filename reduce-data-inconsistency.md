---
title: 数据索引一致性检查
summary: 在事务执行时检查数据索引一致性，阻止写入不一致的数据，防止已经存在的数据不一致问题扩散。
---

# 数据索引一致性检查

本文档介绍数据索引不一致特性的作用范围、可能对用户可见的影响和控制方法。

> **警告：**（可选）
>
> 当前该功能为实验特性，不建议在生产环境中使用。

数据索引一致性检查时 TiDB 从 v5.4 开始支持的特性，用于减少数据索引不一致问题的产生。在用户事务的执行和提交过程中增加了一系列检查，提前发现已经存在的数据索引不一致问题，并阻止写入新的不一致的数据。

## 使用场景

- 对大多数使用场景，推荐开启默认配置，即 `tidb_enable_mutation_checker = 1`，`tidb_txn_assertion_level = FAST`。
- 追求绝对性能的场景，推荐全部关闭，`tidb_enable_mutation_checker = 0`，`tidb_txn_assertion_level = OFF`。
- 对性能要求不高，数据一致性要求更高的场景，推荐打开最高级别，`tidb_enable_mutation_checker = 1`，`tidb_txn_assertion_level = STRICT`

## 使用方法

数据索引一致性检查包含两组独立的检查，可以分别开启。

### Mutation Checker

Mutation checker 在事务执行过程中检查事务写入的内容是否存在不一致，通过系统变量 `tidb_enable_mutation_checker` 开启。可取值为 `{0,1}`

### Assertion

Assertion 在向 TiKV 读写数据时附加一系列断言，断言失败意味着存在数据索引不一致。Assertion 有 3 个级别，分别为：

- `OFF`，不开启
- `FAST`，开启对性能影响较小的部分检查
- `STRICT`，开启全部检查，对悲观事务性能有较大影响

## 使用限制

Mutation checker 对于新的 collation 机制支持的部分 collation、分区表不生效。

Assertion 对于 amend transaction 不生效。

## 常见问题

如果一致性检查报错，但是报错信息发现并无不一致，且 `admin check table/index` 没有返回错误信息，则存在一致性检查误报的可能。可以暂时关闭一致性检查跳过此问题。

不论是否误报，一致性检查报错时，请联系 PingCAP 工程师或 [上报 bug](https://github.com/pingcap/tidb/issues/new?labels=type%2Fbug&template=bug-report.md)。