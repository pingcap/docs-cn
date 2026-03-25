---
title: TiDB 8.5.6 Release Notes
summary: 了解 TiDB 8.5.6 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 8.5.6 Release Notes

发版日期：2026 年 x 月 x 日

TiDB 版本：8.5.6

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v8.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v8.5/production-deployment-using-tiup) | [下载离线包](https://pingkai.cn/download#tidb-community)

## 功能详情

### 稳定性

- 支持为资源管控的后台任务设置资源上限成为正式功能 (GA) [#56019](https://github.com/pingcap/tidb/issues/56019) @[glorv](https://github.com/glorv) **tw@hfxsd** <!--1933-->

    TiDB 资源管控能够识别并降低后台任务的运行优先级。在部分场景下，即使有空闲资源，用户也希望后台任务消耗能够控制在很低的水平。从 v8.4.0 开始，你可以使用参数 `UTILIZATION_LIMIT` 为资源管控的后台任务设置最大可以使用的资源百分比，每个节点把所有后台任务的使用量控制在这个百分比以下。该功能可以让你精细控制后台任务的资源占用，进一步提升集群稳定性。

    在 v8.5.6 中，该功能成为正式功能 (GA)。

    更多信息，请参考[用户文档](/tidb-resource-control-background-tasks.md)。

### 数据迁移

- (dup): release-9.0.0.md > # 数据迁移 * 将 sync-diff-inspector 从 `pingcap/tidb-tools` 迁移至 `pingcap/tiflow` 代码仓库 [#11672](https://github.com/pingcap/tiflow/issues/11672) @[joechenrh](https://github.com/joechenrh)

## 兼容性变更

- note [#issue](https://github.com/pingcap/${repo-name}/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

## 改进提升

+ TiDB

    - 增强慢查询日志的控制能力，支持使用 [`tidb_slow_log_rules`](/system-variables.md#tidb_slow_log_rules-从-v900-版本开始引入) 基于多维指标组合条件定向输出慢查询日志，使用 [`tidb_slow_log_max_per_sec`](/system-variables.md#tidb_slow_log_max_per_sec-从-v900-版本开始引入) 限制每秒日志输出数量，并通过 [`WRITE_SLOW_LOG`](/optimizer-hints.md) Hint 强制记录指定 SQL 的慢查询日志 [#64010](https://github.com/pingcap/tidb/issues/64010) @[zimulala](https://github.com/zimulala)
    - 增强 [Top SQL](/dashboard/top-sql.md) 的资源分析能力，支持展示 Top `5`、`20` 或 `100` 查询，支持按 CPU、网络流量和逻辑 IO 排序查看热点，并支持在 TiKV 实例上按 `Query`、`Table`、`DB` 或 `Region` 维度聚合分析 [#62916](https://github.com/pingcap/tidb/issues/62916) @[yibin87](https://github.com/yibin87)
    - 新增 DXF 的 max_node_count 配置项支持 [#66376](https://github.com/pingcap/tidb/pull/66376)@[D3Hunter](https://github.com/D3Hunter)

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - 删除不存在的 label 时，现在会返回 404 [#10089](https://github.com/tikv/pd/issues/10089) @[lhy1024](https://github.com/lhy1024)
    - (dup): release-7.5.7.md > 改进提升> PD - 减少非必要的错误日志 [#9370](https://github.com/tikv/pd/issues/9370) @[bufferflies](https://github.com/bufferflies)

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiCDC

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - 新增对 MySQL 8.4 作为 DM 上游数据源的支持，适配该版本引入的新术语和版本检测逻辑 [#12532](https://github.com/pingcap/tiflow/pull/12532) @[dveeden](https://github.com/dveeden)
        - 在 DM syncer 中新增外键因果依赖支持，确保多 worker 场景下行变更按照父表至子表的外键顺序执行 [#12552](https://github.com/pingcap/tiflow/pull/12552) @[OliverS929](https://github.com/OliverS929)

    + TiDB Lightning

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

## 错误修复

+ TiDB

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - 修复 tidb_service_scope 设置时未统一转换为小写的问题 [#66835](https://github.com/pingcap/tidb/pull/66835)@[D3Hunter](https://github.com/D3Hunter)
    - 修复 TiDB 重启后无法展示亲和力表的问题 [#66284](https://github.com/pingcap/tidb/issues/66284) @[lcwangchao](https://github.com/lcwangchao)
    - 修复可能出现的内存泄漏 [#65522](https://github.com/pingcap/tidb/issues/65522) @[bufferflies](https://github.com/bufferflies)

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-5.1.4.md > Bug 修复> TiKV - 修复悲观事务中 prewrite 请求重试在极少数情况下影响数据一致性的风险 [#11187](https://github.com/tikv/tikv/issues/11187)

+ PD

    -  修复 distribute table sql panic 问题，特别是 merge region operator 比较多的场景容易触发这个 bug。 [#10292](https://github.com/tikv/pd/pull/10292) @[bufferflies](https://github.com/bufferflies)
    - 修复设置 store limit 后可能不马上生效的问题 [#10108](https://github.com/tikv/pd/issues/10108) @[okJiang](https://github.com/okJiang)

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - 修复当一个列执行将列属性 `NOT NULL` 转为 `NULL` 的 DDL 之后，TiFlash 与 TiKV 之间可能产生不一致数据的问题 [#10680](https://github.com/pingcap/tiflash/issues/10680) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 Grafana 面板中 Raft throughput 可能会错误地显示一个非常大的数值的问题 [#10701](https://github.com/pingcap/tiflash/issues/10701) @[CalvinNeo](https://github.com/CalvinNeo)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiCDC

        - 修复了一个在服务器重启时，changefeed 可能会重复创建无效 dispatcher 的问题。[#4452](https://github.com/pingcap/ticdc/issues/4452) @[wlwilliamx](https://github.com/wlwilliamx)
        - 修复了当 TiDB 版本小于等于 v8.1.x 时，表重命名操作无法正常执行的问题。[#4392](https://github.com/pingcap/ticdc/issues/4392) @[lidezhu](https://github.com/lidezhu)
        - 修复了一个扫描数据时的 Bug，避免启用 CDC 时 TiKV 可能出现异常崩溃。[#19404](https://github.com/tikv/tikv/issues/19404) @[wk989898](https://github.com/wk989898)
        - 为 azblob 下游支持 Azure 托管标识认证，并修复了云存储上传过程中可能出现的卡住问题。[#3093](https://github.com/pingcap/ticdc/issues/3093) @[wlwilliamx](https://github.com/wlwilliamx)

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - 修复 DM 在 binlog rotate 事件时全局 checkpoint 位置未推进的问题 [#12525](https://github.com/pingcap/tiflow/pull/12525) @[OliverS929](https://github.com/OliverS929)
        - 修复含外键约束的表在 DM safe-mode 下的异常行为，移除 UPDATE 改写中多余的 DELETE 操作并避免触发外键级联 [#12541](https://github.com/pingcap/tiflow/pull/12541) @[OliverS929](https://github.com/OliverS929)
        - 修复 DM validator 对 UNSIGNED 列误报校验错误的问题 [#12555](https://github.com/pingcap/tiflow/pull/12555) @[OliverS929](https://github.com/OliverS929)

    + TiDB Lightning

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - 修复 Dumpling 与 MySQL 8.4 的兼容性问题 [#65131](https://github.com/pingcap/tidb/pull/65131) @[dveeden](https://github.com/dveeden)

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
