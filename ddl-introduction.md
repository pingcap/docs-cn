---
title: DDL 语句的执行原理及最佳实践
summary: 介绍 TiDB 中 DDL 语句的实现原理、在线变更过程、最佳实践等内容。
---

# DDL 语句的执行原理及最佳实践

本文介绍了 TiDB 中 DDL 语句的执行原理（包括 DDL Owner 模块和在线变更 DDL 的流程）和最佳实践。

## DDL 执行原理

TiDB 采用在线异步变更的方式执行 DDL 语句，从而实现 DDL 语句的执行不会阻塞其他会话中的 DML 语句。因此，在业务执行过程中，你可以通过在线异步变更 DDL 对数据库对象定义进行变更。

### DDL 语句类型简介

按照执行期间是否阻塞用户业务，DDL 语句可以划分为：

- **离线 DDL 语句**：即数据库接收到用户的 DDL 语句后，会先对要修改的数据库对象进行加锁，再执行元数据变更，在 DDL 执行过程中将阻塞用户业务对数据的修改。

- **在线 DDL 语句**：即数据库在执行 DDL 语句时，通过一定的方法，使得 DDL 执行不阻塞用户业务，且能够保证用户业务可在 DDL 执行期间提交修改，在执行过程中保证对应对象的数据正确性与一致性。

按照是否需要操作 DDL 目标对象所包括的数据来划分，DDL 语句可以划分为：

- **逻辑 DDL 语句**：通常只修改数据库对象的元数据，不对变更对象存储的数据进行处理，例如变更表名或变更列名。

    在 TiDB 中，逻辑 DDL 语句又被称为 General DDL。General DDL 的执行时间通常较短，只需要几十毫秒或者几秒。执行这类 DDL 语句几乎不消耗系统资源，因此不会影响业务负载。

- **物理 DDL 语句**：不但会修改变更对象的元数据，同时也修改变更对象所存储的用户数据。例如，为表创建索引，不仅需要变更表的定义，同时也需要做一次全表扫描以构建新增加的索引。

    在 TiDB 中，物理 DDL 被称为 Reorg DDL（Reorg 即  Reorganization）。目前物理 DDL 只包含 `ADD INDEX` 以及有损列类型变更（例如从 `INT` 转成 `CHAR` 类型）这两种类型。物理 DDL 的特点是执行时间较长，且执行时间与表的数据量、机器配置以及业务负载有关。

    执行物理 DDL 会影响业务负载，具体有两个方面。一方面需要从 TiKV 中读取数据并写入新数据，因此会消耗 TiKV 的 CPU 及 I/O 资源。另一方面，**DDL Owner 所在的 TiDB 节点**或者**被 TiDB 分布式执行框架调度而执行 `ADD INDEX` 任务的 TiDB 节点**需要进行相应的计算，因此会消耗 TiDB 的 CPU 资源。

    > **注意：**
    >
    > DDL 语句对用户业务的影响通常都是由于执行物理 DDL 任务造成的。因此要优化 DDL 语句对于用户业务的影响，重点在于对物理 DDL 任务执行期间的设计，降低对于用户业务的影响。

### TiDB DDL 模块

TiDB DDL 模块引入 DDL Owner（简称 Owner）角色来代理执行所有进入到 TiDB 集群中的 DDL 语句。对于当前 TiDB DDL 模块的实现，在同一时间，整个 TiDB 集群中只有一个 TiDB 节点能当选为 Owner。当选 Owner 后，TiDB 节点中启动的 worker 才能处理集群中的 DDL 任务。

TiDB 通过 etcd 的选举功能从多个 TiDB 节点中选举出一个节点来担任 Owner 的宿主节点。默认情况下，每个 TiDB 节点都可能当选 Owner（你可以通过配置 `run-ddl` 控制某个 TiDB 节点是否竞选 Owner）。Owner 节点是有任期的，并会主动维护自己的任期，即续约。当 Owner 节点宕机后，其他节点可以通过 etcd 感知到并重新选举出新的 Owner，在集群中继续担任 DDL 任务执行者的角色。

