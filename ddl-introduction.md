---
title: DDL 语句的执行原理和最佳实践
summary: 了解 TiDB 中 DDL 语句的实现原理、在线变更过程和最佳实践。
---

# DDL 语句的执行原理和最佳实践

本文介绍了 TiDB 中与 DDL 语句相关的执行原理和最佳实践。这些原理包括 DDL Owner 模块和在线 DDL 变更过程。

## DDL 执行原理

TiDB 使用在线和异步的方式来执行 DDL 语句。这意味着在执行 DDL 语句时，不会阻塞其他会话中的 DML 语句。换句话说，你可以在应用程序运行时使用在线和异步的 DDL 语句来更改数据库对象的定义。

### DDL 语句类型

根据 DDL 语句在执行过程中是否阻塞用户应用，DDL 语句可以分为以下类型：

- **离线 DDL 语句**：当数据库收到用户的 DDL 语句时，首先锁定要修改的数据库对象，然后更改元数据。在 DDL 执行期间，数据库会阻止用户应用修改数据。

- **在线 DDL 语句**：当在数据库中执行 DDL 语句时，使用特定方法确保语句不会阻塞用户应用。这允许用户在 DDL 执行期间提交修改。该方法还确保在执行过程中相应数据库对象的正确性和一致性。

根据是否操作目标 DDL 对象中包含的数据，DDL 语句可以分为以下类型：

- **逻辑 DDL 语句**：逻辑 DDL 语句通常只修改数据库对象的元数据，而不处理存储在对象中的数据，例如更改表名或更改列名。

    在 TiDB 中，逻辑 DDL 语句也称为"一般 DDL"。这些语句通常执行时间较短，通常只需要几十毫秒或几秒钟就能完成。因此，它们不会消耗太多系统资源，也不会影响应用程序的工作负载。

- **物理 DDL 语句**：物理 DDL 语句不仅修改要更改对象的元数据，还修改存储在对象中的用户数据。例如，当 TiDB 为表创建索引时，它不仅更改表的定义，还执行全表扫描以构建新添加的索引。

    在 TiDB 中，物理 DDL 语句也称为"reorg DDL"，即重组。目前，物理 DDL 语句仅包括 `ADD INDEX` 和有损列类型更改（例如从 `INT` 类型更改为 `CHAR` 类型）。这些语句执行时间较长，执行时间受表中数据量、机器配置和应用程序工作负载的影响。

    执行物理 DDL 语句可能会影响应用程序的工作负载，原因有两个。一方面，它消耗 TiKV 的 CPU 和 I/O 资源来读取数据和写入新数据。另一方面，**作为 DDL Owner 的 TiDB 节点**或**那些被 TiDB 分布式执行框架（DXF）调度执行 `ADD INDEX` 任务的 TiDB 节点**消耗 TiDB 的 CPU 资源来执行相应的计算。

    > **注意：**
    >
    > 物理 DDL 任务的执行通常会对用户应用造成最大影响。因此，为了最小化这种影响，关键点是在执行期间优化物理 DDL 语句的设计。这有助于减少对用户应用的影响。

### TiDB DDL 模块

TiDB DDL 模块引入了 DDL Owner（或 Owner）的角色，它作为在 TiDB 集群内执行所有 DDL 语句的代理。在当前实现中，整个集群中任何时候只能有一个 TiDB 节点被选举为 Owner。一旦一个 TiDB 节点被选举为 Owner，该 TiDB 节点中启动的 worker 就可以处理集群中的 DDL 任务。

TiDB 使用 etcd 的选举机制从多个 TiDB 节点中选举一个节点来承载 Owner。默认情况下，每个 TiDB 节点都可能被选举为 Owner（你可以配置 `run-ddl` 来管理节点参与选举）。被选举的 Owner 节点有一个任期，它通过续期来主动维护任期。当 Owner 节点宕机时，另一个节点可以通过 etcd 被选举为新的 Owner，并继续执行集群中的 DDL 任务。

DDL Owner 的简单示意图如下：

![DDL Owner](/media/ddl-owner.png)

你可以使用 `ADMIN SHOW DDL` 语句查看当前的 DDL owner：

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

### TiDB 中在线 DDL 异步变更的工作原理

从设计之初，TiDB DDL 模块就选择了在线异步变更模式，这让你可以在不停机的情况下修改应用程序。

DDL 变更涉及从一个状态转换到另一个状态，通常是从"变更前"状态转换到"变更后"状态。通过在线 DDL 变更，这种转换是通过引入多个相互兼容的小版本状态来实现的。在执行 DDL 语句期间，同一集群中的 TiDB 节点允许有不同的小版本变更，只要变更对象的小版本之间的差异不超过两个版本即可。这是可能的，因为相邻的小版本可以相互兼容。

