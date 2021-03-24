---
title: TiDB Binlog 常见问题
aliases: ['/docs-cn/dev/tidb-binlog/tidb-binlog-faq/','/docs-cn/dev/reference/tidb-binlog/faq/','/docs-cn/dev/faq/tidb-binlog/','/docs-cn/dev/reference/tools/tidb-binlog/faq/']
---

# TiDB Binlog 常见问题

本文介绍 TiDB Binlog 使用过程中的常见问题及解决方案。

## 开启 binog 对 TiDB 的性能有何影响？

- 对于查询无影响。

- 对于有写入或更新数据的事务有一点性能影响。延迟上，在 Prewrite 阶段要并发写一条 p-binlog 成功后才可以提交事务，一般写 binlog 比 KV Prewrite 快，所以不会增加延迟。可以在 Pump 的监控面板看到写 binlog 的响应时间。

## TiDB Binlog 的同步延迟一般为多少？

TiDB Binlog 的同步延迟为秒级别，在非业务高峰时延迟一般为 3 秒左右。

## Drainer 同步下游 TiDB/MySQL 的帐号需要哪些权限？

Drainer 同步帐号需要有如下权限：

* Insert
* Update
* Delete
* Create
* Drop
* Alter
* Execute
* Index
* Select

## Pump 磁盘快满了怎么办？

确认 GC 正常：

- 确认 pump 监控面板 **gc_tso** 时间是否与配置一致。

如 gc 正常以下调整可以降低单个 pump 需要的空间大小：

- 调整 pump **GC** 参数减少保留数据天数。
- 添加 pump 结点。

## Drainer 同步中断怎么办？

使用以下 binlogctl 命令查看 Pump 状态是否正常，以及是否全部非 `offline` 状态的 Pump 都在正常运行。

{{< copyable "shell-regular" >}}

```bash
binlogctl -cmd pumps
```

查看 Drainer 监控与日志是否有对应报错，根据具体问题进行处理。

## Drainer 同步下游 TiDB/MySQL 慢怎么办？

特别关注以下监控项：

- 通过 Drainer 监控 **drainer event**，可以看到 Drainer 当前每秒同步 Insert/Update/Delete 事件到下游的速度。
- 通过 Drainer 监控 **sql query time**，可以看到 Drainer 在下游执行 SQL 的响应时间。

同步慢的可能原因与解决方案：

- 同步的数据库包含没有主键或者唯一索引的表，需要给表加上主键。
- Drainer 与下游之间延迟大，可以调大 Drainer `worker-count` 参数（跨机房同步建议将 Drainer 部署在下游）。
- 下游负载不高，可以尝试调大 Drainer `worker-count` 参数。

## 假如有一个 Pump crash 了会怎样？

Drainer 会因为获取不到这个 Pump 的数据没法同步数据到下游。如果这个 Pump 能恢复，Drainer 就能恢复同步。

如果 Pump 没法恢复，可采用以下方式进行处理：

1. 使用 [binlogctl 将该 Pump 状态修改为 `offline`](/tidb-binlog/maintain-tidb-binlog-cluster.md)（丢失这个 Pump 的数据）
2. Drainer 获取到的数据会丢失这个 Pump 上的数据，下游跟上游数据会不一致，需要重新做全量 + 增量同步。具体步骤如下：
    1. 停止当前 Drainer。
    2. 上游做全量备份。
    3. 清理掉下游数据，包括 checkpoint 表 `tidb_binlog.checkpoint`。
    4. 使用上游的全量备份恢复下游数据。
    5. 部署 Drainer，使用 `initialCommitTs`= {从全量备份获取快照的时间戳}。

## 什么是 checkpoint？

Checkpoint 记录了 Drainer 同步到下游的 commit-ts，Drainer 重启时可以读取 checkpoint 接着从对应 commit-ts 同步数据到下游。Drainer 日志 `["write save point"] [ts=411222863322546177]` 表示保存对应时间戳的 checkpoint。

下游类型不同，checkpoint 的保存方式也不同：

- 下游 MySQL/TiDB 保存在 `tidb_binlog.checkpoint` 表。
- 下游 kafka/file 保存在对应配置目录里的文件。

