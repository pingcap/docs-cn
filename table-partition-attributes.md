---
title: 表属性及分区属性使用文档
summary: 介绍 TiDB 的 `ATTRIBUTES` 使用方法。
---

表属性及分区属性是从 v5.3.0 引入的新特性，主要用于为表或分区添加特定的属性以执行相应的属性对应的行为。

> **注意：** 
> 
> 目前仅支持添加 `merge_option` 属性。

# 使用方法

表属性及分区属性均为 `key=value` 的形式，多个属性需要用逗号分隔。其中 `t` 为所要修改的表名，`p` 为所要修改的分区名，`[]`内部为可选项。

## 设置表或分区属性
```sql
alter table t [partition p ]attributes[=]'key=value[, key1=value1...]';
```

## 重置表或分区属性
```sql
alter table t [partition p ]attributes[=]default;
```

## 查看当前全部表及分区属性
```sql
select * from information_schema.attributes;
```

## 查看某一张表或分区配置的属性
```sql
select * from information_schema.attributes where id='schema/t[/p]';
```

## 查看拥有某属性的所有表及分区
```sql
select * from information_schema.attributes where attributes like '%key%';
```

# 覆盖关系
当表和分区同时存在相同属性的情况下，分区会将表的属性覆盖，如对于分区表 `t` 中分区 `p` 配置下述两个属性后：

```sql
alter table t attributes[=]'key=value';
alter table t partition p attributes[=]'key=value1';
```

则分区 p 实际生效的属性为 `key=value1`。

# 使用表或分区属性控制 Region 合并

通过为表或分区添加 `merge_option` 属性，然后根据该属性对应的值是否为 `deny` 决定是否允许某张表或者分区的 Region 被合并。使用该属性需要注意 PD 的参数 `split-merge-interval` 的配置。如没有配置 `merge_option`，则 Region 在超过 `split-merge-interval` 指定的时间后满足条件即可合并。如果配置了 `merge_option`，则超过指定时间后会根据 `merge_option` 的配置情况决定是否可以合并。

## 禁止属于某个表的 Region 被合并
```sql
alter table t attributes[=]'merge_option=deny';
```

## 允许属于某个表的 Region 被合并
```sql
alter table t attributes[=]'merge_option=allow';
```

## 禁止属于某个分区的 Region 被合并
```sql
alter table t partition p attributes[=]'merge_option=deny';
```

## 允许属于某个分区的 Region 被合并
```sql
alter table t partition p attributes[=]'merge_option=allow';
```

## 查看当前所有配置了 merge_option 属性的表/分区
```sql
select * from information_schema.attributes where attributes like '%merge_option%';
```

## 覆盖关系
```sql
alter table t attributes[=]'merge_option=deny';
alter table t partition p attributes[=]'merge_option=allow';
```

如对于分区表 `t` 的分区 `p`，若配置上述两个属性后，实际分区 `p` 的 Region 可以被合并，当分区的属性被重置，则分区 `p` 将继承表 `t` 的属性，Region 无法合并。

> **注意：** 
> 
> 目前如果只存在分区表的属性时，即使 `merge_option=allow`，默认会按照实际分区数量切分成多个 Region，如需将所有 Region 进行合并需要通过设为 default 重置该分区表属性。