通过这种方式，通过多个小版本的演进确保元数据可以在多个 TiDB 节点之间正确同步。这有助于在过程中维护涉及变更数据的用户事务的正确性和一致性。

以 `ADD INDEX` 为例，整个状态变更过程如下：

```
absent -> delete only -> write only -> write reorg -> public
```

对于用户来说，新创建的索引在 `public` 状态之前是不可用的。

<SimpleTab>
<div label="从 v6.2.0 开始的并行 DDL 框架">

在 TiDB v6.2.0 之前，由于 Owner 一次只能执行一个相同类型（逻辑或物理）的 DDL 任务，这种限制相对严格，影响了用户体验。

如果 DDL 任务之间没有依赖关系，并行执行不会影响数据的正确性和一致性。例如，用户 A 为 `T1` 表添加索引，而用户 B 从 `T2` 表删除列。这两个 DDL 语句可以并行执行。

为了改善 DDL 执行的用户体验，从 v6.2.0 开始，TiDB 使 Owner 能够确定 DDL 任务的相关性。逻辑如下：

+ 对同一个表执行的 DDL 语句相互阻塞。
+ `DROP DATABASE` 和影响数据库中所有对象的 DDL 语句相互阻塞。
+ 在不同表上添加索引和列类型更改可以并发执行。
+ 逻辑 DDL 语句必须等待前一个逻辑 DDL 语句执行完成后才能执行。
+ 在其他情况下，DDL 可以根据并发 DDL 执行的可用性级别执行。

具体来说，TiDB 6.2.0 在以下方面增强了 DDL 执行框架：

+ DDL Owner 可以根据上述逻辑并行执行 DDL 任务。
+ 解决了 DDL Job 队列中先进先出的问题。DDL Owner 不再选择队列中的第一个任务，而是选择当前时间可以执行的任务。
+ 增加了处理物理 DDL 语句的 worker 数量，使多个物理 DDL 语句能够并行执行。

    因为 TiDB 中的所有 DDL 任务都是使用在线变更方式实现的，TiDB 可以通过 Owner 确定新 DDL 任务的相关性，并基于这些信息调度 DDL 任务。这种方法使分布式数据库能够实现与传统数据库相同级别的 DDL 并发性。

并发 DDL 框架增强了 TiDB 中 DDL 语句的执行能力，使其更加符合商业数据库的使用模式。

</div>
<div label="TiDB v6.2.0 之前的在线 DDL 异步变更">

在 v6.2.0 之前，TiDB SQL 层处理异步 schema 变更的过程如下：

1. MySQL Client 向 TiDB 服务器发送 DDL 请求。

2. TiDB 服务器在 MySQL 协议层接收到请求后，对请求进行解析和优化，然后将其发送到 TiDB SQL 层执行。

    一旦 TiDB 的 SQL 层收到 DDL 请求，它就启动 `start job` 模块将请求封装成特定的 DDL job（即 DDL 任务），然后根据语句类型将这个 job 存储在 KV 层相应的 DDL job 队列中。通知相应的 worker 有需要处理的 job。

3. 当收到处理 job 的通知时，worker 确定它是否具有 DDL Owner 角色。如果是，它直接处理 job。否则，它退出而不进行任何处理。

    如果一个 TiDB 服务器不是 Owner 角色，那么另一个节点一定是 Owner。Owner 角色节点的 worker 会定期检查是否有可以执行的可用 job。如果发现这样的 job，worker 将处理它。

4. worker 处理完 Job 后，将 job 从 KV 层的 job 队列中移除，并将其放入 `job history queue`。封装 job 的 `start job` 模块会定期检查 `job history queue` 中 job 的 ID，看它是否已被处理。如果已处理，则 job 对应的整个 DDL 操作结束。

5. TiDB 服务器将 DDL 处理结果返回给 MySQL Client。

在 TiDB v6.2.0 之前，DDL 执行框架有以下限制：

- TiKV 集群只有两个队列：`general job queue` 和 `add index job queue`，分别处理逻辑 DDL 和物理 DDL。
- DDL Owner 总是按照先进先出的方式处理 DDL job。
- DDL Owner 一次只能执行一个相同类型（逻辑或物理）的 DDL 任务，这种限制相对严格，影响了用户体验。

