---
title: TiDB 5.1.5 Release Notes
summary: TiDB 5.1.5 发布日期为 2022 年 12 月 28 日。此版本包含 PD 默认关闭编译 swagger server 的兼容性变更以及 TiDB、TiKV、PD、TiFlash 和 Tools 中的多项 Bug 修复。修复内容涵盖了窗口函数执行、动态模式、函数传入值计算、left join 删除数据、SQL 语句计算、连接错误、索引错误、HTTP 服务异常、并发列类型变更、空闲链接、SESSION 变量、Region 合并、KV client 连接、TiDB Binlog 错误、TiKV 运行、Raftstore 线程、Region merge、Follower Read、Async Commit、网络问题、Unified Read Pool CPU 表达式、TLS、并行聚合、查询错误、日期格式、MPP query、数据回收、逻辑运算符、备份系统表、增量扫描、Sorter 组件监控数据和 ddl schema 缓存优化。
---

# TiDB 5.1.5 Release Notes

发版日期：2022 年 12 月 28 日

TiDB 版本：5.1.5

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v5.1/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v5.1/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/)

## 兼容性变更

+ PD

    - 默认关闭编译 swagger server [#4932](https://github.com/tikv/pd/issues/4932)

## Bug 修复

+ TiDB

    - 修复窗口函数执行时本应报错但是让 TiDB 崩溃的问题 [#30326](https://github.com/pingcap/tidb/issues/30326)
    - 修复在 TiFlash 中为分区表开启动态模式时结果出错的问题 [#37254](https://github.com/pingcap/tidb/issues/37254)
    - 修复当 `GREATEST` 和 `LEAST`  函数传入无符号整型值时，计算结果出错的问题 [#30101](https://github.com/pingcap/tidb/issues/30101)
    - 修复使用 left join 同时删除多张表数据时可能出现错误结果的问题 [#31321](https://github.com/pingcap/tidb/issues/31321)
    - 修复 `concat(ifnull(time(3)))` 的结果与 MySQL 不一致的问题 [#29498](https://github.com/pingcap/tidb/issues/29498)
    - 修复 SQL 语句中包含 `cast(integer as char) union string` 时计算结果出错的问题 [#29513](https://github.com/pingcap/tidb/issues/29513)
    - 修复 `INL_HASH_JOIN` 和 `LIMIT` 一起使用时可能会卡住的问题 [#35638](https://github.com/pingcap/tidb/issues/35638)
    - 修复当有 Region 返回空数据时 `ANY_VALUE` 结果不正确的问题 [#30923](https://github.com/pingcap/tidb/issues/30923)
    - 修复 innerWorker panic 导致的 index join 结果错误的问题 [#31494](https://github.com/pingcap/tidb/issues/31494)
    - 修复当 SQL 语句中存在 JSON 类型列与 `CHAR` 类型列连接时，SQL 出错的问题 [#29401](https://github.com/pingcap/tidb/issues/29401)
    - 修复 TiDB 的后台 HTTP 服务可能没有正确关闭导致集群状态异常的问题 [#30571](https://github.com/pingcap/tidb/issues/30571)
    - 修复并发的列类型变更导致 schema 与数据不一致的问题 [#31048](https://github.com/pingcap/tidb/issues/31048)
    - 修复 `KILL TIDB` 在空闲链接上无法立即生效的问题 [#24031](https://github.com/pingcap/tidb/issues/24031)
    - 修复设置 SESSION 变量会导致 `tidb_snapshot` 不工作的问题 [#35515](https://github.com/pingcap/tidb/issues/35515)
    - 修复 Region 合并情况下 Region cache 没有及时被清理的问题 [#37141](https://github.com/pingcap/tidb/issues/37141)
    - 修复因为 KV client 中连接数据争用导致的 panic 问题 [#33773](https://github.com/pingcap/tidb/issues/33773)
    - 修复在开启 TiDB Binlog 时，TiDB 执行 `ALTER SEQUENCE` 会产生错误的元信息版本号，进而导致 Drainer 报错退出的问题 [#36276](https://github.com/pingcap/tidb/issues/36276)
    - 修复 TiDB 由于 `fatal error: concurrent map read and map write` 发生崩溃的问题 [#35340](https://github.com/pingcap/tidb/issues/35340)
    - 修复在 TiFlash 不支持使用空范围读表的情况，依然选择 TiFlash 导致查询结果错误的问题 [#33083](https://github.com/pingcap/tidb/issues/33083)
    - 修复当从 TiFlash 查询 `avg()` 函数时，返回错误 `ERROR 1105 (HY000): other error for mpp stream: Could not convert to the target type - -value is out of range.` 的问题 [#29952](https://github.com/pingcap/tidb/issues/29952)
    - 修复查询 HashJoin 时，返回错误 `ERROR 1105 (HY000): close of nil channel` 的问题 [#30289](https://github.com/pingcap/tidb/issues/30289)
    - 修复 TiKV 和 TiFlash 在进行逻辑运算时结果不一致的问题 [#37258](https://github.com/pingcap/tidb/issues/37258)
    - 修复某些情况下，`EXECUTE` 语句可能抛出非预期异常的问题 [#37187](https://github.com/pingcap/tidb/issues/37187)
    - 修复了 `tidb_opt_agg_push_down` 和 `tidb_enforce_mpp` 启用时执行处理器的错误行为 [#34465](https://github.com/pingcap/tidb/issues/34465)
    - 修复 TiDB 在执行 `SHOW COLUMNS` 时会发出协处理器请求的问题 [#36496](https://github.com/pingcap/tidb/issues/36496)
    - 当 `enable-table-lock` 参数未开启时为 `lock tables` 和 `unlock tables` 新增警告 [#28967](https://github.com/pingcap/tidb/issues/28967)
    - 修复 Range 分区允许多个 `MAXVALUE` 分区的问题 [#36329](https://github.com/pingcap/tidb/issues/36329)

+ TiKV

    - 修复了 `DATETIME` 类型的数据包含小数部分和 `Z` 后缀导致检查报错的问题 [#12739](https://github.com/tikv/tikv/issues/12739)
    - 修复 replica read 可能违反线性一致性的问题 [#12109](https://github.com/tikv/tikv/issues/12109)
    - 修复 Raftstore 线程繁忙时，可能会出现 Region 重叠的问题 [#13160](https://github.com/tikv/tikv/issues/13160)
    - 修复 apply snapshot 被暂停时会引起 TiKV panic 的问题 [#11618](https://github.com/tikv/tikv/issues/11618)
    - 修复 TiKV 运行 2 年以上可能 panic 的问题 [#11940](https://github.com/tikv/tikv/issues/11940)
    - 修复在 Region merge 时 source peer 通过 snapshot 追日志时可能导致 panic 的问题 [#12663](https://github.com/tikv/tikv/issues/12663)
    - 修复了对空字符串进行类型转换导致 TiKV panic 的问题 [#12673](https://github.com/tikv/tikv/issues/12673)
    - 修复旧信息造成 TiKV panic 的问题 [#12023](https://github.com/tikv/tikv/issues/12023)
    - 修复同时分裂和销毁一个 peer 时可能导致 panic 的问题 [#12825](https://github.com/tikv/tikv/issues/12825)
    - 修复合并 Region 时因 target peer 被一个未进行初始化就被销毁的 peer 所替换，从而引起 TiKV panic 的问题 [#12048](https://github.com/tikv/tikv/issues/12048)
    - 修复进行 Follower Read 时，可能会报 `invalid store ID 0` 错误的问题 [#12478](https://github.com/tikv/tikv/issues/12478)
    - 修复了在悲观事务中使用 Async Commit 导致重复提交记录的问题 [#12615](https://github.com/tikv/tikv/issues/12615)
    - 支持配置 `unreachable_backoff` 避免 Raftstore 发现某个 Peer 无法连接时广播过多消息 [#13054](https://github.com/tikv/tikv/issues/13054)
    - 修复网络出现问题的情况下，已成功提交的乐观事务可能报 `Write Conflict` 错误的问题 [#34066](https://github.com/pingcap/tidb/issues/34066)
    - 修复 Dashboard 中 Unified Read Pool CPU 表达式错误的问题 [#13086](https://github.com/tikv/tikv/issues/13086)

+ PD

    - 修复已清除的 `tombstone store` 信息在切换 PD leader 后再次出现的问题 [#4941](https://github.com/tikv/pd/issues/4941)
    - 修复 PD leader 转移后调度不能立即启动的问题 [#4769](https://github.com/tikv/pd/issues/4769)
    - 修复 `not leader` 的 status code 有误的问题 [#4797](https://github.com/tikv/pd/issues/4797)
    - 修复 PD 无法正确处理 dashboard 代理请求的问题 [#5321](https://github.com/tikv/pd/issues/5321)
    - 修复在某些特殊情况下 TSO fallback 的问题 [#4884](https://github.com/tikv/pd/issues/4884)
    - 修复 PD 在特定条件下不会创建 TiFlash Learner 副本的问题 [#5401](https://github.com/tikv/pd/issues/5401)
    - 修复监控信息中已删除 label 的残留问题 [#4825](https://github.com/tikv/pd/issues/4825)
    - 修复存在较大空间 Store 时（例如 2T），无法检测满的小空间 Store，从而无法进行平衡调度的问题 [#4805](https://github.com/tikv/pd/issues/4805)
    - 修复 `SchedulerMaxWaitingOperator` 设置为 `1` 时不产生调度的问题 [#4946](https://github.com/tikv/pd/issues/4946)

+ TiFlash

    - 修复转换 string 类型为 datetime 类型时，`microsecond` 结果可能不正确的问题 [#3556](https://github.com/pingcap/tiflash/issues/3556)
    - 修复启用 TLS 时可能导致的崩溃 [#4196](https://github.com/pingcap/tiflash/issues/4196)
    - 修复并行聚合出错时可能导致 TiFlash crash 的问题 [#5356](https://github.com/pingcap/tiflash/issues/5356)
    - 修复在执行带有 `JOIN` 的查询遇到错误时可能被挂起的问题 [#4195](https://github.com/pingcap/tiflash/issues/4195)
    - 修复 `OR` 函数计算结果错误的问题 [#5849](https://github.com/pingcap/tiflash/issues/5849)
    - 修复错误地配置存储目录会导致非预期行为的问题 [#4093](https://github.com/pingcap/tiflash/issues/4093)
    - 修复大量 INSERT 和 DELETE 操作后可能导致 TiFlash 数据不一致的问题 [#4956](https://github.com/pingcap/tiflash/issues/4956)
    - 修复 TiFlash 节点上遗留了与 Region range 不匹配的数据的问题 [#4414](https://github.com/pingcap/tiflash/issues/4414)
    - 修复在读取工作量大时添加列后可能出现的查询错误 [#3967](https://github.com/pingcap/tiflash/issues/3967)
    - 修复由于 `commit state jump backward` 错误导致 TiFlash 反复崩溃的问题 [#2576](https://github.com/pingcap/tiflash/issues/2576)
    - 修复查询存在大量 delete 操作的表时可能报错的问题 [#4747](https://github.com/pingcap/tiflash/issues/4747)
    - 修复日期格式将 `''` 处理为非法分隔符的问题 [#4036](https://github.com/pingcap/tiflash/issues/4036)
    - 修复将 `DATETIME` 转换为 `DECIMAL` 时结果错误的问题 [#4151](https://github.com/pingcap/tiflash/issues/4151)
    - 修复一些异常没有被正确地处理的问题 [#4101](https://github.com/pingcap/tiflash/issues/4101)
    - 修复 `Prepare Merge` 可能导致 raft 状态机元数据损坏，从而引起 TiFlash 重启的问题 [#3435](https://github.com/pingcap/tiflash/issues/3435)
    - 修复 MPP query 会随机碰到 gRPC keepalive timeout 导致 query 失败的问题 [#4662](https://github.com/pingcap/tiflash/issues/4662)
    - 修复 `IN` 函数的结果在多值表达式中不正确的问题 [#4016](https://github.com/pingcap/tiflash/issues/4016)
    - 修复 MPP 任务可能永远泄漏线程的问题 [#4238](https://github.com/pingcap/tiflash/issues/4238)
    - 修复过期数据回收缓慢的问题 [#4146](https://github.com/pingcap/tiflash/issues/4146)
    - 修复将 `FLOAT` 类型转换为 `DECIMAL` 类型可能造成溢出的问题 [#3998](https://github.com/pingcap/tiflash/issues/3998)
    - 修复逻辑运算符在 UInt8 类型下查询结果出错的问题 [#6127](https://github.com/pingcap/tiflash/issues/6127)
    - 修复 `json_length` 对空字符串可能会报 `index out of bounds` 错误的问题 [#2705](https://github.com/pingcap/tiflash/issues/2705)
    - 修复极端情况下 decimal 比较结果可能有误的问题 [#4512](https://github.com/pingcap/tiflash/issues/4512)
    - 修复在添加一些 `NOT NULL` 的列时报 `TiFlash_schema_error` 的问题 [#4596](https://github.com/pingcap/tiflash/issues/4596)
    - 修复由于使用 `0.0` 作为整数类型的默认值导致 TiFlash 节点失败的问题，比如`` `i` int(11) NOT NULL DEFAULT '0.0'`` [#3157](https://github.com/pingcap/tiflash/issues/3157)

+ Tools

    + TiDB Binlog

        - 修复 `compressor` 设为 `gzip` 时 Drainer 无法正确发送请求至 Pump 的问题 [#1152](https://github.com/pingcap/tidb-binlog/issues/1152)

    + Backup & Restore (BR)

        - 修复因为并发备份系统表，导致表名更新失败，无法恢复系统表的问题 [#29710](https://github.com/pingcap/tidb/issues/29710)

    + TiCDC

        - 修复了增量扫描特殊场景下的数据丢失问题 [#5468](https://github.com/pingcap/tiflow/issues/5468)
        - 修复 Sorter 组件缺失监控数据的问题 [#5690](https://github.com/pingcap/tiflow/issues/5690)
        - 优化了 ddl schema 缓存方式，降低了内存消耗 [#1386](https://github.com/pingcap/tiflow/issues/1386)
