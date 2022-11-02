---
title: DDL 介绍
summary: 讲解 TiDB DDL 的原理、用法和常见问题。
---

# 相关概念及原理解释

TiDB 采用在线异步变更地方式执行 DDL，DDL 语句的执行不会阻塞其他会话中的 DML 语句。简单来说，在线异步变更 DDL 可以实现用户业务执行过程中对于数据库对象定义进行变更。

## DDL 相关背景与术语介绍

通常数据库中的 DDL 语句按照执行模式来划分可以分为：

- **离线 DDL 语句**：离线 DDL 语句，即数据库接收到用户 DDL 需要修改用户元数据结构时，需要对要修改的数据库对象加锁，阻塞用户业务在元数据变更过程中对于用户数据的修改。即用户业务会在 DDL 语句执行过程中发生阻塞。

- **在线 DDL 语句**：在线 DDL 语句，即数据库在进行 DDL 语句执行的时候，通过一定的方法，使得 DDL 执行不会阻塞用户业务，且能够保证用户业务在 DDL 执行期间的提交，在 DDL 执行过程中对应对象的数据正确性与一致性都能够得到保证。

如果按照 DDL 语句的执行是否需要操作 DDL 目标对象所包括的数据来划分，DDL 语句可以划分为：

- **逻辑 DDL**：逻辑 DDL 语句，通常只需要完成数据库对象元数据的修改，不需要对于变更对象存储的数据进行处理的语句，例如：table rename，column rename 等等；
  在 TiDB 中，逻辑 DDL 又被称为 General DDL。General DDL 的执行时间都很快，只需要几十毫秒或者几秒。执行这类 DDL 几乎不消耗系统的资源，因此不会影响业务负载。

- **物理 DDL**：物理 DDL 语句则是不但需要修改变更对象的元数据，同时也需要修改变更对象所存储的用户数据，例如，为一张表创建一个索引，不仅需要变更表的定义，同时也需要做一次全表扫描构建新增加的索引。
在 TiDB 中，物理 DDL 被称作 Reorg(Reorganization) DDL。目前只有 ADD INDEX 以及有损的列类型变更（例如从 INT 转成 CHAR 类型）这两种 DDL。Reorg DDL 的特点是执行时间较长，与表的数据量、机器配置以及业务负载有关系。
这类 DDL 执行时会影响到业务负载，具体有两个方面。一方面需要从 TiKV 中读取数据并写入新数据，因此会消耗 TiKV 的 CPU 及 IO 资源。另一方面，Owner 节点的 TiDB 需要进行相应的计算，因此会消耗更多的 CPU 资源。由于目前 TiDB 还不支持分布式执行 DDL，因此其他 TiDB 节点不会占用更多的系统资源。

> **注意：**
> 
> 通常我们所说的 DDL 对于用户业务的影响都是由于 Reorg DDL 语句任务的执行造成的。因此优化 DDL 语句对于用户业务的影响也主要集中在对于 Reorg DDL 任务执行期间的设计，降低它对于用户业务的影响；

## TiDB DDL 模块相关概念介绍

**DDL Owner**（简称 owner）：TiDB DDL 模块引入 Owner 的角色来代理执行所有进入到 TiDB 集群当中的 DDL 语句。在当前 TiDB DDL 模块的实现中，整个 TiDB 集群中只有一个节点能当选为 Owner，每个 TiDB 节点都可能当选这个角色（可以通过配置 `run-ddl` 控制某个 TiDB 节点是否竞选 owner）。当选 Owner 后的节点中启动的 worker 才能处理集群中 DDL 任务。

Owner 宿主节点的产生是用 Etcd 的选举功能从多个 TiDB 节点选举出一个节点来担任。Owner 是有任期的，owner 会主动维护自己的任期，即续约。当 owner 节点宕机后，其他节点可以通过 Etcd 感知到并重新选举出新的 owner，在集群中继续担任 DDL 任务执行者的角色。

![owner](/media/owner.png)

上图给出了一个简单的示意图。

用户如何确定 Owner：
可以通过 ADMIN SHOW DDL 语句查看当前 DDL owner：

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

## TiDB Online DDL 变更详解

### Online DDL 异步变更的原理

TiDB 是一种分布式数据库系统，同时 TiDB 用户对于 TiDB 提供在线 DDL 变更能力，有着比较高的诉求，因此 TiDB DDL 模块从设计之初就选择了在线异步变更的模式，能够为 TiDB 的用户提供不停机变更业务的服务能力。

