---
title: 常见问题与解答
category: faq
---

# TiDB 中文 FAQ

## TiDB 是什么？

TiDB 是一个分布式 NewSQL 数据库。支持水平扩展、高可用、ACID 事务、SQL 等特性。同时 TiDB 还支持 MySQL 语法和 MySQL 协议。

## TiDB 是基于 MySQL 开发的吗？

不是。虽然 TiDB 支持 MySQL 语法和协议，但是 TiDB 是由 PingCAP 团队完全自主开发的产品。

## TiDB 和 TiKV 是如何配合使用？ 他们之间的关系是？

TiDB 是 SQL 层，主要负责 SQL 的解析、制定查询计划、生成执行器；TiKV 是分布式 Key-Value 存储引擎，用来存储真正的数据。简而言之，TiKV 是 TiDB 的存储引擎。

## Placement Driver (PD) 是做什么的？

PD 是 TiDB 集群的管理组件，负责存储 TiKV 的元数据，同时也负责分配时间戳以及对 TiKV 做负载均衡调度。

## TiDB 用起来简单吗？

是的，TiDB 用起来很简单。启动整套服务后，就可以将 TiDB 当做一个普通的 MySQL Server 来用，你可以将 TiDB 用在任何以 MySQL 作为后台存储服务的应用中，并且基本上不需要修改应用代码。同时你可以用大部分流行的 MySQL 管理工具来管理 TiDB。

## TiDB 适用的场景是？

原业务的 MySQL 的业务遇到单机容量或者性能瓶颈时，可以考虑使用 TiDB 无缝替换 MySQL。TiDB 可以提供如下特性：

+ 吞吐、存储和计算能力的水平扩展
+ 水平伸缩时不停服务
+ 强一致性
+ 分布式 ACID 事务

## TiDB 不适用于哪些场景？

如果你的应用数据量小 (所有数据千万级别行以下)，且没有高可用、强一致性或者多数据中心复制等要求，那么就不适合使用 TiDB。

## TiDB是如何进行权限管理的？

TiDB 遵循 MySQL 的权限管理体系，可以创建用户并授予权限。

在创建用户时，可以使用 MySQL 语法，如 `CREATE USER 'test'@'localhost' identified by '123';`，这样就添加了一个用户名为 test，密码为 123 的用户，这个用户只能从 localhost 登录。

修改用户密码时，可以使用 Set Password 语句，例如给 TiDB 的默认 root 用户增加密码：`SET PASSWORD FOR 'root'@'%' = '123';`。

在进行授权时，也可以使用 MySQL 语法，如 `GRANT SELECT ON *.* TO  'test'@'localhost';`，将读权限授予 test 用户。

