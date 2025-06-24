---
title: 对象命名规范
summary: 了解 TiDB 中的对象命名规范。
---

# 对象命名规范

本文介绍数据库对象（如数据库、表、索引和用户）的命名规则。

## 通用规则

- 建议使用有意义的英文单词，用下划线分隔。
- 名称中只使用字母、数字和下划线。
- 避免使用 TiDB 保留字（如 `group` 和 `order`）作为列名。
- 建议对所有数据库对象使用小写字母。

## 数据库命名规范

建议按业务、产品或其他指标区分数据库名称，数据库名称不超过 20 个字符。例如，可以将临时库命名为 `tmp_crm`，将测试库命名为 `test_crm`。

## 表命名规范

- 同一业务或模块的表使用相同的前缀，并尽可能确保表名是自解释的。
- 名称中的单词用下划线分隔。建议表名不超过 32 个字符。
- 建议注释表的用途以便更好地理解。例如：
    - 临时表：`tmp_t_crm_relation_0425`
    - 备份表：`bak_t_crm_relation_20170425`
    - 业务操作临时表：`tmp_st_{业务代码}_{创建者缩写}_{日期}`
    - 账期记录表：`t_crm_ec_record_YYYY{MM}{dd}`
- 为不同业务模块的表创建单独的数据库，并添加相应的注释。

## 列命名规范

- 列命名为该列的实际含义或缩写。
- 建议在具有相同含义的表之间使用相同的列名。
- 建议为列添加注释，并为枚举类型指定命名值，例如"0：离线，1：在线"。
- 建议将布尔列命名为 `is_{description}`。例如，`member` 表中表示成员是否启用的列可以命名为 `is_enabled`。
- 不建议列名超过 30 个字符，列数应少于 60 个。
- 避免使用 TiDB 保留字作为列名，如 `order`、`from` 和 `desc`。要检查关键字是否为保留字，请参阅 [TiDB 关键字](/keywords.md)。

## 索引命名规范

- 主键索引：`pk_{表名缩写}_{字段名缩写}`
- 唯一索引：`uk_{表名缩写}_{字段名缩写}`
- 普通索引：`idx_{表名缩写}_{字段名缩写}`
- 多个单词的列名：使用有意义的缩写

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
