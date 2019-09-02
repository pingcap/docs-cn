---
title: TiDB FAQ
category: FAQ
---

# 一、 TiDB 介绍、架构、原理

## 1.1 TiDB 介绍及整体架构
### 1.1.1 TiDB 整体架构

[https://pingcap.com/docs-cn/overview/](https://pingcap.com/docs-cn/overview/)

### 1.1.2 TiDB 是什么？

TiDB 是一个分布式 NewSQL 数据库。它支持水平弹性扩展、ACID 事务、标准 SQL、MySQL 语法和 MySQL 协议，具有数据强一致的高可用特性，是一个不仅适合 OLTP 场景还适合 OLAP 场景的混合数据库。

### 1.1.3 TiDB 是基于 MySQL 开发的吗？

不是，虽然 TiDB 支持 MySQL 语法和协议，但是 TiDB 是由 PingCAP 团队完全自主开发的产品。

### 1.1.4 TiDB、TiKV、Placement Driver (PD)  主要作用？

- TiDB 是 Server 计算层，主要负责 SQL 的解析、制定查询计划、生成执行器。
- TiKV 是分布式 Key-Value 存储引擎，用来存储真正的数据，简而言之，TiKV 是 TiDB 的存储引擎。
- PD 是 TiDB 集群的管理组件，负责存储 TiKV 的元数据，同时也负责分配时间戳以及对 TiKV 做负载均衡调度。

### 1.1.5 TiDB 易用性如何？

TiDB 使用起来很简单，可以将 TiDB 集群当成 MySQL 来用，你可以将 TiDB 用在任何以 MySQL 作为后台存储服务的应用中，并且基本上不需要修改应用代码，同时你可以用大部分流行的 MySQL 管理工具来管理 TiDB。

### 1.1.6 TiDB 和 MySQL 兼容性如何？

TiDB 目前还不支持触发器、存储过程、自定义函数、外键，除此之外，TiDB 支持绝大部分 MySQL 5.7 的语法。

详情参见：[与 MySQL 兼容性对比](sql/mysql-compatibility.md)。

### 1.1.7 TiDB 具备高可用的特性吗？

TiDB 天然具备高可用特性，TiDB、TiKV、PD 这三个组件都能容忍部分实例失效，不影响整个集群的可用性。具体见 [TiDB 高可用性](overview.md#高可用)。

### 1.1.8 TiDB 数据是强一致的吗？

TiDB 使用 Raft 在多个副本之间做数据同步，从而保证数据的强一致，单个副本失效时，不影响数据的可靠性。

### 1.1.9 TiDB 支持分布式事务吗？

TiDB 支持 ACID 分布式事务，事务模型是以 Google 的 Percolator 模型为基础，并做了一些优化。这个模型需要一个时间戳分配器，分配唯一且递增的时间戳。在 TiDB 集群中，PD 承担时间戳分配器的角色。

### 1.1.10 TiDB 支持哪些编程语言？

只要支持 MySQL Client/Driver 的编程语言，都可以直接使用 TiDB。

### 1.1.11 TiDB 是否支持其他存储引擎？

是的，除了 TiKV 之外，TiDB 还支持一些流行的单机存储引擎，比如 GolevelDB、RocksDB、BoltDB 等。如果一个存储引擎是支持事务的 KV 引擎，并且能提供一个满足 TiDB 接口要求的 Client，即可接入 TiDB。

### 1.1.12 官方有没有三中心跨机房多活部署的推荐方案？

从 TiDB 架构来讲，支持真正意义上的跨中心异地多活，从操作层面讲，依赖数据中心之间的网络延迟和稳定性，一般建议延迟在 5ms 以下，目前我们已经有相似客户方案，具体请咨询官方: [info@pingcap.com](mailto:info@pingcap.com)。

### 1.1.13 除了官方文档，有没有其他 TiDB 知识获取途径？

目前 [官方文档](https://pingcap.com/docs-cn/)是获取 TiDB 相关知识最主要、最及时的发布途径。除此之外，我们也有一些技术沟通群，如有需求可发邮件至 [info@pingcap.com](mailto:info@pingcap.com) 获取。

### 1.1.14 TiDB 对那些 MySQL variables 兼容？

详细可参考：[系统变量](sql/variable.md)

### 1.1.15 TiDB 是否支持 select for update 吗？

支持，但语义上和 MySQL 有区别，TiDB 是分布式数据库，采用的乐观锁机制，也就说 select for update 不在事务开启就锁住数据，而是其他事务在提交的时候进行冲突检查，如有冲突，会进行回滚。

### 1.1.16 TiDB 的 codec 能保证 UTF8 的字符串是 memcomparable 的吗？我们的 key 需要支持 UTF8，有什么编码建议吗？

TiDB 字符集默认就是 UTF8 而且目前只支持 UTF8，字符串就是 memcomparable 格式的。

## 1.2 TiDB 原理

### 1.2.1 存储 TiKV

#### 1.2.1.1 TiKV 详细解读

[http://t.cn/RTKRRWv](http://t.cn/RTKRRWv)

### 1.2.2 计算 TiDB

#### 1.2.2.1 TiDB 详细解读

[http://t.cn/RTKRkBh](http://t.cn/RTKRkBh)

### 1.2.3 调度 PD

#### 1.2.3.1 PD 详细解读

[http://t.cn/RTKEZ0U](http://t.cn/RTKEZ0U)

# 二、安装部署升级

## 2.1 环境准备

### 2.1.1 操作系统版本要求

| **Linux 操作系统平台** | **版本** |
| --- | --- |
| Red Hat Enterprise Linux | 7.3 及以上 |
| CentOS | 7.3 及以上 |
| Oracle Enterprise Linux | 7.3 及以上 |

#### 2.1.1.1  为什么要在 CentOS 7 上部署 TiDB 集群？

TiDB 作为一款开源分布式 NewSQL 数据库，可以很好的部署和运行在 Intel 架构服务器环境及主流虚拟化环境，并支持绝大多数的主流硬件网络，作为一款高性能数据库系统，TiDB 支持主流的 Linux 操作系统环境，具体可以参考 TiDB 的[官方部署要求](https://pingcap.com/docs-cn/op-guide/recommendation/)。 其中 TiDB 在 CentOS 7.3 的环境下进行大量的测试，同时也有很多这个操作系统的部署最佳实践，因此，我们推荐客户在部署 TiDB 的时候使用 CentOS 7.3+ 以上的Linux 操作系统。

### 2.1.2 硬件要求

TiDB 支持部署和运行在 Intel x86-64 架构的 64 位通用硬件服务器平台。对于开发，测试，及生产环境的服务器硬件配置有以下要求和建议：

#### 2.1.2.1 开发及测试环境

| **组件** | **CPU** | **内存** | **本地存储** | **网络** | **实例数量(最低要求)** |
| --- | --- | --- | --- | --- | --- |
| TiDB | 8核+ | 16 GB+ | SAS, 200 GB+ | 千兆网卡 | 1（可与 PD 同机器） |
| PD | 8核+ | 16 GB+ | SAS, 200 GB+ | 千兆网卡 | 1（可与 TiDB 同机器） |
| TiKV | 8核+ | 32 GB+ | SSD, 200 GB+ | 千兆网卡 | 3 |
|   |   |   |   | 服务器总计 | 4 |

#### 2.1.2.2 线上环境

| **组件** | **CPU** | **内存** | **硬盘类型** | **网络** | **实例数量(最低要求)** |
| --- | --- | --- | --- | --- | --- |
| TiDB | 16核+ | 48 GB+ | SAS | 万兆网卡（2块最佳） | 2 |
| PD | 8核+ | 16 GB+ | SSD | 万兆网卡（2块最佳） | 3 |
| TiKV | 16核+ | 48 GB+ | SSD | 万兆网卡（2块最佳） | 3 |
| 监控 | 8核+ | 16 GB+ | SAS | 千兆网卡 | 1 |
|   |   |   |   | 服务器总计 | 9 |

#### 2.1.2.3 2 块网卡的目的是？万兆的目的是？

作为一个分布式集群，TiDB 对时间的要求还是比较高的，尤其是 PD 需要分发唯一的时间戳，如果 PD 时间不统一，如果有 PD 切换，将会等待更长的时间。2 块网卡可以做 bond，保证数据传输的稳定，万兆可以保证数据传输的速度，千兆网卡容易出现瓶颈，我们强烈建议使用万兆网卡。

#### 2.1.2.4 SSD 不做 RAID 是否可行？

资源可接受的话，我们建议做 RAID 10，如果资源有限，也可以不做 RAID。

## 2.2 安装部署

### 2.2.1 Ansible 部署方式（强烈推荐）

详细可参考：[TiDB Ansible 部署方案](op-guide/ansible-deployment.md)

#### 2.2.1.1 为什么修改了 TiKV/PD 的 toml 配置文件，却没有生效？

这种情况一般是因为没有使用 `--config` 参数来指定配置文件（目前只会出现在 binary 部署的场景），TiKV/PD 会按默认值来设置。如果要使用配置文件，请设置 TiKV/PD 的 `--config` 参数。对于 TiKV 组件，修改配置后重启服务即可；对于 PD 组件，只会在第一次启动时读取配置文件，之后可以使用 pd-ctl 的方式来修改配置，详情可参考：[https://pingcap.com/docs-cn/tools/pd-control/](https://pingcap.com/docs-cn/tools/pd-control/)

#### 2.2.1.2 TiDB 监控框架 Prometheus + Grafana 监控机器建议单独还是多台部署？

监控机建议单独部署。建议 CPU 8 core，内存 16 GB 以上，硬盘 500 GB 以上。

#### 2.2.1.3 有一部分监控信息显示不出来？

查看访问监控的机器时间跟集群内机器的时间差，如果比较大，更正时间后即可显示正常。

#### 2.2.1.4 supervise/svc/svstat 服务具体起什么作用？

- supervise 守护进程
- svc 启停服务
- svstat 查看进程状态

#### 2.2.1.5 inventory.ini 变量参数解读

| **变量** | **含义** |
| --- | --- |
| cluster_name | 集群名称，可调整 |
| tidb_version | TiDB 版本，TiDB-Ansible 各分支默认已配置 |
| deployment_method | 部署方式，默认为 binary，可选 docker |
| process_supervision | 进程监管方式，默认为 systemd，可选 supervise |
| timezone | 修改部署目标机器时区，默认为 Asia/Shanghai, 可调整，与set_timezone 变量结合使用 |
| set_timezone | 默认为 True，即修改部署目标机器时区，关闭可修改为 False |
| enable_elk | 目前不支持，请忽略 |
| enable_firewalld | 开启防火墙，默认不开启 |
| enable_ntpd | 检测部署目标机器 NTP 服务，默认为 True，请勿关闭 |
| machine_benchmark | 检测部署目标机器磁盘 IOPS，默认为 True，请勿关闭 |
| set_hostname | 根据 IP 修改部署目标机器主机名，默认为 False |
| enable_binlog | 是否部署 pump 并开启 binlog，默认为 False，依赖 Kafka 集群，参见 zookeeper_addrs 变量 |
| zookeeper_addrs | binlog Kafka 集群的 zookeeper 地址 |
| enable_slow_query_log | TiDB 慢查询日志记录到单独文件({{ deploy_dir }}/log/tidb_slow_query.log)，默认为 False，记录到 tidb 日志 |
| deploy_without_tidb | KV 模式，不部署 TiDB 服务，仅部署 PD、TiKV 及监控服务，请将 inventory.ini 文件中 tidb_servers 主机组 IP 设置为空。 |

### 2.2.2 TiDB 离线 Ansible 部署方案

首先这不是我们建议的方式，如果中控机没有外网，也可以通过离线 Ansible 部署方式，详情可参考：[https://pingcap.com/docs-cn/op-guide/offline-ansible-deployment/](https://pingcap.com/docs-cn/op-guide/offline-ansible-deployment/)

### 2.2.3 Docker Compose 快速构建集群（单机部署）

使用 docker-compose 在本地一键拉起一个集群，包括集群监控，还可以根据需求自定义各个组件的软件版本和实例个数，以及自定义配置文件，这种只限于开发环境，详细可参考：[官方文档](https://pingcap.com/docs-cn/op-guide/docker-compose/)。

## 2.3 升级

### 2.3.1 如何使用 Ansible 滚动升级？

滚动升级 TiKV 节点( 只升级单独服务 )

`ansible-playbook rolling_update.yml --tags=tikv`

滚动升级所有服务

`ansible-playbook rolling_update.yml`

### 2.3.2 滚动升级有那些影响?

滚动升级 TiDB 服务，滚动升级期间不影响业务运行，需要配置最小集群拓扑（TiDB * 2、PD * 3、TiKV * 3），如果集群环境中有 Pump/Drainer 服务，建议先停止 Drainer 后滚动升级（升级 TiDB 时会升级 Pump）。

### 2.3.3 Binary 如何升级？

Binary 不是我们建议的安装方式，对升级支持也不友好，建议换成 Ansible 部署。

### 2.3.4 一般升级选择升级 TiKV 还是所有组件都升级？

常规需要一起升，因为整个版本都是一起测试的，单独升级只限当发生一个紧急故障时，需要单独对一个有问题的角色做升级。

### 2.3.5 启动集群或者升级集群过程中出现 “Timeout when waiting for search string 200 OK” 是什么原因？如何处理？

可能有以下几种原因：进程没有正常启动；端口被占用；进程没有正常停掉；停掉集群的情况下使用 rolling_update.yml 来升级集群（操作错误）。

处理方式：登录到相应节点查看进程或者端口的状态；纠正错误的操作步骤。

# 三、集群管理

## 3.1 集群日常管理

### 3.1.1 Ansible 常见运维操作有那些？

| **任务** | **Playbook** |
| --- | --- |
| 启动集群 | ansible-playbook start.yml |
| 停止集群 | ansible-playbook stop.yml |
| 销毁集群 | ansible-playbook unsafe\_cleanup.yml (若部署目录为挂载点，会报错，可忽略） |
| 清除数据(测试用) | ansible-playbook cleanup\_data.yml |
| 滚动升级 | ansible-playbook rolling\_update.yml |
| 滚动升级 TiKV | ansible-playbook rolling\_update.yml --tags=tikv |
| 滚动升级除 PD 外模块 | ansible-playbook rolling\_update.yml --skip-tags=pd |
| 滚动升级监控组件 | ansible-playbook rolling\_update\_monitor.yml |

### 3.1.2 TiDB 如何登录？

和 MySQL 登录方式一样，可以按照下面例子进行登录。

`mysql -h 127.0.0.1 -uroot -P4000`

### 3.1.3 TiDB 如何修改数据库系统变量？

和 MySQL 一样，TiDB 也分为静态参数和固态参数，静态参数可以直接通过`set global xxx = n`的方式进行修改，不过新参数值只限于该实例生命周期有效。

### 3.1.4 TiDB (TiKV) 有哪些数据目录？

默认在 ${[data-dir](https://pingcap.com/docs-cn/op-guide/configuration/#data-dir-1)}/data/ 目录下，其中包括 backup、db、raft、snap 四个目录，分别存储备份、数据、raft 数据及镜像数据。

### 3.1.5 TiDB 有哪些系统表？

和 MySQL 类似，TiDB 中也有系统表，用于存放数据库运行时所需信息，具体信息参考：[TiDB 系统数据库](https://pingcap.com/docs-cn/sql/system-database/)文档。

### 3.1.6 TiDB 各节点服务器下是否有日志文件，如何管理？

默认情况下各节点服务器会在日志中输出标准错误，如果启动的时候通过 `--log-file` 参数指定了日志文件，那么日志会输出到指定的文件中，并且按天做 rotation。

### 3.1.7 如何规范停止 TiDB？

如果是用 Ansible 部署的，可以使用 `ansible-playbook stop.yml` 命令停止 TiDB 集群。如果不是 Ansible 部署的，可以直接 kill 掉所有服务。如果使用 kill 命令，TiDB 的组件会做 graceful 的 shutdown。

### 3.1.8 TiDB 里面可以执行 kill 命令吗？

可以 kill DML 语句，首先使用 `show processlist`，找到对应 session 的 id，然后执行 `kill id`。

可以 kill DDL 语句，首先使用 `admin show ddl jobs`，查找需要 kill 的 DDL job ID，然后执行 `admin cancel ddl jobs 'job_id' [, 'job_id'] ...`。具体可以参考 [admin 操作](sql/admin.md#admin-语句)。

### 3.1.9 TiDB 是否支持会话超时？

TiDB 暂不支持数据库层面的会话超时，目前想要实现超时，在没 LB（Load Balancing）的时候，需要应用侧记录发起的 Session 的 ID，通过应用自定义超时，超时以后需要到发起 Query 的节点上用 `kill id` 来杀掉 SQL。目前建议使用应用程序来实现会话超时，当达到超时时间，应用层就会抛出异常继续执行后续的程序段。

### 3.1.10 TiDB 生产环境的版本管理策略是怎么样的？如何尽可能避免频繁升级？

TiDB 版本目前逐步标准化，每次 Release 都包含详细的 Change log，版本功能 [变化详情](https://github.com/pingcap/TiDB/releases)，生产环境是否有必要升级取决于业务系统，建议升级之前详细了解前后版本的功能差异。

版本号说明参考：Release Version: v1.0.3-1-ga80e796，v1.0.3 表示 GA 标准版 -1 表示该版本 commit 1 次，ga80e796 代表版本的 git-hash。

### 3.1.11 分不清 TiDB master 版本之间的区别，经常用错 TiDB-Ansible 版本?

TiDB 目前社区非常活跃，在 GA 版本发布后，还在不断的优化和修改 BUG，因此 TiDB 的版本更新周期比较快，会不定期有新版本发布，请关注我们的 [新版本发布官方网站](https://pingcap.com/weekly/)。此外 TiDB 安装推荐使用 TiDB-Ansible 进行安装，TiDB-Ansible 的版本也会随着 TiDB 的版本发布进行更新，因此建议用户在安装升级新版本的时候使用最新的 TiDB-Ansible 安装包版本进行安装。 此外，在 TiDB 版本 GA 后，对 TiDB 的版本号进行了统一管理，TiDB 的版本可以通过几种方式进行查看： 

- 通过 `select tidb_version()` 进行查看；
- 通过执行 `tidb-server -V` 进行查看。

### 3.1.12 有没有图形化部署 TiDB 的工具？

暂时没有。

### 3.1.13 TiDB 如何进行水平扩展？

当您的业务不断增长时，数据库可能会面临三方面瓶颈，第一是存储空间，第二是计算资源，第三是读写容量，这时可以对 TiDB 集群做水平扩展。

- 如果是存储资源不够，可以通过添加 TiKV Server 节点来解决，新节点启动后，PD 会自动将其他节点的部分数据迁移过去，无需人工介入。
- 如果是计算资源不够，可以查看 TiDB Server 和 TiKV Server 节点的 CPU 消耗情况，再考虑添加 TiDB Server 节点或者是 TiKV Server 节点来解决，如添加 TiDB Server 节点，将其添加到前端 Load Balancer 配置之中即可。
- 如果是容量跟不上，一般可以考虑同时增加 TiDB Server 和 TiKV Server 节点。

### 3.1.14 Percolator 用了分布式锁，crash 的客户端会保持锁，会造成锁没有 release？

详细可参考：[https://pingcap.com/blog-cn/percolator-and-txn/](https://pingcap.com/blog-cn/percolator-and-txn/)

### 3.1.15 TiDB 为什么选用 gRPC 而不选用 Thrift，是因为 Google 在用吗？

不只是因为 Google 在用，有一些比较好的特性我们需要，比如流控、加密还有 Streaming。

### 3.1.16 like(bindo.customers.name, jason%, 92) 这个92代表什么？

转义字符是那个，默认是 (ASCII 92)

## 3.2 PD 管理

### 3.2.1 访问 PD 报错：TiKV cluster is not bootstrapped

PD 的大部分 API 需要在初始化 TiKV 集群以后才能使用，如果在部署新集群的时候只启动了 PD，还没有启动 TiKV，这时候访问 PD 就会报这个错误。遇到这个错误应该先把要部署的 TiKV 启动起来，TiKV 会自动完成初始化工作，然后就可以正常访问 PD。

### 3.2.2 PD 启动报错：etcd cluster ID mismatch

PD 启动参数中的 `--initial-cluster` 包含了某个不属于该集群的成员。遇到这个错误时请检查各个成员的所属集群，剔除错误的成员后即可正常启动。

### 3.2.3 PD 能容忍的时间同步误差是多少？

理论上误差越小越好，切换 leader 的时候如果时钟回退，就会卡住直到追上之前的 leader。这个容忍是业务上的，PD 多长的误差都能容忍。但是误差越大，主从切换的时候，停止服务的时间越长。

### 3.2.4 Client 连接是如何寻找 PD 的？

Client 连接只能通过 TiDB 访问集群，TiDB 负责连接 PD 与 TiKV，PD 与 TiKV 对 Client 透明。当 TiDB 连接任意一台 PD 的时候，PD 会告知 TiDB 当前的 leader 是谁，如果此台 PD 不是 leader，TiDB 将会重新连接至 leader PD。

### 3.2.5 PD 参数中 leader-schedule-limit 和 region-schedule-limit 调度有什么区别？

- leader-schedule-limit 调度是用来均衡不同 TiKV 的 leader 数，影响处理查询的负载。
- region-schedule-limit 调度是均衡不同 TiKV 的副本数，影响不同节点的数据量。

### 3.2.6 每个 region 的 replica 数量可配置吗？调整的方法是？

可以，目前只能调整全局的 replica 数量。首次启动时 PD 会读配置文件（conf/pd.yml），使用其中的 max-replicas 配置，之后修改需要使用 pd-ctl 配置命令 `config set max-replicas $num`，配置后可通过 `config show all` 来查看已生效的配置。调整的时候，不会影响业务，会在后台添加，注意总 TiKV 实例数总是要大于等于设置的副本数，例如 3 副本需要至少 3 个 TiKV。增加副本数量之前需要预估额外的存储需求。pd-ctl 的详细用法可参考 [PD Control 使用说明](https://pingcap.com/docs-cn/FAQ/tools/pd-control.md)。

### 3.2.7 缺少命令行集群管理工具，整个集群的健康度当前是否正常，不好确认？

可以通过 pd-ctl 等工具来判断集群大概的状态，详细的集群状态还是需要通过监控来确认。

### 3.2.8 集群下线节点后，怎么删除老集群节点监控信息？

下线节点一般指 TiKV 节点通过 pd-ctl 或者监控判断节点是否下线完成。节点下线完成后，手动停止下线节点上相关的服务。从 Prometheus 配置文件中删除对应节点的 node_exporter 信息。从 Ansible inventory.ini 中删除对应节点的信息。

## 3.3 TiDB server 管理

### 3.3.1 TiDB 的 lease 参数应该如何设置？

启动 TiDB Server 时，需要通过命令行参数设置 lease 参数（--lease=60），其值会影响 DDL 的速度（只会影响当前执行 DDL 的 session，其他的 session 不会受影响）。在测试阶段，lease 的值可以设为 1s，加快测试进度；在生产环境下，我们推荐这个值设为分钟级（一般可以设为 60），这样可以保证 DDL 操作的安全。

### 3.3.2 为什么有的时候执行 DDL 会很慢？

可能原因如下：

- 多个 DDL 语句一起执行的时候，后面的几个 DDL 语句会比较慢。原因是当前 TiDB 集群中 DDL 操作是串行执行的。
- 在正常集群启动后，第一个 DDL 操作的执行时间可能会比较久，一般在 30s 左右，这个原因是刚启动时 TiDB 在竞选处理 DDL 的 leader。
- 在滚动升级或者停机升级时，由于停机顺序（先停 PD 再停 TiDB）或者用 `kill -9` 指令停 TiDB 导致 TiDB 没有及时清理注册数据，那么会影响 TiDB 启动后 10min 内的 DDL 语句处理时间。这段时间内运行 DDL 语句时，每个 DDL 状态变化都需要等待 2 * lease（默认 lease = 10s）。
- 当集群中某个 TiDB 与 PD 之间发生通讯问题，即 TiDB 不能从 PD 及时获取或更新版本信息，那么这时候 DDL 操作的每个状态处理需要等待 2 * lease。

### 3.3.3 TiDB 可以使用 S3 作为后端存储吗？

不可以，目前 TiDB 只支持分布式存储引擎和 Goleveldb/Rocksdb/Boltdb 引擎；

### 3.3.4 Information_schema 能否支持更多真实信息？

Information_schema 库里面的表主要是为了兼容 MySQL 而存在，有些第三方软件会查询里面的信息。在目前 TiDB 的实现中，里面大部分只是一些空表。后续随着 TiDB 的升级，会提供更多的参数信息。当前 TiDB 支持的：Information\_schema 请参考[TiDB 系统数据库说明文档](https://pingcap.com/docs-cn/sql/system-database)。

### 3.3.5 TiDB Backoff type 主要原因?

TiDB-server 与 TiKV-server 随时进行通讯，在进行大量数据操作过程中，会出现 Server is busy 或者 backoff.maxsleep 20000ms 的日志提示信息，这是由于 TiKV-server 在处理过程中系统比较忙而出现的提示信息，通常这时候可以通过系统资源监控到 TiKV 主机系统资源使用率比较高的情况出现。如果这种情况出现，可以根据资源使用情况进行相应的扩容操作。

### 3.3.6 TiDB TiClient type 主要原因？

TiClient Region Error 该指标描述的是在 TiDB-server 作为客户端通过 KV 接口访问 TiKV-server 进行数据操作过程中，TiDB-server 操作 TiKV-server 中的 Region 数据出现的错误类型与 mertic 指标，错误类型包括 not_leader、stale_epoch。出现这些错误的情况是当 TiDB-server 根据自己的缓存信息去操作 Region leader 数据的时候，Region leader 发生了迁移或者 TiKV 当前的 Region 信息与 TiDB 缓存的路由信息不一致而出现的错误提示。一般这种情况下，TiDB-server 都会自动重新从 PD 获取最新的路由数据，重做之前的操作。

### 3.3.7 TiDB 同时支持的最大并发连接数？

当前版本 TiDB 没有最大连接数的限制，如果并发过大导致响应时间增加，可以通过增加 TiDB 节点进行扩容。

## 3.4 TiKV 管理

### 3.4.1 TiKV 集群副本建议配置数量是多少，是不是最小高可用配置（3个）最好？

一般建议 3 副本即可，副本升高，性能会有下降，但是安全性更高。是否设置更多副本需要看具体业务需要。

### 3.4.2 TiKV 启动报错：cluster ID mismatch

TiKV 本地存储的 cluster ID 和指定的 PD 的 cluster ID 不一致。在部署新的 PD 集群的时候，PD 会随机生成一个 cluster ID，TiKV 第一次初始化的时候会从 PD 获取 cluster ID 存储在本地，下次启动的时候会检查本地的 cluster ID 与 PD 的 cluster ID 是否一致，如果不一致则会报错并退出。出现这个错误一个常见的原因是，用户原先部署了一个集群，后来把 PD 的数据删除了并且重新部署了新的 PD，但是 TiKV 还是使用旧的数据重启连到新的 PD 上，就会报这个错误。

### 3.4.3 TiKV 启动报错：duplicated store address

启动参数中的地址已经被其他的 TiKV 注册在 PD 集群中了。造成该错误的常见情况：TiKV `--data-dir` 指定的路径下没有数据文件夹（删除或移动后没有更新 --data-dir），用之前参数重新启动该 TiKV。请尝试用 pd-ctl 的[store delete](https://github.com/pingcap/pd/tree/master/pdctl#store-delete-store_id)功能，删除之前的 store, 然后重新启动 TiKV 即可。

### 3.4.4 TiKV master 和 slave 用的是一样的压缩算法，为什么效果不一样?

目前来看 master 有些文件的压缩率会高一些，这个取决于底层数据的分布和 RocksDB 的实现，数据大小偶尔有些波动是正常的，底层存储引擎会根据需要调整数据。

### 3.4.5 TiKV block cache 有哪些特性？

TiKV 使用了 RocksDB 的 Column Family (CF) 特性，KV 数据最终存储在默认 RocksDB 内部的 default、write、lock 3 个 CF 内。

- default CF 存储的是真正的数据，与其对应的参数位于 [rocksdb.defaultcf] 项中。 
- write CF 存储的是数据的版本信息（MVCC）、索引、小表相关的数据，相关的参数位于 [rocksdb.writecf] 项中。
- lock CF 存储的是锁信息，系统使用默认参数。
- Raft Rocksdb 实例存储 Raft log。default CF 主要存储的是 Raft log，与其对应的参数位于 [raftdb.defaultcf] 项中。
- 每个 CF 都有单独的 Block-cache，用于缓存数据块，加速 RocksDB 的读取速度，Block-cache 的大小通过参数 `block-cache-size` 控制，`block-cache-size` 越大，能够缓存的热点数据越多，对读取操作越有利，同时占用的系统内存也会越多。
- 每个 CF 有各自的 Write-buffer，大小通过 `write-buffer-size` 控制。

### 3.4.6 TiKV channel full 是啥原因？

- Raftstore 线程卡了，可以看一下 Raftstore 的 CPU 使用情况。
- TiKV 太忙了（读取、写入、磁盘 IO 等），请求处理不过来。

### 3.4.7 TiKV 频繁切换 Region leader 切换是啥原因？

- 网络问题导致节点间通信卡了，查看 Report failures 监控。
- 原主 Leader 的节点卡了，导致没有及时给 Follower 发送消息。
- Raftstore 线程卡了。

### 3.4.8 Leader 节点挂了会影响服务吗？会有多长时间的影响？

TiDB 使用 Raft 在多个副本之间做数据同步，从而保证数据的强一致，当一份备份出现问题时，其他的副本能保证数据的安全。通常 TiDB 配置每个 Region 为 3 副本，根据 Raft 协议，每个 Region 会选取一个 Leader 提供服务。但单个Region Leader 失效时，在最大 2 * lease time（leasetime 是 10 秒）时间后，通过 Raft 协议会很快选新的 Region Leader 提供服务。

### 3.4.9 TiKV 在分别在那些场景下占用大量 IO、内存、CPU（超过参数配置的多倍）？

在大量写入、读取的场景中会占用大量的磁盘 IO、内存、CPU。在执行很复杂的查询，比如会产生很大中间结果集的情况下，会消耗很多的内存和 CPU 资源。

### 3.4.10 TiKV 是否可以使用 SAS/SATA 盘或者进行 SSD/SAS 混合部署？

不可以使用，TiDB 在进行 OLTP 场景中，数据访问和操作需要高 IO 磁盘的支持，TiDB 作为强一致的分布式数据库，存在一定的写放大，如副本复制、存储底层 Compaction，因此，TiDB 部署的最佳实践中推荐用户使用 NVMe SSD 磁盘作为数据存储磁盘。另外，TiKV 与 PD 不能混合部署。

### 3.4.11 数据表 Key 的 Range 范围划分是在数据接入之前就已经划分好了吗？

不是的，这个和 MySQL 分表规则不一样，需要提前设置好，TiKV 是根据 Region 的大小动态分裂的。

### 3.4.12 Region 是如何进行分裂的？

首先不是前期划分好的，但确实有 Region 分裂机制，有一个参数 `region_split_size`，超过这个值就会触发分裂，分裂后的信息会汇报给 PD。

### 3.4.13 TiKV 是否有类似 MySQL 的 `innodb_flush_log_trx_commit` 参数，来保证提交数据不丢失？

是的，TiKV 单机的存储引擎目前使用两个 RocksDB 实例，其中一个存储 raft-log，TiKV 有个 sync-log 参数，在ture 的情况下，每次提交都会强制刷盘到 raft-log，如果发生 crash 后，通过 raft-log 进行 KV 数据的恢复。

### 3.4.14 对 WAL 存储有什么推荐的硬件配置，例如 SSD，RAID 级别，RAID 卡 cache 策略，NUMA 设置 ,文件系统选择，操作系统的 IO 调度策略等？

WAL 属于顺序写，目前我们并没有单独对他进行配置，建议 SSD，RAID 如果允许的话，最好是 RAID 10，RAID 卡 cache、操作系统 I/O 调度目前没有针对性的最佳实践，Linux 7 以上默认配置即可，NUMA 没有特别建议，NUMA 内存分配策略可以尝试使用 `interleave = all`，文件系统建议 ext4。

### 3.4.15 在最严格 sync-log = ture 的数据可用模式下，写入性能如何？

一般来说开启 sync-log 性能损耗大概 30% 左右，官方有个 `sync-log = false` 的基准测试，可以参考：[https://github.com/pingcap/docs-cn/blob/master/benchmark/sysbench.md](https://github.com/pingcap/docs-cn/blob/master/benchmark/sysbench.md)

### 3.4.16 是否可以利用上层的 Raft + 多副本，达到完全的数据可靠，单机存储引擎不需要最严格模式？

Raft 是强一致复制，写入必须同时超过 50% 的节点接受、应用才返回 ACK（三节点中二节点），在这种情况下，数据一致性是可以保证的，但理论上两个节点也可能同时Crash，所以在诸如金融行业对数据零容忍的场景，还是需要开启 sync-log。

### 3.4.17 使用 Raft 协议，数据写入会有多次网络的 roundtrip，实际写入延迟如何？

理论上和单机数据库比，多四个网络延迟。

### 3.4.18 有没有类似 MySQL 的 innodb Memcached plugin，可以直接使用 KV 接口，可以不需要独立的 Cache？

TiKV 支持单独进行接口调用，理论上也可以起个实例做为 Cache，但 TiDB 最大的价值是分布式关系型数据库，我们原则上不对 TiKV 单独进行支持。

### 3.4.19 Coprocessor 组件的主要作用？

- 减少 TiDB 与 TiKV 之间的数据传输。
- 计算下推，充分利用 TiKV 的分布式计算资源。

## 3.5 TiDB 测试

### 3.5.1 TiDB Sysbench 基准测试结果如何？

很多用户在接触 TiDB 都习惯做一个基准测试或者 TiDB 与 MySQL 的对比测试，官方也做了一个类似测试，汇总很多测试结果后，我们发现虽然测试的数据有一定的偏差，但结论或者方向基本一致，由于 TiDB 与 MySQL 由于架构上的差别非常大，很多方面是很难找到一个基准点，所以官方的建议两点：

- 大家不要用过多精力纠结这类基准测试上，应该更多关注 TiDB 的场景上的区别。
- 大家可以直接参考官方相关测试。官方 Sysbench 测试及 TiDB 与 MySQL 对比测试请参考：
[https://github.com/pingcap/docs-cn/blob/master/benchmark/sysbench.md](https://github.com/pingcap/docs-cn/blob/master/benchmark/sysbench.md)

### 3.5.2 TiDB 集群容量 QPS 与节点数之间关系如何，和 MySQL 对比如何？

- 在 10 节点内，TiDB 写入能力（Insert TPS）和节点数量基本成 40% 线性递增，MySQL 由于是单节点写入，所以不具备写入扩展能力。
- MySQL 读扩容可以通过添加从库进行扩展，但写流量无法扩展，只能通过分库分表，而分库分表有很多问题，具体参考：[http://t.cn/RTD18qV](http://t.cn/RTD18qV)。
- TiDB 不管是读流量、还是写流量都可以通过添加节点快速方便的进行扩展。

### 3.5.3 我们的 DBA 测试过 MySQL 性能，单台 TiDB 的性能没有 MySQL 性能那么好？

TiDB 设计的目标就是针对 MySQL 单台容量限制而被迫做的分库分表的场景，或者需要强一致性和完整分布式事务的场景。它的优势是通过尽量下推到存储节点进行并行计算。对于小表（比如千万级以下），不适合 TiDB， 因为数据量少，Region 有限，发挥不了并行的优势，最极端的就是计数器表，几行记录高频更新，这几行在 TiDB 里，会变成存储引擎上的几个 KV，然后只落在一个 Region 里，而这个 Region 只落在一个节点上。加上后台强一致性复制的开销，TiDB 引擎到 TiKV 引擎的开销，最后表现出来的就是没有单个 MySQL 好。

## 3.6 TiDB 备份恢复

### 3.6.1 TiDB 主要备份方式？

目前 TiDB 主要依赖 mydumper 逻辑导出进行备份，具体可以参考 [https://github.com/maxbube/mydumper](https://github.com/maxbube/mydumper)，虽然 TiDB 也支持使用 MySQL 官方的 mysqldump 工具来进行数据的备份恢复工作，但相比于 mydumper/loader，性能会慢很多，大量数据的备份恢复会花费很多时间，这里我们并不推荐。

使用 mydumper 导出来的数据文件尽可能的小, 最好不要超过 64M, 可以设置参数 -F 64；

loader的 -t 参数可以根据 TiKV 的实例个数以及负载进行评估调整，例如 3 个 TiKV 的场景， 此值可以设为 3 * (1 ～ n)，当 TiKV 负载过高，loader 以及 TiDB 日志中出现大量 `backoffer.maxSleep 15000ms is exceeded` 可以适当调小该值，当 TiKV 负载不是太高的时候，可以适当调大该值。

# 四、数据、流量迁移

## 4.1 全量数据导出导入

### 4.1.1 Mydumper 工具

具体可以参考 [https://github.com/maxbube/mydumper](https://github.com/maxbube/mydumper)

### 4.1.2 Loader 工具

具体可以参考 [https://pingcap.com/docs-cn/tools/loader/](https://pingcap.com/docs-cn/tools/loader/)

### 4.1.3 如何将一个运行在 MySQL 上的应用迁移到 TiDB 上？

TiDB 支持绝大多数 MySQL 语法，一般不需要修改代码。我们提供了一个[检查工具](https://github.com/pingcap/tidb-tools/tree/master/checker)，用于检查 MySQL 中的 Schema 是否和 TiDB 兼容。

### 4.1.4 不小心把 MySQL 的 user 表导入到 TiDB 了，或者忘记密码，无法登录，如何处理？

重启 TiDB 服务，配置文件中增加 `-skip-grant-table=true` 参数，无密码登录集群后，可以根据情况重建用户，或者重建 mysql.user 表，具体表结构搜索官网。

### 4.1.5 如何导出 TiDB 数据？

TiDB 目前暂时不支持 `select into outfile`，可以通过以下方式导出 TiDB 数据：参考 [MySQL使用mysqldump导出某个表的部分数据](http://blog.csdn.net/xin_yu_xin/article/details/7574662)，使用 mysqldump 加 where 条件导出，使用 MySQL client 将 select 的结果输出到一个文件。

### 4.1.6 DB2、Oracle 数据库如何迁移到 TiDB？

DB2、Oracle 到 TiDB 数据迁移（增量+全量），通常做法有：

- 使用 Oracle 官方迁移工具，如 OGG、Gateway（透明网关）、CDC（Change Data Capture）。
- 自研数据导出导入程序实现。
- 导出（Spool）成文本文件，然后通过 Load infile 进行导入。
- 使用第三方数据迁移工具。

目前看来 OGG 最为合适。

## 4.2 增量数据同步

### 4.2.1 Syncer 架构

详细参考：[https://pingcap.com/blog-cn/tidb-syncer/](https://pingcap.com/blog-cn/tidb-syncer/)

#### 4.2.1.1 Syncer 使用文档

详细参考：[https://pingcap.com/docs-cn/tools/syncer/](https://pingcap.com/docs-cn/tools/syncer/)

#### 4.2.1.2 如何配置监控 Syncer 运行情况？

下载 [Syncer Json](https://github.com/pingcap/tidb-ansible/blob/master/scripts/syncer.json) 导入到 Grafana，修改 Prometheus 配置文件，添加以下内容：

- job_name: &#39;syncer_ops&#39; // 任务名字
    static_configs:
- targets: [&#39;10.10.1.1:10096&#39;] //syncer监听地址与端口，通知 prometheus 拉取 syncer 的数据。

重启 Prometheus 即可。

#### 4.2.1.3 有没有现成的同步方案，可以将数据同步到 Hbase、Elasticsearh 等其他存储？

没有，目前依赖程序自行实现。

### 4.2.2 Wormhole 工具

Wormhole 是一项数据同步服务，让用户能够通过 Web 控制台, 轻松操作数据的全量 + 增量同步，支持多种同、异构数据源之间的数据迁移，如 MySQL -> TiDB，MongoDB -> TiDB。具体可联系官方进行试用：[info@pingcap.com](mailto:info@pingcap.com)。

## 4.3 业务流量迁入

### 4.3.1 如何快速迁移业务流量？

我们建议通过 Syncer 或 Wormhole 搭建成多源 MySQL、MongoDB -> TiDB 实时同步环境，读写流量可以按照需求分阶段通过修改网络配置进行流量迁移，建议 DB 上层部署一个稳定的网络 LB（HAproxy、LVS、F5、DNS 等），这样直接修改网络配置就能实现无缝流量迁移。

### 4.3.2 TiDB 总读写流量有限制吗？
TiDB 读流量可以通过增加 TiDB server 进行扩展，总读容量无限制，写流量可以通过增加 TiKV 节点进行扩容，基本上写容量也没有限制。

### 4.3.3 Transaction too large 是什么原因，怎么解决？

由于分布式事务要做两阶段提交，并且底层还需要做 Raft 复制，如果一个事务非常大，会使得提交过程非常慢，并且会卡住下面的 Raft 复制流程。为了避免系统出现被卡住的情况，我们对事务的大小做了限制：

- 单条 KV entry 不超过 6MB
- KV entry 的总条数不超过 30w
- KV entry 的总大小不超过 100MB

在 Google 的 Cloud Spanner 上面，也有类似的[限制](https://cloud.google.com/spanner/docs/limits)。

### 4.3.4 如何批量导入?

导入数据的时候，可以分批插入，每批最好不要超过 1w 行。

对于 insert 和 select，可以开启 `set @@session.tidb_batch_insert=1;` 隐藏参数，insert 会把大事务分批执行。这样不会因为事务太大而超时，但是可能会导致事务原子性的丢失。如果事务执行过程中报错，会导致只完成一部分事务的插入。所以建议只有在需要的时候，在 session 中使用，这样不会影响其他语句。事务完成以后，可以用 `set @@session.tidb_batch_insert=0` 关闭。

对 delete 和 update 语句，可以使用 limit 加循环的方式进行操作。

### 4.3.5 TiDB 中删除数据后会立即释放空间吗？

DELETE，TRUNCATE 和 DROP 都不会立即释放空间。对于 TRUNCATE 和 DROP 操作，在达到 TiDB 的 GC (garbage collection) 时间后（默认 10 分钟），TiDB 的 GC 机制会删除数据并释放空间。对于 DELETE 操作 TiDB 的 GC 机制会删除数据，但不会释放空间，而是当后续数据写入 RocksDB 且进行 compact 时对空间重新利用。

### 4.3.6 Load 数据时可以对目标表执行 DDL 操作吗？

不可以，加载数据期间不能对目标表执行任何 DDL 操作，这会导致数据加载失败。

### 4.3.7 TiDB 是否支持 replace into 语法？

支持，但是 load data 不支持 replace into 语法。

### 4.3.8 数据删除后空间多长时间空间回收？

Delete，Truncate 和 Drop 都不会立即释放空间，对于 Truncate 和 Drop 操作，在达到 TiDB 的 GC (Garbage Collection) 时间后（默认 10 分钟），TiDB 的 GC 机制会删除数据并释放空间。对于 Delete 操作 TiDB 的 GC 机制会删除数据，但不会释放空间，而是当后续数据写入 RocksDB 且进行 Compact 时对空间重新利用。

### 4.3.9 数据删除后查询速度为何会变慢？

大量删除数据后，会有很多无用的 key 存在，影响查询效率。目前正在开发 Region Merge 功能，完善之后可以解决这个问题，具体看参考 [最佳实践](https://pingcap.com/blog-cn/tidb-best-practice/)中的删除数据部分。

### 4.3.10 数据删除最高效最快的方式？

在删除大量数据的时候，建议使用 `Delete * from t where xx limit 5000`（xx 建议在满足业务过滤逻辑下，尽量加上强过滤索引列或者直接使用主键选定范围，如 `id >= 5000*n+m and id <= 5000*(n+1)+m` 这样的方案，通过循环来删除，用 `Affected Rows == 0` 作为循环结束条件，这样避免遇到事务大小的限制。如果一次删除的数据量非常大，这种循环的方式会越来越慢，因为每次删除都是从前向后遍历，前面的删除之后，短时间内会残留不少删除标记（后续会被 GC 掉），影响后面的 Delete 语句。如果有可能，建议把 Where 条件细化。可以参考官网 [最佳实践](https://pingcap.com/blog-cn/tidb-best-practice/)。

### 4.3.11 TiDB 如何提高数据加载速度？

主要三个方面：

- 目前正在开发分布式导入工具 Lightning，需要注意的是数据导入过程中为了性能考虑，不会执行完整的事务流程，所以没办法保证导入过程中正在导入的数据的 ACID 约束，只能保证整个导入过程结束以后导入数据的 ACID 约束。因此适用场景主要为新数据的导入（比如新的表或者新的索引），或者是全量的备份恢复（先 Truncate 原表再导入）。
- TiDB 的数据加载与磁盘以及整体集群状态相关，加载数据时应关注该主机的磁盘利用率，TiClient Error/Backoff/Thread CPU 等相关 metric，可以分析相应瓶颈。

# 五、SQL 优化

## 5.1 TiDB 执行计划解读

详细解读：[https://pingcap.com/docs-cn/sql/understanding-the-query-execution-plan](https://pingcap.com/docs-cn/sql/understanding-the-query-execution-plan)

### 5.1.1 统计信息收集

详细解读：[https://pingcap.com/docs-cn/sql/statistics](https://pingcap.com/docs-cn/sql/statistics)

### 5.1.2 Count 如何加速？

Count 就是暴力扫表，提高并发度能显著的提升速度，修改并发度可以参考 `tidb_distsql_scan_concurrency` 变量，但是也要看 CPU 和 I/O 资源。TiDB 每次查询都要访问 TiKV，在数据量小的情况下，MySQL 都在内存里，TiDB 还需要进行一次网络访问。

提升建议：

- 建议提升硬件配置，可以参考[部署建议](op-guide/requirement.md)。
- 提升并发度，默认是 10，可以提升到 50 试试，但是一般提升在 2-4 倍之间。
- 测试大数据量的 count。
- 调优 TiKV 配置，可以参考[性能调优](op-guide/tune-tikv.md)。

### 5.1.3 查看添加索引进度？

通过 `admin show ddl` 查看当前添加索引 job。

### 5.1.4 如何查看 DDL job？

可以使用 `admin show ddl`，语句查看正在运行的 DDL 作业。
`admin show ddl jobs`，用于查看当前 DDL 作业队列中的所有结果（包括正在运行以及等待运行的任务）以及已执行完成的 DDL 作业队列中的最近十条结果。

### 5.1.5 TiDB 是否支持基于 COST 的优化（CBO），如果支持，实现到什么程度？

是的，TiDB 使用的基于成本的优化器（CBO），我们有一个小组单独会对代价模型、统计信息持续优化，除此之外，我们支持 hash join、soft merge 等关联算法。

# 六、数据库优化

## 6.1 TiDB

### 6.1.1 TiDB 参数及调整

详情参考：[https://pingcap.com/docs-cn/sql/server-command-option](https://pingcap.com/docs-cn/sql/server-command-option)

## 6.2 TiKV

### 6.2.1 TiKV 性能参数调优

详情参考：[https://pingcap.com/docs-cn/op-guide/tune-tikv/](https://pingcap.com/docs-cn/op-guide/tune-tikv/)

# 七、监控

## 7.1 Prometheus 监控框架

详细参考：[https://pingcap.com/docs-cn/op-guide/monitor-overview](https://pingcap.com/docs-cn/op-guide/monitor-overview)

## 7.2 监控指标解读

详细参考：[https://pingcap.com/docs-cn/op-guide/dashboard-overview-info](https://pingcap.com/docs-cn/op-guide/dashboard-overview-info)

### 7.2.1 目前的监控使用方式及主要监控指标，有没有更好看的监控？

TiDB 使用 Prometheus + Grafana 组成 TiDB 数据库系统的监控系统，用户在 Grafana 上通过 dashboard 可以监控到 TiDB 的各类运行指标，包括系统资源的监控指标，包括客户端连接与 SQL 运行的指标，包括内部通讯和 Region 调度的指标，通过这些指标，可以让数据库管理员更好的了解到系统的运行状态，运行瓶颈等内容。在监控指标的过程中，我们按照 TiDB 不同的模块，分别列出了各个模块重要的指标项，一般用户只需要关注这些常见的指标项。具体指标请参见 [官方文档](https://pingcap.com/docs-cn/op-guide/dashboard-overview-info/)。

### 7.2.2 Prometheus 监控数据默认 1个月自动清除一次，可以自己设定成2个月或者手动删除吗？

可以的，在 Prometheus 启动的机器上，找到启动脚本，然后修改启动参数，然后重启 Prometheus 生效。

# 八、Cloud TiDB

## 8.1 腾讯云

### 8.1.1 目前 Cloud TiDB 都有那些云厂商？

Cloud TiDB 目前已经在腾讯云、UCloud 上线，都是数据库一级入口，欢迎大家使用。

# 九、故障排除

## 9.1 TiDB 自定义报错汇总

### 9.1.1 ERROR 9001 (HY000) : PD Server Timeout

请求 PD 超时，请检查 PD Server 状态/监控/日志以及 TiDB Server 与 PD Server 之间的网络。

### 9.1.2 ERROR 9002 (HY000) : TiKV Server Timeout

请求 TiKV 超时，请检查 TiKV Server 状态/监控/日志以及 TiDB Server 与 TiKV Server 之间的网络。

### 9.1.3 ERROR 9003 (HY000) : TiKV Server is Busy

TiKV 操作繁忙，一般出现在数据库负载比较高时，请检查 TiKV Server 状态/监控/日志。

### 9.1.4 ERROR 9004 (HY000) : Resolve Lock Timeout

清理锁超时，当数据库上承载的业务存在大量的事务冲突时，会遇到这种错误，请检查业务代码是否有锁争用。

### 9.1.5 ERROR 9005 (HY000) : Region is unavailable

访问的 Region 不可用，某个 Raft Group 不可用，如副本数目不足，出现在 TiKV 比较繁忙或者是 TiKV 节点停机的时候，请检查 TiKV Server 状态/监控/日志。

### 9.1.6 ERROR 9006 (HY000) : GC Too Early

`GC Life Time` 间隔时间过短，长事务本应读到的数据可能被清理了，应增加 `GC Life Time`。

## 9.2 MySQL 原生报错汇总

### 9.2.1 ERROR 2013 (HY000): Lost connection to MySQL server during query 问题的排查方法？

- log 中是否有 panic
- dmesg 中是否有 oom，命令：`dmesg -T | grep -i oom`
- 长时间没有访问，也会收到这个报错，一般是 tcp 超时导致的，tcp 长时间不用, 会被操作系统 kill。

### 9.2.2 ERROR 1105 (HY000): other error: unknown error Wire Error(InvalidEnumValue(4004)) 是什么意思？

这类问题一般是 TiDB 和 TiKV 版本不匹配，在升级过程尽量一起升级，避免版本 mismatch。
