---
title: TiDB 中 DDL 执行原理及最佳实践
summary: 讲解 TiDB DDL 的实现原理、在线变更过程、最佳实践等。
---

# TiDB 中 DDL 执行原理及最佳实践

本文介绍了 TiDB 中 DDL 语句的执行原理（包括 DDL owner 模块和在线变更 DDL 的流程）和最佳实践。

## DDL 执行原理

TiDB 采用在线异步变更的方式执行 DDL 语句，这样 DDL 语句的执行不会阻塞其他会话中的 DML 语句。简单来说，在线异步变更 DDL 可以实现用户业务执行过程中对于数据库对象定义进行变更。

### DDL 语句类型简介

通常数据库中的 DDL 语句按照执行模式来划分可以分为：

- **离线 DDL 语句**：离线 DDL 语句，即数据库接收到用户 DDL 需要修改用户元数据结构时，需要对要修改的数据库对象加锁，阻塞用户业务在元数据变更过程中对于用户数据的修改。即用户业务会在 DDL 语句执行过程中发生阻塞。

- **在线 DDL 语句**：在线 DDL 语句，即数据库在进行 DDL 语句执行的时候，通过一定的方法，使得 DDL 执行不会阻塞用户业务，且能够保证用户业务在 DDL 执行期间的提交，在 DDL 执行过程中对应对象的数据正确性与一致性都能够得到保证。

如果按照 DDL 语句的执行是否需要操作 DDL 目标对象所包括的数据来划分，DDL 语句可以划分为：

- **逻辑 DDL**：逻辑 DDL 语句，通常只需要完成数据库对象元数据的修改，不需要对于变更对象存储的数据进行处理的语句，例如：table rename，column rename 等等；
  在 TiDB 中，逻辑 DDL 又被称为 General DDL。General DDL 的执行时间都很快，只需要几十毫秒或者几秒。执行这类 DDL 几乎不消耗系统的资源，因此不会影响业务负载。

- **物理 DDL**：物理 DDL 语句则是不但需要修改变更对象的元数据，同时也需要修改变更对象所存储的用户数据，例如，为一张表创建一个索引，不仅需要变更表的定义，同时也需要做一次全表扫描构建新增加的索引。

    在 TiDB 中，物理 DDL 被称作 Reorg (Reorganization) DDL。目前只有 ADD INDEX 以及有损的列类型变更（例如从 INT 转成 CHAR 类型）这两种 DDL。Reorg DDL 的特点是执行时间较长，与表的数据量、机器配置以及业务负载有关系。

    这类 DDL 执行时会影响到业务负载，具体有两个方面。一方面需要从 TiKV 中读取数据并写入新数据，因此会消耗 TiKV 的 CPU 及 IO 资源。另一方面，Owner 节点的 TiDB 需要进行相应的计算，因此会消耗更多的 CPU 资源。由于目前 TiDB 还不支持分布式执行 DDL，因此其他 TiDB 节点不会占用更多的系统资源。

> **注意：**
>
> 通常 DDL 对于用户业务的影响都是由于 Reorg DDL 语句任务的执行造成的。因此优化 DDL 语句对于用户业务的影响也主要集中在对于 Reorg DDL 任务执行期间的设计，降低它对于用户业务的影响。

### TiDB DDL 模块介绍

**DDL Owner**（简称 Owner）：TiDB DDL 模块引入 Owner 的角色来代理执行所有进入到 TiDB 集群当中的 DDL 语句。在当前 TiDB DDL 模块的实现中，整个 TiDB 集群中只有一个节点能当选为 Owner，每个 TiDB 节点都可能当选这个角色（可以通过配置 `run-ddl` 控制某个 TiDB 节点是否竞选 owner）。当选 Owner 后的节点中启动的 worker 才能处理集群中 DDL 任务。

Owner 宿主节点的产生是用 etcd 的选举功能从多个 TiDB 节点选举出一个节点来担任。Owner 是有任期的，Owner 会主动维护自己的任期，即续约。当 Owner 节点宕机后，其他节点可以通过 etcd 感知到并重新选举出新的 Owner，在集群中继续担任 DDL 任务执行者的角色。

![DDL Owner](/media/ddl-owner.png)

上图给出了一个简单的示意图。

用户可以通过 `ADMIN SHOW DDL` 语句查看当前 DDL owner：

```sql
ADMIN SHOW DDL;
```

```sql
ADMIN SHOW DDL;
+------------+--------------------------------------+---------------+--------------+--------------------------------------+-------+
| SCHEMA_VER | OWNER_ID                             | OWNER_ADDRESS | RUNNING_JOBS | SELF_ID                              | QUERY |
+------------+--------------------------------------+---------------+--------------+--------------------------------------+-------+
|         26 | 2d1982af-fa63-43ad-a3d5-73710683cc63 | 0.0.0.0:4000  |              | 2d1982af-fa63-43ad-a3d5-73710683cc63 |       |
+------------+--------------------------------------+---------------+--------------+--------------------------------------+-------+
1 row in set (0.00 sec)
```

