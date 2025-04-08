---
title: TiProxy 流量回放
summary: 介绍 TiProxy 的流量回放的使用场景和使用步骤。
---

# TiProxy 流量回放

从 TiProxy v1.3.0 开始，你可以使用 TiProxy 捕获 TiDB 生产集群中的访问流量，并在测试集群中按照指定的速率回放这些流量。通过该功能，你可以在测试环境中重现生产集群的实际工作负载，从而验证所有 SQL 的执行结果和性能表现。从 TiProxy v1.4.0 开始，该功能成为正式功能。

<img src="https://docs-download.pingcap.com/media/images/docs-cn/tiproxy/tiproxy-traffic-replay.png" alt="TiProxy 流量回放" width="800" />

## 使用场景

流量回放适用于以下场景：

- **TiDB 版本升级前验证**：在新版本的测试集群上回放生产流量，验证新版本 TiDB 能否成功执行所有 SQL 语句。
- **执行变更前影响评估**：在测试集群上使用生产流量模拟，验证变更对集群的影响。例如在变更配置项或系统变量、变更表结构、使用 TiDB 的新功能前，先在测试集群验证效果。
- **TiDB 扩缩容前性能验证**：在新规模的测试集群上按对应速率回放流量，验证新规模集群的性能是否满足要求。例如，为了节省成本要将集群规模缩容到 1/2 时，可以按 1/2 速率回放流量，验证缩容后 SQL 延迟是否满足要求。
- **性能上限测试**：在相同规模的测试集群上多次回放流量，每次调大回放速率，测试该规模下集群的吞吐量上限，以评估性能是否满足未来业务增长需求。

流量回放不适用于以下场景：

- TiDB 与 MySQL 的 SQL 兼容性验证：TiProxy 只支持读取 TiProxy 生成的流量文件，不支持从 MySQL 捕获流量后在 TiDB 上回放。
- TiDB 版本间 SQL 执行结果对比：TiProxy 只验证 SQL 语句是否执行成功，不对比运行结果。

## 使用步骤

在 TiDB v9.0.0 之前，仅支持使用 `tiproxyctl` 连接 TiProxy 进行流量捕获和回放。从 TiDB v9.0.0 开始，建议使用 SQL 捕获和回放流量。

<SimpleTab>
<div label="使用 SQL">

1. 准备测试环境：

    1. 创建测试集群，详情参考[使用 TiUP 部署 TiDB 集群](/production-deployment-using-tiup.md)。
    2. 同步生产集群的数据到测试集群，详情参考[数据迁移概述](/migration-overview.md)。
    3. 在测试集群中运行 [`ANALYZE`](/sql-statements/sql-statement-analyze-table.md) 更新统计信息。

