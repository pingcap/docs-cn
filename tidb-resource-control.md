---
title: 使用资源管控 (Resource Control) 实现资源隔离
summary: 介绍如何通过资源管控能力来实现对应用资源消耗的控制和有效调度
---

# 使用资源管控 (Resource Control) 实现资源隔离

> **警告:**
>
> 资源管控是 TiDB 在 v6.6.0 中引入的实验特性，其语法或者行为表现在 GA 前可能会发生变化。

使用资源管控特性，集群管理员可以定义资源组 (Resource Group)，通过资源组限定读写的配额。将用户绑定到某个资源组后，TiDB 层会根据用户所绑定资源组设定的读写配额对用户的读写请求做流控，TiKV 层会根据读写配额映射的优先级来对请求做调度。通过流控和调度这两层控制，你可以实现应用的资源隔离，满足服务质量（QoS）要求。

资源管控特性的引入对 TiDB 具有里程碑的意义。它能够将一个分布式数据库集群划分成多个逻辑单元，即使个别单元对资源过度使用，也不会挤占其他单元所需的资源。利用该特性：

- 你可以将多个来自不同系统的中小型应用合入一个 TiDB 集群中，个别应用的负载提升，不会影响其他业务的正常运行。而在系统负载较低的时候，繁忙的应用即使超过设定的读写配额，也仍旧可以被分配到所需的系统资源，达到资源的最大化利用。
- 你可以选择将所有测试环境合入一个集群，或者将消耗较大的批量任务编入一个单独的资源组，在保证重要应用获得必要资源的同时，提升硬件利用率，降低运行成本。

此外，合理利用资源管控特性可以减少集群数量，降低运维难度及管理成本。

## 相关参数

资源管控特性引入了两个新的全局开关变量：

* TiDB: 通过全局变量 [`tidb_enable_resource_control`](/system-variables.md#tidb-tidb_enable_resource_control) 控制是否打开资源组流控。
* TiKV: 通过参数配置 [`resource_control.enabled`](/tikv-configuration-file.md#resource_control) 控制是否使用基于资源组配额的请求调度。此参数暂时不支持动态修改，修改后需要重启 TiKV 实例生效。

这两个参数的组合效果见下表：

| `resource_control.enabled`  | `tidb_enable_resource_control`= ON   | `tidb_enable_resource_control`= OFF  |
|:----------------------------|:-------------------------------------|:------------------------------------|
| `resource_control.enabled`= true  |  流控和调度（推荐组合）            | 无效配置                         |  
| `resource_control.enabled`= false |  仅流控                         |  特性被关闭                   |

## 使用方法

对于已有的资源组，你可以通过 [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md) 修改资源组的读写配额，对资源组的配额修改会立即生效。

你可以通过 [`DROP RESOURCE GROUP`](/sql-statements/sql-statement-drop-resource-group.md) 删除资源组，被删除资源组所绑定的用户会使用 `default` 资源组做资源隔离。

> **注意：**
> 
> - `CREATE USER` 或者 `ALTER USER` 对用户资源组绑定后，不会对该用户的已有会话生效，而是只对该用户新建的会话生效。
> - `default` 资源组默认不会对绑定的用户应用做配额限制，建议通过 [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md) 创建 `default` 资源组，或者通过 [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md) 修改 `default` 资源组的配额，从而实现对 `default` 资源组的配额控制。

### 前提条件

创建、修改、删除资源组，需要拥有 `SUPER` 或者 `RESOURCE_GROUP_ADMIN` 权限。

你可以通过 [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md) 在集群中创建资源组，再通过 [`CREATE USER`](/sql-statements/sql-statement-create-user.md) 或 [`ALTER USER`](/sql-statements/sql-statement-alter-user.md) 语句将用户绑定到特定的资源组。

### 第 1 步：开启资源管控特性

开启资源组流控：

```sql
SET GLOBAL tidb_enable_resource_control = 'ON';
```

将 TiKV 配置参数 `resource_control.enabled` 设为 `true`。

### 第 2 步：创建资源组，并绑定用户到资源组

Resource Group 配额采用 [RU (Resource Unit)](/tidb-RU.md) 表达。RU 是 TiDB 对 CPU、IO 等系统资源的统一抽象的单位。

下面举例说明如何创建资源组，并绑定用户到资源组。

1. 创建 `rg1` 资源组，读请求的配额是每秒 500 RU，写请求的配额是每秒 300 RU。在系统资源充足的时候，允许这个资源组的应用超额占用资源。

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg1
    RRU_PER_SEC = 500
    WRU_PER_SEC = 300
    BURSTABLE
    ;
    ```

2. 创建 `rg2` 资源组，读请求的配额是每秒 600 RU，写请求的配额是每秒 400 RU。在系统资源充足的时候，不允许这个资源组的应用超额占用资源。

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg2
    RRU_PER_SEC = 600
    WRU_PER_SEC = 400
    ;
    ```

3. 将用户 `usr1` 和 `usr2` 分别绑定到资源组 `rg1` 和 `rg2`。

    ```sql
    ALTER USER usr1 RESOURCE GROUP rg1;
    ```

    ```sql
    ALTER USER usr2 RESOURCE GROUP rg2;
    ```

完成上述创建资源组和绑定用户的操作后，用户新建立的会话对资源的占用会受到指定配额的限制。读请求会受读 RU 的配额限制，写请求会受写 RU 的配额限制。如果系统负载比较高，没有多余的容量，两个用户的资源消耗速度会严格控制不超过配额，并且，两个用户读写请求 RU 指标的消耗比例也是与指定的配额基本成正比。在系统资源充沛时，由于 `usr1` 绑定的 `rg1` 配置了 `BURSTABLE`，所以 `usr1` 消耗速度允许超过配额，而 `usr2` 则不可以。

## 监控与图表

TiDB 会定时采集资源管控的运行时信息，并在 Grafana 的 **TiDB** > **Resource Control** 面板中提供了相关指标的可视化图表。指标详情见 [TiDB 重要监控指标详解](/grafana-tidb-dashboard.md) 中的 `Resource Control` 部分。

## 工具兼容性

作为实验特性，资源管控暂时不兼容包括 BR、TiDB Lightning、TiCDC 在内的数据导入导出以及同步工具。

## 使用限制

目前，资源管控特性具有以下限制:

* 暂时只支持对前台客户发起的读写请求做限流和调度，不支持对 `DDL` 以及 `Auto Analyze` 等后台任务的限流和调度。
* 资源管控将带来额外的调度开销。因此，开启该特性后，性能可能会有轻微的下降。

## 另请参阅

* [CREATE RESOURCE GROUP](/sql-statements/sql-statement-create-resource-group.md)
* [ALTER RESOURCE GROUP](/sql-statements/sql-statement-alter-resource-group.md)
* [DROP RESOURCE GROUP](/sql-statements/sql-statement-drop-resource-group.md)
* [RESOURCE GROUP RFC](https://docs.google.com/document/d/1sV5EVv8Cdpc6aBCDihc2akpE0iuantPf/)
* [RU](/tidb-RU.md)