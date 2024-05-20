---
title: TiDB Data Migration 对 online DDL 工具的支持
summary: 了解 DM 对常见 online DDL 工具的支持情况，使用方法和注意事项。
---

# TiDB Data Migration 对 online DDL 工具的支持

在 MySQL 生态中，gh-ost 与 pt-osc 等工具较广泛地被使用，TiDB Data Migration (DM) 对其提供了特殊的支持以避免对不必要的中间数据进行迁移。本文介绍了在 DM 中使用常见 online DDL 工具的方法和注意事项。

有关 DM 对 online DDL 工具支持的原理、处理流程等，可参考 [online-ddl](/dm/feature-online-ddl.md)。

## 使用限制

- DM 仅针对 gh-ost 与 pt-osc 做了特殊支持。
- 在开启 `online-ddl` 时，增量复制对应的 checkpoint 应不处于 online DDL 执行过程中。如上游某次 online DDL 操作开始于 binlog `position-A`、结束于 `position-B`，则增量复制的起始点应早于 `position-A` 或晚于 `position-B`，否则可能出现迁移出错，具体可参考 [FAQ](/dm/dm-faq.md#设置了-online-ddl-truegh-ost-表相关的-ddl-报错该如何处理)。

## 参数配置

<SimpleTab>
<div label="v2.0.5 及之后的版本">

在 v2.0.5 及之后的版本，请在 `task` 配置文件中使用 `online-ddl` 配置项。

如上游 MySQL/MariaDB （同时）使用 gh-ost 或 pt-osc 工具，则在 task 的配置文件中设置：

```yml
online-ddl: true
```

> **注意：**
>
> 自 v2.0.5 起，`online-ddl-scheme` 已被弃用，请使用 `online-ddl` 代替 `online-ddl-scheme`。如设置 `online-ddl: true` 会覆盖掉 `online-ddl-scheme`。如设置 `online-ddl-scheme: "pt"` 或 `online-ddl-scheme: "gh-ost"` 会被转换为 `online-ddl: true`。

</div>

<div label="v2.0.5 之前的版本">

在 v2.0.5 之前的版本（不含 v2.0.5），请在 `task` 配置文件中使用 `online-ddl-scheme` 配置项。

如上游 MySQL/MariaDB 使用的是 gh-ost 工具，则在 task 的配置文件中设置：

```yml
online-ddl-scheme: "gh-ost"
```

如上游 MySQL/MariaDB 使用的是 pt-osc 工具，则在 task 的配置文件中设置：

```yml
online-ddl-scheme: "pt"
```

</div>
</SimpleTab>
