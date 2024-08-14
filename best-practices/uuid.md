---
title: UUID 最佳实践
summary: 了解在 TiDB 中使用 UUID 的最佳实践和策略。
---

# UUID 最佳实践

## UUID 概述

通用唯一标识符 (UUID) 用作主键而不是 [`AUTO_INCREMENT`](/auto-increment.md) 整数值时，可以提供以下好处：

- UUID 可以在多个系统生成，而不会产生冲突。某些情况下可以减少到 TiDB 的网络往返次数，从而提高性能。
- 绝大多数编程语言和数据库系统都支持 UUID。
- 用在 URL 中时，UUID 不容易被枚举攻击。相比之下，使用 `AUTO_INCREMENT` 数字，则很容易让发票 ID 或用户 ID 被猜出。

## 最佳实践

### 二进制存储

UUID 文本是一个包含 36 字符的字符串，如 `ab06f63e-8fe7-11ec-a514-5405db7aad56`。使用 [`UUID_TO_BIN()`](/functions-and-operators/miscellaneous-functions.md#uuid_to_bin) 可将 UUID 文本格式转换为 16 字节的二进制格式。这样，你可以将文本存储在 [`BINARY(16)`](/data-type-string.md#binary-类型) 列中。检索 UUID 时，可以使用 [`BIN_TO_UUID()`](/functions-and-operators/miscellaneous-functions.md#bin_to_uuid) 函数再将其转换回文本格式。

### UUID 格式二进制顺序和聚簇主键

`UUID_TO_BIN()` 函数可以接收一个参数 (UUID) 或两个参数（第一个为 UUID，第二个为 `swap_flag`）。建议不要在 TiDB 中设置 `swap_flag`，以避免出现[热点](/best-practices/high-concurrency-best-practices.md)问题。

同时，你也可以在 UUID 主键上显式设置 [`CLUSTERED` 选项](/clustered-indexes.md)来避免热点问题。

为了演示 `swap_flag` 的效果，本文以表结构相同的两张表为例。区别在于，`uuid_demo_1` 表中插入的数据使用 `UUID_TO_BIN(?, 0)`，而 `uuid_demo_2` 表中使用 `UUID_TO_BIN(?, 1)`。

在如下的[流量可视化页面](/dashboard/dashboard-key-visualizer.md)，你可以看到写入操作集中在 `uuid_demo_2` 表的单个 Region 中，而这个表中的二进制格式字段顺序被调换过。

![Key Visualizer](/media/best-practices/uuid_keyviz.png)

```sql
CREATE TABLE `uuid_demo_1` (
  `uuid` varbinary(16) NOT NULL,
  `c1` varchar(255) NOT NULL,
  PRIMARY KEY (`uuid`) CLUSTERED
)
```

```sql
CREATE TABLE `uuid_demo_2` (
  `uuid` varbinary(16) NOT NULL,
  `c1` varchar(255) NOT NULL,
  PRIMARY KEY (`uuid`) CLUSTERED
)
```

## 与 MySQL 兼容性

UUID 也可以在 MySQL 中使用。MySQL 8.0 引入了 `BIN_TO_UUID()` 和 `UUID_TO_BIN()` 函数。`UUID()` 函数在较早的 MySQL 版本中也可以使用。
