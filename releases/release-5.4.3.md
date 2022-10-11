---
title: TiDB 5.4.3 Release Notes
---

# TiDB 5.4.3 Release Notes

发版日期：2022 年 x 月 x 日

TiDB 版本：5.4.3

## 兼容性变更

## 提升改进

+ TiDB **TW: @TomShawn**

    <!--sql-infra **owner: @zimulala**-->

    <!--execution **owner: @zanmato1984**-->

    <!--transaction **owner: @cfzjywxk**-->

    <!--planner **owner: @winoros**-->

    <!--diagnosis **owner: @mornyx**-->

+ TiKV **owner: @tabokie, TW: @Oreoxmt**

    - 支持将 RocksDB write stall 设置为比流量控制阈值更小的值 [#13467](https://github.com/tikv/tikv/issues/13467)
    - (dup) 支持配置 `unreachable_backoff` 避免 Raftstore 发现某个 Peer 无法连接时广播过多消息 [#13054](https://github.com/tikv/tikv/issues/13054)

+ PD **owner: @nolouch, TW: @Oreoxmt**

+ TiFlash **TW: @shichun-0415**

+ Tools

    + TiDB Lightning **owner: @niubell, TW: @ran-huang**

        - (dup) 优化 Scatter Region 为批量模式，提升 Scatter Region 过程的稳定性 [#33618](https://github.com/pingcap/tidb/issues/33618)

    + TiDB Data Migration (DM) **owner: @niubell, TW: @ran-huang**

    + TiCDC **owner: @nongfushanquan, TW: @shichun-0415**

        - (dup) 优化了多 Region 场景下，runtime 上下文切换带来过多性能开销的问题 [#5610](https://github.com/pingcap/tiflow/issues/5610)

    + Backup & Restore (BR) **owner: @3pointer, TW: @shichun-0415**

    + Dumpling **owner: @niubell, TW: @ran-huang**

    + TiDB Binlog

## Bug 修复

+ TiDB **TW: @TomShawn**

    <!--sql-infra **owner: @zimulala**-->
    - (dup) 修复 `SHOW CREATE PLACEMENT POLICY` 输出结果不正确的问题 [#37526](https://github.com/pingcap/tidb/issues/37526)
    - (dup) 修复集群的 PD 节点被替换后一些 DDL 语句会卡住一段时间的问题 [#33908](https://github.com/pingcap/tidb/issues/33908)
    - (dup) 修复 `KILL TIDB` 在空闲连接上无法立即生效的问题 [#24031](https://github.com/pingcap/tidb/issues/24031)
    - 修复在 TiDB 上查询 `INFORMATION_SCHEMA.COLUMNS` 系统表得到的 `DATA_TYPE` 和 `COLUMN_TYPE` 列结果不正确的问题 [#36496](https://github.com/pingcap/tidb/issues/36496)
    - (dup) 修复了在开启 TiDB Binlog 时，TiDB 执行 `ALTER SEQUENCE` 会产生错误的元信息版本号，进而导致 Drainer 报错退出的问题 [#36276](https://github.com/pingcap/tidb/issues/36276)

    <!--execution **owner: @zanmato1984**-->

    - (dup) 修复 `UNION` 运算符可能会非预期地返回空结果的问题 [#36903](https://github.com/pingcap/tidb/issues/36903)
    - (dup) 修复在 TiFlash 中为分区表开启动态模式时结果出错的问题 [#37254](https://github.com/pingcap/tidb/issues/37254)
    - (dup) 修复 `INL_HASH_JOIN` 和 `LIMIT` 一起使用时可能会卡住的问题 [#35638](https://github.com/pingcap/tidb/issues/35638)
    - (dup) 修复执行 `SHOW WARNINGS` 时可能会报 `invalid memory address or nil pointer dereference` 的问题 [#31569](https://github.com/pingcap/tidb/issues/31569)

    <!--transaction **owner: @cfzjywxk**-->

    - 修复在读已提交隔离级别 (RC isolation level) 执行 Stale Read 报 `invalid transaction` 错误的问题 [#30872](https://github.com/pingcap/tidb/issues/30872)
    - (dup) 修复带 DML 算子的 `EXPLAIN ANALYZE` 语句可能在事务提交完成前返回结果的问题 [#37373](https://github.com/pingcap/tidb/issues/37373)
    - (dup) 修复开启 TiDB Binlog 后插入重复数据导致 data and columnID count not match 错误的问题 [#33608](https://github.com/pingcap/tidb/issues/33608)

    <!--planner **owner: @winoros**-->

    - (dup) 修复 Static Partition Prune 模式下带聚合条件的 SQL 语句在表为空时结果错误的问题 [#35295](https://github.com/pingcap/tidb/issues/35295)
    - (dup) 修复 TiDB 在执行 `UPDATE` 语句时可能会 panic 的问题 [#32311](https://github.com/pingcap/tidb/issues/32311)
    - (dup) 修复 `UnionScan` 无法保序导致的查询结果不正确的问题 [#33175](https://github.com/pingcap/tidb/issues/33175)
    - (dup) 修复在某些情况下 `UPDATE` 语句错误地消除了 projection 导致 `Can't find column` 报错的问题 [#37568](https://github.com/pingcap/tidb/issues/37568)
    - (dup) 修复某些情况下分区表无法充分利用索引来扫描数据的问题 [#33966](https://github.com/pingcap/tidb/issues/33966)
    - 修复某些情况下，`EXECUTE` 语句可能抛出非预期异常的问题 [#37187](https://github.com/pingcap/tidb/issues/37187)
    - 修复开启 Prepared Plan Cache 后，使用 `BIT` 类型的索引可能会导致查询结果错误的问题 [#33067](https://github.com/pingcap/tidb/issues/33067)

    <!--diagnosis **owner: @mornyx**-->

+ TiKV **owner: @tabokie, TW: @Oreoxmt**

    - 修复 Web 身份提供程序 (web identity provider) 报错并失效后，自动恢复为默认提供程序 (default provider) 时出现权限拒绝的问题 [#13122](https://github.com/tikv/tikv/issues/13122)
    - (dup) 修复 PD 客户端可能会出现死锁的问题 [#13191](https://github.com/tikv/tikv/issues/13191)
    - (dup) 修复 PD Region heartbeat 连接异常中断后未重新连接的问题 [#12934](https://github.com/tikv/tikv/issues/12934)
    - (dup) 修复 Raftstore 线程繁忙时，可能会出现 Region 重叠的问题 [#13160](https://github.com/tikv/tikv/issues/13160)

+ PD **owner: @nolouch, TW: @Oreoxmt**

    - 修复 PD 无法正确处理 dashboard 代理请求的问题 [#5321](https://github.com/tikv/pd/issues/5321)
    - (dup) 修复已清除的 `tombstone store` 信息在切换 PD leader 后再次出现的问题 [#4941](https://github.com/tikv/pd/issues/4941)
    - (dup) 修复 PD 可能没创建 TiFlash Learner 副本的问题 [#5401](https://github.com/tikv/pd/issues/5401)

+ TiFlash **TW: @shichun-0415**

    <!--compute **owner: @zanmato1984**-->

    - (dup) 修复 `format` 函数可能会报 `Data truncated` 错误的问题 [#4891](https://github.com/pingcap/tiflash/issues/4891)
    - (dup) 修复并行聚合出错时可能导致 TiFlash crash 的问题 [#5356](https://github.com/pingcap/tiflash/issues/5356)

    <!--storage **owner: @flowbehappy**-->

    - (dup) 修复使用包含 `NULL` 值的列创建主键时导致崩溃的问题 [#5859](https://github.com/pingcap/tiflash/issues/5859)

+ Tools

    + TiDB Lightning **owner: @niubell, TW: @ran-huang**

        - 修复 `BIGINT` 类型自增列可能越界的问题 [#27397](https://github.com/pingcap/tidb/issues/27937)
        - (dup) 修复极端情况下去重可能会导致 TiDB Lightning panic 的问题 [#34163](https://github.com/pingcap/tidb/issues/34163)
        - (dup) 修复 TiDB Lightning 不支持 Parquet 文件中以斜线 (`/`)、数字、非 ASCII 字符开头的特殊列名的问题 [#36980](https://github.com/pingcap/tidb/issues/36980)
        - (dup) 修复了使用 IPv6 host 时无法连接到 TiDB 的问题 [#35880](https://github.com/pingcap/tidb/issues/35880)

    + TiDB Data Migration (DM) **owner: @niubell, TW: @ran-huang**

        - (dup) 修复 DM Worker 获取 DB 连接时可能卡住的问题 [#3733](https://github.com/pingcap/tiflow/issues/3733)
        - (dup) 修复 DM 报错 `Specified key was too long` 的问题 [#5315](https://github.com/pingcap/tiflow/issues/5315)
        - (dup) 修复数据同步过程中，latin1 字符集数据可能损坏的问题 [#7028](https://github.com/pingcap/tiflow/issues/7028)
        - (dup) 修复 DM IPv6 支持问题 [#6249](https://github.com/pingcap/tiflow/issues/6249)
        - (dup) 修复 `query-status` 内可能存在 data race 的问题 [#4811](https://github.com/pingcap/tiflow/issues/4811)
        - (dup) 修复 relay 报错时可能导致 goroutine 泄露问题 [#6193](https://github.com/pingcap/tiflow/issues/6193)

    + TiCDC **owner: @nongfushanquan, TW: @shichun-0415**

        - (dup) 修复 `enable-old-value = false` 时可能出现的 cdc panic 问题 [#6198](https://github.com/pingcap/tiflow/issues/6198)

    + Backup & Restore (BR) **owner: @3pointer, TW: @shichun-0415**

        - (dup) 修复当外部存储的鉴权 Key 中存在某些特殊符号时，会导致备份恢复失败的问题 [#37469](https://github.com/pingcap/tidb/issues/37469)
        - (dup) 修复在恢复时配置过高的 concurrency 会导致 Region 不均衡的问题 [#37549](https://github.com/pingcap/tidb/issues/37549)

    + Dumpling **owner: @niubell, TW: @ran-huang**

        - (dup) 修复 GetDSN 方法不支持 IPv6 的问题 [#36112](https://github.com/pingcap/tidb/issues/36112)

    + TiDB Binlog
