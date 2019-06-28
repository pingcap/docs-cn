---
title: Data Migration 常见问题
category: FAQ
---

# Data Migration 常见问题

## 同步任务中断并包含 `invalid connection` 错误应该怎么处理？

发生 `invalid connection` 错误时，通常表示 DM 到下游 TiDB 的数据库连接出现了异常（如网络故障、TiDB 重启、TiKV busy 等）且当前请求已有部分数据发送到了 TiDB。

由于 DM 中存在同步任务并发向下游复制数据的特性，因此在任务中断时可能同时包含多个错误（可通过 `query-status` 或 `query-error` 查询当前错误）。

- 如果错误中仅包含 `invalid connection` 类型的错误且当前处于增量复制阶段，则 DM 会自动进行重试。
- 如果 DM 由于版本问题等未自动进行重试或自动重试未能成功，则可尝试先使用 `stop-task` 停止任务，然后再使用 `start-task` 重启任务。 

## 同步任务中断并包含 `driver: bad connection` 错误应该怎么处理？

发生 `driver: bad connection` 错误时，通常表示 DM 到下游 TiDB 的数据库连接出现了异常（如网络故障、TiDB 重启等）且当前请求的数据暂时未能发送到 TiDB。

当前版本 DM 发生该类型错误时，需要先使用 `stop-task` 停止任务后再使用 `start-task` 重启任务。后续 DM 会完善对此错误类型的自动重试机制。
