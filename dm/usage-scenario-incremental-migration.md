---
title: 增量迁移数据到 TiDB
---

# 增量迁移数据到 TiDB

本文介绍如何使用 DM 将源数据库从指定位置开始的 Binlog 同步到下游 TiDB。本文以迁移一个数据源 MySQL 实例为例。

## 数据源表

假设数据源实例为：

| Schema | Tables |
|:------|:------|
| user  | information, log |
| store | store_bj, store_tj |
| log   | messages |

## 迁移要求

只将数据源 `log` 库从某个 binlog 位置起的数据变更同步到 TiDB 集群。

## 增量数据迁移操作

本节按顺序给出迁移操作步骤，指导如何使用 DM 将数据源的 `log` 库从某个时间点起的数据变动同步到 TiDB 集群。

### 确定增量同步起始位置

首先需要确定开始迁移的数据源 binlog 位置。如果你确定 binlog 的同步位置，那么可以跳过这一步。

你可以通过下面的方法获得对应数据源开启迁移的 binlog 位置点：

- 使用 Dumpling/Mydumper 进行全量数据导出，然后使用其他工具，如 TiDB Lightning，进行全量数据导入，则可以通过导出数据的 [metadata 文件](https://docs.pingcap.com/zh/tidb/stable/dumpling-overview#%E8%BE%93%E5%87%BA%E6%96%87%E4%BB%B6%E6%A0%BC%E5%BC%8F)获取同步位置；

  ```file
  Started dump at: 2020-11-10 10:40:19
  SHOW MASTER STATUS:
        Log: mysql-bin.000001
        Pos: 2022
        GTID: 09bec856-ba95-11ea-850a-58f2b4af5188:1-9 
  Finished dump at: 2020-11-10 10:40:20
  ```
  
- 使用 `SHOW BINLOG EVENTS` 语句，或者使用 `mysqlbinlog` 工具查看 binlog，选择合适的位置。
- 如果从当前时间点开始同步 binlog，则可以使用 `SHOW MASTER STATUS` 命令查看当前位置：

  ```sql
  MySQL [log]> SHOW MASTER STATUS;
  +------------------+----------+--------------+------------------+------------------------------------------+
  | File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set                        |
  +------------------+----------+--------------+------------------+------------------------------------------+
  | mysql-bin.000001 |     2022 |              |                  | 09bec856-ba95-11ea-850a-58f2b4af5188:1-9 |
  +------------------+----------+--------------+------------------+------------------------------------------+
  1 row in set (0.000 sec)
  ```

本例将从 `binlog position=(mysql-bin.000001, 2022), gtid=09bec856-ba95-11ea-850a-58f2b4af5188:1-9` 这个位置开始同步。

### 手动在下游创建表

由于建表 SQL 语句在同步起始位置之前，本次增量同步任务并不会自动在下游创建表。因此需要手动在在下游 TiDB 创建数据源同步起始位置对应的表结构。该教程的示例如下：

{{< copyable "sql" >}}

```sql
CREATE TABLE `messages` (
  `id` int(11) NOT NULL,
  `message` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
)
```

### 创建同步任务

1. 创建任务配置文件 `task.yaml`，配置增量同步模式，以及每个数据源的同步起点。完整的任务配置文件示例如下：

   {{< copyable "yaml" >}}

   ```yaml
   name: task-test             # 任务名称，需要全局唯一
   task-mode: incremental # 任务模式，设为 "incremental" 即只进行增量数据迁移

   ## 配置下游 TiDB 数据库实例访问信息
   target-database:       # 下游数据库实例配置
     host: "127.0.0.1"
     port: 4000
     user: "root"
     password: ""         # 如果密码不为空，则推荐使用经过 dmctl 加密的密文

   ##  使用黑白名单配置需要同步的表
   block-allow-list:   # 数据源数据库实例匹配的表的 block-allow-list 过滤规则集，如果 DM 版本早于 v2.0.0-beta.2 则使用 black-white-list
     bw-rule-1:        # 黑白名单配置项 ID
       do-dbs: ["log"] # 迁移哪些库

   ## 【可选配置】如果增量数据迁移需要重复迁移已经在全量数据迁移中完成迁移的数据，则需要开启 safe mode 避免增量数据迁移报错
   ##  该场景多见于，全量迁移的数据不属于数据源的一个一致性快照，随后从一个早于全量迁移数据之前的位置开始同步增量数据
   syncers:            # sync 处理单元的运行配置参数
     global:           # 配置名称
       safe-mode: true # 设置为 true，则将来自数据源的 `INSERT` 改写为 `REPLACE`，将 `UPDATE` 改写为 `DELETE` 与 `REPLACE`。

   ## 配置数据源
   mysql-instances:
     - source-id: "mysql-01"         # 数据源 ID，可以从数据源配置中获取
       block-allow-list: "bw-rule-1" # 引入上面黑白名单配置
       syncer-config-name: "global"  # 引用上面的 syncers 增量数据配置
       meta:                         # `task-mode` 为 `incremental` 且下游数据库的 `checkpoint` 不存在时 binlog 迁移开始的位置; 如果 `checkpoint` 存在，以 `checkpoint` 为准
         binlog-name: "mysql-bin.000001"
         binlog-pos: 2022
         binlog-gtid: "09bec856-ba95-11ea-850a-58f2b4af5188:1-9"
   ```

2. 使用 `start-task` 命令创建同步任务：

   {{< copyable "shell-regular" >}}

   ```bash
   tiup dmctl --master-addr <master-addr> start-task task.yaml
   ```

   ```
   {
       "result": true,
       "msg": "",
       "sources": [
           {
               "result": true,
               "msg": "",
               "source": "mysql-01",
               "worker": "127.0.0.1:8262"
           }
       ]
   }
   ```

3. 使用 `query-status` 查看同步任务，确认无报错信息：

   {{< copyable "shell-regular" >}}

   ```bash
   tiup dmctl --master-addr <master-addr> query-status test
   ```

   ```
   {
       "result": true,
       "msg": "",
       "sources": [
           {
               "result": true,
               "msg": "",
               "sourceStatus": {
                   "source": "mysql-01",
                   "worker": "127.0.0.1:8262",
                   "result": null,
                   "relayStatus": null
               },
               "subTaskStatus": [
                   {
                       "name": "task-test",
                       "stage": "Running",
                       "unit": "Sync",
                       "result": null,
                       "unresolvedDDLLockID": "",
                       "sync": {
                           "totalEvents": "0",
                           "totalTps": "0",
                           "recentTps": "0",
                           "masterBinlog": "(mysql-bin.000001, 2022)",
                           "masterBinlogGtid": "09bec856-ba95-11ea-850a-58f2b4af5188:1-9",
                           "syncerBinlog": "(mysql-bin.000001, 2022)",
                           "syncerBinlogGtid": "",
                           "blockingDDLs": [
                           ],
                           "unresolvedGroups": [
                           ],
                           "synced": true,
                           "binlogType": "remote"
                       }
                   }
               ]
           }
       ]
   }
   ```

## 测试同步任务

在数据源数据库插入新增数据：

{{< copyable "sql" >}}

```sql
MySQL [log]> INSERT INTO messages VALUES (4, 'msg4'), (5, 'msg5');
Query OK, 2 rows affected (0.010 sec)
Records: 2  Duplicates: 0  Warnings: 0
```

此时数据源数据为：

```sql
MySQL [log]> SELECT * FROM messages;
+----+---------+
| id | message |
+----+---------+
|  1 | msg1    |
|  2 | msg2    |
|  3 | msg3    |
|  4 | msg4    |
|  5 | msg5    |
+----+---------+
5 rows in set (0.001 sec)
```

查询下游数据库，可以发现 `(3, 'msg3')` 之后的数据已同步成功：

```sql
MySQL [log]> SELECT * FROM messages;
+----+---------+
| id | message |
+----+---------+
|  4 | msg4    |
|  5 | msg5    |
+----+---------+
2 rows in set (0.001 sec)
```
