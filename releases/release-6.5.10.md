---
title: TiDB 6.5.10 Release Notes
summary: 了解 TiDB 6.5.10 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 6.5.10 Release Notes

发版日期：2024 年 6 月 20 日

TiDB 版本：6.5.10

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v6.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v6.5.10#version-list)

## 兼容性变更

- 在之前的版本中，TiCDC 在处理包含 `UPDATE` 变更的事务时，如果事件的主键或者非空唯一索引的列值发生改变，则会将该条事件拆分为 `DELETE` 和 `INSERT` 两条事件。从 v6.5.10 开始，当使用 MySQL Sink 时，如果 `UPDATE` 变更所在事务的 `commitTS` 小于对应表开始向下游同步数据时从 PD 获取的当前时间戳 `thresholdTS`，TiCDC 就会将该 `UPDATE` 事件拆分为 `DELETE` 和 `INSERT` 两条事件，然后写入 Sorter 模块。该行为变更解决了由于 TiCDC 接收到的 `UPDATE` 事件顺序可能不正确，导致拆分后的 `DELETE` 和 `INSERT` 事件顺序也可能不正确，从而引发下游数据不一致的问题。更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb/v6.5/ticdc-split-update-behavior#mysql-sink-拆分-update-事件行为说明)。[#10918](https://github.com/pingcap/tiflow/issues/10918) @[lidezhu](https://github.com/lidezhu)
- 使用 TiDB Lightning 的严格格式 `strict-format` 导入 CSV 文件时，必须设置行分隔符 [#37338](https://github.com/pingcap/tidb/issues/37338) @[lance6716](https://github.com/lance6716)

## 改进提升

+ TiDB

    - 优化表达式默认值在 `SHOW CREATE TABLE` 结果中的 MySQL 兼容性 [#52939](https://github.com/pingcap/tidb/issues/52939) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 在 MPP 负载均衡时移除不包含任何 Region 的 Store [#52313](https://github.com/pingcap/tidb/issues/52313) @[xzhangxian1008](https://github.com/xzhangxian1008)

+ TiKV

    - 加快 TiKV 停机的速度 [#16680](https://github.com/tikv/tikv/issues/16680) @[LykxSassinator](https://github.com/LykxSassinator)
    - 添加 CDC event 的等待处理时长监控指标，便于排查下游 CDC event 延迟问题 [#16282](https://github.com/tikv/tikv/issues/16282) @[hicqu](https://github.com/hicqu)

+ Tools

    + Backup & Restore (BR)

        - BR 在恢复数据过程中，会清理空的 SST 文件 [#16005](https://github.com/tikv/tikv/issues/16005) @[Leavrth](https://github.com/Leavrth)
        - 增加由于 DNS 错误而导致的失败的重试次数 [#53029](https://github.com/pingcap/tidb/issues/53029) @[YuJuncen](https://github.com/YuJuncen)
        - 增加因 Region 没有 leader 导致的失败重试次数 [#54017](https://github.com/pingcap/tidb/issues/54017) @[Leavrth](https://github.com/Leavrth)

    + TiCDC

        - 支持当下游为消息队列 (Message Queue, MQ) 或存储服务时直接输出原始事件 [#11211](https://github.com/pingcap/tiflow/issues/11211) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 提升使用 redo log 恢复数据过程中的内存稳定性，减少 OOM 的概率 [#10900](https://github.com/pingcap/tiflow/issues/10900) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - 显著提升事务冲突场景中的数据同步的稳定性，性能最高提升可达 10 倍 [#10896](https://github.com/pingcap/tiflow/issues/10896) @[CharlesCheung96](https://github.com/CharlesCheung96)

## 错误修复

+ TiDB

    - 修复统计信息初始化过程中对元数据的查询可能导致 OOM 的问题 [#52219](https://github.com/pingcap/tidb/issues/52219) @[hawkingrei](https://github.com/hawkingrei)
    - 修复当表中包含 `AUTO_ID_CACHE=1` 的自增列时，系统变量 `auto_increment_increment` 和 `auto_increment_offset` 配置为非默认值可能导致自增 ID 分配错误的问题 [#52622](https://github.com/pingcap/tidb/issues/52622) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复通过 `RESTORE` 语句恢复 `AUTO_ID_CACHE=1` 的表时，会遇到 `Duplicate entry` 报错的问题 [#52680](https://github.com/pingcap/tidb/issues/52680) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复 `INFORMATION_SCHEMA.TIDB_TRX` 表中 `STATE` 字段的 `size` 未定义导致 `STATE` 显示为空的问题 [#53026](https://github.com/pingcap/tidb/issues/53026) @[cfzjywxk](https://github.com/cfzjywxk)
    - 修复创建带有外键的表时，TiDB 未创建对应的统计信息元信息 (`stats_meta`) 的问题 [#53652](https://github.com/pingcap/tidb/issues/53652) @[hawkingrei](https://github.com/hawkingrei)
    - 修复在查询并发较高时，统计信息同步加载机制可能意外加载失败的问题 [#52294](https://github.com/pingcap/tidb/issues/52294) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 GlobalStats 中的 `Distinct_count` 信息可能错误的问题 [#53752](https://github.com/pingcap/tidb/issues/53752) @[hawkingrei](https://github.com/hawkingrei)
    - 修复重启 TiDB 后，主键列统计信息中的直方图和 TopN 未被加载的问题 [#37548](https://github.com/pingcap/tidb/issues/37548) @[hawkingrei](https://github.com/hawkingrei)
    - 修复查询中的某些过滤条件可能导致 planner 模块发生 `invalid memory address or nil pointer dereference` 报错的问题 [#53582](https://github.com/pingcap/tidb/issues/53582) [#53580](https://github.com/pingcap/tidb/issues/53580) [#53594](https://github.com/pingcap/tidb/issues/53594) [#53603](https://github.com/pingcap/tidb/issues/53603) @[YangKeao](https://github.com/YangKeao)
    - 修复使用 `PREPARE`/`EXECUTE` 方式执行带 `CONV` 表达式的语句，且 `CONV` 表达式包含 `?` 参数时，多次执行可能导致查询结果错误的问题 [#53505](https://github.com/pingcap/tidb/issues/53505) @[qw4990](https://github.com/qw4990)
    - 修复使用 Optimizer Hints 时，可能输出错误的 WARNINGS 信息的问题 [#53767](https://github.com/pingcap/tidb/issues/53767) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 information schema 缓存未命中导致 stale read 查询延迟上升的问题 [#53428](https://github.com/pingcap/tidb/issues/53428) @[crazycs520](https://github.com/crazycs520)
    - 修复 DDL 错误使用 etcd 导致任务排队的问题 [#52335](https://github.com/pingcap/tidb/issues/52335) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复执行 `RENAME INDEX` 语句重命名表达式索引时，内部列未被重命名的问题 [#51431](https://github.com/pingcap/tidb/issues/51431) @[ywqzzy](https://github.com/ywqzzy)
    - 修复并发执行 `CREATE OR REPLACE VIEW` 可能报错 `table doesn't exist` 的问题 [#53673](https://github.com/pingcap/tidb/issues/53673) @[tangenta](https://github.com/tangenta)
    - 修复 JOIN 条件包含隐式类型转换时 TiDB 可能 panic 的问题 [#46556](https://github.com/pingcap/tidb/issues/46556) @[qw4990](https://github.com/qw4990)
    - 修复网络问题导致 DDL 卡住的问题 [#47060](https://github.com/pingcap/tidb/issues/47060) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复 IndexJoin 在 Left Outer Anti Semi 类型下计算哈希值时产生重复行的问题 [#52902](https://github.com/pingcap/tidb/issues/52902) @[yibin87](https://github.com/yibin87)
    - 修复 `ALL` 函数中包含子查询时可能会出现错误结果的问题 [#52755](https://github.com/pingcap/tidb/issues/52755) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 `TIMESTAMPADD()` 函数结果错误的问题 [#41052](https://github.com/pingcap/tidb/issues/41052) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复启用 `tidb_mem_quota_analyze` 时，更新统计信息使用的内存超过限制可能导致 TiDB crash 的问题 [#52601](https://github.com/pingcap/tidb/issues/52601) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 `UPDATE` List 中包含子查询可能会导致 TiDB panic 的问题 [#52687](https://github.com/pingcap/tidb/issues/52687) @[winoros](https://github.com/winoros)
    - 修复 `Longlong` 类型在谓词中溢出的问题 [#45783](https://github.com/pingcap/tidb/issues/45783) @[hawkingrei](https://github.com/hawkingrei)
    - 修复添加唯一索引时并发 DML 导致数据索引不一致的问题 [#52914](https://github.com/pingcap/tidb/issues/52914) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复解析索引数据时可能发生 panic 的问题 [#47115](https://github.com/pingcap/tidb/issues/47115) @[zyguan](https://github.com/zyguan)
    - 修复列裁剪未对数组进行浅拷贝可能导致 TiDB panic 的问题 [#52768](https://github.com/pingcap/tidb/issues/52768) @[winoros](https://github.com/winoros)
    - 修复在递归 CTE 中无法使用视图的问题 [#49721](https://github.com/pingcap/tidb/issues/49721) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 `LEADING` hint 不支持查询块别名 (query block alias) 的问题 [#44645](https://github.com/pingcap/tidb/issues/44645) @[qw4990](https://github.com/qw4990)
    - 修复关联子查询中 TopN 算子结果不正确的问题 [#52777](https://github.com/pingcap/tidb/issues/52777) @[yibin87](https://github.com/yibin87)
    - 修复 `UPDATE` 语句可能因为列的唯一 ID 不稳定导致查询报错的问题 [#53236](https://github.com/pingcap/tidb/issues/53236) @[winoros](https://github.com/winoros)
    - 修复 TiDB 持续发送探活请求到已经下线的 TiFlash 节点的问题 [#46602](https://github.com/pingcap/tidb/issues/46602) @[zyguan](https://github.com/zyguan)
    - 修复 `YEAR` 类型的列与超出范围的无符号整数进行比较导致错误结果的问题 [#50235](https://github.com/pingcap/tidb/issues/50235) @[qw4990](https://github.com/qw4990)
    - 修复在 `AUTO_ID_CACHE=1` 时，AutoID Leader 发生变更可能造成自增列的值减少的问题 [#52600](https://github.com/pingcap/tidb/issues/52600) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复非 `BIGINT` 类型的无符号整数与 `STRING`/`DECIMAL` 比较时可能出现错误结果的问题 [#41736](https://github.com/pingcap/tidb/issues/41736) @[LittleFall](https://github.com/LittleFall)
    - 修复将数据从 `FLOAT` 类型转换为 `UNSIGNED` 类型时结果错误的问题 [#41736](https://github.com/pingcap/tidb/issues/41736) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复 `VAR_SAMP()` 无法作为窗口函数的问题 [#52933](https://github.com/pingcap/tidb/issues/52933) @[hi-rustin](https://github.com/Rustin170506)
    - 修复错误的 TableDual 计划导致查询结果为空的问题 [#50051](https://github.com/pingcap/tidb/issues/50051) @[onlyacat](https://github.com/onlyacat)
    - 修复 TiDB 统计信息同步加载机制无限重试加载空统计信息并打印 `fail to get stats version for this histogram` 日志的问题 [#52657](https://github.com/pingcap/tidb/issues/52657) @[hawkingrei](https://github.com/hawkingrei)
    - 修复空 Projection 导致 TiDB panic 的问题 [#49109](https://github.com/pingcap/tidb/issues/49109) @[winoros](https://github.com/winoros)
    - 修复 TopN 算子可能被错误地下推的问题 [#37986](https://github.com/pingcap/tidb/issues/37986) @[qw4990](https://github.com/qw4990)
    - 修复执行谓词总是为 `true` 的 `SHOW ERRORS` 语句导致 TiDB panic 的问题 [#46962](https://github.com/pingcap/tidb/issues/46962) @[elsa0520](https://github.com/elsa0520)
    - 修复元数据锁在计划缓存场景下未能阻止 DDL 推进的问题 [#51407](https://github.com/pingcap/tidb/issues/51407) @[wjhuang2016](https://github.com/wjhuang2016)

+ TiKV

    - 修复某个 TiKV 节点 check-leader 慢导致其他 TiKV 节点 resolved-ts 无法正常推进的问题 [#15999](https://github.com/tikv/tikv/issues/15999) @[crazycs520](https://github.com/crazycs520)
    - 修复查询中 `CONV()` 函数在进行数制转换时可能 overflow 导致 TiKV panic 的问题 [#16969](https://github.com/tikv/tikv/issues/16969) @[gengliqi](https://github.com/gengliqi)
    - 修复测试用例不稳定的问题，确保每次测试都使用独立的临时目录，从而避免在线配置更改影响其他测试用例 [#16871](https://github.com/tikv/tikv/issues/16871) @[glorv](https://github.com/glorv)
    - 修复 `DECIMAL` 类型的小数部分在某些情况下不正确的问题 [#16913](https://github.com/tikv/tikv/issues/16913) @[gengliqi](https://github.com/gengliqi)
    - 修复由于过时的 Region peer 忽略 GC 消息导致 resolve-ts 被阻塞的问题 [#16504](https://github.com/tikv/tikv/issues/16504) @[crazycs520](https://github.com/crazycs520)

+ PD

    - 修复两数据中心部署切换时 Leader 无法迁移的问题 [#7992](https://github.com/tikv/pd/issues/7992) @[TonsnakeLin](https://github.com/TonsnakeLin)
    - 修复使用 Placement Rules 的情况下，down peer 可能无法恢复的问题 [#7808](https://github.com/tikv/pd/issues/7808) @[rleungx](https://github.com/rleungx)
    - 修复 PD 的 `Filter target` 监控指标未提供 scatter range 信息的问题 [#8125](https://github.com/tikv/pd/issues/8125) @[HuSharp](https://github.com/HuSharp)

+ TiFlash

    - 修复跨数据库执行 `ALTER TABLE ... EXCHANGE PARTITION` 后可能导致 TiFlash 同步 schema 失败的问题 [#7296](https://github.com/pingcap/tiflash/issues/7296) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 key range 为空的查询导致 TiFlash 上没有正确生成读取任务，从而可能阻塞 TiFlash 查询的问题 [#9108](https://github.com/pingcap/tiflash/issues/9108) @[JinheLin](https://github.com/JinheLin)
    - 修复函数 `SUBSTRING_INDEX()` 可能导致 TiFlash Crash 的问题 [#9116](https://github.com/pingcap/tiflash/issues/9116) @[wshwsh12](https://github.com/wshwsh12)
    - 修复从低于 v6.5.0 的集群升级到 v6.5.0 及以上版本后，可能出现 TiFlash 元数据损坏以及进程 panic 的问题 [#9039](https://github.com/pingcap/tiflash/issues/9039) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 TiFlash 在高并发读的情况下，可能返回瞬时不正确结果的问题 [#8845](https://github.com/pingcap/tiflash/issues/8845) @[JinheLin](https://github.com/JinheLin)

+ Tools

    + Backup & Restore (BR)

        - 修复测试用例 `TestGetTSWithRetry` 执行时间过长的问题 [#52547](https://github.com/pingcap/tidb/issues/52547) @[Leavrth](https://github.com/Leavrth)
        - 修复在 BR 恢复数据或 TiDB Lightning 物理导入模式下导入数据时，从 PD 获取到的 Region 没有 Leader 的问题 [#51124](https://github.com/pingcap/tidb/issues/51124) [#50501](https://github.com/pingcap/tidb/issues/50501) @[Leavrth](https://github.com/Leavrth)
        - 修复 PD 连接失败导致日志备份 advancer owner 所在的 TiDB 可能崩溃的问题 [#52597](https://github.com/pingcap/tidb/issues/52597) @[YuJuncen](https://github.com/YuJuncen)
        - 修复日志备份在暂停、停止、再重建任务操作后，虽然任务状态显示正常，但 Checkpoint 不推进的问题 [#53047](https://github.com/pingcap/tidb/issues/53047) @[RidRisR](https://github.com/RidRisR)
        - 修复由于某个 TiKV 节点缺少 Leader 导致数据恢复变慢的问题 [#50566](https://github.com/pingcap/tidb/issues/50566) @[Leavrth](https://github.com/Leavrth)
        - 修复因 TiKV 重启，日志备份的 global checkpoint 推进提前于实际备份文件写入点，可能导致少量备份数据丢失的问题 [#16809](https://github.com/tikv/tikv/issues/16809) @[YuJuncen](https://github.com/YuJuncen)
        - 修复 PD leader 发生迁移可能导致恢复数据时 panic 的问题 [#53724](https://github.com/pingcap/tidb/issues/53724) @[Leavrth](https://github.com/Leavrth)
        - 修复恢复暂停的日志备份任务时，如果与 PD 的网络连接不稳定可能导致 TiKV panic 的问题 [#17020](https://github.com/tikv/tikv/issues/17020) @[YuJuncen](https://github.com/YuJuncen)
        - 修复日志备份在 advancer owner 发生迁移后可能被暂停的问题 [#53561](https://github.com/pingcap/tidb/issues/53561) @[RidRisR](https://github.com/RidRisR)
        - 修复在恢复过程中，由于多层重试导致 BR 无法正确识别错误的问题 [#54053](https://github.com/pingcap/tidb/issues/54053) @[RidRisR](https://github.com/RidRisR)

    + TiCDC

        - 修复下游数据库密码以 Base64 编码时启用 Syncpoint 功能的 Changefeed 创建失败的问题 [#10516](https://github.com/pingcap/tiflow/issues/10516) @[asddongmen](https://github.com/asddongmen)
        - 修复没有正确同步 `DROP PRIMARY KEY` 和 `DROP UNIQUE KEY` 的问题 [#10890](https://github.com/pingcap/tiflow/issues/10890) @[asddongmen](https://github.com/asddongmen)
        - 修复 `TIMEZONE` 类型的值没有按照正确的时区设置默认值的问题 [#10931](https://github.com/pingcap/tiflow/issues/10931) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Lightning

        - 修复 TiDB Lightning 导入数据时，kill PD Leader 会导致 `invalid store ID 0` 报错的问题 [#50501](https://github.com/pingcap/tidb/issues/50501) @[Leavrth](https://github.com/Leavrth)
        - 修复 TiDB Lightning Grafana 面板缺失数据的问题 [#43357](https://github.com/pingcap/tidb/issues/43357) @[lichunzhu](https://github.com/lichunzhu)
        - 修复 TiDB Lightning 在服务器模式下可能会将敏感信息打印到日志中的问题 [#36374](https://github.com/pingcap/tidb/issues/36374) @[kennytm](https://github.com/kennytm)
        - 修复使用 TiDB Lightning 导入同时设置了 `SHARD_ROW_ID_BITS` 和 `AUTO_ID_CACHE=1` 的数据表后，无法生成自增 ID 并报错 `Failed to read auto-increment value from storage engine` 的问题 [#52654](https://github.com/pingcap/tidb/issues/52654) @[D3Hunter](https://github.com/D3Hunter)

    + Dumpling

        - 修复 Dumpling 在同时导出表和视图时报错的问题 [#53682](https://github.com/pingcap/tidb/issues/53682) @[tangenta](https://github.com/tangenta)

    + TiDB Binlog

        - 修复开启 TiDB Binlog 后，在 `ADD COLUMN` 执行过程中删除行可能报错 `data and columnID count not match` 的问题 [#53133](https://github.com/pingcap/tidb/issues/53133) @[tangenta](https://github.com/tangenta)