DDL Owner 的简单示意图如下：

![DDL Owner](/media/ddl-owner.png)

你可以通过 `ADMIN SHOW DDL` 语句查看当前 DDL owner：

```sql
ADMIN SHOW DDL;
```

```sql
+------------+--------------------------------------+---------------+--------------+--------------------------------------+-------+
| SCHEMA_VER | OWNER_ID                             | OWNER_ADDRESS | RUNNING_JOBS | SELF_ID                              | QUERY |
+------------+--------------------------------------+---------------+--------------+--------------------------------------+-------+
|         26 | 2d1982af-fa63-43ad-a3d5-73710683cc63 | 0.0.0.0:4000  |              | 2d1982af-fa63-43ad-a3d5-73710683cc63 |       |
+------------+--------------------------------------+---------------+--------------+--------------------------------------+-------+
1 row in set (0.00 sec)
```

### TiDB 在线 DDL 异步变更的原理

TiDB DDL 模块从设计之初就选择了在线异步变更的模式，为 TiDB 的用户提供了不停机变更业务的服务能力。

DDL 变更即两个状态之间的切换（变更前 -> 变更后）。在线变更 DDL，是在两个状态之间引入多个相互兼容的小版本状态。同时，在同一个 DDL 语句在执行期间，对于同一集群中不同 TiDB 节点，允许不同节点的变更对象小版本存在不同（集群中各 TiDB 节点变更对象的小版本差距不超过两个版本），因为相邻两个小版本之间可以相互兼容。

通过多个小版本演进的方式，确保多个 TiDB 节点能够正确同步元数据，并保证期间执行用户事务更改数据的正确性与一致性。

以 `ADD INDEX` 为例，整个变更状态流程如下：

<SimpleTab>
<div label="Online DDL 异步变更流程（TiDB v6.3.0 前）">

在 TiDB v6.3.0 之前我们只支持以下方式的 DDL 执行方式。
```
absent -> delete only -> write only -> write reorg -> public
```
</div>
<div label="Online DDL Fast DDL 模式（TiDB v6.3.0 后）">

从 TiDB v6.5.0 之后我们提供 Fast DDL 执行方式。
```
absent -> delete only -> write only -> write reorg -> public
                                            ｜
                                       -----------
                                      ｜          ｜
                     (backfill fullcopy index)  (merge incremental part of index) 
```

