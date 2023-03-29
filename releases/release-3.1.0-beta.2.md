---
title: TiDB 3.1 Beta.2 Release Notes
---

# TiDB 3.1 Beta.2 Release Notes

发版日期：2020 年 3 月 9 日

TiDB 版本：3.1.0-beta.2

TiDB Ansible 版本：3.1.0-beta.2

> **警告：**
>
> 该版本存在一些已知问题，已在新版本中修复，建议使用 3.1.x 的最新版本。

## 兼容性变化

+ Tools
    - TiDB Lightning
        - 优化配置项，部分配置项在没有进行配置的时候使用 [TiDB Lightning 配置参数](/tidb-lightning/tidb-lightning-configuration.md)中的默认配置 [#255](https://github.com/pingcap/tidb-lightning/pull/255)
        - 新增 `--tidb-password` 命令行参数，用于设置 TiDB 的密码 [#253](https://github.com/pingcap/tidb-lightning/pull/253)

## 新功能

+ TiDB
    - 支持在列属性上添加 `AutoRandom` 关键字，控制系统自动为主键分配随机整数，避免 `AUTO_INCREMENT` 自增主键带来的写入热点问题 [#14555](https://github.com/pingcap/tidb/pull/14555)
    - 新增通过 DDL 语句为表创建、删除列存储副本的功能 [#14537](https://github.com/pingcap/tidb/pull/14537)
    - 新增优化器可自主选择不同的存储引擎的功能 [#14537](https://github.com/pingcap/tidb/pull/14537)
    - 新增 SQL Hint 支持不同的存储引擎的功能 [#14537](https://github.com/pingcap/tidb/pull/14537)
    - 新增通过 `tidb_replic_read` 系统变量从 Follower 上读取数据的功能 [#13464](https://github.com/pingcap/tidb/pull/13464)

+ TiKV
    - Raftstore
        - 新增 `peer_address` 参数，为其他类型的服务提供通过不同端连接此 TiKV server 的能力 [#6491](https://github.com/tikv/tikv/pull/6491)
        - 新增 `read_index` 和 `read_index_resp` 监控项，用于监控 `ReadIndex` 请求数 [#6610](https://github.com/tikv/tikv/pull/6610)
    - PD Client
        - 新增将本地线程统计信息汇报给 PD 的功能 [#6605](https://github.com/tikv/tikv/pull/6605)
    - Backup
        - 用 Rust 的 `async-speed-limit` 流控库替代 `RocksIOLimiter` 流控库，避免备份时拷贝多次内存的问题 [#6462](https://github.com/tikv/tikv/pull/6462)
+ PD
    - 新增 location label 的名字中允许使用斜杠 `/` 的功能 [#2084](https://github.com/pingcap/pd/pull/2084)
+ TiFlash
    - 初始版本
+ TiDB Ansible
    - 新增同一个集群中部署多个 Grafana/Prometheus/Alertmanager 的功能 [#1143](https://github.com/pingcap/tidb-ansible/pull/1143)
    - 新增部署 TiFlash 组件的功能 [#1148](https://github.com/pingcap/tidb-ansible/pull/1148)
    - 新增 TiFlash 组件相关的监控指标 [#1152](https://github.com/pingcap/tidb-ansible/pull/1152)

## Bug 修复

+ TiKV
    - Raftstore
        - 修复静默 Region 读数据处理不当导致无法处理读请求的问题 [#6450](https://github.com/tikv/tikv/pull/6450)
        - 修复 `ReadIndex` 在 leader 切换时可能导致系统 panic 的问题 [#6613](https://github.com/tikv/tikv/pull/6613)
        - 修复 Hibernate Region 在某些特殊条件下未被正确唤醒的问题 [#6730](https://github.com/tikv/tikv/pull/6730) [#6737](https://github.com/tikv/tikv/pull/6737) [#6972](https://github.com/tikv/tikv/pull/6972)
    - Backup
        - 修复备份数据时备份了多余的数据，导致恢复数据时数据索引不一致的问题 [#6659](https://github.com/tikv/tikv/pull/6659)
        - 修复备份时因处理已被删除的值逻辑不正确导致系统 panic 的问题 [#6726](https://github.com/tikv/tikv/pull/6726)
+ PD
    - 修复因 rule checker 给 Region 分配 store 失败导致系统 panic 的问题 [#2161](https://github.com/pingcap/pd/pull/2161)
+ Tools
    - TiDB Lightning
        - 修复在非 Server mode 模式下 web 界面无法打开的问题 [#259](https://github.com/pingcap/tidb-lightning/pull/259)
    - BR
        - 修复在恢复数据过程中遇到不可恢复的错误时，程序无法及时退出的问题 [#152](https://github.com/pingcap/br/pull/152)

+ TiDB Ansible
    - 修复在某些场景下获取不到 PD Leader 导致滚动升级命令执行失败的问题 [#1122](https://github.com/pingcap/tidb-ansible/pull/1122)
