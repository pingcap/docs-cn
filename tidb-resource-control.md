---
title: 使用 Resource Control 实现资源隔离
summary: 介绍如何通过 Resource Control 来实现应用资源消耗的控制和有效调度
---

# 使用 Resource Control 实现资源隔离

Resource control 特性允许集群管理员通过定义资源组(Resource Group)，资源组可以限定读写的配额；将用户绑定到某个资源组，TiDB 层会根据用户所绑定资源组设定的读写配额对用户的读写请求做流控；同时，TiKV 层会使用读写配额映射的优先级来对请求做调度。通过流控加上调度两层控制，你可以实现应用的资源隔离，满足服务质量（QoS）要求。

Resource control 特别适用于在大集群内部实现多用户应用的资源隔离。

> **警告:**
>
> Resource Control 是 TiDB 在 v6.6.0 中引入的实验特性，其语法或者行为表现在 GA 前可能会发生变化。如果你知晓潜在的风险，可通过执行 TiDB SQL 语句`SET GLOBAL tidb_enable_resource_control = 'ON'`， 同时设置 TiKV 配置参数 `tidb_enable_resource_control` 为 'true' 来开启该实验特性。

## 新参数

Resource control 特性引入了2个控制参数。 在 TiDB 层有全局变量 `tidb_enable_resource_control` 控制是否打开资源组流控, TiKV 层有配置参数 `resource_control.enabled` 控制是否使用基于资源组配额的请求调度。`resource_control.enabled` 参数暂时不支持动态修改，修改后需要重启 TiKV 实例生效。
这2个参数的组合效果见下表：

+-----------------------------------+--------------------------------------+--------------------------------------+
|                                   | `tidb_enable_resource_control`= ON   | `tidb_enable_resource_control`= OFF  |
+-----------------------------------+--------------------------------------+--------------------------------------+
| `resource_control.enabled`= true  |          流控和调度（推荐组合）          |               无效配置                ｜
+-----------------------------------+--------------------------------------+--------------------------------------+
| `resource_control.enabled`= false |                 仅流控                |               特性被关闭              ｜
+-----------------------------------+-----------------------------------------------------------------------------+

## 语法

你可以通过[`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md)在集群中创建资源组，再通过[`CREATE USER`](/sql-statements/sql-statement-create-user.md) 语句，或者 [`ALTER USER`](/sql-statements/sql-statement-alter-user.md) 将用户绑定到特定的资源组。

> **注意:**
> 
> `CREATE USER` 或者 `ALTER USER` 对用户资源组绑定后，不会对该用户的已有会话生效，而是只对该用户新建的会话生效。

对于已有的资源组，你可以通过[`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md)修改资源组的读写配额，对资源组的配额修改会立即生效；你可以通过[`DROP RESOURCE GROUP`](/sql-statements/sql-statement-drop-resource-group.md)删除资源组，被删除资源组所绑定的用户会使用`default`资源组做资源隔离。

> **推荐做法：**
> 
> `default`资源组默认是不会对绑定的用户应用做配额限制，我们建议你通过[`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md)创建`default`资源组，从而实现对`default`资源组的配额控制。

### 开启特性

- 开启 Resource Control 特性

    ```sql
    SET GLOBAL tidb_enable_resource_control = 'ON';
    ```
    将 TiKV 配置参数 `resource_control.enabled` 设为 'true'
### 创建资源组，并绑定用户到资源组

>**注意：**
> `Resource Group` 配额采用[`RU` (Resource Unit)](/tidb-RU.md) 表达， `RU` 是 TiDB 对 CPU, IO 等系统资源的统一抽象的单位。

- 创建 `rg1` 资源组

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg1 (
    RRU_PER_SEC = 500
    RRU_PER_SEC = 300
    BURSTABLE
    );
    ```

上面的例子创建了 `rg1` 资源组，读请求的配额是每秒500 `RU`，写请求的配额是每秒300 `RU`，在系统资源充足的时候，允许这个资源组的应用超额占用资源；

```sql
CREATE RESOURCE GROUP IF NOT EXISTS rg2 (
RRU_PER_SEC = 600
RRU_PER_SEC = 400
);
```

上面的例子创建了 `rg2` 资源组，读请求的配额是每秒600 `RU`，写请求的配额是每秒400 `RU`，，在系统资源充足的时候，不允许这个资源组的应用超额占用资源；

- 绑定用户到资源组

    ```sql
    ALTER USER usr1 RESOURCE GROUP rg1;
    ```

    ```sql
    ALTER USER usr2 RESOURCE GROUP rg2;
    ```

    上面的例子将用户 `usr1` 和 `usr2` 分别绑定到资源组 `rg1` 和 `rg2`。

- 效果

  完成上述创建资源组和绑定用户的操作后，用户新建立的会话对资源的占用会受到指定配额的限制。读请求会受读RU的配额限制，写请求会受写RU的配额限制。如果系统负载比较高，没有富余的容量，两个用户的资源消耗速度会严格控制不超过配额，并且，两个用户读写请求RU指标的消耗比例也是与指定的配额基本成正比；在系统资源充沛时，`usr1` 的资源消耗速度允许超过配额。

## 监控与图表

* 新增加内存表 `information_schema.resource_groups` 可以查看集群中定义的资源组
* TiDB 会定时采集 Resource Control 的运行时信息，并在 Grafana 中提供了相关指标的可视化图表。你可以在 TiDB -> Resource Control 的面板下看到这些信息。指标详情见 [TiDB 重要监控指标详解](/grafana-tidb-dashboard.md) 中的 `Resource Control` 部分。

## 工具兼容性

作为实验特性，Resource Control 暂时不兼容包括 BR、TiDB Lightning、TiCDC 在内的数据导入导出以及同步工具。

## 使用限制

目前，Resource Control 特性具有以下限制:

* 暂时只支持前台客户发起的前台读写请求做限流和调度，不支持 `DDL`, 以及 `Auto Analyze` 等后台任务。
* 因为额外调度的开销，开启这个特性后，性能可能会观察到有轻微的回退。

## 另请参阅

* [CREATE RESOURCE GROUP](/sql-statements/sql-statement-create-resource-group.md)
* [ALTER RESOURCE GROUP](/sql-statements/sql-statement-alter-resource-group.md)
* [DROP RESOURCE GROUP](/sql-statements/sql-statement-drop-resource-group.md)
* [RESOURCE GROUP RFC](https://docs.google.com/document/d/1sV5EVv8Cdpc6aBCDihc2akpE0iuantPf/)
* [RU](/tidb-RU.md)