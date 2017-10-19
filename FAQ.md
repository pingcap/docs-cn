---
title: FAQ
category: FAQ
---

# FAQ

+ [产品](#产品)
  + [关于产品](#关于产品)
    - [TiDB 是什么？](#tidb-是什么)
    - [TiDB 是基于 MySQL 开发的吗？](#tidb-是基于-mysql-开发的吗)
    - [TiDB 和 MySQL Group Replication 的区别是什么？](#tidb-和-mysql-group-replication-的区别是什么)
    - [TiDB 和 TiKV 是如何配合使用？ 他们之间的关系是？](#tidb-和-tikv-是如何配合使用-他们之间的关系是)
    - [Placement Driver (PD) 是做什么的？](#placement-driver-pd-是做什么的)
    - [TiDB 用起来简单吗？](#tidb-用起来简单吗)
    - [TiDB 适用的场景是？](#tidb-适用的场景是)
    - [TiDB 不适用于哪些场景？](#tidb-不适用于哪些场景)
    - [TiDB 的强一致特性是什么样的？](#tidb-的强一致特性是什么样的)
    - [TiDB 支持分布式事务吗？](#tidb-支持分布式事务吗)
    - [当多个事务冲突严重时（如同时修改同一行数据），会造成某些事务写入失败吗？](#当多个事务冲突严重时如同时修改同一行数据会造成某些事务写入失败吗)
    - [在使用 TiDB 时，我需要用什么编程语言？](#在使用-tidb-时我需要用什么编程语言)
    - [和 MySQL/Oracle 等传统关系型数据库相比，TiDB 有什么优势？](#和-mysqloracle-等传统关系型数据库相比tidb-有什么优势)
    - [和 Cassandra/Hbase/MongoDB 等 NoSQL 数据库相比，TiDB 有什么优势？](#和-cassandrahbasemongodb-等-nosql-数据库相比tidb-有什么优势)
    - [使用 `go get` 方式安装 TiDB 为什么报错了？](#使用-go-get-方式安装-tidb-为什么报错了)
    - [TiDB 高可用的特性是怎么样的？](#tidb-高可用的特性是怎么样的)
    - [TiDB 中删除数据后会立即释放空间吗？](#tidb-中删除数据后会立即释放空间吗)
    - [Load 数据时可以对目标表执行 DDL 操作吗？](#load-数据时可以对目标表执行-ddl-操作吗)
    - [TiDB 是否支持 replace into 语法？](#tidb-是否支持-replace-into-语法)
    - [如何导出 TiDB 数据？](#如何导出-tidb-数据)
    - [TiDB 是否支持会话超时？](#tidb-是否支持会话超时)
  + [PD](#pd)
    - [访问 PD 报错：`TiKV cluster is not bootstrapped`](#访问-pd-报错tikv-cluster-is-not-bootstrapped)
    - [PD 启动报错：`etcd cluster ID mismatch`](#pd-启动报错etcd-cluster-id-mismatch)
    - [更改 PD 的启动参数](#更改-pd-的启动参数)
    - [PD 能容忍的时间同步误差是多少？](#pd-能容忍的时间同步误差是多少)
    - [Client 连接是如何寻找 PD 的？](#client-连接是如何寻找-pd-的)
    - [PD 参数中 leader-schedule-limit 和 region-schedule-limit 调度有什么区别？](#pd-参数中-leader-schedule-limit-和-region-schedule-limit-调度有什么区别)
    - [每个 region 的 replica 数量可配置吗？调整的方法是？](#每个-region-的-replica-数量可配置吗调整的方法是)
  + [TiDB](#tidb)
    - [TiDB 的 lease 参数应该如何设置？](#tidb-的-lease-参数应该如何设置)
    - [TiDB 是否支持其他存储引擎？](#tidb-是否支持其他存储引擎)
    - [TiDB 中 Raft 的日志存储在哪里？](#tidb-中-raft-的日志存储在哪里)
    - [为什么有的时候执行 DDL 会很慢？](#为什么有的时候执行-ddl-会很慢)
    - [ERROR 2013 (HY000): Lost connection to MySQL server during query 问题的排查方法](#error-2013-hy000-lost-connection-to-mysql-server-during-query-问题的排查方法)
  + [TiKV](#tikv)
    - [TiKV 集群副本建议配置数量是多少，是不是最小高可用配置（3个）最好？](#tikv-集群副本建议配置数量是多少是不是最小高可用配置3个最好)
    - [TiKV 可以指定独立副本机器吗（集群是集群，副本是副本，数据和副本分离）？](#tikv-可以指定独立副本机器吗集群是集群副本是副本数据和副本分离)
    - [为什么 TiKV 数据目录不见了？](#为什么-tikv-数据目录不见了)
    - [TiKV 启动报错：`cluster ID mismatch`](#tikv-启动报错cluster-id-mismatch)
    - [TiKV 启动报错：`duplicated store address`](#tikv-启动报错duplicated-store-address)
    - [按照 TiDB 的 key 设定，会不会很长？](#按照-tidb-的-key-设定会不会很长)
  + [TiSpark](#tispark)
    - [TiSpark 的使用文档在哪里？](#tispark-的使用文档在哪里)
    - [TiSpark 的案例](#tispark-的案例)
+ [运维](#运维)
  + [部署安装](#部署安装)
    - [为什么修改了 TiKV/PD 的 toml 配置文件，却没有生效？](#为什么修改了-tikvpd-的-toml-配置文件却没有生效)
    - [我的数据盘是 XFS 且不能更改怎么办？](#我的数据盘是-xfs-且不能更改怎么办)
    - [可以配置 Chrony 满足 TiDB 对时间同步的要求吗？](#可以配置-chrony-满足-tidb-对时间同步的要求吗)
  + [扩容](#扩容)
    - [如何对 TiDB 进行水平扩展？](#如何对-tidb-进行水平扩展)
  + [监控](#监控)
    - [有一部分监控信息显示不出来？](#有一部分监控信息显示不出来)
    - [TiDB 监控框架 Prometheus + Grafana 监控机器建议单独还是多台部署？建议 cpu 和内存是多少？](#tidb-监控框架-prometheus--grafana-监控机器建议单独还是多台部署建议-cpu-和内存是多少)
  + [数据迁移](#数据迁移)
    - [如何将一个运行在 MySQL 上的应用迁移到 TiDB 上？](#如何将一个运行在-mysql-上的应用迁移到-tidb-上)
  - [性能调优](#性能调优)
  - [备份恢复](#备份恢复)
  + [其他](#其他)
    - [TiDB 是如何进行权限管理的？](#tidb-是如何进行权限管理的)
    - [TiDB/PD/TiKV 的日志在哪里？](#tidbpdtikv-的日志在哪里)
    - [如何安全停止 TiDB?](#如何安全停止-tidb)
    - [TiDB 里面可以执行 kill 命令吗？](#tidb-里面可以执行-kill-命令吗)
+ [SQL](#sql)
  + [SQL 语法](#sql-语法)
    - [出现 `transaction too large` 报错怎么办？](#出现-transaction-too-large-报错怎么办)
    - [查看 DDL job](#查看-ddl-job)
  + [SQL 优化](#sql-优化)
    - [`select count(1)` 比较慢，如何优化？](#select-count1-比较慢如何优化)


## 产品

### 关于产品

#### TiDB 是什么？

TiDB 是一个分布式 NewSQL 数据库。支持水平扩展、高可用、ACID 事务、SQL 等特性。同时 TiDB 还支持 MySQL 语法和 MySQL 协议。

#### TiDB 是基于 MySQL 开发的吗？

不是。虽然 TiDB 支持 MySQL 语法和协议，但是 TiDB 是由 PingCAP 团队完全自主开发的产品。

#### TiDB 和 MySQL Group Replication 的区别是什么？

MySQL Group Replication (MGR) 是基于 MySQL 单机版的一个高可用解决方案，而 MGR 不解决扩展性的问题。TiDB 从架构上就比较适合分布式场景，在开发过程中的各种决策也是以如何适应分布式场景出发来设计的。

#### TiDB 和 TiKV 是如何配合使用？ 他们之间的关系是？

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

高可用是 TiDB 的另一大特点，TiDB/TiKV/PD 这三个组件都能容忍部分实例失效，不影响整个集群的可用性。具体见 [TiDB 高可用性](README.md#高可用)。

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

可以，目前只能调整全局的 replica 数量。首次启动时 PD 会读配置文件（conf/pd.yml），使用其中的 max-replicas 配置，之后修改需要使用 pd-ctl 配置命令 `config set max-replicas $num`，配置后可通过 `config show all` 来查看已生效的配置。调整的时候，不会影响业务，会在后台添加，注意总 TiKV 实例数总是要大于等于设置的副本数，例如 3 副本需要至少 3 个 TiKV。增加副本数量之前需要预估额外的存储需求。pd-ctl 的详细用法可参考 [PD Control 使用说明](tools/pd-control.md)。

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


#### ERROR 2013 (HY000): Lost connection to MySQL server during query 问题的排查方法

+ log 中是否有 panic
+ dmesg 中是否有 oom, 命令：`dmesg |grep -i oom`
+ 长时间没有访问，也会收到这个报错，一般是 tcp 超时导致的，tcp 长时间不用, 会被操作系统 kill。

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

### TiSpark

#### TiSpark 的使用文档在哪里？

可以参考 [TiSpark 用户指南](op-guide/tispark-user-guide.md)。

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

可以，只要能让 PD 机器时间同步就行。若使用 Chrony 配置时间同步，请在运行 deploy 脚本之前将 inventory.ini 配置文件中的 enable_ntpd 置为 False，即 `enable_ntpd = False`。

### 扩容

#### 如何对 TiDB 进行水平扩展？

当您的业务不断增长时，数据库可能会面临三方面瓶颈，第一是存储资源不够，也就是磁盘空间不够；第二是计算资源不够用，如 CPU 占用较高，第三是吞吐跟不上。这时可以对 TiDB 集群做水平扩展。

- 如果是存储资源不够，可以通过添加 TiKV Server 节点来解决。新节点启动后，PD 会自动将其他节点的部分数据迁移过去，无需人工介入。
- 如果是计算资源不够，可以查看 TiDB Server 和 TiKV Server 节点的 CPU 消耗情况，再考虑添加 TiDB Server 节点或者是 TiKV Server 节点来解决。如添加 TiDB Server 节点，将其配置在前端的 Load Balancer 之后即可。
- 如果是吞吐跟不上，一般可以考虑同时增加 TiDB Server 和 TiKV Server 节点。

### 监控

#### TiDB 监控框架 Prometheus + Grafana 监控机器建议单独还是多台部署？建议 cpu 和内存是多少？

监控机建议单独部署。建议 CPU 8 core，内存 32 GB 以上，硬盘 500 GB 以上。

#### 有一部分监控信息显示不出来？

查看访问监控的机器时间跟集群内机器的时间差，如果比较大，更正时间后即可显示正常。

### 数据迁移

#### 如何将一个运行在 MySQL 上的应用迁移到 TiDB 上？

TiDB 支持绝大多数 MySQL 语法，一般不需要修改代码。我们提供了一个[检查工具](https://github.com/pingcap/tidb-tools/tree/master/checker)，用于检查 MySQL 中的 Schema 是否和 TiDB 兼容。

### 性能调优

### 备份恢复

### 其他

#### TiDB 是如何进行权限管理的？

TiDB 遵循 MySQL 的权限管理体系，可以创建用户并授予权限。

在创建用户时，可以使用 MySQL 语法，如 `CREATE USER 'test'@'localhost' identified by '123';`，这样就添加了一个用户名为 test，密码为 123 的用户，这个用户只能从 localhost 登录。

修改用户密码时，可以使用 `Set Password` 语句，例如给 TiDB 的默认 root 用户增加密码：`SET PASSWORD FOR 'root'@'%' = '123';`

在进行授权时，也可以使用 MySQL 语法，如 `GRANT SELECT ON *.* TO  'test'@'localhost';` 将读权限授予 test 用户。

更多细节可以参考[权限管理](https://github.com/pingcap/docs-cn/blob/master/sql/privilege.md)。


#### TiDB/PD/TiKV 的日志在哪里？

这三个组件默认情况下会将日志输出到标准错误，如果启动的时候通过 `--log-file` 参数指定了日志文件，那么日志会输出到指定的文件中，并且按天做 rotation。

#### 如何安全停止 TiDB?

如果是用 Ansible 部署的，可以使用 `ansible-playbook stop.yml` 命令停止 TiDB 集群。如果不是 Ansible 部署的，可以直接 kill 掉所有服务。如果使用 kill 命令，TiDB 的组件会做 graceful 的 shutdown。

#### TiDB 里面可以执行 kill 命令吗？

可以 kill DML 语句。首先使用 `show processlist`，找到对应 session 的 id，然后执行 `kill tidb connection id`。
但是，目前不能 kill DDL 语句。DDL 语句一旦开始执行便不能停止，除非出错，出错以后，会停止运行。

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

> 注意：除非 DDL 遇到错误，否则目前是不能取消的。

### SQL 优化

#### `select count(1)` 比较慢，如何优化？

`count(1)` 就是暴力扫表，提高并发度能显著的提升速度，修改并发度可以参考 [`tidb_distsql_scan_concurrency`](sql/tidb-specific.md#tidb_distsql_scan_concurrency) 变量。 但是也要看 CPU 和 I/O 资源。TiDB 每次查询都要访问 TiKV，在数据量小的情况下，MySQL 都在内存里，TiDB 还需要进行一次网络访问。

> 提升建议：
>
> 1. 建议提升硬件配置，可以参考[部署建议](op-guide/requirement.md)。
> 2. 提升并发度，默认是 10，可以提升到 50 试试，但是一般提升在 2-4 倍之间。
> 3. 测试大数据量的 count。
> 4. 调优 TiKV 配置，可以参考[性能调优](op-guide/tune-tikv.md)。
