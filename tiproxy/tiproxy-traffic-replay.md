---
title: TiProxy 流量回放
summary: 介绍 TiProxy 的流量回放的使用场景和使用步骤。
---

# TiProxy 流量回放

> **警告：**
>
> TiProxy 流量回放目前为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tiproxy/issues) 反馈。

从 TiProxy v1.3.0 开始，你可以使用 TiProxy 捕获 TiDB 生产集群中的访问流量，并在测试集群中按照指定的速率回放这些流量。通过该功能，你可以在测试环境中重现生产集群的实际工作负载，从而验证所有 SQL 的执行结果和性能表现。

<img src="https://download.pingcap.com/images/docs-cn/tiproxy/tiproxy-traffic-replay.png" alt="TiProxy 流量回放" width="800" />

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

1. 准备测试环境：

    1. 创建测试集群，详情参考[使用 TiUP 部署 TiDB 集群](/production-deployment-using-tiup.md)。
    2. 安装 `tiproxyctl`，确保安装 `tiproxyctl` 的主机能连接到生产集群和测试集群的 TiProxy 实例。详情参考[安装 TiProxy Control](/tiproxy/tiproxy-command-line-flags.md#安装-tiproxy-control)。
    3. 同步生产集群的数据到测试集群，详情参考[数据迁移概述](/migration-overview.md)。
    4. 在测试集群中运行 [`ANALYZE`](/sql-statements/sql-statement-analyze-table.md) 更新统计信息。

2. 使用 [`tiproxyctl traffic capture`](/tiproxy/tiproxy-command-line-flags.md#traffic-capture) 命令连接到生产集群的 TiProxy 实例，开始捕获流量。

    > **注意：**
    >
    > - TiProxy 会捕获所有连接上的流量，包括已创建的和新创建的连接。
    > - 在 TiProxy 主备模式下，请确保连接到 TiProxy 主实例。
    > - 如果 TiProxy 配置了虚拟 IP，建议连接到虚拟 IP 地址。
    > - TiProxy 的 CPU 使用率越高，捕获流量对 QPS 的影响越大。为减少对生产集群的影响，建议预留至少 30% 的 CPU，此时平均 QPS 下降约 3%。有关详细性能数据，请参阅[捕获流量测试](/tiproxy/tiproxy-performance-test.md#捕获流量测试)。
    > - 再次捕获流量时，上次的流量文件不会自动删除，需要手动删除。

    例如，以下命令连接到 TiProxy 实例 `10.0.1.10:3080`，捕获一个小时的流量，并将流量保存到 TiProxy 实例的 `/tmp/traffic` 目录下：
    
    ```shell
    tiproxyctl traffic capture --host 10.0.1.10 --port 3080 --output="/tmp/traffic" --duration=1h
    ```

    流量文件会自动转轮和压缩。`/tmp/traffic` 目录下的文件示例如下：

    ```shell
    ls /tmp/traffic
    # meta    traffic-2024-08-29T17-37-12.477.log.gz  traffic-2024-08-29T17-43-11.166.log.gz traffic.log
    ```

    更多信息，请参考 [`tiproxyctl traffic capture`](/tiproxy/tiproxy-command-line-flags.md#traffic-capture)。

3. 将流量文件目录复制到测试集群的 TiProxy 实例上。
4. 使用 [`tiproxyctl traffic replay`](/tiproxy/tiproxy-command-line-flags.md#traffic-replay) 连接到测试集群的 TiProxy 实例，开始回放流量。

    默认配置下，SQL 语句的执行速率与生产集群相同，数据库连接也与生产集群一一对应，以模拟生产集群的负载，并保证事务的执行顺序一致。

    例如，如下命令通过用户名 `u1` 和密码 `123456` 连接到 TiProxy 实例 `10.0.1.10:3080`，从 TiProxy 实例的 `/tmp/traffic` 目录下读取流量文件并回放流量：

    ```shell
    tiproxyctl traffic replay --host 10.0.1.10 --port 3080 --username="u1" --password="123456" --input="/tmp/traffic"
    ```

    由于所有流量在用户 `u1` 下运行，请确保 `u1` 能访问所有数据库和表。如果没有这样的用户，则需要创建一个。

    更多信息，请参考 [`tiproxyctl traffic replay`](/tiproxy/tiproxy-command-line-flags.md#traffic-replay)。

5. 查看回放报告。

    回放完成后，报告存储在测试集群的 `tiproxy_traffic_replay` 数据库下。该数据库包含两个表 `fail` 和 `other_errors`。

    `fail` 表存储运行失败的 SQL 语句，字段说明如下：

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
              err_type: failed to read the connection: EOF
        sample_err_msg: this is an error from the backend connection: failed to read the connection: EOF
    sample_replay_time: 2024-10-17 12:57:39
                 count: 1
    ```

    > **注意：**
    >
    > - `tiproxy_traffic_replay` 中的表结构在未来版本中可能会改变。不推荐在应用程序开发或工具开发中读取 `tiproxy_traffic_replay` 中的数据。
    > - 回放不保证连接之间的事务执行顺序与捕获时完全一致，因此可能会误报错误。
    > - 再次回放时，上一次的回放报告不会自动删除，需要手动删除。

## 测试吞吐量

如果需要测试集群的吞吐量，可以使用 `--speed` 选项调整回放的速率。

例如，`--speed=2` 会使 SQL 语句以两倍速率执行，总回放时间缩短一半：

```shell
tiproxyctl traffic replay --host 10.0.1.10 --port 3080 --username="u1" --password="123456" --input="/tmp/traffic" --speed=2
```

调大回放速率只会缩短 SQL 语句之间的空闲时间，不会增加连接数。因此当会话的空闲时间本身较短时，仅调大倍速可能无法有效提升吞吐量。在这种情况下，可以部署多个 TiProxy 实例，让它们同时回放相同的流量文件，通过增加并发度来提高吞吐量。

## 任务查看与管理

在捕获和回放过程中，如果遇到未知错误会自动停止任务。使用 [`tiproxyctl traffic show`](/tiproxy/tiproxy-command-line-flags.md#traffic-show) 命令可查看当前的任务进度或上次任务的错误信息：

```shell
tiproxyctl traffic show --host 10.0.1.10 --port 3080
```

例如，如下输出代表捕获任务正在运行：

```json
[
   {
      "type": "capture",
      "start_time": "2024-09-03T09:10:58.220644+08:00",
      "duration": "2h",
      "output": "/tmp/traffic",
      "progress": "45%",
      "status": "running"
   }
]
```

更多信息，请参考 [`tiproxyctl traffic show`](/tiproxy/tiproxy-command-line-flags.md#traffic-show)。

如果需要取消当前的捕获或回放任务，可使用 [`tiproxyctl traffic cancel`](/tiproxy/tiproxy-command-line-flags.md#traffic-cancel) 命令：

```shell
tiproxyctl traffic cancel --host 10.0.1.10 --port 3080
```

更多信息，请参考 [`tiproxyctl traffic cancel`](/tiproxy/tiproxy-command-line-flags.md#traffic-cancel)。

## 使用限制

- TiProxy 仅支持回放 TiProxy 捕获的流量文件，不支持其他文件格式，因此生产集群必须先使用 TiProxy 捕获流量。
- TiProxy 不支持过滤 SQL 类型，DML 和 DDL 语句也会被回放，因此重新回放前需要将集群数据恢复到回放前的状态。
- 由于 TiProxy 使用同一个用户名回放流量，因此无法测试[资源管控](/tidb-resource-control.md)和[权限管理](/privilege-management.md)。
- 不支持回放 [`LOAD DATA`](/sql-statements/sql-statement-load-data.md) 语句。

## 资源

关于 TiProxy 流量回放更详细的信息，请参阅[设计文档](https://github.com/pingcap/tiproxy/blob/main/docs/design/2024-08-27-traffic-replay.md)。