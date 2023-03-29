---
title: TiDB 3.1 RC Release Notes
---

# TiDB 3.1 RC Release Notes

发版日期：2020 年 4 月 2 日

TiDB 版本：3.1.0-rc

TiDB Ansible 版本：3.1.0-rc

> **警告：**
>
> 该版本存在一些已知问题，已在新版本中修复，建议使用 3.1.x 的最新版本。

## 新功能

+ TiDB

    - 采用的二分搜索实现分区裁剪，以来提升性能 [#15678](https://github.com/pingcap/tidb/pull/15678)
    - 支持 `RECOVER` 语法恢复被 `truncate table` 删除的数据 [#15460](https://github.com/pingcap/tidb/pull/15460)
    - 支持重用语句重试中已分配的 `AUTO_RANDOM` ID [#15393](https://github.com/pingcap/tidb/pull/15393)
    - 支持 `recover table` 恢复 `AUTO_RANDOM` ID 分配器的状态 [#15393](https://github.com/pingcap/tidb/pull/15393)
    - 支持 `YEAR`、`MONTH`、`TO_DAY` 函数作为 Hash partition table 的分区 key [#15619](https://github.com/pingcap/tidb/pull/15619)
    - 只在读到数据，需要加锁的时候，才对表做 schema-change 的检查 [#15708](https://github.com/pingcap/tidb/pull/15708)
    - 为 session 变量 `tidb_replica_read` 增加 `leader-and-follower` 值，实现读请求在 leader 和 follower 直接负载均衡 [#15721](https://github.com/pingcap/tidb/pull/15721)
    - 支持 TiDB 在每次新建连接时动态更新 TLS 证书，实现不重启更新过期客户端证书 [#15163](https://github.com/pingcap/tidb/pull/15163)
    - 通过更新 PD Client 支持每次新建连接是读取加载最新的证书 [#15425](https://github.com/pingcap/tidb/pull/15425)
    - 如果配置了 `Cluster-SSL-*` 强制让 TiDB-PD 和 TiDB-TiDB 使用配置的证书进行 HTTPS 协议传输 [#15430](https://github.com/pingcap/tidb/pull/15430)
    - 新增和 MySQL 兼容的 `--require-secure-transport` 启动项，配置时强制客户端使用 TLS [#15442](https://github.com/pingcap/tidb/pull/15442)
    - 添加 `cluster-verify-cn` 配置，只有拥有特定 CN 属性值证书的访问者才能访问 TiDB Status Port 或建立 gRPC 连接 [#15137](https://github.com/pingcap/tidb/pull/15137)

+ TiKV

    - 支持通过 Raw KV API 备份数据 [#7051](https://github.com/tikv/tikv/pull/7051)
    - 状态服务支持 TLS [#7142](https://github.com/tikv/tikv/pull/7142)
    - KV server 支持 TLS [#7305](https://github.com/tikv/tikv/pull/7305)
    - 优化持有锁的时间以提升备份性能 [#7202](https://github.com/tikv/tikv/pull/7202)

+ PD

    - `shuffle-region-scheduler` 支持调度 learner [#2235](https://github.com/pingcap/pd/pull/2235)
    - pd-ctl 增加配置 Placement Rules 的命令 [#2306](https://github.com/pingcap/pd/pull/2306)

+ Tools

    - TiDB Binlog

        * 同步链路新增 TLS 功能 [#931](https://github.com/pingcap/tidb-binlog/pull/931) [#937](https://github.com/pingcap/tidb-binlog/pull/937) [#939](https://github.com/pingcap/tidb-binlog/pull/939)
        * Drainer 新增 `kafka-client-id` 配置项，支持连接 Kafka 客户端配置客户端 ID [#929](https://github.com/pingcap/tidb-binlog/pull/929)

    - TiDB Lightning

        * 优化 Lightning 的性能 [#281](https://github.com/pingcap/tidb-lightning/pull/281) [#275](https://github.com/pingcap/tidb-lightning/pull/275)
        * 支持 TLS [#270](https://github.com/pingcap/tidb-lightning/pull/270)

    - BR

        * 优化日志输出信息，对用户更友好 [#189](https://github.com/pingcap/br/pull/189)

+ TiDB Ansible

    - 优化 TiFlash 数据目录创建的方式 [#1242](https://github.com/pingcap/tidb-ansible/pull/1242)
    - TiFlash 新增 `Write Amplification` 监控项 [#1234](https://github.com/pingcap/tidb-ansible/pull/1234)
    - 优化 CPU epollexclusive 检查失败时提示信息，包括：通过升级内核版本解决，且提示支持的最小内核版本 [#1243](https://github.com/pingcap/tidb-ansible/pull/1243)

## Bug 修复

+ TiDB

    - 修复由于 update tiflash replica 类型的 DDL 太频繁导致的 information schema changed 错误的问题 [#14884](https://github.com/pingcap/tidb/pull/14884)
    - 修复在使用 `AUTO_RANDOM` 时，未正确生成的 `last_insert_id` 的问题 [#15149](https://github.com/pingcap/tidb/pull/15149)
    - 修复更新 TiFlash replica 状态时可能导致 DDL 卡住的问题 [#15161](https://github.com/pingcap/tidb/pull/15161)
    - 当存在谓词无法下推时，禁止聚合下推和 `TopN` 下推 [#15141](https://github.com/pingcap/tidb/pull/15141)
    - 禁止相互嵌套地创建 `view` [#15440](https://github.com/pingcap/tidb/pull/15440)
    - 修复 `set role all` 后执行 `select current_role` 报错的问题 [#15570](https://github.com/pingcap/tidb/pull/15570)
    - 修复查询中指定列的 `view` 名时，报不识别 `view` 的问题 [#15573](https://github.com/pingcap/tidb/pull/15573)
    - 修复预处理 DDL 语句在写 binlog 信息时可能出错的问题 [#15444](https://github.com/pingcap/tidb/pull/15444)
    - 修复同时访问视图和分区表时导致 panic 的问题 [#15560](https://github.com/pingcap/tidb/pull/15560)
    - 修复 `update duplicate key` 语句中 `bit(n)` 类型的 column 报错的问题 [#15487](https://github.com/pingcap/tidb/pull/15487)
    - 修复 `max-execution-time` 部分场景下不生效的问题 [#15616](https://github.com/pingcap/tidb/pull/15616)
    - 修复在生成 Index 计划时未判断当前的 ReadEngine 中是否包含 TiKV 的问题 [#15773](https://github.com/pingcap/tidb/pull/15773)

+ TiKV

    - 修复在关闭一致性检查参数时，事务中插入已存在的 Key 且立马删除导致冲突检测失效或数据索引不一致的问题 [#7112](https://github.com/tikv/tikv/pull/7112)
    - 修复 `TopN` 比较无符号整型时计算错误的问题 [#7199](https://github.com/tikv/tikv/pull/7199)
    - Raftstore 引入流控机制，解决没有流控可能导致追日志太慢可能导致集群卡住，以及事务大小太大会导致 TiKV 间连接频繁重连的问题 [#7087](https://github.com/tikv/tikv/pull/7087) [#7078](https://github.com/tikv/tikv/pull/7078)
    - 修复发送到 replicas 的读请求可能被永久卡住的问题 [#6543](https://github.com/tikv/tikv/pull/6543)
    - 修复 replica read 会被 apply snapshot 阻塞的问题 [#7249](https://github.com/tikv/tikv/pull/7249)
    - 修复 read index 在 transfer leader 情况下可能导致 panic 的问题 [#7240](https://github.com/tikv/tikv/pull/7240)
    - 修复备份到 S3 时所有 SST 文件填充为零的问题 [#6967](https://github.com/tikv/tikv/pull/6967)
    - 修复备份时未记录 SST 文件大小的导致恢复后有很多空 Region 的问题 [#6983](https://github.com/tikv/tikv/pull/6983)
    - 备份支持 AWS IAM web identity [#7297](https://github.com/tikv/tikv/pull/7297)

+ PD

    - 修复 PD 因处理 Region heartbeat 时的数据竞争导致 Region 信息不正确的问题 [#2234](https://github.com/pingcap/pd/pull/2234)
    - 修复 `random-merge-scheduler` 未遵守 location labels 和 Placement Rules 规则的问题 [#2212](https://github.com/pingcap/pd/pull/2221)
    - 修复 Placement Rule 被具有相同 `startKey` 和 `endKey` 的 Placement Rule 覆盖的问题 [#2222](https://github.com/pingcap/pd/pull/2222)
    - 修复 API 输出的版本号与 PD server 输出版本号不一致的问题 [#2192](https://github.com/pingcap/pd/pull/2192)

+ Tools

    - TiDB Lightning

        * 修复 backend 是 TiDB 时由于字符转化错误导致数据错误的问题 [#283](https://github.com/pingcap/tidb-lightning/pull/283)

    - BR

        * 修复了在开启 TiFlash 集群中，无法使用 BR 恢复的问题 [#194](https://github.com/pingcap/br/pull/194)
