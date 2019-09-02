---
title: TiDB 2.1.9 Release Notes
category: Releases
---

# TiDB 2.1.9 Release Notes

发版日期：2019 年 5 月 6 日

TiDB 版本：2.1.9

TiDB Ansible 版本：2.1.9

## TiDB

- 修复 `MAKETIME` 函数在 unsigned 类型溢出时的兼容性 [#10089](https://github.com/pingcap/tidb/pull/10089)
- 修复常量折叠在某些情况下导致的栈溢出 [#10189](https://github.com/pingcap/tidb/pull/10189)
- 修复 Update 在某些有别名的情况下权限检查的问题 [#10157](https://github.com/pingcap/tidb/pull/10157) [#10326](https://github.com/pingcap/tidb/pull/10326)
- 追踪以及控制 DistSQL 中的内存使用 [#10197](https://github.com/pingcap/tidb/pull/10197)
- 支持指定 collation 为 utf8mb4_0900_ai_ci [#10201](https://github.com/pingcap/tidb/pull/10201)
- 修复主键为 Unsigned 类型的时候，MAX 函数结果错误的问题 [#10209](https://github.com/pingcap/tidb/pull/10209)
- 修复在非 Strict SQL Mode 下可以插入 NULL 值到 NOT NULL 列的问题 [#10254](https://github.com/pingcap/tidb/pull/10254)
- 修复 COUNT 函数在 DISTINCT 有多列的情况下结果错误的问题 [#10270](https://github.com/pingcap/tidb/pull/10270)
- 修复 LOAD DATA 解析不规则的 CSV 文件时候 Panic 的问题 [#10269](https://github.com/pingcap/tidb/pull/10269)
- 忽略 Index Lookup Join 中内外 join key 类型不一致的时候出现的 overflow 错误 [#10244](https://github.com/pingcap/tidb/pull/10244)
- 修复某些情况下错误判定语句为 point-get 的问题 [#10299](https://github.com/pingcap/tidb/pull/10299)
- 修复某些情况下时间类型未转换时区导致的结果错误问题 [#10345](https://github.com/pingcap/tidb/pull/10345)
- 修复 TiDB 字符集在某些情况下大小写比较不一致的问题 [#10354](https://github.com/pingcap/tidb/pull/10354)
- 支持控制算子返回的行数 [#9166](https://github.com/pingcap/tidb/issues/9166)
    - Selection & Projection [#10110](https://github.com/pingcap/tidb/pull/10110)
    - StreamAgg & HashAgg [#10133](https://github.com/pingcap/tidb/pull/10133)
    - TableReader & IndexReader & IndexLookup [#10169](https://github.com/pingcap/tidb/pull/10169)
- 慢日志改进
    - 增加 SQL Digest 用于区分同类 SQL [#10093](https://github.com/pingcap/tidb/pull/10093)
    - 增加慢语句使用的统计信息的版本信息 [#10220](https://github.com/pingcap/tidb/pull/10220)
    - 输出语句内存使用量 [#10246](https://github.com/pingcap/tidb/pull/10246)
    - 调整 Coprocessor 相关信息的输出格式，让其能被 pt-query-digest 解析 [#10300](https://github.com/pingcap/tidb/pull/10300)
    - 修复慢语句中带有 `#` 字符的问题 [#10275](https://github.com/pingcap/tidb/pull/10275)
    - 增加一些信息的列到慢查询的内存表 [#10317](https://github.com/pingcap/tidb/pull/10317)
    - 将事务提交时间算入慢语句执行时间 [#10310](https://github.com/pingcap/tidb/pull/10310)
    - 修复某些时间格式无法被 pt-query-digest 解析的问题 [#10323](https://github.com/pingcap/tidb/pull/10323)

## PD

- 支持 GetOperator 服务 [#1514](https://github.com/pingcap/pd/pull/1514)

## TiKV

- 修复在 transfer leader 时非预期的 quorum 变化 [#4604](https://github.com/tikv/tikv/pull/4604)

## Tools

- TiDB Binlog
    - 修复 unsigned int 类型的主键列的 binlog 数据为负数，造成同步出错中断的问题 [#574](https://github.com/pingcap/tidb-binlog/pull/574)
    - 删除下游是 `pb` 时的压缩选项，修改下游名字 `pb` 成 `file` [#597](https://github.com/pingcap/tidb-binlog/pull/575)
    - 修复 2.1.7 引入的 Reparo 生成错误 update 语句的 bug [#576](https://github.com/pingcap/tidb-binlog/pull/576)
- TiDB Lightning
    - 修复 parser 解析 bit 类型的 column 数据错误的 bug [#164](https://github.com/pingcap/tidb-lightning/pull/164)
    - 使用 row id 或者列的默认值填充 dump 文件中缺少的 column 数据 [#174](https://github.com/pingcap/tidb-lightning/pull/174)
    - Importer 修复部分 SST 导入失败依然返回导入成功的 bug [#4566](https://github.com/tikv/tikv/pull/4566)
    - Importer 支持 upload SST 到 TiKV 限速 [#4607](https://github.com/tikv/tikv/pull/4607)
    - 修改 Importer RocksDB SST 压缩方法为 `lz4`，减少 CPU 消耗 [#4624](https://github.com/tikv/tikv/pull/4624)
- sync-diff-inspector
    - 支持 checkpoint [#227](https://github.com/pingcap/tidb-tools/pull/227)

## TiDB Ansible

- 更新 tidb-ansible 中的文档链接，兼容重构之后的文档 [#740](https://github.com/pingcap/tidb-ansible/pull/740)，[#741](https://github.com/pingcap/tidb-ansible/pull/741)
- 移除 `inventory.ini` 中的 `enable_slow_query_log` 参数，默认即将 slow log 输出到单独的日志文件中 [#742](https://github.com/pingcap/tidb-ansible/pull/742)
