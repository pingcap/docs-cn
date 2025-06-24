---
title: UUID 最佳实践
summary: UUID 作为主键时具有以下优势：减少网络往返、支持大多数编程语言和数据库、防止枚举攻击。建议将 UUID 以二进制形式存储在 `BINARY(16)` 列中。同时建议在 TiDB 中不要设置 `swap_flag` 以防止热点。MySQL 也支持 UUID。
---

# UUID 最佳实践

## UUID 概述

与使用 [`AUTO_INCREMENT`](/auto-increment.md) 整数值相比，使用通用唯一标识符（UUID）作为主键具有以下优势：

- UUID 可以在多个系统上生成而不会发生冲突。在某些情况下，这意味着可以减少与 TiDB 的网络往返次数，从而提高性能。
- 大多数编程语言和数据库系统都支持 UUID。
- 当作为 URL 的一部分使用时，UUID 不容易受到枚举攻击。相比之下，使用 `AUTO_INCREMENT` 数字时，可能会被猜测到发票 ID 或用户 ID。

## 最佳实践

### 以二进制形式存储

文本形式的 UUID 格式如下：`ab06f63e-8fe7-11ec-a514-5405db7aad56`，这是一个 36 个字符的字符串。通过使用 [`UUID_TO_BIN()`](/functions-and-operators/miscellaneous-functions.md#uuid_to_bin)，可以将文本格式转换为 16 字节的二进制格式。这样你就可以将文本存储在 [`BINARY(16)`](/data-type-string.md#binary-type) 列中。在检索 UUID 时，你可以使用 [`BIN_TO_UUID()`](/functions-and-operators/miscellaneous-functions.md#bin_to_uuid) 函数将其转换回文本格式。

### UUID 格式二进制顺序和聚簇主键

`UUID_TO_BIN()` 函数可以使用一个参数（UUID）或两个参数（第二个参数是 `swap_flag`）。

<CustomContent platform="tidb">

建议在 TiDB 中不要设置 `swap_flag`，以避免[热点问题](/best-practices/high-concurrency-best-practices.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

建议在 TiDB 中不要设置 `swap_flag`，以避免热点问题。

</CustomContent>

你还可以为基于 UUID 的主键显式设置 [`CLUSTERED` 选项](/clustered-indexes.md)，以避免热点。

为了演示 `swap_flag` 的效果，这里有两个结构相同的表。区别在于插入到 `uuid_demo_1` 的数据使用 `UUID_TO_BIN(?, 0)`，而 `uuid_demo_2` 使用 `UUID_TO_BIN(?, 1)`。

<CustomContent platform="tidb">

在下面的 [Key Visualizer](/dashboard/dashboard-key-visualizer.md) 截图中，你可以看到写入集中在 `uuid_demo_2` 表的单个区域，这个表在二进制格式中交换了字段的顺序。

</CustomContent>

<CustomContent platform="tidb-cloud">

在下面的 [Key Visualizer](/tidb-cloud/tune-performance.md#key-visualizer) 截图中，你可以看到写入集中在 `uuid_demo_2` 表的单个区域，这个表在二进制格式中交换了字段的顺序。

</CustomContent>

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

## MySQL 兼容性

MySQL 也可以使用 UUID。`BIN_TO_UUID()` 和 `UUID_TO_BIN()` 函数是在 MySQL 8.0 中引入的。`UUID()` 函数在早期的 MySQL 版本中也可用。
