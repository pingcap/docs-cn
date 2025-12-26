---
title: Data Migration 常见问题
---

# Data Migration 常见问题

## DM 是否支持迁移阿里 RDS 以及其他云数据库的数据？

DM 仅支持解析标准版本的 MySQL/MariaDB 的 binlog，对于阿里云 RDS 以及其他云数据库没有进行过测试，如果确认其 binlog 为标准格式，则可以支持。

已知问题的兼容情况：

- 阿里云 RDS
    - 即使上游表没有主键，阿里云 RDS 的 binlog 中也会包含隐藏的主键列，与上游表结构不一致。
- 华为云 RDS
    - 不支持，详见：[华为云数据库 RDS 是否支持直接读取 Binlog 备份文件](https://support.huaweicloud.com/rds_faq/rds_faq_0210.html)。

## task 配置中的黑白名单的正则表达式是否支持`非获取匹配`（?!）？

目前不支持，DM 仅支持 golang 标准库的正则，可以通过 [re2-syntax](https://github.com/google/re2/wiki/Syntax) 了解 golang 支持的正则表达式。

## 如果在上游执行的一个 statement 包含多个 DDL 操作，DM 是否支持迁移？

DM 会尝试将包含多个 DDL 变更操作的单条语句拆分成只包含一个 DDL 操作的多条语句，但是可能没有覆盖所有的场景。建议在上游执行的一条 statement 中只包含一个 DDL 操作，或者在测试环境中验证一下，如果不支持，可以给 DM 提 [issue](https://github.com/pingcap/dm/issues)。

## 如何处理不兼容的 DDL 语句？

你需要使用 dmctl 手动处理 TiDB 不兼容的 DDL 语句（包括手动跳过该 DDL 语句或使用用户指定的 DDL 语句替换原 DDL 语句，详见[处理出错的 DDL 语句](/dm/handle-failed-ddl-statements.md)）。

> **注意：**
>
> TiDB 目前并不兼容 MySQL 支持的所有 DDL 语句。

## DM 是否会将视图的 DDL 语句和对视图的 DML 语句同步到下游的 TiDB 中？

目前 DM 不会将视图的 DDL 语句同步到下游的 TiDB 集群，也不会将针对视图的 DML 语句同步到下游。

## 如何重置数据迁移任务？

当数据迁移过程中发生异常且无法恢复时，需要重置数据迁移任务，对数据重新进行迁移：

1. 使用 `stop-task` 停止异常的数据迁移任务。

2. 清理下游已迁移的数据。

3. 从下面两种方式中选择其中一种重启数据迁移任务：

    - 修改任务配置文件以指定新的任务名，然后使用 `start-task {task-config-file}` 重启迁移任务。
    - 使用 `start-task --remove-meta {task-config-file}` 重启数据迁移任务。

## 设置了 `online-ddl-scheme: "gh-ost"`， gh-ost 表相关的 DDL 报错该如何处理？

```
[unit=Sync] ["error information"="{\"msg\":\"[code=36046:class=sync-unit:scope=internal:level=high] online ddls on ghost table `xxx`.`_xxxx_gho`\\ngithub.com/pingcap/dm/pkg/terror.(*Error).Generate ......
```

出现上述错误可能有以下原因：

DM 在最后 `rename ghost_table to origin table` 的步骤会把内存的 DDL 信息读出，并且还原为 origin table 的 DDL。而内存中的 DDL 信息是在 `alter ghost_table` 的时候进行[处理](/dm/feature-online-ddl.md#online-schema-change-gh-ost)，记录 ghost_table DDL 的信息；或者是在重启 dm-worker 启动 task 的时候，从 `dm_meta.{task_name}_onlineddl` 中读取出来。

因此，如果在增量复制过程中，指定的 Pos 跳过了 `alter ghost_table` 的 DDL，但是该 Pos 仍在 gh-ost 的 online-ddl 的过程中，就会因为 ghost_table 没有正确写入到内存以及 `dm_meta.{task_name}_onlineddl`，而导致该问题。

可以通过以下方式绕过这个问题：

1. 取消 task 的 `online-ddl-schema` 的配置。

2. 把 `_{table_name}_gho`、`_{table_name}_ghc`、`_{table_name}_del` 配置到 `block-allow-list.ignore-tables` 中。

3. 手工在下游的 TiDB 执行上游的 DDL。

4. 待 Pos 复制到 gh-ost 整体流程后的位置，再重新启用 `online-ddl-schema` 以及注释掉 `block-allow-list.ignore-tables`。

## 如何为已有迁移任务增加需要迁移的表？

假如已有数据迁移任务正在运行，但又有其他的表需要添加到该迁移任务中，可根据当前数据迁移任务所处的阶段按下列方式分别进行处理。

> **注意：**
>
> 向已有数据迁移任务中增加需要迁移的表操作较复杂，请仅在确有强烈需求时进行。

### 迁移任务当前处于 `Dump` 阶段

由于 MySQL 不支持指定 snapshot 来进行导出，因此在导出过程中不支持更新迁移任务并重启以通过断点继续导出，故无法支持在该阶段动态增加需要迁移的表。

如果确实需要增加其他的表用于迁移，建议直接使用新的配置文件重新启动迁移任务。

### 迁移任务当前处于 `Load` 阶段

多个不同的数据迁移任务在导出时，通常对应于不同的 binlog position，如将它们在 `Load` 阶段合并导入，则无法就 binlog position 达成一致，因此不建议在 `Load` 阶段向数据迁移任务中增加需要迁移的表。

### 迁移任务当前处于 `Sync` 阶段

当数据迁移任务已经处于 `Sync` 阶段时，在配置文件中增加额外的表并重启任务，DM 并不会为新增的表重新执行全量导出与导入，而是会继续从之前的断点进行增量复制。

因此，如果需要新增的表对应的全量数据尚未导入到下游，则需要先使用单独的数据迁移任务将其全量数据导出并导入到下游。

将已有迁移任务对应的全局 checkpoint （`is_global=1`）中的 position 信息记为 `checkpoint-T`，如 `(mysql-bin.000100, 1234)`。将需要增加到迁移任务的表在全量导出的 `metedata`（或另一个处于 `Sync` 阶段的数据迁移任务的 checkpoint）的 position 信息记为 `checkpoint-S`，如 `(mysql-bin.000099, 5678)`。则可通过以下步骤将表增加到迁移任务中：

1. 使用 `stop-task` 停止已有迁移任务。如果需要增加的表属于另一个运行中的迁移任务，则也将其停止。

2. 使用 MySQL 客户连接到下游 TiDB 数据库，手动更新已有迁移任务对应的 checkpoint 表中的信息为 `checkpoint-T` 与 `checkpoint-S` 中的较小值（在本例中，为 `(mysql-bin.000099, 5678)`）。

    - 需要更新的 checkpoint 表为 `{dm_meta}` 库中的 `{task-name}_syncer_checkpoint`。

    - 需要更新的 checkpoint 行为 `id={source-id}` 且 `is_global=1`。

    - 需要更新的 checkpoint 列为 `binlog_name` 与 `binlog_pos`。

3. 在迁移任务配置中为 `syncers` 部分设置 `safe-mode: true` 以保证可重入执行。

4. 通过 `start-task` 启动迁移任务。

5. 通过 `query-status` 观察迁移任务状态，当 `syncerBinlog` 超过 `checkpoint-T` 与 `checkpoint-S` 中的较大值后（在本例中，为 `(mysql-bin.000100, 1234)`），即可还原 `safe-mode` 为原始值并重启迁移任务。

## 全量导入过程中遇到报错 `packet for query is too large. Try adjusting the 'max_allowed_packet' variable`

尝试将

- TiDB Server 的全局变量 `max_allowed_packet`
- 任务配置文件中的配置项 `target-database.max-allowed-packet`（详情参见 [DM 任务完整配置文件介绍](/dm/task-configuration-file-full.md)）

设置为比默认 67108864 (64M) 更大的值。

## 2.0+ 集群运行 1.0 已有数据迁移任务时报错 `Error 1054: Unknown column 'binlog_gtid' in 'field list'`

在 DM 2.0 之后，为 checkpoint 等元信息表引入了更多的字段。如果通过 `start-task` 直接使用 1.0 集群的任务配置文件从增量复制阶段继续运行，则会出现 `Error 1054: Unknown column 'binlog_gtid' in 'field list'` 错误。

对于此错误，可 [手动将 DM 1.0 的数据迁移任务导入到 2.0+ 集群](/dm/manually-upgrade-dm-1.0-to-2.0.md)。

## TiUP 无法部署 DM 的某个版本（如 v2.0.0-hotfix）

你可以通过 `tiup list dm-master` 命令查看 TiUP 支持部署的 DM 版本。该命令未展示的版本不能由 TiUP 管理。

## DM 同步报错 `parse mydumper metadata error: EOF`

该错误需要查看报错信息以及日志进一步分析。报错原因可能是 dump 单元由于缺少权限没有产生正确的 metadata 文件。

## DM 分库分表同步中没有明显报错，但是下游数据丢失

需要检查配置项 `block-allow-list` 和 `table-route`：

- `block-allow-list` 填写的是上游数据库表，可以在 `do-tables` 前通过加 “~” 来进行正则匹配。
- `table-route` 不支持正则，采用的是通配符模式，所以 `table_parttern_[0-63]` 只会匹配 table_parttern_0 到 table_pattern_6 这 7 张表。

## DM 上游无写入，replicate lag 监控无数据

在 DM v1.0 中，需要开启 `enable-heartbeat` 才会产生该监控数据。v2.0 及以后版本中，尚未启用该功能，replicate lag 监控无数据是预期行为。

## DM v2.0.0 启动任务时出现 `fail to initial unit Sync of subtask`，报错信息的 `RawCause` 显示 `context deadline exceeded`

该问题是 DM v2.0.0 的已知问题，在同步任务的表数目较多时触发，将在 v2.0.1 修复。使用 TiUP 部署的用户可以升级到开发版 nightly 解决该问题，或者访问 GitHub 上 [DM 仓库的 release 页面](https://github.com/pingcap/tiflow/releases)下载 v2.0.0-hotfix 版本手动替换可执行文件。

## DM 同步中报错 `duplicate entry`

用户需要首先确认任务中没有配置 `disable-detect`（v2.0.7 及之前版本），没有其他同步程序或手动插入数据，表中没有配置相关的 DML 过滤器。

为了便于排查问题，用户收集到下游 TiDB 相关 general log 后可以在 [AskTUG 社区](https://asktug.com/tags/dm) 联系专家进行排查。收集 general log 的方式如下：

```bash
# 开启 general log
curl -X POST -d "tidb_general_log=1" http://{TiDBIP}:10080/settings
# 关闭 general log
curl -X POST -d "tidb_general_log=0" http://{TiDBIP}:10080/settings
```

在发生 `duplicate entry` 报错时，确认日志中包含冲突数据的记录。

## 监控中部分面板显示 `No data point`

请参照 [DM 监控指标](/dm/monitor-a-dm-cluster.md)查看各面板含义，部分面板没有数据是正常现象。例如没有发生错误、不存在 DDL lock、没有启用 relay 功能等情况，均可能使得对应面板没有数据。

## DM v1.0 在任务出错时使用 `sql-skip` 命令无法跳过某些语句

首先需要检查执行 `sql-skip` 之后 binlog 位置是否在推进，如果是的话表示 `sql-skip` 已经生效。重复出错的原因是上游发送了多个不支持的 DDL，可以通过 `sql-skip -s <sql-pattern>` 进行模式匹配。

对于类似下面这种报错（报错中包含 `parse statement`）：

```
if the DDL is not needed, you can use a filter rule with \"*\" schema-pattern to ignore it.\n\t : parse statement: line 1 column 11 near \"EVENT `event_del_big_table` \r\nDISABLE\" %!!(MISSING)(EXTRA string=ALTER EVENT `event_del_big_table` \r\nDISABLE
```

出现报错的原因是 TiDB parser 无法解析上游的 DDL，例如 `ALTER EVENT`，所以 `sql-skip` 不会按预期生效。可以在任务配置文件中添加 [Binlog 过滤规则](/dm/dm-binlog-event-filter.md)进行过滤，并设置 `schema-pattern: "*"`。从 DM 2.0.1 版本开始，已预设过滤了 `EVENT` 相关语句。

在 DM v6.0 版本之后 `sql-skip`、`handle-error` 均已经被 `binlog` 替代，使用 `binlog` 命令可以跳过该类错误。

## DM 同步时下游长时间出现 REPLACE 语句

请检查是否符合 [safe mode 触发条件](/dm/dm-glossary.md#safe-mode)。如果任务发生错误并自动恢复，或者发生高可用调度，会满足“启动或恢复任务的前 1 分钟”这一条件，因此启用 safe mode。

可以检查 DM-worker 日志，在其中搜索包含 `change count` 的行，该行的 `new count` 非零时会启用 safe mode。检查 safe mode 启用时间以及启用前是否有报错，以定位启用原因。

## 使用 DM v2.0 同步数据时重启 DM 进程，出现全量数据导入失败错误

在 DM v2.0.1 及更早版本中，如果全量导入操作未完成时发生重启，重启后的上游数据源与 DM worker 的绑定关系可能会发生变化。例如，可能出现 dump 单元的中间数据在 DM worker A 机器上，但却由 DM worker B 进行 load 单元的情况，进而导致操作失败。

该情况有两种解决方案：

- 如果数据量较小（TB 级以下）或任务有合库合表：清空下游数据库的已导入数据，同时清空导出数据目录，使用 dmctl 删除并 `start-task --remove-meta` 重建任务。后续尽量保证全量导出导入阶段 DM 没有冗余 worker 以及避免在该时段内重启或升级 DM 集群。
- 如果数据量较大（数 TB 或更多）：清空下游数据库的已导入数据，将 lightning 部署到数据所在的 DM worker 节点，使用 [lightning local backend 模式](/tidb-lightning/deploy-tidb-lightning.md) 导入 DM dump 单元导出的数据。全量导入完成后，修改任务的 `task-mode` 为 `incremental`，修改 `mysql-instance.meta.pos` 为 dump 单元导出数据 `metadata` 中记录的位置，启动一个增量任务。

## 使用 DM 同步数据时重启 DM 进程，增量任务出现 `ERROR 1236 (HY000): The slave is connecting using CHANGE MASTER TO MASTER_AUTO_POSITION = 1, but the master has purged binary logs containing GTIDs that the slave requires.` 错误

该错误表明全量迁移期间，dump 单元记录 metadata 中的 binlog 位置已经被上游清理。

解决方案：出现该问题时只能清空下游数据库已同步数据，并在停止任务后加上 `--remove-meta` 参数重建任务。

如要提前避免该问题，需要进行以下配置：

1. 在 DM 全量迁移未完成时调大上游 MySQL 的 `expire_logs_days` 变量，保证全量进行结束时 metadata 中的 binlog 位置到当前时间的 binlog 都还没有被清理掉。如果数据量较大，应该使用 dumpling + lightning 的方式加快全量迁移速度。
2. DM 任务开启 relay log 选项，保证 binlog 被清理后 DM 仍有 relay log 可读取。

## 使用 TiUP v1.3.0, v1.3.1 部署 DM 集群，DM 集群的 grafana 监控报错显示 `failed to fetch dashboard`

该问题为 TiUP 已知 bug，在 TiUP v1.3.2 中已进行修复。可采取以下任一方法解决：

- 方法一：使用 `tiup update --self && tiup update dm` 升级 TiUP 到更新版本，随后先缩容再扩容集群中的 grafana 节点，重建 grafana 服务。
- 方法二：
    1. 备份 `deploy/grafana-$port/bin/public` 文件夹。
    2. 下载 [TiUP DM 离线镜像包](https://download.pingcap.com/tidb-dm-v2.0.1-linux-amd64.tar.gz)，并进行解压，将其中的 grafana-v4.0.3-**.tar.gz 文件解压后，用解压出的 public/ 文件夹替换前面所描述的文件夹，运行 `tiup dm restart $cluster_name -R grafana` 重启 grafana 服务监控。

## 在 DM v2.0 中，同时开启 relay 与 gtid 同步 MySQL 时，运行 `query-status` 发现 syncer checkpoint 中 GTID 不连续

该问题为 DM 已知 bug，在完全满足以下两个条件时将会触发，DM 将在 v2.0.2 修复该问题：

1. DM 配置的 source 同时设置了 `enable-relay` 与 `enable-gtid` 为 `true`
2. DM 同步上游为 **MySQL 从库**，并且该从库通过 `show binlog events in '<newest-binlog>' limit 2` 查询出的 `previous_gtids` 区间不连续，例如：

```
mysql> show binlog events in 'mysql-bin.000005' limit 2;
+------------------+------+----------------+-----------+-------------+--------------------------------------------------------------------+
| Log_name         | Pos  | Event_type     | Server_id | End_log_pos | Info                                                               |
+------------------+------+----------------+-----------+-------------+--------------------------------------------------------------------+
| mysql-bin.000005 |    4 | Format_desc    |    123452 |         123 | Server ver: 5.7.32-35-log, Binlog ver: 4                           |
| mysql-bin.000005 |  123 | Previous_gtids |    123452 |         194 | d3618e68-6052-11eb-a68b-0242ac110002:6-7                           |
+------------------+------+----------------+-----------+-------------+--------------------------------------------------------------------+
```

使用 dmctl 的 `query-status <task>` 指令查询任务信息，如果已经出现 `subTaskStatus.sync.syncerBinlogGtid` 不连续但 `subTaskStatus.sync.masterBinlogGtid` 连续的情况，例如下述例子：

```
query-status test
{
    ...
    "sources": [
        {
            ...
            "sourceStatus": {
                "source": "mysql1",
                ...
                "relayStatus": {
                    "masterBinlog": "(mysql-bin.000006, 744)",
                    "masterBinlogGtid": "f8004e25-6067-11eb-9fa3-0242ac110003:1-50",
                    ...
                }
            },
            "subTaskStatus": [
                {
                    ...
                    "sync": {
                        ...
                        "masterBinlog": "(mysql-bin.000006, 744)",
                        "masterBinlogGtid": "f8004e25-6067-11eb-9fa3-0242ac110003:1-50",
                        "syncerBinlog": "(mysql-bin|000001.000006, 738)",
                        "syncerBinlogGtid": "f8004e25-6067-11eb-9fa3-0242ac110003:1-20:40-49",
                        ...
                        "synced": false,
                        "binlogType": "local"
                    }
                }
            ]
        },
        {
            ...
            "sourceStatus": {
                "source": "mysql2",
                ...
                "relayStatus": {
                    "masterBinlog": "(mysql-bin.000007, 1979)",
                    "masterBinlogGtid": "ddb8974e-6064-11eb-8357-0242ac110002:1-25",
                    ...
                }
            },
            "subTaskStatus": [
                {
                    ...
                    "sync": {
                        "masterBinlog": "(mysql-bin.000007, 1979)",
                        "masterBinlogGtid": "ddb8974e-6064-11eb-8357-0242ac110002:1-25",
                        "syncerBinlog": "(mysql-bin|000001.000008, 1979)",
                        "syncerBinlogGtid": "ddb8974e-6064-11eb-8357-0242ac110002:1-25",
                        ...
                        "synced": true,
                        "binlogType": "local"
                    }
                }
            ]
        }
    ]
}
```

其中 mysql1 的 `syncerBinlogGtid` 不连续，已有数据丢失需要按下述方案之一处理：

- 如果全量导出任务 metadata 中的 position 到当前时间的上游数据库的 binlog 仍未被清理：
    1. 停止当前任务并删除所有 GTID 不连续的 source
    2. 设置所有 source 的 `enable-relay` 为 `false`
    3. 针对 GTID 不连续的 source（上例 mysql1），在对应的任务配置文件 `task.yaml` 中，把 `task-mode` 修改为 `incremental` 并配置增量任务起始点 `mysql-instances.meta` 为各个全量导出任务 metadata 的 binlog name，position 和 gtid 信息
    4. 配置 `task.yaml` 中的 `syncers.safe-mode` 为 `true` 并重启任务
    5. 待增量同步追上后，停止任务并在任务配置文件中设置 `safe-mode` 为 `false`
    6. 再次重启任务
- 如果上游数据库 binlog 已被清理但是本地 relay log 仍未被清理：
    1. 停止当前任务
    2. 针对 GTID 不连续的 source（上例 mysql1），在对应的任务配置文件 `task.yaml` 中，把 `task-mode` 修改为 `incremental` 并配置增量任务起始点 `mysql-instances.meta` 为各个全量导出任务 metadata 的 binlog name，position 和 gtid 信息
    3. 修改其中的 GTID 信息的 `1-y` 为 `previous_gtids` 的前段值，例如，上述例子需要改为 `6-y`
    4. 配置 `task.yaml` 中的 `syncers.safe-mode` 为 `true` 并重启任务
    5. 待增量同步追上后，停止任务并在任务配置文件中设置 `safe-mode` 为 `false`
    6. 再次重启任务
    7. 重启 source 并关闭 gtid 或 relay
- 如果上述条件均不满足或任务同步数据量较小：
    1. 清空下游数据库中数据
    2. 重启 source 并关闭 gtid 或 relay
    3. 重建任务并通过 `start-task task.yaml --remove-meta` 重新同步

上述处理方案中，针对正常同步的 source（如上例 mysql2），重设增量任务时起始点需设置 `mysql-instances.meta` 为 `subTaskStatus.sync` 的 `syncerBinlog` 与 `syncerBinlogGtid`。

## 在 DM 2.0 中开启 heartbeat，虚拟 IP 环境下切换 DM-worker 与 MySQL 实例的连接，遇到 "heartbeat config is different from previous used: serverID not equal" 错误

`heartbeat` 功能在 DM v2.0 及之后版本已经默认关闭，如果用户在同步任务配置文件中开启会干扰高可用特性，在配置文件中关闭该项（通过设置 `enable-heartbeat: false`，然后更新任务配置）即可解决。DM 将会在后续版本强制关闭该功能。

## DM-master 在重启后无法加入集群，报错信息为 "fail to start embed etcd, RawCause: member xxx has already been bootstrapped"

DM-master 会在启动时将 etcd 信息记录在当前目录。如果重启后当前目录发生变化，会导致 DM 缺失 etcd 信息，从而启动失败。

推荐使用 TiUP 运维 DM 避免这一问题。在需要使用二进制部署的场合，需要在 DM-master 配置文件中使用绝对路径配置 data-dir 项，或者注意运行命令的当前目录。

## 使用 dmctl 执行命令时无法连接 DM-master

在使用 dmctl 执行相关命令时，发现连接 DM-master 失败（即使已在命令中指定 `--master-addr` 的参数值），报错内容类似 `RawCause: context deadline exceeded, Workaround: please check your network connection.`，但使用 `telnet <master-addr>` 之类的命令检查网络却没有发现异常。

这种情况可以检查下环境变量 `https_proxy`（注意，这里是 **https** ）。如果配置了该环境变量，dmctl 会自动去连接 `https_proxy`  指定的主机及端口，而如果该主机没有相应的 `proxy` 转发服务，则会导致连接失败。

解决方案：确认 `https_proxy` 是否必须要配置，如果不是必须的，取消该设置即可。如果环境必须，那么在原命令前加环境变量设置 `https_proxy="" ./dmctl --master-addr "x.x.x.x:8261"` 即可。

> **注意：**
>
> 关于 `proxy` 的环境变量有 `http_proxy`，`https_proxy`，`no_proxy` 等。如果依据上述解决方案处理后仍无法连接，可以考虑检查 `http_proxy` 和 `no_proxy` 的参数配置是否有影响。

## v2.0.2 - v2.0.6 版本执行 start-relay 命令报错该如何处理？

```
flush local meta, Rawcause: open relay-dir/xxx.000001/relay.metayyyy: no such file or directory
```

上述报错在以下情况下有可能会被触发：

- DM 从 v2.0.1 及之前的版本升级到 v2.0.2 - v2.0.6 版本，且升级之前曾开启过 relay log，升级完后重新开启。
- 使用 stop-relay 命令暂停 relay log 后重新开启 relay log。

可以通过以下方式解决该问题：

- 重启 relay log:

    ```
    » stop-relay -s sourceID workerName
    » start-relay -s sourceID workerName
    ```

- 升级 DM 至 v2.0.7 或之后版本。
