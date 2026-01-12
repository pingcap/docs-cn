---
title: 管理资源消耗超出预期的查询 (Runaway Queries)
summary: 介绍如何通过资源管控能力来实现对资源消耗超出预期的语句 (Runaway Queries) 进行控制和降级。
---

# 管理资源消耗超出预期的查询 (Runaway Queries)

Runaway Query 是指执行时间或消耗资源超出预期的语句。下面使用 **Runaway Queries** 表示管理 Runaway Query 这一功能。

- 自 v7.2.0 起，TiDB 资源管控引入了对 Runaway Queries 的管理。你可以针对某个资源组设置条件来识别 Runaway Queries，并自动发起应对操作，防止集群资源完全被 Runaway Queries 占用而影响其他正常查询。你可以在 [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md) 或者 [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md) 中配置 `QUERY_LIMIT` 字段，通过规则识别来管理资源组的 Runaway Queries。
- 自 v7.3.0 起，TiDB 资源管控引入了手动管理 Runaway Queries 监控列表的功能，将给定的 SQL 或者 Digest 添加到隔离监控列表，从而实现快速隔离 Runaway Queries。你可以执行语句 [`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md)，手动管理资源组中的 Runaway Queries 监控列表。

更多关于资源管控的信息，请参考[使用资源管控 (Resource Control) 实现资源组限制和流控](/tidb-resource-control-ru-groups.md#相关参数)。

## `QUERY_LIMIT` 参数说明

如果查询超过以下任一限制，就会被识别为 Runaway Query：

- `EXEC_ELAPSED`：检测查询执行的时间是否超限, 该规则适用于读写 DML。
- `PROCESSED_KEYS`：检测 Coprocessor 处理的 key 的数量是否超限，该规则只适用于查询语句。
- `RU`：检测执行语句消耗的总读写 RU 是否超限，该规则只适用于查询语句。

支持的应对操作 (`ACTION`)：

- `DRYRUN`：对执行 Query 不做任何操作，仅记录识别的 Runaway Query。主要用于观测设置条件是否合理。
- `COOLDOWN`：将查询的执行优先级降到最低，查询仍旧会以低优先级继续执行，不占用其他操作的资源。
- `KILL`：识别到的查询将被自动终止，报错 `Query execution was interrupted, identified as runaway query`。
- `SWITCH_GROUP`：从 v8.4.0 开始引入，将识别到的查询切换到指定的资源组继续执行。该查询执行结束后，后续 SQL 仍保持在原资源组中执行。如果指定的资源组不存在，则不做任何动作。

为了避免并发的 Runaway Query 过多导致系统资源耗尽，资源管控引入了 Runaway Query 监控机制，能够快速识别并隔离 Runaway Query。该功能通过 `WATCH` 子句实现，当某一个查询被识别为 Runaway Query 之后，会提取这个查询的匹配特征（由 `WATCH` 后的匹配方式参数决定），在接下来的一段时间里（由 `DURATION` 定义），这个 Runaway Query 的匹配特征会被加入到监控列表，TiDB 实例会将查询和监控列表进行匹配，匹配到的查询直接标记为 Runaway Query，而不再等待其被条件识别，并按照当前应对操作进行隔离。其中 `KILL` 会终止该查询，并报错 `Quarantined and interrupted because of being in runaway watch list`。

`WATCH` 有三种匹配方式：

- `EXACT` 表示完全相同的 SQL 才会被快速识别
- `SIMILAR` 表示会忽略字面值 (Literal)，通过 SQL Digest 匹配所有模式 (Pattern) 相同的 SQL
- `PLAN` 表示通过 Plan Digest 匹配所有模式 (Pattern) 相同的 SQL

`WATCH` 中的 `DURATION` 选项，用于表示此识别项的持续时间，默认为无限长。

添加监控项后，匹配特征和 `ACTION` 都不会随着 `QUERY_LIMIT` 配置的修改或删除而改变或删除。

可以使用 `QUERY WATCH REMOVE` 来删除监控项，或者使用 `QUERY WATCH REMOVE RESOURCE GROUP`（从 v9.0.0 开始引入）批量删除指定资源组的所有监控项。

`QUERY_LIMIT` 具体格式如下：

| 参数            | 含义           | 备注                                   |
|---------------|--------------|--------------------------------------|
| `EXEC_ELAPSED`  | 当查询执行时间超过该值时，会被识别为 Runaway Query | `EXEC_ELAPSED = 60s` 表示查询的执行时间超过 60 秒则被认为是 Runaway Query。 |
| `PROCESSED_KEYS` | 当 Coprocessor 处理的 key 的数量超过该值时，查询会被识别为 Runaway Query | `PROCESSED_KEYS = 1000` 表示 Coprocessor 处理的 key 的数量超过 1000 则被认为是 Runaway Query。 |
| `RU`  | 当查询消耗的总读写 RU 超过该值时，查询会被识别为 Runaway Query | `RU = 1000` 表示查询消耗的总读写 RU 超过 1000 则被认为是 Runaway Query。 |
| `ACTION`    | 当识别到 Runaway Query 时进行的动作 | 可选值有 `DRYRUN`，`COOLDOWN`，`KILL`，`SWITCH_GROUP`。 |
| `WATCH`   | 快速匹配已经识别到的 Runaway Query，即在一定时间内再碰到相同或相似查询直接进行相应动作 | 可选项，配置例如 `WATCH=SIMILAR DURATION '60s'`、`WATCH=EXACT DURATION '1m'`、`WATCH=PLAN`。 |

> **注意：**
>
> 如果你想把 Runaway Queries 严格限制在一个资源组内，推荐将 `SWITCH_GROUP` 和 [`QUERY WATCH`](#query-watch-语句说明) 语句一起搭配使用。因为 `QUERY_LIMIT` 只有在查询达到预设条件时才会触发，所以 `SWITCH_GROUP` 在此类场景下可能会出现无法及时将查询切换到目标资源组的情况。

## 示例

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

## `QUERY WATCH` 语句说明

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

- 通过将 SQL 解析成 SQL Digest，为 `rg1` 资源组的 Runaway Queries 监控列表添加监控匹配特征，并指定 `ACTION` 为 `SWITCH_GROUP(rg2)`。

    ```sql
    QUERY WATCH ADD RESOURCE GROUP rg1 ACTION SWITCH_GROUP(rg2) SQL TEXT SIMILAR TO 'select * from test.t2';
    ```

- 通过 PLAN Digest 为 `rg1` 资源组的 Runaway Queries 监控列表添加监控匹配特征，并指定 `ACTION` 为 `KILL`。

    ```sql
    QUERY WATCH ADD RESOURCE GROUP rg1 ACTION KILL PLAN DIGEST 'd08bc323a934c39dc41948b0a073725be3398479b6fa4f6dd1db2a9b115f7f57';
    ```

- 通过查询 `INFORMATION_SCHEMA.RUNAWAY_WATCHES` 获取监控项 ID，删除该监控项。

    ```sql
    SELECT * FROM INFORMATION_SCHEMA.RUNAWAY_WATCHES ORDER BY id\G
    ```

    ```sql
    *************************** 1. row ***************************
                     ID: 1
    RESOURCE_GROUP_NAME: default
             START_TIME: 2024-09-09 03:35:31
               END_TIME: 2024-09-09 03:45:31
                  WATCH: Exact
            WATCH_TEXT: SELECT variable_name, variable_value FROM mysql.global_variables
                 SOURCE: 127.0.0.1:4000
                ACTION: Kill
                RULE: ProcessedKeys = 666(10)
    1 row in set (0.00 sec)
    ```

    ```sql
    QUERY WATCH REMOVE 1;
    ```

- <span class="version-mark">从 v9.0.0 开始引入</span> 批量删除指定资源组的所有监控项：

    ```sql
    QUERY WATCH REMOVE RESOURCE GROUP rg1;
    ```

## 可观测性

可以通过以下系统表和 `INFORMATION_SCHEMA` 表获得 Runaway 相关的更多信息：

+ `mysql.tidb_runaway_queries` 表中包含了过去 7 天内所有识别到的 Runaway Queries 的历史记录。以其中一行为例：

    ```sql
    MySQL [(none)]> SELECT * FROM mysql.tidb_runaway_queries LIMIT 1\G
    *************************** 1. row ***************************
    resource_group_name: default
         start_time: 2024-09-09 17:43:42
            repeats: 2
         match_type: watch
             action: kill
         sample_sql: select sleep(2) from t
         sql_digest: 4adbc838b86c573265d4b39a3979d0a362b5f0336c91c26930c83ab187701a55
        plan_digest: 5d094f78efbce44b2923733b74e1d09233cb446318293492901c5e5d92e27dbc
        tidb_server: 127.0.0.1:4000
    ```

    字段解释：

    - `start_time` 为该 Runaway Query 被识别的时间。
    - `repeats` 为该 Runaway Query 从 `start_time` 开始后被识别的次数。
    - `match_type` 为该 Runaway Query 的来源，其值如下：
        - `identify` 表示命中条件。
        - `watch` 表示被快速识别机制命中。

+ `information_schema.runaway_watches` 表中包含了 Runaway Queries 的快速识别规则记录。详见 [`RUNAWAY_WATCHES`](/information-schema/information-schema-runaway-watches.md)。