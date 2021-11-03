---
title: TiDB 5.3 Release Notes
---

# TiDB 5.3 Release Notes

发版日期：2021 年 11 月 16 日

TiDB 版本：5.3.0

在 5.3 版本中，你可以获得以下关键特性：

+ 
+ 
+ 

## 兼容性变化

> **注意：**
>
> 当从一个早期的 TiDB 版本升级到 TiDB 5.3.0 时，如需了解所有中间版本对应的兼容性更改说明，请查看对应版本的 [Release Note](/releases/release-notes.md)。

### 系统变量

|  变量名    |  修改类型    |  描述    |
| :---------- | :----------- | :----------- |
|  |  |  |
|  |  |  |
|  |  |  |

### 配置文件参数

|  配置文件    |  配置项    |  修改类型    |  描述    |
| :---------- | :----------- | :----------- | :----------- |
|  |  |  |
|  |  |  |
|  |  |  |

### 其他

- 
- 
- 
- 

## 新功能

### SQL

- **功能 1**

    <功能描述 （功能是什么 + 能给用户带来什么好处 + 需要用户注意什么）>

    <功能支持情况，TiDB 默认开启还是关闭此功能，如果默认关闭，如何开启>

    <如果功能限制或此功能特定的兼容性问题，需要提及>

    [用户文档](/)

- **功能 2**

    <功能描述 （功能是什么 + 能给用户带来什么好处 + 需要用户注意什么）>

    <功能支持情况，TiDB 默认开启还是关闭此功能，如果默认关闭，如何开启>

    <如果功能限制或此功能特定的兼容性问题，需要提及>

    [用户文档](/)    

### 事务

- **功能 3**

    <功能描述 （功能是什么 + 能给用户带来什么好处 + 需要用户注意什么）>

    <功能支持情况，TiDB 默认开启还是关闭此功能，如果默认关闭，如何开启>

    <如果功能限制或此功能特定的兼容性问题，需要提及>

    [用户文档](/)    

### 字符集和排序规则

- **功能 4**

    <功能描述 （功能是什么 + 能给用户带来什么好处 + 需要用户注意什么）>

    <功能支持情况，TiDB 默认开启还是关闭此功能，如果默认关闭，如何开启>

    <如果功能限制或此功能特定的兼容性问题，需要提及>

    [用户文档](/)   

### 安全

- **功能 5**

    <功能描述 （功能是什么 + 能给用户带来什么好处 + 需要用户注意什么）>

    <功能支持情况，TiDB 默认开启还是关闭此功能，如果默认关闭，如何开启>

    <如果功能限制或此功能特定的兼容性问题，需要提及>

    [用户文档](/)   

## 性能优化

- **提升 TiFlash 实时分析能力**

    - 降低远端数据读取的开销，减少网络传输量
    - 大幅优化 TiFlash TableScan 算子的执行效率
    - 新增更多的函数支持，提升
        - 新增运算符支持：LIKE expression
        - 新增若干字符串函数支持：FORMAT(), LOWER(), LTRIM(), RTRIM(), SUBSTRING_INDEX(), TRIM(), UCASE(), UPPER()
        - 新增数学函数支持：ROUND(decimal, int)
        - 新增若干日期时间函数支持：HOUR(), MICROSECOND(), MINUTE(), SECOND(), SYSDATE()
        - 新增 CAST 函数支持：CAST(time, real)
        - 新增若干聚合函数支持：GROUP_CONCAT(), SUM(enum)

    - 支持在非 Linux 平台上，使用 Dashboard 查看硬件信息

    [用户文档](/)  

## 稳定性提升

- **提升 TiFlash 稳定性**

    - 优化在高负载下查询容易超时的问题
    - 优化 TiFlash 日志搜索性能，避免搜索大体量日志（大于 10GB）时出现的卡顿或失败现象
    - 加强数据历史版本的回收策略
    - 使用 TiUP 重启或升级多个 TiFlash 节点时，提升了滚动重启 TiFlash 进程过程中的服务稳定性

