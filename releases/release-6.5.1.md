---
title: TiDB 6.5.1 Release Notes
summary: 了解 TiDB 6.5.1 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 6.5.1 Release Notes

发版日期：2023 年 3 月 10 日

TiDB 版本：6.5.1

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v6.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v6.5.1#version-list)

## 兼容性变更

- 自 2023 年 2 月 20 日起，新发布的 TiDB 和 TiDB Dashboard 版本（包含 6.5.1），默认关闭[遥测功能](/telemetry.md)，即默认不再收集使用情况信息分享给 PingCAP。如果升级至这些版本前使用默认的遥测配置，则升级后遥测功能处于关闭状态。具体的版本可参考 [TiDB 版本发布时间线](/releases/release-timeline.md)。

    - 系统变量 [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-从-v402-版本开始引入) 默认值由 `ON` 修改为 `OFF`。
    - TiDB 配置项 [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-从-v402-版本开始引入) 默认值由 `true` 改为 `false`。
    - PD 配置项 [`enable-telemetry`](/pd-configuration-file.md#enable-telemetry) 默认值由 `true` 改为 `false`。

- 从 v1.11.3 起，新部署的 TiUP 默认关闭遥测功能，即默认不再收集使用情况信息。如果从 v1.11.3 之前的 TiUP 版本升级至 v1.11.3 或更高 TiUP 版本，遥测保持升级前的开启或关闭状态。

- 由于可能存在正确性问题，分区表目前不再支持修改列类型 [#40620](https://github.com/pingcap/tidb/issues/40620) @[mjonss](https://github.com/mjonss)

- TiKV 配置项 [`advance-ts-interval`](/tikv-configuration-file.md#advance-ts-interval) 默认值由 `1s` 修改为 `20s`。你可以通过调整该配置项提高 Stale Read 数据的时效性（即减少延时），详情参见[减少 Stale Read 延时](/stale-read.md#减少-stale-read-延时)。

- TiKV 配置项 [`cdc.min-ts-interval`](/tikv-configuration-file.md#min-ts-interval) 的默认值由 `"200ms"` 修改为 `"1s"`，以减少网络流量。

## 改进提升

+ TiDB

    - 从 v6.5.1 起，由 **v1.4.3 或以上版本的 TiDB Operator** 部署的 TiDB 全栈支持 IPv6 地址，这意味着 TiDB 可以支持更大的地址空间，并提供更好的安全性和网络性能。

        - 完全支持 IPv6 寻址：TiDB 支持使用 IPv6 地址进行所有网络连接，包括客户端连接、节点之间的内部通信以及与外部系统的通信。
        - 双栈支持：如果你尚未准备好完全切换到 IPv6，TiDB 也支持双栈网络。这意味着你可以在同一个 TiDB 集群中使用 IPv4 和 IPv6 地址，可以通过配置 IPv6 优先的方式来选择网络部署模式。

      IPv6 部署相关信息，请参考 [TiDB on Kubernetes 用户文档](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/configure-a-tidb-cluster#ipv6-支持)。

    - 支持指定集群初次启动时的初始化 SQL 脚本 [#35624](https://github.com/pingcap/tidb/issues/35624) @[morgo](https://github.com/morgo)

        TiDB v6.5.1 新增 [`initialize-sql-file`](https://docs.pingcap.com/zh/tidb/v6.5/tidb-configuration-file#initialize-sql-file-从-v651-版本开始引入) 配置项。集群初次启动时，你可通过命令行参数 `--initialize-sql-file` 指定执行的 SQL 脚本。该功能可用于修改系统变量的值、创建用户或分配权限等。更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb/v6.5/tidb-configuration-file#initialize-sql-file-从-v651-版本开始引入)。

    - 定期清理过期的 Region 缓存，避免内存泄漏和性能下降问题 [#40461](https://github.com/pingcap/tidb/issues/40461) @[sticnarf](https://github.com/sticnarf)
    - 新增 `--proxy-protocol-fallbackable` 配置项，控制是否启用 PROXY 协议回退模式。如果设置为 `true`，TiDB 可以接受非 PROXY 协议规范或者没有发送 PROXY 协议头的客户端连接 [#41409](https://github.com/pingcap/tidb/issues/41409) @[blacktear23](https://github.com/blacktear23)
    - 提升了 Memory Tracker 的准确度 [#40900](https://github.com/pingcap/tidb/issues/40900) [#40500](https://github.com/pingcap/tidb/issues/40500) @[wshwsh12](https://github.com/wshwsh12)
    - 当执行计划缓存无法生效时，系统会通过 Warning 返回原因 [#40210](https://github.com/pingcap/tidb/pull/40210) @[qw4990](https://github.com/qw4990)
    - 改进了条件优化器在进行越界估算时的策略 [#39008](https://github.com/pingcap/tidb/issues/39008) @[time-and-fate](https://github.com/time-and-fate)

+ TiKV

    - 支持在小于 1 core 的 CPU 下启动 TiKV [#13586](https://github.com/tikv/tikv/issues/13586) [#13752](https://github.com/tikv/tikv/issues/13752) [#14017](https://github.com/tikv/tikv/issues/14017) @[andreid-db](https://github.com/andreid-db)
    - 将 Unified Read Pool 的线程上限 (`readpool.unified.max-thread-count`) 提高至 CPU 配额的 10 倍 [#13690](https://github.com/tikv/tikv/issues/13690) @[v01dstar](https://github.com/v01dstar)
    - 为了节省跨域流量，`resolved-ts.advance-ts-interval` 的默认值从 `"1s"` 修改为 `"20s"` [#14100](https://github.com/tikv/tikv/issues/14100) @[overvenus](https://github.com/overvenus)

+ TiFlash

    - 显著提升 TiFlash 在大数据量下的启动速度 [#6395](https://github.com/pingcap/tiflash/issues/6395) @[hehechen](https://github.com/hehechen)

+ Tools

    + Backup & Restore (BR)

        - 优化 TiKV 端下载日志备份文件的并发度，提升常规场景下 PITR 恢复的性能 [#14206](https://github.com/tikv/tikv/issues/14206) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - 默认打开 pull-based sink 功能提升系统的吞吐 [#8232](https://github.com/pingcap/tiflow/issues/8232) @[hi-rustin](https://github.com/Rustin170506)
        - 支持将 redo log 存储至兼容 GCS 或 Azure 协议的对象存储 [#7987](https://github.com/pingcap/tiflow/issues/7987) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 采用异步模式实现 MQ sink 和 MySQL sink，提升 sink 的吞吐能力 [#5928](https://github.com/pingcap/tiflow/issues/5928) @[amyangfei](https://github.com/amyangfei) @[CharlesCheung96](https://github.com/CharlesCheung96)

## 错误修复

+ TiDB

    - 修复 [`pessimistic-auto-commit`](/tidb-configuration-file.md#pessimistic-auto-commit) 配置项对 "Point Get" 查询不生效的问题 [#39928](https://github.com/pingcap/tidb/issues/39928) @[zyguan](https://github.com/zyguan)
    - 修复 `INSERT` 或 `REPLACE` 语句在长会话连接中执行可能造成 Panic 的问题 [#40351](https://github.com/pingcap/tidb/issues/40351) @[fanrenhoo](https://github.com/fanrenhoo)
    - 修复了 `auto analyze` 导致 graceful shutdown 耗时长的问题 [#40038](https://github.com/pingcap/tidb/issues/40038) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - 修复了 DDL 在 ingest 过程中可能会发生数据竞争的问题 [#40970](https://github.com/pingcap/tidb/issues/40970) @[tangenta](https://github.com/tangenta)
    - 修复了添加索引时可能导致数据竞争的问题 [#40879](https://github.com/pingcap/tidb/issues/40879) @[tangenta](https://github.com/tangenta)
    - 修复了表 Region 比较多时因 Region 缓存失效导致加索引效率低下的问题 [#38436](https://github.com/pingcap/tidb/issues/38436) @[tangenta](https://github.com/tangenta)
    - 修复了 TiDB 在初始化时有可能死锁的问题 [#40408](https://github.com/pingcap/tidb/issues/40408) @[Defined2014](https://github.com/Defined2014)
    - 修复了 TiDB 构造 key 范围时对 `NULL` 值处理不当，导致读取非预期数据的问题 [#40158](https://github.com/pingcap/tidb/issues/40158) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复了内存重用导致的在某些情况下系统变量的值会被错误修改的问题 [#40979](https://github.com/pingcap/tidb/issues/40979) @[lcwangchao](https://github.com/lcwangchao)
    - 修复了在执行 TTL 任务时，如果表的主键包含 `ENUM` 类型的列任务会失败的问题 [#40456](https://github.com/pingcap/tidb/issues/40456) @[lcwangchao](https://github.com/lcwangchao)
    - 修复了在添加唯一索引时有可能会 panic 的问题 [#40592](https://github.com/pingcap/tidb/issues/40592) @[tangenta](https://github.com/tangenta)
    - 修复了并发 truncate 同一张表时，部分 truncate 操作无法被 MDL 阻塞的问题 [#40484](https://github.com/pingcap/tidb/issues/40484) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复了当动态裁剪模式下的分区表有 global binding 时，TiDB 重启失败的问题 [#40368](https://github.com/pingcap/tidb/issues/40368) @[Yisaer](https://github.com/Yisaer)
    - 修复使用 "Cursor Read" 方式读取数据时可能因为 GC 而报错的问题 [#39447](https://github.com/pingcap/tidb/issues/39447) @[zyguan](https://github.com/zyguan)
    - 修复 `SHOW PROCESSLIST` 信息中未显示 `EXECUTE` 语句的问题 [#41156](https://github.com/pingcap/tidb/issues/41156) @[YangKeao](https://github.com/YangKeao)
    - 修复了 `globalMemoryControl` 在终止查询时可能会遇上 `KILL` 不结束的问题 [#41057](https://github.com/pingcap/tidb/issues/41057) @[wshwsh12](https://github.com/wshwsh12)
    - 修复了 `indexMerge` 遇到错误后可能会导致 TiDB 崩溃的问题 [#41047](https://github.com/pingcap/tidb/issues/41047) [#40877](https://github.com/pingcap/tidb/issues/40877) @[guo-shaoge](https://github.com/guo-shaoge) @[windtalker](https://github.com/windtalker)
    - 修复 `ANALYZE` 语句可能会被 `KILL` 终止的问题 [#41825](https://github.com/pingcap/tidb/issues/41825) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - 修复了 `indexMerge` 中可能会出现 goroutine 泄露的问题 [#41545](https://github.com/pingcap/tidb/issues/41545) [#41605](https://github.com/pingcap/tidb/issues/41605) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复了无符号的 `TINYINT`/`SMALLINT`/`INT` 和小于 `0` 的 `DECIMAL`/`FLOAT`/`DOUBLE` 类型比较时，结果可能出错的问题 [#41736](https://github.com/pingcap/tidb/issues/41736) @[LittleFall](https://github.com/LittleFall)
    - 修复了开启系统变量 `tidb_enable_reuse_chunk` 后可能会出现内存泄露的问题 [#40987](https://github.com/pingcap/tidb/issues/40987) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复了时区中的数据争用可能导致数据和索引不一致问题 [#40710](https://github.com/pingcap/tidb/issues/40710) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复了 `batch cop` 在执行过程中的 scan detail 信息不准确的问题 [#41582](https://github.com/pingcap/tidb/issues/41582) @[you06](https://github.com/you06)
    - 修复 `cop` 并发度上限不受限制的问题 [#41134](https://github.com/pingcap/tidb/issues/41134) @[you06](https://github.com/you06)
    - 修复 `cursor read` 中 `statement context` 被错误缓存的问题 [#39998](https://github.com/pingcap/tidb/issues/39998) @[zyguan](https://github.com/zyguan)
    - 周期性清理过时的 Region 缓存以避免内存泄露和性能倒退 [#40355](https://github.com/pingcap/tidb/issues/40355) @[sticnarf](https://github.com/sticnarf)
    - 修复对包含 `year <cmp> const` 的查询使用 Plan Cache 时结果可能出错的问题 [#41628](https://github.com/pingcap/tidb/issues/41628) @[qw4990](https://github.com/qw4990)
    - 修复查询区间太多且数据改动量大时估算误差可能较大的问题 [#39593](https://github.com/pingcap/tidb/issues/39593) @[time-and-fate](https://github.com/time-and-fate)
    - 修复使用 Plan Cache 时部分条件无法被下推通过 Join 算子的问题 [#40093](https://github.com/pingcap/tidb/issues/40093) [#38205](https://github.com/pingcap/tidb/issues/38205) @[qw4990](https://github.com/qw4990)
    - 修复 IndexMerge 计划在 SET 类型列上可能生成错误区间的问题 [#41273](https://github.com/pingcap/tidb/issues/41273) [#41293](https://github.com/pingcap/tidb/issues/41293) @[time-and-fate](https://github.com/time-and-fate)
    - 修复 Plan Cache 处理 `int_col <cmp> decimal` 条件时可能缓存 FullScan 计划的问题 [#40679](https://github.com/pingcap/tidb/issues/40679) [#41032](https://github.com/pingcap/tidb/issues/41032) @[qw4990](https://github.com/qw4990)
    - 修复 Plan Cache 处理 `int_col in (decimal...)` 条件时可能缓存 FullScan 计划的问题 [#40224](https://github.com/pingcap/tidb/issues/40224) @[qw4990](https://github.com/qw4990)
    - 修复 `ignore_plan_cache` hint 对 INSERT 语句可能不生效的问题 [#40079](https://github.com/pingcap/tidb/issues/40079) [#39717](https://github.com/pingcap/tidb/issues/39717) @[qw4990](https://github.com/qw4990)
    - 修复 Auto Analyze 可能阻碍 TiDB 退出的问题 [#40038](https://github.com/pingcap/tidb/issues/40038) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - 修复在分区表的 Unsigned Primary Key 上可能构造错误访问区间的问题 [#40309](https://github.com/pingcap/tidb/issues/40309) @[winoros](https://github.com/winoros)
    - 修复 Plan Cache 可能缓存 Shuffle 算子导致返回错误结果的问题 [#38335](https://github.com/pingcap/tidb/issues/38335) @[qw4990](https://github.com/qw4990)
    - 修复在分区表上创建 Global Binding 后可能导致 TiDB 启动错误的问题 [#40368](https://github.com/pingcap/tidb/issues/40368) @[Yisaer](https://github.com/Yisaer)
    - 修复慢日志中查询计划算子可能缺失的问题 [#41458](https://github.com/pingcap/tidb/issues/41458) @[time-and-fate](https://github.com/time-and-fate)
    - 修复错误下推包含虚拟列的 TopN 算子到 TiKV 或 TiFlash 导致结果错误的问题 [#41355](https://github.com/pingcap/tidb/issues/41355) @[Dousir9](https://github.com/Dousir9)
    - 修复添加索引时数据不一致的问题 [#40698](https://github.com/pingcap/tidb/issues/40698) [#40730](https://github.com/pingcap/tidb/issues/40730) [#41459](https://github.com/pingcap/tidb/issues/41459) [#40464](https://github.com/pingcap/tidb/issues/40464) [#40217](https://github.com/pingcap/tidb/issues/40217) @[tangenta](https://github.com/tangenta)
    - 修复添加索引时出现 `PessimisticLockNotFound` 的报错问题 [#41515](https://github.com/pingcap/tidb/issues/41515) @[tangenta](https://github.com/tangenta)
    - 修复添加唯一索引时误报重复键的问题 [#41630](https://github.com/pingcap/tidb/issues/41630) @[tangenta](https://github.com/tangenta)
    - 修复 TiDB 使用 `paging` 时性能下降的问题 [#40741](https://github.com/pingcap/tidb/issues/40741) @[solotzg](https://github.com/solotzg)

+ TiKV

    - 修复 Resolved TS 导致网络流量升高的问题 [#14092](https://github.com/tikv/tikv/issues/14092) @[overvenus](https://github.com/overvenus)
    - 修复 TiDB 中事务在执行悲观 DML 失败后，再执行其他 DML 时，如果 TiDB 和 TiKV 之间存在网络故障，可能会造成数据不一致的问题 [#14038](https://github.com/tikv/tikv/issues/14038) @[MyonKeminta](https://github.com/MyonKeminta)
    - 修复转换 `const Enum` 类型到其他类型时报错的问题 [#14156](https://github.com/tikv/tikv/issues/14156) @[wshwsh12](https://github.com/wshwsh12)
    - 修复 cop task 分页计算错误的问题 [#14254](https://github.com/tikv/tikv/issues/14254) @[you06](https://github.com/you06)
    - 修复 `batch cop` 模式下 `scan_detail` 不准确问题 [#14109](https://github.com/tikv/tikv/issues/14109) @[you06](https://github.com/you06)
    - 修复 Raft Engine 中的一个潜在错误，该错误可能导致 TiKV 检测到 Raft 数据损坏而无法重启 [#14338](https://github.com/tikv/tikv/issues/14338) @[tonyxuqqi](https://github.com/tonyxuqqi)

+ PD

    - 修复 `replace-down-peer` 在特定条件下执行变慢的问题 [#5788](https://github.com/tikv/pd/issues/5788) @[HundunDM](https://github.com/HunDunDM)
    - 修复 PD 可能会非预期地向 Region 添加多个 Learner 的问题 [#5786](https://github.com/tikv/pd/issues/5786) @[HunDunDM](https://github.com/HunDunDM)
    - 修复 Region Scatter 任务会生成非预期的多余副本的问题 [#5909](https://github.com/tikv/pd/issues/5909) @[HundunDM](https://github.com/HunDunDM)
    - 修复调用 `ReportMinResolvedTS` 过于频繁导致 PD OOM 的问题 [#5965](https://github.com/tikv/pd/issues/5965) @[HundunDM](https://github.com/HunDunDM)
    - 修复 Region Scatter 接口可能导致 leader 分布不均匀的问题 [#6017](https://github.com/tikv/pd/issues/6017) @[HunDunDM](https://github.com/HunDunDM)

+ TiFlash

    - 修复半连接在计算笛卡尔积时，使用内存过量的问题 [#6730](https://github.com/pingcap/tiflash/issues/6730) @[gengliqi](https://github.com/gengliqi)
    - 修复 TiFlash 日志搜索过慢的问题 [#6829](https://github.com/pingcap/tiflash/issues/6829) @[hehechen](https://github.com/hehechen)
    - 修复 TiFlash 在反复重启后由于误删文件而无法启动的问题 [#6486](https://github.com/pingcap/tiflash/issues/6486) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 TiFlash 在添加新列后查询可能报错的问题 [#6726](https://github.com/pingcap/tiflash/issues/6726) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 TiFlash 配置不支持 IPv6 的问题 [#6734](https://github.com/pingcap/tiflash/issues/6734) @[ywqzzy](https://github.com/ywqzzy)

+ Tools

    + Backup & Restore (BR)

        - 修复 PD 与 TiDB server 的连接故障导致 PITR 备份进度不推进的问题 [#41082](https://github.com/pingcap/tidb/issues/41082) @[YuJuncen](https://github.com/YuJuncen)
        - 修复 PD 与 TiKV 的连接故障导致 TiKV 不能监听 PITR 任务的问题 [#14159](https://github.com/tikv/tikv/issues/14159) @[YuJuncen](https://github.com/YuJuncen)
        - 修复 PITR 不支持 PD 集群配置变更的问题 [#14165](https://github.com/tikv/tikv/issues/14165) @[YuJuncen](https://github.com/YuJuncen)
        - 修复 PITR 功能不支持 CA-bundle 认证的问题 [#38775](https://github.com/pingcap/tidb/issues/38775) @[3pointer](https://github.com/3pointer)
        - 修复 PITR 备份任务被删除时，存在备份信息残留导致新任务出现数据不一致的问题 [#40403](https://github.com/pingcap/tidb/issues/40403) @[joccau](https://github.com/joccau)
        - 修复使用 `br debug` 命令解析 backupmeta 文件导致的 panic 的问题 [#40878](https://github.com/pingcap/tidb/issues/40878) @[MoCuishle28](https://github.com/MoCuishle28)
        - 修复在某些情况下因无法获取 Region 大小导致恢复失败的问题 [#36053](https://github.com/pingcap/tidb/issues/36053) @[YuJuncen](https://github.com/YuJuncen)
        - 修复当 TiDB 集群不存在 PITR 备份任务时，`resolve lock` 频率过高的问题 [#40759](https://github.com/pingcap/tidb/issues/40759) @[joccau](https://github.com/joccau)
        - 修复恢复数据到正在运行日志备份的集群，导致日志备份文件无法恢复的问题 [#40797](https://github.com/pingcap/tidb/issues/40797) @[Leavrth](https://github.com/Leavrth)
        - 修复全量备份失败后，从断点重启备份时 BR 会 panic 的问题 [#40704](https://github.com/pingcap/tidb/issues/40704) @[Leavrth](https://github.com/Leavrth)
        - 修复 PITR 错误被覆盖的问题 [#40576](https://github.com/pingcap/tidb/issues/40576) @[Leavrth](https://github.com/Leavrth)
        - 修复 PITR 备份任务在 advance owner 与 gc owner 不同时 checkpoint 不推进的问题 [#41806](https://github.com/pingcap/tidb/issues/41806) @[joccau](https://github.com/joccau)

    + TiCDC

        - 修复 changefeed 在 TiKV、TiCDC 节点扩缩容等特殊场景下卡住的问题 [#8174](https://github.com/pingcap/tiflow/issues/8174) @[hicqu](https://github.com/hicqu)
        - 修复 redo log 存储路径没做权限预检查的问题 [#6335](https://github.com/pingcap/tiflow/issues/6335) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复 redo log 容忍 S3 存储故障的时间过短的问题 [#8089](https://github.com/pingcap/tiflow/issues/8089) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复不能通过配置文件修改 `transaction_atomicity` 和 `protocol` 参数的问题 [#7935](https://github.com/pingcap/tiflow/issues/7935) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复在同步大量表时 checkpoint 不推进问题 [#8004](https://github.com/pingcap/tiflow/issues/8004) @[overvenus](https://github.com/overvenus)
        - 修复当同步的延迟过大时 apply redo log 可能会出现 OOM 的问题 [#8085](https://github.com/pingcap/tiflow/issues/8085) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复当开启 redo log 写 meta 时性能下降的问题 [#8074](https://github.com/pingcap/tiflow/issues/8074) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 修复没有配置大事务拆分时，同步数据超过 context deadline 的问题 [#7982](https://github.com/pingcap/tiflow/issues/7982) @[hi-rustin](https://github.com/Rustin170506)
        - 修复在 PD 异常时，暂停一个 changefeed 会错误设置状态的问题 [#8330](https://github.com/pingcap/tiflow/issues/8330) @[sdojjy](https://github.com/sdojjy)
        - 修复下游为 TiDB 或 MySQL 时，无主键且非空唯一索引所在列指定了 CHARACTER SET 同步时可能会出现数据不一致的问题 [#8420](https://github.com/pingcap/tiflow/issues/8420) @[asddongmen](https://github.com/asddongmen)
        - 修复 table scheduling 或 blackhole sink 存在 panic 的问题 [#8024](https://github.com/pingcap/tiflow/issues/8024) [#8142](https://github.com/pingcap/tiflow/issues/8142) @[hicqu](https://github.com/hicqu)

    + TiDB Data Migration (DM)

        - 修复 `binlog-schema delete` 命令执行失败的问题 [#7373](https://github.com/pingcap/tiflow/issues/7373) @[liumengya94](https://github.com/liumengya94)
        - 修复当最后一个 binlog 是被 skip 的 DDL 时，checkpoint 不推进的问题 [#8175](https://github.com/pingcap/tiflow/issues/8175) @[D3Hunter](https://github.com/D3Hunter)
        - 修复当在某个表上同时指定 `UPDATE` 和非 `UPDATE` 类型的表达式过滤规则 `expression-filter` 时，所有 `UPDATE` 操作被跳过的问题 [#7831](https://github.com/pingcap/tiflow/issues/7831) @[lance6716](https://github.com/lance6716)

    + TiDB Lightning

        - 修复 precheck 检查项有时无法监测到之前的导入失败遗留的脏数据的问题 [#39477](https://github.com/pingcap/tidb/issues/39477) @[dsdashun](https://github.com/dsdashun)
        - 修复 TiDB Lightning 在 split-region 阶段发生 panic 的问题 [#40934](https://github.com/pingcap/tidb/issues/40934) @[lance6716](https://github.com/lance6716)
        - 修复冲突处理逻辑 (`duplicate-resolution`) 可能导致 checksum 不一致的问题 [#40657](https://github.com/pingcap/tidb/issues/40657) @[sleepymole](https://github.com/sleepymole)
        - 修复在并行导入时，当除最后一个 TiDB Lightning 实例外的其他实例都遇到本地重复记录时，TiDB Lightning 可能会错误地跳过冲突处理的问题 [#40923](https://github.com/pingcap/tidb/issues/40923) @[lichunzhu](https://github.com/lichunzhu)
        - 修复了在使用 Local Backend 模式导入数据时，当导入目标表的复合主键中存在 `auto_random` 列，且源数据中没有指定该列的值时，相关列没有自动生成数据的问题 [#41454](https://github.com/pingcap/tidb/issues/41454) @[D3Hunter](https://github.com/D3Hunter)
