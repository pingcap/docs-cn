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

## 同步任务中断并包含 `get binlog error ERROR 1236 (HY000)`, `binlog checksum mismatch, data may be corrupted` 等 binlog 获取或解析失败错误

在 DM 进行增量同步过程中，如果遇到了上游超过 4G 的 binlog 文件，并且 DM 在处理这个 binlog 过程中出现了同步中断（包括正常的 pause/stop 任务，异常的原因发生的中断时），DM 需要保存同步 checkpoint 信息，因为 MySQL position 使用 uint32 存储，所以超过 4G 部分的断点位置值会溢出，存储的是一个不合法的断点值，遇到这种情况需要手动进行恢复。恢复方法：
- 首先判断出错发生在 relay log 写入时还是 binlog replication unit 同步，如果错误发生在 relay log 写入，binlog replication 保存的断点都是正确的情况，可以先停止任务，停止 DM-worker，手动调节 relay meta 的 binlog-position 到 4，重启 DM-worker 重新拉取 relay log ，relay log 写入正常后启动任务会自动从断点继续同步。
- 如果 relay log 写入正常，已经写到了下一个文件，错误发生在 binlog replication unit 读取当前超过 4G relay log 文件的一个不合法 position，这时候可以停止任务，手动调节该任务的 checkpoint 信息到该 relay log 的一个合法 position，比如 4，注意需要同时调整 global checkpoint 和每张表的 checkpoint（如果某张表的 checkpoint 是比当前 relay log 更旧的 relay log，则不需要修改）。设置任务的 sage-mode 为 true ，保证可重入执行，这之后就可以重新启动同步任务，观察同步状态。
