---
title: 使用资源控制实现资源隔离
summary: 了解如何使用资源控制功能来控制和调度应用程序资源。
---

# 使用资源控制实现资源隔离

> **注意：**
>
> 此功能在 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

作为集群管理员，你可以使用资源控制功能创建资源组，为资源组设置配额，并将用户绑定到这些组。

TiDB 资源控制功能提供两层资源管理能力：TiDB 层的流量控制能力和 TiKV 层的优先级调度能力。这两种能力可以单独或同时启用。详见[资源控制参数](#资源控制参数)。这使得 TiDB 层能够根据资源组设置的配额控制用户读写请求的流量，并使 TiKV 层能够根据与读写配额映射的优先级调度请求。通过这种方式，你可以确保应用程序的资源隔离并满足服务质量（QoS）要求。

- TiDB 流量控制：TiDB 流量控制使用[令牌桶算法](https://en.wikipedia.org/wiki/Token_bucket)。如果桶中没有足够的令牌，并且资源组未指定 `BURSTABLE` 选项，对该资源组的请求将等待令牌桶补充令牌并重试。重试可能因超时而失败。

- TiKV 调度：你可以根据需要设置绝对优先级 [(`PRIORITY`)](/information-schema/information-schema-resource-groups.md#examples)。不同的资源根据 `PRIORITY` 设置进行调度。高 `PRIORITY` 的任务优先调度。如果你没有设置绝对优先级，TiKV 使用每个资源组的 `RU_PER_SEC` 值来确定每个资源组的读写请求优先级。基于这些优先级，存储层使用优先级队列来调度和处理请求。

从 v7.4.0 开始，资源控制功能支持控制 TiFlash 资源。其原理与 TiDB 流量控制和 TiKV 调度类似：

<CustomContent platform="tidb">

- TiFlash 流量控制：通过 [TiFlash pipeline 执行模型](/tiflash/tiflash-pipeline-model.md)，TiFlash 可以更准确地获取不同查询的 CPU 消耗并转换为 [Request Units (RU)](#什么是请求单位-ru) 进行扣减。流量控制使用令牌桶算法实现。
- TiFlash 调度：当系统资源不足时，TiFlash 根据资源组的优先级在多个资源组之间调度 pipeline 任务。具体逻辑是：首先评估资源组的 `PRIORITY`，然后考虑 CPU 使用率和 `RU_PER_SEC`。因此，如果 `rg1` 和 `rg2` 具有相同的 `PRIORITY` 但 `rg2` 的 `RU_PER_SEC` 是 `rg1` 的两倍，那么 `rg2` 的 CPU 使用率是 `rg1` 的两倍。

</CustomContent>

<CustomContent platform="tidb-cloud">

- TiFlash 流量控制：通过 [TiFlash pipeline 执行模型](http://docs.pingcap.com/tidb/dev/tiflash-pipeline-model)，TiFlash 可以更准确地获取不同查询的 CPU 消耗并转换为 [Request Units (RU)](#什么是请求单位-ru) 进行扣减。流量控制使用令牌桶算法实现。
- TiFlash 调度：当系统资源不足时，TiFlash 根据资源组的优先级在多个资源组之间调度 pipeline 任务。具体逻辑是：首先评估资源组的 `PRIORITY`，然后考虑 CPU 使用率和 `RU_PER_SEC`。因此，如果 `rg1` 和 `rg2` 具有相同的 `PRIORITY` 但 `rg2` 的 `RU_PER_SEC` 是 `rg1` 的两倍，那么 `rg2` 的 CPU 使用率是 `rg1` 的两倍。

</CustomContent>

## 资源控制的应用场景

资源控制功能的引入是 TiDB 的一个里程碑。它可以将分布式数据库集群划分为多个逻辑单元。即使某个单元过度使用资源，也不会挤占其他单元所需的资源。

通过此功能，你可以：

- 将来自不同系统的多个中小型应用程序合并到单个 TiDB 集群中。当某个应用程序的工作负载增大时，不会影响其他应用程序的正常运行。当系统工作负载较低时，即使超出设定配额，繁忙的应用程序仍然可以获得所需的系统资源，从而实现资源的最大利用。
- 选择将所有测试环境合并到单个 TiDB 集群中，或将消耗更多资源的批处理任务分组到单个资源组中。这可以提高硬件利用率并降低运营成本，同时确保关键应用程序始终能获得必要的资源。
- 当系统中存在混合工作负载时，你可以将不同的工作负载放入单独的资源组中。通过使用资源控制功能，你可以确保事务应用程序的响应时间不受数据分析或批处理应用程序的影响。
- 当集群遇到意外的 SQL 性能问题时，你可以将 SQL 绑定与资源组结合使用，临时限制 SQL 语句的资源消耗。

此外，合理使用资源控制功能可以减少集群数量，降低运维难度，节省管理成本。

> **注意：**
>
> - 要评估资源管理的有效性，建议将集群部署在独立的计算和存储节点上。在使用 `tiup playground` 创建的部署中，由于实例之间共享资源，调度和其他集群资源敏感功能很难正常工作。

## 限制

资源控制会产生额外的调度开销。因此，启用此功能时可能会出现轻微的性能下降（小于 5%）。

## 什么是请求单位 (RU)

请求单位（Request Unit，RU）是 TiDB 中系统资源的统一抽象单位，目前包括 CPU、IOPS 和 IO 带宽指标。它用于表示对数据库的单个请求所消耗的资源量。一个请求消耗的 RU 数量取决于多种因素，例如操作类型以及被查询或修改的数据量。目前，RU 包含以下表格中资源的消耗统计：

<table>
    <thead>
        <tr>
            <th>资源类型</th>
            <th>RU 消耗</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan="3">读取</td>
            <td>2 个存储读取批次消耗 1 RU</td>
        </tr>
        <tr>
            <td>8 个存储读取请求消耗 1 RU</td>
        </tr>
        <tr>
            <td>64 KiB 读取请求负载消耗 1 RU</td>
        </tr>
        <tr>
            <td rowspan="3">写入</td>
            <td>1 个存储写入批次消耗 1 RU</td>
        </tr>
        <tr>
            <td>1 个存储写入请求消耗 1 RU</td>
        </tr>
        <tr>
            <td>1 KiB 写入请求负载消耗 1 RU</td>
        </tr>
        <tr>
            <td>CPU</td>
            <td>3 毫秒消耗 1 RU</td>
        </tr>
    </tbody>
</table>

> **注意：**
>
> - 每个写入操作最终都会复制到所有副本（默认情况下，TiKV 有 3 个副本）。每个复制操作都被视为不同的写入操作。
> - 上表仅列出了 TiDB 自管理集群中涉及 RU 计算的资源，不包括网络和存储消耗。关于 TiDB Cloud Serverless RU，请参见 [TiDB Cloud Serverless 定价详情](https://www.pingcap.com/tidb-cloud-serverless-pricing-details/)。
> - 目前，TiFlash 资源控制仅考虑 SQL CPU，即查询的 pipeline 任务执行所消耗的 CPU 时间，以及读取请求负载。

## 资源控制参数

资源控制功能引入了以下系统变量或参数：

* TiDB：你可以使用 [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660) 系统变量来控制是否启用资源组的流量控制。

<CustomContent platform="tidb">

* TiKV：你可以使用 [`resource-control.enabled`](/tikv-configuration-file.md#resource-control) 参数来控制是否基于资源组使用请求调度。
* TiFlash：你可以使用 [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660) 系统变量和 [`enable_resource_control`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) 配置项（v7.4.0 引入）来控制是否启用 TiFlash 资源控制。

</CustomContent>

<CustomContent platform="tidb-cloud">

* TiKV：对于 TiDB 自管理版本，你可以使用 `resource-control.enabled` 参数来控制是否基于资源组配额使用请求调度。对于 TiDB Cloud，`resource-control.enabled` 参数默认值为 `true` 且不支持动态修改。
* TiFlash：对于 TiDB 自管理版本，你可以使用 `tidb_enable_resource_control` 系统变量和 `enable_resource_control` 配置项（v7.4.0 引入）来控制是否启用 TiFlash 资源控制。

</CustomContent>

从 TiDB v7.0.0 开始，`tidb_enable_resource_control` 和 `resource-control.enabled` 默认启用。这两个参数组合的结果如下表所示：

| `resource-control.enabled`  | `tidb_enable_resource_control`= ON   | `tidb_enable_resource_control`= OFF  |
|:----------------------------|:-------------------------------------|:-------------------------------------|
| `resource-control.enabled`= true  | 流量控制和调度（推荐） | 无效组合      |
| `resource-control.enabled`= false | 仅流量控制（不推荐）                 | 功能禁用 |

<CustomContent platform="tidb">

从 v7.4.0 开始，TiFlash 配置项 `enable_resource_control` 默认启用。它与 `tidb_enable_resource_control` 一起控制 TiFlash 资源控制功能。只有当 `enable_resource_control` 和 `tidb_enable_resource_control` 都启用时，TiFlash 资源控制才会执行流量控制和优先级调度。此外，当 `enable_resource_control` 启用时，TiFlash 使用 [Pipeline 执行模型](/tiflash/tiflash-pipeline-model.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

从 v7.4.0 开始，TiFlash 配置项 `enable_resource_control` 默认启用。它与 `tidb_enable_resource_control` 一起控制 TiFlash 资源控制功能。只有当 `enable_resource_control` 和 `tidb_enable_resource_control` 都启用时，TiFlash 资源控制才会执行流量控制和优先级调度。此外，当 `enable_resource_control` 启用时，TiFlash 使用 [Pipeline 执行模型](http://docs.pingcap.com/tidb/dev/tiflash-pipeline-model)。

</CustomContent>

有关资源控制机制和参数的更多信息，请参见 [RFC: Global Resource Control in TiDB](https://github.com/pingcap/tidb/blob/release-8.1/docs/design/2022-11-25-global-resource-control.md) 和 [TiFlash Resource Control](https://github.com/pingcap/tiflash/blob/release-8.1/docs/design/2023-09-21-tiflash-resource-control.md)。

## 如何使用资源控制

本节描述如何使用资源控制功能来管理资源组并控制每个资源组的资源分配。

### 估算集群容量

<CustomContent platform="tidb">

在进行资源规划之前，你需要了解集群的整体容量。TiDB 提供了 [`CALIBRATE RESOURCE`](/sql-statements/sql-statement-calibrate-resource.md) 语句来估算集群容量。你可以使用以下方法之一：

- [基于实际工作负载估算容量](/sql-statements/sql-statement-calibrate-resource.md#基于实际工作负载估算容量)
- [基于硬件部署估算容量](/sql-statements/sql-statement-calibrate-resource.md#基于硬件部署估算容量)

你可以查看 TiDB Dashboard 中的[资源管理页面](/dashboard/dashboard-resource-manager.md)。更多信息，请参见 [`CALIBRATE RESOURCE`](/sql-statements/sql-statement-calibrate-resource.md#估算容量的方法)。

</CustomContent>

<CustomContent platform="tidb-cloud">

对于 TiDB 自管理版本，你可以使用 [`CALIBRATE RESOURCE`](https://docs.pingcap.com/tidb/stable/sql-statement-calibrate-resource) 语句来估算集群容量。

对于 TiDB Cloud，[`CALIBRATE RESOURCE`](https://docs.pingcap.com/tidb/stable/sql-statement-calibrate-resource) 语句不适用。

</CustomContent>

### 管理资源组

要创建、修改或删除资源组，你需要具有 `SUPER` 或 `RESOURCE_GROUP_ADMIN` 权限。

你可以使用 [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md) 为集群创建资源组。

对于现有资源组，你可以使用 [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md) 修改资源组的 `RU_PER_SEC` 选项（每秒补充 RU 的速率）。对资源组的更改会立即生效。

你可以使用 [`DROP RESOURCE GROUP`](/sql-statements/sql-statement-drop-resource-group.md) 删除资源组。

### 创建资源组

以下是创建资源组的示例。

1. 创建资源组 `rg1`。资源限制为每秒 500 RU，并允许该资源组中的应用程序超出资源限制。

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg1 RU_PER_SEC = 500 BURSTABLE;
    ```

2. 创建资源组 `rg2`。RU 补充速率为每秒 600 RU，并且不允许该资源组中的应用程序超出资源限制。

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg2 RU_PER_SEC = 600;
    ```

3. 创建资源组 `rg3`，并将绝对优先级设置为 `HIGH`。绝对优先级当前支持 `LOW|MEDIUM|HIGH`。默认值为 `MEDIUM`。

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg3 RU_PER_SEC = 100 PRIORITY = HIGH;
    ```

### 绑定资源组

TiDB 支持以下三个级别的资源组设置。

- 用户级别。通过 [`CREATE USER`](/sql-statements/sql-statement-create-user.md) 或 [`ALTER USER`](/sql-statements/sql-statement-alter-user.md#修改用户绑定的资源组) 语句将用户绑定到特定资源组。用户绑定到资源组后，该用户创建的会话会自动绑定到相应的资源组。
- 会话级别。通过 [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md) 设置当前会话的资源组。
- 语句级别。通过 [`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name) 优化器提示设置当前语句的资源组。

#### 将用户绑定到资源组

以下示例创建用户 `usr1` 并将其绑定到资源组 `rg1`。`rg1` 是在[创建资源组](#创建资源组)示例中创建的资源组。

```sql
CREATE USER 'usr1'@'%' IDENTIFIED BY '123' RESOURCE GROUP rg1;
```

以下示例使用 `ALTER USER` 将用户 `usr2` 绑定到资源组 `rg2`。`rg2` 是在[创建资源组](#创建资源组)示例中创建的资源组。

```sql
ALTER USER usr2 RESOURCE GROUP rg2;
```

绑定用户后，新创建的会话的资源消耗将受到指定配额（Request Unit，RU）的控制。如果系统工作负载相对较高且没有空闲容量，`usr2` 的资源消耗率将被严格控制不超过配额。因为 `usr1` 绑定的是配置了 `BURSTABLE` 的 `rg1`，所以允许 `usr1` 的消耗率超过配额。

如果有太多请求导致资源组资源不足，客户端的请求将等待。如果等待时间太长，请求将报错。

> **注意：**
>
> - 当你使用 `CREATE USER` 或 `ALTER USER` 将用户绑定到资源组时，它不会对用户的现有会话生效，而只会对用户的新会话生效。
> - TiDB 在集群初始化期间自动创建 `default` 资源组。对于此资源组，`RU_PER_SEC` 的默认值为 `UNLIMITED`（相当于 `INT` 类型的最大值，即 `2147483647`），并且处于 `BURSTABLE` 模式。未绑定到资源组的语句会自动绑定到此资源组。此资源组不支持删除，但你可以修改其 RU 配置。

要将用户从资源组解绑，你可以简单地将它们重新绑定到 `default` 组，如下所示：

```sql
ALTER USER 'usr3'@'%' RESOURCE GROUP `default`;
```

更多详情，请参见 [`ALTER USER ... RESOURCE GROUP`](/sql-statements/sql-statement-alter-user.md#修改用户绑定的资源组)。

#### 将当前会话绑定到资源组

通过将会话绑定到资源组，相应会话的资源使用受到指定使用量（RU）的限制。

以下示例将当前会话绑定到资源组 `rg1`。

```sql
SET RESOURCE GROUP rg1;
```

#### 将当前语句绑定到资源组

通过在 SQL 语句中添加 [`RESOURCE_GROUP(resource_group_name)`](/optimizer-hints.md#resource_groupresource_group_name) 提示，你可以指定语句绑定的资源组。此提示支持 `SELECT`、`INSERT`、`UPDATE` 和 `DELETE` 语句。

以下示例将当前语句绑定到资源组 `rg1`。

```sql
SELECT /*+ RESOURCE_GROUP(rg1) */ * FROM t limit 10;
```

### 管理消耗超出预期资源的查询（Runaway Queries）

Runaway query 是指消耗时间或资源超出预期的查询（仅限 `SELECT` 语句）。以下使用 **runaway queries** 来描述管理 runaway query 的功能。

- 从 v7.2.0 开始，资源控制功能引入了对 runaway queries 的管理。你可以为资源组设置标准来识别 runaway queries，并自动采取行动防止它们耗尽资源和影响其他查询。你可以通过在 [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md) 或 [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md) 中包含 `QUERY_LIMIT` 字段来管理资源组的 runaway queries。
- 从 v7.3.0 开始，资源控制功能引入了 runaway watches 的手动管理，可以快速识别给定 SQL 语句或 Digest 的 runaway queries。你可以执行 [`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md) 语句来手动管理资源组中的 runaway queries 监视列表。

#### `QUERY_LIMIT` 参数

支持的条件设置：

- `EXEC_ELAPSED`：当查询执行时间超过此限制时，将其识别为 runaway query。

支持的操作（`ACTION`）：

- `DRYRUN`：不采取任何行动。仅为 runaway queries 添加记录。这主要用于观察条件设置是否合理。
- `COOLDOWN`：将查询的执行优先级降低到最低级别。查询继续以最低优先级执行，不占用其他操作的资源。
- `KILL`：自动终止被识别的查询并报错 `Query execution was interrupted, identified as runaway query`。

为了避免太多并发的 runaway queries 耗尽系统资源，资源控制功能引入了快速识别机制，可以快速识别和隔离 runaway queries。你可以通过 `WATCH` 子句使用此功能。当查询被识别为 runaway query 时，此机制提取查询的匹配特征（由 `WATCH` 后的参数定义）。在接下来的一段时间内（由 `DURATION` 定义），runaway query 的匹配特征被添加到监视列表中，TiDB 实例将查询与监视列表进行匹配。匹配的查询直接被标记为 runaway queries 并根据相应的操作进行隔离，而不是等待它们被条件识别。`KILL` 操作终止查询并报错 `Quarantined and interrupted because of being in runaway watch list`。

`WATCH` 有三种匹配方法用于快速识别：

- `EXACT` 表示只有完全相同的 SQL 文本才会被快速识别。
- `SIMILAR` 表示通过 SQL Digest 匹配所有具有相同模式的 SQL 语句，忽略字面值。
- `PLAN` 表示通过 Plan Digest 匹配所有具有相同模式的 SQL 语句。

`WATCH` 中的 `DURATION` 选项表示识别项的持续时间，默认为无限期。

添加监视项后，无论 `QUERY_LIMIT` 配置如何更改或删除，匹配特征和 `ACTION` 都不会更改或删除。你可以使用 `QUERY WATCH REMOVE` 删除监视项。

`QUERY_LIMIT` 的参数如下：

| 参数          | 描述            | 说明                                  |
|---------------|--------------|--------------------------------------|
| `EXEC_ELAPSED`  | 当查询执行时间超过此值时，将其识别为 runaway query | EXEC_ELAPSED =`60s` 表示如果执行时间超过 60 秒，则将查询识别为 runaway query。 |
| `ACTION`    | 识别到 runaway query 时采取的行动 | 可选值为 `DRYRUN`、`COOLDOWN` 和 `KILL`。 |
| `WATCH`   | 快速匹配已识别的 runaway query。如果在一定时间内再次遇到相同或类似的查询，立即执行相应的操作。 | 可选。例如 `WATCH=SIMILAR DURATION '60s'`、`WATCH=EXACT DURATION '1m'` 和 `WATCH=PLAN`。 |

#### 示例

1. 创建资源组 `rg1`，配额为每秒 500 RU，并定义超过 60 秒的查询为 runaway query，并降低 runaway query 的优先级。

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg1 RU_PER_SEC = 500 QUERY_LIMIT=(EXEC_ELAPSED='60s', ACTION=COOLDOWN);
    ```

2. 更改 `rg1` 资源组以终止 runaway queries，并在接下来的 10 分钟内立即将具有相同模式的查询标记为 runaway queries。

    ```sql
    ALTER RESOURCE GROUP rg1 QUERY_LIMIT=(EXEC_ELAPSED='60s', ACTION=KILL, WATCH=SIMILAR DURATION='10m');
    ```

3. 更改 `rg1` 资源组以取消 runaway query 检查。

    ```sql
    ALTER RESOURCE GROUP rg1 QUERY_LIMIT=NULL;
    ```

#### `QUERY WATCH` 参数

有关 `QUERY WATCH` 的语法概要，请参见 [`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md)。

参数如下：

- `RESOURCE GROUP` 指定资源组。此语句添加的 runaway queries 匹配特征将添加到该资源组的监视列表中。此参数可以省略。如果省略，则应用于 `default` 资源组。
- `ACTION` 的含义与 `QUERY LIMIT` 相同。此参数可以省略。如果省略，识别后的相应操作采用资源组中 `QUERY LIMIT` 配置的 `ACTION`，且操作不随 `QUERY LIMIT` 配置变化。如果资源组中没有配置 `ACTION`，则报错。
- `QueryWatchTextOption` 参数有三个选项：`SQL DIGEST`、`PLAN DIGEST` 和 `SQL TEXT`。
    - `SQL DIGEST` 与 `SIMILAR` 相同。以下参数接受字符串、用户定义变量或产生字符串结果的其他表达式。字符串长度必须为 64，与 TiDB 中的 Digest 定义相同。
    - `PLAN DIGEST` 与 `PLAN` 相同。以下参数是 Digest 字符串。
    - `SQL TEXT` 将输入 SQL 作为原始字符串匹配（`EXACT`），或根据以下参数解析并编译为 `SQL DIGEST`（`SIMILAR`）或 `PLAN DIGEST`（`PLAN`）。

- 为默认资源组的 runaway query 监视列表添加匹配特征（需要提前为默认资源组设置 `QUERY LIMIT`）。

    ```sql
    QUERY WATCH ADD ACTION KILL SQL TEXT EXACT TO 'select * from test.t2';
    ```

- 通过将 SQL 解析为 SQL Digest 为 `rg1` 资源组的 runaway query 监视列表添加匹配特征。当未指定 `ACTION` 时，使用已为 `rg1` 资源组配置的 `ACTION` 选项。

    ```sql
    QUERY WATCH ADD RESOURCE GROUP rg1 SQL TEXT SIMILAR TO 'select * from test.t2';
    ```

- 使用 `PLAN DIGEST` 为 `rg1` 资源组的 runaway query 监视列表添加匹配特征。

    ```sql
    QUERY WATCH ADD RESOURCE GROUP rg1 ACTION KILL PLAN DIGEST 'd08bc323a934c39dc41948b0a073725be3398479b6fa4f6dd1db2a9b115f7f57';
    ```

- 通过查询 `INFORMATION_SCHEMA.RUNAWAY_WATCHES` 获取监视项 ID 并删除监视项。

    ```sql
    SELECT * from information_schema.runaway_watches ORDER BY id;
    ```

    ```sql
    *************************** 1. row ***************************
                    ID: 20003
    RESOURCE_GROUP_NAME: rg2
            START_TIME: 2023-07-28 13:06:08
            END_TIME: UNLIMITED
                WATCH: Similar
            WATCH_TEXT: 5b7fd445c5756a16f910192ad449c02348656a5e9d2aa61615e6049afbc4a82e
                SOURCE: 127.0.0.1:4000
                ACTION: Kill
    1 row in set (0.00 sec)
    ```

    ```sql
    QUERY WATCH REMOVE 20003;
    ```

#### 可观测性

你可以从以下系统表和 `INFORMATION_SCHEMA` 获取有关 runaway queries 的更多信息：

+ `mysql.tidb_runaway_queries` 表包含过去 7 天内识别的所有 runaway queries 的历史记录。以下是其中一行的示例：

    ```sql
    MySQL [(none)]> SELECT * FROM mysql.tidb_runaway_queries LIMIT 1\G
    *************************** 1. row ***************************
    resource_group_name: rg1
                   time: 2023-06-16 17:40:22
             match_type: identify
                 action: kill
           original_sql: select * from sbtest.sbtest1
            plan_digest: 5b7d445c5756a16f910192ad449c02348656a5e9d2aa61615e6049afbc4a82e
            tidb_server: 127.0.0.1:4000
    ```

    在上述输出中，`match_type` 表示 runaway query 是如何被识别的。值可以是以下之一：

    - `identify` 表示它匹配 runaway query 的条件。
    - `watch` 表示它匹配监视列表中的快速识别规则。

+ `information_schema.runaway_watches` 表包含 runaway queries 快速识别规则的记录。更多信息，请参见 [`RUNAWAY_WATCHES`](/information-schema/information-schema-runaway-watches.md)。
### 管理后台任务

> **警告：**
>
> 此功能为实验特性。不建议在生产环境中使用。此功能可能会在没有预先通知的情况下进行更改或移除。如果发现 bug，你可以在 GitHub 上报告一个[问题](https://docs.pingcap.com/tidb/stable/support)。
> 
> 资源控制中的后台任务管理基于 TiKV 对 CPU/IO 利用率的资源配额动态调整。因此，它依赖于每个实例的可用资源配额。如果在单个服务器上部署多个组件或实例，必须通过 `cgroup` 为每个实例设置适当的资源配额。在像 TiUP Playground 这样的共享资源部署中很难达到预期效果。

后台任务，如数据备份和自动统计信息收集，是低优先级但消耗大量资源的任务。这些任务通常是周期性或不定期触发的。在执行过程中，它们会消耗大量资源，从而影响在线高优先级任务的性能。

从 v7.4.0 开始，TiDB 资源控制功能支持管理后台任务。当一个任务被标记为后台任务时，TiKV 会动态限制此类任务使用的资源，以避免影响其他前台任务的性能。TiKV 实时监控所有前台任务消耗的 CPU 和 IO 资源，并根据实例的总资源限制计算后台任务可以使用的资源阈值。所有后台任务在执行过程中都受此阈值限制。

#### `BACKGROUND` 参数

`TASK_TYPES`：指定需要作为后台任务管理的任务类型。使用逗号（`,`）分隔多个任务类型。

TiDB 支持以下类型的后台任务：

<CustomContent platform="tidb">

- `lightning`：使用 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 执行导入任务。支持 TiDB Lightning 的物理导入和逻辑导入模式。
- `br`：使用 [BR](/br/backup-and-restore-overview.md) 执行备份和恢复任务。不支持 PITR。
- `ddl`：控制 Reorg DDL 批量数据写回阶段的资源使用。
- `stats`：手动执行或由 TiDB 自动触发的[收集统计信息](/statistics.md#收集统计信息)任务。
- `background`：预留的任务类型。你可以使用 [`tidb_request_source_type`](/system-variables.md#tidb_request_source_type-new-in-v740) 系统变量将当前会话的任务类型指定为 `background`。

</CustomContent>

<CustomContent platform="tidb-cloud">

- `lightning`：使用 [TiDB Lightning](https://docs.pingcap.com/tidb/stable/tidb-lightning-overview) 执行导入任务。支持 TiDB Lightning 的物理导入和逻辑导入模式。
- `br`：使用 [BR](https://docs.pingcap.com/tidb/stable/backup-and-restore-overview) 执行备份和恢复任务。不支持 PITR。
- `ddl`：控制 Reorg DDL 批量数据写回阶段的资源使用。
- `stats`：手动执行或由 TiDB 自动触发的[收集统计信息](/statistics.md#收集统计信息)任务。
- `background`：预留的任务类型。你可以使用 [`tidb_request_source_type`](/system-variables.md#tidb_request_source_type-new-in-v740) 系统变量将当前会话的任务类型指定为 `background`。

</CustomContent>

默认情况下，标记为后台任务的任务类型为 `""`，后台任务管理功能被禁用。要启用后台任务管理，你需要手动修改 `default` 资源组的后台任务类型。后台任务被识别和匹配后，会自动执行资源控制。这意味着当系统资源不足时，后台任务会自动降低到最低优先级，以确保前台任务的执行。

> **注意：**
>
> 目前，所有资源组的后台任务都绑定到 `default` 资源组。你可以通过 `default` 全局管理后台任务类型。目前不支持将后台任务绑定到其他资源组。

#### 示例

1. 修改 `default` 资源组，将 `br` 和 `ddl` 标记为后台任务。

    ```sql
    ALTER RESOURCE GROUP `default` BACKGROUND=(TASK_TYPES='br,ddl');
    ```

2. 更改 `default` 资源组以将后台任务类型恢复为默认值。

    ```sql
    ALTER RESOURCE GROUP `default` BACKGROUND=NULL;
    ```

3. 更改 `default` 资源组以将后台任务类型设置为空。在这种情况下，此资源组的所有任务都不会被视为后台任务。

    ```sql
    ALTER RESOURCE GROUP `default` BACKGROUND=(TASK_TYPES="");
    ```

4. 查看 `default` 资源组的后台任务类型。

    ```sql
    SELECT * FROM information_schema.resource_groups WHERE NAME="default";
    ```

    输出如下：

    ```
    +---------+------------+----------+-----------+-------------+---------------------+
    | NAME    | RU_PER_SEC | PRIORITY | BURSTABLE | QUERY_LIMIT | BACKGROUND          |
    +---------+------------+----------+-----------+-------------+---------------------+
    | default | UNLIMITED  | MEDIUM   | YES       | NULL        | TASK_TYPES='br,ddl' |
    +---------+------------+----------+-----------+-------------+---------------------+
    ```

5. 要显式地将当前会话中的任务标记为后台类型，你可以使用 `tidb_request_source_type` 显式指定任务类型。以下是一个示例：

    ``` sql
    SET @@tidb_request_source_type="background";
    /* 添加后台任务类型 */
    ALTER RESOURCE GROUP `default` BACKGROUND=(TASK_TYPES="background");
    /* 在当前会话中执行 LOAD DATA */
    LOAD DATA INFILE "s3://resource-control/Lightning/test.customer.aaaa.csv"
    ```

## 禁用资源控制

<CustomContent platform="tidb">

1. 执行以下语句以禁用资源控制功能。

    ```sql
    SET GLOBAL tidb_enable_resource_control = 'OFF';
    ```

2. 将 TiKV 参数 [`resource-control.enabled`](/tikv-configuration-file.md#resource-control) 设置为 `false` 以禁用基于资源组的 RU 调度。

3. 将 TiFlash 配置项 [`enable_resource_control`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) 设置为 `false` 以禁用 TiFlash 资源控制。

</CustomContent>

<CustomContent platform="tidb-cloud">

1. 执行以下语句以禁用资源控制功能。

    ```sql
    SET GLOBAL tidb_enable_resource_control = 'OFF';
    ```

2. 对于 TiDB 自管理版本，你可以使用 `resource-control.enabled` 参数来控制是否基于资源组配额使用请求调度。对于 TiDB Cloud，`resource-control.enabled` 参数默认值为 `true` 且不支持动态修改。如果需要为 TiDB Cloud Dedicated 集群禁用它，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。

3. 对于 TiDB 自管理版本，你可以使用 `enable_resource_control` 配置项来控制是否启用 TiFlash 资源控制。对于 TiDB Cloud，`enable_resource_control` 参数默认值为 `true` 且不支持动态修改。如果需要为 TiDB Cloud Dedicated 集群禁用它，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。

</CustomContent>

## 查看 RU 消耗

你可以查看有关 RU 消耗的信息。

### 查看 SQL 的 RU 消耗

你可以通过以下方式查看 SQL 语句的 RU 消耗：

- 系统变量 `tidb_last_query_info`
- `EXPLAIN ANALYZE`
- 慢查询及其对应的系统表
- `statements_summary`

#### 通过查询系统变量 `tidb_last_query_info` 查看最后一次 SQL 执行消耗的 RU

TiDB 提供了系统变量 [`tidb_last_query_info`](/system-variables.md#tidb_last_query_info-new-in-v4014)。此系统变量记录了最后执行的 DML 语句的信息，包括 SQL 执行消耗的 RU。

示例：

1. 运行 `UPDATE` 语句：

    ```sql
    UPDATE sbtest.sbtest1 SET k = k + 1 WHERE id = 1;
    ```

    ```
    Query OK, 1 row affected (0.01 sec)
    Rows matched: 1  Changed: 1  Warnings: 0
    ```

2. 查询系统变量 `tidb_last_query_info` 以查看最后执行语句的信息：

    ```sql
    SELECT @@tidb_last_query_info;
    ```

    ```
    +------------------------------------------------------------------------------------------------------------------------+
    | @@tidb_last_query_info                                                                                                 |
    +------------------------------------------------------------------------------------------------------------------------+
    | {"txn_scope":"global","start_ts":446809472210829315,"for_update_ts":446809472210829315,"ru_consumption":4.34885578125} |
    +------------------------------------------------------------------------------------------------------------------------+
    1 row in set (0.01 sec)
    ```

    在结果中，`ru_consumption` 是此 SQL 语句执行消耗的 RU。

#### 通过 `EXPLAIN ANALYZE` 查看 SQL 执行过程中消耗的 RU

你可以使用 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md#ru-request-unit-consumption) 语句获取 SQL 执行过程中消耗的 RU 数量。请注意，RU 数量受缓存（例如，[协处理器缓存](/coprocessor-cache.md)）的影响。当同一个 SQL 多次执行时，每次执行消耗的 RU 数量可能不同。RU 值不代表每次执行的确切值，但可以作为估算的参考。

#### 慢查询及其对应的系统表

<CustomContent platform="tidb">

当你启用资源控制时，TiDB 的[慢查询日志](/identify-slow-queries.md)和对应的系统表 [`INFORMATION_SCHEMA.SLOW_QUERY`](/information-schema/information-schema-slow-query.md) 包含相应 SQL 的资源组、RU 消耗以及等待可用 RU 的时间。

</CustomContent>

<CustomContent platform="tidb-cloud">

当你启用资源控制时，系统表 [`INFORMATION_SCHEMA.SLOW_QUERY`](/information-schema/information-schema-slow-query.md) 包含相应 SQL 的资源组、RU 消耗以及等待可用 RU 的时间。

</CustomContent>

#### 通过 `statements_summary` 查看 RU 统计信息

TiDB 中的系统表 [`INFORMATION_SCHEMA.statements_summary`](/statement-summary-tables.md#statements_summary) 存储了 SQL 语句的规范化和聚合统计信息。你可以使用该系统表查看和分析 SQL 语句的执行性能。它还包含资源控制的统计信息，包括资源组名称、RU 消耗以及等待可用 RU 的时间。更多详情，请参见 [`statements_summary` 字段描述](/statement-summary-tables.md#statements_summary-字段描述)。

### 查看资源组的 RU 消耗

从 v7.6.0 开始，TiDB 提供系统表 [`mysql.request_unit_by_group`](/mysql-schema/mysql-schema.md#与资源控制相关的系统表) 来存储每个资源组的 RU 消耗历史记录。

示例：

```sql
SELECT * FROM request_unit_by_group LIMIT 5;
```

```
+----------------------------+----------------------------+----------------+----------+
| start_time                 | end_time                   | resource_group | total_ru |
+----------------------------+----------------------------+----------------+----------+
| 2024-01-01 00:00:00.000000 | 2024-01-02 00:00:00.000000 | default        |   334147 |
| 2024-01-01 00:00:00.000000 | 2024-01-02 00:00:00.000000 | rg1            |     4172 |
| 2024-01-01 00:00:00.000000 | 2024-01-02 00:00:00.000000 | rg2            |    34028 |
| 2024-01-02 00:00:00.000000 | 2024-01-03 00:00:00.000000 | default        |   334088 |
| 2024-01-02 00:00:00.000000 | 2024-01-03 00:00:00.000000 | rg1            |     3850 |
+----------------------------+----------------------------+----------------+----------+
5 rows in set (0.01 sec)
```

> **注意：**
>
> `mysql.request_unit_by_group` 的数据由 TiDB 调度任务在每天结束时自动导入。如果某个资源组在某一天的 RU 消耗为 0，则不会生成记录。默认情况下，此表存储最近三个月（最多 92 天）的数据。超过此期限的数据会自动清除。
## 监控指标和图表

<CustomContent platform="tidb">

TiDB 定期收集资源控制的运行时信息，并在 Grafana 的 **TiDB** > **Resource Control** 仪表板中提供指标的可视化图表。这些指标在 [TiDB 重要监控指标](/grafana-tidb-dashboard.md) 的 **Resource Control** 部分有详细说明。

TiKV 也记录了来自不同资源组的请求 QPS。更多详情，请参见 [TiKV 监控指标详解](/grafana-tikv-dashboard.md#grpc)。

你可以在 TiDB Dashboard 中查看当前 [`RESOURCE_GROUPS`](/information-schema/information-schema-resource-groups.md) 表中的资源组数据。更多详情，请参见[资源管理页面](/dashboard/dashboard-resource-manager.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 本节仅适用于 TiDB 自管理版本。目前，TiDB Cloud 不提供资源控制指标。

TiDB 定期收集资源控制的运行时信息，并在 Grafana 的 **TiDB** > **Resource Control** 仪表板中提供指标的可视化图表。

TiKV 也在 Grafana 的 **TiKV** 仪表板中记录了来自不同资源组的请求 QPS。

</CustomContent>

## 工具兼容性

资源控制功能不影响数据导入、导出和其他复制工具的常规使用。BR、TiDB Lightning 和 TiCDC 目前不支持处理与资源控制相关的 DDL 操作，它们的资源消耗也不受资源控制限制。

## 常见问题

1. 如果我不想使用资源组，是否必须禁用资源控制？

    不需要。未指定任何资源组的用户将被绑定到具有无限资源的 `default` 资源组。当所有用户都属于 `default` 资源组时，资源分配方式与禁用资源控制时相同。

2. 一个数据库用户可以绑定到多个资源组吗？

    不可以。一个数据库用户只能绑定到一个资源组。但是，在会话运行时，你可以使用 [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md) 设置当前会话使用的资源组。你还可以使用优化器提示 [`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name) 为运行的语句设置资源组。

3. 当所有资源组的总资源分配（`RU_PER_SEC`）超过系统容量时会发生什么？

    TiDB 在创建资源组时不验证容量。只要系统有足够的可用资源，TiDB 就可以满足每个资源组的资源需求。当系统资源超出限制时，TiDB 优先满足优先级更高的资源组的请求。如果无法满足所有具有相同优先级的请求，TiDB 会根据资源分配（`RU_PER_SEC`）按比例分配资源。

## 另请参见

* [CREATE RESOURCE GROUP](/sql-statements/sql-statement-create-resource-group.md)
* [ALTER RESOURCE GROUP](/sql-statements/sql-statement-alter-resource-group.md)
* [DROP RESOURCE GROUP](/sql-statements/sql-statement-drop-resource-group.md)
* [RESOURCE GROUP RFC](https://github.com/pingcap/tidb/blob/release-8.1/docs/design/2022-11-25-global-resource-control.md)
