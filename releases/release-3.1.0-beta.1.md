---
title: TiDB 3.1 Beta.1 Release Notes
---

# TiDB 3.1 Beta.1 Release Notes

发版日期：2020 年 1 月 10 日

TiDB 版本：3.1.0-beta.1

TiDB Ansible 版本：3.1.0-beta.1

## TiKV

+ backup
    - 备份文件的名称由 `start_key` 改为 `start_key` 的 hash 值，减少文件名的长度，方便阅读 [#6198](https://github.com/tikv/tikv/pull/6198)
    - 关闭 RocksDB `force_consistency_checks` 检查功能，避免一致性检查误报的问题 [#6249](https://github.com/tikv/tikv/pull/6249)
    - 新增增量备份功能 [#6286](https://github.com/tikv/tikv/pull/6286)
+ sst_importer
    - 修复恢复后 SST 文件没有 MVCC Properties 的问题 [#6378](https://github.com/tikv/tikv/pull/6378)
    - 新增 `tikv_import_download_duration`、`tikv_import_download_bytes`、`tikv_import_ingest_duration`、`tikv_import_ingest_bytes`、`tikv_import_error_counter` 等监控项，用于观察 Download SST 和 Ingest SST 的开销 [#6404](https://github.com/tikv/tikv/pull/6404)
+ raftstore
    - 修复因 Follower Read 在 leader 变更时读到旧数据的问题，导致事务的隔离性被破坏的问题 [#6343](https://github.com/tikv/tikv/pull/6343)

## Tools

+ BR (Backup and Restore)
    - 修复备份进度信息不准确的问题 [#127](https://github.com/pingcap/br/pull/127)
    - 提升 split Region 的性能 [#122](https://github.com/pingcap/br/pull/122)
    - 新增备份恢复分区表的功能 [#137](https://github.com/pingcap/br/pull/137)
    - 新增自动调度 PD schedulers 功能 [#123](https://github.com/pingcap/br/pull/123)
    - 修复非 PKIsHandle 表恢复后数据覆盖的问题 [#139](https://github.com/pingcap/br/pull/139)

## TiDB Ansible

- 新增初始化阶段自动关闭操作系统 THP 的功能 [#1086](https://github.com/pingcap/tidb-ansible/pull/1086)
- 新增 BR 组件的 Grafana 监控 [#1093](https://github.com/pingcap/tidb-ansible/pull/1093)
- 优化 TiDB Lightning 部署，自动创建相关目录 [#1104](https://github.com/pingcap/tidb-ansible/pull/1104)
