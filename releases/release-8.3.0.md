---
title: TiDB 8.3.0 Release Notes
summary: 了解 TiDB 8.3.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 8.3.0 Release Notes

发版日期：2024 年 x 月 x 日

TiDB 版本：8.3.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v8.3/quick-start-with-tidb) | [下载离线包](https://cn.pingcap.com/product-community/?version=v8.3.0-DMR#version-list)

在 8.3.0 版本中，你可以获得以下关键特性：

## 功能详情

### 可扩展性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 性能

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* Projection 下推功能正式发布 [#51876](https://github.com/pingcap/tidb/issues/51876) @[yibin87](https://github.com/yibin87) **tw@Oreoxmt** <!--1872-->

    将 `Projection` 算子下推到存储引擎可以减少计算引擎和存储引擎之间的传输的数据量，特别是对 [JSON 查询类函数](/functions-and-operators/json-functions/json-functions-search.md)或 [JSON 值属性类函数](/functions-and-operators/json-functions/json-functions-return.md)，效果更加显著。在 v8.3.0 版本中，TiDB 正式发布 Projection 下推功能。在该功能启用时，优化器会自动将符合条件的 JSON 查询类函数、JSON 值属性类函数等下推至存储引擎。
    
    变量 [tidb_opt_projection_push_down](/system-variables.md#tidb_opt_projection_push_down-从-v610-版本开始引入) 控制是否启用 Projection 下推功能。该变量的默认值将调整为 `ON`，表示默认启用该功能。

    更多信息，请参考[用户文档](/system-variables.md#tidb_opt_projection_push_down-从-v610-版本开始引入)。
    
* 优化 KV 请求的批处理策略 [#xxx](https://github.com/pingcap/tidb/issues/xxx) @[zyguan](https://github.com/zyguan) **tw@Oreoxmt** <!--1897-->

    TiDB 读取数据需要通过 KV 请求进行。通过将 KV 请求攒批并进行批处理，可以有效提高执行效率。在 v8.3.0 版本之前，TiDB 批处理策略的效率不高。在 v8.3.0 版本，TiDB 在现有的基础 KV 请求批处理策略基础上，引入更加高效的策略。通过新增的配置项 [`tikv-client.batch-policy·](/tidb-configuration-file.md#batch-policy-从-v830-版本开始引入) 设定不同的批处理策略。
    
    更多信息，请参考[用户文档](/tidb-configuration-file.md#batch-policy-从-v830-版本开始引入)。
    
* 增加获取 TSO 的 RPC 模式，降低获取 TSO 的延迟 [#xxx](https://github.com/pingcap/tidb/issues/xxx) @[MyonKeminta](https://github.com/MyonKeminta) **tw@qiancai** <!--1893-->

    TiDB 在向 PD 请求 TSO 时，会汇总一定时间段的请求并以同步的方式进行批处理以减少 RPC 请求数量、降低 PD 负载。对于延迟敏感的场景，这种模式的性能并不理想。在 v8.3.0 版本中，TiDB 新增 TSO 请求的异步批处理模式，并提供不同的并发能力，以增加相应的 PD 负载为代价，降低获取 TSO 的延迟。通过新增的变量 [tidb_tso_client_rpc_mode](/system-variables.md#tidb_tso_client_rpc_mode-从-v830-版本开始引入) 设定获取 TSO 的 RPC 模式。
    
    更多信息，请参考[用户文档](/system-variables.md#tidb_tso_client_rpc_mode-从-v830-版本开始引入)。
    
* TiFlash 新增 Hashagg 聚合计算模式，提升高 NDV 数据的聚集计算性能 [#9196](https://github.com/pingcap/tiflash/issues/9196) @[guo-shaoge](https://github.com/guo-shaoge) **tw@Oreoxmt** <!--1855-->

    TiFlash 的 Hashagg 聚合计算中，第一阶段也会进行聚集计算。对于高 NDV 数据，这种模式效率较低。在 v8.3.0 版本中，TiFlash 引入多种 Hashagg 聚合计算模式，提升不同特征数据的聚集计算性能。通过新增的变量 [tiflash_hashagg_preaggregation_mode](/system-variables.md#tiflash_hashagg_preaggregation_mode-从-v830-版本开始引入) 设定 Hashagg 聚合计算模式。
    
    更多信息，请参考[用户文档](/system-variables.md#tiflash_hashagg_preaggregation_mode-从-v830-版本开始引入)。
    
### 稳定性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* TiProxy 支持虚拟 IP 管理功能 [#583](https://github.com/pingcap/tiproxy/issues/583) @[djshow832](https://github.com/djshow832) **tw@Oreoxmt** <!--1887-->

    在 v8.3.0 版本之前，使用主从模式保证高可用时，TiProxy 还需要额外的组件管理虚拟 IP 功能。在 v8.3.0 版本，TiProxy 支持虚拟 IP 管理功能。在主动模式下，当出现主从节点切换时，主节点自动绑定指定的虚拟 IP，保证客户端的正常访问。 
    
    通过设定 TiProxy 配置项 [`ha.virtual-ip`](/tiproxy/tiproxy-configuration.md#virtual-ip) 指定虚拟 IP。如果未指定，则表示不启用该功能。
    
    更多信息，请参考[用户文档](/tiproxy/tiproxy-overview.md)。
    
### 高可用

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### SQL 功能

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* 支持 `Shared Lock` 升级为 `Exclusive Lock` [#54999](https://github.com/pingcap/tidb/issues/54999) @[cfzjywxk](https://github.com/cfzjywxk) **tw@hfxsd** <!--1857-->

    TiDB 暂不支持 `Shared Lock`. 在 v8.3.0 版本中，TiDB 支持将 `Shared Lock` 升级为 `Exclusive Lock`，实现对 `Shared Lock` 语法的支持。通过新增的变量 [tidb_enable_shared_lock_upgrade](/system-variables.md#tidb_enable_shared_lock_upgrade-从-v830-版本开始引入) 控制是否启用该功能。

### 数据库管理

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 可观测性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* 系统视图 `PROCESS LIST` 增加 `ROWS_AFFECTED` 字段 [#54486](https://github.com/pingcap/tidb/issues/54486) @[ekexium](https://github.com/ekexium) **tw@qiancai** <!--1903-->

    TiDB 并不能显示当前 DML 语句已经处理的数据行数。在 v8.3.0 版本中，系统视图 `PROCESS LIST` 增加 `ROWS_AFFECTED` 字段，展示当前 DML 语句已经写入的数据行数。
    
    更多信息，请参考[用户文档](/information-schema/information-schema-processlist.md)。
    
### 安全

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 数据迁移

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

## 兼容性变更

> **注意：**
>
> 以下为从 v8.2.0 升级至当前版本 (v8.3.0) 所需兼容性变更信息。如果从 v8.1.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 Release Notes 中提到的兼容性变更信息。

### 行为变更

* 行为变更 1
* 行为变更 2

### MySQL 兼容性

* 兼容性 1

* 兼容性 2

### 系统变量

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
|        |                              |      |
|        |                              |      |
|        |                              |      |
|        |                              |      |

### 系统表

### 其他

## 离线包变更

## 废弃功能

* 废弃功能 1

* 废弃功能 2

## 改进提升

+ TiDB

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - TopN 算子支持数据落盘功能 [#47733](https://github.com/pingcap/tidb/issues/47733) @[xzhangxian1008](https://github.com/xzhangxian1008) **tw@Oreoxmt** <!--1715-->
    - TiDB 支持 `WITH ROLLUP` 修饰符和 `GROUPING` 函数 [#42631](https://github.com/pingcap/tidb/issues/42631) @[Arenatlx](https://github.com/Arenatlx) **tw@Oreoxmt** <!--1714-->
    - 变量 `tidb_low_resolution_tso` 增加全局作用域 [#55022](https://github.com/pingcap/tidb/issues/55022) @[cfzjywxk](https://github.com/cfzjywxk) **tw@hfxsd** <!--1857-->
    - 优化 MemDB 实现，降低写事务延迟 [#xxx](https://github.com/pingcap/tidb/issues/xxx) @[you06](https://github.com/you06) **tw@hfxsd** <!--1892-->
    - GC 支持并发删除 Range 以提升处理效率 [#xxx](https://github.com/pingcap/tidb/issues/xxx) @[ekexium](https://github.com/ekexium) **tw@qiancai** <!--1890-->

+ TiKV

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ PD

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiFlash

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiCDC

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Data Migration (DM)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

## 错误修复

+ TiDB

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiKV

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ PD

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiFlash

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiCDC

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Data Migration (DM)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
                - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [贡献者 GitHub ID]()
