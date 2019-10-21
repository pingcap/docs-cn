---
title: Data Migration 故障诊断
category: reference
---

# Data Migration 故障诊断

本文总结了在 DM 工具使用过程中遇到问题的诊断流程，并指引用户通过错误信息查找相应的解决方案。

如果你在运行 DM 工具时出现了错误，请尝试以下解决方案：

1. 执行 `query-status` 命令查看任务运行状态以及相关错误输出。

2. 查看与该错误相关的日志文件。日志文件位于 DM-master、DM-worker 部署节点上，通过 [Data Migration 错误含义](/dev/reference/tools/data-migration/faq-and-troubleshooting/error-system.md) 获取错误的关键信息，然后查看 [Data Migration 常见错误及修复](/dev/reference/tools/data-migration/faq-and-troubleshooting/error-handler.md)以寻找相应的解决方案。

3. 如果该错误还没有相应的解决方案，并且你无法通过查询日志或监控指标自行解决此问题，你可以联系相关销售人员进行支持。

4. 一般情况下，错误处理完成后，只需使用 dmctl 重启任务即可。

    {{< copyable "shell-regular" >}}

    ```bash
    resume-task ${task name}
    ```

但在某些情况下，你还需要重置数据同步任务。有关何时需要重置以及如何重置，详见[重置数据同步任务](/dev/reference/tools/data-migration/faq.md#重置数据同步任务)。
