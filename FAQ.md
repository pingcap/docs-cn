---
title: TiDB FAQ
category: FAQ
---

# TiDB FAQ

## 产品

### 关于产品

#### TiDB 是什么？

TiDB 是一个分布式 NewSQL 数据库。支持水平扩展、高可用、ACID 事务、SQL 等特性。同时 TiDB 还支持 MySQL 语法和 MySQL 协议。

#### TiDB 是基于 MySQL 开发的吗？

不是。虽然 TiDB 支持 MySQL 语法和协议，但是 TiDB 是由 PingCAP 团队完全自主开发的产品。

#### TiDB 和 MySQL Group Replication 的区别是什么？

MySQL Group Replication (MGR) 是基于 MySQL 单机版的一个高可用解决方案，而 MGR 不解决扩展性的问题。TiDB 从架构上就比较适合分布式场景，在开发过程中的各种决策也是以如何适应分布式场景出发来设计的。

#### TiDB 和 TiKV 如何配合使用？ 他们之间的关系是？

TiDB 是 SQL 层，主要负责 SQL 的解析、制定查询计划、生成执行器；TiKV 是分布式 Key-Value 存储引擎，用来存储真正的数据。简而言之，TiKV 是 TiDB 的存储引擎。

#### Placement Driver (PD) 是做什么的？

PD 是 TiDB 集群的管理组件，负责存储 TiKV 的元数据，同时也负责分配时间戳以及对 TiKV 做负载均衡调度。

#### TiDB 用起来简单吗？

是的，TiDB 用起来很简单。启动整套服务后，就可以将 TiDB 当做一个普通的 MySQL Server 来用，你可以将 TiDB 用在任何以 MySQL 作为后台存储服务的应用中，并且基本上不需要修改应用代码。同时你可以用大部分流行的 MySQL 管理工具来管理 TiDB。

#### TiDB 适用的场景是？

原业务的 MySQL 的业务遇到单机容量或者性能瓶颈时，可以考虑使用 TiDB 无缝替换 MySQL。TiDB 可以提供如下特性：

+ 吞吐、存储和计算能力的水平扩展
+ 水平伸缩时不停服务
+ 强一致性
+ 分布式 ACID 事务

#### TiDB 不适用于哪些场景？

如果你的应用数据量小（所有数据千万级别行以下），且没有高可用、强一致性或者多数据中心复制等要求，那么就不适合使用 TiDB。

#### TiDB 的强一致特性是什么样的？

TiDB 使用 Raft 在多个副本之间做数据同步，从而保证数据的强一致。单个副本失效时，不影响数据的可靠性。

#### TiDB 支持分布式事务吗？

TiDB 支持 ACID 分布式事务。事务模型是以 Google 的 Percolator 模型为基础，并做了一些优化。这个模型需要一个时间戳分配器，分配唯一且递增的时间戳。在 TiDB 集群中，PD 承担时间戳分配器的角色。

#### 当多个事务冲突严重时（如同时修改同一行数据），会造成某些事务写入失败吗？

会，事务冲突中写入失败的事务会进行退避，并在合适的时机进行重试，TiDB 中默认失败重试的次数为 10 次。

#### 在使用 TiDB 时，我需要用什么编程语言？

可以用任何你喜欢的编程语言，只要该语言有 MySQL Client/Driver。

#### 和 MySQL/Oracle 等传统关系型数据库相比，TiDB 有什么优势？

和这些数据库相比，TiDB 最大的特点是可以无限水平扩展，在此过程中不损失事务特性。

#### 和 Cassandra/Hbase/MongoDB 等 NoSQL 数据库相比，TiDB 有什么优势？

TiDB 在提供水平扩展特性的同时，还能提供 SQL 以及分布式事务。

#### 使用 `go get` 方式安装 TiDB 为什么报错了？

请手动将 TiDB 复制到 `GOPATH` 目录，然后运行 `make` 命令。TiDB 是一个项目而不是一个库，它的依赖比较复杂，并且 parser 也是根据 `parser.y` 生成的，我们不支持 `go get` 方式，而是使用 `Makefile` 来管理。

如果你是开发者并且熟悉 Go 语言，你可以尝试在 TiDB 项目的根目录运行 `make parser; ln -s _vendor/src vendor` ，之后就可以使用 `go run`, `go test`, `go install` 等命令，但是并不推荐这种做法。

#### TiDB 高可用的特性是怎么样的？