原生 Online DDL 方案中处理最慢的地方是扫描全表创建索引数据的阶段，而创建索引数据的最大性能瓶颈点是按照事务批量回填索引的方式，因此我们考虑从全量数据的索引创建模式、数据传输、并行导入三方面进行改造。参考：[天下武功唯快不破：TiDB 在线 DDL 性能提升 10 倍](https://mp.weixin.qq.com/s/tyBAPm1p27FqgnZgvndPsA)
原生方案的问题：
1. 索引记录在事务两阶段提交的时间开销：因为每个索引事务提交的数据 batch-size 通常在 256 或者更小，当索引记录比较多的时候，索引以事务方式提交回 TiKV 的总事务提交时间是非常可观的。
2. 索引事务和用户事务提交冲突时回滚和重试的开销：原生方案在索引记录回填阶段采用事务方式提交数据，当该方式提交的索引记录与用户业务提交的索引记录存在冲突更新时，将触发用户事务或者索引回填事务回滚和重试，从而影响性能。

Fast DDL 优化项：
1. 引入批量模式：我们将原生方式中事务批量写入模式改进为文件批量导入的模式，如上图下半部分所示：首先仍是扫描全表数据，之后根据扫描的数据构造索引 KV 对并存入 TiDB 的本地存储，在 TiDB 对于 KV 进行排序后，最终以 Ingest 方式将索引记录写入 TiKV。新方案消除了两阶段事务的提交时间开销以及索引回填事务与用户事务提交冲突回滚的开销。
2. 提升数据传输效率：针对索引创建阶段的数据传输，我们做了极致的优化：原生方案中我们需要将每一行表记录返回到 TiDB，选出其中的索引需要的列，构造成为索引的 KV；新方案中，在 TiKV 层返回数据回 TiDB 之前我们先将索引需要的列取出，只返回创建索引真正需要的列，极大的降低了数据传输的总量，从而减少了整体创建索引的总时间。
3. 并行导入：最后，我们通过并行导入的方式将索引记录以 Ingest 方式导入到 TiKV，并行导入提升了数据写回 TiKV 的效率，但同时也给 TiKV 在线处理负载带来了一定压力。我们正在研发系列流控手段，让并行导入能够既充分利用 TiKV 的空闲带宽，同时不给 TiKV 正常处理负载带来过大压力。
</div>
</SimpleTab>

对于用户来说，新建的索引在 `public` 状态前都不可用。

<SimpleTab>
<div label="Online DDL 异步变更流程（TiDB v6.2.0 前）">

在 v6.2.0 之前，TiDB SQL 层中处理异步 Schema 变更的基本流程如下：

1. MySQL Client 发送给 TiDB server 一个 DDL 操作请求。

2. 某个 TiDB server 收到请求（即 TiDB server 的 MySQL Protocol 层对请求进行解析优化），然后发送到 TiDB SQL 层进行执行。

    TiDB SQL 层接到 DDL 请求后，会启动 `start job` 模块根据请求将请求封装成特定的 DDL Job（即 DDL 任务），然后将此 Job 按语句类型分类，分别存储到 KV 层的对应 DDL Job 队列，并通知自身对应的 worker 有 Job 需要处理。

3. 接收到处理 Job 通知的 worker，会判断自身是否处于 DDL Owner 的角色。如果是 Owner 角色则直接处理此 Job。如果没有处于 Owner 角色则退出不做任何处理。

    假设某台 TiDB server 不是 Owner 角色，那么其他某个节点一定有一个是 Owner。处于 Owner 角色的节点的 worker 通过定期检测机制来检查是否有 Job 可以被执行。如果发现有 Job ，那么 worker 就会处理该 Job。

4. Worker 处理完 Job 后，会将此 Job 从 KV 层对应的 Job queue 中移除，并放入 `job history queue`。之前封装 Job 的 `start job` 模块会定期在 `job history queue` 中查看是否有已经处理完成的 Job 的 ID。如果有，则这个 Job 对应的整个 DDL 操作结束执行。

5. TiDB server 将 DDL 处理结果返回至 MySQL Client。

在 TiDB v6.2.0 前，该 DDL 执行框架存在以下限制：

- TiKV 集群中只有 `general job queue` 和 `add index job queue` 两个队列，分别处理逻辑 DDL 和物理 DDL。
- DDL Owner 总是以先入先出的方式处理 DDL Job。
- DDL Owner 每次只能执行一个同种类型（逻辑或物理）的 DDL 任务，这个约束较为严格。

这些限制可能会导致一些“非预期”的 DDL 阻塞行为。具体可以参考 [SQL FAQ - DDL 执行](/faq/sql-faq.md#ddl-执行)。

</div>
<div label="并发 DDL 框架（TiDB v6.2 及以上）">

在 TiDB v6.2 之前，由于 Owner 每次只能执行一个同种类型（逻辑或物理）的 DDL 任务，这个约束较为严格，同时影响用户体验。

当 DDL 任务之间不存在相关依赖时，并行执行并不会影响数据正确性和一致性。例如：用户 A 在 `T1` 表上增加一个索引，同时用户 B 从 `T2` 表删除一列。这两条 DDL 语句可以并行执行。

为了提升 DDL 执行的用户体验，从 v6.2.0 起，TiDB 对原有的 DDL Owner 角色进行了升级，使得 Owner 能对 DDL 任务做相关性判断，判断逻辑如下：

+ 涉及同一张表的 DDL 相互阻塞。
+ `DROP DATABASE` 和数据库内所有对象的 DDL 互相阻塞。
+ 涉及不同表的加索引和列类型变更可以并发执行。
+ 逻辑 DDL 需要等待之前正在执行的逻辑 DDL 执行完才能执行。
+ 其他情况下 DDL 可以根据 Concurrent DDL 并行度可用情况确定是否可以执行。

具体来说，TiDB 在 v6.2.0 中对 DDL 执行框架进行了如下升级：

+ DDL Owner 能够根据以上判断逻辑并行执行 DDL 任务。
+ 改善了 DDL Job 队列先入先出的问题。DDL Owner 不再选择当前队列最前面的 DDL Job，而是选择当前可以执行的 DDL Job。
+ 扩充了处理物理 DDL 的 worker 数量，使得能够并行地添加多个物理 DDL。

    因为 TiDB 中所有支持的 DDL 任务都是以在线变更的方式来实现的，TiDB 通过 Owner 即可对新的 DDL Job 进行相关性判断，并根据相关性结果进行 DDL 任务的调度，从而使分布式数据库实现了和传统数据库中 DDL 并发相同的效果。

并发 DDL 框架的实现进一步加强了 TiDB 中 DDL 语句的执行能力，并更符合商用数据库的使用习惯。

</div>
<div label="Fast DDL（TiDB v6.3 及以上）">

从 TiDB v6.3 版本开始，我们开始对于 DDL 语句执行进行优化，通过提供给 DDL 语句提供快速执行路径来提升用户在使用 TiDB 在线 DDL 服务的体验，同时也通过提升 10 倍在线增加索引速度的优化，使得 TiDB 大数据量用户真的可以在业务运行过程中能够真的享受到 TiDB Fast Online DDL 带来的对于业务的收益。

从 v6.5 我们将 Fast DDL 模式默认打开，为了让更多用户可以体验到我们对的服务，和 Fast DDL 相关的参数如下：

System Variables
- [`tidb_ddl_enable_fast_reorg=on`](/system-variables.md#tidb_ddl_enable_fast_reorg-span-classversion-mark-v630-span): 这个参数用来控制 Fast 模式起停；
- ['tidb_ddl_disk_quota`](/system-variables.md#tidb_ddl_disk_quota-span-classversion-mark-v630-span): 这个参数设置 Fast DDL 本地磁盘的大小。([100 GiB, 1 PiB])；

Config parameters
TiDB 配置参数：
- [`temp-dir`](/command-line-flags-for-tidb-configuration.md#--temp-dir): 用来指定 TiDB Fast DDL 本地存储路径。
</div>
</SimpleTab>

## 最佳实践

### 通过系统变量来平衡物理 DDL 的执行速度与对业务负载的影响

执行物理 DDL（包括添加索引或列类型变更）时，适当调整以下系统变量可以平衡 DDL 执行速度与对业务负载的影响：

- [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)：这个变量用来设置 DDL 操作 reorg worker 的数量，控制回填的并发度。

- [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)：这个变量用来设置 DDL 操作 `re-organize` 阶段的 batch size，以控制回填的数据量。

    推荐值：

    - 在 Fast DDL mode 下面，如需让 `ADD INDEX` 尽量不影响其他业务，可以将 `tidb_ddl_reorg_worker_cnt` 和 `tidb_ddl_reorg_batch_size` 适当调小，例如将两个变量值分别调为 `4` 和 `256`。
    - 在无其他负载情况下，如需让 `ADD INDEX` 尽快完成，可以将 `tidb_ddl_reorg_worker_cnt` 和 `tidb_ddl_reorg_batch_size` 的值适当调大，例如将两个变量值分别调为 `20` 和 `2048`。
    - 在有其他负载情况下，如需让 `ADD INDEX` 尽量不影响其他业务，可以将 `tidb_ddl_reorg_worker_cnt` 和 `tidb_ddl_reorg_batch_size` 适当调小，例如将两个变量值分别调为 `4` 和 `256`。
> **建议：**
>
> - 以上两个变量均可以在 DDL 任务执行过程中动态调整，并且在下一个事务批次中生效。
> - 在 Fast DDL 模式下面建议 `tidb_ddl_reorg_worker_cnt` 和 `tidb_ddl_reorg_batch_size` 值不超过 `16` 和 `1024`。
> - 根据 DDL 操作的类型，并结合业务负载压力，选择合适的时间点执行，例如建议在业务负载比较低的情况运行 `ADD INDEX` 操作。
> - 由于添加索引的时间跨度较长，发送相关的指令后，TiDB 会在后台执行任务，TiDB server 宕机不会影响继续执行。

### 并发发送 DDL 请求实现快速建大量表

一个建表的操作耗时大约 50 毫秒。受框架的限制，建表耗时可能更长。

为了更快地建表，推荐通过并发发送多个 DDL 请求以达到最快建表速度。如果串行地发送 DDL 请求，并且没有发给 Owner 节点，则建表速度会很慢。

### 在一条 `ALTER` 语句中进行多次变更

自 v6.2.0 起，TiDB 支持在一条 `ALTER` 语句中修改一张表的多个模式对象（如列、索引），同时保证整个语句的原子性。因此推荐在一条 `ALTER` 语句中进行多次变更。

### 检查读写性能

在添加索引时，回填数据阶段会对集群造成一定的读写压力。在 `ADD INDEX` 的命令发送成功后，并且在 `write reorg` 阶段，建议检查 Grafana 面板上 TiDB 和 TiKV 读写相关的性能指标，以及业务响应时间，来确定 `ADD INDEX` 操作对集群是否造成影响。

## DDL 相关的命令介绍

- `ADMIN SHOW DDL`：用于查看 TiDB DDL 的状态，包括当前 schema 版本号、DDL Owner 的 DDL ID 和地址、正在执行的 DDL 任务和 SQL、当前 TiDB 实例的 DDL ID。详情参阅 [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md#admin-show-ddl)。

- `ADMIN SHOW DDL JOBS`：查看集群环境中的 DDL 任务运行中详细的状态。详情参阅 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md#admin-show-ddl-jobs)。

- `ADMIN SHOW DDL JOB QUERIES job_id [, job_id]`：用于查看 job_id 对应的 DDL 任务的原始 SQL 语句。详情参阅 [`ADMIN SHOW DDL JOB QUERIES`](/sql-statements/sql-statement-admin-show-ddl.md#admin-show-ddl-job-queries)。

- `ADMIN CANCEL DDL JOBS job_id [, job_id]`：用于取消已经提交但未执行完成的 DDL 任务。取消完成后，执行 DDL 任务的 SQL 语句会返回 `ERROR 8214 (HY000): Cancelled DDL job` 错误。

    取消一个已经执行完成的 DDL 任务会在 `RESULT` 列看到 `DDL Job:90 not found` 的错误，表示该任务已从 DDL 等待队列中被移除。

- `ADMIN PAUSE DDL JOBS job_id [, job_id]`：用于暂停正在执行的 DDL 任务。执行该命令后，执行 DDL 任务的 SQL 语句体现为正在执行，后台任务暂停执行。详情参阅 [`ADMIN PAUSE DDL JOBS`](/sql-statements/sql-statement-admin-pause-ddl.md)。

    只有处于执行中或仍在等待中的 DDL 任务可以暂停，否则会在 `RESULT` 列看到 `Job 3 can't be paused now`。

- `ADMIN RESUME DDL JOBS job_id [, job_id]`：用于恢复已被暂停的 DDL 任务。执行该命令后，执行 DDL 任务的 SQL 语句体现为正在执行，后台任务正常执行。详情参阅 [`ADMIN RESUME DDL JOBS`](/sql-statements/sql-statement-admin-resume-ddl.md)。

    你只能对暂停状态的 DDL 任务进行恢复操作，否则会在 `RESULT` 列看到 `Job 3 can't be resumed`。

## 常见问题

DDL 语句执行相关的常见问题，参考 [SQL FAQ - DDL 执行](/faq/sql-faq.md#ddl-执行)。
