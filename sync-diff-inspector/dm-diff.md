---
title: 从 DM 拉取配置 
---

# 从 DM 拉取配置

用户在使用 DM 等同步工具时，可以从 `DM-master` 拉取指定 `task-name` 的配置。

下面是一个简单的例子：

```toml
# Diff Configuration.

######################### Global config #########################

# 检查数据的线程数量，上下游数据库的连接数会略大于该值
check-thread-count = 4

# 如果开启，若表存在不一致，则输出用于修复的 SQL 语句。
export-fix-sql = true

# 只对比表结构而不对比数据
check-struct-only = false

# dm-master 的地址, 格式为 "http://127.0.0.1:8261"
dm-addr = "http://127.0.0.1:8261"

# 指定 DM 的 `task-name`
dm-task = "test"

######################### Task config #########################
[task]
    # 1 fix sql: fix-target-TIDB1.sql
    # 2 log: sync-diff.log
    # 3 summary: summary.txt
    # 4 checkpoint: a dir
    output-dir = "./output"

    # 需要比对的下游数据库的表，每个表需要包含数据库名和表名，两者由 `.` 隔开
    target-check-tables = ["hb_test.*"]
```
