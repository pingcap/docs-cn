---
title: TiDB 2.1 RC3 Release Notes
category: Releases
aliases: ['/docs-cn/releases/21rc3/']
---

# TiDB 2.1 RC3 Release Notes

2018 年 9 月 29 日，TiDB 发布 2.1 RC3 版。相比 2.1 RC2 版本，该版本对系统稳定性、兼容性、优化器以及执行引擎做了很多改进。

## TiDB

+ SQL 优化器
    - 修复语句内包含内嵌的 `LEFT OUTER JOIN` 时，结果不正确的问题 [#7689](https://github.com/pingcap/tidb/pull/7689)
    - 增强 `JOIN` 语句上的 predicate pushdown 优化规则 [#7645](https://github.com/pingcap/tidb/pull/7645)
    - 修复 `UnionScan` 算子的 predicate pushdown 优化规则 [#7695](https://github.com/pingcap/tidb/pull/7695)
    - 修复 `Union` 算子的 unique key 属性设置不正确的问题 [#7680](https://github.com/pingcap/tidb/pull/7680)
    - 增强常量折叠的优化规则 [#7696](https://github.com/pingcap/tidb/pull/7696)
    - 把常量传播后的 filter 是 null 的 data source 优化成 table dual [#7756](https://github.com/pingcap/tidb/pull/7756)
+ SQL 执行引擎
    - 优化事务内读请求的性能 [#7717](https://github.com/pingcap/tidb/pull/7717)
    - 优化部分执行器 Chunk 内存分配的开销 [#7540](https://github.com/pingcap/tidb/pull/7540)
    - 修复点查全部为 NULL 的列导致数组越界的问题 [#7790](https://github.com/pingcap/tidb/pull/7790)
+ Server
    - 修复配置文件里内存配额选项不生效的问题 [#7729](https://github.com/pingcap/tidb/pull/7729)
    - 添加 tidb_force_priority 系统变量用来整体设置语句执行的优先级 [#7694](https://github.com/pingcap/tidb/pull/7694)
    - 支持使用 `admin show slow` 语句来获取 SLOW QUERY LOG [#7785](https://github.com/pingcap/tidb/pull/7785)
+ 兼容性
    - 修复 `information_schema.schemata` 里 `charset/collation` 结果不正确的问题 [#7751](https://github.com/pingcap/tidb/pull/7751)
    - 修复 `hostname` 系统变量的值为空的问题 [#7750](https://github.com/pingcap/tidb/pull/7750)
+ 表达式
    - 内建函数 `AES_ENCRYPT/AES_DECRYPT` 支持 `init_vecter` 参数 [#7425](https://github.com/pingcap/tidb/pull/7425)
    - 修复部分表达式 `Format` 结果不正确的问题 [#7770](https://github.com/pingcap/tidb/pull/7770)
    - 支持内建函数 `JSON_LENGTH` [#7739](https://github.com/pingcap/tidb/pull/7739)
    - 修复 unsigned integer 类型 cast 为 decimal 类型结果不正确的问题 [#7792](https://github.com/pingcap/tidb/pull/7792)
+ DML
    - 修复 `INSERT … ON DUPLICATE KEY UPDATE` 语句在 unique key 更新时结果不正确的问题 [#7675](https://github.com/pingcap/tidb/pull/7675)
+ DDL
    - 修复在新建的 timestamp 类型的列上新建索引时，索引值没有做时区转换的问题 [#7724](https://github.com/pingcap/tidb/pull/7724)
    - 支持 enum 类型 append 新的值 [#7767](https://github.com/pingcap/tidb/pull/7767)
    - 快速新建 etcd session，使网络隔离后，集群更快恢复可用 [#7774](https://github.com/pingcap/tidb/pull/7774)

## PD

+ 新特性
    - 添加获取按大小逆序排序的 Region 列表 API (/size) [#1254](https://github.com/pingcap/pd/pull/1254)
+ 功能改进
    - Region API 会返回更详细的信息 [#1252](https://github.com/pingcap/pd/pull/1252)
+ Bug 修复
    - 修复 PD 切换 leader 以后 `adjacent-region-scheduler` 可能会导致 crash 的问题 [#1250](https://github.com/pingcap/pd/pull/1250)

## TiKV

+ 性能优化
    - 优化函数下推的并发支持 [#3515](https://github.com/tikv/tikv/pull/3515)
+ 新特性
    - 添加对 Log 函数的支持 [#3603](https://github.com/tikv/tikv/pull/3603)
    - 添加对 `sha1` 函数的支持 [#3612](https://github.com/tikv/tikv/pull/3612)
    - 添加 `truncate_int` 函数的支持 [#3532](https://github.com/tikv/tikv/pull/3532)
    - 添加 `year` 函数的支持 [#3622](https://github.com/tikv/tikv/pull/3622)
    - 添加 `truncate_real` 函数的支持 [#3633](https://github.com/tikv/tikv/pull/3633)
+ Bug 修复
    - 修正时间函数相关的报错行为 [#3487](https://github.com/tikv/tikv/pull/3487) [#3615](https://github.com/tikv/tikv/pull/3615)
    - 修复字符串解析成时间与 TiDB 不一致的问题 [#3589](https://github.com/tikv/tikv/pull/3589)