在线异步变更的原理是将原来 DDL 变更的两个状态之间的切换(变更前 -> 变更后)的方式。变为引入多个相互之间兼容的小版本状态，同时允许整个集群当中，同一个 DDL在执行过程中，允许 不同 TiDB 节点变更对象小版本可以不同（集群中各 TiDB 节点变更对象的小版本差距不超过两个版本），因为相邻两个小版本之间是可以相互兼容的，通过这样多个小版本演进的方式确保多个 TiDB 服务器能够正确同步元数据并保证期间执行用户事务更改数据的正确性与一致性。

以 ADD INDEX 为例，整个变更状态如下：

`absent` -> `delete only` -> `write only` -> `write reorg` -> `public`

对于用户来说，新建的索引在 absent 到 write Reorg 状态该索引都不可用，直到进入 public 阶段。

### Online DDL 异步变更流程（TiDB v6.2 之前）

本章节介绍 TiDB SQL 层中处理异步 Schema 变更的流程。 下面将介绍每个模块以及基本的变更流程。

1. MySQL Client 发送给 TiDB server 一个 DDL 操作请求。
2. 某个 TiDB server 收到请求（MySQL Protocol 层收到请求进行解析优化），然后到达 TiDB SQL 层进行执行。这步骤主要是在 TiDB SQL 层接到请求后，会起个 start job 的模块根据请求将其封装成特定的 DDL job，然后将此 job 按语句类型分类，分别存储到 KV 层的对应 DDL job 队列，并通知自身对应 worker 有 job 需要处理。
3. 接收到处理 job 通知的 worker，会判断自身是否处于 owner 的角色，如果是 owner 角色则直接处理此 job，如果没有处于此角色则退出不做任何处理。假设此 TiDB Server 不是此角色，那么其他的某个节点中肯定有一个是 owner。那个处于 owner 角色节点的 worker 通过定期检测机制来检查是否有 job 可以被执行。如果发现有 job ，那么 worker 就会处理。
4. 当 worker 处理完 job 后， 它会将此 job 从 KV 层对应的 job queue 中移除，并放入 job history queue。之前封装 job 的 start job 模块会定期去 job history queue 查看是否有之前放进去的 job 对应 ID 的 job，如果有则整个 DDL 操作结束。
5. TiDB Server 将 response 返回 MySQL Client。

![ddl-framework](/media/ddl-framework.png)

旧框架的限制：
在旧的框架中，只有 general job queue 和 add index job queue 两个队列，分别处理 general DDL 和 reorg DDL。另一方面，Owner 对这些 DDL job 的处理总是以先入先出的方式。这些限制可能会导致一些“非预期”的 DDL 阻塞行为。具体可以参考常见问题 7.6。

## 并发 DDL 新框架(TiDB 6.2 发布）

在 TiDB 6.2 之前，owner 每次只能执行一个同种类型（general 或 reorg）的 DDL 任务，这个约束对于 DDL 任务执行来讲比较严格，同时对于用户的使用体验也不好。标准数据库 DDL 任务之间如果没有相关依赖，其实是可以并行执行的，例如： 用户 A 对 T1 表 增加一个索引，同时用户 B 对于 T2 表 删除一个列。这两条 DDL 语句即可并行执行。

为了提升用户体验，为用户提供更为强大的 DDL 执行能力，我们在 TiDB v6.2 版本对原有的 owner 进行升级，使得 owner 能够对于 DDL 任务进行相关性判断，原则如下：

1. 数据库的对象是按照下图形成一个分层结构，一个 Schema（DB）包含多张 table，view， function 和 stored procedure。一个 table 又包含多个 index，列。
2. 同一层不同对象之间可以并行进行 DDL 变更。
3. 不同层的对象之间执行 DDL 任务需要阻塞，例如：A 用户正在删除数据库 DB1， B 用户则不能对于数据库 DB1 创建一张新表 T1；

**特别的，我们改善了 DDL Job 队列先入先出的问题，不再是选择当前队列最前面的 DDL Job，而是选择当前可以执行的 DDL Job。并且我们还扩充了处理 Reorg DDL 的 worker 数量，使得能够并行地添加多个索引。**

