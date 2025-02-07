---
title: 使用资源管控 (Resource Control) 管理后台任务
summary: 介绍如何通过资源管控 (Resource Control) 控制后台任务。
---
# 使用资源管控 (Resource Control) 管理后台任务

> **警告：**
>
> - 该功能目前为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。如果发现 bug，请[提交 issue](/support.md) 反馈。
> - 资源管控的后台任务管理是基于 TiKV 的 CPU/IO 的资源利用率动态调整资源配额的，因此它依赖各个实例可用资源上限 (Quota)。如果在单个服务器混合部署多个组件或实例，需要通过 `cgroup` 为各个实例设置合适的资源上限 (Quota)。TiUP Playground 等共享资源的配置很难表现出预期效果。

后台任务是指那些优先级不高但是需要消耗大量资源的任务，如数据备份和自动统计信息收集等。这些任务通常定期或不定期触发，在执行的时候会消耗大量资源，从而影响在线的高优先级任务的性能。

自 v7.4.0 开始，[TiDB 资源管控](/tidb-resource-control-ru-groups.md)引入了对后台任务的管理。当一种任务被标记为后台任务时，TiKV 会动态地限制该任务的资源使用，以尽量避免此类任务在执行时对其他前台任务的性能产生影响。TiKV 通过实时地监测所有前台任务所消耗的 CPU 和 IO 等资源，并根据实例总的资源上限计算出后台任务可使用的资源阈值，所有后台任务在执行时会受此阈值的限制。

## `BACKGROUND` 参数说明

- `TASK_TYPES`：设置需要作为后台任务管理的任务类型，多个任务类型以 `,` 分隔。
- `UTILIZATION_LIMIT`：限制每个 TiKV 节点上后台任务最大可以使用的资源百分比 (0-100)。默认情况下，TiKV 会根据节点的总资源以及当前前台任务所占用的资源，来计算后台任务的可用资源。如果设置此限制，则实际分配给后台任务的资源不会超过此限制的比例。

目前 TiDB 支持如下几种后台任务的类型：

- `lightning`：使用 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 执行导入任务。同时支持 TiDB Lightning 的物理和逻辑导入模式。
- `br`：使用 [BR](/br/backup-and-restore-overview.md) 执行数据备份和恢复。目前不支持 PITR。
- `ddl`：对于 Reorg DDL，控制批量数据回写阶段的资源使用。
- `stats`：对应手动执行或系统自动触发的[收集统计信息](/statistics.md#收集统计信息)任务。
- `background`：预留的任务类型，可使用 [`tidb_request_source_type`](/system-variables.md#tidb_request_source_type-从-v740-版本开始引入) 系统变量指定当前会话的任务类型为 `background`。

默认情况下，被标记为后台任务的任务类型为 `""`，此时后台任务的管理功能处于关闭状态。如需开启后台任务管理功能，你需要手动修改 `default` 资源组的后台任务类型以开启后台任务管理。后台任务类型被识别匹配后，资源管控会自动进行，即当系统资源紧张时，后台任务会自动降为最低优先级，保证前台任务的执行。

> **注意：**
>
> 目前，所有资源组的后台任务默认都会绑定到默认资源组 `default` 下进行管控，你可以通过 `default` 全局管控后台任务类型。暂不支持将后台任务绑定到其他资源组。

## 示例

1. 修改 `default` 资源组，将 `br` 和 `ddl` 标记为后台任务，并配置后台任务最多可使用 TiKV 节点总资源的 30%。

    ```sql
    ALTER RESOURCE GROUP `default` BACKGROUND=(TASK_TYPES='br,ddl', UTILIZATION_LIMIT=30);
    ```

2. 修改 `default` 资源组，将后台任务的类型还原为默认值。

    ```sql
    ALTER RESOURCE GROUP `default` BACKGROUND=NULL;
    ```

3. 修改 `default` 资源组，将后台任务的类型设置为空，此时此资源组的所有任务类型都不会作为后台任务处理。

    ```sql
    ALTER RESOURCE GROUP `default` BACKGROUND=(TASK_TYPES="");
    ```

4. 查看 `default` 资源组的后台任务类型。

    ```sql
    SELECT * FROM information_schema.resource_groups WHERE NAME="default";
    ```

    输出结果如下：

    ```
    +---------+------------+----------+-----------+-------------+-------------------------------------------+
    | NAME    | RU_PER_SEC | PRIORITY | BURSTABLE | QUERY_LIMIT | BACKGROUND                                |
    +---------+------------+----------+-----------+-------------+-------------------------------------------+
    | default | UNLIMITED  | MEDIUM   | YES       | NULL        | TASK_TYPES='br,ddl', UTILIZATION_LIMIT=30 |
    +---------+------------+----------+-----------+-------------+-------------------------------------------+
    ```

5. 如果希望将当前会话里的任务显式标记为后台类型，你可以使用 `tidb_request_source_type` 显式指定任务类型，如：

    ``` sql
    SET @@tidb_request_source_type="background";
    /* 添加 background 任务类型 */
    ALTER RESOURCE GROUP `default` BACKGROUND=(TASK_TYPES="background");
    /* 在当前会话中执行 LOAD DATA */
    LOAD DATA INFILE "s3://resource-control/Lightning/test.customer.aaaa.csv"
    ```