这些限制可能会导致一些"意外"的 DDL 阻塞行为。更多详情，请参见 [SQL FAQ - DDL 执行](https://docs.pingcap.com/tidb/stable/sql-faq#ddl-execution)。

</div>
</SimpleTab>

## 最佳实践

### 通过系统变量平衡物理 DDL 执行速度和对应用负载的影响

在执行物理 DDL 语句（包括添加索引或列类型更改）时，你可以调整以下系统变量的值来平衡 DDL 执行速度和对应用负载的影响：

- [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)：此变量设置 DDL 操作的 reorg worker 数量，控制回填的并发度。

- [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)：此变量设置 DDL 操作在 `re-organize` 阶段的批处理大小，控制要回填的数据量。

    推荐值：

    - 如果没有其他负载，你可以增加 `tidb_ddl_reorg_worker_cnt` 和 `tidb_ddl_reorg_batch_size` 的值来加快 `ADD INDEX` 操作。例如，你可以将这两个变量的值分别设置为 `20` 和 `2048`。
    - 如果有其他负载，你可以减小 `tidb_ddl_reorg_worker_cnt` 和 `tidb_ddl_reorg_batch_size` 的值以最小化对其他应用的影响。例如，你可以将这些变量的值分别设置为 `4` 和 `256`。

> **提示：**
>
> - 上述两个变量可以在 DDL 任务执行期间动态调整，并在下一个事务批次中生效。
> - 根据操作类型和应用负载压力选择适当的时间执行 DDL 操作。例如，建议在应用负载较低时运行 `ADD INDEX` 操作。
> - 由于添加索引的持续时间相对较长，TiDB 会在发送命令后在后台执行任务。如果 TiDB 服务器宕机，执行不会受到影响。

### 通过并发发送 DDL 请求快速创建多个表

创建表操作大约需要 50 毫秒。由于框架限制，实际创建表所需的时间可能会更长。

为了更快地创建表，建议并发发送多个 DDL 请求以实现最快的表创建速度。如果你串行发送 DDL 请求且不发送到 Owner 节点，表创建速度会非常慢。

### 在单个 `ALTER` 语句中进行多个更改

从 v6.2.0 开始，TiDB 支持在单个 `ALTER` 语句中修改表的多个 schema 对象（如列和索引），同时确保整个语句的原子性。因此，建议在单个 `ALTER` 语句中进行多个更改。

### 检查读写性能

当 TiDB 添加索引时，回填数据的阶段会对集群造成读写压力。在发送 `ADD INDEX` 命令并开始 `write reorg` 阶段后，建议在 Grafana 仪表板上检查 TiDB 和 TiKV 的读写性能指标以及应用程序响应时间，以确定 `ADD INDEX` 操作是否影响集群。

## DDL 相关命令

- `ADMIN SHOW DDL`：用于查看 TiDB DDL 操作的状态，包括当前 schema 版本号、DDL Owner 的 DDL ID 和地址、正在执行的 DDL 任务和 SQL，以及当前 TiDB 实例的 DDL ID。详情请参见 [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md#admin-show-ddl)。

- `ADMIN SHOW DDL JOBS`：用于查看集群环境中运行的 DDL 任务的详细状态。详情请参见 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md#admin-show-ddl-jobs)。

- `ADMIN SHOW DDL JOB QUERIES job_id [, job_id]`：用于查看与 `job_id` 对应的 DDL 任务的原始 SQL 语句。详情请参见 [`ADMIN SHOW DDL JOB QUERIES`](/sql-statements/sql-statement-admin-show-ddl.md#admin-show-ddl-job-queries)。

- `ADMIN CANCEL DDL JOBS job_id, [, job_id]`：用于取消已提交但未完成的 DDL 任务。取消完成后，执行 DDL 任务的 SQL 语句会返回 `ERROR 8214 (HY000): Cancelled DDL job` 错误。

    如果取消已完成的 DDL 任务，你可以在 `RESULT` 列中看到 `DDL Job:90 not found` 错误，这意味着该任务已从 DDL 等待队列中移除。

- `ADMIN PAUSE DDL JOBS job_id [, job_id]`：用于暂停正在执行的 DDL 任务。命令执行后，执行 DDL 任务的 SQL 语句显示为正在执行，而后台任务已被暂停。详情请参见 [`ADMIN PAUSE DDL JOBS`](/sql-statements/sql-statement-admin-pause-ddl.md)。

    你只能暂停正在进行或仍在队列中的 DDL 任务。否则，`RESULT` 列中会显示 `Job 3 can't be paused now` 错误。

- `ADMIN RESUME DDL JOBS job_id [, job_id]`：用于恢复已暂停的 DDL 任务。命令执行后，执行 DDL 任务的 SQL 语句显示为正在执行，后台任务恢复执行。详情请参见 [`ADMIN RESUME DDL JOBS`](/sql-statements/sql-statement-admin-resume-ddl.md)。

    你只能恢复已暂停的 DDL 任务。否则，`RESULT` 列中会显示 `Job 3 can't be resumed` 错误。

## 常见问题

关于 DDL 执行的常见问题，请参见 [SQL FAQ - DDL 执行](https://docs.pingcap.com/tidb/stable/sql-faq)。
