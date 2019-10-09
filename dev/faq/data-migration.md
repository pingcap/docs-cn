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

## relay 处理单元报错 `event from * in * diff from passed-in event *` 或同步任务中断并包含 `get binlog error ERROR 1236 (HY000)`, `binlog checksum mismatch, data may be corrupted` 等 binlog 获取或解析失败错误

在 DM 进行 relay log 拉取与增量同步过程中，如果遇到了上游超过 4GB 的 binlog 文件，就可能出现这个错误。

原因是 DM 在写 relay log 时需要依据 binlog position 及文件大小对 event 进行验证，且需要保存同步的 binlog position 信息作为 checkpoint。但是 MySQL binlog position 官方定义使用 uint32 存储，所以超过 4G 部分的 binlog position 的 offset 值会溢出，进而出现上面的错误。

对于 relay 处理单元，可通过以下步骤手动恢复：

1. 在上游确认出错时对应的 binlog 文件的大小超出了 4GB。
2. 停止 DM-worker。
3. 将上游对应的 binlog 文件复制到 relay log 目录作为 relay log 文件。
4. 更新 relay log 目录内对应的 _relay.meta_ 文件以从下一个 binlog 开始拉取。

    例如：报错时有 `binlog-name = "mysql-bin.004451"` 与`binlog-pos = 2453`，则将其分别更新为 `binlog-name = "mysql-bin.004452"` 与`binlog-pos = 4`。
5. 重启 DM-worker。

对于 binlog replication 处理单元，可通过以下步骤手动恢复：

1. 在上游确认出错时对应的 binlog 文件的大小超出了 4GB。
2. 通过 `stop-task` 停止同步任务。
3. 将下游 `dm_meta` 数据库中 global checkpoint 与每个 table 的 checkpoint 中的 `binlog_name` 更新为出错的 binlog 文件、`binlog_pos` 更新为已同步过的一个合法的 position 值，比如 4。

    例如：出错任务名为 `dm_test`，对应的 `source-id` 为 `replica-1`，出错时对应的 binlog 文件为 `mysql-bin|000001.004451`，则执行 `UPDATE dm_test_syncer_checkpoint SET binlog_name='mysql-bin|000001.004451', binlog_pos = 4 WHERE id='replica-1';`。
4. 在同步任务配置中为 `syncers` 部分设置 `safe-mode: true` 以保证可重入执行。
5. 通过 `start-task` 启动同步任务。
6. 通过 `query-status` 观察同步任务状态，当原造成出错的 relay log 文件同步完成后，即可关闭 `safe-mode` 并重启同步任务。
