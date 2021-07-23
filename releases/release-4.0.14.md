---
title: TiDB 4.0.14 Release Notes
---

# TiDB 4.0.14 Release Notes

发版日期：2021 年 7 月 22 日

TiDB 版本：4.0.14

## 兼容性更改

+ TiDB

    - 在 v4.0 中将 `tidb_multi_statement_mode` 的默认值从 `WARN` 更改为 `OFF`。建议使用客户端库的多语句功能，参考[`tidb_multi_statement_mode` 文档](/system-variables.md#tidb_multi_statement_mode-从-v4011-版本开始引入)。[#25749](https://github.com/pingcap/tidb/pull/25749)
    - 将 Grafana 从 v6.1.16 升级到 v7.5.7 以解决两个安全漏洞，参考 [Grafana 博文](https://grafana.com/blog/2020/06/03/grafana-6.7.4-and-7.0.2-released-with-important-security-fix/)。
    - 将系统变量 `tidb_stmt_summary_max_stmt_count` 的默认值从 `200` 修改为 `3000` [#25872](https://github.com/pingcap/tidb/pull/25872)

+ TiKV

    - 将 `merge-check-tick-interval` 配置项的默认值从 `10` 修改为 `2` 以加快 Region 合并的速度 [#9676](https://github.com/tikv/tikv/pull/9676)

## 功能增强

+ TiKV

    - 添加监控项 `pending` 用以监控 pending PD 心跳，帮助定位 PD 线程变慢的问题 [#10008](https://github.com/tikv/tikv/pull/10008)
    - 支持 virtual-host 风格的地址来让 BR 兼容类 S3 储存 [#10242](https://github.com/tikv/tikv/pull/10242)

+ TiDB Dashboard

    - 新增 OIDC SSO 支持。通过设置兼容 OIDC 标准的 SSO 服务（例如 Okta、Auth0 等），用户可以在不输入 SQL 密码的情况下登录 TiDB Dashboard [#960](https://github.com/pingcap/tidb-dashboard/pull/960)
    - 新增 **Debug API** 界面用于高级调试，通过该界面可以替代命令行方式来调用 TiDB 和 PD 的内部调试性 API [#927](https://github.com/pingcap/tidb-dashboard/pull/927)

## 改进提升

+ TiDB

    - 对于 point/batch point get 算子，在唯一索引写入过程中，将悲观锁 LOCK 记录转化为 PUT 记录 [#26223](https://github.com/pingcap/tidb/pull/26223)
    - 支持 MySQL 的系统变量 `init_connect` 及其相关功能 [#26031](https://github.com/pingcap/tidb/pull/26031)
    - 支持稳定结果模式，使查询结果更稳定 [#26003](https://github.com/pingcap/tidb/pull/26003)
    - 支持将函数 `json_unquote()` 下推到 TiKV [#25721](https://github.com/pingcap/tidb/pull/25721)
    - 使 SQL 计划管理 (SPM) 不受字符集的影响 [#23295](https://github.com/pingcap/tidb/pull/23295)

+ TiKV

    - 关闭 TiKV 时，优先关闭 status server 来确保客户端可以正确检测关闭状态 [#10504](https://github.com/tikv/tikv/pull/10504)
    - 响应过期副本的消息，以确保过期副本被更快清除 [#10400](https://github.com/tikv/tikv/pull/10400)
    - 限制 TiCDC sink 的内存消耗 [#10147](https://github.com/tikv/tikv/pull/10147)
    - 当 Region 太大时，使用均匀分裂来加快分裂速度 [#10275](https://github.com/tikv/tikv/pull/10275)

+ PD

    - 减少各调度器在同时工作时产生的冲突 [#3854](https://github.com/tikv/pd/pull/3854)

+ TiDB Dashboard

    - 更新 TiDB Dashboard 版本至 v2021.07.17.1 [#3882](https://github.com/pingcap/pd/pull/3882)
    - 支持将当前会话分享为只读的会话，禁止对分享的会话进行修改操作 [#960](https://github.com/pingcap/tidb-dashboard/pull/960)

+ Tools

    + Backup & Restore (BR)

        - 恢复数据时合并小文件以提升恢复速度 [#655](https://github.com/pingcap/br/pull/655)

    + Dumpling

        - 上游是 TiDB v3.x 集群时，使用 `_tidb_rowid` 来切分表以减少 TiDB 的内存使用 [#306](https://github.com/pingcap/dumpling/pull/306)

    + TiCDC

        - 优化 PD 节点缺失证书时的报错信息 [#2184](https://github.com/pingcap/ticdc/pull/2184)
        - 优化 sorter I/O 报错信息 [#1976](https://github.com/pingcap/ticdc/pull/1976)
        - 在 KV client 中新增 Region 增量扫描的并发度上限，减小 TiKV 的压力 [#1926](https://github.com/pingcap/ticdc/pull/1926)
        - 新增表内存使用量的监控项 [#1884](https://github.com/pingcap/ticdc/pull/1884)
        - 新增 TiCDC 服务端配置项 `capture-session-ttl` [#2169](https://github.com/pingcap/ticdc/pull/2169)

## Bug 修复

+ TiDB

    - 修复当连接一个带 `WHERE` 条件的子查询（值为 `false`）时 `SELECT` 的结果与 MySQL 不兼容的问题 [#24865](https://github.com/pingcap/tidb/issues/24865)
    - 修复当参数是 `ENUM` 或 `SET` 类型时 `ifnull` 函数计算错误的问题 [#24944](https://github.com/pingcap/tidb/issues/24944)
    - 修复某些情况下错误的聚合函数消除 [#25202](https://github.com/pingcap/tidb/issues/25202)
    - 修复 Merge Join 运算中当列为 `SET` 类型时可能产生错误结果的问题 [#25669](https://github.com/pingcap/tidb/issues/25669)
    - 修复 Cartesian Join 运算返回错误结果的问题 [#25591](https://github.com/pingcap/tidb/issues/25591)
    - 修复 `SELECT ... FOR UPDATE` 语句进行连接运算且连接使用分区表时，可能产生异常退出情况的问题 [#20028](https://github.com/pingcap/tidb/issues/20028)
    - 修复缓存的 `prepared` 计划被错误用于 `point get` 的问题 [#24741](https://github.com/pingcap/tidb/issues/24741)
    - 修复 `LOAD DATA` 语句可以不正常导入非 utf8 数据的问题 [#25979](https://github.com/pingcap/tidb/issues/25979)
    - 修复通过 HTTP API 访问统计信息时，可能导致内存泄露的问题 [#24650](https://github.com/pingcap/tidb/pull/24650)
    - 修复执行 `ALTER USER` 语句时出现的安全性问题 [#25225](https://github.com/pingcap/tidb/issues/25225)
    - 修复系统表 `TIKV_REGION_PEERS` 不能正确处理 `DOWN` 状态的问题 [#24879](https://github.com/pingcap/tidb/issues/24879)
    - 修复解析 `DateTime` 不截断非法字符串的问题 [#22231](https://github.com/pingcap/tidb/issues/22231)
    - 修复 `select into outfile` 语句在列类型是 `YEAR` 时，可能无法产生结果的问题 [#22159](https://github.com/pingcap/tidb/issues/22159)

+ TiKV

    - 修复特定平台上的 duration 计算可能崩溃的问题 [#related-issue](https://github.com/rust-lang/rust/issues/86470#issuecomment-877557654)
    - 修复将 `DOUBLE` 类型转换为 `DOUBLE` 的错误函数 [#25200](https://github.com/pingcap/tidb/issues/25200)
    - 修复使用 async logger 时 panic 日志可能会丢失的问题 [#8998](https://github.com/tikv/tikv/issues/8998)
    - 修复开启加密后再次生成同样的 snapshot 会出现 panic 的问题 [#10462](https://github.com/tikv/tikv/pull/10462)
    - 修复 coprocessor 中 `json_unquote()` 函数错误的参数类型 [#10176](https://github.com/tikv/tikv/issues/10176)
    - 修复关机期间出现的可疑警告和来自 Raftstore 的非确定性响应 [#10353](https://github.com/tikv/tikv/issues/10353) [#10307](https://github.com/tikv/tikv/issues/10307)
    - 修复备份线程泄漏的问题 [#10287](https://github.com/tikv/tikv/issues/10287)
    - 修复 Region split 过慢以及进行 Region merge 时，Region split 可能会损坏 metadata 的问题 [#8456](https://github.com/tikv/tikv/issues/8456) [#8783](https://github.com/tikv/tikv/issues/8783)
    - 修复特定情况下 Region 心跳会导致 TiKV 不进行 split 的问题 [#10111](https://github.com/tikv/tikv/issues/10111)
    - 修复 TiKV 和 TiDB 间 CM Sketch 格式不一致导致统计信息错误问题 [#25638](https://github.com/pingcap/tidb/issues/25638)
    - 修复 `apply wait duration` 指标的错误统计 [#9893](https://github.com/tikv/tikv/issues/9893)
    - 修复使用 Titan 时 `delete_files_in_range` 以后可能会产生 "Missing Blob" 报错的问题 [#10232](https://github.com/tikv/tikv/pull/10232)

+ PD

    - 修复调度器在执行删除操作后可能再次出现的问题 [#2572](https://github.com/tikv/pd/issues/2572)
    - 修复调度器在临时配置加载完毕前启动可能导致数据争用的问题 [#3771](https://github.com/tikv/pd/issues/3771)
    - 修复打散 Region 操作可能导致 PD panic 的问题 [#3761](https://github.com/pingcap/pd/pull/3761)
    - 修复部分 Operator 未被正确设置优先级的问题 [#3703](https://github.com/pingcap/pd/pull/3703)
    - 修复从不存在的 Store 上删除 `evict-leader` 调度器时可能导致 PD panic 的问题 [#3660](https://github.com/tikv/pd/issues/3660)
    - 修复了当集群内 Store 非常多时，PD 切换 Leader 慢的问题 [#3697](https://github.com/tikv/pd/issues/3697)

+ TiDB Dashboard

    - 修复实例性能分析界面无法获取全部 TiDB 实例信息的问题 [#944](https://github.com/pingcap/tidb-dashboard/pull/944)
    - 修复 SQL 语句分析界面不显示执行“计划数”的问题 [#939](https://github.com/pingcap/tidb-dashboard/pull/939)
    - 修复在升级集群后慢查询界面可能显示 "unknown field" 错误的问题 [#902](https://github.com/pingcap/tidb-dashboard/issues/902)

+ TiFlash

    - 修复编译 DAG 请求时出现进程崩溃的潜在问题
    - 修复读负载高的情况下进程崩溃的问题
    - 修复因列存中 split 失败导致 TiFlash 不断重启的问题
    - 修复无法删除 Delta 历史数据的潜在问题
    - 修复并发复制共享 Delta 索引导致结果错误的问题
    - 修复当数据缺失时 TiFlash 无法重启的问题
    - 修复旧的 dm 文件无法被自动清理的问题
    - 修复 `SUBSTRING` 函数包含特殊参数时引起进程崩溃的潜在问题
    - 修复将 `INT` 类型转换为 `TIME` 类型时产生错误结果的问题

+ Tools

    + Backup & Restore (BR)

        - 修复不能恢复 `mysql` 库内的用户表的问题 [#1142](https://github.com/pingcap/br/pull/1142)

    + TiDB Lightning

        - 修复 TiDB Lightning 解析 Parquet 文件中 `DECIMAL` 类型数据失败的问题 [#1276](https://github.com/pingcap/br/pull/1276)
        - 修复 TiDB Lightning 导入大文件拆分时遇到的 EOF 报错问题 [#1133](https://github.com/pingcap/br/issues/1133)
        - 修复 TiDB Lightning 导入含 `auto_increment` 的 `DOUBLE` 或 `FLOAT` 类型列的表时生成极大 base 值的问题 [#1185](https://github.com/pingcap/br/pull/1185)
        - 修复在生成超过 4 GB 的 KV 数据时可能发生的 panic 问题 [#1128](https://github.com/pingcap/br/pull/1128)

    + Dumpling

        - 使用 Dumpling 导出至 S3 存储时，不再要求 `s3:ListBucket` 权限覆盖整个 Bucket，只需要覆盖导出的前缀即可 [#898](https://github.com/pingcap/br/issues/898)

    + TiCDC

        - 修复分区表新增分区后的处理 [#2205](https://github.com/pingcap/ticdc/pull/2205)
        - 修复 TiCDC 无法读取 `/proc/meminfo` 导致崩溃的问题 [#2023](https://github.com/pingcap/ticdc/pull/2023)
        - 减少 TiCDC 运行时的内存使用 [#2011](https://github.com/pingcap/ticdc/pull/2011) [#1957](https://github.com/pingcap/ticdc/pull/1957)
        - 修复 MySQL sink 遇到错误或暂停时，MySQL 连接会泄漏的问题 [#1945](https://github.com/pingcap/ticdc/pull/1945)
        - 修复当 start TS 小于 current TS 减去 GC TTL 时无法创建 TiCDC changefeed 的问题 [#1839](https://github.com/pingcap/ticdc/issues/1839)
        - 减少 sort heap 的内存 `malloc`，以降低 CPU 开销 [#1853](https://github.com/pingcap/ticdc/issues/1853)
        - 修复调度数据表时可能发生的同步终止问题 [#1827](https://github.com/pingcap/ticdc/pull/1827)
