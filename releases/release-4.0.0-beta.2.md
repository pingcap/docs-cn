---
title: TiDB 4.0.0 Beta.2 Release Notes
---

# TiDB 4.0.0 Beta.2 Release Notes

发版日期：2020 年 3 月 18 日

TiDB 版本：4.0.0-beta.2

TiDB Ansible 版本：4.0.0-beta.2

## 兼容性变化

+ Tools
    - TiDB Binlog
        - 修复 Drainer 配置 `disable-dispatch`、`disable-causality` 时系统直接报错并退出的问题 [#915](https://github.com/pingcap/tidb-binlog/pull/915)

## 新功能

+ TiKV
    - 支持将动态修改配置的结果持久化存储到硬盘 [#6684](https://github.com/tikv/tikv/pull/6684)

+ PD
    - 支持将动态修改配置的结果持久化存储到硬盘 [#2153](https://github.com/pingcap/pd/pull/2153)

+ Tools
    - TiDB Binlog
        - 新增 TiDB 集群之间数据双向复制功能 [#879](https://github.com/pingcap/tidb-binlog/pull/879) [#903](https://github.com/pingcap/tidb-binlog/pull/903)
    - TiDB Lightning
        - 新增配置 TLS 功能 [#40](https://github.com/tikv/importer/pull/40) [#270](https://github.com/pingcap/tidb-lightning/pull/270)
    - 新增 TiCDC 工具，提供以下功能：
        - 捕捉 TiKV 变化的数据，同步到下游 Kafka、MySQL 协议的数据库
        - 确保数据最终一致性，若下游是 Kafka，也可确保行级别的有序
        - 提供进程级别的高可用能力
    - BR
        - 开启增量备份、支持将备份文件存储在 AWS S3 等实验性功能 [#175](https://github.com/pingcap/br/pull/175)

+ TiDB Ansible
    - 新增将节点信息注册到 etcd 的功能 [#1196](https://github.com/pingcap/tidb-ansible/pull/1196)
    - 新增支持在 ARM 平台上部署 TiDB 服务的功能 [#1204](https://github.com/pingcap/tidb-ansible/pull/1204)

## Bug 修复

+ TiKV
    - 修复 backup 在遇到空的 short value 时可能 panic 的问题 [#6718](https://github.com/tikv/tikv/pull/6718)
    - 修复 Hibernate Region 在某些特殊条件下未被正确唤醒的问题 [#6772](https://github.com/tikv/tikv/pull/6672) [#6648](https://github.com/tikv/tikv/pull/6648) [#6376](https://github.com/tikv/tikv/pull/6736)

+ PD
    - 修复因 rule checker 在给 Region 分配 store 失败导致系统 panic 的问题 [#2160](https://github.com/pingcap/pd/pull/2160)
    - 修复启用动态修改配置功能后，配置可能在切换 leader 时有同步延迟的问题 [#2154](https://github.com/pingcap/pd/pull/2154)

+ Tools
    - BR
        - 修复因 PD 无法处理过大消息导致在数据规模较大时恢复失败的问题 [#167](https://github.com/pingcap/br/pull/167)
        - 修复因 BR 与 TiDB 版本不兼容导致 BR 运行失败的问题 [#186](https://github.com/pingcap/br/pull/186)
        - 修复因 BR 与 TiFlash 不兼容导致 BR 运行失败的问题 [#194](https://github.com/pingcap/br/pull/194)
