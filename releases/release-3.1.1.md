---
title: TiDB 3.1.1 Release Notes
---

# TiDB 3.1.1 Release Notes

发版日期：2020 年 4 月 30 日

TiDB 版本：3.1.1

TiDB Ansible 版本：3.1.1

## 新功能

+ TiDB

    - 添加 `auto_rand_base` 的 table option [#16812](https://github.com/pingcap/tidb/pull/16812)
    - 添加 `Feature ID` 注释：在 SQL 语句的特殊注释中，只有被注册了语句片段才能被 parser 正常解析，否则将被忽略 [#16155](https://github.com/pingcap/tidb/pull/16155)

+ TiFlash

    - 缓存 `handle` 列和 `version` 列减小单次读请求的磁盘 I/O
    - Grafana 添加 DeltaTree 引擎读写负载相关图表
    - 优化 TiFlash chunk encode decimal 数据的流程
    - TiFlash 低负载时，减少打开的文件描述符数量

## Bug 修复

+ TiDB

    - 修复实例级别的隔离读设置不生效的问题，以及 TiDB 升级后隔离读设置被不正确保留的问题 [#16482](https://github.com/pingcap/tidb/pull/16482) [#16802](https://github.com/pingcap/tidb/pull/16802)
    - 修复 hash 分区表上面的分区选择语法，现在 `partition(P0)` 这样的语法不会报错 [#16076](https://github.com/pingcap/tidb/pull/16076)
    - 修复若 update sql 中包含 view，但不会对 view 进行 update，update 语句仍然报错的问题[#16789](https://github.com/pingcap/tidb/pull/16789)
    - 修复对查询最内层的 `not not` 消除而造成结果错误的问题 [#16423](https://github.com/pingcap/tidb/pull/16423)

+ TiFlash

    - 修复当 Region 处于非 normal 状态时读取产生的数据错误
    - 修复 TiFlash 中表名的映射方式以正确支持 `recover table`/`flashback table`
    - 修复数据存储路径以解决 `rename table` 时潜在的数据丢失问题 
    - 修复在线更新时的读模型以优化读性能
    - 修复 database/table name 含特殊字符，升级后无法正常启动的问题

+ Tools

    - Backup & Restore (BR)

        * 修复 BR 恢复带有 auto_random 属性的表之后，插入数据有一定概率触发duplicate entry 错误的问题 [#241](https://github.com/pingcap/br/issues/241)
