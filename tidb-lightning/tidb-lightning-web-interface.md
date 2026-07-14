---
title: TiDB Lightning Web 界面
summary: 了解 TiDB Lightning Web 界面的移除以及推荐的替代方案。
aliases: ['/docs-cn/dev/tidb-lightning/tidb-lightning-web-interface/','/docs-cn/dev/reference/tools/tidb-lightning/web/']
---

# TiDB Lightning Web 界面

> **警告：**
>
> 从 TiDB v8.5.7 开始，TiDB Lightning 不再支持 Web 界面。

要使用 TiDB Lightning 导入数据，请使用 TiDB Lightning 命令行工具：`tidb-lightning` 用于导入任务，`tidb-lightning-ctl` 用于 checkpoint 和故障排查操作。

- 关于基本操作流程，参见 [TiDB Lightning 快速上手](/get-started-with-tidb-lightning.md)。
- 关于命令行参数，参见 [TiDB Lightning 命令行参数](/tidb-lightning/tidb-lightning-command-line-full.md)。

要检查导入进度，可以在 TiDB Lightning 日志中搜索 `progress` 关键字，或使用 [TiDB Lightning 监控面板](/tidb-lightning/monitor-tidb-lightning.md)。

对于新的数据导入负载，你也可以使用 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 语句。
