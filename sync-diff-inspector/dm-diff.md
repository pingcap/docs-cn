---
title: 基于 DM 同步场景下的数据校验
summary: 了解如何使用 TiDB DM 拉取指定配置进行数据校验。
---

# 基于 DM 同步场景下的数据校验

当你在使用 [TiDB DM](https://docs.pingcap.com/zh/tidb-data-migration/stable/overview) 等同步工具时，需要校验 DM 同步后数据的一致性。你可以从 `DM-master` 拉取指定 `task-name` 的配置，进行数据校验。

下面是一个简单的配置文件说明，要了解完整配置，请参考 [sync-diff-inspector 用户文档](/sync-diff-inspector/sync-diff-inspector-overview.md)。

```toml
# Diff Configuration.

######################### Global config #########################

# 检查数据的线程数量，上下游数据库的连接数会略大于该值
check-thread-count = 4

# 如果开启，若表存在不一致，则输出用于修复的 SQL 语句
export-fix-sql = true

# 只对比表结构而不对比数据
check-struct-only = false

# dm-master 的地址, 格式为 "http://127.0.0.1:8261"
dm-addr = "http://127.0.0.1:8261"

# 指定 DM 的 `task-name`
dm-task = "test"

######################### Task config #########################
[task]
    output-dir = "./output"

    # 需要比对的下游数据库的表，每个表需要包含数据库名和表名，两者由 `.` 隔开
    target-check-tables = ["hb_test.*"]
```

该配置在 dm-task = "test" 中，会对该任务下 hb_test 库的所有表进行检验，自动从 DM 配置中获取上游对下游库名的正则匹配，以校验 DM 同步后数据的一致性。
