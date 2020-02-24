---
title: TiDB 2.1.14 Release Notes
category: Releases
---

# TiDB 2.1.14 Release Notes

发版日期：2019 年 7 月 4 日

TiDB 版本：2.1.14

TiDB Ansible 版本：2.1.14

## TiDB

- 修复某些情况下列裁剪导致查询结果不正确的问题 [#11019](https://github.com/pingcap/tidb/pull/11019)
- 修复 `show processlist` 中 `db` 和 `info` 列信息显示有误的问题 [#11000](https://github.com/pingcap/tidb/pull/11000)
- 修复 `MAX_EXECUTION_TIME` 作为 SQL hint 和全局变量在某些情况下不生效的问题 [#10999](https://github.com/pingcap/tidb/pull/10999)
- 支持根据负载情况自动调整 Auto ID 分配的步长 [#10997](https://github.com/pingcap/tidb/pull/10997)
- 修复 SQL 查询结束时 `MemTracker` 统计的 DistSQL 内存信息未正确清理的问题 [#10971](https://github.com/pingcap/tidb/pull/10971)
- `information_schema.processlist` 表中新增 `MEM` 列用于描述 Query 的内存使用情况 [#10896](https://github.com/pingcap/tidb/pull/10896)
- 新增全局系统变量  `max_execution_time`，用于控制查询的最大执行时间 [10940](https://github.com/pingcap/tidb/pull/10940)
- 修复使用未支持的聚合函数导致 TiDB panic 的问题 [#10911](https://github.com/pingcap/tidb/pull/10911)
- 新增 `load data` 语句失败后自动回滚最后一个事务功能 [#10862](https://github.com/pingcap/tidb/pull/10862)
- 修复 TiDB 超过内存配额的行为配置为 CANCEL 时，某些情况下 TiDB 返回结果不正确的问题 [#11016](https://github.com/pingcap/tidb/pull/11016)
- 禁用 `TRACE` 语句，避免 TiDB panic 问题 [#11039](https://github.com/pingcap/tidb/pull/11039)
- 新增 `mysql.expr_pushdown_blacklist` 系统表，控制动态开启/关闭 TiDB 下推到 Coprocessor 的函数 [#10998](https://github.com/pingcap/tidb/pull/10998)
- 修复 `ANY_VALUE` 函数在 `ONLY_FULL_GROUP_BY` 模式下不生效的问题 [#10994](https://github.com/pingcap/tidb/pull/10994)
- 修复给字符串类型的用户量赋值时因未深度拷贝导致赋值不正确的问题 [#11043](https://github.com/pingcap/tidb/pull/11043)

## TiKV

- 优化 Raftstore 消息处理中对空回调的处理流程，避免发送不必要的消息 [#4682](https://github.com/tikv/tikv/pull/4682)

## PD

- 调整当读取到无效配置项时日志信息输出的级别，由 Error 调整为 Warning [#1577](https://github.com/pingcap/pd/pull/1577)

## Tools

TiDB Binlog

- Reparo
    - 新增 `safe-mode` 配置项，开启后支持导入重复的数据 [#662](https://github.com/pingcap/tidb-binlog/pull/662)
- Pump
    - 新增 `stop-write-at-available-space` 配置项，限制 Binlog 空间保留的大小 [#659](https://github.com/pingcap/tidb-binlog/pull/659)
    - 修复 LevelDB L0 文件个数为 0 时 GC 有时不生效的问题 [#648](https://github.com/pingcap/tidb-binlog/pull/648)
    - 优化 log 文件删除的算法，加速释放空间 [#648](https://github.com/pingcap/tidb-binlog/pull/648)
- Drainer
    - 修复下游 TiDB BIT 类型列更新失败的问题 [#655](https://github.com/pingcap/tidb-binlog/pull/655)

## TiDB Ansible

- 新增 `ansible` 命令及其 `jmespath`、`Jinja2` 依赖包的预检查功能 [#807](https://github.com/pingcap/tidb-ansible/pull/807)
- Pump 新增 `stop-write-at-available-space` 参数，当磁盘剩余空间小于该值（默认 10 GiB）时，Pump 停止写入 Binlog [#807](https://github.com/pingcap/tidb-ansible/pull/807)
