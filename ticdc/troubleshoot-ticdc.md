---
title: TiCDC 常见问题和故障处理
aliases: ['/docs-cn/stable/ticdc/troubleshoot-ticdc/','/docs-cn/v4.0/ticdc/troubleshoot-ticdc/','/docs-cn/stable/reference/tools/ticdc/troubleshoot/']
---

# TiCDC 常见问题和故障处理

本文档总结了在使用 TiCDC 过程中经常遇到的问题，给出合适的运维方法。本文档还总结了常见的运行故障，并给出相对应的解决方案。

## TiCDC 创建任务时如何选择 start-ts？

首先需要理解同步任务的 `start-ts` 对应于上游 TiDB 集群的一个 TSO，同步任务会从这个 TSO 开始请求数据。所以同步任务的 `start-ts` 需要满足以下两个条件：

- `start-ts` 的值需要大于 TiDB 集群当前的 `tikv_gc_safe_point`，否则创建任务时会报错。
- 启动任务时，需要保证下游已经具有 `start-ts` 之前的所有数据。对于同步到消息队列等场景，如果不需要保证上下游数据的一致，可根据业务场景放宽此要求。

如果不指定 `start-ts` 或者指定 `start-ts=0`，在启动任务的时候会去 PD 获取一个当前 TSO，并从该 TSO 开始同步。

## 为什么 TiCDC 创建任务时提示部分表不能同步？

