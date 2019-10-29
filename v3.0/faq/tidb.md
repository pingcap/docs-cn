---
title: TiDB FAQ
category: FAQ
aliases: ['/docs-cn/FAQ/','/docs-cn/faq/tidb/']
---

# FAQ

## 一、 TiDB 介绍、架构、原理

### 1.1 TiDB 介绍及整体架构

#### 1.1.1 TiDB 整体架构

[https://pingcap.com/docs-cn/dev/overview/](/v3.0/overview.md#tidb-简介)

#### 1.1.2 TiDB 是什么？

TiDB 是一个分布式 NewSQL 数据库。它支持水平弹性扩展、ACID 事务、标准 SQL、MySQL 语法和 MySQL 协议，具有数据强一致的高可用特性，是一个不仅适合 OLTP 场景还适合 OLAP 场景的混合数据库。

#### 1.1.3 TiDB 是基于 MySQL 开发的吗？

不是，虽然 TiDB 支持 MySQL 语法和协议，但是 TiDB 是由 PingCAP 团队完全自主开发的产品。

#### 1.1.4 TiDB、TiKV、Placement Driver (PD)  主要作用？

- TiDB 是 Server 计算层，主要负责 SQL 的解析、制定查询计划、生成执行器。
- TiKV 是分布式 Key-Value 存储引擎，用来存储真正的数据，简而言之，TiKV 是 TiDB 的存储引擎。
- PD 是 TiDB 集群的管理组件，负责存储 TiKV 的元数据，同时也负责分配时间戳以及对 TiKV 做负载均衡调度。

#### 1.1.5 TiDB 易用性如何？

TiDB 使用起来很简单，可以将 TiDB 集群当成 MySQL 来用，你可以将 TiDB 用在任何以 MySQL 作为后台存储服务的应用中，并且基本上不需要修改应用代码，同时你可以用大部分流行的 MySQL 管理工具来管理 TiDB。

#### 1.1.6 TiDB 和 MySQL 兼容性如何？

TiDB 目前还不支持触发器、存储过程、自定义函数、外键，除此之外，TiDB 支持绝大部分 MySQL 5.7 的语法。

详情参见[与 MySQL 兼容性对比](/v3.0/reference/mysql-compatibility.md)。

#### 1.1.7 TiDB 具备高可用的特性吗？

TiDB 天然具备高可用特性，TiDB、TiKV、PD 这三个组件都能容忍部分实例失效，不影响整个集群的可用性。具体见 [TiDB 高可用性](/v3.0/key-features.md#高可用)。

#### 1.1.8 TiDB 数据是强一致的吗？

TiDB 实现了快照隔离 (Snapshot Isolation) 级别的一致性。为与 MySQL 保持一致，又称其为“可重复读”。通过使用 [Raft 一致性算法](https://raft.github.io/)，数据在各 TiKV 节点间复制为多副本，以确保某个节点挂掉时数据的安全性。

在底层，TiKV 使用复制日志 + 状态机 (State Machine) 的模型来复制数据。对于写入请求，数据被写入 Leader，然后 Leader 以日志的形式将命令复制到它的 Follower 中。当集群中的大多数节点收到此日志时，日志会被提交，状态机会相应作出变更。

#### 1.1.9 TiDB 支持分布式事务吗？

支持。无论是一个地方的几个节点，还是[跨多个数据中心的多个节点](/v3.0/how-to/deploy/geographic-redundancy/overview.md)，TiDB 均支持 ACID 分布式事务。

TiDB 事务模型灵感源自 Google Percolator 模型，主体是一个两阶段提交协议，并进行了一些实用的优化。该模型依赖于一个时间戳分配器，为每个事务分配单调递增的时间戳，这样就检测到事务冲突。在 TiDB 集群中，[PD](/v3.0/architecture.md#pd-server) 承担时间戳分配器的角色。

#### 1.1.10 TiDB 支持哪些编程语言？

只要支持 MySQL Client/Driver 的编程语言，都可以直接使用 TiDB。

#### 1.1.11 TiDB 是否支持其他存储引擎？

是的，除了 TiKV 之外，TiDB 还支持一些流行的单机存储引擎，比如 GolevelDB、RocksDB、BoltDB 等。如果一个存储引擎是支持事务的 KV 引擎，并且能提供一个满足 TiDB 接口要求的 Client，即可接入 TiDB。

#### 1.1.12 官方有没有三中心跨机房多活部署的推荐方案？

从 TiDB 架构来讲，支持真正意义上的跨中心异地多活，从操作层面讲，依赖数据中心之间的网络延迟和稳定性，一般建议延迟在 5ms 以下，目前我们已经有相似客户方案，具体请咨询官方 [info@pingcap.com](mailto:info@pingcap.com)。

#### 1.1.13 除了官方文档，有没有其他 TiDB 知识获取途径？

目前[官方文档](/v3.0/overview.md#tidb-简介)是获取 TiDB 相关知识最主要、最及时的发布途径。除此之外，我们也有一些技术沟通群，如有需求可发邮件至 [info@pingcap.com](mailto:info@pingcap.com) 获取。

#### 1.1.14 TiDB 对哪些 MySQL variables 兼容？

详细可参考[系统变量](/v3.0/reference/configuration/tidb-server/mysql-variables.md)。

#### 1.1.15 TiDB 是否支持 select for update？

支持，但语义上和 MySQL 有区别，TiDB 是分布式数据库，采用的乐观锁机制，也就说 select for update 不在事务开启就锁住数据，而是其他事务在提交的时候进行冲突检查，如有冲突，会进行回滚。

#### 1.1.16 TiDB 的 codec 能保证 UTF8 的字符串是 memcomparable 的吗？我们的 key 需要支持 UTF8，有什么编码建议吗？

TiDB 字符集默认就是 UTF8 而且目前只支持 UTF8，字符串就是 memcomparable 格式的。

#### 1.1.17 TiDB 用户名长度限制？

在 TiDB 中用户名最长为 32 字符。

#### 1.1.18 一个事务中的语句数量最大是多少？

一个事务中的语句数量，默认限制最大为 5000 条。

#### 1.1.19 TiDB 是否支持 XA？

虽然 TiDB 的 JDBC 驱动用的就是 MySQL JDBC（Connector / J），但是当使用 Atomikos 的时候，数据源要配置成类似这样的配置：`type="com.mysql.jdbc.jdbc2.optional.MysqlXADataSource"`。MySQL JDBC XADataSource 连接 TiDB 的模式目前是不支持的。MySQL JDBC 中配置好的 XADataSource 模式，只对 MySQL 数据库起作用（DML 去修改 redo 等）。

Atomikos 配好两个数据源后，JDBC 驱动都要设置成 XA 模式，然后 Atomikos 在操作 TM 和 RM（DB）的时候，会通过数据源的配置，发起带有 XA 指令到 JDBC 层，JDBC 层 XA 模式启用的情况下，会对 InnoDB（如果是 MySQL 的话）下发操作一连串 XA 逻辑的动作，包括 DML 去变更 redo log 等，就是两阶段递交的那些操作。TiDB 目前的引擎版本中，没有对上层应用层 JTA / XA 的支持，不解析这些 Atomikos 发过来的 XA 类型的操作。

MySQL 是单机数据库，只能通过 XA 来满足跨数据库事务，而 TiDB 本身就通过 Google 的 Percolator 事务模型支持分布式事务，性能稳定性比 XA 要高出很多，所以不会也不需要支持 XA。

#### 1.1.20 show processlist 是否显示系统进程号？

TiDB 的 `show processlist` 与 MySQL 的 `show processlist` 显示内容基本一样，不会显示系统进程号，而 ID 表示当前的 session ID。其中 TiDB 的 `show processlist` 和 MySQL 的 `show processlist` 区别如下：

1）由于 TiDB 是分布式数据库，tidb-server 实例是无状态的 SQL 解析和执行引擎（详情可参考 [TiDB 整体架构](/v3.0/overview.md#tidb-整体架构)），用户使用 MySQL 客户端登录的是哪个 tidb-server，`show processlist` 就会显示当前连接的这个 tidb-server 中执行的 session 列表，不是整个集群中运行的全部 session 列表；而 MySQL 是单机数据库，`show processlist` 列出的是当前整个 MySQL 数据库的全部执行 SQL 列表。

2）TiDB 的 `show processlist` 显示内容比起 MySQL 来讲，多了一个当前 session 使用内存的估算值（单位 Byte）。

#### 1.1.21 如何修改用户名密码和权限？

TiDB 作为分布式数据库，在 TiDB 中修改用户密码建议使用 `set password for 'root'@'%' = '0101001';` 或 `alter` 方法，不推荐使用 `update mysql.user` 的方法进行，这种方法可能会造成其它节点刷新不及时的情况。修改权限也一样，都建议采用官方的标准语法。详情可参考 [TiDB 用户账户管理](/v3.0/reference/security/user-account-management.md)。

#### 1.1.22 TiDB 中，为什么出现后插入数据的自增 ID 反而小？

TiDB 的自增 ID (`AUTO_INCREMENT`) 只保证自增且唯一，并不保证连续分配。TiDB 目前采用批量分配的方式，所以如果在多台 TiDB 上同时插入数据，分配的自增 ID 会不连续。当多个线程并发往不同的 tidb-server 插入数据的时候，有可能会出现后插入的数据自增 ID 小的情况。此外，TiDB允许给整型类型的字段指定 AUTO_INCREMENT，且一个表只允许一个属性为 `AUTO_INCREMENT` 的字段。详情可参考[CREATE TABLE 语法](/v3.0/reference/mysql-compatibility.md#自增-id)。

#### 1.1.23 sql_mode 默认除了通过命令 set 修改，配置文件怎么修改？

TiDB 的 sql_mode 与 MySQL 的 sql_mode 设置方法有一些差别，TiDB 不支持配置文件配置设置数据库的 sql\_mode，而只能使用 set 命令去设置，具体方法为：`set @@global.sql_mode = 'STRICT_TRANS_TABLES';`。

#### 1.1.24 TiDB 支持哪些认证协议，过程是怎样的？

这一层跟 MySQL 一样，走的 SASL 认证协议，用于用户登录认证，对密码的处理流程。

客户端连接 TiDB 的时候，走的是 challenge-response（挑战-应答）的认证模式，过程如下：

第一步：客户端连接服务器；

第二步：服务器发送随机字符串 challenge 给客户端；

第三步：客户端发送 username + response 给服务器；

第四步：服务器验证 response。

### 1.2 TiDB 原理

#### 1.2.1 存储 TiKV

##### 1.2.1.1 TiKV 详细解读

[http://t.cn/RTKRRWv](http://t.cn/RTKRRWv)

#### 1.2.2 计算 TiDB

##### 1.2.2.1 TiDB 详细解读

[http://t.cn/RTKRkBh](http://t.cn/RTKRkBh)

#### 1.2.3 调度 PD

##### 1.2.3.1 PD 详细解读

[http://t.cn/RTKEZ0U](http://t.cn/RTKEZ0U)

## 二、安装部署升级

### 2.1 环境准备

#### 2.1.1 操作系统版本要求

| **Linux 操作系统平台** | **版本** |
| --- | --- |
| Red Hat Enterprise Linux | 7.3 及以上 |
| CentOS | 7.3 及以上 |
| Oracle Enterprise Linux | 7.3 及以上 |

##### 2.1.1.1  为什么要在 CentOS 7 上部署 TiDB 集群？

TiDB 作为一款开源分布式 NewSQL 数据库，可以很好的部署和运行在 Intel 架构服务器环境及主流虚拟化环境，并支持绝大多数的主流硬件网络，作为一款高性能数据库系统，TiDB 支持主流的 Linux 操作系统环境，具体可以参考 TiDB 的[官方部署要求](/v3.0/how-to/deploy/hardware-recommendations.md)。其中 TiDB 在 CentOS 7.3 的环境下进行大量的测试，同时也有很多这个操作系统的部署最佳实践，因此，我们推荐客户在部署 TiDB 的时候使用 CentOS 7.3+ 以上的Linux 操作系统。

#### 2.1.2 硬件要求

TiDB 支持部署和运行在 Intel x86-64 架构的 64 位通用硬件服务器平台。对于开发，测试，及生产环境的服务器硬件配置有以下要求和建议：

##### 2.1.2.1 开发及测试环境

| **组件** | **CPU** | **内存** | **本地存储** | **网络** | **实例数量(最低要求)** |
| --- | --- | --- | --- | --- | --- |
| TiDB | 8核+ | 16 GB+ | SAS, 200 GB+ | 千兆网卡 | 1（可与 PD 同机器） |
| PD | 8核+ | 16 GB+ | SAS, 200 GB+ | 千兆网卡 | 1（可与 TiDB 同机器） |
| TiKV | 8核+ | 32 GB+ | SSD, 200 GB+ | 千兆网卡 | 3 |
|   |   |   |   | 服务器总计 | 4 |

##### 2.1.2.2 线上环境

| **组件** | **CPU** | **内存** | **硬盘类型** | **网络** | **实例数量(最低要求)** |
| --- | --- | --- | --- | --- | --- |
| TiDB | 16核+ | 48 GB+ | SAS | 万兆网卡（2块最佳） | 2 |
| PD | 8核+ | 16 GB+ | SSD | 万兆网卡（2块最佳） | 3 |
| TiKV | 16核+ | 48 GB+ | SSD | 万兆网卡（2块最佳） | 3 |
| 监控 | 8核+ | 16 GB+ | SAS | 千兆网卡 | 1 |
|   |   |   |   | 服务器总计 | 9 |

##### 2.1.2.3 2 块网卡的目的是？万兆的目的是？

作为一个分布式集群，TiDB 对时间的要求还是比较高的，尤其是 PD 需要分发唯一的时间戳，如果 PD 时间不统一，如果有 PD 切换，将会等待更长的时间。2 块网卡可以做 bond，保证数据传输的稳定，万兆可以保证数据传输的速度，千兆网卡容易出现瓶颈，我们强烈建议使用万兆网卡。

##### 2.1.2.4 SSD 不做 RAID 是否可行？

资源可接受的话，我们建议做 RAID 10，如果资源有限，也可以不做 RAID。

##### 2.1.2.5 TiDB 集群各个组件的配置推荐？

- TiDB 需要 CPU 和内存比较好的机器，参考官网配置要求，如果后期需要开启 Binlog，根据业务量的评估和 GC 时间的要求，也需要本地磁盘大一点，不要求 SSD 磁盘；
- PD 里面存了集群元信息，会有频繁的读写请求，对磁盘 I/O 要求相对比较高，磁盘太差会影响整个集群性能，推荐 SSD 磁盘，空间不用太大。另外集群 Region 数量越多对 CPU、内存的要求越高；
- TiKV 对 CPU、内存、磁盘要求都比较高，一定要用 SSD 磁盘。

详情可参考 [TiDB 软硬件环境需求](/v3.0/how-to/deploy/hardware-recommendations.md)。

### 2.2 安装部署

#### 2.2.1 Ansible 部署方式（强烈推荐）

详细可参考[使用 TiDB Ansible 部署 TiDB 集群](/v3.0/how-to/deploy/orchestrated/ansible.md)。

##### 2.2.1.1 为什么修改了 TiKV/PD 的 toml 配置文件，却没有生效？

这种情况一般是因为没有使用 `--config` 参数来指定配置文件（目前只会出现在 binary 部署的场景），TiKV/PD 会按默认值来设置。如果要使用配置文件，请设置 TiKV/PD 的 `--config` 参数。对于 TiKV 组件，修改配置后重启服务即可；对于 PD 组件，只会在第一次启动时读取配置文件，之后可以使用 pd-ctl 的方式来修改配置，详情可参考[这里](/v3.0/reference/configuration/pd-server/configuration.md)。

##### 2.2.1.2 TiDB 监控框架 Prometheus + Grafana 监控机器建议单独还是多台部署？

监控机建议单独部署。建议 CPU 8 core，内存 16 GB 以上，硬盘 500 GB 以上。

##### 2.2.1.3 有一部分监控信息显示不出来？

查看访问监控的机器时间跟集群内机器的时间差，如果比较大，更正时间后即可显示正常。

##### 2.2.1.4 supervise/svc/svstat 服务具体起什么作用？

- supervise 守护进程
- svc 启停服务
- svstat 查看进程状态

##### 2.2.1.5 inventory.ini 变量参数解读

| **变量** | **含义** |
| --- | --- |
| cluster_name | 集群名称，可调整 |
| tidb_version | TiDB 版本，TiDB Ansible 各分支默认已配置 |
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

#### 2.2.2 TiDB 离线 Ansible 部署方案

首先这不是我们建议的方式，如果中控机没有外网，也可以通过离线 Ansible 部署方式，详情可参考[这里](/v3.0/how-to/deploy/orchestrated/offline-ansible.md)。

#### 2.2.3 Docker Compose 快速构建集群（单机部署）

使用 docker-compose 在本地一键拉起一个集群，包括集群监控，还可以根据需求自定义各个组件的软件版本和实例个数，以及自定义配置文件，这种只限于开发环境，详细可参考[官方文档](/v3.0/how-to/get-started/deploy-tidb-from-docker-compose.md)。

#### 2.2.4 如何单独记录 TiDB 中的慢查询日志，如何定位慢查询 SQL？

1）TiDB 中，对慢查询的定义在 tidb-ansible 的 `conf/tidb.yml` 配置文件中，`slow-threshold: 300`，这个参数是配置慢查询记录阈值的，单位是 ms。

慢查询日志默认记录到 tidb.log 中，如果希望生成单独的慢查询日志文件，修改 inventory.ini 配置文件的参数 `enable_slow_query_log` 为 True。

如上配置修改之后，需要执行 `ansible-playbook rolling_update.yml --tags=tidb`，对 tidb-server 实例进行滚动升级，升级完成后，tidb-server 将在 `tidb_slow_query.log`
文件中记录慢查询日志。

2）如果出现了慢查询，可以从 Grafana 监控定位到出现慢查询的 tidb-server 以及时间点，然后在对应节点查找日志中记录的 SQL 信息。

3）除了日志，还可以通过 `admin show slow` 命令查看，详情可参考 [`admin show slow` 命令](/v3.0/how-to/maintain/identify-slow-queries.md#admin-show-slow-命令)。

#### 2.2.5 首次部署 TiDB 集群时，没有配置 tikv 的 Label 信息，在后续如何添加配置 Label？

TiDB 的 Label 设置是与集群的部署架构相关的，是集群部署中的重要内容，是 PD 进行全局管理和调度的依据。如果集群在初期部署过程中没有设置 Label，需要在后期对部署结构进行调整，就需要手动通过 PD 的管理工具 pd-ctl 来添加 location-labels 信息，例如：`config set location-labels "zone, rack, host"`（根据实际的 label 层级名字配置）。

pd-ctl 的使用参考 [PD Control 使用说明](/v3.0/reference/tools/pd-control.md)。

#### 2.2.6 为什么测试磁盘的 dd 命令用 oflag=direct 这个选项？

Direct 模式就是把写入请求直接封装成 I/O 指令发到磁盘，这样是为了绕开文件系统的缓存，可以直接测试磁盘的真实的 I/O 读写能力。

#### 2.2.7 如何用 fio 命令测试 TiKV 实例的磁盘性能？

- 随机读测试：

    {{< copyable "shell-regular" >}}

    ```bash
    ./fio -ioengine=psync -bs=32k -fdatasync=1 -thread -rw=randread -size=10G -filename=fio_randread_test.txt -name='fio randread test' -iodepth=4 -runtime=60 -numjobs=4 -group_reporting --output-format=json --output=fio_randread_result.json
    ```

- 顺序写和随机读混合测试：

    {{< copyable "shell-regular" >}}

    ```bash
    ./fio -ioengine=psync -bs=32k -fdatasync=1 -thread -rw=randrw -percentage_random=100,0 -size=10G -filename=fio_randread_write_test.txt -name='fio mixed randread and sequential write test' -iodepth=4 -runtime=60 -numjobs=4 -group_reporting --output-format=json --output=fio_randread_write_test.json
    ```

#### 2.2.8 使用 TiDB Ansible 部署 TiDB 集群的时候，遇到 `UNREACHABLE! "msg": "Failed to connect to the host via ssh: "` 报错是什么原因？

有两种可能性：

- ssh 互信的准备工作未做好，建议严格参照我们的[官方文档步骤](/v3.0/how-to/deploy/orchestrated/ansible.md)配置互信，并使用命令 `ansible -i inventory.ini all -m shell -a 'whoami' -b` 来验证互信配置是否成功。

- 如果涉及到单服务器分配了多角色的场景，例如多组件混合部署或单台服务器部署了多个 TiKV 实例，可能是由于 ssh 复用的机制引起这个报错，可以使用 `ansible … -f 1` 的选项来规避这个报错。

### 2.3 升级

#### 2.3.1 如何使用 Ansible 滚动升级？

滚动升级 TiKV 节点( 只升级单独服务 )

`ansible-playbook rolling_update.yml --tags=tikv`

滚动升级所有服务

`ansible-playbook rolling_update.yml`

#### 2.3.2 滚动升级有那些影响?

滚动升级 TiDB 服务，滚动升级期间不影响业务运行，需要配置最小集群拓扑（TiDB \* 2、PD \* 3、TiKV \* 3），如果集群环境中有 Pump/Drainer 服务，建议先停止 Drainer 后滚动升级（升级 TiDB 时会升级 Pump）。

#### 2.3.3 Binary 如何升级？

Binary 不是我们建议的安装方式，对升级支持也不友好，建议换成 Ansible 部署。

#### 2.3.4 一般升级选择升级 TiKV 还是所有组件都升级？

常规需要一起升，因为整个版本都是一起测试的，单独升级只限当发生一个紧急故障时，需要单独对一个有问题的角色做升级。

#### 2.3.5 启动集群或者升级集群过程中出现 “Timeout when waiting for search string 200 OK” 是什么原因？如何处理？

可能有以下几种原因：进程没有正常启动；端口被占用；进程没有正常停掉；停掉集群的情况下使用 rolling_update.yml 来升级集群（操作错误）。

处理方式：登录到相应节点查看进程或者端口的状态；纠正错误的操作步骤。

## 三、集群管理

### 3.1 集群日常管理

#### 3.1.1 Ansible 常见运维操作有那些？

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

#### 3.1.2 TiDB 如何登录？

和 MySQL 登录方式一样，可以按照下面例子进行登录。

`mysql -h 127.0.0.1 -uroot -P4000`

#### 3.1.3 TiDB 如何修改数据库系统变量？

和 MySQL 一样，TiDB 也分为静态参数和固态参数，静态参数可以直接通过`set global xxx = n`的方式进行修改，不过新参数值只限于该实例生命周期有效。

#### 3.1.4 TiDB (TiKV) 有哪些数据目录？

默认在 [`--data-dir`](/v3.0/reference/configuration/tikv-server/configuration.md#--data-dir) 目录下，其中包括 backup、db、raft、snap 四个目录，分别存储备份、数据、raft 数据及镜像数据。

#### 3.1.5 TiDB 有哪些系统表？

和 MySQL 类似，TiDB 中也有系统表，用于存放数据库运行时所需信息，具体信息参考 [TiDB 系统数据库](/v3.0/reference/system-databases/mysql.md)文档。

#### 3.1.6 TiDB 各节点服务器下是否有日志文件，如何管理？

默认情况下各节点服务器会在日志中输出标准错误，如果启动的时候通过 `--log-file` 参数指定了日志文件，那么日志会输出到指定的文件中，并且按天做 rotation。

#### 3.1.7 如何规范停止 TiDB？

如果是用 Ansible 部署的，可以使用 `ansible-playbook stop.yml` 命令停止 TiDB 集群。如果不是 Ansible 部署的，可以直接 kill 掉所有服务。如果使用 kill 命令，TiDB 的组件会做 graceful 的 shutdown。

#### 3.1.8 TiDB 里面可以执行 kill 命令吗？

- 可以 kill DML 语句，首先使用 `show processlist`，找到对应 session 的 id，然后执行 `kill tidb [session id]`。
- 可以 kill DDL 语句，首先使用 `admin show ddl jobs`，查找需要 kill 的 DDL job ID，然后执行 `admin cancel ddl jobs 'job_id' [, 'job_id'] ...`。具体可以参考 [admin 操作](/v3.0/reference/sql/statements/admin.md)。

#### 3.1.9 TiDB 是否支持会话超时？

TiDB 暂不支持数据库层面的会话超时，目前想要实现超时，在没 LB（Load Balancing）的时候，需要应用侧记录发起的 Session 的 ID，通过应用自定义超时，超时以后需要到发起 Query 的节点上用 `kill tidb [session id]` 来杀掉 SQL。目前建议使用应用程序来实现会话超时，当达到超时时间，应用层就会抛出异常继续执行后续的程序段。

#### 3.1.10 TiDB 生产环境的版本管理策略是怎么样的？如何尽可能避免频繁升级？

TiDB 版本目前逐步标准化，每次 Release 都包含详细的 Change log，版本功能[变化详情](https://github.com/pingcap/TiDB/releases)，生产环境是否有必要升级取决于业务系统，建议升级之前详细了解前后版本的功能差异。

版本号说明参考：Release Version: `v1.0.3-1-ga80e796`

- `v1.0.3` 表示 GA 标准版
- `1` 表示该版本 commit 1 次
- `ga80e796` 代表版本的 `git-hash`

#### 3.1.11 分不清 TiDB master 版本之间的区别，经常用错 TiDB Ansible 版本?

TiDB 目前社区非常活跃，在 1.0 GA 版本发布后，还在不断的优化和修改 BUG，因此 TiDB 的版本更新周期比较快，会不定期有新版本发布，请关注我们的[新版本发布官方网站](https://pingcap.com/weekly/)。此外 TiDB 安装推荐使用 TiDB Ansible 进行安装，TiDB Ansible 的版本也会随着 TiDB 的版本发布进行更新，因此建议用户在安装升级新版本的时候使用最新的 TiDB Ansible 安装包版本进行安装。此外，在 TiDB 1.0 GA 版本后，对 TiDB 的版本号进行了统一管理，TiDB 的版本可以通过以下两种方式进行查看：

- 通过 `select tidb_version()` 进行查看
- 通过执行 `tidb-server -V` 进行查看

#### 3.1.12 有没有图形化部署 TiDB 的工具？

暂时没有。

#### 3.1.13 TiDB 如何进行水平扩展？

当您的业务不断增长时，数据库可能会面临三方面瓶颈，第一是存储空间，第二是计算资源，第三是读写容量，这时可以对 TiDB 集群做水平扩展。

- 如果是存储资源不够，可以通过添加 TiKV Server 节点来解决，新节点启动后，PD 会自动将其他节点的部分数据迁移过去，无需人工介入。
- 如果是计算资源不够，可以查看 TiDB Server 和 TiKV Server 节点的 CPU 消耗情况，再考虑添加 TiDB Server 节点或者是 TiKV Server 节点来解决，如添加 TiDB Server 节点，将其添加到前端 Load Balancer 配置之中即可。
- 如果是容量跟不上，一般可以考虑同时增加 TiDB Server 和 TiKV Server 节点。

#### 3.1.14 Percolator 用了分布式锁，crash 的客户端会保持锁，会造成锁没有 release？

详细可参考 [https://pingcap.com/blog-cn/percolator-and-txn/](https://pingcap.com/blog-cn/percolator-and-txn/)。

#### 3.1.15 TiDB 为什么选用 gRPC 而不选用 Thrift，是因为 Google 在用吗？

不只是因为 Google 在用，有一些比较好的特性我们需要，比如流控、加密还有 Streaming。

#### 3.1.16 like(bindo.customers.name, jason%, 92) 这个92代表什么？

那个是转义字符，默认是 (ASCII 92)。

#### 3.1.17 为什么 `information_schema.tables.data_length` 记录的大小和 TiKV 监控面板上的 store size 不一样？

这是因为两者计算的角度不一样。`information_schema.tables.data_length` 是通过统计信息（平均每行的大小）得到的估算值。TiKV 监控面板上的 store size 是单个 TiKV 实例的数据文件（RocksDB 的 SST 文件）的大小总和。由于多版本和 TiKV 会压缩数据，所以两者显示的大小不一样。

### 3.2 PD 管理

#### 3.2.1 访问 PD 报错：TiKV cluster is not bootstrapped

PD 的大部分 API 需要在初始化 TiKV 集群以后才能使用，如果在部署新集群的时候只启动了 PD，还没有启动 TiKV，这时候访问 PD 就会报这个错误。遇到这个错误应该先把要部署的 TiKV 启动起来，TiKV 会自动完成初始化工作，然后就可以正常访问 PD。

#### 3.2.2 PD 启动报错：etcd cluster ID mismatch

PD 启动参数中的 `--initial-cluster` 包含了某个不属于该集群的成员。遇到这个错误时请检查各个成员的所属集群，剔除错误的成员后即可正常启动。

#### 3.2.3 PD 能容忍的时间同步误差是多少？

理论上，时间同步误差越小越好。PD 可容忍任意时长的误差，但是，时间同步误差越大意味着 PD 分配的时间戳与真实的物理时间相差越大，这个差距会影响读历史版本等功能。

#### 3.2.4 Client 连接是如何寻找 PD 的？

Client 连接只能通过 TiDB 访问集群，TiDB 负责连接 PD 与 TiKV，PD 与 TiKV 对 Client 透明。当 TiDB 连接任意一台 PD 的时候，PD 会告知 TiDB 当前的 leader 是谁，如果此台 PD 不是 leader，TiDB 将会重新连接至 leader PD。

#### 3.2.5 PD 参数中 leader-schedule-limit 和 region-schedule-limit 调度有什么区别？

- leader-schedule-limit 调度是用来均衡不同 TiKV 的 leader 数，影响处理查询的负载。
- region-schedule-limit 调度是均衡不同 TiKV 的副本数，影响不同节点的数据量。

#### 3.2.6 每个 region 的 replica 数量可配置吗？调整的方法是？

可以，目前只能调整全局的 replica 数量。首次启动时 PD 会读配置文件（conf/pd.yml），使用其中的 max-replicas 配置，之后修改需要使用 pd-ctl 配置命令 `config set max-replicas $num`，配置后可通过 `config show all` 来查看已生效的配置。调整的时候，不会影响业务，会在后台添加，注意总 TiKV 实例数总是要大于等于设置的副本数，例如 3 副本需要至少 3 个 TiKV。增加副本数量之前需要预估额外的存储需求。pd-ctl 的详细用法可参考 [PD Control 使用说明](/v3.0/reference/tools/pd-control.md)。

#### 3.2.7 缺少命令行集群管理工具，整个集群的健康度当前是否正常，不好确认？

可以通过 pd-ctl 等工具来判断集群大概的状态，详细的集群状态还是需要通过监控来确认。

#### 3.2.8 集群下线节点后，怎么删除老集群节点监控信息？

下线节点一般指 TiKV 节点通过 pd-ctl 或者监控判断节点是否下线完成。节点下线完成后，手动停止下线节点上相关的服务。从 Prometheus 配置文件中删除对应节点的 node_exporter 信息。从 Ansible inventory.ini 中删除对应节点的信息。

#### 3.2.9 使用 PD Control 连接 PD Server 时，为什么只能通过本机 IP 连接，不能通过 127.0.0.1 连接？

因为使用 TiDB Ansible 部署的集群，PD 对外服务端口不会绑定到 127.0.0.1，所以 PD Control 不会识别 127.0.0.1。

### 3.3 TiDB server 管理

#### 3.3.1 TiDB 的 lease 参数应该如何设置？

启动 TiDB Server 时，需要通过命令行参数设置 lease 参数（--lease=60），其值会影响 DDL 的速度（只会影响当前执行 DDL 的 session，其他的 session 不会受影响）。在测试阶段，lease 的值可以设为 1s，加快测试进度；在生产环境下，我们推荐这个值设为分钟级（一般可以设为 60），这样可以保证 DDL 操作的安全。

#### 3.3.2 DDL 在正常情况下的耗时是多少？

一般情况下处理一个 DDL 操作（之前没有其他 DDL 操作在处理）的耗时基本可以分如下为三种：

- add index 操作，且此操作对应表数据行数比较少，耗时约为 3s。
- add index 操作，且此操作对应表数据行数比较多，耗时具体由表中数据行数和当时 QPS 情况定（add index 操作优先级比一般 SQL 低）。
- 其他 DDL 操作耗时约为 1s。

此外，如果接收 DDL 请求的 TiDB 和 DDL owner 所处的 TiDB 是一台，那么上面列举的第一和第三种可能的耗时应该在几十到几百毫秒。

#### 3.3.3 为什么有的时候执行 DDL 会很慢？

可能原因如下：

- 多个 DDL 语句一起执行的时候，后面的几个 DDL 语句会比较慢。原因是当前 TiDB 集群中 DDL 操作是串行执行的。
- 在正常集群启动后，第一个 DDL 操作的执行时间可能会比较久，一般在 30s 左右，这个原因是刚启动时 TiDB 在竞选处理 DDL 的 leader。
- 由于停 TiDB 时不能与 PD 正常通信（包括停电情况）或者用 `kill -9` 指令停 TiDB 导致 TiDB 没有及时从 PD 清理注册数据，那么会影响 TiDB 启动后 10min 内的 DDL 语句处理时间。这段时间内运行 DDL 语句时，每个 DDL 状态变化都需要等待 2 * lease（默认 lease = 45s）。
- 当集群中某个 TiDB 与 PD 之间发生通信问题，即 TiDB 不能从 PD 及时获取或更新版本信息，那么这时候 DDL 操作的每个状态处理需要等待 2 * lease。

#### 3.3.4 TiDB 可以使用 S3 作为后端存储吗？

不可以，目前 TiDB 只支持分布式存储引擎和 GolevelDB/RocksDB/BoltDB 引擎。

#### 3.3.5 Information_schema 能否支持更多真实信息？

Information_schema 库里面的表主要是为了兼容 MySQL 而存在，有些第三方软件会查询里面的信息。在目前 TiDB 的实现中，里面大部分只是一些空表。后续随着 TiDB 的升级，会提供更多的参数信息。当前 TiDB 支持的 Information\_schema 请参考 [TiDB 系统数据库说明文档](/v3.0/reference/system-databases/information-schema.md)。

#### 3.3.6 TiDB Backoff type 主要原因?

TiDB-server 与 TiKV-server 随时进行通信，在进行大量数据操作过程中，会出现 `Server is busy` 或者 `backoff.maxsleep 20000ms` 的日志提示信息，这是由于 TiKV-server 在处理过程中系统比较忙而出现的提示信息，通常这时候可以通过系统资源监控到 TiKV 主机系统资源使用率比较高的情况出现。如果这种情况出现，可以根据资源使用情况进行相应的扩容操作。

#### 3.3.7 TiDB TiClient type 主要原因？

TiClient Region Error 该指标描述的是在 TiDB-server 作为客户端通过 KV 接口访问 TiKV-server 进行数据操作过程中，TiDB-server 操作 TiKV-server 中的 Region 数据出现的错误类型与 metric 指标，错误类型包括 not_leader、stale_epoch。出现这些错误的情况是当 TiDB-server 根据自己的缓存信息去操作 Region leader 数据的时候，Region leader 发生了迁移或者 TiKV 当前的 Region 信息与 TiDB 缓存的路由信息不一致而出现的错误提示。一般这种情况下，TiDB-server 都会自动重新从 PD 获取最新的路由数据，重做之前的操作。

#### 3.3.8 TiDB 同时支持的最大并发连接数？

当前版本 TiDB 没有最大连接数的限制，如果并发过大导致响应时间增加，可以通过增加 TiDB 节点进行扩容。

#### 3.3.9 如何查看某张表创建的时间？

information_schema 库中的 tables 表里的 create_time 即为表的真实创建时间。

#### 3.3.9 TiDB 的日志中 EXPENSIVE_QUERY 是什么意思？

TiDB 在执行 SQL 时，预估出来每个 operator 处理了超过 10000 条数据就认为这条 query 是 expensive query。可以通过修改 tidb-server 配置参数来对这个门限值进行调整，调整后需要重新启动 tidb-server。

#### 3.3.10 在 TiDB 中如何控制或改变 SQL 提交的执行优先级？

TiDB 支持改变 [per-session](/v3.0/reference/configuration/tidb-server/tidb-specific-variables.md#tidb_force_priority)、[全局](/v3.0/reference/configuration/tidb-server/configuration-file.md#force-priority)或单个语句的优先级。优先级包括：

- HIGH_PRIORITY：该语句为高优先级语句，TiDB 在执行阶段会优先处理这条语句
- LOW_PRIORITY：该语句为低优先级语句，TiDB 在执行阶段会降低这条语句的优先级

以上两种参数可以结合 TiDB 的 DML 语言进行使用，使用方法举例如下：

1. 通过在数据库中写 SQL 的方式来调整优先级：

    {{< copyable "sql" >}}

    ```sql
    select HIGH_PRIORITY | LOW_PRIORITY count(*) from table_name;
    insert HIGH_PRIORITY | LOW_PRIORITY into table_name insert_values;
    delete HIGH_PRIORITY | LOW_PRIORITY from table_name;
    update HIGH_PRIORITY | LOW_PRIORITY table_reference set assignment_list where where_condition;
    replace HIGH_PRIORITY | LOW_PRIORITY into table_name;
    ```

2. 全表扫会自动调整为低优先级，analyze 也是默认低优先级。

#### 3.3.11 在 TiDB 中 auto analyze 的触发策略是怎样的？

触发策略：新表达到 1000 条，并且在 1 分钟内没有写入，会自动触发。

当表的（修改数/当前总行数）大于 `tidb_auto_analyze_ratio` 的时候，会自动触发 `analyze` 语句。`tidb_auto_analyze_ratio` 的默认值为 0.5，即默认开启此功能。为了保险起见，在开启此功能的时候，保证了其最小值为 0.3。但是不能大于等于 `pseudo-estimate-ratio`（默认值为 0.8），否则会有一段时间使用 pseudo 统计信息，建议设置值为 0.5。

#### 3.3.12 SQL 中如何通过 hint 使用一个具体的 index？

同 MySQL 的用法一致，例如：
`select column_name from table_name use index（index_name）where where_condition;`

#### 3.3.13 触发 Information schema is changed 错误的原因？

TiDB 在执行 SQL 语句时，会使用当时的 `schema` 来处理该 SQL 语句，而且 TiDB 支持在线异步变更 DDL。那么，在执行 DML 的时候可能有 DDL 语句也在执行，而你需要确保每个 SQL 语句在同一个 `schema` 上执行。所以当执行 DML 时，遇到正在执行中的 DDL 操作就可能会报 `Information schema is changed` 的错误。为了避免太多的 DML 语句报错，已做了一些优化。

现在会报此错的可能原因如下（后两个报错原因与表无关）：

- 执行的 DML 语句中涉及的表和集群中正在执行的 DDL 的表有相同的，那么这个 DML 语句就会报此错。
- 这个 DML 执行时间很久，而这段时间内执行了很多 DDL 语句，导致中间 `schema` 版本变更次数超过 1024（v3.0.5 版本之前此值为定值 100。v3.0.5 及之后版本默认值为 1024，可以通过 `tidb_max_delta_schema_count` 变量修改）。
- 接受 DML 请求的 TiDB 长时间不能加载到 `schema information`（TiDB 与 PD 或 TiKV 之间的网络连接故障等会导致此问题），而这段时间内执行了很多 DDL 语句，导致中间 `schema` 版本变更次数超过 100。

> **注意：**
>
> + 目前 TiDB 未缓存所有的 `schema` 版本信息。
> + 对于每个 DDL 操作，`schema` 版本变更的数量与对应 `schema state` 变更的次数一致。
> + 不同的 DDL 操作版本变更次数不一样。例如，`create table` 操作会有 1 次 `schema` 版本变更；`add column` 操作有 4 次 `schema` 版本变更。

#### 3.3.14 触发 Information schema is out of date 错误的原因？

当执行 DML 时，TiDB 超过一个 DDL lease 时间（默认 45s）没能加载到最新的 schema 就可能会报 `Information schema is out of date` 的错误。遇到此错的可能原因如下：

- 执行此 DML 的 TiDB 被 kill 后准备退出，且此 DML 对应的事务执行时间超过一个 DDL lease，在事务提交时会报这个错误。
- TiDB 在执行此 DML 时，有一段时间内连不上 PD 或者 TiKV，导致 TiDB 超过一个 DDL lease 时间没有 load schema，或者导致 TiDB 断开与 PD 之间带 keep alive 设置的连接。

#### 3.3.15 高并发执行 DDL 报错？

高并发情况下执行 DDL （比如批量建表）时，极少部分 DDL 可能会由于并发执行时 key 冲突而执行失败。
建议 DDL 并发低于20。否则需要在应用端重试失败的 DDL 语句。

### 3.4 TiKV 管理

#### 3.4.1 TiKV 集群副本建议配置数量是多少，是不是最小高可用配置（3个）最好？

如果是测试环境 3 副本足够；在生产环境中，不可让集群副本数低于 3，需根据架构特点、业务系统及恢复能力的需求，适当增加副本数。值得注意的是，副本升高，性能会有下降，但是安全性更高。

#### 3.4.2 TiKV 启动报错：cluster ID mismatch

TiKV 本地存储的 cluster ID 和指定的 PD 的 cluster ID 不一致。在部署新的 PD 集群的时候，PD 会随机生成一个 cluster ID，TiKV 第一次初始化的时候会从 PD 获取 cluster ID 存储在本地，下次启动的时候会检查本地的 cluster ID 与 PD 的 cluster ID 是否一致，如果不一致则会报错并退出。出现这个错误一个常见的原因是，用户原先部署了一个集群，后来把 PD 的数据删除了并且重新部署了新的 PD，但是 TiKV 还是使用旧的数据重启连到新的 PD 上，就会报这个错误。

#### 3.4.3 TiKV 启动报错：duplicated store address

启动参数中的地址已经被其他的 TiKV 注册在 PD 集群中了。造成该错误的常见情况：TiKV `--data-dir` 指定的路径下没有数据文件夹（删除或移动后没有更新 --data-dir），用之前参数重新启动该 TiKV。请尝试用 pd-ctl 的 [store delete](https://github.com/pingcap/pd/tree/55db505e8f35e8ab4e00efd202beb27a8ecc40fb/tools/pd-ctl#store-delete--label--weight-store_id----jqquery-string) 功能，删除之前的 store，然后重新启动 TiKV 即可。

#### 3.4.4 TiKV master 和 slave 用的是一样的压缩算法，为什么效果不一样?

目前来看 master 有些文件的压缩率会高一些，这个取决于底层数据的分布和 RocksDB 的实现，数据大小偶尔有些波动是正常的，底层存储引擎会根据需要调整数据。

#### 3.4.5 TiKV block cache 有哪些特性？

TiKV 使用了 RocksDB 的 Column Family (CF) 特性，KV 数据最终存储在默认 RocksDB 内部的 default、write、lock 3 个 CF 内。

- default CF 存储的是真正的数据，与其对应的参数位于 `[rocksdb.defaultcf]` 项中。
- write CF 存储的是数据的版本信息（MVCC）、索引、小表相关的数据，相关的参数位于 `[rocksdb.writecf]` 项中。
- lock CF 存储的是锁信息，系统使用默认参数。
- Raft RocksDB 实例存储 Raft log。default CF 主要存储的是 Raft log，与其对应的参数位于 `[raftdb.defaultcf]` 项中。
- 所有 CF 共享一个 Block-cache，用于缓存数据块，加速 RocksDB 的读取速度，Block-cache 的大小通过参数 `block-cache-size` 控制，`block-cache-size` 越大，能够缓存的热点数据越多，对读取操作越有利，同时占用的系统内存也会越多。
- 每个 CF 有各自的 Write-buffer，大小通过 `write-buffer-size` 控制。

#### 3.4.6 TiKV channel full 是什么原因？

- Raftstore 线程太忙，或者因 I/O 而卡住。可以看一下 Raftstore 的 CPU 使用情况。
- TiKV 过忙（CPU、磁盘 I/O 等），请求处理不过来。

#### 3.4.7 TiKV 频繁切换 Region leader 是什么原因？

- 网络问题导致节点间通信卡了，查看 Report failures 监控。
- 原主 Leader 的节点卡了，导致没有及时给 Follower 发送消息。
- Raftstore 线程卡了。

#### 3.4.8 如果一个节点挂了会影响服务吗？影响会持续多久？

TiDB 使用 Raft 在多个副本之间做数据同步（默认为每个 Region 3 个副本）。当一份备份出现问题时，其他的副本能保证数据的安全。根据 Raft 协议，当某个节点挂掉导致该节点里的 Leader 失效时，在最大 2 * lease time（leasetime 是 10 秒）时间后，通过 Raft 协议会很快将一个另外一个节点里的 Follower 选为新的 Region Leader 来提供服务。

#### 3.4.9 TiKV 在分别在那些场景下占用大量 IO、内存、CPU（超过参数配置的多倍）？

在大量写入、读取的场景中会占用大量的磁盘 IO、内存、CPU。在执行很复杂的查询，比如会产生很大中间结果集的情况下，会消耗很多的内存和 CPU 资源。

#### 3.4.10 TiKV 是否可以使用 SAS/SATA 盘或者进行 SSD/SAS 混合部署？

不可以使用，TiDB 在进行 OLTP 场景中，数据访问和操作需要高 IO 磁盘的支持，TiDB 作为强一致的分布式数据库，存在一定的写放大，如副本复制、存储底层 Compaction，因此，TiDB 部署的最佳实践中推荐用户使用 NVMe SSD 磁盘作为数据存储磁盘。另外，TiKV 与 PD 不能混合部署。

#### 3.4.11 数据表 Key 的 Range 范围划分是在数据接入之前就已经划分好了吗？

不是的，这个和 MySQL 分表规则不一样，需要提前设置好，TiKV 是根据 Region 的大小动态分裂的。

#### 3.4.12 Region 是如何进行分裂的？

Region 不是前期划分好的，但确实有 Region 分裂机制。当 Region 的大小超过参数 `region-max-size` 或 `region-max-keys` 的值时，就会触发分裂，分裂后的信息会汇报给 PD。

#### 3.4.13 TiKV 是否有类似 MySQL 的 `innodb_flush_log_trx_commit` 参数，来保证提交数据不丢失？

是的，TiKV 单机的存储引擎目前使用两个 RocksDB 实例，其中一个存储 raft-log，TiKV 有个 sync-log 参数，在 ture 的情况下，每次提交都会强制刷盘到 raft-log，如果发生 crash 后，通过 raft-log 进行 KV 数据的恢复。

#### 3.4.14 对 WAL 存储有什么推荐的硬件配置，例如 SSD，RAID 级别，RAID 卡 cache 策略，NUMA 设置，文件系统选择，操作系统的 IO 调度策略等？

WAL 属于顺序写，目前我们并没有单独对他进行配置，建议 SSD，RAID 如果允许的话，最好是 RAID 10，RAID 卡 cache、操作系统 I/O 调度目前没有针对性的最佳实践，Linux 7 以上默认配置即可，NUMA 没有特别建议，NUMA 内存分配策略可以尝试使用 `interleave = all`，文件系统建议 ext4。

#### 3.4.15 在最严格的 `sync-log = true` 数据可用模式下，写入性能如何？

一般来说，开启 `sync-log` 会让性能损耗 30% 左右。关闭 `sync-log` 时的性能表现，请参见 [TiDB Sysbench 性能测试报告](https://github.com/pingcap/docs-cn/blob/master/dev/benchmark/sysbench-v4.md)。

#### 3.4.16 是否可以利用 TiKV 的 Raft + 多副本达到完全的数据可靠，单机存储引擎是否需要最严格模式？

通过使用 [Raft 一致性算法](https://raft.github.io/)，数据在各 TiKV 节点间复制为多副本，以确保某个节点挂掉时数据的安全性。只有当数据已写入超过 50% 的副本时，应用才返回 ACK（三副本中的两副本）。但理论上两个节点也可能同时发生故障，所以除非是对性能要求高于数据安全的场景，一般都强烈推荐开启 `sync-log`。

另外，还有一种 `sync-log` 的替代方案，即在 Raft group 中用五个副本而非三个。这将允许两个副本同时发生故障，而仍然能保证数据安全性。

对于单机存储引擎也同样推荐打开 `sync-log` 模式。否则如果节点宕机可能会丢失最后一次写入数据。

#### 3.4.17 使用 Raft 协议，数据写入会有多次网络的 roundtrip，实际写入延迟如何？

理论上，和单机数据库相比，数据写入会多四个网络延迟。

#### 3.4.18 有没有类似 MySQL 的 InnoDB Memcached plugin，可以直接使用 KV 接口，可以不需要独立的 Cache？

TiKV 支持单独进行接口调用，理论上也可以起个实例做为 Cache，但 TiDB 最大的价值是分布式关系型数据库，我们原则上不对 TiKV 单独进行支持。

#### 3.4.19 Coprocessor 组件的主要作用？

- 减少 TiDB 与 TiKV 之间的数据传输。
- 计算下推，充分利用 TiKV 的分布式计算资源。

#### 3.4.20 IO error: No space left on device While appending to file

这是磁盘空间不足导致的，需要加节点或者扩大磁盘空间。

#### 3.4.21 为什么 TiKV 容易出现 OOM？

TiKV 的内存占用主要来自于 RocksDB 的 block-cache，默认为系统总内存的 40%。当 TiKV 容易出现 OOM 时，检查 `block-cache-size` 配置是否过高。还需要注意，当单机部署了多个 TiKV 实例时，需要显式地配置该参数，以防止多个实例占用过多系统内存导致 OOM。

#### 3.4.22 TiDB 数据和 RawKV 数据可存储于同一个 TiKV 集群里吗？

不可以。TiDB 数据（或使用其他事务 API 生成的数据）依赖于一种特殊的键值格式，和 RawKV API 数据（或其他基于 RawKV 的服务生成的数据）并不兼容。

### 3.5 TiDB 测试

#### 3.5.1 TiDB Sysbench 基准测试结果如何？

很多用户在接触 TiDB 都习惯做一个基准测试或者 TiDB 与 MySQL 的对比测试，官方也做了一个类似测试，汇总很多测试结果后，我们发现虽然测试的数据有一定的偏差，但结论或者方向基本一致，由于 TiDB 与 MySQL 由于架构上的差别非常大，很多方面是很难找到一个基准点，所以官方的建议两点：

- 大家不要用过多精力纠结这类基准测试上，应该更多关注 TiDB 的场景上的区别。
- 大家可以直接参考 [TiDB Sysbench 性能测试报告](https://github.com/pingcap/docs-cn/blob/master/dev/benchmark/sysbench-v4.md)。

#### 3.5.2 TiDB 集群容量 QPS 与节点数之间关系如何，和 MySQL 对比如何？

- 在 10 节点内，TiDB 写入能力（Insert TPS）和节点数量基本成 40% 线性递增，MySQL 由于是单节点写入，所以不具备写入扩展能力。
- MySQL 读扩容可以通过添加从库进行扩展，但写流量无法扩展，只能通过分库分表，而分库分表有很多问题，具体参考 [http://t.cn/RTD18qV](http://t.cn/RTD18qV)。
- TiDB 不管是读流量、还是写流量都可以通过添加节点快速方便的进行扩展。

#### 3.5.3 我们的 DBA 测试过 MySQL 性能，单台 TiDB 的性能没有 MySQL 性能那么好？

TiDB 设计的目标就是针对 MySQL 单台容量限制而被迫做的分库分表的场景，或者需要强一致性和完整分布式事务的场景。它的优势是通过尽量下推到存储节点进行并行计算。对于小表（比如千万级以下），不适合 TiDB，因为数据量少，Region 有限，发挥不了并行的优势，最极端的就是计数器表，几行记录高频更新，这几行在 TiDB 里，会变成存储引擎上的几个 KV，然后只落在一个 Region 里，而这个 Region 只落在一个节点上。加上后台强一致性复制的开销，TiDB 引擎到 TiKV 引擎的开销，最后表现出来的就是没有单个 MySQL 好。

### 3.6 TiDB 备份恢复

#### 3.6.1 TiDB 主要备份方式？

目前，推荐的备份方式是使用 [PingCAP fork 的 Mydumper](/v3.0/reference/tools/mydumper.md)。尽管 TiDB 也支持使用 MySQL 官方工具 `mysqldump` 进行数据备份、恢复，但其性能低于 [`mydumper`](/v3.0/reference/tools/mydumper.md)/[`loader`](/v3.0/reference/tools/loader.md)，并且该工具备份、恢复大量数量时，要耗费更多时间。

使用 Mydumper 导出来的数据文件尽可能的小, 最好不要超过 64M, 可以设置参数 -F 64；

loader 的 -t 参数可以根据 TiKV 的实例个数以及负载进行评估调整，例如 3 个 TiKV 的场景， 此值可以设为 3 * (1 ～ n)，当 TiKV 负载过高，loader 以及 TiDB 日志中出现大量 `backoffer.maxSleep 15000ms is exceeded` 可以适当调小该值，当 TiKV 负载不是太高的时候，可以适当调大该值。

## 四、数据、流量迁移

### 4.1 全量数据导出导入

#### 4.1.1 Mydumper

参见 [Mydumper 使用文档](/v3.0/reference/tools/mydumper.md)。

#### 4.1.2 Loader

参见 [Loader 使用文档](/v3.0/reference/tools/loader.md)。

#### 4.1.3 如何将一个运行在 MySQL 上的应用迁移到 TiDB 上？

TiDB 支持绝大多数 MySQL 语法，一般不需要修改代码。

#### 4.1.4 不小心把 MySQL 的 user 表导入到 TiDB 了，或者忘记密码，无法登录，如何处理？

重启 TiDB 服务，配置文件中增加 `-skip-grant-table=true` 参数，无密码登录集群后，可以根据情况重建用户，或者重建 mysql.user 表，具体表结构搜索官网。

#### 4.1.5 在 Loader 运行的过程中，TiDB 可以对外提供服务吗？

该操作进行逻辑插入，TiDB 仍可对外提供服务，但不要执行相关 DDL 操作。

#### 4.1.6 如何导出 TiDB 数据？

TiDB 目前暂时不支持 `select into outfile`，可以通过以下方式导出 TiDB 数据：参考 [MySQL 使用 mysqldump 导出某个表的部分数据](http://blog.csdn.net/xin_yu_xin/article/details/7574662)，使用 mysqldump 加 where 条件导出，使用 MySQL client 将 select 的结果输出到一个文件。

#### 4.1.7 如何从 DB2、Oracle 数据库迁移到 TiDB？

DB2、Oracle 到 TiDB 数据迁移（增量+全量），通常做法有：

- 使用 Oracle 官方迁移工具，如 OGG、Gateway（透明网关）、CDC（Change Data Capture）。
- 自研数据导出导入程序实现。
- 导出（Spool）成文本文件，然后通过 Load infile 进行导入。
- 使用第三方数据迁移工具。

目前看来 OGG 最为合适。

#### 4.1.8 用 Sqoop 批量写入 TiDB 数据，虽然配置了 `--batch` 选项，但还是会遇到 `java.sql.BatchUpdateExecption:statement count 5001 exceeds the transaction limitation` 的错误，该如何解决？

- 在 Sqoop 中，`--batch` 是指每个批次提交 100 条 statement，但是默认每个 statement 包含 100 条 SQL 语句，所以此时 100 * 100 = 10000 条 SQL 语句，超出了 TiDB 的事务限制 5000 条，可以增加选项 `-Dsqoop.export.records.per.statement=10` 来解决这个问题，完整的用法如下：

    {{< copyable "shell-regular" >}}

    ```bash
    sqoop export \
        -Dsqoop.export.records.per.statement=10 \
        --connect jdbc:mysql://mysql.example.com/sqoop \
        --username sqoop ${user} \
        --password ${passwd} \
        --table ${tab_name} \
        --export-dir ${dir} \
        --batch
    ```

- 也可以选择增大 tidb 的单个事物语句数量限制，不过这个会导致内存上涨。

#### 4.1.9 TiDB 有像 Oracle 那样的 Flashback Query 功能么，DDL 支持么？

有，也支持 DDL。详细参考 [TiDB 历史数据回溯](/v3.0/how-to/get-started/read-historical-data.md)。

### 4.2 在线数据同步

#### 4.2.1 Syncer 架构

详细参考 [解析 TiDB 在线数据同步工具 Syncer](https://pingcap.com/blog-cn/tidb-syncer/)。

##### 4.2.1.1 Syncer 使用文档

详细参考 [Syncer 使用文档](/v3.0/reference/tools/syncer.md)。

##### 4.2.1.2 如何配置监控 Syncer 运行情况？

下载 [Syncer Json](https://github.com/pingcap/tidb-ansible/blob/master/scripts/syncer.json) 导入到 Grafana，修改 Prometheus 配置文件，添加以下内容：

- job_name: &#39;syncer_ops&#39; // 任务名字
    static_configs:
- targets: [&#39;10.10.1.1:10096&#39;] // Syncer 监听地址与端口，通知 prometheus 拉取 Syncer 的数据。

重启 Prometheus 即可。

##### 4.2.1.3 有没有现成的同步方案，可以将数据同步到 Hbase、Elasticsearh 等其他存储？

没有，目前依赖程序自行实现。

##### 4.2.1.4 利用 Syncer 做数据同步的时候是否支持只同步部分表？

支持，具体参考 Syncer 使用手册 [Syncer 使用文档](/v3.0/reference/tools/syncer.md)

##### 4.2.1.5 频繁的执行 DDL 会影响 Syncer 同步速度吗？

频繁执行 DDL 对同步速度会有影响。对于 Sycner 来说，DDL 是串行执行的，当同步遇到了 DDL，就会以串行的方式执行，所以这种场景就会导致同步速度下降。

##### 4.2.1.6 使用 Syncer gtid 的方式同步时，同步过程中会不断更新 syncer.meta 文件，如果 Syncer 所在的机器坏了，导致 syncer.meta 文件所在的目录丢失，该如何处理？

当前 Syncer 版本的没有进行高可用设计，Syncer 目前的配置信息 syncer.meta 直接存储在硬盘上，其存储方式类似于其他 MySQL 生态工具，比如 Mydumper。因此，要解决这个问题当前可以有两个方法：

1）把 syncer.meta 数据放到比较安全的磁盘上，例如磁盘做好 raid1；

2）可以根据 Syncer 定期上报到 Prometheus 的监控信息来还原出历史同步的位置信息，该方法的位置信息在大量同步数据时由于延迟会可能不准确。

##### 4.2.1.7  Syncer 下游 TiDB 数据和 MySQL 数据不一致，DML 会退出么？

- 上游 MySQL 中存在数据，下游 TiDB 中该数据不存在，上游 MySQL 执行 `UPDATE` 或 `DELETE`（更新/删除）该条数据的操作时，Syncer 同步过程即不会报错退出也没有该条数据。
- 下游有主键索引或是唯一索引冲突时，执行 `UPDATE` 会退出，执行 `INSERT` 不会退出。

### 4.3 业务流量迁入

#### 4.3.1 如何快速迁移业务流量？

我们建议通过 Syncer 工具搭建成多源 MySQL -> TiDB 实时同步环境，读写流量可以按照需求分阶段通过修改网络配置进行流量迁移，建议 DB 上层部署一个稳定的网络 LB（HAproxy、LVS、F5、DNS 等），这样直接修改网络配置就能实现无缝流量迁移。

#### 4.3.2 TiDB 总读写流量有限制吗？

TiDB 读流量可以通过增加 TiDB server 进行扩展，总读容量无限制，写流量可以通过增加 TiKV 节点进行扩容，基本上写容量也没有限制。

#### 4.3.3 Transaction too large 是什么原因，怎么解决？

由于分布式事务要做两阶段提交，并且底层还需要做 Raft 复制，如果一个事务非常大，会使得提交过程非常慢，并且会卡住下面的 Raft 复制流程。为了避免系统出现被卡住的情况，我们对事务的大小做了限制：

- 单个事务包含的 SQL 语句不超过 5000 条（默认）
- 单条 KV entry 不超过 6MB
- KV entry 的总条数不超过 30w
- KV entry 的总大小不超过 100MB

在 Google 的 Cloud Spanner 上面，也有类似的[限制](https://cloud.google.com/spanner/docs/limits)。

#### 4.3.4 如何批量导入？

导入数据的时候，可以分批插入，每批最好不要超过 1w 行。

对于 insert 和 select，可以开启 `set @@session.tidb_batch_insert=1;` 隐藏参数，insert 会把大事务分批执行。这样不会因为事务太大而超时，但是可能会导致事务原子性的丢失，因此不建议在生产环境中使用。如果事务执行过程中报错，会导致只完成一部分事务的插入。所以建议只有在需要的时候，在 session 中使用，这样不会影响其他语句。事务完成以后，可以用 `set @@session.tidb_batch_insert=0` 关闭。

对 delete 和 update 语句，可以使用 limit 加循环的方式进行操作。

#### 4.3.5 TiDB 中删除数据后会立即释放空间吗？

DELETE，TRUNCATE 和 DROP 都不会立即释放空间。对于 TRUNCATE 和 DROP 操作，在达到 TiDB 的 GC (garbage collection) 时间后（默认 10 分钟），TiDB 的 GC 机制会删除数据并释放空间。对于 DELETE 操作 TiDB 的 GC 机制会删除数据，但不会释放空间，而是当后续数据写入 RocksDB 且进行 compact 时对空间重新利用。

#### 4.3.6 Load 数据时可以对目标表执行 DDL 操作吗？

不可以，加载数据期间不能对目标表执行任何 DDL 操作，这会导致数据加载失败。

#### 4.3.7 TiDB 是否支持 replace into 语法？

支持，但是 load data 不支持 replace into 语法。

#### 4.3.8 数据删除后查询速度为何会变慢？

大量删除数据后，会有很多无用的 key 存在，影响查询效率。目前正在开发 Region Merge 功能，完善之后可以解决这个问题，具体看参考[最佳实践](https://pingcap.com/blog-cn/tidb-best-practice/)中的删除数据部分。

#### 4.3.9 数据删除最高效最快的方式？

在删除大量数据的时候，建议使用 `Delete * from t where xx limit 5000`（xx 建议在满足业务过滤逻辑下，尽量加上强过滤索引列或者直接使用主键选定范围，如 `id >= 5000*n+m and id <= 5000*(n+1)+m` 这样的方案，通过循环来删除，用 `Affected Rows == 0` 作为循环结束条件，这样避免遇到事务大小的限制。如果一次删除的数据量非常大，这种循环的方式会越来越慢，因为每次删除都是从前向后遍历，前面的删除之后，短时间内会残留不少删除标记（后续会被 GC 掉），影响后面的 Delete 语句。如果有可能，建议把 Where 条件细化。可以参考官网[最佳实践](https://pingcap.com/blog-cn/tidb-best-practice/)。

#### 4.3.10 TiDB 如何提高数据加载速度？

主要有两个方面：

- 目前已开发分布式导入工具 [Lightning](/v3.0/reference/tools/tidb-lightning/overview.md)，需要注意的是数据导入过程中为了性能考虑，不会执行完整的事务流程，所以没办法保证导入过程中正在导入的数据的 ACID 约束，只能保证整个导入过程结束以后导入数据的 ACID 约束。因此适用场景主要为新数据的导入（比如新的表或者新的索引），或者是全量的备份恢复（先 Truncate 原表再导入）。
- TiDB 的数据加载与磁盘以及整体集群状态相关，加载数据时应关注该主机的磁盘利用率，TiClient Error/Backoff/Thread CPU 等相关 metric，可以分析相应瓶颈。

#### 4.3.11 对数据做删除操作之后，空间回收比较慢，如何处理？

可以设置并行 GC，加快对空间的回收速度。默认并发为 1，最大可调整为 tikv 实例数量的 50%。可使用 `update mysql.tidb set VARIABLE_VALUE="3" where VARIABLE_NAME="tikv_gc_concurrency";` 命令来调整。

## 五、SQL 优化

### 5.1 TiDB 执行计划解读

详细解读 [理解 TiDB 执行计划](/v3.0/reference/performance/understanding-the-query-execution-plan.md)。

#### 5.1.1 统计信息收集

详细解读 [统计信息](/v3.0/reference/performance/statistics.md)。

#### 5.1.2 Count 如何加速？

Count 就是暴力扫表，提高并发度能显著的提升速度，修改并发度可以参考 `tidb_distsql_scan_concurrency` 变量，但是也要看 CPU 和 I/O 资源。TiDB 每次查询都要访问 TiKV，在数据量小的情况下，MySQL 都在内存里，TiDB 还需要进行一次网络访问。

提升建议：

- 建议提升硬件配置，可以参考[部署建议](/v3.0/how-to/deploy/hardware-recommendations.md)。
- 提升并发度，默认是 10，可以提升到 50 试试，但是一般提升在 2-4 倍之间。
- 测试大数据量的 count。
- 调优 TiKV 配置，可以参考[性能调优](/v3.0/reference/performance/tune-tikv.md)。

#### 5.1.3 查看当前 DDL 的进度？

通过 `admin show ddl` 查看当前 job 进度。操作如下：

{{< copyable "sql" >}}

```sql
admin show ddl;
```

```
*************************** 1. row ***************************
  SCHEMA_VER: 140
       OWNER: 1a1c4174-0fcd-4ba0-add9-12d08c4077dc
RUNNING_JOBS: ID:121, Type:add index, State:running, SchemaState:write reorganization, SchemaID:1, TableID:118, RowCount:77312, ArgLen:0, start time: 2018-12-05 16:26:10.652 +0800 CST, Err:<nil>, ErrCount:0, SnapshotVersion:404749908941733890
     SELF_ID: 1a1c4174-0fcd-4ba0-add9-12d08c4077dc
```

从上面操作结果可知，当前正在处理的是 `add index` 操作。且从 `RUNNING_JOBS` 列的 `RowCount` 字段可以知道当前 `add index` 操作已经添加了 77312 行索引。

#### 5.1.4 如何查看 DDL job？

可以使用 `admin show ddl` 语句查看正在运行的 DDL 作业。

- `admin show ddl jobs`：用于查看当前 DDL 作业队列中的所有结果（包括正在运行以及等待运行的任务）以及已执行完成的 DDL 作业队列中的最近十条结果。
- `admin show ddl job queries 'job_id' [, 'job_id'] ...`：用于显示 `job_id` 对应的 DDL 任务的原始 SQL 语句。此 `job_id` 只搜索正在执行中的任务以及 DDL 历史作业队列中的最近十条结果。

#### 5.1.5 TiDB 是否支持基于 COST 的优化（CBO），如果支持，实现到什么程度？

是的，TiDB 使用的基于成本的优化器（CBO），我们有一个小组单独会对代价模型、统计信息持续优化，除此之外，我们支持 hash join、soft merge 等关联算法。

#### 5.1.6 如何确定某张表是否需要做 analyze ？

可以通过 `show stats_healthy` 来查看 Healthy 字段，一般小于等于 60 的表需要做 analyze。

#### 5.1.7 SQL 的执行计划展开成了树，ID 的序号有什么规律吗？这棵树的执行顺序会是怎么样的？

ID 没什么规律，只要是唯一就行，不过生成的时候，是有一个计数器，生成一个 plan 就加一，执行的顺序和序号无关，整个执行计划是一颗树，执行时从根节点开始，不断地向上返回数据。执行计划的理解，请参考[理解 TiDB 执行计划](/v3.0/reference/performance/understanding-the-query-execution-plan.md)。

#### 5.1.8 TiDB 执行计划中，task cop 在一个 root 下，这个是并行的么？

目前 TiDB 的计算任务隶属于两种不同的 task：cop task 和 root task。cop task 是指被下推到 KV 端分布式执行的计算任务，root task 是指在 TiDB 端单点执行的计算任务。一般来讲 root task 的输入数据是来自于 cop task 的；但是 root task 在处理数据的时候，TiKV 上的 cop task 也可以同时处理数据，等待 TiDB 的 root task 拉取，所以从这个观点上来看，他们是并行的；但是存在数据上下游关系；在执行的过程中，某些时间段其实也是并行的，第一个 cop task 在处理 [100, 200] 的数据，第二个 cop task 在处理 [1, 100] 的数据。执行计划的理解，请参考[理解 TiDB 执行计划](/v3.0/reference/performance/understanding-the-query-execution-plan.md)。

## 六、数据库优化

### 6.1 TiDB

#### 6.1.1 TiDB 参数及调整

详情参考 [TiDB 配置参数](/v3.0/reference/configuration/tidb-server/configuration.md)。

#### 6.1.2 如何打散热点

TiDB 中以 Region 分片来管理数据库，通常来讲，TiDB 的热点指的是 Region 的读写访问热点。而 TiDB 中对于 PK 非整数或没有 PK 的表，可以通过设置 `SHARD_ROW_ID_BITS` 来适度分解 Region 分片，以达到打散 Region 热点的效果。详情可参考官网 [TiDB 专用系统变量和语法](/v3.0/reference/configuration/tidb-server/tidb-specific-variables.md#shard_row_id_bits)中 `SHARD_ROW_ID_BITS` 的介绍。

### 6.2 TiKV

#### 6.2.1 TiKV 性能参数调优

详情参考 [TiKV 性能参数调优](/v3.0/reference/performance/tune-tikv.md)。

## 七、监控

### 7.1 Prometheus 监控框架

详细参考 [TiDB 监控框架概述](/v3.0/how-to/monitor/overview.md)。

### 7.2 监控指标解读

详细参考 [重要监控指标详解](/v3.0/reference/key-monitoring-metrics/overview-dashboard.md)。

#### 7.2.1 目前的监控使用方式及主要监控指标，有没有更好看的监控？

TiDB 使用 Prometheus + Grafana 组成 TiDB 数据库系统的监控系统，用户在 Grafana 上通过 dashboard 可以监控到 TiDB 的各类运行指标，包括系统资源的监控指标，包括客户端连接与 SQL 运行的指标，包括内部通信和 Region 调度的指标，通过这些指标，可以让数据库管理员更好的了解到系统的运行状态，运行瓶颈等内容。在监控指标的过程中，我们按照 TiDB 不同的模块，分别列出了各个模块重要的指标项，一般用户只需要关注这些常见的指标项。具体指标请参见[官方文档](/v3.0/reference/key-monitoring-metrics/overview-dashboard.md)。

#### 7.2.2 Prometheus 监控数据默认 15 天自动清除一次，可以自己设定成 2 个月或者手动删除吗？

可以的，在 Prometheus 启动的机器上，找到启动脚本，然后修改启动参数，然后重启 Prometheus 生效。

```config
--storage.tsdb.retention="60d"
```

#### 7.2.3 Region Health 监控项

TiDB-2.0 版本中，PD metric 监控页面中，对 Region 健康度进行了监控，其中 Region Health 监控项是对所有 Region 副本状况的一些统计。其中 miss 是缺副本，extra 是多副本。同时也增加了按 Label 统计的隔离级别，level-1 表示这些 Region 的副本在第一级 Label 下是物理隔离的，没有配置 location label 时所有 Region 都在 level-0。

#### 7.2.4 Statement Count 监控项中的 selectsimplefull 是什么意思？

代表全表扫，但是可能是很小的系统表。

#### 7.2.5 监控上的 QPS 和 Statement OPS 有什么区别？

QPS 会统计执行的所有 SQL 命令，包括 use database、load data、begin、commit、set、show、insert、select 等。

Statement OPS 只统计 select、update、insert 等业务相关的，所以 Statement OPS 的统计和业务比较相符。

## 八、Cloud TiDB

### 8.1 腾讯云

#### 8.1.1 目前 Cloud TiDB 都有那些云厂商？

Cloud TiDB 目前已经在腾讯云、UCloud 上线，都是数据库一级入口，欢迎大家使用。

## 九、故障排除

### 9.1 TiDB 自定义报错汇总

#### 9.1.1 ERROR 8005 (HY000) : Write Conflict, txnStartTS is stale

可以检查 `tidb_disable_txn_auto_retry` 是否为 on。如是，将其设置为 off；如已经是 off，将 `tidb_retry_limit` 调大到不再发生该错误。

#### 9.1.2 ERROR 9001 (HY000) : PD Server Timeout

请求 PD 超时，请检查 PD Server 状态/监控/日志以及 TiDB Server 与 PD Server 之间的网络。

#### 9.1.3 ERROR 9002 (HY000) : TiKV Server Timeout

请求 TiKV 超时，请检查 TiKV Server 状态/监控/日志以及 TiDB Server 与 TiKV Server 之间的网络。

#### 9.1.4 ERROR 9003 (HY000) : TiKV Server is Busy

TiKV 操作繁忙，一般出现在数据库负载比较高时，请检查 TiKV Server 状态/监控/日志。

#### 9.1.5 ERROR 9004 (HY000) : Resolve Lock Timeout

清理锁超时，当数据库上承载的业务存在大量的事务冲突时，会遇到这种错误，请检查业务代码是否有锁争用。

#### 9.1.6 ERROR 9005 (HY000) : Region is unavailable

访问的 Region 不可用，某个 Raft Group 不可用，如副本数目不足，出现在 TiKV 比较繁忙或者是 TiKV 节点停机的时候，请检查 TiKV Server 状态/监控/日志。

#### 9.1.7 ERROR 9006 (HY000) : GC life time is shorter than transaction duration

`GC Life Time` 间隔时间过短，长事务本应读到的数据可能被清理了，可使用如下命令增加 `GC Life Time`：

{{< copyable "sql" >}}

```sql
update mysql.tidb set variable_value='30m' where variable_name='tikv_gc_life_time';
```

其中 30m 代表仅清理 30 分钟前的数据，这可能会额外占用一定的存储空间。

#### 9.1.8 ERROR 9007 (HY000) : Write Conflict

可以检查 `tidb_disable_txn_auto_retry` 是否为 on。如是，将其设置为 off；如已经是 off，将 `tidb_retry_limit` 调大到不再发生该错误。

### 9.2 MySQL 原生报错汇总

#### 9.2.1 ERROR 2013 (HY000): Lost connection to MySQL server during query 问题的排查方法？

- log 中是否有 panic
- dmesg 中是否有 oom，命令：`dmesg -T | grep -i oom`
- 长时间没有访问，也会收到这个报错，一般是 tcp 超时导致的，tcp 长时间不用, 会被操作系统 kill。

#### 9.2.2 ERROR 1105 (HY000): other error: unknown error Wire Error(InvalidEnumValue(4004)) 是什么意思？

这类问题一般是 TiDB 和 TiKV 版本不匹配，在升级过程尽量一起升级，避免版本 mismatch。

#### 9.2.3 ERROR 1148 (42000): the used command is not allowed with this TiDB version 问题的处理方法？

这个问题是因为在执行 `LOAD DATA LOCAL` 语句的时候，MySQL 客户端不允许执行此语句（即 `local_infile` 选项为 0）。解决方法是在启动 MySQL 客户端时，用 `--local-infile=1` 选项。具体启动指令类似：`mysql --local-infile=1 -u root -h 127.0.0.1 -P 4000`。有些 MySQL 客户端需要设置而有些不需要设置，原因是不同版本的 MySQL 客户端对 `local-infile` 的默认值不同。

#### 9.2.4 ERROR 9001 (HY000): PD server timeout start timestamp may fall behind safe point

这个报错一般是 TiDB 访问 PD 出了问题，TiDB 后台有个 worker 会不断地从 PD 查询 safepoint，如果超过 100s 查不成功就会报这个错。一般是因为 PD 磁盘操作过忙、反应过慢，或者 TiDB 和 PD 之间的网络有问题。TiDB 常见错误码请参考[错误码与故障诊断](/v3.0/reference/error-codes.md)。

### 9.3 TiDB 日志中的报错信息

#### 9.3.1 EOF

当客户端或者 proxy 断开连接时，TiDB 不会立刻察觉连接已断开，而是等到开始往连接返回数据时，才发现连接已断开，此时日志会打印 EOF 错误。
