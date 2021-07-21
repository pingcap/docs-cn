---
title: TiDB 4.0.14 Release Notes
---

# TiDB 4.0.14 Release Notes

发版日期：2021 年 7 月 22 日

TiDB 版本：4.0.14

## 兼容性更改

+ TiDB

    - 在 v4.0 中将 `tidb_multi_statement_mode` 的默认值从 `WARN` 更改为 `OFF`，建议使用客户端库的多语句功能。参考[`tidb_multi_statement_mode` 文档](/system-variables.md#tidb_multi_statement_mode-new-in-v4011) [#25749](https://github.com/pingcap/tidb/pull/25749)
    - 将 Grafana 从 v6.1.16 升级到 v7.5.7 以解决两个安全漏洞. 参考 [Grafana post](https://grafana.com/blog/2020/06/03/grafana-6.7.4-and-7.0.2-released-with-important-security-fix/)
    - 将系统变量 `tidb_stmt_summary_max_stmt_count` 的默认值 200 修改为 3000 [#25872](https://github.com/pingcap/tidb/pull/25872)

+ TiKV

    - 将 `merge-check-tick-interval` 配置项的默认值从 `10` 修改为 `2` 以加快 Region 合并的速度 [#9676](https://github.com/tikv/tikv/pull/9676)

## 功能增强

+ TiKV

    - 添加监控项 `pending` 用以监控 pending PD 心跳，帮助定位 PD 线程变慢的问题 [#10008](https://github.com/tikv/tikv/pull/10008)
    - 支持 virtual-host 风格的地址来让 BR 兼容类 S3 储存 [#10242](https://github.com/tikv/tikv/pull/10242)

+ TiDB Dashboard

    - 新增 OIDC SSO 支持，通过设置兼容 OIDC 标准的 SSO 服务（例如 Okta、Auth0 等），用户可以在不输入 SQL 密码的情况下登录 TiDB Dashboard [#960](https://github.com/pingcap/tidb-dashboard/pull/960)
    - 新增 Debug API 界面用于高级调试，通过界面可以替代目前的命令行方式来调用 TiDB 和 PD 的内部调试性 API [#927](https://github.com/pingcap/tidb-dashboard/pull/927)

## 改进提升

+ TiDB

    - 在 update 语句中的读过程，使用 point/batch point get 写入 index 的 key 来替代给 row 数据上锁  [#26223](https://github.com/pingcap/tidb/pull/26223)
    - 支持 MySQL 的系统变量 `init_connect` 及其相关功能 [#26031](https://github.com/pingcap/tidb/pull/26031)
    - 支持稳定结果模式 [#26003](https://github.com/pingcap/tidb/pull/26003)
    - 支持函数 `json_unquote()` 下推到 TiKV [#25721](https://github.com/pingcap/tidb/pull/25721)
    - 使 SPM 不受字符集的影响 [#23295](https://github.com/pingcap/tidb/pull/23295)

+ TiKV

    - 关闭 TiKV 时，优先关闭 status server 来确保客户端可以正确检测关闭状态 [#10504](https://github.com/tikv/tikv/pull/10504)
    - 响应过期副本的消息，以确保过期副本被更快清除 [#10400](https://github.com/tikv/tikv/pull/10400)
    - 限制 TiCDC sink 的内存消耗 [#10147](https://github.com/tikv/tikv/pull/10147)
    - 当 Region 太大时，使用均匀分裂来加快分裂速度 [#10275](https://github.com/tikv/tikv/pull/10275)

+ PD

    - 更新 TiDB Dashboard 版本至 v2021.07.17.1 [#3882](https://github.com/pingcap/pd/pull/3882)
    - 减少各调度器在同时工作时的冲突 [#3854](https://github.com/tikv/pd/pull/3854)
    - 修复了当集群内 Store 非常多时，PD 切换 Leader 慢的问题 [#3718](https://github.com/pingcap/pd/pull/3718)

+ TiDB Dashboard

    - 支持将当前会话分享为只读的会话，禁止分享出来的会话进行修改操作 [#960](https://github.com/pingcap/tidb-dashboard/pull/960)

## Bug 修复

+ TiDB

    - 当所有的聚合函数被消除时生成正确的行数量 [#26039](https://github.com/pingcap/tidb/pull/26039)
    - 修复当参数是 enum/set 类型时，ifnull 函数的计算错误 [#26035](https://github.com/pingcap/tidb/pull/26035)
    - 修复某些情况下错误的聚合函数消除 [#26033](https://github.com/pingcap/tidb/pull/26033)
    - 修复 merge join 中当列为 set 类型时可能产生的错误结果 [#26032](https://github.com/pingcap/tidb/pull/26032)
    - 修复 IN 语句的某些执行错误 [#25665](https://github.com/pingcap/tidb/pull/25665)
    - 修复 `select ... for update` 语句在 join on 分区表时，可能产生异常退出的情况 [#25501](https://github.com/pingcap/tidb/pull/25501)
    - 修复 plan cache 中，在事务过程中 point get plan 不正确的问题 [#24764](https://github.com/pingcap/tidb/pull/24764)
    - 修复 `load data` 语句可以不正常导入非 utf8 数据的问题 [#26142](https://github.com/pingcap/tidb/pull/26142)
    - 修复通过 http API 访问统计信息时，可能导致内存泄露的问题 [#24650](https://github.com/pingcap/tidb/pull/24650)
    - 修复执行 `ALTER USER` 语句的安全性问题 [#25347](https://github.com/pingcap/tidb/pull/25347)
    - 修复系统表 `TIKV_REGION_PEERS` 不能正确处理 `DOWN` 状态. [#24918](https://github.com/pingcap/tidb/pull/24918)
    - 修复解析 DateTime 不截断非法字符串 [#22260](https://github.com/pingcap/tidb/pull/22260)
    - 修复 `select into outfile` 语句在列类型是 year 时，可能无法产生结果的问题 [#22185](https://github.com/pingcap/tidb/pull/22185)

+ TiKV

    - 性能统计时容忍时间倒退避免 panic [#10572](https://github.com/tikv/tikv/pull/10572)
    - 修复 double 转 double 时对符号的错误处理 [#10532](https://github.com/tikv/tikv/pull/10532)
    - 修复 panic 退出有时报错信息会丢失的问题 [#10488](https://github.com/tikv/tikv/pull/10488)
    - 修复开启加密情况下重新生成同样 snapshot 会 panic 的问题 [#10462](https://github.com/tikv/tikv/pull/10462)
    - 修复 json_unquote 中错误的参数类型 [#10425](https://github.com/tikv/tikv/pull/10425)
    - 滚动重启时跳过清除回调以避免在高冲突下破坏事务一致 [#10395](https://github.com/tikv/tikv/pull/10395)
    - 修复 backup 线程泄漏 [#10360](https://github.com/tikv/tikv/pull/10360)
    - 修复 split 和创建新 region 冲突时可能会损坏 metadata 的问题 [#9584](https://github.com/tikv/tikv/pull/9584)
    - 修复特定情况下 region 心跳会导致 TiKV 不进行 split 的问题 [#10274](https://github.com/tikv/tikv/pull/10274)
    - 修复 CM Sketch 格式不一致导致的统计信息错误问题 [#10433](https://github.com/tikv/tikv/pull/10433)
    - 修复 apply wait duration 的错误统计 [#9966](https://github.com/tikv/tikv/pull/9966)
    - 修复使用 titan 时 delete_files_in_range 以后可能会产生 "Missing Blob" 报错的问题 [#10232](https://github.com/tikv/tikv/pull/10232)

+ PD

    - 修复调度器在执行删除操作后可能再次出现的问题 [#3825](https://github.com/pingcap/pd/pull/3825)
    - 修复调度器在临时配置加载完毕前启动可能导致数据争用的问题 [#3773](https://github.com/pingcap/pd/pull/3773)
    - 修复打散 Region 操作可能导致 PD Panic 的问题 [#3761](https://github.com/pingcap/pd/pull/3761)
    - 修复部分 Operator 未被设置正确的优先级的问题 [#3703](https://github.com/pingcap/pd/pull/3703)
    - 修复删除不存在的 Store 的  evict-leader 调度器时可能导致 PD Panic 的问题 [#3680](https://github.com/pingcap/pd/pull/3680)

+ TiDB Dashboard

    - 修复实例性能分析界面中部分 TiDB 可能抓取性能数据失败的问题 [#944](https://github.com/pingcap/tidb-dashboard/pull/944)
    - 修复 SQL 语句分析界面不显示 "执行计划数" 的问题 [#939](https://github.com/pingcap/tidb-dashboard/pull/939)
    - 修复在升级集群后慢查询界面可能显示 "unknown field" 错误的问题 [#930](https://github.com/pingcap/tidb-dashboard/pull/930)

+ TiFlash

    - 修复编译 DAG 请求时出现进程崩溃的潜在问题
    - 修复读负载高的情况下进程崩溃的问题
    - 修复因 split 失败而不断重启的问题
    - 修复无法删除 Delta 历史数据的潜在问题
    - 修复并发复制共享 Delta 索引导致结果错误的问题
    - 修复当存在数据缺失的情况下 TiFlash 无法启动的问题
    - 修复旧的 dm 文件无法被自动清理的问题
    - 修复 SUBSTRING 函数包含特殊参数时引起进程崩溃的潜在问题
    - 修复 INT 类型转换为 TIME 类型时产生错误结果的问题
