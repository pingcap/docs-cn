---
title: 迁移升级 TiDB 集群
summary: 本文介绍如何使用 BR 全量备份恢复与 TiCDC 增量数据同步实现 TiDB 集群的迁移升级。
---

# 迁移升级 TiDB 集群

本文介绍如何使用 [BR](/br/backup-and-restore-overview.md) 全量备份恢复与 [TiCDC](/ticdc/ticdc-overview.md) 增量数据同步实现 TiDB 集群的迁移升级（又称蓝绿升级）。该方案通过双集群冗余架构与增量同步技术，确保业务流量平滑切换并支持快速回退，为关键业务系统提供高可靠、低风险的升级路径。建议定期升级数据库版本，以持续获得性能优化与新特性，构建安全高效的数据库体系。该方案具体优势如下：

- **风险可控**：支持分钟级回退至旧版本集群，确保业务连续性。
- **数据完整**：采用多阶段验证机制，确保数据零丢失。
- **业务影响小**：仅需一次短暂停机窗口即可完成最终切换。

迁移升级的核心流程如下：

1. **风险预检**：检查集群状态与方案适用性。
2. **准备新集群**：基于旧集群的全量备份创建新集群，并升级至目标版本。
3. **增量同步**：通过 TiCDC 建立正向数据同步通道。
4. **切换验证**：完成多维度验证后，将业务流量切换至新集群，并建立 TiCDC 回退通道。
5. **观察状态**：维持回退通道。观察期结束后清理环境。

**回退计划**：在迁移升级过程中，如果新集群出现故障，可随时将业务流量切换回旧集群。

迁移升级 TiDB 集群的标准化流程和通用操作步骤如下，相关命令以 TiDB Self-Managed 环境为例。

## 步骤一：评估方案可行性

在开始迁移升级前，需评估相关组件的适用性，并检查集群的健康状态。

- 检查 TiDB 集群的版本：此迁移升级方案适用于 v6.5.0 及以上版本的 TiDB 集群。