更多细节可以参考[权限管理](https://github.com/pingcap/docs-cn/blob/master/sql/privilege.md)。

## 如何对 TiDB 进行水平扩展？

当您的业务不断增长时，数据库可能会面临三方面瓶颈，第一是存储资源不够，也就是磁盘空间不够；第二是计算资源不够用，如 CPU 占用较高， 第三是吞吐跟不上。这时可以对 TiDB 集群做水平扩展。

如果是存储资源不够，可以通过添加 TiKV Server 节点来解决。新节点启动后，PD 会自动将其他节点的部分数据迁移过去，无需人工介入。

如果是计算资源不够，可以查看 TiDB Server 和 TiKV Server 节点的 CPU 消耗情况，再考虑添加 TiDB Server 节点或者是 TiKV Server 节点来解决。如添加 TiDB Server 节点，将其配置在前端的 Load Balancer 之后即可。

如果是吞吐跟不上，一般可以考虑同时增加 TiDB Server 和 TiKV Server 节点。

## TiDB 高可用的特性是怎么样的？

高可用是 TiDB 的另一大特点，TiDB/TiKV/PD 这三个组件都能容忍部分实例失效，不影响整个集群的可用性。具体见 [TiDB 高可用性](README.md#高可用)。

## TiDB 的强一致特性是什么样的？

TiDB 使用 Raft 在多个副本之间做数据同步，从而保证数据的强一致。单个副本失效时，不影响数据的可靠性。

## TiDB 支持分布式事务吗？

TiDB 支持 ACID 分布式事务。事务模型是以 Google 的 Percolator 模型为基础，并做了一些优化。这个模型需要一个时间戳分配器，分配唯一且递增的时间戳。在 TiDB 集群中，PD 承担时间戳分配器的角色。

## 在使用 TiDB 时，我需要用什么编程语言？

可以用任何你喜欢的编程语言，只要该语言有 MySQL Client/Driver。

## TiDB 的 lease 参数应该如何设置？

启动 TiDB Server 时，需要通过命令行参数设置 lease 参数（`--lease=60`），其值会影响 DDL 的速度（只会影响当前执行 DDL 的 session，其他的 session 不会受影响）。在测试阶段，lease 的值可以设为 1s，加快测试进度；在生产环境下，我们推荐这个值设为分钟级（一般可以设为 60），这样可以保证 DDL 操作的安全。

## 在使用 TiDB 时，DDL 语句为什么这么慢？

TiDB 实现了 Google F1 的在线 Schema 变更算法（具体参见 [F1 论文](http://research.google.com/pubs/pub41376.html) 和[我们的一篇 Blog](https://github.com/ngaut/builddatabase/blob/master/f1/schema-change.md)）。 一般情况下，DDL 并不是一个频繁的操作，我们首先要保证的是数据的一致性以及线上业务不受影响。一个完整的 DDL 过程会有 2 到 5 个阶段（取决于语句类型），每个阶段至少会执行 2\*lease 时间，假设 lease 设为 1分钟，对于 Drop Table 语句（需要两个阶段），会执行 2\*2\*1 = 4 分钟。除此之外，DDL 的时间还取决其他的条件，比如做 Add Index 操作时，表中已有的数据量是影响 DDL 时间的主要因素。我们也了解过 Google 内部在 F1 上是如何做 DDL，一般是提交给 DBA，DBA 再通过专用的工具执行，执行的时间会很长。

## 和 MySQL/Oracle 等传统关系型数据库相比，TiDB 有什么优势？

和这些数据库相比，TiDB 最大的特点是可以无限水平扩展，在此过程中不损失事务特性。

## 和 Cassandra/Hbase/MongoDB 等 NoSQL 数据库相比，TiDB 有什么优势？

TiDB 在提供水平扩展特性的同时，还能提供 SQL 以及分布式事务。

## 如何将一个运行在 MySQL 上的应用迁移到 TiDB 上？

TiDB 支持绝大多数 MySQL 语法，一般不需要修改代码。我们提供了一个[检查工具](https://github.com/pingcap/tidb-tools/tree/master/checker)，用于检查 MySQL 中的 Schema 是否和 TiDB 兼容。

## TiDB 是否支持其他存储引擎？

是的。除了 TiKV 之外，TiDB 还支持一些流行的单机存储引擎，比如 GolevelDB, RocksDB,  BoltDB 等。如果一个存储引擎是支持事务的 KV 引擎，并且能提供一个满足 TiDB 接口要求的 Client，即可接入 TiDB。

## 使用 go get 方式安装 TiDB 为什么报错了？

请手动将TiDB克隆到GOPATH目录，然后运行 `make` 命令。TiDB是一个项目而不是一个库，它的依赖比较复杂，并且parser也是根据 `parser.y` 生成的，我们不支持 `go get` 方式，而是使用 Makefile 来管理。

如果你是开发者并且熟悉Go语言，你可以尝试在TiDB项目的根目录运行 `make parser; ln -s _vendor/src vendor` ，之后就可以使用 `go run`, `go test` `go install` 等命令，但是并不推荐这种做法。

## 为什么修改了 TiKV/PD 的 toml 配置文件，却没有生效？

如果要使用配置文件，请设置 TiKV/PD 的 --config 参数，TiKV/PD 默认情况下不会读取配置文件。

## 为什么 TiKV 数据目录不见了

TiKV 的 `--data-dir` 参数默认值为 `/tmp/tikv/store`，在某些虚拟机中，重启操作系统会删除 /tmp 目录下的数据，推荐通过 `--data-dir` 参数显式设置 TiKV 数据目录。

## TiKV 启动报错：cluster ID mismatch

TiKV 本地存储的 cluster ID 和指定的 PD 的 cluster ID 不一致。在部署新的 PD 集群的时候，PD 会随机生成一个 cluster ID，TiKV 第一次初始化的时候会从 PD 获取 cluster ID 存储在本地，下次启动的时候会检查本地的 cluster ID 与 PD 的 cluster ID 是否一致，如果不一致则会报错并退出。出现这个错误一个常见的原因是，用户原先部署了一个集群，后来把 PD 的数据删除了并且重新部署了新的 PD，但是 TiKV 还是使用旧的数据重启连到新的 PD 上，就会报这个错误。

## TiKV 启动报错：duplicated store address

启动参数中的地址已经被其他的 TiKV 注册在 PD 集群中了。造成该错误的常见情况：TiKV `--data-dir` 指定的路径下没有数据文件夹时（删除或移动后没有更新 `--data-dir`），用之前参数重新启动该 TiKV。请尝试用 pdctl 的 [store 删除](https://github.com/pingcap/pd/tree/master/pdctl#store-delete-store_id)功能，删除之前的 store, 然后重新启动 TiKV 即可。

## 访问 PD 报错：TiKV cluster is not bootstrapped

PD 的大部分 API 需要在初始化 TiKV 集群以后才能使用，如果在部署新集群的时候只启动了 PD，还没有启动 TiKV，这时候访问 PD 就会报这个错误。遇到这个错误应该先把要部署的 TiKV 启动起来，TiKV 会自动完成初始化工作，然后就可以正常访问 PD 。

## PD 启动报错：etcd cluster ID mismatch

PD 启动参数中的 `--initial-cluster` 包含了某个不属于该集群的成员。遇到这个错误时请检查各个成员的所属集群，剔除错误的成员后即可正常启动。

## 更改 PD 的启动参数

当想更改 PD 的 `--client-url`，`--advertise-client-url` 或 `--name` 时，只要用更新后的参数重新启动该 PD 就可以了。当更改的参数是 `--peer-url` 或 `--advertise-peer-url` 时，有以下几种情况需要区别处理：

 - 之前的启动参数中有 `--advertise-peer-url`，但只想更新 `--peer-url`：用更新后的参数重启即可。
 - 之前的启动参数中没有 `--advertise-peer-url`：先[用 etcdctl 更新该 PD 的信息](https://coreos.com/etcd/docs/latest/op-guide/runtime-configuration.html#update-a-member)，之后再用更新后的参数重启即可。

## TiDB/PD/TiKV 的日志在哪里

这三个组件默认情况下会将日志输出到标准错误，如果启动的时候通过 `--log-file` 参数指定了日志文件，那么日志会输出到指定的文件中，并且按天做 rotation。

## 我的数据盘是 xfs 且不能更改怎么办？
因为 rocksdb 在 xfs 和某些 linux kernel 中有 [bug](https://github.com/facebook/rocksdb/pull/2038)。所以不推荐使用 xfs 作为文件系统。

目前有个测试脚本，在 tikv 的部署盘运行，如果结果是 5000，可以尝试使用，但是上生产不建议。

	#!/bin/bash
	touch tidb_test
	fallocate -n -o 0 -l 9192 tidb_test
	printf 'a%.0s' {1..5000} > tidb_test
	truncate -s 5000 tidb_test
	fallocate -p -n -o 5000 -l 4192 tidb_test
	LANG=en_US.UTF-8 stat tidb_test |awk 'NR==2{print $2}'
	rm -rf tidb_test
	
## 出现 transaction too large 报错怎么办？ 	
由于分布式事务要做两阶段提交，并且底层还需要做 Raft 复制，如果一个事务非常大，会使得提交过程非常慢，并且会卡住下面的 Raft 复制流程。为了避免系统出现被卡住的情况，我们对事务的大小做了限制：

- 单条 KV entry 不超过 6MB

- KV entry 的总条数不超过 30w

- KV entry 的总大小不超过 100MB

在 Google 的 Cloud Spanner 上面，也有类似的限制（https://cloud.google.com/spanner/docs/limits）。

#### 解决方案：

##### 导入：
分批插入时一批最好别超过1w行，性能会好点。
##### insert select ：
我们内部有一个隐藏参数，当开启这个参数的时候，insert 会把大事务分批执行。好处是就不会因为事务太大导致超时了，坏处是语句就没有原子性了，假如中间报错，会造成“插一半”的情况，所以只有在需要的时候，使用这个功能。

	set @@session.tidb_batch_insert=1;

建议：

1.建议在 session 中使用，不影响其他语句 

2.使用以后可以关闭 `set @@session.tidb_batch_insert=0`

##### delete && update：
可以使用 limit 加循环的方式进行操作。

## select count(1) 比较慢，有优化方法么？
count(1)就是暴力扫表，提高并发度能显著的提升速度，修改并发度可以参考https://github.com/pingcap/docs-cn/blob/master/sql/tidb-specific.md#tidb_distsql_scan_concurrency。 但是也要看cpu、io资源。TiDB 每次查询都要访问 TiKV，在数据量小的情况下，mysql都在内存里，TiDB 还需要进行一次网络访问。

提升建议：

1. 建议提升硬件，符合我们的标准https://github.com/pingcap/docs-cn/blob/master/op-guide/recommendation.md
2. 提升并发度，默认是10，可以提升到50试试，但是一般提升在2-4倍之间
3. 测试大数据量的count
4. 调优 TiKV 配置： https://github.com/pingcap/docs-cn/blob/master/op-guide/tune-tikv.md



