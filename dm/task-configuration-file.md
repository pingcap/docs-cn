---
title: DM 任务配置文件介绍
---

# DM 任务配置文件介绍

本文档主要介绍 Data Migration (DM) 的任务基础配置文件，包含[全局配置](#全局配置)和[实例配置](#实例配置)两部分。

完整的任务配置参见 [DM 任务完整配置文件介绍](/dm/task-configuration-file-full.md)。关于各配置项的功能和配置，请参阅[数据迁移功能](/dm/dm-key-features.md)。

## 关键概念

关于包括 `source-id` 和 DM-worker ID 在内的关键概念的介绍，请参阅[关键概念](/dm/dm-config-overview.md#关键概念)。

## 基础配置文件示例

下面是一个基础的配置文件示例，通过该示例可以完成简单的数据迁移功能。

```yaml
---

# ----------- 全局配置 -----------
## ********* 基本信息配置 *********
name: test             # 任务名称，需要全局唯一
task-mode: all         # 任务模式，可设为 "full"、"incremental"、"all"

target-database:       # 下游数据库实例配置
  host: "127.0.0.1"
  port: 4000
  user: "root"
  password: ""         # 如果密码不为空，则推荐使用经过 dmctl 加密的密文

## ******** 功能配置集 **********
block-allow-list:        # 上游数据库实例匹配的表的 block-allow-list 过滤规则集，如果 DM 版本早于 v2.0.0-beta.2 则使用 black-white-list
  bw-rule-1:             # 黑白名单配置的名称
    do-dbs: ["all_mode"] # 迁移哪些库

# ----------- 实例配置 -----------
mysql-instances:
  - source-id: "mysql-replica-01"  # 上游实例或者复制组 ID，参考 `dm-master.toml` 的 `source-id` 配置
    block-allow-list:  "bw-rule-1" # 黑白名单配置名称，如果 DM 版本早于 v2.0.0-beta.2 则使用 black-white-list
    mydumper-thread: 4             # dump 处理单元用于导出数据的线程数量
    loader-thread: 16              # load 处理单元用于导入数据的线程数量，当有多个实例同时向 TiDB 迁移数据时可根据负载情况适当调小该值
    syncer-thread: 16              # sync 处理单元用于复制增量数据的线程数量，当有多个实例同时向 TiDB 迁移数据时可根据负载情况适当调小该值

  - source-id: "mysql-replica-02" # 上游实例或者复制组 ID，参考 `dm-master.toml` 的 `source-id` 配置
    block-allow-list:  "bw-rule-1" # 黑白名单配置名称，如果 DM 版本早于 v2.0.0-beta.2 则使用 black-white-list
    mydumper-thread: 4             # dump 处理单元用于导出数据的线程数量
    loader-thread: 16              # load 处理单元用于导入数据的线程数量，当有多个实例同时向 TiDB 迁移数据时可根据负载情况适当调小该值
    syncer-thread: 16              # sync 处理单元用于复制增量数据的线程数量，当有多个实例同时向 TiDB 迁移数据时可根据负载情况适当调小该值
```

## 配置顺序

通过上面的配置文件示例，可以看出配置文件总共分为两个部分：`全局配置`和`实例配置`，其中`全局配置`又分为`基础信息配置`和`功能配置集`，配置顺序如下：

1. 编辑[全局配置](#全局配置)。
2. 根据全局配置编辑[实例配置](#实例配置)。

## 全局配置

### 任务基本信息配置

配置任务的基本信息，配置项的说明参见以上示例配置文件中的注释。关于 `task-mode` 的特殊说明如下：

- 描述：任务模式，可以通过任务模式来指定需要执行的数据迁移工作。
- 值为字符串（`full`，`incremental` 或 `all`）。
    - `full`：只全量备份上游数据库，然后将数据全量导入到下游数据库。
    - `incremental`：只通过 binlog 把上游数据库的增量修改复制到下游数据库, 可以设置实例配置的 `meta` 配置项来指定增量复制开始的位置。
    - `all`：`full` + `incremental`。先全量备份上游数据库，将数据全量导入到下游数据库，然后从全量数据备份时导出的位置信息 (binlog position) 开始通过 binlog 增量复制数据到下游数据库。

> **注意：**
>
> DM 2.0 及更新的版本使用 dumpling 工具执行全量备份。全量备份过程中会使用 [`FLUSH TABLES WITH READ LOCK`](https://dev.mysql.com/doc/refman/8.0/en/flush.html#flush-tables-with-read-lock) 短暂地中断备份库的 DML 和 DDL 操作，从而保证并发备份连接的一致性并记录 binlog 位置用于增量复制。所有的并发备份连接启动事务后释放该锁。
> 
> 推荐在业务低峰或者 MySQL 备库上进行全量备份。

### 功能配置集

对于一般的业务场景，只需要配置黑白名单过滤规则集，配置说明参见以上示例配置文件中 `block-allow-list` 的注释以及 [Block & Allow Lists](/dm/dm-key-features.md#block--allow-table-lists)

## 实例配置

本小节定义具体的数据迁移子任务，DM 支持从单个或者多个上游 MySQL 实例迁移数据到同一个下游数据库实例。配置项说明参见以上示例配置文件中 `mysql-instances` 的注释。

## 修改任务配置

因为 DM 集群会持久化保存任务配置，所以修改任务配置需要通过 `stop-task`、`start-task` 将修改后的配置更新到 DM 集群中，如果直接修改任务配置文件，但是不重启任务，配置变更不会生效，DM 集群重启时仍然会读取之前保存的任务配置。

这里以修改 `timezone` 配置为例，举例说明任务配置修改步骤：

1. 修改任务配置文件，将 `timezone` 设置为 `Asia/Shanghai`

2. 通过 `stop-task` 命令停止任务：`stop-task <task-name | task-file>`

3. 通过 `start-task` 命令启动任务：`start-task <config-file>`

4. 在 DM v2.0.1 及其以后版本中，可通过 `get-config` 命令检查配置是否生效：`get-config task <task-name>`