同时我们避免使用传统的 MDL 锁机制来进行调度，因为 TiDB 中所有支持的 DDL 任务都是以 Online 方式来实现的，我们只需要通过 owner 对于进来的 DDL job 进行相关性判断，并根据相关性结果进行 DDL 任务的调度。最后实现和 传统数据库 DDL 并发相同的效果，同时，也是一种对于 分布式数据库友好的调度算法。

在实现新并发 DDL 框架之后，TiDB 对于数据库 DDL 语句的执行能力得到了加强，更加符合数据库用户使用商用数据库的习惯。

# 最佳实践

# 执行 Reorg DDL （加索引/列类型变更）时，调整合适参数以平衡 DDL 执行速度与对业务负载的影响

- tidb_ddl_reorg_worker_cnt 该参数用来设置 DDL reorg worker 的数量，控制回填的并发度。
- 作用域: GLOBAL，默认值 4（3.0.3 版本起）。
- tidb_ddl_reorg_batch_size 控制回填的数据量。这个变量用来设置 DDL 操作 re-organize 阶段的 batch size。比如 ADD INDEX 操作，需要回填索引数据，通过并发 tidb_ddl_reorg_worker_cnt 个 worker 一起回填数据，每个 worker 以 batch 为单位进行回填。如果 ADD INDEX 时有较多 Update 操作或者 Replace 等更新操作，batch size 越大，事务冲突的概率也会越大，此时建议调小 batch size 的值，最小值是 32。在没有事务冲突的情况下，batch size 可设为较大值，最大值是 10240，这样回填数据的速度更快，但是 TiKV 的写入压力也会变大。
- 作用域: GLOBAL，默认值 256（3.0.3 版本起）。
  推荐值：
  通过我们实际测试经验，通常：
- 在无其他负载情况下，想让 ADD INDEX 尽快完成，可以将 tidb_ddl_reorg_worker_cnt 和 tidb_ddl_reorg_batch_size 适当调大，比如 20，2048。 
- 在有其他负载情况下，想让 ADD INDEX 尽量不影响其他业务，可以将 tidb_ddl_reorg_worker_cnt 和 tidb_ddl_reorg_batch_size 适当调小，比如 4, 256。

> **Note:**
>
> 2 个参数均可以在 DDL 任务执行过程中动态调整，并且在下一个 batch 生效。
> 注意事项：
> 
> - 请根据 DDL 操作的类型，并结合业务负载压力，选择合适的时间点执行，如 ADD INDEX 操作建议在业务负载比较低的情况运行。
> - 由于添加索引时间跨度较长，发送相关的指令后，会在后台执行，TiDB Server 挂掉不会影响继续执行。

## 并发发送 DDL 请求实现快速建大量表

一个建表的操作大概耗时 50ms左右。受框架的限制，其耗时可能更长。为了更快地建表，推荐通过并非发送多个 DDL 请求以达到最快速度。如果是串行地发送请求，并且没有发给 Owner 节点，则建表速度会很慢。

## 在一条 ALTER 语句中进行多次变更

TiDB 在 v6.2.0 版本后支持在一条 ALTER 语句中修改一个表的多个模式对象（如列、索引），同时保证整个语句的原子性。推荐在一条 ALTER 语句中进行多次变更，后续版本中 TiDB 会进行更多优化，例如建多个索引只需要读取一次表数据。

# DDL 相关的命令介绍

## ADMIN SHOW DDL

用于查看 TiDB DDL 的状态，包括当前 schema 版本号、owner 的 DDL ID 和地址、正在执行的 DDL 任务和 SQL、当前 TiDB 实例的 DDL ID。

## ADMIN SHOW DDL JOBS [n]

查看集群环境中的 DDL 任务运行中详细的状态。

- JOB_ID：每个 DDL 操作对应一个 DDL 任务，JOB_ID 全局唯一。
- DB_NAME：执行 DDL 操作的数据库的名称。
- TABLE_NAME：执行 DDL 操作的表的名称。
- JOB_TYPE：DDL 操作的类型。
- SCHEMA_STATE：DDL 操作的 schema 对象的当前状态。如果 JOB_TYPE 是 ADD INDEX，则为索引的状态；如果是 add column，则为列的状态，如果是 create table，则为表的状态。常见的状态有以下几种：
    - none：表示不存在。一般 drop 操作或者 create 操作失败回滚后，会变为 none 状态。
    - delete only、write only、delete reorganization、write reorganization：这四种状态是中间状态，具体含义请参考 “TiDB Online DDL 变更详解” 一节，在此不再赘述。由于中间状态转换很快，一般操作中看不到这几种状态，只有执行 ADD INDEX 操作时能看到处于 write reorganization 状态，表示正在添加索引数据。
    - public：表示存在且对用户可用。一般 create table 和 ADD INDEX/column 等操作完成后，会变为 public 状态，表示新建的 table/column/index 可以正常读写了。