高可用是 TiDB 的另一大特点，TiDB/TiKV/PD 这三个组件都能容忍部分实例失效，不影响整个集群的可用性。具体见 [TiDB 高可用性](overview.md#高可用)。

#### TiDB 中删除数据后会立即释放空间吗？

DELETE，TRUNCATE 和 DROP 都不会立即释放空间。对于 TRUNCATE 和 DROP 操作，在达到 TiDB 的 GC (garbage collection) 时间后（默认 10 分钟），TiDB 的 GC 机制会删除数据并释放空间。对于 DELETE 操作 TiDB 的 GC 机制会删除数据，但不会释放空间，而是当后续数据写入 RocksDB 且进行 compact 时对空间重新利用。

#### Load 数据时可以对目标表执行 DDL 操作吗？

不可以，加载数据期间不能对目标表执行任何 DDL 操作，这会导致数据加载失败。

#### TiDB 是否支持 replace into 语法？

支持，但是 load data 不支持 replace into 语法。

#### 如何导出 TiDB 数据？

TiDB 目前暂时不支持 select into outfile，可以通过以下方式导出 TiDB 数据：

+ 参考 [MySQL使用mysqldump导出某个表的部分数据](http://blog.csdn.net/xin_yu_xin/article/details/7574662)，使用 mysqldump 加 where 条件导出。
+ 使用 MySQL client 将 select 的结果输出到一个文件。

#### TiDB 是否支持会话超时？

TiDB 暂不支持数据库层面的会话超时，目前想要实现超时，在没 LB（Load Balancing） 的时候，需要应用侧记录发起的 session 的 id，通过应用自定义超时，超时以后需要到发起 query 的节点上用 kill tidb id 来杀掉 sql。目前建议使用应用程序来实现会话超时，当达到超时时间，应用层就会抛出异常继续执行后续的程序段。

#### TiDB 生产环境的版本管理策略是怎么样的？如何尽可能避免频繁升级？
TiDB 版本目前逐步标准化，每次 Release 都包含详细的 Change list，版本功能[变化详情](https://github.com/pingcap/TiDB/releases)，生产环境是否有必要升级取决于业务系统，建议升级之前详细了解前后版本的功能差异。

版本号说明参考：`Release Version: v1.0.3-1-ga80e796`，`v1.0.3` 表示 GA 标准版 `-1` 表示该版本 commit 1 次，`ga80e796` 代表版本的 `git-hash`。

#### 分不清 TiDB master 版本之间的区别，经常用错 TiDB-Ansible 版本?
TiDB 目前社区非常活跃，在 GA 版本发布后，还在不断的优化和修改 BUG。因此 TiDB 的版本更新周期比较快，会不定期有新版本发布，请关注我们的[新版本发布官方网站](https://pingcap.com/weekly/)。此外 TiDB 安装推荐使用 TiDB-Ansible 进行安装，TiDB-Ansible 的版本也会随着 TiDB 的版本发布进行更新，因此建议用户在安装升级新版本的时候使用最新的 TiDB-Ansible 安装包版本进行安装。
此外，在 TiDB 版本 GA 后，对 TiDB 的版本号进行了统一管理，TiDB 的版本可以通过几种方式进行查看：
+ 通过 `select tidb_version()` 进行查看；
+ 通过执行 `tidb-server -V` 进行查看。

#### 官方有没有三中心跨机房部署的推荐方案？
从 TiDB 架构来讲，完全支持真正意义上的跨中心异地多活，操作层面依赖数据中心之间的网络延迟和稳定性，一般建议延迟在 5ms 以下，目前我们已经有相似客户方案，具体请咨询官方:info@pingcap.com。

#### 除了官方文档，有没有其他 TiDB 知识获取途径？
目前[官方文档](https://pingcap.com/docs-cn/)是获取 TiDB 相关知识最主要、最及时的发布途径。除此之外，我们也有一些技术沟通群，如有需求可发邮件至 Info@pingcap.com 获取。

#### TiDB 集群容量 QPS 与节点数之间关系如何，如何进行容量预估？
可以理解为大概是线性的关系，当前集群每个节点可以承载的 QPS，可参考[官方测试文档](http://t.cn/RT8oi0j)。

### PD

#### 访问 PD 报错：`TiKV cluster is not bootstrapped`

PD 的大部分 API 需要在初始化 TiKV 集群以后才能使用，如果在部署新集群的时候只启动了 PD，还没有启动 TiKV，这时候访问 PD 就会报这个错误。遇到这个错误应该先把要部署的 TiKV 启动起来，TiKV 会自动完成初始化工作，然后就可以正常访问 PD 了。

#### PD 启动报错：`etcd cluster ID mismatch`

PD 启动参数中的 `--initial-cluster` 包含了某个不属于该集群的成员。遇到这个错误时请检查各个成员的所属集群，剔除错误的成员后即可正常启动。

#### 更改 PD 的启动参数

当想更改 PD 的 `--client-url`，`--advertise-client-url` 或 `--name` 时，只要用更新后的参数重新启动该 PD 就可以了。当更改的参数是 `--peer-url` 或 `--advertise-peer-url` 时，有以下几种情况需要区别处理：

 - 之前的启动参数中有 `--advertise-peer-url`，但只想更新 `--peer-url`：用更新后的参数重启即可。
 - 之前的启动参数中没有 `--advertise-peer-url`：先[用 `etcdctl` 更新该 PD 的信息](https://coreos.com/etcd/docs/latest/op-guide/runtime-configuration.html#update-a-member)，之后再用更新后的参数重启即可。

#### PD 能容忍的时间同步误差是多少？

理论上误差越小越好，切换 leader 的时候如果时钟回退，就会卡住直到追上之前的 leader。这个容忍是业务上的，PD 多长的误差都能容忍。 但是误差越大，主从切换的时候，停止服务的时间越长。

#### Client 连接是如何寻找 PD 的？

Client 连接只能通过 TiDB 访问集群，TiDB 负责连接 PD 与 TiKV，PD 与 TiKV 对 client 透明。当 TiDB 连接任意一台 PD 的时候，PD 会告知 TiDB 当前的 leader 是谁，如果此台 PD 不是 leader ，TiDB 将会重新连接至 leader PD。

#### PD 参数中 leader-schedule-limit 和 region-schedule-limit 调度有什么区别？

leader-schedule-limit 调度是用来均衡不同 TiKV 的 leader 数，影响处理查询的负载。region-schedule-limit 调度是均衡不同 TiKV 的副本数，影响不同节点的数据量。

#### 每个 region 的 replica 数量可配置吗？调整的方法是？

可以，目前只能调整全局的 replica 数量。首次启动时 PD 会读配置文件（`conf/pd.yml`），使用其中的 max-replicas 配置，之后修改需要使用 pd-ctl 配置命令 `config set max-replicas $num`，配置后可通过 `config show all` 来查看已生效的配置。调整的时候，不会影响业务，会在后台添加，注意总 TiKV 实例数总是要大于等于设置的副本数，例如 3 副本需要至少 3 个 TiKV。增加副本数量之前需要预估额外的存储需求。pd-ctl 的详细用法可参考 [PD Control 使用说明](tools/pd-control.md)。

#### 集群下线节点后，怎么删除老集群节点监控信息？
下线节点一般指 TiKV 节点通过 pd-ctl 或者监控判断节点是否下线完成。节点下线完成后，手动停止下线节点上相关的服务。从 Prometheus 配置文件中删除对应节点的 `node_exporter` 信息。从 Ansible `inventory.ini` 中删除对应节点的信息。

#### 缺少命令行集群管理工具，整个集群的健康度当前是否正常，不好确认？
可以通过 pd-ctl 等工具来判断集群大体的状态，详细的集群状态还是需要通过监控来确认。

### TiDB

#### TiDB 的 lease 参数应该如何设置？

启动 TiDB Server 时，需要通过命令行参数设置 lease 参数（`--lease=60`），其值会影响 DDL 的速度（只会影响当前执行 DDL 的 session，其他的 session 不会受影响）。在测试阶段，lease 的值可以设为 1s，加快测试进度；在生产环境下，我们推荐这个值设为分钟级（一般可以设为 60），这样可以保证 DDL 操作的安全。

#### TiDB 是否支持其他存储引擎？

是的。除了 TiKV 之外，TiDB 还支持一些流行的单机存储引擎，比如 GolevelDB, RocksDB,  BoltDB 等。如果一个存储引擎是支持事务的 KV 引擎，并且能提供一个满足 TiDB 接口要求的 Client，即可接入 TiDB。

#### TiDB 中 Raft 的日志存储在哪里？

在 RocksDB 中。

#### 为什么有的时候执行 DDL 会很慢？

可能原因如下：

+ 多个 DDL 语句一起执行的时候，后面的几个 DDL 语句会比较慢。原因是当前 TiDB 集群中 DDL 操作是串行执行的。
+ 在正常集群启动后，第一个 DDL 操作的执行时间可能会比较久，一般在 30s 左右，这个原因是刚启动时 TiDB 在竞选处理 DDL 的 leader。
+ 在滚动升级或者停机升级时，由于停机顺序（先停 PD 再停 TiDB）或者用 `kill -9` 指令停 TiDB 导致 TiDB 没有及时清理注册数据，那么会影响 TiDB 启动后 10min 内的 DDL 语句处理时间。这段时间内运行 DDL 语句时，每个 DDL 状态变化都需要等待 2 * lease（默认 lease = 10s）。
+ 当集群中某个 TiDB 与 PD 之间发生通讯问题，即 TiDB 不能从 PD 及时获取或更新版本信息，那么这时候 DDL 操作的每个状态处理需要等待 2 * lease。

#### ERROR 2013 (HY000): Lost connection to MySQL server during query 问题的排查方法

+ log 中是否有 panic
+ dmesg 中是否有 oom, 命令：`dmesg |grep -i oom`
+ 长时间没有访问，也会收到这个报错，一般是 tcp 超时导致的，tcp 长时间不用, 会被操作系统 kill。

#### TiDB 可以使用 S3 作为后端存储吗？

不可以，目前 TiDB 只支持分布式存储引擎和 Goleveldb/Rocksdb/Boltdb 引擎；

#### 是否支持如下 DDL： `CREATE TABLE ... LOCATION "s3://xxx/yyy"`？

如果你能够实现 S3 存储引擎客户端，应该基于 TiKV 接口实现。

#### Infomation_schema 能否支持更多真实信息？
`Infomation_schema` 库里面的表主要是为了兼容 MySQL 而存在，有些第三方软件会查询里面的信息。在目前 TiDB 的实现中，里面大部分只是一些空表。后续随着 TiDB 的升级，会提供更多的参数信息。
当前 TiDB 支持的：`Infomation_schema` 请参考 [TiDB 系统数据库说明文档](https://pingcap.com/docs-cn/SQL/system-database/)。

#### TiDB 针对不同存储的优化建议？
TiDB 在进行 OLTP 场景中，数据访问和操作需要高 IO 磁盘的支持，因此，TiDB 部署的最佳实践中推荐用户使用 NVMe SSD 磁盘作为数据存储磁盘。

#### TiDB Backoff type 场景解释?
TiDB-server 在与 TiKV-server 通讯过程中，在进行大量数据操作过程中，会出现 `Server is busy` 或者 `backoff.maxsleep 20000ms` 的日志提示信息，这是由于 TiKV-server 在处理过程中系统比较忙而出现的提示信息。通常这时候可以通过系统资源监控到 TiKV 主机系统资源使用率比较高的情况出现。如果这种情况出现，可以根据资源使用情况进行相应的扩容操作。

#### TiClient type 场景解释
`TiClient Region Error` 该指标描述的是在 TiDB-server 作为客户端通过 kv 接口访问 TiKV-server 进行数据操作过程中，TiDB-server 操作 TiKV-server 中的 Region 数据出现的错误类型与 mertic 指标，错误类型包括 `not_leader`、`stale_epoch`。出现这些错误的情况是当 TiDB-server 根据自己的缓存信息去操作 Region leader 数据的时候，Region leader 发生了迁移或者 TiKV 当前的 Region 信息与 TiDB 缓存的路由信息不一致而出现的错误提示。一般这种情况下，TiDB-server 都会自动重新从 PD 获取最新的路由数据，重做之前的操作。

### TiKV

#### TiKV 集群副本建议配置数量是多少，是不是最小高可用配置（3个）最好？

测试的话，3 副本即可，副本升高，性能会有下降，但是安全性更高。是否设置更多副本需要看具体业务需要。

#### TiKV 可以指定独立副本机器吗（集群是集群，副本是副本，数据和副本分离）？

不可以。

#### 为什么 TiKV 数据目录不见了？

TiKV 的 `--data-dir` 参数默认值为 `/tmp/tikv/store`，在某些虚拟机中，重启操作系统会删除 `/tmp` 目录下的数据，推荐通过 `--data-dir` 参数显式设置 TiKV 数据目录。

#### TiKV 启动报错：`cluster ID mismatch`

TiKV 本地存储的 cluster ID 和指定的 PD 的 cluster ID 不一致。在部署新的 PD 集群的时候，PD 会随机生成一个 cluster ID，TiKV 第一次初始化的时候会从 PD 获取 cluster ID 存储在本地，下次启动的时候会检查本地的 cluster ID 与 PD 的 cluster ID 是否一致，如果不一致则会报错并退出。出现这个错误一个常见的原因是，用户原先部署了一个集群，后来把 PD 的数据删除了并且重新部署了新的 PD，但是 TiKV 还是使用旧的数据重启连到新的 PD 上，就会报这个错误。

#### TiKV 启动报错：`duplicated store address`

启动参数中的地址已经被其他的 TiKV 注册在 PD 集群中了。造成该错误的常见情况：TiKV `--data-dir` 指定的路径下没有数据文件夹时（删除或移动后没有更新 `--data-dir`），用之前参数重新启动该 TiKV。请尝试用 pdctl 的 [store 删除](https://github.com/pingcap/pd/tree/master/pdctl#store-delete-store_id)功能，删除之前的 store, 然后重新启动 TiKV 即可。

#### 按照 TiDB 的 key 设定，会不会很长？

RocksDB 对于 key 有压缩。

#### TiKV master 和 slave 用的是一样的压缩算法，为什么效果不一样?

目前来看 master 有些文件的压缩率会高一些，这个取决于底层数据的分布和 RocksDB 的实现，数据大小偶尔有些波动是正常的，底层存储引擎会根据需要调整数据。

#### TiKV block cache 有哪些特性？

TiKV 使用了 RocksDB 的 Column Family (CF) 特性，KV 数据最终存储在默认 RocksDB 内部的 default、write 和 lock 3 个 CF 内。

- default CF 存储的是真正的数据，与其对应的参数位于 [rocksdb.defaultcf] 项中； write CF 存储的是数据的版本信息（MVCC）以及索引相关的数据，相关的参数位于 [rocksdb.writecf] 项中； lock CF 存储的是锁信息，系统使用默认参数。

- Raft Rocksdb 实例存储 Raft log。 default CF 主要存储的是 Raft log，与其对应的参数位于 [raftdb.defaultcf] 项中。

- 每个 CF 都有单独的 block-cache，用于缓存数据块，加速 RocksDB 的读取速度，block-cache 的大小通过参数 block-cache-size 控制，block-cache-size 越大，能够缓存的热点数据越多，对读取操作越有利，同时占用的系统内存也会越多。

- 每个 CF 有各自的 write-buffer，大小通过 write-buffer-size 控制。

#### TiKV 相关线程解释

- 通过 `ps -Tp ${tikvPID}` 查看该 TiKV 下线程数量
- 登陆 TiKV 机器，通过 `top -h` 查看该机器下线程使用 CPU 状态
- 登陆 Grafana 查看 TiKV dashboard 中 Thread-CPU；该 tab 中有各线程使用 CPU 状态

| 线程名 | 相关信息 |
|----|-----  |
| grpc-server-* | TiKV 与邻居以及 TiDB & PD 网络通信线程 |
| raftstore-* |  负责处理 raft 消息，通常写入量大的时候该线程会增高 |
| sched-worker-* | TiKV 写入会经过这个线程，当有大量写入数据时，线程使用cpu 增高 |
| endpoint-* | TiKV 读取数据会经过这个线程，需要读取大量数据或者 explain 出现 TableScan，线程使用 CPU 增高 |
| apply worker | 数据写入操作完成后，会经过这个线程写入到 rocksdb |
| rocksdb:bg* | rocksdb 对数据进行 compaction 的线程 |

#### TiKV channel full 是啥原因？
+ Raftstore 线程卡了，可以看一下 Raftstore 的 CPU 使用情况。
+ TiKV 太忙了（读取、写入、磁盘 IO 等），请求处理不过来。

#### TiKV 频繁切换 Region leader 切换是啥原因？
+ 网络问题导致节点间通信卡了，查看 Report failures 监控。
+ 原主 Leader 的节点卡了，导致没有及时给 Follower 发送消息。
+ Raftstore 线程卡了。

#### Leader 节点挂了会影响服务吗？会有多久的影响 ？
TiDB 使用 Raft 在多个副本之间做数据同步，从而保证数据的强一致，当一份备份出现问题时，其他的副本能保证数据的安全。通常 TiDB 配置每个 Region 为 3 副本，根据 Raft 协议，每个 Region 会选取一个 Leader 提供服务。但单个Region Leader 失效时，在最大 2 * lease time（leasetime 是 10秒）时间后，通过 Raft 协议会很快选新的 Region Leader 提供服务。

#### TiKV 在分别那些场景下占用大量 IO，内存，CPU，超过参数配置的多倍？
在大量写入、读取的场景中会占用大量的磁盘 IO、内存和 CPU。在执行很复杂的查询，比如会产生很大中间结果集的情况下，会消耗很多的内存和 CPU 资源。

### TiSpark

#### TiSpark 的使用文档在哪里？

可以参考 [TiSpark 用户指南](tispark/tispark-user-guide.md)。

#### TiSpark 的案例

请参考[链接](https://github.com/zhexuany/tispark_examples)中介绍的案例。

## 运维

### 部署安装

#### 为什么修改了 TiKV/PD 的 toml 配置文件，却没有生效？

如果要使用配置文件，请设置 TiKV/PD 的 `--config` 参数，TiKV/PD 默认情况下不会读取配置文件。

#### 我的数据盘是 XFS 且不能更改怎么办？

因为 RocksDB 在 XFS 和某些 Linux kernel 中有 [bug](https://github.com/facebook/rocksdb/pull/2038)。所以不推荐使用 XFS 作为文件系统。

如果您想尝试使用，可以在 TiKV 的部署盘运行如下脚本，如果结果是 5000，可以尝试使用，但是不建议在生产环境中使用。

```bash
#!/bin/bash
touch tidb_test
fallocate -n -o 0 -l 9192 tidb_test
printf 'a%.0s' {1..5000} > tidb_test
truncate -s 5000 tidb_test
fallocate -p -n -o 5000 -l 4192 tidb_test
LANG=en_US.UTF-8 stat tidb_test |awk 'NR==2{print $2}'
rm -rf tidb_test
```
#### 可以配置 Chrony 满足 TiDB 对时间同步的要求吗？

可以，只要能让 PD 机器时间同步就行。若使用 Chrony 配置时间同步，请在运行 deploy 脚本之前将 `inventory.ini` 配置文件中的 `enable_ntpd` 置为 False，即 `enable_ntpd = False`。

#### TiDB 是否可以使用 SAS/SATA 盘或者进行 SSD/SAS 混合部署？
不可以使用，TiDB 在进行 OLTP 场景中，数据访问和操作需要高 IO 磁盘的支持，TiDB 作为强一致的分布式数据库，存在一定的写放大，如副本复制、存储底层 Compaction，因此，TiDB 部署的最佳实践中推荐用户使用 NVMe SSD 磁盘作为数据存储磁盘。另外，TiKV 与 PD 不能混合部署。

#### 有没有图形化部署 TiDB 的工具？
暂时没有。

#### 不想用 Ansible 部署 TiDB，能否支持其他部署的方法？
除 Ansible 之外，还支持 Docker 容器化部署，详细可在[官网](https://pingcap.com/docs-cn/op-guide/docker-deployment/)进行检索。官方更推荐 Ansible 方式，可以对集群主机做出相关优化以及检测，可以自动生成启动、停止、升级等脚本方便后期管理，同时部署了相关监控系统，在测试与调优以及排查问题时非常直观。

#### 可否在单机上安装开发环境？
可以，使用 `docker-compose` 在本地一键拉起一个集群，包括集群监控，还可以根据需求自定义各个组件的软件版本和实例个数，以及自定义配置文件。详细可参考[官方文档](https://github.com/pingcap/tidb-docker-compose)。

#### TiDB 同时支持的最大并发连接数 ？
当前版本 TiDB 没有最大连接数的限制，如果并发过大导致响应时间增加，可以通过增加 TiDB 节点进行扩容。

#### 是否可以将 TiDB 和 TiKV 部署在一起？
TiDB 和 TiKV 对 CPU 和内存都有比较高的要求，不建议部署到相同节点。

#### 为什么要在 CentOS 7 上部署 TiDB 集群？
TiDB 作为一款开源分布式 NewSQL 数据库，可以很好的部署和运行在 Intel 架构服务器环境及主流虚拟化环境，并支持绝大多数的主流硬件网络，作为一款高性能数据库系统，TiDB 支持主流的 Linux 操作系统环境，具体可以参考 TiDB 的[官方部署要求](https://pingcap.com/docs-cn/op-guide/recommendation/)。
其中 TiDB 在 CentOS 7 的环境下进行大量的测试，同时也有很多这个操作系统的部署最佳实践，因此，我们推荐客户在部署 TiDB 的时候使用 CentOS 7+ 以上的Linux 操作系统。

#### 2块网卡的目的是？万兆的目的是？
作为一个分布式集群，TiDB 对时间的要求还是比较高的，尤其是 PD 需要分发唯一的时间戳，如果 PD 时间不统一，如果有 PD 切换，将会等待更长的时间。2 块网卡可以做 bond，保证数据传输的稳定，万兆可以保证数据传输的速度，千兆网卡容易出现瓶颈，我们强烈建议使用万兆网卡。

### 扩容

#### 如何对 TiDB 进行水平扩展？

当您的业务不断增长时，数据库可能会面临三方面瓶颈，第一是存储资源不够，也就是磁盘空间不够；第二是计算资源不够用，如 CPU 占用较高，第三是吞吐跟不上。这时可以对 TiDB 集群做水平扩展。

- 如果是存储资源不够，可以通过添加 TiKV Server 节点来解决。新节点启动后，PD 会自动将其他节点的部分数据迁移过去，无需人工介入。
- 如果是计算资源不够，可以查看 TiDB Server 和 TiKV Server 节点的 CPU 消耗情况，再考虑添加 TiDB Server 节点或者是 TiKV Server 节点来解决。如添加 TiDB Server 节点，将其配置在前端的 Load Balancer 之后即可。
- 如果是吞吐跟不上，一般可以考虑同时增加 TiDB Server 和 TiKV Server 节点。

### 监控

#### TiDB 监控框架 Prometheus + Grafana 监控机器建议单独还是多台部署？建议 CPU 和内存是多少？

监控机建议单独部署。建议 CPU 8 core，内存 32 GB 以上，硬盘 500 GB 以上。

#### 有一部分监控信息显示不出来？

查看访问监控的机器时间跟集群内机器的时间差，如果比较大，更正时间后即可显示正常。

#### 如何配置监控 Syncer 运行情况？

下载 [Syncer Json](https://github.com/pingcap/docs/blob/master/etc/Syncer.json) 导入到 Grafana，修改 Prometheus 配置文件，添加以下内容：

```
- job_name: ‘syncer_ops’ // 任务名字
    static_configs:
      - targets: [’10.10.1.1:10096’] //syncer监听地址与端口，通知prometheus去拉去syncer的数据。
```

重启 Prometheus 即可。

#### 目前的监控使用方式及主要监控指标，有没有更好看的监控？
TiDB 使用 Prometheus + Grafana 组成 TiDB 数据库系统的监控系统，用户在 Grafana 上通过 dashboard 可以监控到 TiDB 的各类运行指标，包括系统资源的监控指标，包括客户端连接与 SQL 运行的指标，包括内部通讯和 Region 调度的指标，通过这些指标，可以让数据库管理员更好的了解到系统的运行状态，运行瓶颈等内容。在监控指标的过程中，我们按照 TiDB 不同的模块，分别列出了各个模块重要的指标项，一般用户只需要关注这些常见的指标项。具体指标请参见[官方文档](https://pingcap.com/docs-cn/op-guide/dashboard-overview-info/)。

### 数据迁移

#### 如何将一个运行在 MySQL 上的应用迁移到 TiDB 上？

TiDB 支持绝大多数 MySQL 语法，一般不需要修改代码。我们提供了一个[检查工具](https://github.com/pingcap/tidb-tools/tree/master/checker)，用于检查 MySQL 中的 Schema 是否和 TiDB 兼容。

#### 不小心把 MySQL 的 user 表导入到 TiDB 了，无法登陆，是否有办法恢复？

重启 TiDB 服务，配置文件中增加 `-skip-grant-table=true` 参数，登陆集群后按照如下 SQL 重建：

```sql
DROP TABLE IF EXIST mysql.user;

CREATE TABLE if not exists mysql.user (
    Host        CHAR(64),
    User        CHAR(16),
    Password      CHAR(41),
    Select_priv     ENUM('N','Y') NOT NULL DEFAULT 'N',
    Insert_priv     ENUM('N','Y') NOT NULL DEFAULT 'N',
    Update_priv     ENUM('N','Y') NOT NULL DEFAULT 'N',
    Delete_priv     ENUM('N','Y') NOT NULL DEFAULT 'N',
    Create_priv     ENUM('N','Y') NOT NULL DEFAULT 'N',
    Drop_priv     ENUM('N','Y') NOT NULL DEFAULT 'N',
    Process_priv      ENUM('N','Y') NOT NULL DEFAULT 'N',
    Grant_priv      ENUM('N','Y') NOT NULL DEFAULT 'N',
    References_priv     ENUM('N','Y') NOT NULL DEFAULT 'N',
    Alter_priv      ENUM('N','Y') NOT NULL DEFAULT 'N',
    Show_db_priv      ENUM('N','Y') NOT NULL DEFAULT 'N',
    Super_priv      ENUM('N','Y') NOT NULL DEFAULT 'N',
    Create_tmp_table_priv   ENUM('N','Y') NOT NULL DEFAULT 'N',
    Lock_tables_priv    ENUM('N','Y') NOT NULL DEFAULT 'N',
    Execute_priv      ENUM('N','Y') NOT NULL DEFAULT 'N',
    Create_view_priv    ENUM('N','Y') NOT NULL DEFAULT 'N',
    Show_view_priv      ENUM('N','Y') NOT NULL DEFAULT 'N',
    Create_routine_priv   ENUM('N','Y') NOT NULL DEFAULT 'N',
    Alter_routine_priv    ENUM('N','Y') NOT NULL DEFAULT 'N',
    Index_priv      ENUM('N','Y') NOT NULL DEFAULT 'N',
    Create_user_priv    ENUM('N','Y') NOT NULL DEFAULT 'N',
    Event_priv      ENUM('N','Y') NOT NULL DEFAULT 'N',
    Trigger_priv      ENUM('N','Y') NOT NULL DEFAULT 'N',
    PRIMARY KEY (Host, User));

INSERT INTO mysql.user VALUES ("%", "root", "", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y");

```
#### 怎样把数据从 TiDB 导出／导入呢？
TiDB 遵从 MySQL 协议，可以使用 Mydumper 工具导出数据，使用 Loader 工具导入数据，和 MySQL 导出／导入方式一样。

#### 数据删除后空间多长时间空间回收？
Delete，Truncate 和 Drop 都不会立即释放空间，对于 Truncate 和 Drop 操作，在达到 TiDB 的 GC (Garbage Collection) 时间后（默认 10 分钟），TiDB 的 GC 机制会删除数据并释放空间。对于 Delete 操作 TiDB 的 GC 机制会删除数据，但不会释放空间，而是当后续数据写入 RocksDB 且进行 Compact 时对空间重新利用。

#### 数据删除后查询速度变慢了？
大量删除数据后，会有很多无用的 key 存在，影响查询效率。目前正在开发 Region Merge 功能，完善之后可以解决这个问题，具体看参考[最佳实践](https://pingcap.com/blog-cn/tidb-best-practice/)中的删除数据部分。

#### 数据删除最高效最快的方式？
在删除大量数据的时候，建议使用 `Delete * from t where xx limit 5000`（xx 建议在满足业务过滤逻辑下，尽量加上强过滤索引列或者直接使用主键选定范围，如 `id >= 5000*n+m and id < 5000*(n+1)+m `）这样的方案，通过循环来删除，用 `Affected Rows == 0` 作为循环结束条件，这样避免遇到事务大小的限制。如果一次删除的数据量非常大，这种循环的方式会越来越慢，因为每次删除都是从前向后遍历，前面的删除之后，短时间内会残留不少删除标记（后续会被 GC 掉），影响后面的 Delete 语句。如果有可能，建议把 Where 条件细化。可以参考官网[最佳实践](https://pingcap.com/blog-cn/TiDB-best-practice/)。

#### Syncer / Drainer 同步出错、中断怎么处理？
+ 查看 log 分析出错原因。
+ 查看 [Syncer](https://pingcap.com/docs-cn/tools/syncer/)/ [Drainer](https://pingcap.com/docs-cn/tools/tidb-binlog-kafka/#pump-drainer-%E9%85%8D%E7%BD%AE) 文档寻求帮助。
+ 及时更换新版的 Syncer / Drainer。

### 性能调优

#### TiDB 如何提高数据加载速度？
主要三个方面：

+ 目前正在开发分布式导入工具 Lightning，需要注意的是数据导入过程中为了性能考虑，不会执行完整的事务流程，所以没办法保证导入过程中正在导入的数据的 ACID 约束，只能保证整个导入过程结束以后导入数据的 ACID 约束。因此适用场景主要为新数据的导入（比如新的表或者新的索引），或者是全量的备份恢复（先 Truncate 原表再导入）。
+ TiDB 的数据加载与磁盘以及整体集群状态相关，加载数据时应关注该主机的磁盘利用率/ TiClient Error / Backoff / Thread CPU 等相关 metric，可以分析相应瓶颈。


### 备份恢复

### 其他

#### TiDB 是如何进行权限管理的？

TiDB 遵循 MySQL 的权限管理体系，可以创建用户并授予权限。

在创建用户时，可以使用 MySQL 语法，如 `CREATE USER 'test'@'localhost' identified by '123';`，这样就添加了一个用户名为 test，密码为 123 的用户，这个用户只能从 localhost 登录。

修改用户密码时，可以使用 `Set Password` 语句，例如给 TiDB 的默认 root 用户增加密码：`SET PASSWORD FOR 'root'@'%' = '123';`

在进行授权时，也可以使用 MySQL 语法，如 `GRANT SELECT ON *.* TO  'test'@'localhost';` 将读权限授予 test 用户。

更多细节可以参考[权限管理](sql/privilege.md)。


#### TiDB/PD/TiKV 的日志在哪里？

这三个组件默认情况下会将日志输出到标准错误，如果启动的时候通过 `--log-file` 参数指定了日志文件，那么日志会输出到指定的文件中，并且按天做 rotation。

#### 如何安全停止 TiDB?

如果是用 Ansible 部署的，可以使用 `ansible-playbook stop.yml` 命令停止 TiDB 集群。如果不是 Ansible 部署的，可以直接 kill 掉所有服务。如果使用 kill 命令，TiDB 的组件会做 graceful 的 shutdown。

#### TiDB 里面可以执行 kill 命令吗？

可以 kill DML 语句。首先使用 `show processlist`，找到对应 session 的 id，然后执行 `kill tidb connection id`。
但是，目前不能 kill DDL 语句。DDL 语句一旦开始执行便不能停止，除非出错，出错以后，会停止运行。

#### supervise/svc/svstat 服务具体起什么作用？

- supervise 守护进程
- svc 启停服务
- svstat 查看进程状态

## SQL

### SQL 语法

#### 出现 `transaction too large` 报错怎么办？

由于分布式事务要做两阶段提交，并且底层还需要做 Raft 复制，如果一个事务非常大，会使得提交过程非常慢，并且会卡住下面的 Raft 复制流程。为了避免系统出现被卡住的情况，我们对事务的大小做了限制：

- 单条 KV entry 不超过 6MB
- KV entry 的总条数不超过 30w
- KV entry 的总大小不超过 100MB

在 Google 的 Cloud Spanner 上面，也有类似的[限制](https://cloud.google.com/spanner/docs/limits)。

**解决方案：**

+ 导入数据的时候，可以分批插入，每批最好不要超过 1w 行。
+ 对于 `insert` 和 `select`，可以开启 `set @@session.tidb_batch_insert=1;` 隐藏参数，`insert` 会把大事务分批执行。这样不会因为事务太大而超时，但是可能会导致事务原子性的丢失。如果事务执行过程中报错，会导致只完成一部分事务的插入。所以建议只有在需要的时候，在 session 中使用，这样不会影响其他语句。事务完成以后，可以用 `set @@session.tidb_batch_insert=0` 关闭。
+ 对 `delete` 和 `update` 语句，可以使用 `limit` 加循环的方式进行操作。

#### 查看 DDL job

+ 可以使用 `admin show ddl`，语句查看正在运行的 DDL 作业。
+ `admin show ddl jobs`，用于查看当前 DDL 作业队列中的所有结果（包括正在运行以及等待运行的任务）以及已执行完成的 DDL 作业队列中的最近十条结果。

#### 查看添加索引进度

+ 通过 `admin show ddl` 查看当前添加索引 job；如下:

```sql
mysql> admin show ddl;
+------------+--------------------------------------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------------+
| SCHEMA_VER | OWNER                                | JOB                                                                                                                             | SELF_ID                              |
+------------+--------------------------------------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------------+
|         69 | 9deb4179-fb5c-4040-b3b3-2e8fc585d8db | ID:102, Type:add index, State:running, SchemaState:write reorganization, SchemaID:81, TableID:90, RowCount:1293344122, ArgLen:0 | 9deb4179-fb5c-4040-b3b3-2e8fc585d8db |
+------------+--------------------------------------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------------+

```

+ 其中 OWNER 代表了正在执行此 DDL 的 tidb 机器；JOB 列出了任务详细信息
  + JOB 中 `SchemaID:81, TableID:90` 为数据库 ID 和用户表 ID
  + JOB 中 `RowCount:1293344122` 为当前已操作行数

#### 执行 `grant SHOW DATABASES on db.*` 报错 `column Show_db_priv not found`

`SHOW DATABASES` 是一个全局的权限而不是数据库级的权限，所以授予此项权限时，不能授予某个数据库，而是需要授予所有数据库：`grant SHOW DATABASES on *.*`。

### SQL 优化

#### TiDB 的执行计划如何查看？
参考[官网文档](https://pingcap.com/docs-cn/SQL/understanding-the-query-execution-plan/)。

#### `select count(1)` 比较慢，如何优化？

`count(1)` 就是暴力扫表，提高并发度能显著的提升速度，修改并发度可以参考 [`tidb_distsql_scan_concurrency`](sql/tidb-specific.md#tidb_distsql_scan_concurrency) 变量。但是也要看 CPU 和 I/O 资源。TiDB 每次查询都要访问 TiKV，在数据量小的情况下，MySQL 都在内存里，TiDB 还需要进行一次网络访问。

> 提升建议：
>
> 1. 建议提升硬件配置，可以参考[部署建议](op-guide/recommendation.md)。
> 2. 提升并发度，默认是 10，可以提升到 50 试试，但是一般提升在 2-4 倍之间。
> 3. 测试大数据量的 count。
> 4. 调优 TiKV 配置，可以参考[性能调优](op-guide/tune-tikv.md)。

#### 如何解决 FROM_UNIXTIME 效率低的问题？

获取系统时间不要使用 `FROM_UNIXTIME`，建议采用 `datetime` 转成时间戳去比较的方式，目前 `FROM_UNIXTIME` 无法走索引。

#### 每次手动或者定时 Analyze 表比较麻烦，什么时候可以实现自动 Analyze？
自动分析目前还没具体时间计划，但我们正在开发自动持续增量更新直方图的功能。
