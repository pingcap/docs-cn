---
title: 表属性
summary: 介绍 TiDB 的 `ATTRIBUTES` 使用方法。
---

# 表属性

表属性是 TiDB 从 5.3.0 版本开始引入的新特性，用于为表或分区添加特定的属性，以对表或分区执行相应属性对应的操作，例如可以利用表属性控制 Region 的合并。

> **注意：**
>
> - 目前 TiDB 仅支持为表或分区添加 `merge_option` 属性，用于控制 Region 合并。该属性仅能处理部分热点问题。如需了解更多的热点问题处理相关内容，请参阅 [TiDB 热点问题处理](/troubleshoot-hot-spot-issues.md)。
> - 当使用 TiCDC 进行同步或者使用 BR 进行增量备份时，同步和备份会跳过设置表属性的 DDL 语句。如需在下游或者备份集群使用表属性，需要在下游或者备份集群手动执行该 DDL 语句以设置表属性。

## 使用方法

表属性为 `key=value` 的形式，多个属性需要用逗号分隔。具体示例如下，其中 `t` 为所要修改的表名，`p` 为所要修改的分区名，`[]`内部为可选项。

+ 设置表或分区属性

    ```sql
    ALTER TABLE t [PARTITION p] ATTRIBUTES [=] 'key=value[, key1=value1...]';
    ```

+ 重置表或分区属性

    ```sql
    ALTER TABLE t [PARTITION p] ATTRIBUTES [=] DEFAULT;
    ```

+ 查看全部表及分区属性

    ```sql
    SELECT * FROM information_schema.attributes;
    ```

+ 查看某一张表或分区配置的属性

    ```sql
    SELECT * FROM information_schema.attributes WHERE id='schema/t[/p]';
    ```

+ 查看拥有某属性的所有表及分区

    ```sql
    SELECT * FROM information_schema.attributes WHERE attributes LIKE '%key%';
    ```

## 覆盖关系

为分区表配置的属性会对表的所有分区生效。一种例外情况是，如果分区表和分区都配置了相同属性但属性值不同，分区属性将覆盖分区表属性。例如，当分区表 `t` 配置属性 `key=value`，同时分区 `p` 配置属性 `key=value1` 时：

```sql
ALTER TABLE t ATTRIBUTES[=]'key=value';
ALTER TABLE t PARTITION p ATTRIBUTES[=]'key=value1';
```

分区 `p` 实际生效的属性为 `key=value1`。

## 使用表属性控制 Region 合并

### 使用场景

当写入或读取数据存在热点时，可以使用表属性控制 Region 合并，通过为表或分区添加 `merge_option` 属性，将其设置为 `deny` 来解决。以下介绍了两种使用场景。

#### 新建表或分区的写入热点问题

在对某张新建表或某个新建分区写入数据存在热点问题时，通常需要使用分裂打散 Region 的操作避免写入热点，但由于新建表或分区的分裂操作实际产生的是空 Region，如果分裂打散操作距离写入存在一定时间间隔，则 Region 可能会被合并，从而导致无法真正规避写入热点问题。此时可以为表或分区添加 `merge_option` 属性，设置为 `deny` 来解决问题。

#### 只读场景下周期性读热点问题

在只读场景下，如果是通过手动分裂 Region 缓解某张表或分区的周期性读热点问题，且不希望热点消失后手动分裂的 Region 被合并。此时可以为表或分区添加 `merge_option` 属性，设置为 `deny` 来解决问题。

### 使用方法

使用方法如下，其中 `t` 为所要修改的表名，`p` 为所要修改的分区名。

+ 禁止属于某个表的 Region 被合并

    ```sql
    ALTER TABLE t ATTRIBUTES 'merge_option=deny';
    ```

+ 允许属于某个表的 Region 被合并

    ```sql
    ALTER TABLE t ATTRIBUTES 'merge_option=allow';
    ```

+ 重置某个表的属性

    ```sql
    ALTER TABLE t ATTRIBUTES DEFAULT;
    ```

+ 禁止属于某个分区的 Region 被合并

    ```sql
    ALTER TABLE t PARTITION p ATTRIBUTES 'merge_option=deny';
    ```

+ 允许属于某个分区的 Region 被合并

    ```sql
    ALTER TABLE t PARTITION p attributes 'merge_option=allow';
    ```

+ 查看所有配置了 `merge_option` 属性的表或分区

    ```sql
    SELECT * FROM information_schema.attributes WHERE attributes LIKE '%merge_option%';
    ```

### 覆盖关系

```sql
ALTER TABLE t ATTRIBUTES 'merge_option=deny';
ALTER TABLE t PARTITION p ATTRIBUTES 'merge_option=allow';
```

同时配置上述两个属性时，实际分区 `p` 的 Region 可以被合并。当分区的属性被重置时，分区 `p` 则会继承表 `t` 的属性，Region 无法被合并。

> **注意：** 
> 
> - 如果目前只存在分区表的属性，即使配置 `merge_option=allow`，分区也会默认按照实际分区数量切分成多个 Region。如需合并所有 Region，则需要[重置该分区表的属性](#使用方法)。
> - 使用该属性需要注意 PD 的参数 [`split-merge-interval`](/pd-configuration-file.md#split-merge-interval) 的配置。如果没有配置 `merge_option`，Region 在超过 `split-merge-interval` 指定的时间后满足条件即可合并。如果配置了 `merge_option`，则超过指定时间后会根据 `merge_option` 的配置情况再决定是否可以合并。