- SCHEMA_ID：执行 DDL 操作的数据库的 ID。
- TABLE_ID：执行 DDL 操作的表的 ID。
- ROW_COUNT：执行 ADD INDEX 操作时，当前已经添加完成的数据行数。
- START_TIME：DDL 操作的开始时间。
- STATE：DDL 操作的状态。常见的状态有以下几种：
    - queueing：表示该操作任务已经进入 DDL 任务队列中，但尚未执行，因为还在排队等待前面的 DDL 任务完成。另一种原因可能是执行 drop 操作后，会变为 none 状态，但是很快会更新为 synced 状态，表示所有 TiDB 实例都已经同步到该状态。
    - running：表示该操作正在执行。
    - synced：表示该操作已经执行成功，且所有 TiDB 实例都已经同步该状态。
    - rollback done：表示该操作执行失败，回滚完成。
    - rollingback：表示该操作执行失败，正在回滚。
    - cancelling：表示正在取消该操作。这个状态只有在用 ADMIN CANCEL DDL JOBS 命令取消 DDL 任务时才会出现。

## ADMIN SHOW DDL JOB QUERIES job_id [, job_id]

用于查看 job_id 对应的 DDL 任务的原始 SQL 语句。

## ADMIN CANCEL DDL JOBS job_id, [, job_id]

用于取消已经提交，但未执行完成的 DDL 任务。取消完成后，执行 DDL 任务的 SQL 语句会返回 ERROR 8214 (HY000): Cancelled DDL job 的错误。

取消一个已经执行完成的 DDL 任务会在 RESULT 列看到 DDL Job:90 not found 的错误，表示该任务已从 DDL 等待队列中被移除。

## 检查读写性能

在添加索引时，回填数据阶段会对集群造成一定的读写压力，ADD INDEX 的命令发送成功后，并且在 write reorg 阶段，建议检查 Grafana 中 TiDB 和 TiKV 读写相关的性能指标，以及业务响应时间，来确定 ADD INDEX 操作对集群是否造成影响。

# 常见问题

## 各类 DDL 操作预估耗时

在 DDL 操作没有阻塞，各个 TiDB Server 能够正常更新 Schema 版本的情况下，以及 DDL Owner 节点正常运行的情况下，各类 DDL 操作的预估耗时如下：

| 操作类型                                                                                                                                                                    | 预估耗时                   |
|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------|
| Reorg DDL、add index/modify column(with reorg data)                                                                                                                      | 取决于数据量、系统负载、 DDL 参数的设置 |
| General DDL（除了 reorg DDL 的其它 DDL），比如：create database / table、drop database / table、truncate table、alter table add / drop / modify column(without reorg data)、drop index | 1秒左右                   |

> **Note:**
>
> 以上为各类操作的预估耗时，请以实际操作耗时为准。

## 执行 DDL 会慢的可能原因

- 在一个链接上，DDL 语句之前有非 autocommit 的 DML 语句，且此 DML 语句提交操作比较慢会导致出现 DDL 语句执行慢的现象。原因是执行 DDL 语句前，会将之前没有提交的 DML 先提交。
- 多个 DDL 语句一起执行的时候，后面的几个 DDL 语句可能会比较慢，因为可能需要排队等待。排队场景包括：
    - 同一类型 DDL 语句需要排队（比如 create table 和 create database 都是 general DDL，两个操作同时执行时，需要排队）。在 v6.2 后，支持并行 DDL 语句，但也有并发度问题，会有一定的排队情况。
    - 同一个表的 DDL 存在依赖关系，后面的 DDL 需要等待前面的 DDL 完成。
- 在正常集群启动后，第一个 DDL 操作的执行时间可能会比较久，可能是 DDL 在做 owner 的选举。
- 由于停 TiDB 时不能与 PD 正常通信（包括停电情况）或者用 kill -9 指令停 TiDB 导致 TiDB 没有及时从 PD 清理注册数据。
- 当集群中某个 TiDB 与 PD 或者 TiKV 之间发生通信问题，即 TiDB 不能及时获取最新版本信息。

### 触发 Information schema is changed 错误的原因

