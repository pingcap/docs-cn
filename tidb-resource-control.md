---
title: 使用资源管控 (Resource Control) 实现资源隔离
summary: 介绍如何通过资源管控能力来实现对应用资源消耗的控制和有效调度。
---

# 使用资源管控 (Resource Control) 实现资源隔离

使用资源管控特性，集群管理员可以定义资源组 (Resource Group)，通过资源组限定配额。

TiDB 资源管控特性提供了两层资源管理能力，包括在 TiDB 层的流控能力和 TiKV 层的优先级调度的能力。两个能力可以单独或者同时开启，详情请参见[参数组合效果表](#相关参数)。将用户绑定到某个资源组后，TiDB 层会根据用户所绑定资源组设定的配额对用户的读写请求做流控，TiKV 层会根据配额映射的优先级来对请求做调度。通过流控和调度这两层控制，可以实现应用的资源隔离，满足服务质量 (QoS) 要求。

- TiDB 流控：TiDB 流控使用[令牌桶算法](https://en.wikipedia.org/wiki/Token_bucket) 做流控。如果桶内令牌数不够，而且资源组没有指定 `BURSTABLE` 特性，属于该资源组的请求会等待令牌桶回填令牌并重试，重试可能会超时失败。
- TiKV 调度：你可以为资源组设置绝对优先级 ([`PRIORITY`](/information-schema/information-schema-resource-groups.md#示例))，不同的资源按照 `PRIORITY` 的设置进行调度，`PRIORITY` 高的任务会被优先调度。如果没有设置绝对优先级 (`PRIORITY`)，TiKV 会将资源组的 `RU_PER_SEC` 取值映射成各自资源组读写请求的优先级，并基于各自的优先级在存储层使用优先级队列调度处理请求。

从 v7.4.0 开始，TiDB 资源管控特性支持管控 TiFlash 资源，其原理与 TiDB 流控和 TiKV 调度类似：

- TiFlash 流控：借助 [TiFlash Pipeline Model 执行模型](/tiflash/tiflash-pipeline-model.md)，可以更精确地获取不同查询的 CPU 消耗情况，并转换为 [Request Unit (RU)](#什么是-request-unit-ru) 进行扣除。流量控制通过令牌桶算法实现。
- TiFlash 调度：当系统资源不足时，会根据优先级对多个资源组之间的 pipeline task 进行调度。具体逻辑是：首先判断资源组的优先级 `PRIORITY`，然后根据 CPU 使用情况，再结合 `RU_PER_SEC` 进行判断。最终效果是，如果 rg1 和 rg2 的 `PRIORITY` 一样，但是 rg2 的 `RU_PER_SEC` 是 rg1 的两倍，那么 rg2 可使用的 CPU 时间是 rg1 的两倍。

## 使用场景

资源管控特性的引入对 TiDB 具有里程碑的意义。它能够将一个分布式数据库集群划分成多个逻辑单元，即使个别单元对资源过度使用，也不会挤占其他单元所需的资源。利用该特性：

- 你可以将多个来自不同系统的中小型应用合入一个 TiDB 集群中，个别应用的负载升高，不会影响其他业务的正常运行。而在系统负载较低的时候，繁忙的应用即使超过设定的读写配额，也仍然可以被分配到所需的系统资源，达到资源的最大化利用。
- 你可以选择将所有测试环境合入一个集群，或者将消耗较大的批量任务编入一个单独的资源组，在保证重要应用获得必要资源的同时，提升硬件利用率，降低运行成本。
- 当系统中存在多种业务负载时，可以将不同的负载分别放入各自的资源组。利用资源管控技术，确保交易类业务的响应时间不受数据分析或批量业务的影响。
- 当集群遇到突发的 SQL 性能问题，可以结合 SQL Binding 和资源组，临时限制某个 SQL 的资源消耗。

此外，合理利用资源管控特性可以减少集群数量，降低运维难度及管理成本。

> **注意：**
>
> 推荐在部署资源相对独立的计算和存储节点上测试资源管控的效果，因为调度等对集群资源敏感的功能通常很难在单节点运行的 TiUP Playground 上表现出良好性能。

## 使用限制

资源管控将带来额外的调度开销。因此，开启该特性后，性能可能会有轻微下降（低于 5%）。

## 什么是 Request Unit (RU)

Request Unit (RU) 是 TiDB 对 CPU、IO 等系统资源的统一抽象的计量单位，用于表示对数据库的单个请求消耗的资源量。请求消耗的 RU 数量取决于多种因素，例如操作类型或正在检索或修改的数据量。目前，RU 包含以下资源的统计信息：

<table>
    <thead>
        <tr>
            <th>资源类型</th>
            <th>RU 消耗</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan="3">Read</td>
            <td>2 storage read batches 消耗 1 RU</td>
        </tr>
        <tr>
            <td>8 storage read requests 消耗 1 RU</td>
        </tr>
        <tr>
            <td>64 KiB read request payload 消耗 1 RU</td>
        </tr>
        <tr>
            <td rowspan="3">Write</td>
            <td>1 storage write batch 消耗 1 RU</td>
        </tr>
        <tr>
            <td>1 storage write request 消耗 1 RU</td>
        </tr>
        <tr>
            <td>1 KiB write request payload 消耗 1 RU</td>
        </tr>
        <tr>
            <td>CPU</td>
            <td> 3 ms 消耗 1 RU</td>
        </tr>
    </tbody>
</table>

> **注意：**
>
> - 每个写操作最终都被会复制到所有副本（TiKV 默认 3 个数据副本），并且每次复制都被认为是一个不同的写操作。
> - 上表只列举了本地部署的 TiDB 计算 RU 时涉及的相关资源，其中不包括网络和存储部分。TiDB Serverless 的 RU 可参考 [TiDB Serverless Pricing Details](https://www.pingcap.com/tidb-cloud-serverless-pricing-details/)。
> - 目前 TiFlash 资源管控仅考虑 SQL CPU（即查询的 pipeline task 运行所占用的 CPU 时间）以及 read request payload。

## 相关参数

资源管控特性引入了如下系统变量或参数：

- TiDB：通过配置全局变量 [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-从-v660-版本开始引入) 控制是否打开资源组流控。
- TiKV：通过配置参数 [`resource-control.enabled`](/tikv-configuration-file.md#resource-control) 控制是否使用基于资源组配额的请求调度。
- TiFlash：通过配置全局变量 [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-从-v660-版本开始引入) 和 TiFlash 配置项 [`enable_resource_control`](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml)（v7.4.0 开始引入）控制是否开启 TiFlash 资源管控。

从 v7.0.0 开始，`tidb_enable_resource_control` 和 `resource-control.enabled` 开关都被默认打开。这两个参数的组合效果见下表：

| `resource-control.enabled`  | `tidb_enable_resource_control`= ON | `tidb_enable_resource_control`= OFF  |
|:----------------------------|:-----------------------------------|:------------------------------------|
| `resource-control.enabled`= true  | 流控和调度（推荐组合）                        | 无效配置                         |
| `resource-control.enabled`= false | 仅流控（不推荐）                           |  特性被关闭                   |

从 v7.4.0 开始，TiFlash 配置项 `enable_resource_control` 默认打开，与 `tidb_enable_resource_control` 一起控制 TiFlash 资源管控功能。只有二者都启用时，TiFlash 资源管控功能才能进行流控以及优先级调度。同时，在开启 `enable_resource_control` 时，TiFlash 会使用 [Pipeline Model 执行模型](/tiflash/tiflash-pipeline-model.md)。

关于资源管控实现机制及相关参数的详细介绍，请参考 [RFC: Global Resource Control in TiDB](https://github.com/pingcap/tidb/blob/master/docs/design/2022-11-25-global-resource-control.md) 以及 [TiFlash Resource Control](https://github.com/pingcap/tiflash/blob/master/docs/design/2023-09-21-tiflash-resource-control.md)。

## 使用方法

下面介绍如何使用资源管控特性。

### 预估集群容量

在进行资源规划之前，你需要了解集群的整体容量。TiDB 提供了命令 [`CALIBRATE RESOURCE`](/sql-statements/sql-statement-calibrate-resource.md) 用来估算集群容量。目前提供两种估算方式：

- [根据实际负载估算容量](/sql-statements/sql-statement-calibrate-resource.md#根据实际负载估算容量)
- [基于硬件部署估算容量](/sql-statements/sql-statement-calibrate-resource.md#基于硬件部署估算容量)

可通过 [TiDB Dashboard 资源管控页面](/dashboard/dashboard-resource-manager.md)进行查看。详情请参考 [`CALIBRATE RESOURCE` 预估方式](/sql-statements/sql-statement-calibrate-resource.md#预估方式)。

### 管理资源组

创建、修改、删除资源组，需要拥有 `SUPER` 或者 `RESOURCE_GROUP_ADMIN` 权限。

你可以通过 [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md) 在集群中创建资源组。

对于已有的资源组，可以通过 [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md) 修改资源组的配额，对资源组的配额修改会立即生效。

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

要解除用户与资源组的绑定，只需将其重新绑定到 `default` 资源组即可，如下所示：

```sql
ALTER USER 'usr3'@'%' RESOURCE GROUP `default`;
```

更多信息，请参见 [`ALTER USER ... RESOURCE GROUP`](/sql-statements/sql-statement-alter-user.md#修改用户绑定的资源组)。

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

### 管理资源消耗超出预期的查询 (Runaway Queries)

> **警告：**
>
> 该功能目前为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

Runaway Query 是指执行时间或消耗资源超出预期的查询（仅指 `SELECT` 语句）。下面使用 **Runaway Queries** 表示管理 Runaway Query 这一功能。

- 自 v7.2.0 起，TiDB 资源管控引入了对 Runaway Queries 的管理。你可以针对某个资源组设置条件来识别 Runaway Queries，并自动发起应对操作，防止集群资源完全被 Runaway Queries 占用而影响其他正常查询。你可以在 [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md) 或者 [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md) 中配置 `QUERY_LIMIT` 字段，通过规则识别来管理资源组的 Runaway Queries。
- 自 v7.3.0 起，TiDB 资源管控引入了手动管理 Runaway Queries 监控列表的功能，将给定的 SQL 或者 Digest 添加到隔离监控列表，从而实现快速隔离 Runaway Queries。你可以执行语句 [`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md)，手动管理资源组中的 Runaway Queries 监控列表。

#### `QUERY_LIMIT` 参数说明

支持的条件设置：

- `EXEC_ELAPSED`: 当查询执行的时间超限时，识别为 Runaway Query。

支持的应对操作 (`ACTION`)：

- `DRYRUN`：对执行 Query 不做任何操作，仅记录识别的 Runaway Query。主要用于观测设置条件是否合理。
- `COOLDOWN`：将查询的执行优先级降到最低，查询仍旧会以低优先级继续执行，不占用其他操作的资源。
- `KILL`：识别到的查询将被自动终止，报错 `Query execution was interrupted, identified as runaway query`。

为了避免并发的 Runaway Query 过多导致系统资源耗尽，资源管控引入了 Runaway Query 监控机制，能够快速识别并隔离 Runaway Query。该功能通过 `WATCH` 子句实现，当某一个查询被识别为 Runaway Query 之后，会提取这个查询的匹配特征（由 `WATCH` 后的匹配方式参数决定），在接下来的一段时间里（由 `DURATION` 定义），这个 Runaway Query 的匹配特征会被加入到监控列表，TiDB 实例会将查询和监控列表进行匹配，匹配到的查询直接标记为 Runaway Query，而不再等待其被条件识别，并按照当前应对操作进行隔离。其中 `KILL` 会终止该查询，并报错 `Quarantined and interrupted because of being in runaway watch list`。

`WATCH` 有三种匹配方式：

- `EXACT` 表示完全相同的 SQL 才会被快速识别
- `SIMILAR` 表示会忽略字面值 (Literal)，通过 SQL Digest 匹配所有模式 (Pattern) 相同的 SQL
- `PLAN` 表示通过 Plan Digest 匹配所有模式 (Pattern) 相同的 SQL

`WATCH` 中的 `DURATION` 选项，用于表示此识别项的持续时间，默认为无限长。

添加监控项后，匹配特征和 `ACTION` 都不会随着 `QUERY_LIMIT` 配置的修改或删除而改变或删除。可以使用 `QUERY WATCH REMOVE` 来删除监控项。

`QUERY_LIMIT` 具体格式如下：

| 参数            | 含义           | 备注                                   |
|---------------|--------------|--------------------------------------|
| `EXEC_ELAPSED`  | 当查询执行时间超过该值后被识别为 Runaway Query | EXEC_ELAPSED =`60s` 表示查询的执行时间超过 60 秒则被认为是 Runaway Query。 |
| `ACTION`    | 当识别到 Runaway Query 时进行的动作 | 可选值有 `DRYRUN`，`COOLDOWN`，`KILL`。 |
| `WATCH`   | 快速匹配已经识别到的 Runaway Query，即在一定时间内再碰到相同或相似查询直接进行相应动作 | 可选项，配置例如 `WATCH=SIMILAR DURATION '60s'`、`WATCH=EXACT DURATION '1m'`、`WATCH=PLAN`。 |

#### 示例

1. 创建 `rg1` 资源组，限额是每秒 500 RU，并且定义超过 60 秒为 Runaway Query，并对 Runaway Query 降低优先级执行。

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg1 RU_PER_SEC = 500 QUERY_LIMIT=(EXEC_ELAPSED='60s', ACTION=COOLDOWN);
    ```

2. 修改 `rg1` 资源组，对 Runaway Query 直接终止，并且在接下来的 10 分钟里，把相同模式的查询直接标记为 Runaway Query。

    ```sql
    ALTER RESOURCE GROUP rg1 QUERY_LIMIT=(EXEC_ELAPSED='60s', ACTION=KILL, WATCH=SIMILAR DURATION='10m');
    ```

3. 修改 `rg1` 资源组，取消 Runaway Queries 检查。

    ```sql
    ALTER RESOURCE GROUP rg1 QUERY_LIMIT=NULL;
    ```

#### `QUERY WATCH` 语句说明

语法详见 [`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md)。

参数说明如下：

- `RESOURCE GROUP` 用于指定资源组。此语句添加的 Runaway Queries 监控特征将添加到该资源组的监控列表中。此参数可以省略，省略时作用于 `default` 资源组。
- `ACTION` 的含义与 `QUERY LIMIT` 相同。此参数可以省略，省略时表示识别后的对应操作采用此时资源组中 `QUERY LIMIT` 配置的 `ACTION`，且不会随着 `QUERY LIMIT` 配置的改变而改变。如果资源组没有配置 `ACTION`，会报错。
- `QueryWatchTextOption` 参数有 `SQL DIGEST`、`PLAN DIGEST`、`SQL TEXT` 三种类型。
    - `SQL DIGEST` 的含义与 `QUERY LIMIT` `WATCH` 类型中的 `SIMILAR` 相同，后面紧跟的参数可以是字符串、用户自定义变量以及其他计算结果为字符串的表达式。字符串长度必须为 64，与 TiDB 中关于 Digest 的定义一致。
    - `PLAN DIGEST` 的含义与 `PLAN` 相同。输入参数为 Digest 字符串。
    - `SQL TEXT` 可以根据后面紧跟的参数，将输入的 SQL 的原始字符串（使用 `EXACT` 选项）作为模式匹配项，或者经过解析和编译转化为 `SQL DIGEST`（使用 `SIMILAR` 选项）、`PLAN DIGEST`（使用 `PLAN` 选项）来作为模式匹配项。

- 为默认资源组的 Runaway Queries 监控列表添加监控匹配特征（需要提前为默认资源组设置 `QUERY LIMIT`）。

    ```sql
    QUERY WATCH ADD ACTION KILL SQL TEXT EXACT TO 'select * from test.t2';
    ```

- 通过将 SQL 解析成 SQL Digest，为 `rg1` 资源组的 Runaway Queries 监控列表添加监控匹配特征。未指定 `ACTION` 时，使用 `rg1` 资源组已配置的 `ACTION`。

    ```sql
    QUERY WATCH ADD RESOURCE GROUP rg1 SQL TEXT SIMILAR TO 'select * from test.t2';
    ```

- 通过 PLAN Digest 为 `rg1` 资源组的 Runaway Queries 监控列表添加监控匹配特征。

    ```sql
    QUERY WATCH ADD RESOURCE GROUP rg1 ACTION KILL PLAN DIGEST 'd08bc323a934c39dc41948b0a073725be3398479b6fa4f6dd1db2a9b115f7f57';
    ```

- 通过查询 `INFORMATION_SCHEMA.RUNAWAY_WATCHES` 获取监控项 ID，删除该监控项。

    ```sql
    SELECT * FROM INFORMATION_SCHEMA.RUNAWAY_WATCHES ORDER BY id;
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

可以通过以下系统表和 `INFORMATION_SCHEMA` 表获得 Runaway 相关的更多信息：

+ `mysql.tidb_runaway_queries` 表中包含了过去 7 天内所有识别到的 Runaway Queries 的历史记录。以其中一行为例：

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

    其中，`match_type` 为该 Runaway Query 的来源，其值如下：

    - `identify` 表示命中条件。
    - `watch` 表示被快速识别机制命中。

+ `information_schema.runaway_watches` 表中包含了 Runaway Queries 的快速识别规则记录。详见 [`RUNAWAY_WATCHES`](/information-schema/information-schema-runaway-watches.md)。

### 管理后台任务

> **警告：**
>
> 该功能目前为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。如果发现 bug，请[提交 issue](/support.md) 反馈。
> 
> 资源管控的后台任务管理是基于 TiKV 的 CPU/IO 的资源利用率动态调整资源配额的，因此它依赖各个实例可用资源上限 (Quota)。如果在单个服务器混合部署多个组件或实例，需要通过 cgroup 为各个实例设置合适的资源上限 (Quota)。TiUP Playground 这类共享资源的配置很难表现出预期效果。

后台任务是指那些优先级不高但是需要消耗大量资源的任务，如数据备份和自动统计信息收集等。这些任务通常定期或不定期触发，在执行的时候会消耗大量资源，从而影响在线的高优先级任务的性能。

自 v7.4.0 开始，TiDB 资源管控引入了对后台任务的管理。当一种任务被标记为后台任务时，TiKV 会动态地限制该任务的资源使用，以尽量避免此类任务在执行时对其他前台任务的性能产生影响。TiKV 通过实时地监测所有前台任务所消耗的 CPU 和 IO 等资源，并根据实例总的资源上限计算出后台任务可使用的资源阈值，所有后台任务在执行时会受此阈值的限制。

#### `BACKGROUND` 参数说明

`TASK_TYPES`：设置需要作为后台任务管理的任务类型，多个任务类型以 `,` 分隔。

目前 TiDB 支持如下几种后台任务的类型：

- `lightning`：使用 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 执行导入任务。同时支持 TiDB Lightning 的物理和逻辑导入模式。
- `br`：使用 [BR](/br/backup-and-restore-overview.md) 执行数据备份和恢复。目前不支持 PITR。
- `ddl`：对于 Reorg DDL，控制批量数据回写阶段的资源使用。
- `stats`：对应手动执行或系统自动触发的[收集统计信息](/statistics.md#统计信息的收集)任务。
- `background`：预留的任务类型，可使用 [`tidb_request_source_type`](/system-variables.md#tidb_request_source_type-从-v740-版本开始引入) 系统变量指定当前会话的任务类型为 `background`。

默认情况下，被标记为后台任务的任务类型为 `""`，此时后台任务的管理功能处于关闭状态。如需开启后台任务管理功能，你需要手动修改 `default` 资源组的后台任务类型以开启后台任务管理。后台任务类型被识别匹配后，资源管控会自动进行，即当系统资源紧张时，后台任务会自动降为最低优先级，保证前台任务的执行。

> **注意：**
>
> 目前，所有资源组的后台任务默认都会绑定到默认资源组 `default` 下进行管控，你可以通过 `default` 全局管控后台任务类型。暂不支持将后台任务绑定到其他资源组。

#### 示例

1. 修改 `default` 资源组，将 `br` 和 `ddl` 标记为后台任务。

    ```sql
    ALTER RESOURCE GROUP `default` BACKGROUND=(TASK_TYPES='br,ddl');
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
    +---------+------------+----------+-----------+-------------+---------------------+
    | NAME    | RU_PER_SEC | PRIORITY | BURSTABLE | QUERY_LIMIT | BACKGROUND          |
    +---------+------------+----------+-----------+-------------+---------------------+
    | default | UNLIMITED  | MEDIUM   | YES       | NULL        | TASK_TYPES='br,ddl' |
    +---------+------------+----------+-----------+-------------+---------------------+
    ```

5. 如果希望将当前会话里的任务显式标记为后台类型，你可以使用 `tidb_request_source_type` 显式指定任务类型，如：

    ``` sql
    SET @@tidb_request_source_type="background";
    /* 添加 background 任务类型 */
    ALTER RESOURCE GROUP `default` BACKGROUND=(TASK_TYPES="background");
    /* 在当前会话中执行 LOAD DATA */
    LOAD DATA INFILE "s3://resource-control/Lightning/test.customer.aaaa.csv"
    ```

## 关闭资源管控特性

1. 执行以下命令关闭资源管控特性：

    ```sql
    SET GLOBAL tidb_enable_resource_control = 'OFF';
    ```

2. 将 TiKV 参数 [`resource-control.enabled`](/tikv-configuration-file.md#resource-control) 设为 `false`，关闭按照资源组配额调度。

3. 将 TiFlash 参数 [`enable_resource_control`](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml) 设为 `false`，关闭 TiFlash 资源管控。

## 查看 RU 消耗

你可以查看 RU 消耗的相关信息。

### 查看 SQL 的 RU 消耗

你可以通过以下方式查询 SQL 消耗的 RU：

- 系统变量 `tidb_last_query_info`
- `EXPLAIN ANALYZE`
- 慢查询及对应的系统表
- `statements_summary`

#### 使用系统变量 `tidb_last_query_info` 查询执行上一条 SQL 语句的 RU 消耗

TiDB 提供系统变量 [`tidb_last_query_info`](/system-variables.md#tidb_last_query_info-从-v4014-版本开始引入)，记录上一条 DML 语句执行的信息，其中包含 SQL 执行消耗的 RU。

使用示例：

1. 执行 `UPDATE` 语句：

    ```sql
    UPDATE sbtest.sbtest1 SET k = k + 1 WHERE id = 1;
    ```

    ```
    Query OK, 1 row affected (0.01 sec)
    Rows matched: 1  Changed: 1  Warnings: 0
    ```

2. 通过查询系统变量 `tidb_last_query_info`，查看上条执行的语句的相关信息：

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

    返回结果中的 `ru_consumption` 即为执行此 SQL 语句消耗的 RU。

#### 使用 `EXPLAIN ANALYZE` 查询 SQL 执行时所消耗的 RU

你也可以通过 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md#ru-request-unit-消耗) 语句获取到 SQL 执行时所消耗的 RU。注意 RU 的大小会受缓存的影响（比如[下推计算结果缓存](/coprocessor-cache.md)），多次执行同一条 SQL 所消耗的 RU 可能会有不同。因此这个 RU 值并不代表每次执行的精确值，但可以作为估算的参考。

#### 慢查询及对应的系统表

在开启资源管控时，TiDB 的[慢查询日志](/identify-slow-queries.md)以及对应系统表 [`INFORMATION_SCHEMA.SLOW_QUERY`](/information-schema/information-schema-slow-query.md) 中均包含对应 SQL 所属的资源组、等待可用 RU 的耗时、以及真实 RU 消耗等相关信息。

#### 通过 `statements_summary` 查询 RU 相关的统计信息

TiDB 的系统表 [`INFORMATION_SCHEMA.statements_summary`](/statement-summary-tables.md#statements_summary) 中保存了 SQL 语句归一化聚合后的各种统计信息，可以用于查看分析各个 SQL 语句的执行性能。其中也包含资源管控相关的统计信息，包括资源组名、RU 消耗、等待可用 RU 的耗时等信息。具体请参考[`statements_summary` 字段介绍](/statement-summary-tables.md#statements_summary-字段介绍)。

### 查看资源组的 RU 消耗

从 v7.6.0 版本开始，TiDB 提供系统表 [`mysql.request_unit_by_group`](/mysql-schema.md#资源管控相关系统表) 存放各个资源组每日消耗的 RU 的历史记录。

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
> `mysql.request_unit_by_group` 的数据由 TiDB 的定时任务在每天结束后自动导入。如果某个资源组当天的 RU 消耗为 0，则不会产生一条记录。此表默认只存放最近 3 个月（最多 92 天）的数据。超过此期限的数据会自动被清理。

## 监控与图表

TiDB 会定时采集资源管控的运行时信息，并在 Grafana 的 **Resource Control Dashboard** 中提供了相关指标的可视化图表，详见 [Resource Control 监控指标详解](/grafana-resource-control-dashboard.md)。

TiKV 中也记录了来自于不同资源组的请求 QPS，详见 [TiKV 监控指标详解](/grafana-tikv-dashboard.md#grpc)。

TiDB Dashboard 中可以查看当前 [`RESOURCE_GROUPS`](/information-schema/information-schema-resource-groups.md) 表中资源组的数据。详见 [TiDB Dashboard 资源管控页面](/dashboard/dashboard-resource-manager.md)。

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