因为 kafka/file 的数据内容包含了 commit-ts，所以如果 checkpoint 丢失，可以消费下游最新的一条数据看写到下游数据的最新 commit-ts。

Drainer 启动的时候会去读取 checkpoint，如果读取不到，就会使用配置的 `initial-commit-ts` 做为初次启动开始的同步时间点。

## Drainer 机器发生故障，下游数据还在，如何在新机器上重新部署 Drainer？

如果下游数据还在，只要保证能从对应 checkpoint 接着同步即可。

假如 checkpoint 还在，可采用以下方式进行处理：

1. 部署新的 Drainer 并启动即可（参考 checkpoint 介绍，Drainer 可以读取 checkpoint 接着同步）。
2. 使用 [binlogctl 将老的 Drainer 状态修改成 `offline`](/tidb-binlog/maintain-tidb-binlog-cluster.md)。

假如 checkpoint 不在，可以如下处理：

1. 获取之前 Drainer 的 checkpoint `commit-ts`，做为新部署 Drainer 的 `initial-commit-ts` 配置来部署新的 Drainer。
2. 使用 [binlogctl 将老的 Drainer 状态修改成 `offline`](/tidb-binlog/maintain-tidb-binlog-cluster.md)。

## 如何用全量 + binlog 备份文件来恢复一个集群？

1. 清理集群数据并使用全部备份恢复数据。
2. 使用 reparo 设置 `start-tso` = {全量备份文件快照时间戳+1}，`end-ts` = 0（或者指定时间点），恢复到备份文件最新的数据。

## 主从同步开启 `ignore-error` 触发 critical error 后如何重新部署？

TiDB 配置开启 `ignore-error` 写 binlog 失败后触发 critical error 告警，后续都不会再写 binlog，所以会有 binlog 数据丢失。如果要恢复同步，需要如下处理：

1. 停止当前 Drainer。
2. 重启触发 critical error 的 `tidb-server` 实例重新开始写 binlog（触发 critical error 后不会再写 binlog 到 pump）。
3. 上游做全量备份。
4. 清理掉下游数据包括 checkpoint 表 `tidb_binlog.checkpoint`。
5. 使用上游的全量备份恢复下游。
6. 部署 Drainer，使用 `initialCommitTs`= {从全量备份获取快照的时间戳}。

## 同步时出现上游数据库支持但是下游数据库执行会出错的 DDL，应该怎么办？

1. 查看 drainer.log 日志，查找 `exec failed` 找到 Drainer 退出前最后一条执行失败的 DDL。
2. 将 DDL 改为下游兼容支持的版本，在下游数据库中手动执行。
3. 查看 drainer.log 日志，查找执行失败的 DDL 语句，可以查询到该 DDL 的 commit-ts。例如：

    ```
    [2020/05/21 09:51:58.019 +08:00] [INFO] [syncer.go:398] ["add ddl item to syncer, you can add this commit ts to `ignore-txn-commit-ts` to skip this ddl if needed"] [sql="ALTER TABLE `test` ADD INDEX (`index1`)"] ["commit ts"=416815754209656834]。
    ```

4. 编辑 `drainer.toml` 配置文件，在 `ignore-txn-commit-ts` 项中添加该 commit-ts，重启 Drainer。

在绝大部分情况下，TiDB 和 MySQL 的语句都是兼容的。用户需要注意的是上下游的 `sql_mode` 应当保持一致。

## 在什么情况下暂停和下线 Pump/Drainer？

首先需要通过以下内容来了解 Pump/Drainer 的状态定义和启动、退出的流程。

暂停主要针对临时需要停止服务的场景，例如：

- 版本升级：停止进程后使用新的 binary 启动服务。
- 服务器维护：需要对服务器进行停机维护。退出进程，等维护完成后重启服务。

下线主要针对永久（或长时间）不再使用该服务的场景，例如：

- Pump 缩容：不再需要那么多 Pump 服务了，所以下线部分服务。
- 同步任务取消：不再需要将数据同步到某个下游，所以下线对应的 Drainer。
- 服务器迁移：需要将服务迁移到其他服务器。下线服务，在新的服务器上重新部署。

