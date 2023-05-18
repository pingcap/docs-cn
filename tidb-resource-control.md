---
title: 使用资源管控 (Resource Control) 实现资源隔离
summary: 介绍如何通过资源管控能力来实现对应用资源消耗的控制和有效调度。
---

# 使用资源管控 (Resource Control) 实现资源隔离

使用资源管控特性，集群管理员可以定义资源组 (Resource Group)，通过资源组限定读写的配额。

TiDB 资源管控特性提供了两层资源管理能力，包括在 TiDB 层的流控能力和 TiKV 层的优先级调度的能力。两个能力可以单独或者同时开启，详情请参见[参数组合效果表](#相关参数)。将用户绑定到某个资源组后，TiDB 层会根据用户所绑定资源组设定的读写配额对用户的读写请求做流控，TiKV 层会根据读写配额映射的优先级来对请求做调度。通过流控和调度这两层控制，可以实现应用的资源隔离，满足服务质量 (QoS) 要求。

- TiDB 流控：TiDB 流控使用[令牌桶算法](https://en.wikipedia.org/wiki/Token_bucket) 做流控。如果桶内令牌数不够，而且资源组没有指定 `BURSTABLE` 特性，属于该资源组的请求会等待令牌桶回填令牌并重试，重试可能会超时失败。
- TiKV 调度：你可以为资源组设置绝对优先级 ([`PRIORITY`](/information-schema/information-schema-resource-groups.md#示例))，不同的资源按照 `PRIORITY` 的设置进行调度，`PRIORITY` 高的任务会被优先调度。如果没有设置绝对优先级 (`PRIORITY`)，TiKV 会将资源组的 `RU_PER_SEC` 取值映射成各自资源组读写请求的优先级，并基于各自的优先级在存储层使用优先级队列调度处理请求。

## 使用场景

资源管控特性的引入对 TiDB 具有里程碑的意义。它能够将一个分布式数据库集群划分成多个逻辑单元，即使个别单元对资源过度使用，也不会挤占其他单元所需的资源。利用该特性：

- 你可以将多个来自不同系统的中小型应用合入一个 TiDB 集群中，个别应用的负载升高，不会影响其他业务的正常运行。而在系统负载较低的时候，繁忙的应用即使超过设定的读写配额，也仍然可以被分配到所需的系统资源，达到资源的最大化利用。
- 你可以选择将所有测试环境合入一个集群，或者将消耗较大的批量任务编入一个单独的资源组，在保证重要应用获得必要资源的同时，提升硬件利用率，降低运行成本。
- 当系统中存在多种业务负载时，可以将不同的负载分别放入各自的资源组。利用资源管控技术，确保交易类业务的响应时间不受数据分析或批量业务的影响。
- 当集群遇到突发的 SQL 性能问题，可以结合 SQL Binding 和资源组，临时限制某个 SQL 的资源消耗。

此外，合理利用资源管控特性可以减少集群数量，降低运维难度及管理成本。

## 使用限制

目前，资源管控特性具有以下限制:

- 只支持对前台客户发起的读写请求做限流和调度，不支持对 DDL 以及 Auto Analyze 等后台任务的限流和调度。
- 资源管控将带来额外的调度开销。因此，开启该特性后，性能可能会有轻微下降。

## 什么是 Request Unit (RU)

Request Unit (RU) 是 TiDB 对 CPU、IO 等系统资源的统一抽象的单位, 目前包括 CPU、IOPS 和 IO 带宽三个指标。这三个指标的消耗会按照一定的比例统一到 RU 单位上。

下表是用户请求对 TiKV 存储层 CPU 和 IO 资源的消耗以及对应的 RU 权重：

| 资源       | RU 权重        |
|:-----------|:-------------|
| CPU        | 1/3 RU / 毫秒  |
| 读 IO      | 1/64 RU / KB |
| 写 IO      | 1 RU / KB    |
| 一次读请求的基本开销 | 0.25 RU      |
| 一次写请求的基本开销 | 1.5 RU       |

基于上表，假设某个资源组消耗的 TiKV 时间是 `c` 毫秒，`r1` 次请求读取了 `r2` KB 数据，`w1` 次写请求写入了 `w2` KB 数据，集群中非 witness TiKV 节点数是 `n`，则该资源组消耗的总 RU 的公式如下：

`c`\* 1/3 + (`r1` \* 0.25 + `r2` \* 1/64) + (`w1` \* 1.5  + `w2` \* 1 \* `n`)

## 相关参数

资源管控特性引入了两个新的全局开关变量：

- TiDB：通过配置全局变量 [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-从-v660-版本开始引入) 控制是否打开资源组流控。
- TiKV：通过配置参数 [`resource-control.enabled`](/tikv-configuration-file.md#resource-control) 控制是否使用基于资源组配额的请求调度。

从 v7.0.0 开始，两个开关都被默认打开。这两个参数的组合效果见下表：

| `resource-control.enabled`  | `tidb_enable_resource_control`= ON | `tidb_enable_resource_control`= OFF  |
|:----------------------------|:-----------------------------------|:------------------------------------|
| `resource-control.enabled`= true  | 流控和调度（推荐组合）                        | 无效配置                         |
| `resource-control.enabled`= false | 仅流控（不推荐）                           |  特性被关闭                   |

关于资源管控实现机制及相关参数的详细介绍，请参考 [RFC: Global Resource Control in TiDB](https://github.com/pingcap/tidb/blob/master/docs/design/2022-11-25-global-resource-control.md)。

## 使用方法

下面介绍如何使用资源管控特性。

### 预估集群容量

在进行资源规划之前，你需要了解集群的整体容量。TiDB 提供了命令 [`CALIBRATE RESOURCE`](/sql-statements/sql-statement-calibrate-resource.md) 用来估算集群容量。目前提供两种估算方式：

- [根据实际负载估算容量](/sql-statements/sql-statement-calibrate-resource.md#根据实际负载估算容量)
- [基于硬件部署估算容量](/sql-statements/sql-statement-calibrate-resource.md#基于硬件部署估算容量)

详情请参考 [`CALIBRATE RESOURCE` 预估方式](/sql-statements/sql-statement-calibrate-resource.md#预估方式)。

### 管理资源组

创建、修改、删除资源组，需要拥有 `SUPER` 或者 `RESOURCE_GROUP_ADMIN` 权限。

你可以通过 [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md) 在集群中创建资源组。

对于已有的资源组，可以通过 [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md) 修改资源组的读写配额，对资源组的配额修改会立即生效。

可以使用 [`DROP RESOURCE GROUP`](/sql-statements/sql-statement-drop-resource-group.md) 删除资源组。

### 创建资源组

下面举例说明如何创建资源组。

1. 创建 `rg1` 资源组，限额是每秒 500 RU，并且允许这个资源组的应用超额占用资源。

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg1 RU_PER_SEC = 500 BURSTABLE;
    ```

2. 创建 `rg2` 资源组，RU 的回填速度是每秒 600 RU。在系统资源充足的时候，不允许这个资源组的应用超额占用资源。

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg2 RU_PER_SEC = 600;
    ```

3. 创建 `rg3` 资源组，设置绝对优先级为 `HIGH`。绝对优先级目前支持 `LOW|MEDIUM|HIGH`，资源组的默认绝对优先级为 `MEDIUM`。

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg3 RU_PER_SEC = 100 PRIORITY = HIGH;
    ```

### 绑定资源组

TiDB 支持如下三个级别的资源组设置：

- 用户级别。通过 [`CREATE USER`](/sql-statements/sql-statement-create-user.md) 或 [`ALTER USER`](/sql-statements/sql-statement-alter-user.md#修改用户绑定的资源组) 语句将用户绑定到特定的资源组。绑定后，对应的用户新创建的会话会自动绑定对应的资源组。
- 会话级别。通过 [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md) 设置当前会话使用的资源组。
- 语句级别。通过 [`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name) Optimizer Hint 设置当前语句使用的资源组。

#### 将用户绑定到资源组

下面的示例创建一个用户 `usr1` 并将其绑定到资源组 `rg1`。其中 `rg1` 为[创建资源组](#创建资源组)示例中创建的资源组。

```sql
CREATE USER 'usr1'@'%' IDENTIFIED BY '123' RESOURCE GROUP rg1;
```

下面示例使用 `ALTER USER` 将用户 `usr2` 绑定到资源组 `rg2`。其中 `rg2` 为[创建资源组](#创建资源组)示例中创建的资源组。

```sql
ALTER USER usr2 RESOURCE GROUP rg2;
```

绑定用户后，用户新建立的会话对资源的占用会受到指定用量 (RU) 的限制。如果系统负载比较高，没有多余的容量，用户 `usr2` 的资源消耗速度会被严格控制不超过指定用量。由于 `usr1` 绑定的 `rg1` 配置了 `BURSTABLE`，所以 `usr1` 消耗速度允许超过指定用量。

如果资源组对应的请求太多导致资源组的资源不足，客户端的请求处理会发生等待。如果等待时间过长，请求会报错。

> **注意：**
>
> - 使用 `CREATE USER` 或者 `ALTER USER` 将用户绑定到资源组后，只会对该用户新建的会话生效，不会对该用户已有的会话生效。
> - TiDB 集群在初始化时会自动创建 `default` 资源组，其 `RU_PER_SEC` 的默认值为 `UNLIMITED` (等同于 `INT` 类型最大值，即 `2147483647`)，且为 `BURSTABLE` 模式。对于没有绑定资源组的语句会自动绑定至此资源组。此资源组不支持删除，但允许修改其 RU 的配置。

#### 将当前会话绑定到资源组

通过把当前会话绑定到资源组，会话对资源的占用会受到指定用量 (RU) 的限制。

下面的示例将当前的会话绑定至资源组 `rg1`。

```sql
SET RESOURCE GROUP rg1;
```

#### 将语句绑定到资源组

通过在 SQL 语句中添加 [`RESOURCE_GROUP(resource_group_name)`](/optimizer-hints.md#resource_groupresource_group_name) Hint，可以将该语句绑定到指定的资源组。此 Hint 支持 `SELECT`、`INSERT`、`UPDATE`、`DELETE` 四种语句。

示例：

```sql
SELECT /*+ RESOURCE_GROUP(rg1) */ * FROM t limit 10;
```

## 关闭资源管控特性

1. 执行以下命令关闭资源管控特性：

    ```sql
    SET GLOBAL tidb_enable_resource_control = 'OFF';
    ```

2. 将 TiKV 参数 [`resource-control.enabled`](/tikv-configuration-file.md#resource-control) 设为 `false`，关闭按照资源组配额调度。

## 监控与图表

TiDB 会定时采集资源管控的运行时信息，并在 Grafana 的 **Resource Control Dashboard** 中提供了相关指标的可视化图表。指标详情参见 [Resource Control 监控指标详解](/grafana-resource-control-dashboard.md) 。

TiKV 中也记录了来自于不同资源组的请求 QPS，详见 [TiKV监控指标详解](/grafana-tikv-dashboard.md#grpc)

## 工具兼容性

资源管控不影响数据导入导出以及其他同步工具的正常使用，BR、TiDB Lightning、TiCDC 等工具不支持对资源管控相关 DDL 的处理，这些工具的资源消耗也不受资源管控的限制。

## 常见问题

1. 如果我暂时不想使用资源组对资源进行管控，是否一定要关闭这个特性？ 

    不需要。没有指定任何资源组的用户，将被放入系统预定义的 `default` 资源组，而 `default` 资源组默认拥有无限用量。当所有用户都属于 `default` 资源组时，资源分配方式与关闭资源管控时相同。

2. 一个数据库用户是否可以绑定到不同的资源组？

    不能。一个数据库用户只能绑定到一个资源组。但是，在会话运行的过程中，可以通过 [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md) 设置当前会话使用的资源组。你也可以通过优化器 [`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name) Hint 为运行的语句设置资源组。

3. 当各个资源组设置的用量 (`RU_PER_SEC`) 总和超出系统容量会发生什么？

    TiDB 在创建资源组时不会检查容量。只要系统有足够的空闲资源，TiDB 就会满足每个资源组的用量设置。当系统资源超过限制时，TiDB 会优先满足高优先级 (PRIORITY) 资源组的请求。如果同一优先级的请求无法全部满足，TiDB 会根据用量 (`RU_PER_SEC`) 的大小按比例分配。

## 另请参阅

* [CREATE RESOURCE GROUP](/sql-statements/sql-statement-create-resource-group.md)
* [ALTER RESOURCE GROUP](/sql-statements/sql-statement-alter-resource-group.md)
* [DROP RESOURCE GROUP](/sql-statements/sql-statement-drop-resource-group.md)
* [RESOURCE GROUP RFC](https://github.com/pingcap/tidb/blob/master/docs/design/2022-11-25-global-resource-control.md)