在使用 `cdc cli changefeed create` 创建同步任务时会检查上游表是否符合[同步限制](/ticdc/ticdc-overview.md#同步限制)。如果存在表不满足同步限制，会提示 `some tables are not eligible to replicate` 并列出这些不满足的表。用户选择 `Y` 或 `y` 则会继续创建同步任务，并且同步过程中自动忽略这些表的所有更新。用户选择其他输入，则不会创建同步任务。

## 如何处理 TiCDC 同步任务的中断？

目前已知可能发生的同步中断包括以下两类场景：

- 下游持续异常，TiCDC 多次重试后仍然失败。

    - 该场景下 TiCDC 会保存任务信息，由于 TiCDC 已经在 PD 中设置的 service GC safepoint，在 `gc-ttl` 的有效期内，同步任务 checkpoint 之后的数据不会被 TiKV GC 清理掉。

    - 处理方法：用户可以在下游恢复正常后，通过 HTTP 接口恢复同步任务。

- 因下游存在不兼容的 SQL 语句，导致同步不能继续。

    - 该场景下 TiCDC 会保存任务信息，由于 TiCDC 已经在 PD 中设置的 service GC safepoint，在 `gc-ttl` 的有效期内，同步任务 checkpoint 之后的数据不会被 TiKV GC 清理掉。
    - 处理方法：
        1. 用户需先通过 `cdc cli changefeed query` 查询同步任务状态信息，记录 `checkpoint-ts` 值。
        2. 使用新的任务配置文件，增加`ignore-txn-start-ts` 参数跳过指定 `start-ts` 对应的事务。
        3. 通过 HTTP API 停止旧的同步任务，使用 `cdc cli changefeed create` ，指定新的任务配置文件，指定 `start-ts` 为刚才记录的 `checkpoint-ts`，启动新的同步任务恢复同步。

## 如何判断 TiCDC 同步任务出现中断？

- 通过 Grafana 检查同步任务的 `changefeed checkpoint`（注意选择正确的 `changefeed id`）监控项。如果该值不发生变化（也可以查看 `checkpoint lag` 是否不断增大），可能同步任务出现中断。
- 通过 Grafana 检查 `exit error count` 监控项，该监控项大于 0 代表同步任务出现错误。
- 通过 `cdc cli changefeed list` 和 `cdc cli changefeed query` 命令查看同步任务的状态信息。任务状态为 `stopped` 代表同步中断，`error` 项会包含具体的错误信息。任务出错后可以在 TiCDC server 日志中搜索 `error on running processor` 查看错误堆栈，帮助进一步排查问题。
- 部分极端异常情况下 TiCDC 出现服务重启，可以在 TiCDC server 日志中搜索 `FATAL` 级别的日志排查问题。

## TiCDC 的 `gc-ttl` 和文件排序是什么？

从 TiDB v4.0.0-rc.1 版本起，PD 支持外部服务设置服务级别 GC safepoint。任何一个服务可以注册更新自己服务的 GC safepoint。PD 会保证任何小于该 GC safepoint 的 KV 数据不会在 TiKV 中被 GC 清理掉。在 TiCDC 中启用了这一功能，用来保证 TiCDC 在不可用、或同步任务中断情况下，可以在 TiKV 内保留 TiCDC 需要消费的数据不被 GC 清理掉。

启动 TiCDC server 时可以通过 `gc-ttl` 指定 GC safepoint 的 TTL，这个值的含义是当 TiCDC 服务全部挂掉后，由 TiCDC 在 PD 所设置的 GC safepoint 保存的最长时间，该值默认为 86400 秒。

如果同步任务长时间中断，累积未消费的数据比较多，初始启动 TiCDC 可能会发生 OOM。这种情况下可以启用 TiCDC 提供的文件排序功能，该功能会使用文件系统文件进行排序。启用的方式是创建同步任务时在 `cdc cli` 内传入 `--sort-engine=file` 和 `--sort-dir=/path/to/sort_dir`，使用示例如下：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --pd=http://10.0.10.25:2379 --start-ts=415238226621235200 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --sort-engine="file" --sort-dir="/data/cdc/sort"
```

> **注意：**
>
> + TiCDC（4.0 发布版本）还不支持动态修改文件排序和内存排序。
> + 目前文件排序功能的处理能力有限。如果单表数据量过多导致文件排序失败，可以修改 TiCDC 任务配置过滤掉这张表，通过其他备份恢复工具例如 BR 恢复这张表之后再继续同步该表。

## 如何处理 TiCDC 创建同步任务或同步到 MySQL 时遇到 `Error 1298: Unknown or incorrect time zone: 'UTC'` 错误？

这是因为下游 MySQL 没有加载时区，可以通过 [mysql_tzinfo_to_sql](https://dev.mysql.com/doc/refman/8.0/en/mysql-tzinfo-to-sql.html) 命令加载时区，加载后就可以正常创建任务或同步任务。

{{< copyable "shell-regular" >}}

```shell
mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root mysql -p
```

```
Enter password:
Warning: Unable to load '/usr/share/zoneinfo/iso3166.tab' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/leap-seconds.list' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/zone.tab' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/zone1970.tab' as time zone. Skipping it.
```

如果是在特殊的公有云环境使用 MySQL，譬如阿里云 RDS 并且没有修改 MySQL 的权限，就需要通过 `--tz` 参数指定时区。可以首先在 MySQL 查询其使用的时区，然后在创建同步任务和创建 TiCDC 服务时使用该时区。

{{< copyable "shell-regular" >}}

```shell
show variables like '%time_zone%';
```

```
+------------------+--------+
| Variable_name    | Value  |
+------------------+--------+
| system_time_zone | CST    |
| time_zone        | SYSTEM |
+------------------+--------+
```

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --sink-uri="mysql://root@127.0.0.1:3306/" --tz=Asia/Shanghai
```

> **注意：**
>
> 在 MySQL 中 CST 时区通常实际代表的是 China Standard Time (UTC+08:00)，通常系统中不能直接使用 `CST`，而是用 `Asia/Shanghai` 来替换。

> **注意：**
>
> 请谨慎设置 TiCDC server 的时区，因为该时区会用于时间类型的转换。推荐上下游数据库使用相同的时区，并且启动 TiCDC server 时通过 `--tz` 参数指定该时区。TiCDC server 时区使用的优先级如下：
>
> - 最优先使用 `--tz` 传入的时区。
> - 没有 `--tz` 参数，会尝试读取 `TZ` 环境变量设置的时区。
> - 如果还没有 `TZ` 环境变量，会从 TiCDC server 运行机器的默认时区。

## 如何处理升级 TiCDC 后配置文件不兼容的问题？

请参阅[配置文件兼容注意事项](/ticdc/manage-ticdc.md#配置文件兼容性的注意事项)。

## TiCDC 是否支持输出 Canal 格式的变更数据？

支持。要开启 Canal 格式输出，只需在 `--sink-uri` 中指定 protocol 为 `canal` 即可，例如：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --pd=http://10.0.10.25:2379 --sink-uri="kafka://127.0.0.1:9092/cdc-test?kafka-version=2.4.0&protocol=canal" --config changefeed.toml
```

> **注意：**
>
> * 该功能在 TiCDC 4.0.2 版本引入。
> * 目前 TiCDC 仅支持将 Canal 格式的变更数据输出到 Kafka。

更多信息请参考[创建同步任务](/ticdc/manage-ticdc.md#创建同步任务)。

## 如何查看 TiCDC 同步任务的状态？

可以使用 `cdc cli` 查询同步任务的状态。例如：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed list --pd=http://10.0.10.25:2379
```

上述命令输出如下：

```json
[{
    "id": "4e24dde6-53c1-40b6-badf-63620e4940dc",
    "summary": {
      "state": "normal",
      "tso": 417886179132964865,
      "checkpoint": "2020-07-07 16:07:44.881",
      "error": null
    }
}]
```

* `checkpoint`：即为 TiCDC 已经将该时间点前的数据同步到了下游。
* `state` 为该同步任务的状态：
    * `normal`：正常同步。
    * `stopped`：停止同步（手动暂停或出错）。
    * `removed`：已删除任务。

> **注意：**
>
> 该功能在 TiCDC 4.0.3 版本引入。

## 如何查看 TiCDC 同步任务是否被人为终止？

可以使用 `cdc cli` 查询同步任务是否被人为终止。例如：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed query --pd=http://10.0.10.25:2379 --changefeed-id 28c43ffc-2316-4f4f-a70b-d1a7c59ba79f
```

上述命令的输出中 `admin-job-type` 标志这个同步的任务的状态：

* `0`: 任务进行中，没有被人为停止。
* `1`: 任务暂停，停止任务后所有同步 `processor` 会结束退出，同步任务的配置和同步状态都会保留，可以从 `checkpoint-ts` 恢复任务。
* `2`: 任务恢复，同步任务从 `checkpoint-ts` 继续同步。
* `3`: 任务已删除，接口请求后会结束所有同步 `processor`，并清理同步任务配置信息。同步状态保留，只提供查询，没有其他实际功能。

## 为什么 TiCDC 到 Kafka 的同步任务延时越来越大？

* 请参考 [如何查看 TiCDC 同步任务的状态？](/ticdc/troubleshoot-ticdc.md#如何查看-ticdc-同步任务的状态) 检查下同步任务的状态是否正常。
* 请适当调整 Kafka 的以下参数：
    * `message.max.bytes`，将 Kafka 的 `server.properties` 中该参数调大到 `1073741824` (1 GB)。
    * `replica.fetch.max.bytes`，将 Kafka 的 `server.properties` 中该参数调大到 `1073741824` (1 GB)。
    * `fetch.message.max.bytes`，适当调大 `consumer.properties` 中该参数，确保大于 `message.max.bytes`。

## TiCDC 把数据同步到 Kafka 时，是把一个事务内的所有变更都写到一个消息中吗？如果不是，是根据什么划分的？

不是，根据配置的分发策略不同，有不同的划分方式，包括 `default`、`row id`、`table`、`ts`。更多请参考[同步任务配置文件描述](/ticdc/manage-ticdc.md#同步任务配置文件描述)。

## TiCDC 把数据同步到 Kafka 时，能在 TiDB 中控制单条消息大小的上限吗？

不能，目前 TiCDC 控制了向 Kafka 发送的消息批量的大小最大为 512 MB，其中单个消息的大小最大为 4 MB。

## TiCDC 把数据同步到 Kafka 时，一条消息中会不会包含多种数据变更？

会，一条消息中可能出现多个 `update` 或 `delete`，`update` 和 `delete` 也有可能同时存在。

## TiCDC 把数据同步到 Kafka 时，如何查看 TiCDC Open protocol 输出变更数据中的时间戳、表名和库名？

这些信息包含在 Kafka 消息的 Key 中，比如：

```json
{
    "ts":<TS>,
    "scm":<Schema Name>,
    "tbl":<Table Name>,
    "t":1
}
```

更多信息请参考 [Open protocol Event 格式定义](/ticdc/ticdc-open-protocol.md#event-格式定义)

## TiCDC 把数据同步到 Kafka 时，如何确定一条消息中包含的数据变更发生在哪个时间点？

把 Kafka 消息的 Key 中的 `ts` 右移 18 位即得 unix timestamp。

## TiCDC Open protocol 如何标示 null 值？

Open protocol 的输出中 type = 6 即为 null，比如：

| 类型         | Code | 输出示例 | 说明 |
| :---------- | :--- | :------ | :-- |
| Null        | 6    | `{"t":6,"v":null}` | |

更多信息请参考 [Open protocol Event 格式定义](/ticdc/ticdc-open-protocol.md#column-的类型码)。