## 可以通过哪些方式暂停 Pump/Drainer？

- 直接 kill 进程。

    >**注意：**
    >
    > 不能使用 `kill -9` 命令，否则 Pump/Drainer 无法对信号进行处理。

- 如果 Pump/Drainer 运行在前台，则可以通过按下 <kbd>Ctrl</kbd>+<kbd>C</kbd> 来暂停。
- 使用 binlogctl 的 `pause-pump` 或 `pause-drainer` 命令。

## 可以使用 binlogctl 的 `update-pump`/`update-drainer` 命令来下线 Pump/Drainer 服务吗？

不可以。使用 `update-pump`/`update-drainer` 命令会直接修改 PD 中保存的状态信息，并且不会通知 Pump/Drainer 做相应的操作。使用不当时，可能会干扰数据同步，某些情况下还可能会造成**数据不一致**的严重后果。例如：

- 当 Pump 正常运行或者处于暂停状态时，如果使用 `update-pump` 将该 Pump 设置为 `offline`，那么 Drainer 会放弃获取处于 `offline` 状态的 Pump 的 binlog 数据，导致该 Pump 最新的 binlog 数据没有同步到 Drainer，造成上下游数据不一致。
- 当 Drainer 正常运行时，使用 `update-drainer` 命令将该 Drainer 设置为 `offline`。如果这时启动一个 Pump 节点，Pump 只会通知 `online` 状态的 Drainer，导致该 Drainer 没有及时获取到该 Pump 的 binlog 数据，造成上下游数据不一致。

## 可以使用 binlogctl 的 `update-pump`/`update-drainer` 命令来暂停 Pump/Drainer 服务吗？

不可以。`update-pump`/`update-drainer` 命令直接修改 PD 中保存的状态信息。执行这个命令并不会通知 Pump/Drainer 做相应的操作，**而且使用不当会使数据同步中断，甚至造成数据丢失。**

## 什么情况下使用 binlogctl 的 `update-pump` 命令设置 Pump 状态为 `paused`？

在某些异常情况下，Pump 没有正确维护自己的状态，实际上状态应该为 `paused`。这时可以使用 `update-pump` 对状态进行修正，例如：

- Pump 异常退出（可能由 panic 或者误操作执行 `kill -9` 命令直接 kill 掉进程导致），Pump 保存在 PD 中的状态仍然为 `online`。如果暂时不需要重启 Pump 恢复服务，可以使用 `update-pump` 把该 Pump 状态设置为 `paused`，避免对 TiDB 写 binlog 和 Drainer 获取 binlog 造成干扰。

## 什么情况下使用 binlogctl 的 `update-drainer` 命令设置 Drainer 状态为 `paused`？

在某些异常情况下，Drainer 没有正确维护自己的状态，，对数据同步造成了影响，实际上状态应该为 `paused`。这时可以使用 `update-drainer` 对状态进行修正，例如：

- Drainer 异常退出（出现 panic 直接退出进程，或者误操作执行 `kill -9` 命令直接 kill 掉进程），Drainer 保存在 PD 中的状态仍然为 `online`。当 Pump 启动时无法正常通知该 Drainer（报错 `notify drainer ...`），导致 Pump 无法正常运行。这个时候可以使用 `update-drainer` 将 Drainer 状态更新为 `paused`，再启动 Pump。

## 可以通过哪些方式下线 Pump/Drainer？

目前只可以使用 binlogctl 的 `offline-pump` 和 `offline-drainer` 命令来下线 Pump 和 Drainer。

## 什么情况下使用 binlogctl 的 `update-pump` 命令设置 Pump 状态为 `offline`?

> **警告：**
>
> 仅在可以容忍 binlog **数据丢失、上下游数据不一致**或者确认不再需要使用该 Pump 存储的 binlog 数据的情况下，才能使用 `update-pump` 修改 Pump 状态为 `offline`。

可以使用 `update-pump` 修改 Pump 状态为 `offline` 的情况有：

