---
title: 备份统计信息
summary: 了解如何备份统计信息。在恢复备份数据时，可以同时恢复统计信息。
---

# 备份统计信息

使用 Backup & Restore (BR) 执行数据备份任务时，在默认情况下 BR 不会备份统计信息。但恢复数据后的集群可能会因为没有统计信息，无法选择最佳的执行计划。

从 TiDB v7.5.0 起，备份恢复特性引入了备份统计信息的功能。该功能可以在备份数据的同时备份每张表的统计信息。

## 使用场景

如果你的恢复集群需要使用备份集群的统计信息，那么，你可以同时备份统计信息。

## 使用方法

当你想要在备份集群数据的同时备份统计信息，你可以关闭参数 `--ignore-stats`：

```shell
br backup full \
--storage local:///br_data/ --pd "${PD_IP}:2379" --log-file restore.log \
--ignore-stats=false
```

如果备份数据中存在统计信息，BR 在恢复数据时，也会自动恢复统计信息：

```shell
br restore full \
--storage local:///br_data/ --pd "${PD_IP}:2379" --log-file restore.log 
```

## 实现原理

备份恢复功能在备份时将统计信息通过 json 格式存储在 backupmeta 中，在恢复时将 json 格式的统计信息导入到集群中。详细内容可以参考 [LOAD STATS](/sql-statements/sql-statement-load-stats.md)。