- **功能 8**

    <功能描述 （功能是什么 + 能给用户带来什么好处 + 需要用户注意什么）>

    <功能支持情况，TiDB 默认开启还是关闭此功能，如果默认关闭，如何开启>

    <如果功能限制或此功能特定的兼容性问题，需要提及>

    [用户文档](/)  

## 高可用和容灾

- **功能 9**

    <功能描述 （功能是什么 + 能给用户带来什么好处 + 需要用户注意什么）>

    <功能支持情况，TiDB 默认开启还是关闭此功能，如果默认关闭，如何开启>

    <如果功能限制或此功能特定的兼容性问题，需要提及>

    [用户文档](/)  

## 数据迁移

- **支持部署多个 TiDB Lightning**

    新版本 TiDB Lightning 支持用户同时部署多个 Lightning，并行地将单表或者多表数据迁移 TiDB。 该功能无需特别的配置，在不改变用户使用习惯的同时，极大提高了用户的数据迁移能力，助力大数据量业务架构升级，在生产环境使用 TiDB。

    在产品性能测试中，使用 x 个 Lightning 导入整体大小 x TB MySQL 分表数据到 TiDB 单表，总耗时 x h，平均单台 Lightning 速度达到 x GB/h。（数据待更新）

    [用户文档](/)  

- **提高 DM 复制性能**

    支持以下功能，实现以更低的延迟将数据从 MySQL 同步数据到 TiDB。

    - 合并单行数据的多次变更（Compact multiple updates on a single row into one statement）
    - 点查更新合并为批量操作（Merge batch updates of multiple rows into one statement）
    - 异步保存检查点（Async Checkpoint）

- **增加 DM 的 OpenAPI 以更方便地管理集群**

    <功能描述 （DM 的 OpenAPI 是什么 + 能给用户带来什么好处 + 需要用户注意什么）>

    <功能支持情况，TiDB 默认开启还是关闭此功能，如果默认关闭，如何开启>

    <如果功能限制或此功能特定的兼容性问题，需要提及>

    [用户文档](/)  

- **Lightning 支持导入 GBK 编码文件** 

    [用户文档](/tidb-lightning-configuration.md)

- **Lightning 支持忽略部分错误行**

    <能给用户带来什么好处>

## TiDB 数据共享订阅

- **功能 10**

    <功能描述 （功能是什么 + 能给用户带来什么好处 + 需要用户注意什么）>

    <功能支持情况，TiDB 默认开启还是关闭此功能，如果默认关闭，如何开启>

    <如果功能限制或此功能特定的兼容性问题，需要提及>

    [用户文档](/)  

## 问题诊断效率

- **功能 10**

    <功能描述 （功能是什么 + 能给用户带来什么好处 + 需要用户注意什么）>

    <功能支持情况，TiDB 默认开启还是关闭此功能，如果默认关闭，如何开启>

    <如果功能限制或此功能特定的兼容性问题，需要提及>

    [用户文档](/)  

## 部署及运维

- **持续性能分析**

    TiDB Dashboard 引入持续性能分析功能，提供在集群运行状态时自动保存实例性能分析结果的能力，通过火焰图的形式提高了 TiDB 集群性能的可观测性，有助于缩短故障诊断时间。

    该功能默认关闭，需进入 TiDB Dashboard 持续性能分析页面开启。

    持续性能分析功能必须使用 TiUP 1.7.0 及以上版本升级或安装的集群才可使用。

    [用户文档](/)  

## 遥测

TiDB 在遥测中新增收集 <列出本次新增遥测内容>。

若要了解所收集的信息详情及如何禁用该行为，请参见[遥测](/telemetry.md)文档。

## 提升改进

