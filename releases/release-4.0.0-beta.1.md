---
title: TiDB 4.0.0 Beta.1 Release Notes
---

# TiDB 4.0.0 Beta.1 Release Notes

发版日期：2020 年 2 月 28 日

TiDB 版本：4.0.0-beta.1

TiDB Ansible 版本：4.0.0-beta.1

## 兼容性变化

* TiDB
    + 修改配置项 `log.enable-slow-log` 的类型，由整数型改为布尔类型 [#14864](https://github.com/pingcap/tidb/pull/14864)
    + 调整修改系统表 `mysql.user` 中 `password` 列名为 `authentication_string`，与 MySQL 5.7 保持一致（**该变动会导致升级后不能回退**） [#14598](https://github.com/pingcap/tidb/pull/14598)
    + `txn-total-size-limit` 配置项的默认值由 1GB 调整为 100MB [#14522](https://github.com/pingcap/tidb/pull/14522)
    + 新增动态修改、更新配置项的功能，配置项由 PD 持久化存储 [#14750](https://github.com/pingcap/tidb/pull/14750) [#14303](https://github.com/pingcap/tidb/pull/14303) [#14830](https://github.com/pingcap/tidb/pull/14830)

* TiKV
    + 新增 `readpool.unify-read-pool` 配置项，默认值为 `True`，用于控制点查是否共用 Coprocessor 的处理线程 [#6375](https://github.com/tikv/tikv/pull/6375) [#6401](https://github.com/tikv/tikv/pull/6401) [#6534](https://github.com/tikv/tikv/pull/6534) [#6582](https://github.com/tikv/tikv/pull/6582) [#6585](https://github.com/tikv/tikv/pull/6585) [#6593](https://github.com/tikv/tikv/pull/6593) [#6597](https://github.com/tikv/tikv/pull/6597) [#6677](https://github.com/tikv/tikv/pull/6677)

* PD
    + 优化 HTTP API 兼容以新的配置项管理方式 [#2080](https://github.com/pingcap/pd/pull/2080)

* TiDB Lightning
    + 优化配置项，部分配置项在没有设置的时候使用默认配置 [#255](https://github.com/pingcap/tidb-lightning/pull/255)

* TiDB Ansible
    + 将 `theflash` 更名为 `tiflash` [#1130](https://github.com/pingcap/tidb-ansible/pull/1130)
    + 优化 TiFlash 配置文件中的默认值及相关配置 [#1138](https://github.com/pingcap/tidb-ansible/pull/1138)

## 新功能

* TiDB
    + 慢日志系统表 `SLOW_QUERY / CLUSTER_SLOW_QUERY` 支持查询任意时间段的日志[#14840](https://github.com/pingcap/tidb/pull/14840) [#14878](https://github.com/pingcap/tidb/pull/14878)
    + 支持 SQL 性能诊断功能
        - [#14843](https://github.com/pingcap/tidb/pull/14843) [#14810](https://github.com/pingcap/tidb/pull/14810) [#14835](https://github.com/pingcap/tidb/pull/14835) [#14801](https://github.com/pingcap/tidb/pull/14801) [#14743](https://github.com/pingcap/tidb/pull/14743)
        - [#14718](https://github.com/pingcap/tidb/pull/14718) [#14721](https://github.com/pingcap/tidb/pull/14721) [#14670](https://github.com/pingcap/tidb/pull/14670) [#14663](https://github.com/pingcap/tidb/pull/14663) [#14668](https://github.com/pingcap/tidb/pull/14668)
        - [#14896](https://github.com/pingcap/tidb/pull/14896)
    + 新增 Sequence 功能 [#14731](https://github.com/pingcap/tidb/pull/14731) [#14589](https://github.com/pingcap/tidb/pull/14589) [#14674](https://github.com/pingcap/tidb/pull/14674) [#14442](https://github.com/pingcap/tidb/pull/14442)
    + 新增动态修改、更新配置项的功能，配置项由 PD 持久化存储 [#14750](https://github.com/pingcap/tidb/pull/14750) [#14303](https://github.com/pingcap/tidb/pull/14303) [#14830](https://github.com/pingcap/tidb/pull/14830)
    + 新增系统自动根据负载均衡策略从不同角色上读取数据的功能，且新增 `leader-and-follower` 系统变量用于控制开启此功能 [#14761](https://github.com/pingcap/tidb/pull/14761)
    + 新增 `Coercibility` 函数 [#14739](https://github.com/pingcap/tidb/pull/14739)
    + 支持在分区表上建立 TiFlash 副本 [#14735](https://github.com/pingcap/tidb/pull/14735) [#14713](https://github.com/pingcap/tidb/pull/14713) [#14644](https://github.com/pingcap/tidb/pull/14644)
    + 完善 `SLOW_QUERY` 表的权限检查 [#14451](https://github.com/pingcap/tidb/pull/14451)
    + 新增当 `Join` 时若内存不足时系统自动将中间结果写磁盘文件的功能 [#14708](https://github.com/pingcap/tidb/pull/14708) [#14279](https://github.com/pingcap/tidb/pull/14279)
    + 新增通过查询 `information_schema.PARTITIONS` 系统表查看 partition 详细信息的功能 [#14347](https://github.com/pingcap/tidb/pull/14347)
    + 新增 `json_objectagg` 聚合函数 [#11154](https://github.com/pingcap/tidb/pull/11154)
    + 新增审计日志记录用户登录失败的功能 [#14594](https://github.com/pingcap/tidb/pull/14594)
    + 新增 `max-server-connections` 配置项，默认值为 `4096` ，用于控制单个服务器连接数 [#14409](https://github.com/pingcap/tidb/pull/14409)
    + 支持隔离读在 Server 级别指定多个存储引擎 [#14440](https://github.com/pingcap/tidb/pull/14440)
    + 优化 `Apply` 算子和 `Sort` 算子的代价估算模型，提升系统稳定性 [#13550](https://github.com/pingcap/tidb/pull/13550) [#14708](https://github.com/pingcap/tidb/pull/14708)

* TiKV
    + 新增通过 HTTP API 从 status 端口获取配置项的功能 [#6480](https://github.com/tikv/tikv/pull/6480)
    + 提升 Coprocessor 的 Chunk Encoder 的性能 [#6341](https://github.com/tikv/tikv/pull/6341)

* PD
    + 新增通过 UI 访问集群热点数据分布功能 [#2086](https://github.com/pingcap/pd/pull/2086)
    + 新增收集集群组件的启动时间的功能 [#2116](https://github.com/pingcap/pd/pull/2116)
    + member API 返回信息新增部署路径和组件版本信息 [#2130](https://github.com/pingcap/pd/pull/2130)
    + pd-ctl 新增 `component` 命令用于修改、查看组件配置信息 (experimental) [#2092](https://github.com/pingcap/pd/pull/2092)

* TiDB Binlog
    + 同步链路新增 TLS 功能 [#904](https://github.com/pingcap/tidb-binlog/pull/904) [#894](https://github.com/pingcap/tidb-binlog/pull/894)
    + Drainer 新增 `kafka-client-id` 配置项，支持连接 Kafka 客户端配置客户端 ID [#902](https://github.com/pingcap/tidb-binlog/pull/902)
    + Drainer 新增清理增量备份文件的功能 [#885](https://github.com/pingcap/tidb-binlog/pull/885)

* TiDB Ansible
    + 新增同一个集群中部署多个 Grafana/Prometheus/Alertmanager 的功能 [#1142](https://github.com/pingcap/tidb-ansible/pull/1142)
    + TiFlash 配置文件新增 `metrics_port` 配置项，默认值为`8234` [#1145](https://github.com/pingcap/tidb-ansible/pull/1145)
    + TiFlash 配置文件新增 `flash_proxy_status_port` 配置项，默认值为 `20292` [#1141](https://github.com/pingcap/tidb-ansible/pull/1141)
    + 新增 TiFlash 监控 Dashboard [#1147](https://github.com/pingcap/tidb-ansible/pull/1147) [#1151](https://github.com/pingcap/tidb-ansible/pull/1151)

## Bug 修复

* TiDB
    + 修复创建视图时，列名超过 64 个字符时将报错的问题，报错改为重命名过长的列名 [#14850](https://github.com/pingcap/tidb/pull/14850)
    + 修复因 `create or replace view` 语句处理逻辑不正确导致 `information_schema.views` 中有重复数据的问题 [#14832](https://github.com/pingcap/tidb/pull/14832)
    + 修复开启 `plan cache` 之后，`BatchPointGet` 的获取到错误数据的问题 [#14855](https://github.com/pingcap/tidb/pull/14855)
    + 修复按照时间分区的分区表，在修改时区后，因处理逻辑不正确导致数据插入到错误分区表的问题 [#14370](https://github.com/pingcap/tidb/pull/14370)
    + 修复 `IsTrue` 函数的表达式因名称不正确，在执行外连化简利用非法函数名重建表达式导致系统 panic 的问题 [#14515](https://github.com/pingcap/tidb/pull/14515)
    + 修复 `show binding` 语句权限检查不正确的问题 [#14443](https://github.com/pingcap/tidb/pull/14443)

* TiKV
    + 修复 `CAST` 函数在 TiDB 和 TiKV 中行为不一致性的问题 [#6463](https://github.com/tikv/tikv/pull/6463) [#6461](https://github.com/tikv/tikv/pull/6461) [#6459](https://github.com/tikv/tikv/pull/6459) [#6474](https://github.com/tikv/tikv/pull/6474) [#6492](https://github.com/tikv/tikv/pull/6492) [#6569](https://github.com/tikv/tikv/pull/6569)

* TiDB Lightning
    + 修复在非 server mode 模式下 web 界面无法打开的问题 [#259](https://github.com/pingcap/tidb-lightning/pull/259)