### TiDB 中在线 DDL 异步变更的原理

TiDB 是一种分布式数据库系统，同时 TiDB 用户对于 TiDB 提供在线 DDL 变更能力，有着比较高的诉求，因此 TiDB DDL 模块从设计之初就选择了在线异步变更的模式，能够为 TiDB 的用户提供不停机变更业务的服务能力。

在线异步变更的原理是将原来 DDL 变更的两个状态之间的切换(变更前 -> 变更后)的方式。变为引入多个相互之间兼容的小版本状态，同时允许整个集群当中，同一个 DDL在执行过程中，允许 不同 TiDB 节点变更对象小版本可以不同（集群中各 TiDB 节点变更对象的小版本差距不超过两个版本），因为相邻两个小版本之间是可以相互兼容的，通过这样多个小版本演进的方式确保多个 TiDB 服务器能够正确同步元数据并保证期间执行用户事务更改数据的正确性与一致性。

以 ADD INDEX 为例，整个变更状态如下：

`absent` -> `delete only` -> `write only` -> `write reorg` -> `public`

对于用户来说，新建的索引在 absent 到 write Reorg 状态该索引都不可用，直到进入 public 阶段。

<SimpleTab>
<div label="Online DDL 异步变更流程（TiDB v6.2 之前）">

本节介绍 v6.2 前 TiDB SQL 层中处理异步 Schema 变更的流程。以下为每个模块以及基本的变更流程。

1. MySQL Client 发送给 TiDB server 一个 DDL 操作请求。
2. 某个 TiDB server 收到请求（MySQL Protocol 层收到请求进行解析优化），然后到达 TiDB SQL 层进行执行。这步骤主要是在 TiDB SQL 层接到请求后，会起个 start job 的模块根据请求将其封装成特定的 DDL job，然后将此 job 按语句类型分类，分别存储到 KV 层的对应 DDL job 队列，并通知自身对应 worker 有 job 需要处理。
3. 接收到处理 job 通知的 worker，会判断自身是否处于 owner 的角色，如果是 owner 角色则直接处理此 job，如果没有处于此角色则退出不做任何处理。假设此 TiDB Server 不是此角色，那么其他的某个节点中肯定有一个是 owner。那个处于 owner 角色节点的 worker 通过定期检测机制来检查是否有 job 可以被执行。如果发现有 job ，那么 worker 就会处理。
4. 当 worker 处理完 job 后， 它会将此 job 从 KV 层对应的 job queue 中移除，并放入 job history queue。之前封装 job 的 start job 模块会定期去 job history queue 查看是否有之前放进去的 job 对应 ID 的 job，如果有则整个 DDL 操作结束。
5. TiDB Server 将 response 返回 MySQL Client。

![ddl-framework](/media/ddl-framework.png)

旧框架的限制：
在旧的框架中，只有 general job queue 和 add index job queue 两个队列，分别处理 general DDL 和 reorg DDL。另一方面，Owner 对这些 DDL job 的处理总是以先入先出的方式。这些限制可能会导致一些“非预期”的 DDL 阻塞行为。具体可以参考常见问题 7.6。

</div>
<div label="并发 DDL 框架（TiDB v6.2 及以上）">

在 TiDB 6.2 之前，owner 每次只能执行一个同种类型（general 或 reorg）的 DDL 任务，这个约束对于 DDL 任务执行来讲比较严格，同时对于用户的使用体验也不好。标准数据库 DDL 任务之间如果没有相关依赖，其实是可以并行执行的，例如： 用户 A 对 T1 表 增加一个索引，同时用户 B 对于 T2 表 删除一个列。这两条 DDL 语句即可并行执行。

为了提升用户体验，为用户提供更为强大的 DDL 执行能力，我们在 TiDB v6.2 版本对原有的 owner 进行升级，使得 owner 能够对于 DDL 任务进行相关性判断，原则如下：

1. 数据库的对象是按照下图形成一个分层结构，一个 Schema（DB）包含多张 table，view， function 和 stored procedure。一个 table 又包含多个 index，列。
2. 同一层不同对象之间可以并行进行 DDL 变更。
3. 不同层的对象之间执行 DDL 任务需要阻塞，例如：A 用户正在删除数据库 DB1， B 用户则不能对于数据库 DB1 创建一张新表 T1；

**特别的，我们改善了 DDL Job 队列先入先出的问题，不再是选择当前队列最前面的 DDL Job，而是选择当前可以执行的 DDL Job。并且我们还扩充了处理 Reorg DDL 的 worker 数量，使得能够并行地添加多个索引。**

