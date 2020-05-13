---
title: TiDB Binlog 故障诊断
category: reference
aliases: ['/docs-cn/dev/how-to/troubleshoot/tidb-binlog/']
---

# TiDB Binlog 故障诊断

本文总结了在 TiDB Binlog 的使用过程中遇到问题的诊断流程，并指引用户通过监控、状态、日志等信息查找相应的解决方案。

如果你在使用 TiDB Binlog 时出现了异常，请尝试以下方式排查问题：

1. 查看各个监控指标是否异常，参见[TiDB Binlog 集群监控](/reference/tidb-binlog/monitor.md)。

2. 使用 [binlogctl 工具](/reference/tidb-binlog/maintain.md#binlogctl-工具)查看各个 Pump、Drainer 的状态是否有异常。

3. 查看 Pump、Drainer 日志中是否有 `ERROR`、`WARN`，并根据详细的日志信息初步判断问题原因。

通过以上方式定位到问题后，在 [FAQ](/reference/tidb-binlog/faq.md) 以及 [常见错误及修复](/reference/tidb-binlog/troubleshoot/error-handling.md) 中查找解决方案，如果没有查找到解决方案或者提供的解决方案无法解决问题，请提交 [issue](https://github.com/pingcap/tidb-binlog/issues) 或者联系相关技术支持人员。
