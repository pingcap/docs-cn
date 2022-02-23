---
title: 适配 online schema change 工具自定义的临时表名
summary: 了解如何通过正则表达式匹配自定义后的 pt-osc、gh-ost 等 online schema change 工具产生的临时表
---

# 适配 online schema change 工具自定义的临时表名

DM 支持自动识别和优化上游数据库的 online schema change 变更操作，例如 [gh-ost](https://github.com/github/gh-ost) 和 [pt-osc](https://www.percona.com/doc/percona-toolkit/3.0/pt-online-schema-change.html)均为常用工具。如果对此特性仍有疑惑，请先阅读 [迁移使用 GH-ost/PT-osc 的源数据库](/dm/feature-online-ddl.md)。

在使用 online schema change 工具的过程中，一般会生成三种表：`ghost table`，`trash table` 和 `real table` 。默认情况下 DM 支持自动识别`gh-ost`和`pt-osc`工具生成的临时表，仅需设置`online-ddl=true`。

但是在某些场景下，管理人员可能需要变更 online schema change 工具的默认行为，自定义`ghost table`和 `trash table`的名称；或者期望使用`gh-ost`和`pt-osc`之外的工具（原理和变更流程仍然保持一致）。此时则需要自行编写正则表达式以匹配`ghost table` 和 `trash table`。

- gh-ost 默认临时表命名规则
    - ghost table : _{origin_table}_gho
    - trash table : _{origin_table}_del
    - real table : 执行 online schema change 的 origin table
- pt-osc 默认临时表命名规则
    - ghost table : _{origin_table}_new
    - trash table : _{origin_table}_old
    - real table : 执行 online schema change 的 origin table

自 v2.0.7 起 DM 实验性支持修改过的 online schema change 工具。在 DM 任务配置中设置 `online-ddl=true` 后，配合`shadow-table-rules`和`trash-table-rules`即可支持通过正则表达式来匹配修改过的临时表。

假设自定义 pt-osc 的`ghost table`规则为`_{origin_table}_pcnew` 以及`trash table`规则为`_{origin_table}_pcold`, 那么自定义规则需配置如下：

```yaml
online-ddl: true
shadow-table-rules: ["^_(.+)_(?:pcnew)$"]
trash-table-rules: ["^_(.+)_(?:pcold)$"]
```
