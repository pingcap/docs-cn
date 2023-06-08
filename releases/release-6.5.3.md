---
title: TiDB 6.5.3 Release Notes
summary: 了解 TiDB 6.5.3 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 6.5.3 Release Notes

发版日期：2023 年 x 月 x 日

TiDB 版本：6.5.3

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v6.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v6.5.3#version-list)

## 兼容性变更

- note 1

## 改进提升

+ TiDB

    - note 1

+ TiKV

    - note 1

+ PD

    - note 1

+ TiFlash

    - note 1

+ Tools

    + Backup & Restore (BR)

        - note 1

    + TiCDC

        - note 1

    + TiDB Data Migration (DM)

        - note 1

    + TiDB Lightning

        - note 1

    + Dumpling

        - note 1

## 错误修复

+ TiDB

    - 修复一个 min, max 查询结果出错的问题  [#43805](https://github.com/pingcap/tidb/issues/43805) @[wshwsh12](https://github.com/wshwsh12)
    - 修复一个窗口函数计算下推到 tiflash 时执行计划构造错误的问题 [#43981](https://github.com/pingcap/tidb/issues/43981) @[gengliqi](https://github.com/gengliqi)
    - 修复一个使用 CTE 的查询 hang 住的问题 [#43758](https://github.com/pingcap/tidb/issues/43758) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复一个使用 AES_DECRYPT 表达时，sql 报错 runtime error: index out of range 的问题 [#43086](https://github.com/pingcap/tidb/issues/43086) @[lcwangchao](https://github.com/lcwangchao)
    - 修复 show processlist 无法显示子查询时间较长语句的事务的 start ts 的问题。[#44243](https://github.com/pingcap/tidb/pull/44243) @[crazycs520](https://github.com/crazycs520)
    - 修复 PD 隔离有可能导致运行的 DDL 阻塞的问题。 [#44022](https://github.com/pingcap/tidb/pull/44022), [#43784](https://github.com/pingcap/tidb/pull/43784), [#44299](https://github.com/pingcap/tidb/pull/44299) @[wjhuang2016](https://github.com/wjhuang2016) 
    - 修复了某些情况下临时表 union 视图时可能造成 Panic 的问题 [#42702](https://github.com/pingcap/tidb/pull/42702) @[lcwangchao](https://github.com/lcwangchao) 
    - 修复放置规则在分区表下的一些行为，使得删除的分区放置规则被正确设置以及回收 [#44149](https://github.com/pingcap/tidb/pull/44149) @[lcwangchao](https://github.com/lcwangchao) 
    - 修复了在 TRUNCATE 分区表的某个分区时可能造成分区的放置规则失效的问题 [#44061](https://github.com/pingcap/tidb/pull/44061) @[lcwangchao](https://github.com/lcwangchao) 
    - 修复在重命名表期间 TiCDC 可能丢失部分行变更的问题 [#43458](https://github.com/pingcap/tidb/pull/43458) @[tangenta](https://github.com/tangenta) 
    - 修复使用 BR 导入表后 DDL 作业历史记录丢失的问题 [#43878](https://github.com/pingcap/tidb/pull/43878) @[tangenta](https://github.com/tangenta) 
    - 修复了在启用 CursorFetch 时执行其他语句后继续 Fetch 或 Close 可能出现 Panic 或错误结果的问题 [#42602](https://github.com/pingcap/tidb/pull/42602) @[YangKeao](https://github.com/YangKeao) 
    - 修复了某些情况下 json_object 函数错误地返回 JSON 格式错误的问题 [#44100](https://github.com/pingcap/tidb/pull/44100) @[YangKeao](https://github.com/YangKeao) 
    - 修复了在 IPv6 环境下读取 information_schema 失败和一些相关信息错误的问题。[#43834](https://github.com/pingcap/tidb/pull/43834)，[#44084]([https://github.com/pingcap/tidb/pull/44084) @[Defined2014](](https://github.com/pingcap/tidb/pull/44084)@[Defined2014]()https://github.com/Defined2014) ，@[nexustar](https://github.com/nexustar)
    - 修复了 PD 增减节点，PD 集群的 leader IP 变更后，autoid 服务无法自动重连的问题。该问题触发后会导致 AUTO_ID_CACHE=0 的表上面的操作卡死。[#43537](https://github.com/pingcap/tidb/pull/43537) @[tiancaiamao](https://github.com/tiancaiamao) 
    - 修复了放置规则回收时，TiDB 向 PD 发送重复请求，造成 PD 侧大量 "full config reset" 日志打印的问题 [#44335](https://github.com/pingcap/tidb/pull/44335) @[tiancaiamao](https://github.com/tiancaiamao) 
    - 修复了 show privileges 显示权限列表不全的问题 [#40610](https://github.com/pingcap/tidb/pull/40610) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 修复在 ADMIN SHOW DDL JOB QUERIES 中使用 LIMIT 子句时返回错误结果的问题 [#42427](https://github.com/pingcap/tidb/pull/42427) @[CbcWestwolf](https://github.com/CbcWestwolf) 
    - 修复在开启密码强度校验时对 tidb_auth_token 用户进行校验的问题 [#44144](https://github.com/pingcap/tidb/pull/44144) @[CbcWestwolf](https://github.com/CbcWestwolf) 
    - 修复了分区表在做 index join 的时，其 key 没有定位到 partition 会报错的问题。[#44275](https://github.com/pingcap/tidb/pull/44275) @[mjonss](https://github.com/mjonss) 
    - 修复了在分区表上执行 modify column 时输出 truncate data 相关 warning 的问题。[#41115](https://github.com/pingcap/tidb/pull/41115)  @[mjonss](https://github.com/mjonss) 
    - 修复了 TRUNCATE 分区表后，没有分裂 region 的问题。[#44084](https://github.com/pingcap/tidb/pull/44084 @[jiyfhust](https://github.com/jiyfhust)

+ TiKV

    - note 1

+ PD

    - note 1

+ TiFlash

    - 修复一个分区表查询报错的问题 [#7519](https://github.com/pingcap/tiflash/issues/7519) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复在表字段同时存在 TIMESTAMP 或者 TIME 类型和 GENERATED 类型情况下，查询 TiFlash 可能会报错的问题 [#7468](https://github.com/pingcap/tiflash/issues/7468) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复大的更新事务可能会导致 TiFlash 反复报错重启的问题 [#7316](https://github.com/pingcap/tiflash/issues/7316) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复一个 insert select 语句从 tiflash 读取数据时，sql 报错 Truncate error cast decimal as decimal 的问题 [#7348](https://github.com/pingcap/tiflash/issues/7348) @[windtalker](https://github.com/windtalker)
   - 修复查询在 Join build 侧数据非常大，且包含许多小型字符串类型列时，可能会使用比实际需要更大的内存的问题。 [#7416](https://github.com/pingcap/tiflash/issues/7416) @[yibin87](https://github.com/yibin87)

+ Tools

    + Backup & Restore (BR)

        - note 1

    + TiCDC

        - note 1

    + TiDB Data Migration (DM)

        - note 1

    + TiDB Lightning

        - note 1

    + Dumpling

        - note 1
