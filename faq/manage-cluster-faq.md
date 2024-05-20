---
title: TiDB 集群管理常见问题
summary: 介绍 TiDB 集群管理的常见问题、原因及解决方法。
---

# TiDB 集群管理常见问题

本文介绍管理 TiDB 集群时的常见问题、原因及解决方法。

## 集群日常管理

本小节介绍集群日程管理中的常见问题、原因及解决方法。

### TiDB 如何登录？

和 MySQL 登录方式一样，可以按照下面例子进行登录。

{{< copyable "shell-regular" >}}

```shell
mysql -h 127.0.0.1 -uroot -P4000
```

### TiDB 如何修改数据库系统变量？

和 MySQL 一样，TiDB 也分为静态参数和固态参数，静态参数可以直接通过 `SET GLOBAL xxx = n` 的方式进行修改，不过新参数值只限于该实例生命周期有效。

### TiDB (TiKV) 有哪些数据目录？

默认在 [`--data-dir`](/command-line-flags-for-tikv-configuration.md#--data-dir) 目录下，其中包括 backup、db、raft、snap 四个目录，分别存储备份、数据、raft 数据及镜像数据。

### TiDB 有哪些系统表？

和 MySQL 类似，TiDB 中也有系统表，用于存放数据库运行时所需信息，具体信息参考 [TiDB 系统表](/mysql-schema.md)文档。

### TiDB 各节点服务器下是否有日志文件，如何管理？

默认情况下各节点服务器会在日志中输出标准错误，如果启动的时候通过 `--log-file` 参数指定了日志文件，那么日志会输出到指定的文件中，并且按天做 rotation。

### TiDB、TiKV、PD 节点的各类文件存放在哪里？

如需快速了解 TiDB 节点、TiKV 节点、PD 节点的配置文件、数据文件及日志文件的相关介绍与其存放位置，建议观看下面的培训视频（时长 9 分钟）。

<video src="https://download.pingcap.com/docs-cn/Lesson12_log.mp4" width="100%" height="100%" controls="controls" poster="https://download.pingcap.com/docs-cn/poster_lesson12.png"></video>

### 如何规范停止 TiDB？

- 若使用了 load balancer（推荐）：先停止 load balancer，然后执行 `SHUTDOWN` 语句。此时 TiDB 会根据 [`graceful-wait-before-shutdown`](/tidb-configuration-file.md#graceful-wait-before-shutdown-从-v50-版本开始引入) 设置值等待所有会话断开，然后停止运行。

- 若未使用 load balancer：执行 `SHUTDOWN` 语句，TiDB 组件会做 graceful shutdown。

### TiDB 里面可以执行 kill 命令吗？

- Kill DML 语句：

    查询 `information_schema.cluster_processlist`，获取正在执行 DML 语句的 TiDB 实例地址和 session ID，然后执行 kill 命令。

    TiDB 从 v6.1.0 起新增 Global Kill 功能（由 [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-从-v610-版本开始引入) 配置项控制，默认启用）。启用 Global Kill 功能时，直接执行 `kill session_id` 即可。

    对于 TiDB v6.1.0 之前的版本，或未启用 Global Kill 功能时，`kill session_id` 默认不生效，客户端需要连接到正在执行 DML 语句的 TiDB 实例，然后执行 `kill tidb session_id` 才能 kill DML 语句。如果客户端连接到其他 TiDB 实例或者客户端和 TiDB 集群之间有代理，`kill tidb session_id` 可能会被路由到其他的 TiDB 实例，从而错误地终止其他会话。具体可以参考 [`KILL`](/sql-statements/sql-statement-kill.md)。

- Kill DDL 语句：执行 `admin show ddl jobs`，查找需要 kill 的 DDL job ID，然后执行 `admin cancel ddl jobs 'job_id' [, 'job_id'] ...`。具体可以参考 [`ADMIN`](/sql-statements/sql-statement-admin.md)。

### TiDB 是否支持会话超时？

TiDB 目前支持 [`wait_timeout`](/system-variables.md#wait_timeout)、[`interactive_timeout`](/system-variables.md#interactive_timeout) 和 [`tidb_idle_transaction_timeout`](/system-variables.md#tidb_idle_transaction_timeout-从-v760-版本开始引入) 三种超时。

### TiDB 的版本管理策略是怎么样的？

关于 TiDB 版本的管理策略，可以参考 [TiDB 版本规则](/releases/versioning.md)。

### 部署和维护 TiDB 集群的运营成本如何？

TiDB 提供了一些特性和[工具](/ecosystem-tool-user-guide.md)，可以帮助你以低成本管理集群：

- 在运维方面，[TiUP](/tiup/tiup-documentation-guide.md) 作为包管理器，简化了部署、扩缩容、升级和其他运维任务。
- 在监控方面，[TiDB 监控框架](/tidb-monitoring-framework.md)使用 [Prometheus](https://prometheus.io/) 存储监控和性能指标，使用 [Grafana](https://grafana.com/grafana/) 可视化这些指标。Grafana 内置了数十个面板，覆盖了数百个指标。
- 在故障诊断方面，[TiDB 集群问题导图](/tidb-troubleshooting-map.md)汇总了 TiDB 服务器和其他组件的常见问题。你可以使用这个导图来诊断和解决遇到的相关问题。

### 分不清 TiDB master 版本之间的区别，应该怎么办？

TiDB 目前社区非常活跃，同时，我们还在不断的优化和修改 BUG，因此 TiDB 的版本更新周期比较快，会不定期有新版本发布，请关注我们的[版本发布时间线](/releases/release-timeline.md)。此外 TiDB 安装推荐[使用 TiUP 进行安装](/production-deployment-using-tiup.md)或[使用 TiDB Operator 进行安装](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable)。TiDB 的版本号目前实现了统一管理，你可以通过如下任意方式查看 TiDB 的版本号：

- 通过 `select tidb_version()` 进行查看
- 通过执行 `tidb-server -V` 进行查看

### 如何扩容 TiDB 集群？

可以在不影响线上服务的情况下，对 TiDB 集群进行扩容。

- 如果是使用 [TiUP](/production-deployment-using-tiup.md) 部署的集群，可以参考[使用 TiUP 扩容 TiDB 集群](/scale-tidb-using-tiup.md)。
- 如果是使用 [TiDB Operator](/tidb-operator-overview.md) 在 Kubernetes 上部署的集群，可以参考[在 Kubernetes 中手动扩容 TiDB 集群](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/scale-a-tidb-cluster)。

### TiDB 如何进行水平扩展？

当您的业务不断增长时，数据库可能会面临三方面瓶颈，第一是存储空间，第二是计算资源，第三是读写容量，这时可以对 TiDB 集群做水平扩展。

- 如果是存储资源不够，可以通过添加 TiKV Server 节点来解决，新节点启动后，PD 会自动将其他节点的部分数据迁移过去，无需人工介入。
- 如果是计算资源不够，可以查看 TiDB Server 和 TiKV Server 节点的 CPU 消耗情况，再考虑添加 TiDB Server 节点或者是 TiKV Server 节点来解决，如添加 TiDB Server 节点，将其添加到前端 Load Balancer 配置之中即可。
- 如果是容量跟不上，一般可以考虑同时增加 TiDB Server 和 TiKV Server 节点。

### Percolator 用了分布式锁，crash 的客户端会保持锁，会造成锁没有 release？

详细可参考 [Percolator 和 TiDB 事务算法](https://pingcap.com/blog-cn/percolator-and-txn/)。

### TiDB 为什么选用 gRPC 而不选用 Thrift，是因为 Google 在用吗？

不只是因为 Google 在用，有一些比较好的特性我们需要，比如流控、加密还有 Streaming。

### like(bindo.customers.name, jason%, 92) 这个92代表什么？

那个是转义字符，默认是 (ASCII 92)。

### 为什么 `information_schema.tables.data_length` 记录的大小和 TiKV 监控面板上的 store size 不一样？

这是因为两者计算的角度不一样。`information_schema.tables.data_length` 是通过统计信息（平均每行的大小）得到的估算值。TiKV 监控面板上的 store size 是单个 TiKV 实例的数据文件（RocksDB 的 SST 文件）的大小总和。由于多版本和 TiKV 会压缩数据，所以两者显示的大小不一样。

### 为什么事务没有使用异步提交或一阶段提交？

在以下情况中，即使通过系统变量开启了[异步提交](/system-variables.md#tidb_enable_async_commit-从-v50-版本开始引入)和[一阶段提交](/system-variables.md#tidb_enable_1pc-从-v50-版本开始引入)，TiDB 也不会使用这些特性：

- 如果开启了 TiDB Binlog，受 TiDB Binlog 的实现原理限制，TiDB 不会使用异步提交或一阶段提交特性。
- TiDB 只在事务写入不超过 256 个键值对，以及所有键值对里键的总大小不超过 4 KB 时，才会使用异步提交或一阶段提交特性。这是因为对于写入量大的事务，异步提交不能明显提升执行性能。

## PD 管理

本小节介绍 PD 管理中的常见问题、原因及解决方法。

### 访问 PD 报错：TiKV cluster is not bootstrapped

PD 的大部分 API 需要在初始化 TiKV 集群以后才能使用，如果在部署新集群的时候只启动了 PD，还没有启动 TiKV，这时候访问 PD 就会报这个错误。遇到这个错误应该先把要部署的 TiKV 启动起来，TiKV 会自动完成初始化工作，然后就可以正常访问 PD。

### PD 启动报错：etcd cluster ID mismatch

PD 启动参数中的 `--initial-cluster` 包含了某个不属于该集群的成员。遇到这个错误时请检查各个成员的所属集群，剔除错误的成员后即可正常启动。

### PD 开启静态加密报错：`[PD:encryption:ErrEncryptionNewMasterKey]fail to get encryption key from file /root/path/file%!(EXTRA string=open /root/path/file: permission denied)`

静态加密不支持将密钥文件存放在 `root` 目录或其子目录下，即使增加读取权限也会报相同的错误。遇到这个报错时，可以将密钥文件存放在非 `root` 目录的路径下。

### PD 能容忍的时间同步误差是多少？

理论上，时间同步误差越小越好。PD 可容忍任意时长的误差，但是，时间同步误差越大意味着 PD 分配的时间戳与真实的物理时间相差越大，这个差距会影响读历史版本等功能。

### Client 连接是如何寻找 PD 的？

Client 连接只能通过 TiDB 访问集群，TiDB 负责连接 PD 与 TiKV，PD 与 TiKV 对 Client 透明。当 TiDB 连接任意一台 PD 的时候，PD 会告知 TiDB 当前的 leader 是谁，如果此台 PD 不是 leader，TiDB 将会重新连接至 leader PD。

### TiKV 节点 (Store) 各状态 (Up, Disconnect, Offline, Down, Tombstone) 之间的关系是什么？

使用 `pd-ctl` 可以查看 TiKV 节点的状态信息。如需查看各个状态之间的关系，请参考 [TiKV Store 状态之间的关系](/tidb-scheduling.md#信息收集)。

### PD 参数中 leader-schedule-limit 和 region-schedule-limit 调度有什么区别？

- leader-schedule-limit 调度是用来均衡不同 TiKV 的 leader 数，影响处理查询的负载。
- region-schedule-limit 调度是均衡不同 TiKV 的副本数，影响不同节点的数据量。

### 每个 region 的 replica 数量可配置吗？调整的方法是？

可以，目前只能调整全局的 replica 数量。首次启动时 PD 会读配置文件 (conf/pd.yml)，使用其中的 max-replicas 配置，之后修改需要使用 pd-ctl 配置命令 `config set max-replicas $num`，配置后可通过 `config show all` 来查看已生效的配置。调整的时候，不会影响业务，会在后台添加，注意总 TiKV 实例数总是要大于等于设置的副本数，例如 3 副本需要至少 3 个 TiKV。增加副本数量之前需要预估额外的存储需求。pd-ctl 的详细用法可参考 [PD Control 使用说明](/pd-control.md)。

### 缺少命令行集群管理工具，整个集群的健康度当前是否正常，不好确认？

可以通过 pd-ctl 等工具来判断集群大概的状态，详细的集群状态还是需要通过监控来确认。

### 集群下线节点后，怎么删除老集群节点监控信息？

下线节点一般指 TiKV 节点通过 pd-ctl 或者监控判断节点是否下线完成。节点下线完成后，手动停止下线节点上相关的服务。从 Prometheus 配置文件中删除对应节点的 node_exporter 信息。

## TiDB server 管理

本小节介绍 TiDB server 管理中的常见问题、原因及解决方法。

### TiDB 的 lease 参数应该如何设置？

启动 TiDB Server 时，需要通过命令行参数设置 lease 参数 (`--lease=60`)，其值会影响 DDL 的速度（只会影响当前执行 DDL 的 session，其他的 session 不会受影响）。在测试阶段，lease 的值可以设为 1s，加快测试进度；在生产环境下，我们推荐这个值设为分钟级（一般可以设为 60），这样可以保证 DDL 操作的安全。

### DDL 在正常情况下的耗时是多少？

一般情况下处理一个 DDL 操作（之前没有其他 DDL 操作在处理）的耗时基本可以分如下为三种：

- add index 操作，且此操作对应表数据行数比较少，耗时约为 3s。
- add index 操作，且此操作对应表数据行数比较多，耗时具体由表中数据行数和当时 QPS 情况定（add index 操作优先级比一般 SQL 低）。
- 其他 DDL 操作耗时约为 1s。

此外，如果接收 DDL 请求的 TiDB 和 DDL owner 所处的 TiDB 是一台，那么上面列举的第一和第三种可能的耗时应该在几十到几百毫秒。

### 为什么有的时候执行 DDL 会很慢？

可能原因如下：

- 多个 DDL 语句一起执行的时候，后面的几个 DDL 语句会比较慢。原因是当前 TiDB 集群中 DDL 操作是串行执行的。
- 在正常集群启动后，第一个 DDL 操作的执行时间可能会比较久，一般在 30s 左右，这个原因是刚启动时 TiDB 在竞选处理 DDL 的 leader。
- 由于停 TiDB 时不能与 PD 正常通信（包括停电情况）或者用 `kill -9` 指令停 TiDB 导致 TiDB 没有及时从 PD 清理注册数据，那么会影响 TiDB 启动后 10min 内的 DDL 语句处理时间。这段时间内运行 DDL 语句时，每个 DDL 状态变化都需要等待 2 * lease（默认 lease = 45s）。
- 当集群中某个 TiDB 与 PD 之间发生通信问题，即 TiDB 不能从 PD 及时获取或更新版本信息，那么这时候 DDL 操作的每个状态处理需要等待 2 * lease。

### TiDB 可以使用 S3 作为后端存储吗？

不可以，目前 TiDB 只支持分布式存储引擎和 GolevelDB/RocksDB/BoltDB 引擎。

### Information_schema 能否支持更多真实信息？

Information_schema 库里面的表主要是为了兼容 MySQL 而存在，有些第三方软件会查询里面的信息。在目前 TiDB 的实现中，里面大部分只是一些空表。后续随着 TiDB 的升级，会提供更多的参数信息。当前 TiDB 支持的 Information\_schema 请参考 [TiDB 系统数据库说明文档](/information-schema/information-schema.md)。

### TiDB Backoff type 主要原因？

TiDB-server 与 TiKV-server 随时进行通信，在进行大量数据操作过程中，会出现 `Server is busy` 或者 `backoff.maxsleep 20000ms` 的日志提示信息，这是由于 TiKV-server 在处理过程中系统比较忙而出现的提示信息，通常这时候可以通过系统资源监控到 TiKV 主机系统资源使用率比较高的情况出现。如果这种情况出现，可以根据资源使用情况进行相应的扩容操作。

### TiDB TiClient type 主要原因？

TiClient Region Error 该指标描述的是在 TiDB-server 作为客户端通过 KV 接口访问 TiKV-server 进行数据操作过程中，TiDB-server 操作 TiKV-server 中的 Region 数据出现的错误类型与 metric 指标，错误类型包括 not_leader、stale_epoch。出现这些错误的情况是当 TiDB-server 根据自己的缓存信息去操作 Region leader 数据的时候，Region leader 发生了迁移或者 TiKV 当前的 Region 信息与 TiDB 缓存的路由信息不一致而出现的错误提示。一般这种情况下，TiDB-server 都会自动重新从 PD 获取最新的路由数据，重做之前的操作。

### TiDB 同时支持的最大并发连接数？

默认情况下，每个 TiDB 服务器的最大连接数没有限制。如有需要，可以在 `config.toml` 文件中设置 `instance.max_connections`（或者系统变量 `max_connections`）来限制最大连接数。如果并发量过大导致响应时间增加，建议通过添加 TiDB 节点进行扩容。

### 如何查看某张表创建的时间？

information_schema 库中的 tables 表里的 create_time 即为表的真实创建时间。

### TiDB 的日志中 EXPENSIVE_QUERY 是什么意思？

TiDB 在执行 SQL 时，预估出来每个 operator 处理了超过 10000 条数据就认为这条 query 是 expensive query。可以通过修改 tidb-server 配置参数来对这个门限值进行调整，调整后需要重新启动 tidb-server。

### 如何预估 TiDB 中一张表的大小？

要预估 TiDB 中一张表的大小，你可以参考使用以下查询语句：

{{< copyable "sql" >}}

```sql
SELECT
    db_name,
    table_name,
    ROUND(SUM(total_size / cnt), 2) Approximate_Size,
    ROUND(SUM(total_size / cnt / (SELECT
                    ROUND(AVG(value), 2)
                FROM
                    METRICS_SCHEMA.store_size_amplification
                WHERE
                    value > 0)),
            2) Disk_Size
FROM
    (SELECT
        db_name,
            table_name,
            region_id,
            SUM(Approximate_Size) total_size,
            COUNT(*) cnt
    FROM
        information_schema.TIKV_REGION_STATUS
    WHERE
        db_name = @dbname
            AND table_name IN (@table_name)
    GROUP BY db_name , table_name , region_id) tabinfo
GROUP BY db_name , table_name;
```

在使用以上语句时，你需要根据实际情况填写并替换掉语句里的以下字段：

- `@dbname`：数据库名称。
- `@table_name`：目标表的名称。

此外，以上语句中：

- `store_size_amplification` 表示集群压缩比的平均值。除了使用 `SELECT * FROM METRICS_SCHEMA.store_size_amplification;` 语句进行查询以外，你还可以查看 Grafana 监控 **PD - statistics balance** 面板下各节点的 `Size amplification` 指标来获取该信息，集群压缩比的平均值即为所有节点的 `Size amplification` 平均值。
- `Approximate_Size` 表示压缩前表的单副本大小，该值为估算值，并非准确值。
- `Disk_Size` 表示压缩后表的大小，可根据 `Approximate_Size` 和 `store_size_amplification` 得出估算值。

## TiKV 管理

本小节介绍 TiKV 管理中的常见问题、原因及解决方法。

### 如何为合规性或多租户应用程序指定数据位置？

可以使用[放置规则 (Placement Rules)](/placement-rules-in-sql.md) 为合规性或多租户应用程序指定数据位置。

Placement Rules in SQL 用于控制任何连续数据范围的属性，例如副本数量、Raft 角色、放置位置以及规则生效的键范围。

### TiKV 集群副本建议配置数量是多少，是不是最小高可用配置（3个）最好？

如果是测试环境 3 副本足够；在生产环境中，不可让集群副本数低于 3，需根据架构特点、业务系统及恢复能力的需求，适当增加副本数。值得注意的是，副本升高，性能会有下降，但是安全性更高。

### TiKV 启动报错：cluster ID mismatch

TiKV 本地存储的 cluster ID 和指定的 PD 的 cluster ID 不一致。在部署新的 PD 集群的时候，PD 会随机生成一个 cluster ID，TiKV 第一次初始化的时候会从 PD 获取 cluster ID 存储在本地，下次启动的时候会检查本地的 cluster ID 与 PD 的 cluster ID 是否一致，如果不一致则会报错并退出。出现这个错误一个常见的原因是，用户原先部署了一个集群，后来把 PD 的数据删除了并且重新部署了新的 PD，但是 TiKV 还是使用旧的数据重启连到新的 PD 上，就会报这个错误。

### TiKV 启动报错：duplicated store address

启动参数中的地址已经被其他的 TiKV 注册在 PD 集群中了。造成该错误的常见情况：TiKV `--data-dir` 指定的路径下没有数据文件夹（删除或移动后没有更新 --data-dir），用之前参数重新启动该 TiKV。请尝试用 pd-ctl 的 [store delete](https://github.com/pingcap/pd/tree/55db505e8f35e8ab4e00efd202beb27a8ecc40fb/tools/pd-ctl#store-delete--label--weight-store_id----jqquery-string) 功能，删除之前的 store，然后重新启动 TiKV 即可。

### TiKV master 和 slave 用的是一样的压缩算法，为什么效果不一样？

目前来看 master 有些文件的压缩率会高一些，这个取决于底层数据的分布和 RocksDB 的实现，数据大小偶尔有些波动是正常的，底层存储引擎会根据需要调整数据。

### TiKV block cache 有哪些特性？

TiKV 使用了 RocksDB 的 Column Family (CF) 特性，KV 数据最终存储在默认 RocksDB 内部的 default、write、lock 3 个 CF 内。

- default CF 存储的是真正的数据，与其对应的参数位于 `[rocksdb.defaultcf]` 项中。
- write CF 存储的是数据的版本信息 (MVCC)、索引、小表相关的数据，相关的参数位于 `[rocksdb.writecf]` 项中。
- lock CF 存储的是锁信息，系统使用默认参数。
- Raft RocksDB 实例存储 Raft log。default CF 主要存储的是 Raft log，与其对应的参数位于 `[raftdb.defaultcf]` 项中。
- 所有 CF 共享一个 Block-cache，用于缓存数据块，加速 RocksDB 的读取速度。Block-cache 的大小通过参数 `block-cache-size` 控制，`block-cache-size` 越大，能够缓存的热点数据越多，对读取操作越有利，同时占用的系统内存也会越多。
- 每个 CF 有各自的 Write-buffer，大小通过 `write-buffer-size` 控制。

### TiKV channel full 是什么原因？

- Raftstore 线程太忙，或者因 I/O 而卡住。可以看一下 Raftstore 的 CPU 使用情况。
- TiKV 过忙（CPU、磁盘 I/O 等），请求处理不过来。

### TiKV 频繁切换 Region leader 是什么原因？

- 网络问题导致节点间通信卡了，查看 Report failures 监控。
- 原主 Leader 的节点卡了，导致没有及时给 Follower 发送消息。
- Raftstore 线程卡了。

### 如果一个节点挂了会影响服务吗？影响会持续多久？

TiDB 使用 Raft 在多个副本之间做数据同步（默认为每个 Region 3 个副本）。当一份备份出现问题时，其他的副本能保证数据的安全。根据 Raft 协议，当某个节点挂掉导致该节点里的 Leader 失效时，在最大 2 * lease time（leasetime 是 10 秒）时间后，通过 Raft 协议会很快将一个另外一个节点里的 Follower 选为新的 Region Leader 来提供服务。

### TiKV 在分别在哪些场景下占用大量 IO、内存、CPU（超过参数配置的多倍）？

在大量写入、读取的场景中会占用大量的磁盘 IO、内存、CPU。在执行很复杂的查询，比如会产生很大中间结果集的情况下，会消耗很多的内存和 CPU 资源。

### TiKV 是否可以使用 SAS/SATA 盘或者进行 SSD/SAS 混合部署？

不可以使用。TiDB 在进行 OLTP 场景中，数据访问和操作需要高 IO 磁盘的支持。TiDB 作为强一致的分布式数据库，存在一定的写放大，如副本复制、存储底层 Compaction，因此，TiDB 部署的最佳实践中推荐用户使用 NVMe SSD 磁盘作为数据存储磁盘。另外，TiKV 与 PD 不能混合部署。

### 数据表 Key 的 Range 范围划分是在数据接入之前就已经划分好了吗？

不是的，这个和 MySQL 分表规则不一样，需要提前设置好，TiKV 是根据 Region 的大小动态分裂的。

### Region 是如何进行分裂的？

Region 不是前期划分好的，但确实有 Region 分裂机制。当 Region 的大小超过参数 `region-max-size` 或 `region-max-keys` 的值时，就会触发分裂，分裂后的信息会汇报给 PD。

### TiKV 是否有类似 MySQL 的 `innodb_flush_log_trx_commit` 参数，来保证提交数据不丢失？

是的。TiKV 单机的存储引擎目前使用两个 RocksDB 实例，其中一个存储 raft-log。TiKV 有个 sync-log 参数，在 true 的情况下，每次提交都会强制刷盘到 raft-log，如果发生 crash 后，通过 raft-log 进行 KV 数据的恢复。

### 对 WAL 存储有什么推荐的硬件配置，例如 SSD，RAID 级别，RAID 卡 cache 策略，NUMA 设置，文件系统选择，操作系统的 IO 调度策略等？

WAL 属于顺序写，目前我们并没有单独对他进行配置，建议 SSD。RAID 如果允许的话，最好是 RAID 10，RAID 卡 cache、操作系统 I/O 调度目前没有针对性的最佳实践，Linux 7 以上默认配置即可。NUMA 没有特别建议，NUMA 内存分配策略可以尝试使用 `interleave = all`，文件系统建议 ext4。

### 在最严格的 `sync-log = true` 数据可用模式下，写入性能如何？

一般来说，开启 `sync-log` 会让性能损耗 30% 左右。关闭 `sync-log` 时的性能表现，请参见 [TiDB Sysbench 性能测试报告](/benchmark/v3.0-performance-benchmarking-with-sysbench.md)。

### 是否可以利用 TiKV 的 Raft + 多副本达到完全的数据可靠，单机存储引擎是否需要最严格模式？

通过使用 [Raft 一致性算法](https://raft.github.io/)，数据在各 TiKV 节点间复制为多副本，以确保某个节点挂掉时数据的安全性。只有当数据已写入超过 50% 的副本时，应用才返回 ACK（三副本中的两副本）。但理论上两个节点也可能同时发生故障，所以除非是对性能要求高于数据安全的场景，一般都强烈推荐开启 `sync-log`。

另外，还有一种 `sync-log` 的替代方案，即在 Raft group 中用五个副本而非三个。这将允许两个副本同时发生故障，而仍然能保证数据安全性。

对于单机存储引擎也同样推荐打开 `sync-log` 模式。否则如果节点宕机可能会丢失最后一次写入数据。

### 使用 Raft 协议，数据写入会有多次网络的 roundtrip，实际写入延迟如何？

理论上，和单机数据库相比，数据写入会多四个网络延迟。

### 有没有类似 MySQL 的 InnoDB Memcached plugin，可以直接使用 KV 接口，可以不需要独立的 Cache？

TiKV 支持单独进行接口调用，理论上也可以起个实例做为 Cache，但 TiDB 最大的价值是分布式关系型数据库，我们原则上不对 TiKV 单独进行支持。

### Coprocessor 组件的主要作用？

- 减少 TiDB 与 TiKV 之间的数据传输。
- 计算下推，充分利用 TiKV 的分布式计算资源。

### IO error: No space left on device While appending to file

这是磁盘空间不足导致的，需要加节点或者扩大磁盘空间。

### 为什么 TiKV 容易出现 OOM？

TiKV 的内存占用主要来自于 RocksDB 的 block-cache，默认为系统总内存的 40%。当 TiKV 容易出现 OOM 时，检查 `block-cache-size` 配置是否过高。还需要注意，当单机部署了多个 TiKV 实例时，需要显式地配置该参数，以防止多个实例占用过多系统内存导致 OOM。

### TiDB 数据和 RawKV 数据可存储于同一个 TiKV 集群里吗？

不可以。TiDB 数据（或使用其他事务 API 生成的数据）依赖于一种特殊的键值格式，和 RawKV API 数据（或其他基于 RawKV 的服务生成的数据）并不兼容。

## TiDB 测试

本小节介绍 TiDB 测试中的常见问题、原因及解决方法。

### TiDB Sysbench 基准测试结果如何？

很多用户在接触 TiDB 都习惯做一个基准测试或者 TiDB 与 MySQL 的对比测试，官方也做了一个类似测试。我们汇总很多测试结果后，发现虽然测试的数据有一定的偏差，但结论或者方向基本一致，由于 TiDB 与 MySQL 由于架构上的差别非常大，很多方面是很难找到一个基准点，所以官方的建议两点：

- 大家不要用过多精力纠结这类基准测试上，应该更多关注 TiDB 的场景上的区别。
- 大家可以直接参考 [TiDB Sysbench 性能测试报告](/benchmark/v3.0-performance-benchmarking-with-sysbench.md)。

### TiDB 集群容量 QPS 与节点数之间关系如何，和 MySQL 对比如何？

- 在 10 节点内，TiDB 写入能力 (Insert TPS) 和节点数量基本成 40% 线性递增，MySQL 由于是单节点写入，所以不具备写入扩展能力。
- MySQL 读扩容可以通过添加从库进行扩展，但写流量无法扩展，只能通过分库分表，而分库分表有很多问题，具体参考[方案虽好，成本先行：数据库 Sharding+Proxy 实践解析](http://dbaplus.cn/news-11-1854-1.html)。
- TiDB 不管是读流量、还是写流量都可以通过添加节点快速方便的进行扩展。

### 我们的 DBA 测试过 MySQL 性能，单台 TiDB 的性能没有 MySQL 性能那么好？

TiDB 设计的目标就是针对 MySQL 单台容量限制而被迫做的分库分表的场景，或者需要强一致性和完整分布式事务的场景。它的优势是通过尽量下推到存储节点进行并行计算。对于小表（比如千万级以下），不适合 TiDB，因为数据量少，Region 有限，发挥不了并行的优势。其中最极端的例子就是计数器表，几行记录高频更新，这几行在 TiDB 里，会变成存储引擎上的几个 KV，然后只落在一个 Region 里，而这个 Region 只落在一个节点上。加上后台强一致性复制的开销，TiDB 引擎到 TiKV 引擎的开销，最后表现出来的就是没有单个 MySQL 好。

## TiDB 备份恢复

本小节介绍 TiDB 备份恢复中的常见问题、原因及解决方法。

### TiDB 主要备份方式？

目前，数据量大时（大于 1 TB）推荐使用 [Backup & Restore (BR)](/br/backup-and-restore-overview.md) 进行备份。其他场景推荐使用 [Dumpling](/dumpling-overview.md) 进行备份。

尽管 TiDB 也支持使用 MySQL 官方工具 `mysqldump` 进行数据备份和恢复，但其性能低于 [Dumpling](/dumpling-overview.md)，并且 `mysqldump` 备份和恢复大量数据的耗费更长。

其他备份恢复相关问题，可以参考[备份与恢复常见问题](/faq/backup-and-restore-faq.md)。

### 备份和恢复的速度如何？

使用 [BR](/br/backup-and-restore-overview.md) 进行备份和恢复时，备份速度大约为每个 TiKV 实例 40 MB/s，恢复速度大约为每个 TiKV 实例 100 MB/s。
