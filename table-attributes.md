---
title: 表属性使用文档
summary: 介绍 TiDB 的 `ATTRIBUTES` 使用方法。
---

# 表属性使用文档

表属性是 TiDB 从 5.3.0 版本开始引入的新特性，用于为表或分区添加特定的属性，以对表或分区执行相应属性对应的操作，例如可以利用表属性控制 Region 的合并。

> **注意：** 
> 
> 目前仅支持添加 `merge_option` 属性。

## 使用方法

表属性为 `key=value` 的形式，多个属性需要用逗号分隔。具体示例如下，其中 `t` 为所要修改的表名，`p` 为所要修改的分区名，`[]`内部为可选项。

+ 设置表或分区属性

    ```sql
    alter table t [partition p ]attributes[=]'key=value[, key1=value1...]';
    ```

+ 重置表或分区属性

    ```sql
    alter table t [partition p ]attributes[=]default;
    ```

+ 查看当前全部表及分区属性

    ```sql
    select * from information_schema.attributes;
    ```

+ 查看某一张表或分区配置的属性

    ```sql
    select * from information_schema.attributes where id='schema/t[/p]';
    ```

+ 查看拥有某属性的所有表及分区

    ```sql
    select * from information_schema.attributes where attributes like '%key%';
    ```

## 覆盖关系
如果表和分区同时存在相同属性，分区会将表的属性覆盖。例如，为分区表 `t` 中的分区 `p` 同时配置 `key=value` 和 `key=value1` 两个属性时：

```sql
alter table t attributes[=]'key=value';
alter table t partition p attributes[=]'key=value1';
```

分区 `p` 实际生效的属性为 `key=value1`。

## 使用表属性控制 Region 合并

### 使用场景

+ 场景一：在对某张新建表或某个新建分区写入数据存在热点问题时，通常需要用户使用分裂打散 Region 的操作避免写入热点，但由于新建表或分区的分裂操作实际产生的是空 Region，如果分裂打散操作距离写入存在一定时间间隔，则 Region 会被合并，从而导致无法真正规避写入热点问题。该场景下，可通过为表或分区添加 `merge_option` 属性，设置值为 `deny`，有效解决写入热点问题。
+ 场景二：在只读场景下，如果是通过手动分裂 Region 缓解某张表或分区的周期性读热点问题，且不希望热点消失后手动分裂的 Region 被合并，可以通过为表或分区添加 `merge_option` 属性，设置值为 `deny` 解决这一问题。

### 使用方法

+ 禁止属于某个表的 Region 被合并

    ```sql
    alter table t attributes[=]'merge_option=deny';
    ```

+ 允许属于某个表的 Region 被合并

    ```sql
    alter table t attributes[=]'merge_option=allow';
    ```

+ 重置某个表的属性

    ```sql
    alter table t attributes[=]default；
    ```

+ 禁止属于某个分区的 Region 被合并

    ```sql
    alter table t partition p attributes[=]'merge_option=deny';
    ```

+ 允许属于某个分区的 Region 被合并

    ```sql
    alter table t partition p attributes[=]'merge_option=allow';
    ```

+ 查看当前所有配置了 `merge_option` 属性的表或分区

    ```sql
    select * from information_schema.attributes where attributes like '%merge_option%';
    ```

### 覆盖关系

```sql
alter table t attributes[=]'merge_option=deny';
alter table t partition p attributes[=]'merge_option=allow';
```

当对分区表 `t` 中的分区 `p` 同时配置上述两个属性时，实际分区 `p` 的 Region 可以被合并。当分区的属性被重置时，分区 `p` 则会继承表 `t` 的属性，Region 无法被合并。

> **注意：** 
> 
> 1. 如果目前只存在分区表的属性，即使配置 `merge_option=allow`，分区也会默认按照实际分区数量切分成多个 Region。如需合并所有 Region，则需要[重置该分区表](#使用方法)的属性。
> 2. 使用该属性需要注意 PD 的参数 [`split-merge-interval`](/pd-configuration-file.md#split-merge-interval) 的配置。如果没有配置 `merge_option`，Region 在超过 `split-merge-interval` 指定的时间后满足条件即可合并。如果配置了 `merge_option`，则超过指定时间后会根据 `merge_option` 的配置情况再决定是否可以合并。
