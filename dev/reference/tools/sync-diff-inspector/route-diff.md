---
title: 不同库名／表名的数据校验
category: tools
---

### 不同库名／表名的数据校验

用户在使用 DM 等同步工具时，可以设置 `route-rules` 将数据同步到下游指定表中，sync-diff-inspector 提供了校验不同库名、表名的表的功能。

下面是一个简单的例子：

```
######################### Tables config #########################

# 配置需要对比的*目标数据库*中的表
[[check-tables]]
    # 目标库中数据库的名称
    schema = "test_2"

    # 需要检查的表
    tables = ["t_2"]

# 下面是一个对比不同库名和表名的两个表的配置示例
[[table-config]]
    # 目标库名
    schema = "test_2"

    # 目标表名
    table = "t_2"

    # 源数据的配置
    [[table-config.source-tables]]
        # 源库的实例 id
        instance-id = "source-1"
        # 源数据库的名称
        schema = "test_1"
        # 源表的名称
        table  = "t_1"
```

使用该配置会对下游的 `test_2.t_2 ` 与实例 `source-1` 中的 `test_1.t_1` 进行校验。

如果需要校验大量的不同库名或者表名的表，可以通过 `table-rule` 设置映射关系来简化配置。可以只配置 schema 或者 table 的映射关系，也可以都配置。例如上游库 `test_1` 中的所有表都同步到了下游的 `test_2` 库中，可以使用如下配置进行校验：

```
######################### Tables config #########################

# 配置需要对比的*目标数据库*中的表
[[check-tables]]
    # 目标库中数据库的名称
    schema = "test_2"

    # 检查所有表
    tables = ["~^"]

[[table-rules]]
    # schema-pattern 和 table-pattern 支持通配符 *?
    schema-pattern = "test_1"
    #table-pattern = ""
    target-schema = "test_2"
    #target-table = ""

```
