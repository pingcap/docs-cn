---
title: TiDB Lightning 错误处理
summary: 介绍了如何解决导入数据过程中的类型转换和冲突错误。
---

# 错误处理

> **警告:**
>
> TiDB Lightning 错误处理功能是实验特性。**不建议**在生产环境中仅依赖该功能处理相关错误。 

从 TiDB 5.3.0 开始，你可以配置 TiDB Lightning 以跳过诸如无效类型转换、唯一键冲突等错误，让导入任务持续进行，就如同出现错误的行数据不存在一样。你可以依据生成的报告，手动修复这些错误。该功能适用于以下场景：

- 要导入的数据有少许错误
- 手动定位错误比较困难
- 如果遇到错误就重启 TiDB Lightning，代价太大

## 类型错误 （Type error）

你可以通过修改配置项 `lightning.max-error` 来增加数据类型相关的容错数量。如果设置为 *N*，那么 TiDB Lightning 允许数据源中出现 *N* 个错误，而且会跳过这些错误，一旦超过这个错误数就会退出。默认值为 0，表示不允许出现错误。

{{< copyable "" >}}

```toml
[lightning]
max-error = 0
```

该配置对下列错误有效：

* 无效值。例如：在 INT 列设置了 `'Text'`
* 数字溢出。例如：在 TINYINT 列设置了 500
* 字符串溢出。例如: 在 VARCHAR(5) column 列中设置了`'Very Long Text'`
* 零日期时间，如 `'0000-00-00'` 和 `'2021-12-00'`
* 在 NOT NULL 列中设置了 NULL
* 生成的列表达式求值失败
* 列计数不匹配。行中数值的数量和列的数量不一致。
* `on-duplicate = "error"` 时，TiDB 后端的唯一键/主键冲突
* 其他 SQL 错误

下列错误是致命错误，不能通过配置 `max-error` 跳过：

* 原始 CSV、SQL 或者 Parquet 文件中的语法错误，例如未闭合的引号。
* I/O、网络、或系统权限错误。 

在 Local 后端模式下，唯一键/主键冲突的冲突是单独处理的。将在接下来的章节进行介绍。

## 解决重复问题

Local 后端模式下，TiDB Lightning 导入数据时先将数据转换成 KV 对数组（KV pairs），然后批量添加到 TiKV 中。与 TiDB 后端模式不同，直到任务结束才会检测重复行。因此，Local 模式下的重复错误不是通过 `max-error` 进行控制，而是通过 `duplicate-resolution` 配置项进行控制的。

{{< copyable "" >}}

```toml
[tikv-importer]
duplicate-resolution = 'record'
```

`duplicate-resolution`有以下三个选项：

* **'none'**：不对重复数据进行检测。如果唯一键/主键冲突确实存在，那么导入的表格里会出现不一致的数据和索引，checksum 检查的时候会失败。
* **'record'**：检测重复数据，但不会对重复数据进行修复。如果唯一键/主键冲突确实存在，那么导入的表格里会出现不一致的数据和索引，checksum 检查的时候会失败。
* **'remove'**：检测重复数据，并且删除*全部*重复行。导入的表格会保持一致，但是重复的行会被忽略，只能通过手动方式添加回来。 

TiDB Lightning 只能检测数据源的重复项，不能解决运行 TiDB Lightning 之前的存量数据的冲突问题。