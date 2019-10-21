---
title: Data Migration 常见错误及修复
category: reference
---

# Data Migration 常见错误及修复

## 常见错误说明和处理方法

| 错误码       | 错误说明                                                     | 解决方法                                                     |
| :----------- | :------------------------------------------------------------ | :----------------------------------------------------------- |
| `code=10001` | 数据库操作异常                                               | 进一步分析错误信息和错误堆栈                                 |
| `code=10002` | 数据库底层的 `bad connection` 错误，通常表示 DM 到下游 TiDB 的数据库连接出现了异常（如网络故障、TiDB 重启等）且当前请求的数据暂时未能发送到 TiDB。 | DM 提供针对此类错误的自动恢复。如果长时间未恢复，需要用户检查网络或 TiDB 状态。 |
| `code=10003` | 数据库底层 `invalid connection` 错误，通常表示 DM 到下游 TiDB 的数据库连接出现了异常（如网络故障、TiDB 重启、TiKV busy 等）且当前请求已有部分数据发送到了 TiDB。 | DM 提供针对此类错误的自动恢复。如果未能正常恢复，需要用户进一步检查错误信息并根据具体场景进行分析。 |
| `code=10005` | 数据库查询类语句出错                                         |                                                              |
| `code=10006` | 数据库 `EXECUTE` 类型语句出错，包括 DDL 和 `INSERT`/`UPDATE`/`DELETE` 类型的 DML。更详细的错误信息可通过错误 message 获取。错误 message 中通常包含操作数据库所返回的错误码和错误信息。 |                                                              |
| `code=11006` |  DM 内置的 parser 解析不兼容的 DDL 时出错              |  可参考 [Data Migration 故障诊断-处理不兼容的 DDL 语句](/dev/reference/tools/data-migration/faq.md#处理不兼容的-ddl-语句) 提供的解决方案 |
| `code=20010` | 处理任务配置时，解密数据库的密码出错                             |  检查任务配置中提供的下游数据库密码是否有[使用 dmctl 正确加密](/dev/how-to/deploy/data-migration-with-ansible.md#使用-dmctl-加密上游-mysql-用户密码) |
| `code=26002` | 任务检查创建数据库连接失败。更详细的错误信息可通过错误 message 获取。错误 message 中包含操作数据库所返回的错误码和错误信息。 |  检查 DM-master 所在的机器是否有权限访问上游 |
| `code=38008` | DM 组件间的 gRPC 通信出错                                      |  检查 `class`， 定位错误发生在哪些组件的交互环节，根据错误 message 判断是哪类通信错误。如果是 gRPC 建立连接出错，可检查通信服务端是否运行正常。 |

## 同步任务中断并包含 `invalid connection` 错误

发生 `invalid connection` 错误时，通常表示 DM 到下游 TiDB 的数据库连接出现了异常（如网络故障、TiDB 重启、TiKV busy 等）且当前请求已有部分数据发送到了 TiDB。

由于 DM 中存在同步任务并发向下游复制数据的特性，因此在任务中断时可能同时包含多个错误（可通过 `query-status` 或 `query-error` 查询当前错误）。

- 如果错误中仅包含 `invalid connection` 类型的错误且当前处于增量复制阶段，则 DM 会自动进行重试。
- 如果 DM 由于版本问题等未自动进行重试或自动重试未能成功，则可尝试先使用 `stop-task` 停止任务，然后再使用 `start-task` 重启任务。

## 同步任务中断并包含 `driver: bad connection` 错误

发生 `driver: bad connection` 错误时，通常表示 DM 到下游 TiDB 的数据库连接出现了异常（如网络故障、TiDB 重启等）且当前请求的数据暂时未能发送到 TiDB。

当前版本 DM 发生该类型错误时，需要先使用 `stop-task` 停止任务后再使用 `start-task` 重启任务。后续 DM 会完善对此错误类型的自动重试机制。

## relay 处理单元报错 `event from * in * diff from passed-in event *` 或同步任务中断并包含 `get binlog error ERROR 1236 (HY000)`、`binlog checksum mismatch, data may be corrupted` 等 binlog 获取或解析失败错误

在 DM 进行 relay log 拉取与增量同步过程中，如果遇到了上游超过 4GB 的 binlog 文件，就可能出现这两个错误。

原因是 DM 在写 relay log 时需要依据 binlog position 及文件大小对 event 进行验证，且需要保存同步的 binlog position 信息作为 checkpoint。但是 MySQL binlog position 官方定义使用 uint32 存储，所以超过 4G 部分的 binlog position 的 offset 值会溢出，进而出现上面的错误。

对于 relay 处理单元，可通过以下步骤手动恢复：

1. 在上游确认出错时对应的 binlog 文件的大小超出了 4GB。
2. 停止 DM-worker。
3. 将上游对应的 binlog 文件复制到 relay log 目录作为 relay log 文件。
4. 更新 relay log 目录内对应的 `relay.meta` 文件以从下一个 binlog 开始拉取。

    例如：报错时有 `binlog-name = "mysql-bin.004451"` 与`binlog-pos = 2453`，则将其分别更新为 `binlog-name = "mysql-bin.004452"` 与`binlog-pos = 4`。
5. 重启 DM-worker。

对于 binlog replication 处理单元，可通过以下步骤手动恢复：

1. 在上游确认出错时对应的 binlog 文件的大小超出了 4GB。
2. 通过 `stop-task` 停止同步任务。
3. 将下游 `dm_meta` 数据库中 global checkpoint 与每个 table 的 checkpoint 中的 `binlog_name` 更新为出错的 binlog 文件，将 `binlog_pos` 更新为已同步过的一个合法的 position 值，比如 4。

    例如：出错任务名为 `dm_test`，对应的 `source-id` 为 `replica-1`，出错时对应的 binlog 文件为 `mysql-bin|000001.004451`，则执行 `UPDATE dm_test_syncer_checkpoint SET binlog_name='mysql-bin|000001.004451', binlog_pos = 4 WHERE id='replica-1';`。
4. 在同步任务配置中为 `syncers` 部分设置 `safe-mode: true` 以保证可重入执行。
5. 通过 `start-task` 启动同步任务。
6. 通过 `query-status` 观察同步任务状态，当原造成出错的 relay log 文件同步完成后，即可还原 `safe-mode` 为原始值并重启同步任务。

## 执行 `query-status` 或查看日志时出现 `Access denied for user 'root'@'172.31.43.27' (using password: YES)`

在所有 DM 配置文件中，数据库相关的密码都必须使用经 dmctl 加密后的密文（若数据库密码为空，则无需加密）。有关如何使用 dmctl 加密明文密码，参见[使用 dmctl 加密上游 MySQL 用户密码](/dev/how-to/deploy/data-migration-with-ansible.md#使用-dmctl-加密上游-mysql-用户密码)。

此外，在 DM 运行过程中，上下游数据库的用户必须具备相应的读写权限。在启动同步任务过程中，DM 会自动进行相应权限的前置检查，详见[上游 MySQL 实例配置前置检查](/dev/reference/tools/data-migration/precheck.md)。