2. 使用 [`TRAFFIC CAPTURE`](/sql-statements/sql-statement-traffic-capture.md) 语句捕获流量。

    TiProxy 支持捕获流量到本地和外部存储。捕获到本地时，需要在捕获之后把流量文件手动复制到回放的 TiProxy 集群上，而使用外部存储时不需要手动复制。TiProxy 支持的外部存储包括 Amazon S3、Google Cloud Storage (GCS)、Azure Blob Storage，或者实现 S3 协议的其他文件存储服务。关于外部存储，请参见[外部存储服务的 URI 格式](/external-storage-uri.md)。

    捕获流量需要当前用户具备 `SUPER` 或 [`TRAFFIC_CAPTURE_ADMIN`](/privilege-management.md#动态权限) 权限。

    > **注意：**
    >
    > - TiProxy 会捕获所有连接上的流量，包括已创建的和新创建的连接。
    > - TiProxy 的 CPU 使用率越高，捕获流量对 QPS 的影响越大。为减少对生产集群的影响，建议预留至少 30% 的 CPU，此时平均 QPS 下降约 3%。有关详细性能数据，请参阅[捕获流量测试](/tiproxy/tiproxy-performance-test.md#捕获流量测试)。
    > - 再次捕获流量时，上次的流量文件不会自动删除，需要手动删除。

    例如，以下语句使所有 TiProxy 实例捕获一个小时的流量，并将流量保存到 TiProxy 实例的 `/tmp/traffic` 目录下：
    
    ```sql
    TRAFFIC CAPTURE TO "/tmp/traffic" DURATION="1h"
    ```

    流量文件会自动转轮和压缩。更多选项，请参考 [`TRAFFIC CAPTURE`](/sql-statements/sql-statement-traffic-capture.md)。

3. 如果流量文件捕获到 TiProxy 本机上，需要将流量文件目录复制到测试集群的 TiProxy 实例上。

4. 使用 [`TRAFFIC REPLAY`](/sql-statements/sql-statement-traffic-replay.md) 语句回放流量。

    捕获流量需要当前用户具备 `SUPER` 或 [`TRAFFIC_REPLAY_ADMIN`](/privilege-management.md#动态权限) 权限。

    默认配置下，SQL 语句的执行速率与生产集群相同，数据库连接也与生产集群一一对应，以模拟生产集群的负载。

    例如，如下 SQL 通过用户名 `u1` 和密码 `123456` 连接到所有 TiProxy 实例，并从各实例的 `/tmp/traffic` 目录下读取流量文件并回放流量：

    ```sql
    TRAFFIC REPLAY FROM "/tmp/traffic" USER="u1" PASSWORD="123456"
    ```

    由于所有流量在用户 `u1` 下运行，请确保 `u1` 能访问所有数据库和表。如果用户不存在，则需要创建。如果生产集群有[资源组](/tidb-resource-control-ru-groups.md#管理资源组)，那么回放时 TiProxy 会自动将每个会话的资源组设置为与捕获时相同。因此，要为 `u1` 配置 [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md) 的[权限](/sql-statements/sql-statement-set-resource-group.md#权限)。

    如果回放所有语句，再次回放前可能需要恢复数据到上次回放之前，以避免数据重复引起的报错。也可以加上 `READ_ONLY=true` 选项，只回放只读语句，避免每次回放前恢复数据。

    更多信息，请参考 [`TRAFFIC REPLAY`](/sql-statements/sql-statement-traffic-replay.md)。

</div>
<div label="使用 tiproxyctl">

1. 准备测试环境：

    1. 创建测试集群，详情参考[使用 TiUP 部署 TiDB 集群](/production-deployment-using-tiup.md)。
    2. 安装 `tiproxyctl`，确保安装 `tiproxyctl` 的主机能连接到生产集群和测试集群的 TiProxy 实例。详情参考[安装 TiProxy Control](/tiproxy/tiproxy-command-line-flags.md#安装-tiproxy-control)。
    3. 同步生产集群的数据到测试集群，详情参考[数据迁移概述](/migration-overview.md)。
    4. 在测试集群中运行 [`ANALYZE`](/sql-statements/sql-statement-analyze-table.md) 更新统计信息。

2. 使用 [`tiproxyctl traffic capture`](/tiproxy/tiproxy-command-line-flags.md#traffic-capture) 命令连接到生产集群的 TiProxy 实例，开始捕获流量。

    TiProxy 支持捕获流量到本地和外部存储。捕获到本地时，需要在捕获之后把流量文件手动复制到回放的 TiProxy 集群上，而使用外部存储时不需要手动复制。TiProxy 支持的外部存储包括 Amazon S3、Google Cloud Storage (GCS)、Azure Blob Storage，或者实现 S3 协议的其他文件存储服务。关于外部存储，请参见[外部存储服务的 URI 格式](/external-storage-uri.md)。

    > **注意：**
    >
    > - TiProxy 会捕获所有连接上的流量，包括已创建的和新创建的连接。
    > - 如果 TiProxy 配置了虚拟 IP，建议连接到虚拟 IP 地址。如果有多台活跃的 TiProxy 实例，需要连接到每一台 TiProxy 实例执行。
    > - TiProxy 的 CPU 使用率越高，捕获流量对 QPS 的影响越大。为减少对生产集群的影响，建议预留至少 30% 的 CPU，此时平均 QPS 下降约 3%。有关详细性能数据，请参阅[捕获流量测试](/tiproxy/tiproxy-performance-test.md#捕获流量测试)。
    > - 再次捕获流量时，上次的流量文件不会自动删除，需要手动删除。

    例如，以下命令连接到 TiProxy 实例 `10.0.1.10:3080`，捕获一个小时的流量，并将流量保存到 TiProxy 实例的 `/tmp/traffic` 目录下：
    
    ```shell
    tiproxyctl traffic capture --host 10.0.1.10 --port 3080 --output="/tmp/traffic" --duration=1h
    ```

    流量文件会自动转轮和压缩。更多选项，请参考 [`tiproxyctl traffic capture`](/tiproxy/tiproxy-command-line-flags.md#traffic-capture)。

3. 将流量文件目录复制到测试集群的 TiProxy 实例上。
4. 使用 [`tiproxyctl traffic replay`](/tiproxy/tiproxy-command-line-flags.md#traffic-replay) 连接到测试集群的 TiProxy 实例，开始回放流量。

    默认配置下，SQL 语句的执行速率与生产集群相同，数据库连接也与生产集群一一对应，以模拟生产集群的负载。

    例如，如下命令通过用户名 `u1` 和密码 `123456` 连接到 TiProxy 实例 `10.0.1.10:3080`，从 TiProxy 实例的 `/tmp/traffic` 目录下读取流量文件并回放流量：

    ```shell
    tiproxyctl traffic replay --host 10.0.1.10 --port 3080 --username="u1" --password="123456" --input="/tmp/traffic"
    ```

    由于所有流量在用户 `u1` 下运行，请确保 `u1` 能访问所有数据库和表。如果用户不存在，则需要创建。如果生产集群有[资源组](/tidb-resource-control-ru-groups.md#管理资源组)，那么回放时 TiProxy 会自动将每个会话的资源组设置为与捕获时相同。因此，要为 `u1` 配置 [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md) 的[权限](/sql-statements/sql-statement-set-resource-group.md#权限)。

    如果回放所有语句，再次回放前可能需要恢复数据到上次回放之前，以减少报错。也可以加上 `--read-only=true` 选项，只回放只读语句，避免每次回放前恢复数据。

    更多信息，请参考 [`tiproxyctl traffic replay`](/tiproxy/tiproxy-command-line-flags.md#traffic-replay)。

</div>
</SimpleTab>

## 查看回放报告

回放完成后，报告存储在测试集群的 `tiproxy_traffic_replay` 数据库下。该数据库包含两个表 `fail` 和 `other_errors`。

`fail` 表存储运行失败的 SQL 语句，字段说明如下：

- `replay_start_time`：回放任务的开始时间，用于唯一标识一次回放任务。可用于过滤回放任务。
- `cmd_type`：运行错误的命令类型，例如 `Query`（执行普通语句）、`Prepare`（预处理语句）、`Execute`（执行预处理语句）。
- `digest`：执行失败的 SQL 语句的指纹。
- `sample_stmt`：SQL 语句首次执行失败时的 SQL 文本。
- `sample_err_msg`：SQL 语句执行失败的报错信息。
- `sample_conn_id`：SQL 语句在流量文件中记录的连接 ID，可用于在流量文件中查看 SQL 语句的执行上下文。
- `sample_capture_time`：SQL 语句在流量文件中记录的执行时间，可用于在流量文件中查看 SQL 语句的执行上下文。
- `sample_replay_time`：SQL 语句在回放时执行失败的时间，可用于在 TiDB 日志文件中查看错误信息。
- `count`：SQL 语句执行失败的次数。

以下是 `fail` 表的输出示例：

```sql
SELECT * FROM tiproxy_traffic_replay.fail LIMIT 1\G
```

```
*************************** 1. row ***************************
  replay_start_time: 2024-10-17 13:05:03
           cmd_type: StmtExecute
             digest: 89c5c505772b8b7e8d5d1eb49f4d47ed914daa2663ed24a85f762daa3cdff43c
        sample_stmt: INSERT INTO new_order (no_o_id, no_d_id, no_w_id) VALUES (?, ?, ?) params=[3077 6 1]
     sample_err_msg: ERROR 1062 (23000): Duplicate entry '1-6-3077' for key 'new_order.PRIMARY'
     sample_conn_id: 1356
sample_capture_time: 2024-10-17 12:59:15
 sample_replay_time: 2024-10-17 13:05:05
              count: 4
```

`other_errors` 表存储其他未预期错误，例如网络错误、连接数据库错误。字段说明如下：

- `replay_start_time`：回放任务的开始时间，用于唯一标识一次回放任务。可用于过滤回放任务。
- `err_type`：错误的类型，是一个简短的错误信息，例如 `i/o timeout`。
- `sample_err_msg`：错误首次出现时的完整错误信息。
- `sample_replay_time`：错误在回放时执行失败的时间，可用于在 TiDB 日志文件中查看错误信息。
- `count`：错误出现的次数。

以下是 `other_errors` 表的输出示例：

```sql
SELECT * FROM tiproxy_traffic_replay.other_errors LIMIT 1\G
```

```
*************************** 1. row ***************************
 replay_start_time: 2024-10-17 12:57:35
          err_type: failed to read the connection: EOF
    sample_err_msg: this is an error from the backend connection: failed to read the connection: EOF
sample_replay_time: 2024-10-17 12:57:39
             count: 1
```

> **注意：**
>
> - `tiproxy_traffic_replay` 中的表结构在未来版本中可能会改变。不推荐在应用程序开发或工具开发中读取 `tiproxy_traffic_replay` 中的数据。
> - 回放不保证连接之间的事务执行顺序与捕获时完全一致，因此可能会误报错误。

## 测试吞吐量

<SimpleTab>
<div label="使用 SQL">

如果需要测试集群的吞吐量，可以使用 `SPEED` 选项调整回放的速率。

例如，`SPEED=2` 会使 SQL 语句以两倍速率执行，总回放时间缩短一半：

```sql
TRAFFIC REPLAY FROM "/tmp/traffic" USER="u1" PASSWORD="123456" SPEED=2
```

</div>
<div label="使用 tiproxyctl">

如果需要测试集群的吞吐量，可以使用 `--speed` 选项调整回放的速率。

例如，`--speed=2` 会使 SQL 语句以两倍速率执行，总回放时间缩短一半：

```shell
tiproxyctl traffic replay --host 10.0.1.10 --port 3080 --username="u1" --password="123456" --input="/tmp/traffic" --speed=2
```

</div>
</SimpleTab>

调大回放速率只会缩短 SQL 语句之间的空闲时间，不会增加连接数。因此当会话的空闲时间本身较短时，仅调大倍速可能无法有效提升吞吐量。在这种情况下，可以部署多个 TiProxy 实例，让它们同时回放相同的流量文件，通过增加并发度来提高吞吐量。

## 任务查看与管理

<SimpleTab>
<div label="使用 SQL">

在捕获和回放过程中，如果遇到未知错误会自动停止任务。使用 [`SHOW TRAFFIC JOBS`](/sql-statements/sql-statement-show-traffic-jobs.md) 可查看当前的任务进度或上次任务的错误信息：

```sql
SHOW TRAFFIC JOBS
```

当前用户拥有的权限不同，执行该语句显示结果也不同。

- 如果用户有 [`TRAFFIC_CAPTURE_ADMIN`](/privilege-management.md#动态权限) 权限，执行该语句显示流量捕获任务。
- 如果用户有 [`TRAFFIC_REPLAY_ADMIN`](/privilege-management.md#动态权限) 权限，执行该语句显示流量回放任务。
- 如果用户有 `SUPER` 权限或同时具有上述两种权限，执行该语句同时显示流量捕获和流量回放任务。

例如，如下输出代表有 2 台 TiProxy 正在捕获流量：

```
+----------------------------+----------+----------------+---------+----------+---------+-------------+----------------------------------------------------------------------------+
| START_TIME                 | END_TIME | INSTANCE       | TYPE    | PROGRESS | STATUS  | FAIL_REASON | PARAMS                                                                     |
+----------------------------+----------+----------------+---------+----------+---------+-------------+----------------------------------------------------------------------------+
| 2024-12-17 10:54:41.000000 |          | 10.1.0.10:3080 | capture | 45%      | running |             | OUTPUT="/tmp/traffic", DURATION="90m", COMPRESS=true, ENCRYPTION_METHOD="" |
| 2024-12-17 10:54:41.000000 |          | 10.1.0.11:3080 | capture | 45%      | running |             | OUTPUT="/tmp/traffic", DURATION="90m", COMPRESS=true, ENCRYPTION_METHOD="" |
+----------------------------+----------+----------------+---------+----------+---------+-------------+----------------------------------------------------------------------------+
2 rows in set (0.01 sec)
```

更多信息，请参考 [`SHOW TRAFFIC JOBS`](/sql-statements/sql-statement-show-traffic-jobs.md)。

如果需要取消当前的捕获或回放任务，可使用 [`CANCEL TRAFFIC JOBS`](/sql-statements/sql-statement-cancel-traffic-jobs.md)：

```sql
CANCEL TRAFFIC JOBS
```

取消捕获任务需要 `SUPER` 或 [`TRAFFIC_CAPTURE_ADMIN`](/privilege-management.md#动态权限) 权限，取消回放任务需要 `SUPER` 或 [`TRAFFIC_REPLAY_ADMIN`](/privilege-management.md#动态权限) 权限。

更多信息，请参考 [`CANCEL TRAFFIC JOBS`](/sql-statements/sql-statement-cancel-traffic-jobs.md)。

</div>
<div label="使用 tiproxyctl">

在捕获和回放过程中，如果遇到未知错误会自动停止任务。使用 [`tiproxyctl traffic show`](/tiproxy/tiproxy-command-line-flags.md#traffic-show) 命令可查看当前的任务进度或上次任务的错误信息：

```shell
tiproxyctl traffic show --host 10.0.1.10 --port 3080
```

例如，如下输出代表捕获任务正在运行：

```json
[
   {
      "type": "capture",
      "status": "running",
      "start_time": "2024-09-03T09:10:58.220644+08:00",
      "progress": "45%",
      "output": "/tmp/traffic",
      "duration": "2h"
   }
]
```

更多信息，请参考 [`tiproxyctl traffic show`](/tiproxy/tiproxy-command-line-flags.md#traffic-show)。

如果需要取消当前的捕获或回放任务，可使用 [`tiproxyctl traffic cancel`](/tiproxy/tiproxy-command-line-flags.md#traffic-cancel) 命令：

```shell
tiproxyctl traffic cancel --host 10.0.1.10 --port 3080
```

更多信息，请参考 [`tiproxyctl traffic cancel`](/tiproxy/tiproxy-command-line-flags.md#traffic-cancel)。

</div>
</SimpleTab>

## 使用限制

- TiProxy 仅支持回放 TiProxy 捕获的流量文件，不支持其他文件格式，因此生产集群必须先使用 TiProxy 捕获流量。
- 不支持回放 [`LOAD DATA`](/sql-statements/sql-statement-load-data.md) 语句。
- 为安全原因，以下语句不会被捕获和回放：

    - `CREATE USER` 语句
    - `ALTER USER` 语句
    - `SET PASSWORD` 语句
    - `GRANT` 语句
    - `BACKUP` 语句
    - `RESTORE` 语句
    - `IMPORT` 语句

## 资源

关于 TiProxy 流量回放更详细的信息，请参阅[设计文档](https://github.com/pingcap/tiproxy/blob/main/docs/design/2024-08-27-traffic-replay.md)。