+ TiDB

    - 当 coprocessor 遇到锁时，在调试日志中显示受影响的 SQL 语句帮助诊断问题 [#27718](https://github.com/pingcap/tidb/issues/27718)
    - 在 SQL 逻辑层备份和恢复数据时，支持显示备份和恢复数据的大小 [#27247](https://github.com/pingcap/tidb/issues/27247)

+ TiKV

    - 简化 L0 层流控算法 [#10879](https://github.com/tikv/tikv/issues/10879)
    - 优化 raft client 错误日志的收集 [#10983](https://github.com/tikv/tikv/pull/10983)
    - 优化日志线程以避免其成为性能瓶颈 [#10841](https://github.com/tikv/tikv/issues/10841)
    - 添加更多的写入查询统计类型 [#10507](https://github.com/tikv/tikv/issues/10507)

+ PD

    - 热点调度器的 QPS 维度支持更多的写请求类型 [#3869](https://github.com/tikv/pd/issues/3869)
    - 通过动态调整 Balance Region 调度器的重试上限，优化该调度器的性能 [#3744](https://github.com/tikv/pd/issues/3744)
    - 将 TiDB Dashboard 升级至 v2021.10.08.1 [#4070](https://github.com/tikv/pd/pull/4070)
    - 允许 Evict Leader 调度器调度拥有不健康副本的 Region [#4093](https://github.com/tikv/pd/issues/4093)
    - 优化调度器退出的速度 [#4146](https://github.com/tikv/pd/issues/4146)

+ Tools

    + TiCDC

        - 通过修改 Kafka sink 配置项 `MaxMessageBytes` 的默认值，由 64 MB 减小为 1 MB，以修复消息过大会被 Kafka Broker 拒收的问题 [#3104](https://github.com/pingcap/ticdc/pull/3104)
        - 减少同步链路中的内存占用 [#2553](https://github.com/pingcap/ticdc/issues/2553)[#3037](https://github.com/pingcap/ticdc/pull/3037) [#2726](https://github.com/pingcap/ticdc/pull/2726) 
        - 优化监控项和告警规则，提升了同步链路、内存 GC、存量数据扫描过程的可观测性 [#2735](https://github.com/pingcap/ticdc/pull/2735) [#1606](https://github.com/pingcap/ticdc/issues/1606) [#3000](https://github.com/pingcap/ticdc/pull/3000) [#2985](https://github.com/pingcap/ticdc/issues/2985) [#2156](https://github.com/pingcap/ticdc/issues/2156)
        - 当同步任务状态正常时，不再显示历史错误信息，避免误导用户 [#2242](https://github.com/pingcap/ticdc/issues/2242)

## Bug 修复

+ TiDB

    - 修复在分区中下推聚合算子时，因浅拷贝 schema 列导致执行计划出错，进而导致执行时报错的问题 [#27797](https://github.com/pingcap/tidb/issues/27797) [#26554](https://github.com/pingcap/tidb/issues/26554)
    - 修复 `plan cache` 无法感知 `unsigned` 标志变化的问题 [#28254](https://github.com/pingcap/tidb/issues/28254)
    - 修复当分区功能出现 `out of range` 时 `partition pruning` 出错的问题 [#28233](https://github.com/pingcap/tidb/issues/28233)
    - 修复在某些情况下 Planner 可能缓存无效 `join` 计划的问题 [#28087](https://github.com/pingcap/tidb/issues/28087)
    - 修复 hash 列为 `enum` 时构建错误 `IndexLookUpJoin` 的问题 [#27893](https://github.com/pingcap/tidb/issues/27893)
    - 修复批处理客户端在某些罕见情况下回收空闲连接可能会阻塞发送请求的问题 [#27688](https://github.com/pingcap/tidb/pull/27688)
    - 修复当 TiDB Lightning 在目标集群上执行校验失败时 panic 的问题 [#27686](https://github.com/pingcap/tidb/pull/27686)
    - 修复某些情况下 `date_add` 和 `date_sub` 函数执行结果错误的问题 [#27232](https://github.com/pingcap/tidb/issues/27232)
    - 修复 `hour` 函数在向量化表达式中执行结果错误的问题 [#28643](https://github.com/pingcap/tidb/issues/28643)
    - 修复连接到 MySQL 5.1 或更早的客户端时存在的认证问题 [#27855](https://github.com/pingcap/tidb/issues/27855)
    - 修复当新增索引时自动分析可能会在指定时间之外触发的问题 [#28698](https://github.com/pingcap/tidb/issues/28698)
    - 修复设置任何会话变量都会使 `tidb_snapshot` 失效的问题 [#28683](https://github.com/pingcap/tidb/pull/28683)
    - 修复在有大量 `miss-peer region` 的集群中 BR 不可用的问题 [#27534](https://github.com/pingcap/tidb/issues/27534)
    - 修复当不支持的 `cast` 被下推到 TiFlash 时出现的非预期错误，例如 `tidb_cast to Int32 is not supported` [#23907](https://github.com/pingcap/tidb/issues/23907)
    - 修复 `%s value is out of range in '%s'` 报错中缺失 `DECIMAL overflow` 信息的问题 [#27964](https://github.com/pingcap/tidb/issues/27964)
    - 修复 MPP 节点的可用性检测在某些边界场景中无法工作的问题 [#3118](https://github.com/pingcap/tics/issues/3118)
    - 修复分配 `MPP task ID` 时出现 `DATA RACE` 的问题 [#27952](https://github.com/pingcap/tidb/issues/27952)
    - 修复删除空的 `dual table` 后 MPP 查询出现 `index out of range` 报错的问题 [#28250](https://github.com/pingcap/tidb/issues/28250)
    - 修复运行 MPP 查询时出现 `invalid cop task execution summaries length` 相关日志的问题 [#1791](https://github.com/pingcap/tics/issues/1791)
    - 修复运行 MPP 查询时出现 `cannot found column in Schema column` 报错的问题 [#28149](https://github.com/pingcap/tidb/pull/28149)
    - 修复 TiDB 在 TiFlash 关闭时可能出现 panic 的问题 [#28096](https://github.com/pingcap/tidb/issues/28096)
    - 移除对基于 3DES (三重数据加密算法) 不安全的 TLS 加密套件的支持 [#27859](https://github.com/pingcap/tidb/pull/27859)
    - 修复因 Lightning 前置检查会连接已下线的 TiKV 节点而导致导入失败的问题 [#27826](https://github.com/pingcap/tidb/pull/27826)
    - 修复在导入太多文件到表时前置检查花费太多时间的问题 [#27605](https://github.com/pingcap/tidb/issues/27605)
    - 修复表达式重写时 `between` 推断出错误排序规则的问题 [#27146](https://github.com/pingcap/tidb/issues/27146)
    - 修复 `group_concat` 函数没有考虑排序规则的问题 [#27429](https://github.com/pingcap/tidb/issues/27429)
    - 修复 `extract` 函数处理负值时的问题 [#27236](https://github.com/pingcap/tidb/issues/27236)
    - 修复当设置 `NO_UNSIGNED_SUBTRACTION` 时创建分区失败的问题 [#26765](https://github.com/pingcap/tidb/issues/26765)
    - 避免在列修剪和聚合下推中使用有副作用的表达式 [#27106](https://github.com/pingcap/tidb/issues/27106)
    - 删除无用的 gRPC 日志 [#24190](https://github.com/pingcap/tidb/issues/24190)
    - 限制有效的小数点长度以修复精度相关的问题 [3091](https://github.com/pingcap/tics/issues/3091)
    - 修复 `plus` 表达式中检查溢出方法出错的问题 [26977](https://github.com/pingcap/tidb/issues/26977)
    - 修复当导出带有 `new collation` 数据的表的统计信息时报 `data too long` 错误的问题 [27024](https://github.com/pingcap/tidb/issues/27024)
    - 修复 `TIDB_TRX` 中不包含重试事务的问题 [28670](https://github.com/pingcap/tidb/pull/28670)

+ TiKV

    - 修复 Region 迁移时 Raftstore 模块出现死锁导致 TiKV 不可用的问题。用户可通过关闭调度并重启出问题的 TiKV 来临时应对。[#10909](https://github.com/tikv/tikv/issues/10909)
    - 修复因 Congest 错误而导致的 CDC 频繁增加 scan 重试的问题 [#11082](https://github.com/tikv/tikv/issues/11082)
    - 修复因 channel 打满而导致的 Raft 断连情况 [#11047](https://github.com/tikv/tikv/issues/11047)
    - 修复 Raft client 中 batch 消息过大的问题 [#9714](https://github.com/tikv/tikv/issues/9714)
    - 修复 `resolved_ts` 中协程泄漏的问题 [#10965](https://github.com/tikv/tikv/issues/10965)
    - 修复当 response 大小超过 4 GiB 时 Coprocessor panic 的问题 [#9012](https://github.com/tikv/tikv/issues/9012)
    - 修复当一个 snapshot 文件无法被垃圾清理 (GC) 时 snapshot GC 会缺失 GC snapshot 文件的问题 [#10813](https://github.com/tikv/tikv/issues/10813)
    - 修复当处理 Coprocessor 请求时因超时而导致 panic 的问题 [#10852](https://github.com/tikv/tikv/issues/10852)

+ PD

    - 修复因超过副本配置数量而导致错误删除带有数据且处于 pending 状态的副本的问题 [#4045](https://github.com/tikv/pd/issues/4045)
    - 修复 PD 未能及时修复 Down Peer 副本的问题 [#4077](https://github.com/tikv/pd/issues/4077)
    - 修复 Scatter Range 调度器无法对空 Region 进行调度的问题 [#4118](https://github.com/tikv/pd/pull/4118)
    - 修复 key manager 占用过多 CPU 的问题 [#4071](https://github.com/tikv/pd/issues/4071)
    - 修复热点调度器变更配置的过程中可能会存在的数据竞争问题 [#4159](https://github.com/tikv/pd/issues/4159)
    - 修复因 Region syncer 卡住而导致 leader 选举慢的问题 [#3936](https://github.com/tikv/pd/issues/3936)

+ TiFlash

    - 修复 TiFlash 在部分平台上由于缺失 `nsl` 库而无法启动的问题

+ Tools

    + TiCDC

        - 修复当上游 TiDB 实例意外退出时，TiCDC 同步任务推进可能停滞的问题 [#3061](https://github.com/pingcap/ticdc/issues/3061)
        - 修复当 TiKV 向同一 Region 发送重复请求时，TiCDC 进程 panic 的问题 [#2386](https://github.com/pingcap/ticdc/issues/2386)
        - 修复在验证下游 TiDB/MySQL 可用性时产生的不必要的 CPU 消耗 [#3073](https://github.com/pingcap/ticdc/issues/3073)
        - 修复 TiCDC 产生的 Kafka 消息体积不受 `max-message-size` 约束的问题 [#2962](https://github.com/pingcap/ticdc/issues/2962)
        - 修复当写入 Kafka 消息发生错误时，TiCDC 同步任务推进可能停滞的问题 [#2978](https://github.com/pingcap/ticdc/issues/2978)
        - 修复当开启 `force-replicate` 时，可能某些没有有效索引的分区表被忽略的问题 [#2834](https://github.com/pingcap/ticdc/issues/2834)
        - 修复当扫描存量数据耗时过长时，可能由于 TiKV 进行 GC 而导致存量数据扫描失败的问题 [#2470](https://github.com/pingcap/ticdc/issues/2470)
        - 修复在将某些类型的列编码为 Open Protocol 格式时，TiCDC 进程可能 panic 的问题 [#2758](https://github.com/pingcap/ticdc/issues/2758)
        - 修复在将某些类型的列编码为 Avro 格式时，TiCDC 进程可能 panic 的问题 [#2648](https://github.com/pingcap/ticdc/issues/2648)
    
    + TiDB Binlog

        - 修复当大部分表被过滤掉时，在某些特殊的负载下，checkpoint 不更新的问题 [#1075](https://github.com/pingcap/tidb-binlog/pull/1075)