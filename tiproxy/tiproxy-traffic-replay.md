---
title: TiProxy 流量回放
summary: 介绍 TiProxy 的流量回放的使用场景和使用步骤。
---

# TiProxy 流量回放

> **警告：**
>
> TiProxy 流量回放目前为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tiproxy/issues) 反馈。

从 v1.3.0 开始，TiProxy 支持捕获生产集群的流量，并将流量回放到测试集群。

<img src="https://download.pingcap.com/images/docs-cn/tiproxy/tiproxy-traffic-replay.png" alt="TiProxy 流量回放" width="800" />

## 使用场景

流量回放适用于以下场景：

- 升级 TiDB 版本之前，在新版本的测试集群上回放生产流量，验证新版本 TiDB 能成功执行所有 SQL 语句。
- 扩缩容 TiDB 之前，在新规模的测试集群上按对应速率回放流量，验证新规模集群的性能是否满足要求。例如，为了节省成本要将集群规模缩容到 1/2，则按 1/2 速率回放流量，验证缩容后 SQL 延迟是否满足要求。
- 在相同规模的测试集群上多次回放流量，每次调大回放速率，测试该规模集群的吞吐量上限，以判断性能是否满足未来的业务增长。

不适用于以下场景：

- 从 MySQL 捕获流量后在 TiDB 上回放，验证 TiDB 与 MySQL 的 SQL 兼容性。TiProxy 只支持读取 TiProxy 生成的流量文件。
- 验证新版本 TiDB 的 SQL 语句执行结果与旧版本相同。TiProxy 只验证 SQL 语句是否执行成功，不对比运行结果。

## 使用步骤

1. 创建测试集群，将生产集群的数据同步到测试集群，并在测试集群中运行 `ANALYZE` 更新统计信息。
2. 使用 `tiproxyctl traffic capture` 命令连接到生产集群的 TiProxy 实例，开始捕获流量。TiProxy 会捕获所有连接上的流量，包括已创建的新创建的连接。

    在 TiProxy 主备模式下，请确保连接到 TiProxy 主实例。如果集群使用了虚拟 IP，建议连接到虚拟 IP 地址。

    例如，以下命令连接到 TiProxy 实例 `10.0.1.10:3080`，捕获一个小时的流量，并将流量保存到 TiProxy 实例的 `/tmp/traffic` 目录下：
    
    ```shell
    tiproxyctl traffic capture --curls 10.0.1.10:3080 --output="/tmp/traffic" --duration=1h
    ```

    流量文件会自动转轮和压缩。`/tmp/traffic` 目录下的文件样例：

    ```shell
    $ ls /tmp/traffic
    meta    traffic-2024-08-29T17-37-12.477.log.gz  traffic-2024-08-29T17-43-11.166.log.gz traffic.log
    ```
    
    更多详细信息请参考 [`tiproxyctl traffic capture`](/tiproxy/tiproxy-command-line-flags.md#traffic-capture) 的使用文档。

3. 将流量文件目录复制到测试集群的 TiProxy 实例上。
4. 使用 `tiproxyctl traffic replay` 连接到测试集群的 TiProxy 实例，开始回放流量。

    默认配置下，SQL 语句的执行速率与生产集群相同，数据库连接也与生产集群一一对应，以模拟生产集群的负载，并保证事务的执行顺序一致。

    例如，如下命令通过用户名 `u1` 和密码 `123456` 连接到 TiProxy 实例 `10.0.1.10:3080`，并从 TiProxy 实例的 `/tmp/traffic` 目录下读取流量文件，并回放流量：

    ```shell
    tiproxyctl traffic replay --curls 10.0.1.10:3080 --username="u1" --password="123456" --input="/tmp/traffic"
    ```

    由于所有流量在用户 `u1` 下运行，请确保 `u1` 能访问所有数据库和表。如果没有这样的用户，则需要创建一个。

    如果需要测试集群的吞吐量，可以调整回放的速率。例如，加上选项 `--speed=2` 后，SQL 语句的执行间隔缩短，以 2 倍速率执行，总的回放时间缩短一半：

    ```shell
    tiproxyctl traffic replay --curls 10.0.1.10:3080 --username="u1" --password="123456" --input="/tmp/traffic" --speed=2
    ```

    更多详细信息请参考 [`tiproxyctl traffic replay`](/tiproxy/tiproxy-command-line-flags.md#traffic-replay) 的使用文档。

5. 在捕获和回放过程中，如果遇到未知错误会自动停止任务。通过 `tiproxyctl traffic show` 命令可查看当前的任务进度或上次任务的错误信息：

    ```shell
    tiproxyctl traffic show --curls 10.0.1.10:3080
    ```

    例如，如下输出代表捕获任务正在运行：

    ```json
    [{"type":"capture","start_time":"2024-09-03T09:10:58.220644+08:00","duration":"2h","progress":"45%","status":"running"}]
    ```

    更多详细信息请参考 [`tiproxyctl traffic show`](/tiproxy/tiproxy-command-line-flags.md#traffic-show) 的使用文档。

    如果需要取消当前的捕获或回放任务，可使用 `tiproxyctl traffic cancel` 命令：

    ```shell
    tiproxyctl traffic cancel --curls 10.0.1.10:3080
    ```

    更多详细信息请参考 [`tiproxyctl traffic cancel`](/tiproxy/tiproxy-command-line-flags.md#traffic-cancel) 的使用文档。

6. 回放完成之后，报告存储在测试集群的 `tiproxy_traffic_report` 数据库下。该数据库下有两个表，`fail` 和 `other_errors`。

    表 `fail` 存储运行失败的 SQL 语句。它的字段如下：

    - `cmd_type`: 运行错误的命令类型，常见的有 `Query`(执行普通语句)、`Prepare`(预处理语句)、`Execute`(执行预处理语句)。
    - `digest`: 执行失败的 SQL 语句的指纹。
    - `sample_stmt`: 该 SQL 语句首次执行失败时的 SQL 文本。
    - `sample_err_msg`: 以上 SQL 语句执行失败的报错信息。
    - `sample_capture_time`: 以上 SQL 语句在流量文件中记录的执行时间，可用于在流量文件中查看 SQL 语句的执行上下文。
    - `sample_replay_time`: 以上 SQL 语句在回放时执行失败的时间，可用于在 TiDB 日志文件中查看错误信息。
    - `count`: 该 SQL 语句执行失败的次数。

    表 `other_errors` 存储其他未预期错误，例如网络错误、连接数据库错误。它的字段如下：

    - `err_type`: 该错误的类型，是一个简短的错误信息，例如 `i/o timeout`。
    - `sample_err_msg`: 该错误首次出现时的完整错误信息。
    - `sample_replay_time`: 该错误在回放时执行失败的时间，可用于在 TiDB 日志文件中查看错误信息。
    - `count`: 该错误出现的次数。

## 使用限制

- TiProxy 仅支持回放 TiProxy 捕获的流量文件，不支持其他文件格式，因此生产集群使用了 TiProxy 之后才能捕获和回放流量。
- TiProxy 不支持过滤 SQL 类型，DML 或 DDL 语句也会回放，因此重新回放前需要恢复集群数据到回放之前的状态。
- 由于 TiProxy 使用同一个用户名回放流量，因此不能测试[资源管控](/tidb-resource-control.md)和[权限管理](/privilege-management.md)。
- 不支持回放 [`LOAD DATA`](/sql-statements/sql-statement-load-data.md) 语句。