- 检查 TiCDC 适用性：

    - **表结构要求**：确保待同步的表包含有效索引，详见 [TiCDC 有效索引](/ticdc/ticdc-overview.md#有效索引)。
    - **功能限制**：TiCDC 暂不支持 Sequence、TiFlash DDL 同步等，详见 [TiCDC 暂不支持的场景](/ticdc/ticdc-overview.md#暂不支持的场景)。
    - **最佳实践**：在切换过程中，应尽量避免在 TiCDC 的上游集群执行 DDL 操作。

- 检查 BR 适用性：

    - 查看 BR 全量备份的兼容性说明，详见 [BR 版本兼容性矩阵](/br/backup-and-restore-overview.md#tidb-v650-版本到-v850-之间的-br-版本兼容性矩阵)。
    - 检查 BR 备份与恢复功能的已知限制，详见 [BR 使用限制](/br/backup-and-restore-overview.md#使用限制)。

- 检查集群健康状态，例如 [Region](/glossary.md#regionpeerraft-group) 的健康状态、节点资源利用率等。

## 步骤二：准备新集群

### 1. 调整旧集群的 GC lifetime

为确保数据同步链路的稳定性，必须调整系统变量 [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-从-v50-版本开始引入) 的值，以确保其足以覆盖以下操作及其间隔的总时长：BR 备份、恢复、升级集群版本和创建 TiCDC Changefeed 同步链路。否则，同步任务将进入不可恢复的 `failed` 状态。此时整个迁移升级的步骤，需要重新开始一个新的全量备份开始执行。

以下示例将 `tidb_gc_life_time` 调整为 `60h`：

```sql
-- 查看当前 GC lifetime 设置
SHOW VARIABLES LIKE '%tidb_gc_life_time%';
-- 设置 GC lifetime
SET GLOBAL tidb_gc_life_time=60h;
```

> **注意：**
>
> 调高 `tidb_gc_life_time` 会增加 [MVCC](/glossary.md#multi-version-concurrency-control-mvcc) 版本数据占用的存储空间，并可能影响查询性能。详见 [GC 机制简介](/garbage-collection-overview.md)。建议综合考虑存储和性能影响，根据预计的操作总时长合理设置 GC 时长。

### 2. 迁移全量数据到新集群

迁移全量数据到新集群时，需注意以下事项：

- **版本匹配**：执行备份与恢复时，BR 组件的版本需与旧集群的大版本保持一致。
- **性能影响**：BR 备份会占用系统资源，建议在业务低峰期执行备份操作，以减少对业务的影响。
- **时间预估**：在无硬件资源瓶颈（磁盘 IO、网络带宽等）的情况下，可以参考以下时间：

    - 备份速度：单个 TiKV 节点数据量为 1 TiB，使用 8 个线程备份大约需 1 小时。
    - 恢复速度：单个 TiKV 节点数据量为 1 TiB，平均恢复时间大约为 20 分钟。

- **配置一致性**：确保新旧集群的 [`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap) 配置项相同，否则 BR 恢复会失败。
- **系统表恢复**：执行 BR 恢复时，需使用 `--with-sys-table` 选项，以恢复部分系统表数据。

迁移全量数据到新集群的具体操作步骤如下：

1. 对旧集群执行 BR 全量备份：

    ```shell
    tiup br:${cluster_version} backup full --pd ${pd_host}:${pd_port} -s ${backup_location}
    ```

2. 记录旧集群的 TSO，用于后续创建 TiCDC Changefeed：

    ```shell
    tiup br:${cluster_version} validate decode --field="end-version" \
    --storage "s3://xxx?access-key=${access-key}&secret-access-key=${secret-access-key}" | tail -n1
    ```

3. 部署新集群：

    ```shell
    tiup cluster deploy ${new_cluster_name} ${cluster_version} tidb-cluster.yaml
    ```

4. 将全量备份恢复到新集群：

    ```shell
    tiup br:${cluster_version} restore full --pd ${pd_host}:${pd_port} -s ${backup_location} --with-sys-table
    ```

### 3. 升级新集群至目标版本

为节省时间，可执行以下命令进行停机升级。关于更多 TiDB 升级方式，参考[使用 TiUP 升级 TiDB](/upgrade-tidb-using-tiup.md)。

```shell
tiup cluster stop <new_cluster_name>      # 暂停集群
tiup cluster upgrade <new_cluster_name> <v_target_version> --offline  # 停机升级
tiup cluster start <new_cluster_name>     # 启动集群
```

此外，还需同步旧集群必要的关键配置至新集群，例如系统配置项和系统变量等，以确保业务运行一致性。

## 步骤三：同步增量数据

### 1. 建立正向数据同步通道

现在，旧集群为原始版本，新集群已升级至目标版本。接下来，需要建立从旧集群到新集群的正向数据同步通道。

> **注意：**
>
> TiCDC 组件的版本需与旧集群的大版本保持一致。

- 创建 Changefeed 同步任务，其中增量同步起始点 `${tso}` 为[步骤二](#步骤二准备新集群)中记录的备份的准确时间戳 TSO，以避免数据丢失：

    ```shell
    tiup ctl:${cluster_version} cdc changefeed create --server http://${cdc_host}:${cdc_port} --sink-uri="mysql://${username}:${password}@${tidb_endpoint}:${port}" --config config.toml --start-ts ${tso}
    ```

- 检查同步任务状态，确认 `tso` 或 `checkpoint` 是否在持续推进：

    ```shell
    tiup ctl:${cluster_version} cdc changefeed list --server http://${cdc_host}:${cdc_port}
    ```

    输出示例如下：

    ```shell
    [{
        "id": "cdcdb-cdc-task-standby",
        "summary": {
          "state": "normal",
          "tso": 417886179132964865,
          "checkpoint": "202x-xx-xx xx:xx:xx.xxx",
          "error": null
        }
    }]
    ```

在同步增量数据期间，需要持续监控数据同步通道的运行状态，并进行必要调整：

- 延迟指标：`Changefeed checkpoint lag` 应保持在较小范围内，例如 5 分钟内。
- 吞吐健康：`Sink flush rows/s` 应持续高于业务写入速率。
- 异常告警：定期检查 TiCDC 节点日志与告警信息。
- （可选）测试数据同步：更新一些测试数据，验证 Changefeed 是否能将其同步到新集群。
- （可选）调整 TiCDC 的配置项 [`gc-ttl`](/ticdc/ticdc-server-config.md#gc-ttl)（默认值为 24 小时）。

    当同步任务不可用或因某种原因中断，且无法及时解决时，`gc-ttl` 配置可确保 TiCDC 需要消耗的数据保留在 TiKV 中而不被集群 GC 清理。超过此时间后，同步任务将进入 `failed` 状态且无法恢复，而 PD 对应的服务 GC 安全点会继续推进，这种情况下需要重新开始新的备份。

    增加 `gc-ttl` 配置的值会累积更多 MVCC 数据，影响与调大 `tidb_gc_life_time` 相同，因此建议设置为合理的足够长的值。

### 2. 检查数据是否一致

数据同步完成后，需要验证新旧集群数据是否一致。可使用以下方法：

- 使用 [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md) 工具：

    ```shell
    ./sync_diff_inspector --config=./config.toml
    ```

- 使用 [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md) 的 snapshot 配置结合 TiCDC 的 [Syncpoint](/ticdc/ticdc-upstream-downstream-check.md) 功能，在不停止 Changefeed 同步任务的情况下，对新旧集群数据进行一致性验证。详见 [TiDB 主从集群数据校验和快照读](/ticdc/ticdc-upstream-downstream-check.md)。

- 通过业务数据层面的手工校验方式确认数据一致性，例如对比表的行数是否一致。

### 3. 检查环境就绪状态

本文使用 BR `--with-sys-table` 选项恢复部分系统表数据。对于不在恢复范围的内容，需要手动补齐。常见需要检查和补齐的内容包括：

- 权限体系：对比 `mysql.user` 表。
- 配置：包括各节点的参数配置和系统变量。
- 自增列：在新集群上清除自增 ID 的缓存。
- 统计信息：新集群可使用手动或自动收集方式。

此外，还可对新集群进行扩容，以满足预计的业务负载，并迁移周边运维任务，如告警订阅、定时统计信息收集脚本和数据备份脚本等。

## 步骤四：切换业务流量及回退

### 1. 切换前准备

- 确认同步状态：

    - 监控 TiCDC Changefeed 的同步延迟。
    - 确保增量同步的吞吐量大于或等于业务写入峰值。

- 执行多维度验证，例如：

    - 确保所有数据和内容验证步骤均已完成，并补充必要的检查项。
    - 在新集群上对应用程序进行合理性测试或集成测试。

### 2. 执行切换

1. 停止应用服务，确保旧集群不再承载业务流量。此外，可以通过以下方式进一步确保集群不会被访问：

    - 锁定旧集群的用户账户：

        ```sql
        ALTER USER ACCOUNT LOCK;
        ```

    - 将旧集群设为只读模式。建议重启旧集群的 TiDB 节点，以清理业务会话连接，防止未进入只读状态的连接：

        ```sql
        SET GLOBAL tidb_super_read_only=ON;
        ```

2. 确认 TiCDC 追平：

    - 在旧集群进入只读模式后，获取旧集群当前的 `up-tso`：

        ```sql
        BEGIN; SELECT TIDB_CURRENT_TSO(); ROLLBACK;
        ```

    - 观察 Changefeed `checkpointTs`，确保其大于 `up-tso`，即 TiCDC 已完成数据同步。

3. 确保新旧集群数据一致：

    - 在 TiCDC 追平后，获取新集群的 `down-tso`。
    - 使用 [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md) 工具对比新旧集群在 `up-tso` 和 `down-tso` 时刻的数据一致性。

4. 暂停 Changefeed 正向同步任务：

    ```shell
    tiup ctl:${cluster_version} cdc changefeed pause --server http://${cdc_host}:${cdc_port} -c <changefeedid>
    ```

5. 重启新集群的 TiDB 节点，以清除自增 ID 的缓存。

6. 检查新集群运行状态，可以通过以下方式确认：

    - 检查 TiDB 版本信息是否与目标版本一致：

        ```shell
        tiup cluster display <cluster-name>
        ```

    - 登录数据库，检查各组件版本是否符合预期：

        ```sql
        SELECT * FROM INFORMATION_SCHEMA.CLUSTER_INFO;
        ```

    - 通过 Grafana 监控服务状态：查看 [**Overview 面板 > Services Port Status**](/grafana-overview-dashboard.md#services-port-status)，确保所有服务均为 **Up** 状态。

7. 建立从新集群到旧集群的逆向数据同步通道。

    1. 解锁旧集群的用户账户，并恢复其读写模式：

        ```sql
        ALTER USER ACCOUNT UNLOCK;
        SET GLOBAL tidb_super_read_only=OFF;
        ```

    2. 记录新集群当前的 TSO：

        ```sql
        BEGIN; SELECT TIDB_CURRENT_TSO(); ROLLBACK;
        ```

    3. 配置逆向数据同步链路，并确认 Changefeed 任务正常：

        - 由于此时业务已停止，可使用当前 TSO。
        - 确保 `sink-uri` 设置为旧集群的地址，以避免回环写入风险。

        ```shell
        tiup ctl:${cluster_version} cdc changefeed create --server http://${cdc_host}:${cdc_port} --sink-uri="mysql://${username}:${password}@${tidb_endpoint}:${port}" --config config.toml --start-ts ${tso}

        tiup ctl:${cluster_version} cdc changefeed list --server http://${cdc_host}:${cdc_port}
        ```

8. 切换业务流量到新集群。

9. 检查新集群的负载及运行状态是否正常，可以通过以下 Grafana 面板进行监控：

    - [**TiDB Dashboard** > **Query Summary**](/grafana-tidb-dashboard.md#query-summary)：检查 Duration、QPS、Failed Query OPM 监控项是否正常。
    - [**TiDB Dashboard** > **Server**](/grafana-tidb-dashboard.md#server)：检查 Connection Count 监控项，查看各节点之间的连接数是否均匀。

此时，业务流量已成功切换至新集群，并建立了 TiCDC 逆向同步通道。

### 3. 应急回滚

回退方案：

- 定期检查新旧集群的数据一致性，确保逆向同步链路正常运行。
- 观察一段时间，例如一周，如发现问题，可随时切换回旧集群。
- 观察期结束后，关闭 TiCDC 逆向同步链路，并下线旧集群。

应急回滚：流量切回旧集群

- 适用场景：当业务在短时间内无法解决关键问题时，需要考虑是否实施回退方案。
- 操作步骤：

    1. 停止对新集群的业务访问。
    2. 重新授权业务账户，恢复对旧集群的读写权限。
    3. 检查逆向同步链路，确认 TiCDC 追平，并确保新旧集群数据一致。
    4. 切换业务流量回旧集群。

## 步骤五：结束与清理

经过一段时间的观察，确认业务在新集群上稳定运行后，可下线 TiCDC 逆向同步链路并删除旧集群：

- 下线 TiCDC 逆向同步链路：

    ```shell
    tiup ctl:${cluster_version} cdc changefeed remove --server http://${cdc_host}:${cdc_port} -c <changefeedid>
    ```

- 删除旧集群。如果不删除，请确保将 `tidb_gc_life_time` 恢复为原始值：

    ```sql
    -- 恢复为变更前的值
    SET GLOBAL tidb_gc_life_time=10m;
    ```
