---
title: 切换 DM-worker 与上游 MySQL 实例的连接
summary: 了解如何切换 DM-worker 与上游 MySQL 实例的连接。
category: reference
---

# 切换 DM-worker 与上游 MySQL 实例的连接

当需要对 DM-worker 所连接的上游 MySQL 实例进行停机维护或该实例意外宕机时，需要将 DM-worker 的连接切换到同一个主从复制集群内的另一个 MySQL 实例上。本文介绍如何将 DM-worker 的连接从一个 MySQL 实例切换到另一个 MySQL 实例上。

> **注意：**
>
> - 仅支持在同一个主从复制集内的 MySQL 实例间进行切换。
> - 将要切换到的 MySQL 实例必须拥有 DM-worker 所需的 binlog。
> - DM-worker 必须以 GTID sets 模式运行，即 DM 通过 DM-Ansible 部署时必须指定 `enable_gtid=true`。
> - DM 仅支持以下两种切换场景，且必须严格按照各场景的步骤执行操作，否则可能需要根据切换后的 MySQL 实例重新搭建 DM 集群并完整重做数据迁移任务。

有关 GTID sets 的概念解释，请参考 [MySQL 文档](https://dev.mysql.com/doc/refman/5.7/en/replication-gtids-concepts.html#replication-gtids-concepts-gtid-sets)。

## 虚拟 IP 环境下切换 DM-worker 与 MySQL 实例的连接

如果 DM-worker 通过虚拟 IP (VIP) 连接上游的 MySQL 实例，更改 VIP 所指向的 MySQL 实例，即是在 DM-worker 对应上游连接地址不变的情况下切换 DM-worker 实际所连接的 MySQL 实例。

> **注意：**
>
> 如果不对 DM 执行必要变更，当切换 VIP 所指向的 MySQL 实例时，DM 内部不同的 connection 可能会同时连接到切换前后不同的 MySQL 实例，造成 DM 拉取的 binlog 与从上游获取到的其他状态不一致，从而导致难以预期的异常行为甚至数据损坏。

如果 DM-worker 连接的 VIP 需要指向新的 MySQL 实例，需要按以下步骤进行操作：

1. 使用 `query-status` 命令获取当前 relay 处理单元已从原 MySQL 实例获取到的 binlog 对应的 GTID sets (`relayBinlogGtid`)，记为 `gtid-W`。
2. 在将要切换到的 MySQL 实例上使用 `SELECT @@GLOBAL.gtid_purged;` 获取已经被 purged 的 binlog 对应的 GTID sets，记为 `gtid-P`。
3. 在将要切换到的 MySQL 实例上使用 `SELECT @@GLOBAL.gtid_executed;` 获取所有已经执行成功的事务对应的 GTID sets，记为 `gtid-E`。
4. 确保满足以下关系，否则不支持将 DM-worker 连接切换到相应的 MySQL 实例：
    - `gtid-W` 包含 `gtid-P`（`gtid-P` 可以为空）
    - `gtid-E` 包含 `gtid-W`
5. 使用 `pause-relay` 命令暂停 relay 处理。
6. 使用 `pause-task` 命令暂停所有运行中的数据迁移任务。
7. 变更 VIP 以指向新的 MySQL 实例。
8. 使用 `switch-relay-master` 命令通知 relay 处理单元进行主从切换。
9. 使用 `resume-relay` 命令恢复 relay 处理，使其从新的 MySQL 实例读取 binlog。
10. 使用 `resume-task` 命令恢复之前的数据迁移任务。

## 变更 DM-worker 连接的上游 MySQL 实例地址

若要变更 DM-worker 的配置信息来使 DM-worker 连接到新的上游 MySQL 实例，需要按以下步骤进行操作：

1. 使用 `query-status` 命令获取当前 relay 处理单元已从原 MySQL 实例获取到的 binlog 对应的 GTID sets (`relayBinlogGtid`)，记为 `gtid-W`。
2. 在将要切换到的 MySQL 实例上使用 `SELECT @@GLOBAL.gtid_purged;` 获取已经被 purged 的 binlog 对应的 GTID sets，记为 `gtid-P`。
3. 在将要切换到的 MySQL 实例上使用 `SELECT @@GLOBAL.gtid_executed;` 获取所有已经执行成功的事务对应的 GTID sets，记为 `gtid-E`。
4. 确保满足以下关系，否则不支持将 DM-worker 连接切换到相应的 MySQL 实例：
    - `gtid-W` 包含 `gtid-P`（`gtid-P` 可以为空）
    - `gtid-E` 包含 `gtid-W`
5. 使用 `stop-task` 命令停止所有运行中的数据迁移任务。
6. 更新 `inventory.ini` 中的 DM-worker 配置，并使用 DM-Ansible 对 DM-worker 进行滚动升级操作。
7. 使用 `start-task` 命令重新启动数据迁移任务。
