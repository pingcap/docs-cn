---
title: TiDB 3.0.12 Release Notes
---

# TiDB 3.0.12 Release Notes

发版日期：2020 年 3 月 16 日

TiDB 版本：3.0.12

TiDB Ansible 版本：3.0.12

> **警告：**
>
> 该版本存在一些已知问题，已在新版本中修复，建议使用 3.0.x 的最新版本。

## 兼容性变化

+ TiDB
    - 修复慢日志中记录 prewrite binlog 的时间部分计时不准确问题。原本计时的字段名是 `Binlog_prewrite_time`，这次修正后，名称更改为 `Wait_prewrite_binlog_time`。[#15276](https://github.com/pingcap/tidb/pull/15276)

## 新功能

+ TiDB
    - 支持通过 `alter instance` 语句动态加载已被替换的证书文件 [#15080](https://github.com/pingcap/tidb/pull/15080) [#15292](https://github.com/pingcap/tidb/pull/15292)
    - 添加 `cluster-verify-cn` 配置项，配置后必须是对应 CN 证书才使用 status 服务 [#15164](https://github.com/pingcap/tidb/pull/15164)
    - 在每个 TiDB server 中添加对 DDL 请求的一个限流的功能，从而降低 DDL 请求冲突报错频率 [#15148](https://github.com/pingcap/tidb/pull/15148)
    - 支持在 binlog 写入失败时，TiDB 退出 [#15339](https://github.com/pingcap/tidb/pull/15339)

+ Tools
    - TiDB Binlog
        - Drainer 新增 `kafka-client-id` 配置项，支持连接 Kafka 客户端配置客户端 ID [#929](https://github.com/pingcap/tidb-binlog/pull/929)

## Bug 修复

+ TiDB
    - 使 `GRANT`/`REVOKE` 在对多个用户修改时，保证原子性 [#15092](https://github.com/pingcap/tidb/pull/15092)
    - 修复在分区表上面悲观锁的加锁未能锁住正确的行的问题 [#15114](https://github.com/pingcap/tidb/pull/15114)
    - 建索引长度超过限制时，使报错信息根据配置中 `max-index-length` 的值显示 [#15130](https://github.com/pingcap/tidb/pull/15130)
    - 修复 `FROM_UNIXTIME` 函数小数点位数不正确的问题 [#15270](https://github.com/pingcap/tidb/pull/15270)
    - 修复一个事务中删除自己写的记录导致冲突检测失效或数据索引不一致问题 [#15176](https://github.com/pingcap/tidb/pull/15176)

+ TiKV
    - 修复一个在关闭一致性检查参数时，在事务中插入一个已存在的 Key 然后立马删除，导致冲突检测失效或数据索引不一致的问题 [#7054](https://github.com/tikv/tikv/pull/7054)
    - Raftstore 引入流控机制，解决没有流控可能导致追日志太慢可能导致集群卡住，以及事务大小太大会导致 TiKV 间连接频繁重连的问题 [#7072](https://github.com/tikv/tikv/pull/7072) [#6993](https://github.com/tikv/tikv/pull/6993)

+ PD
    - 修复 PD 因处理 Region heartbeat 时的数据竞争导致 Region 信息不正确的问题 [#2233](https://github.com/pingcap/pd/pull/2233)

+ TiDB Ansible
    - 支持一个集群部署多个 Grafana/Prometheus/Alertmanager [#1198](https://github.com/pingcap/tidb-ansible/pull/1198)
