---
title: 使用资源管控 (Resource Control) 实现资源隔离
summary: 介绍如何通过资源管控能力来实现对应用资源消耗的控制和有效调度。
---

# 使用资源管控 (Resource Control) 实现资源隔离

> **警告：**
>
> 资源管控是 TiDB 在 v6.6.0 中引入的实验特性，其语法或者行为表现在 GA 前可能会发生变化。

使用资源管控特性，集群管理员可以定义资源组 (Resource Group)，通过资源组限定读写的配额。将用户绑定到某个资源组后，TiDB 层会根据用户所绑定资源组设定的读写配额对用户的读写请求做流控，TiKV 层会根据读写配额映射的优先级来对请求做调度。通过流控和调度这两层控制，你可以实现应用的资源隔离，满足服务质量 (QoS) 要求。

TiDB 资源管控特性提供了两层资源管理能力，包括在 TiDB 层的流控能力和 TiKV 层的优先级调度的能力。两个能力可以单独或者同时开启，详情请参见[参数组合效果表](#相关参数)。

- TiDB 流控：TiDB 流控使用[令牌桶算法](https://en.wikipedia.org/wiki/Token_bucket) 做流控；如果桶内令牌数不够，而且资源组没有指定 `BURSTABLE` 特性，属于该资源组的请求会等待令牌桶回填令牌并重试，重试可能会超时失败。
- TiKV 调度：如果开启该特性，TiKV 使用基于资源组 `RU_PER_SEC` 的取值映射成各自资源组读写请求的优先级，基于各自的优先级在存储层使用优先级队列调度处理请求。

## 使用场景

资源管控特性的引入对 TiDB 具有里程碑的意义。它能够将一个分布式数据库集群划分成多个逻辑单元，即使个别单元对资源过度使用，也不会挤占其他单元所需的资源。利用该特性：

- 你可以将多个来自不同系统的中小型应用合入一个 TiDB 集群中，个别应用的负载升高，不会影响其他业务的正常运行。而在系统负载较低的时候，繁忙的应用即使超过设定的读写配额，也仍然可以被分配到所需的系统资源，达到资源的最大化利用。
- 你可以选择将所有测试环境合入一个集群，或者将消耗较大的批量任务编入一个单独的资源组，在保证重要应用获得必要资源的同时，提升硬件利用率，降低运行成本。

此外，合理利用资源管控特性可以减少集群数量，降低运维难度及管理成本。

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

* TiDB: 通过配置全局变量 [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-从-v660-版本开始引入) 控制是否打开资源组流控。
* TiKV: 通过配置参数 [`resource-control.enabled`](/tikv-configuration-file.md#resource-control) 控制是否使用基于资源组配额的请求调度。

这两个参数的组合效果见下表：

| `resource-control.enabled`  | `tidb_enable_resource_control`= ON | `tidb_enable_resource_control`= OFF  |
|:----------------------------|:-----------------------------------|:------------------------------------|
| `resource-control.enabled`= true  | 流控和调度（推荐组合）                        | 无效配置                         |
| `resource-control.enabled`= false | 仅流控（不推荐）                           |  特性被关闭                   |

关于资源管控实现机制及相关参数的详细介绍，请参考 [RFC: Global Resource Control in TiDB](https://github.com/pingcap/tidb/blob/master/docs/design/2022-11-25-global-resource-control.md)。

## 使用方法

创建、修改、删除资源组，需要拥有 `SUPER` 或者 `RESOURCE_GROUP_ADMIN` 权限。

你可以通过 [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md) 在集群中创建资源组，再通过 [`CREATE USER`](/sql-statements/sql-statement-create-user.md) 或 [`ALTER USER`](/sql-statements/sql-statement-alter-user.md) 语句将用户绑定到特定的资源组。

对于已有的资源组，可以通过 [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md) 修改资源组的读写配额，对资源组的配额修改会立即生效。

可以通过 [`DROP RESOURCE GROUP`](/sql-statements/sql-statement-drop-resource-group.md) 删除资源组。

> **注意：**
>
> - `CREATE USER` 或者 `ALTER USER` 对用户资源组绑定后，不会对该用户的已有会话生效，而是只对该用户新建的会话生效。
> - 如果用户没有绑定到某个资源组或者是绑定到 `default` 资源组，该用户的请求不会受 TiDB 的流控限制。`default` 资源组目前对用户不可见也不可以创建或者修改属性，不能通过 `SHOW CREATE RESOURCE GROUP` 或 `SELECT * FROM information_schema.resource_groups` 查看，但是可以通过 `mysql.user` 表查看。

### 第 1 步：开启资源管控特性

1. 执行以下命令开启资源管控特性：

    ```sql
    SET GLOBAL tidb_enable_resource_control = 'ON';
    ```

2. 将 TiKV 参数 [`resource-control.enabled`](/tikv-configuration-file.md#resource-control) 设为 `true`。

### 第 2 步：创建资源组，并绑定用户到资源组

下面举例说明如何创建资源组，并绑定用户到资源组。

1. 创建 `rg1` 资源组，RU 的回填速度是每秒 500 RU，并且允许这个资源组的应用超额占用资源。

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg1 RU_PER_SEC = 500 BURSTABLE;
    ```

2. 创建 `rg2` 资源组，RU 的回填速度是每秒 600 RU。在系统资源充足的时候，不允许这个资源组的应用超额占用资源。

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg2 RU_PER_SEC = 600;
    ```

3. 将用户 `usr1` 和 `usr2` 分别绑定到资源组 `rg1` 和 `rg2`。

    ```sql
    ALTER USER usr1 RESOURCE GROUP rg1;
    ```

    ```sql
    ALTER USER usr2 RESOURCE GROUP rg2;
    ```

完成上述创建资源组和绑定用户的操作后，用户新建立的会话对资源的占用会受到指定用量 (RU) 的限制。如果系统负载比较高，没有多余的容量，`usr2` 用户的资源消耗速度会严格控制不超过指定用量，由于 `usr1` 绑定的 `rg1` 配置了 `BURSTABLE`，所以 `usr1` 消耗速度允许超过指定用量。

如果资源组对应的请求太多导致资源组的资源不足，客户端的请求处理会发生等待。如果等待时间过长，请求会报错。

## 监控与图表

TiDB 会定时采集资源管控的运行时信息，并在 Grafana 的 **Resource Control Dashboard** 中提供了相关指标的可视化图表。指标详情参见 [Resource Control 监控指标详解](/grafana-resource-control-dashboard.md) 。

TiKV 中也记录了来自于不同资源组的请求 QPS，详见 [TiKV监控指标详解](/grafana-tikv-dashboard.md#grpc)

## 工具兼容性

资源管控目前为实验特性，不影响数据导入导出以及其他同步工具的正常使用，BR、TiDB Lightning、TiCDC 等工具不支持对资源管控相关 DDL 的处理，这些工具的资源消耗也不受资源管控的限制。

## 使用限制

目前，资源管控特性具有以下限制:

* 暂时只支持对前台客户发起的读写请求做限流和调度，不支持对 DDL 以及 Auto Analyze 等后台任务的限流和调度。
* 资源管控将带来额外的调度开销。因此，开启该特性后，性能可能会有轻微下降。

## 另请参阅

* [CREATE RESOURCE GROUP](/sql-statements/sql-statement-create-resource-group.md)
* [ALTER RESOURCE GROUP](/sql-statements/sql-statement-alter-resource-group.md)
* [DROP RESOURCE GROUP](/sql-statements/sql-statement-drop-resource-group.md)
* [RESOURCE GROUP RFC](https://github.com/pingcap/tidb/blob/master/docs/design/2022-11-25-global-resource-control.md)
