---
title: TiDB 垃圾回收 (GC)
category: reference
---

# TiDB 垃圾回收 (GC)

TiDB 采用 MVCC 的方式来进行并发控制。当对数据进行更新或者删除时，原有的数据不会被立刻删除，而是会被保留一段时间，并且在这段时间内这些旧数据仍然可以被读取。这使得写入操作和读取操作不必互斥，并使读取历史数据成为可能。

存在超过一定时间并且不再使用的版本会被清理，否则它们将始终占用硬盘空间，并对性能产生负面影响。TiDB 使用一个垃圾回收 (GC) 机制来清理这些旧数据。

## 工作方式

TiDB 会周期性地进行 GC。每个 TiDB Server 启动后都会在后台运行一个 gc_worker，每个集群中会有其中一个 gc_worker 被选为 leader，leader 负责维护 GC 的状态并向所有的 TiKV Region leader 发送 GC 命令。

## 配置与监测方法

GC 相关的配置和运行状态记录在 `mysql.tidb` 这张系统表中，可以通过 SQL 语句进行检测和配置：

{{< copyable "sql" >}}

```sql
select VARIABLE_NAME, VARIABLE_VALUE from mysql.tidb;
```

```
+-----------------------+------------------------------------------------------------------------------------------------+
| VARIABLE_NAME         | VARIABLE_VALUE                                                                                 |
+-----------------------+------------------------------------------------------------------------------------------------+
| bootstrapped          | True                                                                                           |
| tidb_server_version   | 18                                                                                             |
| tikv_gc_leader_uuid   | 58accebfa7c0004                                                                                |
| tikv_gc_leader_desc   | host:ip-172-16-30-5, pid:95472, start at 2018-04-11 13:43:30.73076656 +0800 CST m=+0.068873865 |
| tikv_gc_leader_lease  | 20180418-11:02:30 +0800 CST                                                                    |
| tikv_gc_run_interval  | 10m0s                                                                                          |
| tikv_gc_life_time     | 10m0s                                                                                          |
| tikv_gc_last_run_time | 20180418-10:59:30 +0800 CST                                                                    |
| tikv_gc_safe_point    | 20180418-10:58:30 +0800 CST                                                                    |
| tikv_gc_concurrency   | 1                                                                                              |
+-----------------------+------------------------------------------------------------------------------------------------+
10 rows in set (0.02 sec)
```

其中，`tikv_gc_run_interval`，`tikv_gc_life_time`，`tikv_gc_concurrency` 这三条记录可以手动配置。其余带有 `tikv_gc` 前缀的记录为当前运行状态的记录， TiDB 会自动更新这些记录，请勿手动修改。

`tikv_gc_run_interval` 是 GC 运行时间间隔。`tikv_gc_life_time` 是历史版本的保留时间，每次进行 GC 时，会清理超过该时间的历史数据。这两项配置不应低于 10 分钟，默认值均为 10 分钟。可以直接用 SQL 修改其数值来进行配置。比如，如果想保留一天以内的历史数据，就可以执行：

{{< copyable "sql" >}}

```sql
update mysql.tidb set VARIABLE_VALUE = '24h' where VARIABLE_NAME = 'tikv_gc_life_time';
```

时长字符串的形式是数字后接时间单位的序列，如 `24h`、`2h30m`、`2.5h`。可以使用的时间单位包括 "h"、"m"、"s"。

> **注意：**
>
> 在数据更新频繁的场景下如果将 `tikv_gc_life_time` 设置得比较大（如数天甚至数月），可能会有一些潜在的问题：
>
> * 随着版本的不断增多，数据占用的磁盘空间会随之增加。
> * 大量的历史版本会在一定程度上导致查询变慢，主要影响范围查询（如 `select count(*) from t`）。
> * 如果在运行中突然将 `tikv_gc_life_time` 配置调小，可能会导致短时间内大量历史数据被删除，造成 I/O 负担。

`tikv_gc_concurrency` 是运行 GC 的并发数。默认该选项为 1，即单线程运行，逐个向每个涉及的 Region 发起请求并等待响应。可以增加该数值以改善性能，最大不能超过 128。

`tikv_gc_leader_uuid`，`tikv_gc_leader_desc`，`tikv_gc_leader_lease` 是当前的 GC leader 的信息。`tikv_gc_last_run_time` 是上一次执行 GC 的时间。

`tikv_gc_safe_point` 的含义是，在该时间点以前的版本已经被 GC 清理，并保证该时间点以后的读取可以正确进行。

## 实现细节

GC 的实施过程实际上比较复杂。我们要在保证一致性不被破坏的前提下，清除不再使用的数据。具体来说，每次执行 GC，要顺序执行三个步骤：

### 1. Resolve Locks

TiDB 的事务是基于 Google Percolator 模型实现的，事务的提交是一个两阶段提交的过程。第一阶段完成时，所有涉及的 key 会加上一个锁，其中一个锁会被设定为 Primary，其余的锁（Secondary）则会指向 Primary；第二阶段会将 Primary 锁所在的 key 加上一个 Write 记录，并去除锁。这里的 Write 记录就是历史上对该 key 进行写入或删除，或者该 key 上发生事务回滚的记录。Primary 锁被替换为何种 Write 记录标志着该事务提交成功与否。接下来，所有 Secondary 锁也会被依次替换。如果替换这些 Secondary 锁的线程死掉了，锁就残留了下来。在 GC 过程中如果遇到了时间戳在 safe point 之前的这样的锁，就会根据该事务提交与否，将该锁也替换成 Write 记录。

这一步是必须的，因为如果其 Primary 的 Write 记录被 GC 清除掉了，就再也无法知道该事务是否成功，也就难以保证一致性。

### 2. Delete Ranges

DeleteRanges 通常在 drop table 这样的操作之后需要进行，用于删除可能很大的一个区间。如果 TiKV 的 `use_delete_range` 选项没有打开，那么 TiKV 会把范围中的 key 逐个删除。

### 3. Do GC

这一步把每一个 key 的 safe point 之前的数据和 Write 记录清除掉。有一个特例是，如果在 safe point 之前的所有 `Put` 类型和 `Delete` 类型的 Write 记录中，最后一个记录是 `Put`（即写入），那么该记录（及其对应的数据）不能被直接删除。否则，时间戳在 safe point 之后、该 key 的下一个版本之前的读取操作将无法读取到该数据。
