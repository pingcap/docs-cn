---
title: 数据迁移场景概述
summary: 了解在不同业务需求场景下如何配置数据迁移任务。
---

# 数据迁移场景概述

> **注意：**
>
> 在创建数据迁移任务之前，需要先完成以下操作：
>
> 1. [使用 TiUP 部署 DM 集群](/dm/deploy-a-dm-cluster-using-tiup.md)。
> 2. [创建数据源](/dm/quick-start-create-source.md)。

本文介绍多个业务需求场景下如何配置数据迁移任务。你可以根据具体的场景介绍，选择参考适合的教程来创建对应的数据迁移任务。

除了业务需求场景导向的创建数据迁移任务教程之外：

- 完整的数据迁移任务配置示例，请参考 [DM 任务完整配置文件介绍](/dm/task-configuration-file-full.md)
- 数据迁移任务的配置向导，请参考 [数据迁移任务配置向导](/dm/dm-task-configuration-guide.md)

## 多数据源汇总迁移到 TiDB

如果你需要将多个数据源的数据汇总迁移到 TiDB，此外还需要进行表重命名以防止多个数据源中相同表名在迁移过程中出现冲突，或者需要屏蔽掉某些表的某些 DDL/DML 操作，那么你可以参考[多数据源汇总迁移到 TiDB](/dm/usage-scenario-simple-migration.md)。

## 分库分表合并迁移到 TiDB

如果你需要将使用分表方案的业务合并迁移到 TiDB，可以参考[分表合并迁移到 TiDB](/dm/usage-scenario-shard-merge.md)。

## 只迁移数据源增量数据到 TiDB

如果你使用其他工具进行了全量数据迁移，例如使用 TiDB Lightning 迁移了全量数据，然后只使用 DM 进行增量数据迁移，那么该场景的数据迁移任务配置可以参考[只迁移数据源增量数据到 TiDB](/dm/usage-scenario-incremental-migration.md)。

## TiDB 目标表比数据源表的列更多

如果你需要在 TiDB 中定制创建表结构，TiDB 的表结构包含数据源对应表的所有列，且比数据源的表结构有更多的列，那么该场景的数据迁移任务配置需要参考 [TiDB 表结构存在更多列场景的数据迁移](/dm/usage-scenario-downstream-more-columns.md)。
