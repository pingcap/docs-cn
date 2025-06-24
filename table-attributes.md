---
title: 表属性
summary: 了解如何使用 TiDB 的表属性功能。
---

# 表属性

表属性功能在 TiDB v5.3.0 中引入。使用此功能，你可以为表或分区添加特定属性，以执行与这些属性相对应的操作。例如，你可以使用表属性来控制 Region 合并行为。

<CustomContent platform="tidb">

目前，TiDB 仅支持为表或分区添加 `merge_option` 属性来控制 Region 合并行为。`merge_option` 属性只是处理热点问题的一部分。更多信息，请参考[热点问题处理](/troubleshoot-hot-spot-issues.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

目前，TiDB 仅支持为表或分区添加 `merge_option` 属性来控制 Region 合并行为。`merge_option` 属性只是处理热点问题的一部分。

</CustomContent>

> **注意：**
>
> - 当你使用 TiDB Binlog 或 TiCDC 执行复制，或使用 BR 执行增量备份时，复制或备份操作会跳过设置表属性的 DDL 语句。要在下游或备份集群中使用表属性，你需要在下游或备份集群中手动执行 DDL 语句。

## 用法

表属性的形式为 `key=value`。多个属性之间用逗号分隔。在以下示例中，`t` 是要修改的表名，`p` 是要修改的分区名。`[]` 中的项为可选项。

+ 为表或分区设置属性：

    ```sql
    ALTER TABLE t [PARTITION p] ATTRIBUTES [=] 'key=value[, key1=value1...]';
    ```

+ 重置表或分区的属性：

    ```sql
    ALTER TABLE t [PARTITION p] ATTRIBUTES [=] DEFAULT;
    ```

+ 查看所有表和分区的属性：

    ```sql
    SELECT * FROM information_schema.attributes;
    ```

+ 查看表或分区配置的属性：

    ```sql
    SELECT * FROM information_schema.attributes WHERE id='schema/t[/p]';
    ```

+ 查看具有特定属性的所有表和分区：

    ```sql
    SELECT * FROM information_schema.attributes WHERE attributes LIKE '%key%';
    ```

## 属性覆盖规则

为表配置的属性对该表的所有分区都生效。但有一个例外：如果表和分区配置了相同的属性但属性值不同，分区属性会覆盖表属性。例如，假设表 `t` 配置了 `key=value` 属性，分区 `p` 配置了 `key=value1`。

```sql
ALTER TABLE t ATTRIBUTES[=]'key=value';
ALTER TABLE t PARTITION p ATTRIBUTES[=]'key=value1';
```

在这种情况下，`key=value1` 是在 `p1` 分区上实际生效的属性。

## 使用表属性控制 Region 合并行为

### 使用场景

如果存在写热点或读热点，你可以使用表属性来控制 Region 合并行为。你可以首先为表或分区添加 `merge_option` 属性，然后将其值设置为 `deny`。以下是两种场景。

#### 新建表或分区的写热点

如果在向新建的表或分区写入数据时出现热点问题，通常需要拆分和打散 Region。但是，如果拆分/打散操作与写入之间存在一定的时间间隔，这些操作并不能真正避免写热点。这是因为在创建表或分区时执行的拆分操作会产生空的 Region，所以如果存在时间间隔，拆分的 Region 可能会被合并。要处理这种情况，你可以为表或分区添加 `merge_option` 属性，并将属性值设置为 `deny`。

#### 只读场景中的周期性读热点

假设在只读场景中，你尝试通过手动拆分 Region 来减少表或分区上出现的周期性读热点，并且你不希望手动拆分的 Region 在热点问题解决后被合并。在这种情况下，你可以为表或分区添加 `merge_option` 属性，并将其值设置为 `deny`。

### 用法

+ 防止表的 Region 合并：

    ```sql
    ALTER TABLE t ATTRIBUTES 'merge_option=deny';
    ```

+ 允许合并属于表的 Region：

    ```sql
    ALTER TABLE t ATTRIBUTES 'merge_option=allow';
    ```

+ 重置表的属性：

    ```sql
    ALTER TABLE t ATTRIBUTES DEFAULT;
    ```

+ 防止分区的 Region 合并：

    ```sql
    ALTER TABLE t PARTITION p ATTRIBUTES 'merge_option=deny';
    ```

+ 允许合并属于分区的 Region：

    ```sql
    ALTER TABLE t PARTITION p ATTRIBUTES 'merge_option=allow';
    ```

+ 查看所有配置了 `merge_option` 属性的表或分区：

    ```sql
    SELECT * FROM information_schema.attributes WHERE attributes LIKE '%merge_option%';
    ```

### 属性覆盖规则

```sql
ALTER TABLE t ATTRIBUTES 'merge_option=deny';
ALTER TABLE t PARTITION p ATTRIBUTES 'merge_option=allow';
```

当同时配置上述两个属性时，属于分区 `p` 的 Region 实际上可以被合并。当重置分区的属性时，分区 `p` 会继承表 `t` 的属性，Region 不能被合并。

<CustomContent platform="tidb">

> **注意：**
>
> - 对于带有分区的表，如果仅在表级别配置了 `merge_option` 属性，即使 `merge_option=allow`，该表默认仍会根据实际分区数量拆分为多个 Region。要合并所有 Region，你需要[重置表的属性](#用法)。
> - 使用 `merge_option` 属性时，你需要注意 PD 配置参数 [`split-merge-interval`](/pd-configuration-file.md#split-merge-interval)。假设未配置 `merge_option` 属性。在这种情况下，如果 Region 满足条件，Region 可以在 `split-merge-interval` 指定的间隔后合并。如果配置了 `merge_option` 属性，PD 会根据 `merge_option` 配置在指定间隔后决定是否合并 Region。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> - 对于带有分区的表，如果仅在表级别配置了 `merge_option` 属性，即使 `merge_option=allow`，该表默认仍会根据实际分区数量拆分为多个 Region。要合并所有 Region，你需要[重置表的属性](#用法)。
> - 假设未配置 `merge_option` 属性。在这种情况下，如果 Region 满足条件，Region 可以在一小时后合并。如果配置了 `merge_option` 属性，PD 会根据 `merge_option` 配置在一小时后决定是否合并 Region。

</CustomContent>
