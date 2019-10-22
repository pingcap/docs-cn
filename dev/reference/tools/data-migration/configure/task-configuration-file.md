---
title: DM 任务配置文件介绍
category: reference
---

# DM 任务配置文件介绍

本文档主要介绍 Data Migration (DM) 的任务基础配置文件 [`task_basic.yaml`](https://github.com/pingcap/dm/blob/master/dm/master/task_basic.yaml)，包含[全局配置](#全局配置) 和[实例配置](#实例配置) 两部分。

完整的任务配置参见 [DM 任务完整配置文件介绍](/dev/reference/tools/data-migration/configure/task-configuration-file-full.md)

关于各配置项的功能和配置，请参阅[数据同步功能](/dev/reference/tools/data-migration/features/overview.md)。

## 关键概念

关于包括 `source-id` 和 DM-worker ID 在内的关键概念的介绍，请参阅[关键概念](/dev/reference/tools/data-migration/configure/overview.md#关键概念)。

## 基础配置文件示例

下面是一个基础的配置文件示例，通过该示例可以完成简单的数据同步功能。

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
  password: ""         # 如果不为空则需经过 dmctl 加密

## ******** 功能配置集 **********
black-white-list:        # 上游数据库实例匹配的表的 black & white list 过滤规则集
  bw-rule-1:             # 黑白名单配置的名称
    do-dbs: ["all_mode"] # 同步哪些库

# ----------- 实例配置 -----------
mysql-instances:
  - source-id: "mysql-replica-01"  # 上游实例或者复制组 ID，参考 `dm-master.toml` 的 `source-id` 配置
    black-white-list:  "bw-rule-1" # 黑白名单配置名称
    mydumper-thread: 4             # mydumper 用于导出数据的线程数量，在 v1.0.2 版本引入
    loader-thread: 16              # loader 用于导入数据的线程数量，在 v1.0.2 版本引入
    syncer-thread: 16              # syncer 用于同步增量数据的线程数量，在 v1.0.2 版本引入

  - source-id: "mysql-replica-02" # 上游实例或者复制组 ID，参考 `dm-master.toml` 的 `source-id` 配置
    black-white-list:  "bw-rule-1" # 黑白名单配置名称
    mydumper-thread: 4             # mydumper 用于导出数据的线程数量，在 v1.0.2 版本引入
    loader-thread: 16              # loader 用于导入数据的线程数量，在 v1.0.2 版本引入
    syncer-thread: 16              # syncer 用于同步增量数据的线程数量，在 v1.0.2 版本引入
```

## 配置顺序

通过上面的配置文件示例，可以看出配置文件总共分为两个部分：`全局配置`和`实例配置`，其中`全局配置`又分为`基础信息配置`和`功能配置集`，配置顺序如下：

1. 编辑[全局配置](#全局配置)。
2. 根据全局配置编辑[实例配置](#实例配置)。

## 全局配置

### 任务基本信息配置

配置任务的基本信息，配置项的说明参见以上示例配置文件中的注释。其中 `task-mode` 需要特殊说明：

`task-mode`

- 描述：任务模式，可以通过任务模式来指定需要执行的数据迁移工作。
- 值为字符串（`full`，`incremental` 或 `all`）。
    - `full`：只全量备份上游数据库，然后将数据全量导入到下游数据库。
    - `incremental`：只通过 binlog 把上游数据库的增量修改同步到下游数据库, 可以设置实例配置的 `meta` 配置项来指定增量同步开始的位置。
    - `all`：`full` + `incremental`。先全量备份上游数据库，将数据全量导入到下游数据库，然后从全量数据备份时导出的位置信息 (binlog position) 开始通过 binlog 增量同步数据到下游数据库。

### 功能配置集

对于一般的业务场景，只需要配置黑白名单过滤规则集，配置说明参见以上示例配置文件中 `black-white-list` 的注释。

## 实例配置

本小节定义具体的数据同步子任务，DM 支持从单个或者多个上游 MySQL 实例同步数据到同一个下游数据库实例。
配置项说明参见以上示例配置文件中 `mysql-instances` 的注释。
