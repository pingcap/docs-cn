---
title: DM Checkpoint 作用机制
---

# Checkpoint 作用机制

DM 里有两种 checkpoint：

* 内存 checkpoint：表示这个 binlog 已经被 DM 接收，正处在同步队列中，其状态可能是还未同步、正在同步、已经同步。
* flushed checkpoint：指的是已经写入下游数据库中的同步进度，表示某个位置的 binlog 一定已经成功同步到了下游。

对于两种 checkpoint，都包含以下三个信息：

- global checkpoint：下次重启任务时开始同步的 binlog 位置。小于这个位置的所有 binlog 一定已经被同步。内存的 global checkpoint 在重启时由 flushed checkpoint 重新加载。
- table checkpoints：每个表同步的 binlog 位置以及此时的表结构（以 TiDB TableInfo JSON 表示）。
- safe mode exit point：如果不为空，小于这个 checkpoint 的 binlog 有可能在同步队列中，但大于它的则一定不在。在任务从错误恢复重启时，它可以清楚地标识出可能已经同步过的 binlog，因此 (table checkpoint, safe mode exit point] 之间的同步作业必须开启 [safe mode](/dm/dm-safe-mode.md)，**以免出现重复处理而导致的下游报错**。重启任务后，binlog position 超过 safe mode exit point 时，DM 关闭 safe mode。

由它们的语义我们可以知道，这三个信息的顺序是：global checkpoint ≤ table checkpoints ≤ safe mode exit point。

## 内存 checkpoint

### 任务启动/重启

由于每次访问和写入 flushed checkpoint 的开销很大，因此，将内存 checkpoint 作为 flushed checkpoint 在某种意义上的缓存，可以减少访问和写入 flushed checkpoint 的开销。

当 DM 启动任务时，DM 会从数据库中读取该任务的 flushed checkpoint，并将 flushed checkpoint 恢复成内存 checkpoint：

* 如果 flushed checkpoint 存在，说明这个任务是重启任务，binlog 的同步位置会被定位到 global checkpoint，这里将作为下次同步任务的开始位置。
* 如果 flushed checkpoint 不存在，说明该任务是第一次启动或者重新开始同步，DM 会在下游新建一个 checkpoint。

### 内存 checkpoint 的更新时机

- global checkpoint：当遇到 XID event 或 DDL event 时，将当前位置写入 global checkpoint。
- table checkpoints：遇到 DML event 和 DDL event 时，将当前位置写入 table checkpoint。
- safe mode exit point：在处理每个 event 之前，比较 currentLocation 和 safe mode exit point。如果前者比较大，则需要更新后者为当前位置。

## flushed checkpoint

### 写入时机

1. 当 XID event 或者 rows event 被处理完时，DM 会调用 checkShouldFlush 函数判断是否需要写入 flushed checkpoint。如果超过一定 interval 都还没有 flush 过，会尝试将 checkpoint 写入到下游。
2. DM 处理完 DDL event 后，会尝试将内存 checkpoint 写入到下游。
3. DM 在尝试写入 checkpoint 时，会先判断 global checkpoint 和 table checkpoints 的值是否有改变，没有改变则不写。
4. safe mode exit point：只在 syncer 退出时，等待同步队列写入下游后 flush。

## 常见问题

### 为什么根据配置文件启动，实际的 position 地址却没有根据配置文件定义的 position ？

在配置文件中定义的 position 只有在第一次启动任务且模式是 incremental 的情况下生效。如果任务经历暂停、重启等，syncer 会根据 checkpoint 中记录的 position 启动。如果模式是 all 且第一次启动，则会根据全量导入产生的 meta 文件来确定 position。

DM 启动任务时，binlog position 同步的处理优先级如下：

- 使用 [`start-task` 命令](/dm/dm-create-task.md)创建任务时，以 `--start-time` 参数指定的任务起始位点（6.0 新功能）
- meta 信息中记录的 checkpoint 位置
- 任务配置文件中指定的 position

### 如何清理 checkpoint

checkpoint 一般存放在下游数据库中。如果配置文件没有定义 meta 信息的库名，则默认在 dm_meta 库中。不同的任务的同步进度存放在以任务名为表名的表中。你可以通过以下两种方式清理 checkpoint：

* 在下次启动任务时，新增 `--remove-meta` flag 来清理已存在的 checkpoint。
* 清理相关表的表内容。（不推荐）

### async checkpoint 的机制？

同步 checkpoint 在 flush 之前，必须保证所有的 job worker 把所有的 jobs 都执行完之后，才将 checkpoint 写入。这个过程会导致后续的 event 必须等前面的 job 都执行完才分配给 job worker 执行，从而导致性能下降。async checkpoint 则会让 worker 来通知 async checkpoint routine 是否已经之前的 job 都 flush 完毕，而期间 worker 会正常活动；当所有 worker flush 完成后，则触发 checkpoint flush。

async checkpoint 会在 syncer 内部维护复数个 casuality map（用来检查冲突），当 checkpoint 的同步比较慢时，内部可能会有多个 casaulity map，而每次检查冲突都要遍历检查这些 map 导致性能下降。大部分情况下，async checkpoint 性能更高。