同时我们避免使用传统的 MDL 锁机制来进行调度，因为 TiDB 中所有支持的 DDL 任务都是以 Online 方式来实现的，我们只需要通过 owner 对于进来的 DDL job 进行相关性判断，并根据相关性结果进行 DDL 任务的调度。最后实现和 传统数据库 DDL 并发相同的效果，同时，也是一种对于 分布式数据库友好的调度算法。

在实现新并发 DDL 框架之后，TiDB 对于数据库 DDL 语句的执行能力得到了加强，更加符合数据库用户使用商用数据库的习惯。

</div>
</SimpleTab>

## 最佳实践

### 通过系统变量来平衡 Reorg DDL 的执行速度与对业务负载的影响

执行 Reorg DDL（包括添加索引或列类型变更）时，适当调整以下系统变量以平衡 DDL 执行速度与对业务负载的影响：

- [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)：用来设置这个变量用来设置 DDL 操作 reorg worker 的数量，控制回填的并发度。

- [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)：这个变量用来设置 DDL 操作 `re-organize` 阶段的 batch size，以控制回填的数据量。

    推荐值：

    - 在无其他负载情况下，想让 `ADD INDEX` 尽快完成，可以将 `tidb_ddl_reorg_worker_cnt` 和 `tidb_ddl_reorg_batch_size` 的值适当调大，例如将两个变量值分别调为 `20` 和 `2048`。
    - 在有其他负载情况下，想让 `ADD INDEX` 尽量不影响其他业务，可以将 `tidb_ddl_reorg_worker_cnt` 和 `tidb_ddl_reorg_batch_size` 适当调小，例如将两个变量值分别调为 `4` 和·`256`。

> **建议：**
>
> - 以上两个变量均可以在 DDL 任务执行过程中动态调整，并且在下一个 batch 生效。
> - 请根据 DDL 操作的类型，并结合业务负载压力，选择合适的时间点执行，例如建议在业务负载比较低的情况运行 `ADD INDEX` 操作。
> - 由于添加索引的时间跨度较长，发送相关的指令后，TiDB 会在后台执行任务，TiDB Server 挂掉不会影响继续执行。

### 并发发送 DDL 请求实现快速建大量表

一个建表的操作大概耗时 50ms左右。受框架的限制，其耗时可能更长。为了更快地建表，推荐通过并非发送多个 DDL 请求以达到最快速度。如果是串行地发送请求，并且没有发给 Owner 节点，则建表速度会很慢。

### 在一条 ALTER 语句中进行多次变更

TiDB 在 v6.2.0 版本后支持在一条 ALTER 语句中修改一个表的多个模式对象（如列、索引），同时保证整个语句的原子性。推荐在一条 ALTER 语句中进行多次变更，后续版本中 TiDB 会进行更多优化，例如建多个索引只需要读取一次表数据。

## DDL 相关的命令介绍

- `ADMIN SHOW DDL`：用于查看 TiDB DDL 的状态，包括当前 schema 版本号、owner 的 DDL ID 和地址、正在执行的 DDL 任务和 SQL、当前 TiDB 实例的 DDL ID。详情参阅 [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md#admin-show-ddl)。

- `ADMIN SHOW DDL JOBS`：查看集群环境中的 DDL 任务运行中详细的状态。详情参阅 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md#admin-show-ddl-jobs)。

- `ADMIN SHOW DDL JOB QUERIES job_id [, job_id]`：用于查看 job_id 对应的 DDL 任务的原始 SQL 语句。详情参阅 [`ADMIN SHOW DDL JOB QUERIES`](/sql-statements/sql-statement-admin-show-ddl.md#admin-show-ddl-job-queries)。

- `ADMIN CANCEL DDL JOBS job_id, [, job_id]`：用于取消已经提交，但未执行完成的 DDL 任务。取消完成后，执行 DDL 任务的 SQL 语句会返回 ERROR 8214 (HY000): Cancelled DDL job 的错误。

    取消一个已经执行完成的 DDL 任务会在 RESULT 列看到 DDL Job:90 not found 的错误，表示该任务已从 DDL 等待队列中被移除。

## 检查读写性能

在添加索引时，回填数据阶段会对集群造成一定的读写压力，ADD INDEX 的命令发送成功后，并且在 write reorg 阶段，建议检查 Grafana 中 TiDB 和 TiKV 读写相关的性能指标，以及业务响应时间，来确定 ADD INDEX 操作对集群是否造成影响。

## 常见问题

DDL 语句执行相关的常见问题，参考 [SQL FAQ - DDL 执行](/faq/sql-faq.md#ddl-执行)。å
