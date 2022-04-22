---
title: Data Migration 中的 DML 同步机制
summary: 本文介绍了 DM 核心处理单元 Sync 如何同步 DML 语句。
---

# Data Migration 中的 DML 同步机制

本文介绍了 DM 核心处理单元 Sync 如何同步从数据源或 relay log 中读取到的 DML。本文将介绍 Binlog 的整体处理流程，包括 binlog 读取、过滤、路由、转换、优化以及执行等逻辑，并详细解读 DML 优化逻辑和 DML 执行逻辑。

## DML 处理流程

Sync 单元对 DML 的处理步骤如下：

1. 从 MySQL、MariaDB 或 relay log 中，读取 binlog event。
2. 转换读取到的 binlog event：

    1. [Binlog filter](/dm/dm-key-features.md#binlog-event-filter)：根据 binlog 表达式过滤 binlog event，通过 `filters` 配置。
    2. [Table routing](/dm/dm-key-features.md#table-routing)：根据“库/表”路由规则对“库/表”名进行转换，通过 `routes` 配置。
    3. [Expression filter](/filter-dml-event.md)：根据 SQL 表达式过滤 binlog event，通过 `expression-filter` 配置。

3. 优化 DML 执行：

    1. Compactor：将对同一条记录（主键相同）的多个操作合并成一个操作，通过 `syncer.compact` 开启。
    2. Causality：将不同记录（主键不同）进行冲突检测，分发到不同的 group 并发处理。
    3. Merger：将多条 binlog 合并成一条 DML，通过 `syncer.multiple-rows` 开启。

4. 将 DML 执行到下游。
5. 定期保存 binlog position 或 GTID 到 checkpoint 中。

![DML 处理逻辑](/media/xxx.jpg)

## DML 优化逻辑

Sync 单元通过 Compactor、Causality、Merger 三个步骤，实现对 DML 的优化逻辑。

### Compactor

DM 根据上游 binlog 记录，捕获记录的变更并同步到下游。当上游对同一条记录短时间内做了多次变更时（`INSERT`/`UPDATE`/`DELETE`），DM 可以通过 Compactor 将多次变更压缩成一次变更，减少下游压力，提升吞吐。例如：

```
INSERT + UPDATE => INSERT
INSERT + DELETE => DELETE
UPDATE + UPDATE => UPDATE
UPDATE + DELETE => DELETE
DELETE + INSERT => UPDATE
```

### Causality

MySQL binlog 顺序同步模型要求按照 binlog 顺序依次同步 binlog event，这样的同步模型无法满足高 QPS 低同步延迟的需求。此外，由于不是所有的 binlog 涉及到的操作都存在冲突，顺序同步也是非必要的。

DM 通过冲突检测机制，识别出需要顺序执行的 binlog，确保这些 binlog 顺序执行的同时，最大程度地保持其他 binlog 并发执行，以此提高 binlog 同步的性能。

Causality 采用一种类似并查集的算法，对每一个 DML 进行分类，将相互关联的 DML 分为一组。具体算法可参考[并行执行 DML](https://pingcap.com/zh/blog/tidb-binlog-source-code-reading-8#并行执行DML)。

### Merger

根据 MySQL binlog 协议，每条 binlog 对应一行数据的变更操作。通过 Merger，DM 可以将多条 binlog 合并成一条 DML，再执行到下游，减少网络的交互。例如：

```
  INSERT tb(a,b) VALUES(1,1);
+ INSERT tb(a,b) VALUES(2,2);
= INSERT tb(a,b) VALUES(1,1),(2,2);

  UPDATE tb SET a=1, b=1 WHERE a=1;
+ UPDATE tb SET a=2, b=2 WHERE a=2;
= INSERT tb(a,b) VALUES(1,1),(2,2) ON DUPLICATE UPDATE a=VALUES(a), b=VALUES(b)

  DELETE tb WHERE a=1
+ DELETE tb WHERE a=2
= DELETE tb WHERE (a) IN (1),(2);
```

## DML 执行逻辑

Sync 单元对 DML 进行优化后，再进行执行逻辑。

### DML 生成

DM 内嵌一个 schema tracker，用于记录上下游的 schema 信息：

* 当 DM 收到 DDL 时，DM 更新内部 schema tracker 的表结构。
* 当收到 DML 时，DM 根据 schema tracker 的表结构生成对应的 DML。

生成 DML 的具体逻辑如下：

1. Sync 记录上游的初始表结构：
    * 当启动全量与增量任务时，Sync 使用**上游全量同步时导出的表结构**作为上游的初始表结构。
    * 当启动增量任务时，由于 MySQL binlog 没有记录表结构信息，Sync 使用**下游对应的表的表结构**作为上游的初始表结构。
2. 由于用户上下游表结构可能不一致，例如下游比上游多了额外的列，或者上下游主键不一致，为了保证数据同步的正确性，DM 记录**下游对应表的主键和唯一键信息**。
3. DM 生成 DML：
    * 使用 **schema tracker 中记录的上游表结构**生成 DML 语句的列。
    * 使用 **binlog 中记录的列值**生成 DML 语句的列值。
    * 使用 **schema tracker 中记录的下游主键或唯一键**生成 DML 语句中的 `WHERE` 条件。当表结构无唯一键时，DM 会使用 binlog 中记录的所有列值作为 `WHERE` 条件。

### Worker count

Causality 可以通过冲突检测算法将 binlog 分成多个 group 并发地执行到下游。DM 通过设置 worker-count，控制并发的数量。当下游 TiDB 的 CPU 占用不高时，增大并发的数量可以有效地提高数据同步的吞吐量。

你可以通过 [`syncer.worker-count` 配置项](/dm/dm-tune-configuration.md#worker-count)，修改并发迁移 DML 的线程数量。

### Batch

DM 将多条 DML 攒到一个事务中执行到下游。当 DML Worker 收到 DML 时，将 DML 加入到缓存中。当缓存中 DML 数量达到预定阈值时，或者 DML worker 较长时间没有收到 DML 时，DML worker 将缓存中的 DML 执行到下游。

你可以通过 [`syncer.batch` 配置项](/dm/dm-tune-configuration.md#batch)，修改每个事务包含的 DML 的数量。

### checkpoint

DML 执行和 checkpoint 更新的操作不是原子的。

在 DM 中，checkpoint 默认每 30 秒更新一次。同时，由于存在多个 DML worker 进程，checkpoint 进程会计算所有 DML worker 中同步进度最晚的 binlog 位点，将该位点作为当前同步的 checkpoint。所有早于此位点的 binlog，都已保证被成功地执行到下游。

关于 Checkpoint 的详细信息，参考 [Checkpoint](/dm/dm-checkpoint.md)。

## 注意事项

### 事务一致性

DM 是按照“行级别”进行数据同步的。在 DM 中，上游的一个事务会被拆成多行，分发到不同的 DML Worker 中并发执行。因此，当 DM 同步任务报错暂停，或者用户手动暂停任务时，下游可能停留在一个中间状态；即上游一个事务中的 DML 语句，可能一部分同步到下游，一部分没有，导致下游处于不一致的状态。

为了尽可能使任务暂停时下游处于一致状态，DM v5.3.0 起，在任务暂停时会等待上游事务全部同步到下游后，才真正暂停任务。这个等待时间为 10 秒，如果上游一个事务在 10 秒内还未全部同步到下游，那么下游仍然可能处于不一致的状态。

### 安全模式

DML 执行和 checkpoint 写操作不是同步的，并且写 checkpoint 操作和写下游数据也并不能保证原子性。当 DM 因为某些原因异常退出时，checkpoint 可能只记录到退出时刻之前的一个恢复点。因此，当同步任务重启时，DM 可能会重复写入部分数据，也就是说，DM 实际上提供的是“至少一次处理”的逻辑（At-least-once processing），相同的数据可能会被处理一次以上。

为了保证数据是可重入的，DM 在异常重启时会进入安全模式。具体逻辑参阅 [DM 安全模式](/dm/dm-safe-mode.md)。

开启安全模式期间，为了保证数据可重入，DM 会进行如下转换：

* 将上游 `INSERT` 语句，转换成 `REPLACE` 语句
* 将上游 `UPDATE` 语句，转换成 `DELETE` + `REPLACE` 语句。

### 精确一次处理 (Exactly-Once Processing)

DM 的拆分事务再并发同步的逻辑存在已知问题，比如下游可能停在一个不一致的状态，数据的同步顺序与上游不一致，可能导致数据重入。安全模式期间 `REPLACE` 语句会有一定的性能损失，如果下游需要捕获数据变更（如 change data capture），那么重复处理也不可接受。