TiDB 在执行 SQL 语句时，会使用当时的 schema 来处理该 SQL 语句，而且 TiDB 支持在线异步变更 DDL。那么，在执行 DML 的时候可能有 DDL 语句也在执行，而你需要确保每个 SQL 语句在同一个 schema 上执行。所以当执行 DML 时，遇到正在执行中的 DDL 操作就可能会报 Information schema is changed 的错误。为了避免太多的 DML 语句报错，已做了一些优化。
现在会报此错的可能原因如下（后两个报错原因与表无关）：

- 执行的 DML 语句中涉及的表和集群中正在执行的 DDL 的表有相同的，那么这个 DML 语句就会报此错。
- 这个 DML 执行时间很久，而这段时间内执行了很多 DDL 语句，导致中间 schema 版本变更次数超过 1024（v3.0.5 版本之前此值为定值 100。v3.0.5 及之后版本默认值为 1024，可以通过 tidb_max_delta_schema_count 变量修改）。
- 接受 DML 请求的 TiDB 长时间不能加载到 schema information（TiDB 与 PD 或 TiKV 之间的网络连接故障等会导致此问题），而这段时间内执行了很多 DDL 语句，导致中间 schema 版本变更次数超过 100。

> **Note:**
>
> - 目前 TiDB 未缓存所有的 schema 版本信息。
> - - 对于每个 DDL 操作，schema 版本变更的数量与对应 schema state 变更的次数一致。
> - - 不同的 DDL 操作版本变更次数不一样。例如，create table 操作会有 1 次 schema 版本变更；add column 操作有 4 次 schema 版本变更。

### 触发 Information schema is out of date 错误的原因

当执行 DML 时，TiDB 超过一个 DDL lease 时间（默认 45s）没能加载到最新的 schema 就可能会报 Information schema is out of date 的错误。遇到此错的可能原因如下：

- 执行此 DML 的 TiDB 被 kill 后准备退出，且此 DML 对应的事务执行时间超过一个 DDL lease，在事务提交时会报这个错误。
- TiDB 在执行此 DML 时，有一段时间内连不上 PD 或者 TiKV，导致 TiDB 超过一个 DDL lease 时间没有 load schema，或者 TiDB 断开了与 PD 之间带 keep alive 设置的连接。

### 高并发情况下执行 DDL 时报错的原因

高并发情况下执行 DDL（比如批量建表）时，极少部分 DDL 可能会由于并发执行时 key 冲突而执行失败。
并发执行 DDL 时，建议将 DDL 数量保持在 20 以下，否则你需要在应用端重试失败的 DDL 语句。

### DDL 执行被阻塞的原因

在 6.2 版本之前，DDL 按照类型分配到两个先入先出的队列中，即 reorg DDL 进入 reorg 队列中，general DDL 进入 general 队列中。由于先入先出以及同一张表上的 DDL 需要串行执行这一原则，多个DDL 在执行过程中可能会出现阻塞的问题。

例如以下情况：

DDL1: CREATE INDEX idx on t(a int);

DDL2: ALTER TABLE t ADD COLUMN b int;

DDL3:CREATE TABLE t1(a int);

由于队列先入先出的限制，DDL3 需要等待 DDL2 执行。同时又因为同一张表上的 DDL 需要串行执行，DDL2 需要等待 DDL1 执行。因此，DDL3 需要等待 DDL1 先执行完，即使它们操作在不同的表上。

6.2 版本及之后的版本中，TiDB DDL 处理采用了新的框架。在新的框架中，不再有同一个队列先进先出的问题，而是从所有的 DDL 任务中选出可以执行的 DDL 来执行。并且 reorg worker 的数量进行了扩充，大概为节点 CPU / 4，这使得新框架中可以同时为多张表同时进行建索引。

不管是新的集群还是升级来的集群，在 6.2 版本中都会自动使用新框架，用户无需进行调整。

### 定位 DDL 卡住问题

1. 可以先排除正常会慢的可能原因。
2. 找出 DDL owner 节点，具体方法有如下两种：
3. 通过 `curl http://{TiDBIP}:10080/info/all` 获取当前集群的 owner；
4. 通过监控 DDL - DDL META OPM 查看某个时间段的 owner
5. 如果 owner 不存在，尝试手动触发 owner 选举。`curl -X POST http://{TiDBIP}:10080/ddl/owner/resign`
6. 如果 owner 存在，导出 goroutine 堆栈并检查可能卡住的地方。