- 在某些情况下，Pump 异常退出进程，且无法恢复服务，同步就会中断。如果希望恢复同步且可以容忍部分 binlog 数据丢失，可以使用 `update-pump` 命令将该 Pump 状态设置为 `offline`，则 Drainer 会放弃拉取该 Pump 的 binlog 然后继续同步数据。
- 有从历史任务遗留下来且不再使用的 Pump 且进程已经退出（例如测试使用的服务），之后不再需要使用该服务，使用 `update-pump` 将该 Pump 设置为 `offline`。

在其他情况下一定要使用 `offline-pump` 命令让 Pump 走正常的下线处理流程。

## Pump 进程已经退出，且状态为 `paused`，现在不想使用这个 Pump 节点了，能否用 binlogctl 的 `update-pump` 命令设置节点状态为 `offline`？

Pump 以 `paused` 状态退出进程时，不保证所有 binlog 数据被下游 Drainer 消费。所以这样做会有上下游数据不一致的风险。正确的做法是重新启动 Pump，然后使用 `offline-pump` 下线该 Pump。

## 什么情况下使用 binlogctl 的 `update-drainer` 命令设置 Drainer 状态为 `offline`？

- 有从历史任务遗留下来且不再使用的 Drainer 且进程已经退出（例如测试使用的服务），之后不再需要使用该服务，使用 `update-drainer` 将该 Drainer 设置为 `offline`。

## 可以使用 `change pump`、`change drainer` 等 SQL 操作来暂停或者下线 Pump/Drainer 服务吗？

目前还不支持。这种 SQL 操作会直接修改 PD 中保存的状态，在功能上等同于使用 binlogctl 的 `update-pump`、`update-drainer` 命令。如果需要暂停或者下线，仍然要使用 binlogctl。

## TiDB 写入 binlog 失败导致 TiDB 卡住，日志中出现 `listener stopped, waiting for manual stop`

在 TiDB v3.0.12 以及之前，binlog 写入失败会导致 TiDB 报 fatal error。但是 TiDB 不会自动退出只是停止服务，看起来像服务卡住。TiDB 日志中可看到 `listener stopped, waiting for manual stop`。

遇到该问题需要根据具体情况判断是什么原因导致 binlog 写入失败。如果是 binlog 写入下游缓慢导致的，可以考虑扩容 Pump 或增加写 binlog 的超时时间。

TiDB 在 v3.0.13 版本中已优化此逻辑，写入 binlog 失败将使事务执行失败返回报错，而不会导致 TiDB 卡住。

## TiDB 向 Pump 写入了重复的 binlog？

TiDB 在写入 binlog 失败或者超时的情况下，会重试将 binlog 写入到下一个可用的 Pump 节点直到写入成功。所以如果写入到某个 Pump 节点较慢，导致 TiDB 超时（默认 15s），此时 TiDB 判定写入失败并尝试写入下一个 Pump 节点。如果超时的 Pump 节点实际也写入成功，则会出现同一条 binlog 被写入到多个 Pump 节点。Drainer 在处理 binlog 的时候，会自动去重 TSO 相同的 binlog，所以这种重复的写入对下游无感知，不会对同步逻辑产生影响。

## 在使用全量 + 增量方式恢复的过程中，Reparo 中断了，可以使用日志里面最后一个 TSO 恢复同步吗？

可以。Reparo 不会在启动时自动开启 safe-mode 模式，需要手动操作：

1. Reparo 中断后，记录日志中最后一个 TSO，记为 `checkpoint-tso`。
2. 修改 Reparo 配置文件，将配置项 `start-tso` 设为 `checkpoint-tso + 1`，将 `stop-tso` 设为 `checkpoint-tso + 80,000,000,000`（大概是 `checkpoint-tso` 延后 5 分钟），将 `safe-mode` 设置为 `true`。启动 Reparo，Reparo 会将数据同步到 `stop-tso` 后自动停止。
3. Reparo 自动停止后，将 `start-tso` 设置为 `checkpoint tso + 80,000,000,001`，将 `stop-tso` 设置为 `0`，将 `safe-mode` 设为 `false`。启动 Reparo 继续同步。
