---
title: DM-worker 在上游 MySQL 主从间切换
summary: 切换 DM-worker 所连接上游 MySQL 实例的限制与操作步骤。
category: reference
---

# DM-worker 在上游 MySQL 主从间切换

本文介绍如何切换 DM-worker 以连接到上游同一个主从复制集内的另一个 MySQL 实例。

> **注意：**
>
> - 仅支持 DM-worker 在同一个主从复制集内的进行切换。
> - 将要切换到的 MySQL 实例必须拥有 DM-worker 所需的 binlog。
> - DM-worker 必须以 GTID Sets 模式运行，即通过 DM-Ansible 部署时必须指定 `enable_gtid=true`。

有关 GTID sets 的概念解释，请参考 [MySQL 官方文档](https://dev.mysql.com/doc/refman/5.7/en/replication-gtids-concepts.html#replication-gtids-concepts-gtid-sets)。

## 虚拟 IP 环境下的上游主从切换

如果 DM-worker 通过虚拟 IP (VIP) 连接上游的 MySQL 实例，且 VIP 指向的 MySQL 实例将发生变化，即在 DM-worker 对应上游连接地址不变的情况下切换 DM-worker 实际所连接的 MySQL 实例。

如果不对 DM 进行相应的变更操作，对于某些 VIP 方案，可能 DM-worker 仍会继续从 VIP 切换前的上游 MySQL 实例拉取 binlog，而其他数据库相关操作则可能发送给 VIP 切换后的 MySQL 实例，并导致 DM 行为难以预期。因此，需按以下步骤执行变更操作：

1. 使用 `query-status` 命令获取当前 relay 处理单元已从原 MySQL 实例获取到的 binlog 对应的 GTID Sets (`relayBinlogGtid`)，记为 _gtid-W_。
2. 在将要切换到的 MySQL 实例上使用 `SELECT @@GLOBAL.gtid_purged;` 获取已经被 purged 的 binlog 对应的 GTID Sets，记为 _gtid-P_。
3. 在将要切换到的 MySQL 实例上使用 `SELECT @@GLOBAL.gtid_executed;` 获取所有已经执行成功的事务对应的 GTID Sets，记为 _gtid-E_。
4. 确保满足以下关系，否则不支持将 DM-worker 切换到相应的 MySQL 实例：
    - _gtid-W_ 包含 _gtid-P_（_gtid-P_ 可以为空）
    - _gtid-E_ 包含 _gtid-W_
5. 使用 `pause-relay` 命令暂停 relay 处理。
6. 使用 `pause-task` 命令暂停所有运行中的数据迁移任务。
7. 变更 VIP 以指向新的 MySQL 实例。
8. 使用 `switch-relay-master` 命令通知 relay 处理单元进行主从切换。
9. 使用 `resume-relay` 命令恢复 relay 处理，使其从新的 MySQL 实例读取 binlog。
10. 使用 `resume-task` 命令恢复之前的数据迁移任务。

## 变更 DM-worker 连接的上游 MySQL 实例地址

如果期望变更 DM-worker 的配置信息以使其连接到上游新的 MySQL 实例，需要按以下步骤进行操作：

1. 使用 `query-status` 命令获取当前 relay 处理单元已从原 MySQL 实例获取到的 binlog 对应的 GTID Sets (`relayBinlogGtid`)，记为 _gtid-W_。
2. 在将要切换到的 MySQL 实例上使用 `SELECT @@GLOBAL.gtid_purged;` 获取已经被 purged 的 binlog 对应的 GTID Sets，记为 _gtid-P_。
3. 在将要切换到的 MySQL 实例上使用 `SELECT @@GLOBAL.gtid_executed;` 获取所有已经执行成功的事务对应的 GTID Sets，记为 _gtid-E_。
4. 确保满足以下关系，否则不支持将 DM-worker 切换到相应的 MySQL 实例：
    - _gtid-W_ 包含 _gtid-P_（_gtid-P_ 可以为空）
    - _gtid-E_ 包含 _gtid-W_
5. 使用 `stop-task` 命令停止所有运行中的数据迁移任务。
6. 更新 _inventory.ini_ 中的 DM-worker 配置，并使用 DM-Ansible 对 DM-worker 进行滚动升级操作。
7. 使用 `start-task` 命令重新启动数据迁移任务。
