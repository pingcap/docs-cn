---
title: TiCDC 常见问题和故障处理
---

# TiCDC 常见问题和故障处理

本文档总结了在使用 TiCDC 过程中经常遇到的问题，给出合适的运维方法。本文档还总结了常见的运行故障，并给出相对应的解决方案。

> **注意：**
>
> 本文档 `cdc cli` 命令中指定 PD 地址为 `--pd=http://10.0.10.25:2379`，用户在使用时需根据实际地址进行替换。

## TiCDC 创建任务时如何选择 start-ts？

首先需要理解同步任务的 `start-ts` 对应于上游 TiDB 集群的一个 TSO，同步任务会从这个 TSO 开始请求数据。所以同步任务的 `start-ts` 需要满足以下两个条件：

- `start-ts` 的值需要大于 TiDB 集群当前的 `tikv_gc_safe_point`，否则创建任务时会报错。
- 启动任务时，需要保证下游已经具有 `start-ts` 之前的所有数据。对于同步到消息队列等场景，如果不需要保证上下游数据的一致，可根据业务场景放宽此要求。

如果不指定 `start-ts` 或者指定 `start-ts=0`，在启动任务的时候会去 PD 获取一个当前 TSO，并从该 TSO 开始同步。

## 为什么 TiCDC 创建任务时提示部分表不能同步？

在使用 `cdc cli changefeed create` 创建同步任务时会检查上游表是否符合[同步限制](/ticdc/ticdc-overview.md#同步限制)。如果存在表不满足同步限制，会提示 `some tables are not eligible to replicate` 并列出这些不满足的表。用户选择 `Y` 或 `y` 则会继续创建同步任务，并且同步过程中自动忽略这些表的所有更新。用户选择其他输入，则不会创建同步任务。

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

## TiCDC 同步任务出现中断

### 如何判断 TiCDC 同步任务出现中断？

- 通过 Grafana 检查同步任务的 `changefeed checkpoint`（注意选择正确的 `changefeed id`）监控项。如果该值不发生变化（也可以查看 `checkpoint lag` 是否不断增大），可能同步任务出现中断。
- 通过 Grafana 检查 `exit error count` 监控项，该监控项大于 0 代表同步任务出现错误。
- 通过 `cdc cli changefeed list` 和 `cdc cli changefeed query` 命令查看同步任务的状态信息。任务状态为 `stopped` 代表同步中断，`error` 项会包含具体的错误信息。任务出错后可以在 TiCDC server 日志中搜索 `error on running processor` 查看错误堆栈，帮助进一步排查问题。
- 部分极端异常情况下 TiCDC 出现服务重启，可以在 TiCDC server 日志中搜索 `FATAL` 级别的日志排查问题。

### 如何查看 TiCDC 同步任务是否被人为终止？

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

### 如何处理 TiCDC 同步任务的中断？

目前已知可能发生的同步中断包括以下场景：

- 下游持续异常，TiCDC 多次重试后仍然失败。

    - 该场景下 TiCDC 会保存任务信息，由于 TiCDC 已经在 PD 中设置的 service GC safepoint，在 `gc-ttl` 的有效期内，同步任务 checkpoint 之后的数据不会被 TiKV GC 清理掉。
    - 处理方法：用户可以在下游恢复正常后，通过 HTTP 接口恢复同步任务。

- 因下游存在不兼容的 SQL 语句，导致同步不能继续。

    - 该场景下 TiCDC 会保存任务信息，由于 TiCDC 已经在 PD 中设置的 service GC safepoint，在 `gc-ttl` 的有效期内，同步任务 checkpoint 之后的数据不会被 TiKV GC 清理掉。
    - 处理方法：
        1. 用户需先通过 `cdc cli changefeed query` 查询同步任务状态信息，记录 `checkpoint-ts` 值。
        2. 使用新的任务配置文件，增加`ignore-txn-start-ts` 参数跳过指定 `start-ts` 对应的事务。
        3. 通过 HTTP API 停止旧的同步任务，使用 `cdc cli changefeed create` ，指定新的任务配置文件，指定 `start-ts` 为刚才记录的 `checkpoint-ts`，启动新的同步任务恢复同步。

- 在 v4.0.13 及以下版本中 TiCDC 同步分区表存在问题，导致同步停止。

    - 该场景下 TiCDC 会保存任务信息，由于 TiCDC 已经在 PD 中设置的 service GC safepoint，在 `gc-ttl` 的有效期内，同步任务 checkpoint 之后的数据不会被 TiKV GC 清理掉。
    - 处理方法：
        1. 通过 `cdc cli changefeed pause -c <changefeed-id>` 暂停同步。
        2. 等待约一分钟后，通过 `cdc cli changefeed resume -c <changefeed-id>` 恢复同步。

### 同步任务中断，尝试再次启动后 TiCDC 发生 OOM，如何处理？

升级 TiDB 集群和 TiCDC 集群到最新版本。OOM 问题在 v4.0.14 上已得到缓解。

如无法升级，则需要开启 Unified Sorter 排序功能，该功能会在系统内存不足时使用磁盘进行排序。启用的方式是创建同步任务时在 `cdc cli` 内传入 `--sort-engine=unified` 和 `--sort-dir=/path/to/sort_dir`，使用示例如下：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed update -c <changefeed-id> --sort-engine="unified" --sort-dir="/data/cdc/sort" --pd=http://10.0.10.25:2379
```

> **注意：**
>
> + TiCDC 从 4.0.9 版本起支持 Unified Sorter 排序引擎。
> + TiCDC（4.0 发布版本）还不支持动态修改排序引擎。在修改排序引擎设置前，请务必确保 changefeed 已经停止 (stopped)。
> + `sort-dir` 在不同版本之间有不同的行为，请参考 [`sort-dir` 及 `data-dir` 配置项的兼容性说明](/ticdc/ticdc-overview.md#sort-dir-及-data-dir-配置项的兼容性说明)，谨慎配置。
> + 目前 Unified Sorter 排序引擎为实验特性，在数据表较多 (>= 100) 时可能出现性能问题，影响同步速度，故不建议在生产环境中使用。开启 Unified Sorter 前请保证各 TiCDC 节点机器上有足够硬盘空间。如果积攒的数据总量有可能超过 1 TB，则不建议使用 TiCDC 进行同步。

## TiCDC 的 `gc-ttl` 是什么？

从 TiDB v4.0.0-rc.1 版本起，PD 支持外部服务设置服务级别 GC safepoint。任何一个服务可以注册更新自己服务的 GC safepoint。PD 会保证任何晚于该 GC safepoint 的 KV 数据不会在 TiKV 中被 GC 清理掉。在 TiCDC 中启用了这一功能，用来保证 TiCDC 在不可用、或同步任务中断情况下，可以在 TiKV 内保留 TiCDC 需要消费的数据不被 GC 清理掉。

启动 TiCDC server 时可以通过 `gc-ttl` 指定 GC safepoint 的 TTL，这个值的含义是当 TiCDC 服务全部挂掉后，由 TiCDC 在 PD 所设置的 GC safepoint 保存的最长时间，该值默认为 86400 秒。

## TiCDC GC safepoint 的完整行为是什么

TiCDC 服务启动后，如果有任务开始同步，TiCDC owner 会根据所有同步任务最小的 checkpoint-ts 更新到 PD service GC safepoint，service GC safepoint 可以保证该时间点及之后的数据不被 GC 清理掉。如果 TiCDC 同步任务中断，该任务的 checkpoint-ts 不会再改变，PD 对应的 service GC safepoint 也不会再更新。TiCDC 为 service GC safepoint 设置的存活有效期为 24 小时，即 TiCDC 服务中断 24 小时内恢复能保证数据不因 GC 而丢失。

## 如何处理 TiCDC 创建同步任务或同步到 MySQL 时遇到 `Error 1298: Unknown or incorrect time zone: 'UTC'` 错误？

这是因为下游 MySQL 没有加载时区，可以通过 [mysql_tzinfo_to_sql](https://dev.mysql.com/doc/refman/8.0/en/mysql-tzinfo-to-sql.html) 命令加载时区，加载后就可以正常创建任务或同步任务。

{{< copyable "shell-regular" >}}

```shell
mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root mysql -p
```

显示类似于下面的输出则表示导入已经成功：

```
Enter password:
Warning: Unable to load '/usr/share/zoneinfo/iso3166.tab' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/leap-seconds.list' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/zone.tab' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/zone1970.tab' as time zone. Skipping it.
```

如果下游是特殊的 MySQL 环境（某种公有云 RDS 或某些 MySQL 衍生版本等），使用上述方式导入时区失败，就需要通过 sink-uri 中的 `time-zone` 参数指定下游的 MySQL 时区。可以首先在 MySQL 中查询其使用的时区：

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

然后在创建同步任务和创建 TiCDC 服务时使用该时区：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --sink-uri="mysql://root@127.0.0.1:3306/?time-zone=CST" --pd=http://10.0.10.25:2379
```

> **注意：**
>
> CST 可能是以下四个不同时区的缩写：
>
> + 美国中部时间：Central Standard Time (USA) UT-6:00
> + 澳大利亚中部时间：Central Standard Time (Australia) UT+9:30
> + 中国标准时间：China Standard Time UT+8:00
> + 古巴标准时间：Cuba Standard Time UT-4:00
>
> 在中国，CST 通常表示中国标准时间，使用时请注意甄别。

## 如何理解 TiCDC 时区和上下游数据库系统时区之间的关系？

||上游时区| TiCDC 时区| 下游时区 |
| :-: | :-: | :-: | :-: |
| 配置方式 | 见[时区支持](/configure-time-zone.md) | 启动 ticdc server 时的 `--tz` 参数 | sink-uri 中的 `time-zone` 参数 |
| 说明 | 上游 TiDB 的时区，影响 timestamp 类型的 DML 操作和与 timestamp 类型列相关的 DDL 操作。 | TiCDC 会将假设上游 TiDB 的时区和 TiCDC 时区配置相同，对 timestamp 类型的列进行相关处理。 | 下游 MySQL 将按照下游的时区设置对 DML 和 DDL 操作中包含的 timestamp 进行处理。|

> **注意：**
>
> 请谨慎设置 TiCDC server 的时区，因为该时区会用于时间类型的转换。上游时区、TiCDC 时区和下游时区应该保持一致。TiCDC server 时区使用的优先级如下：
>
> - 最优先使用 `--tz` 传入的时区。
> - 没有 `--tz` 参数，会尝试读取 `TZ` 环境变量设置的时区。
> - 如果还没有 `TZ` 环境变量，会从 TiCDC server 运行机器的默认时区。

## 创建同步任务时，如果不指定 `--config` 配置文件，TiCDC 的默认的行为是什么？

在使用 `cdc cli changefeed create` 命令时如果不指定 `--config` 参数，TiCDC 会按照以下默认行为创建同步任务：

* 同步所有的非系统表
* 开启 old value 功能
* 不同步不包含[有效索引](/ticdc/ticdc-overview.md#同步限制)的表

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
> * 目前 TiCDC 仅支持将 Canal 格式的变更数据输出到 MQ 类的 Sink（例如：Kafka，Pulsar）。

更多信息请参考[创建同步任务](/ticdc/manage-ticdc.md#创建同步任务)。

## 为什么 TiCDC 到 Kafka 的同步任务延时越来越大？

* 请参考[如何查看 TiCDC 同步任务的状态？](/ticdc/troubleshoot-ticdc.md#如何查看-ticdc-同步任务的状态)检查下同步任务的状态是否正常。
* 请适当调整 Kafka 的以下参数：
    * `message.max.bytes`，将 Kafka 的 `server.properties` 中该参数调大到 `1073741824` (1 GB)。
    * `replica.fetch.max.bytes`，将 Kafka 的 `server.properties` 中该参数调大到 `1073741824` (1 GB)。
    * `fetch.message.max.bytes`，适当调大 `consumer.properties` 中该参数，确保大于 `message.max.bytes`。

## TiCDC 把数据同步到 Kafka 时，是把一个事务内的所有变更都写到一个消息中吗？如果不是，是根据什么划分的？

不是，根据配置的分发策略不同，有不同的划分方式，包括 `default`、`row id`、`table`、`ts`。更多请参考[同步任务配置文件描述](/ticdc/manage-ticdc.md#同步任务配置文件描述)。

## TiCDC 把数据同步到 Kafka 时，能在 TiDB 中控制单条消息大小的上限吗？

可以通过 `max-message-bytes` 控制每次向 Kafka broker 发送消息的最大数据量（可选，默认值 64MB）；通过 `max-batch-size` 参数指定每条 kafka 消息中变更记录的最大数量，目前仅对 Kafka 的 protocol 为 `default` 时有效（可选，默认值为 `4096`）。

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

## TiCDC 启动任务的 start-ts 时间戳与当前时间差距较大，任务执行过程中同步中断，出现错误 `[CDC:ErrBufferReachLimit]`，怎么办？

自 v4.0.9 起可以尝试开启 unified sorter 特性进行同步；或者使用 BR 工具进行一次增量备份和恢复，然后从新的时间点开启 TiCDC 同步任务。TiCDC 将会在后续版本中对该问题进行优化。

## 如何区分 TiCDC Open Protocol 中的 Row Changed Event 是 `INSERT` 事件还是 `UPDATE` 事件？

如果没有开启 Old Value 功能，用户无法区分 TiCDC Open Protocol 中的 Row Changed Event 是 `INSERT` 事件还是 `UPDATE` 事件。如果开启了 Old Value 功能，则可以通过事件中的字段判断事件类型：

* 如果同时存在 `"p"` 和 `"u"` 字段为 `UPDATE` 事件
* 如果只存在 `"u"` 字段则为 `INSERT` 事件
* 如果只存在 `"d"` 字段则为 `DELETE` 事件

更多信息请参考 [Open protocol Row Changed Event 格式定义](/ticdc/ticdc-open-protocol.md#row-changed-event)。

## TiCDC 占用多少 PD 的存储空间

TiCDC 使用 PD 内部的 etcd 来存储元数据并定期更新。因为 etcd 的多版本并发控制 (MVCC) 以及 PD 默认的 compaction 间隔是 1 小时，TiCDC 占用的 PD 存储空间与 1 小时内元数据的版本数量成正比。在 v4.0.5、v4.0.6、v4.0.7 三个版本中 TiCDC 存在元数据写入频繁的问题，如果 1 小时内有 1000 张表创建或调度，就会用尽 etcd 的存储空间，出现 `etcdserver: mvcc: database space exceeded` 错误。出现这种错误后需要清理 etcd 存储空间，参考 [etcd maintaince space-quota](https://etcd.io/docs/v3.4.0/op-guide/maintenance/#space-quota)。推荐使用这三个版本的用户升级到 v4.0.9 及以后版本。

## TiCDC 支持同步大事务吗？有什么风险吗？

TiCDC 对大事务（大小超过 5 GB）提供部分支持，根据场景不同可能存在以下风险：

+ 当 TiCDC 内部处理能力不足时，可能出现同步任务报错 `ErrBufferReachLimit`。
+ 当 TiCDC 内部处理能力不足或 TiCDC 下游吞吐能力不足时，可能出现内存溢出 (OOM)。

当遇到上述错误时，建议将包含大事务部分的增量数据通过 BR 进行增量恢复，具体操作如下：

1. 记录因为大事务而终止的 changefeed 的 `checkpoint-ts`，将这个 TSO 作为 BR 增量备份的 `--lastbackupts`，并执行[增量备份](/br/use-br-command-line-tool.md#增量备份)。
2. 增量备份结束后，可以在 BR 日志输出中找到类似 `["Full backup Failed summary : total backup ranges: 0, total success: 0, total failed: 0"] [BackupTS=421758868510212097]` 的日志，记录其中的 `BackupTS`。
3. 执行[增量恢复](/br/use-br-command-line-tool.md#增量恢复)。
4. 建立一个新的 changefeed，从 `BackupTS` 开始同步任务。
5. 删除旧的 changefeed。

## 当 changefeed 的下游为类 MySQL 数据库时，TiCDC 执行了一个耗时较长的 DDL 语句，阻塞了所有其他 changefeed，应该怎样处理？

1. 首先暂停执行耗时较长的 DDL 的 changefeed。此时可以观察到，这个 changefeed 暂停后，其他的 changefeed 不再阻塞了。
2. 在 TiCDC log 中搜寻 `apply job` 字段，确认耗时较长的 DDL 的 `start-ts`。
3. 手动在下游执行该 DDL 语句，执行完毕后进行下面的操作。
4. 修改 changefeed 配置，将上述 `start-ts` 添加到 `ignore-txn-start-ts` 配置项中。
5. 恢复被暂停的 changefeed。

## TiCDC 集群升级到 v4.0.8 之后，changefeed 报错 `[CDC:ErrKafkaInvalidConfig]Canal requires old value to be enabled`，为什么？

自 v4.0.8 起，如果 changefeed 使用 canal 或者 maxwell 协议输出，TiCDC 会自动开启 Old Value 功能。但如果 TiCDC 是从较旧版本升级到 v4.0.8 或以上版本的，changefeed 使用 canal 或 maxwell 协议的同时 Old Value 功能被禁用，此时会出现该报错。可以按照以下步骤解决该报错：

1. 将 changefeed 配置文件中 `enable-old-value` 的值设为 `true`。
2. 使用 `cdc cli changefeed pause` 暂停同步任务。

    {{< copyable "shell-regular" >}}

    ```shell
    cdc cli changefeed pause -c test-cf --pd=http://10.0.10.25:2379
    ```

3. 使用 `cdc cli changefeed update` 更新原有 changefeed 的配置。

    {{< copyable "shell-regular" >}}

    ```shell
    cdc cli changefeed update -c test-cf --pd=http://10.0.10.25:2379 --sink-uri="mysql://127.0.0.1:3306/?max-txn-row=20&worker-number=8" --config=changefeed.toml
    ```

4. 使用 `cdc cli changefeed resume` 恢复同步任务。

    {{< copyable "shell-regular" >}}

    ```shell
    cdc cli changefeed resume -c test-cf --pd=http://10.0.10.25:2379
    ```

## 使用 TiCDC 创建 changefeed 时报错 `[tikv:9006]GC life time is shorter than transaction duration, transaction starts at xx, GC safe point is yy`

解决方案：需要执行 `pd-ctl service-gc-safepoint --pd <pd-addrs>` 命令查询当前的 GC safepoint 与 service GC safepoint。如果 GC safepoint 小于 TiCDC changefeed 同步任务的开始时间戳 `start-ts`，则用户可以直接在 `cdc cli create changefeed` 命令后加上 `--disable-gc-check` 参数创建 changefeed。

如果 `pd-ctl service-gc-safepoint --pd <pd-addrs>` 的结果中没有 `gc_worker service_id`：

+ 如果 PD 的版本 <= v4.0.8，详见 [PD issue #3128](https://github.com/tikv/pd/issues/3128)。
+ 如果 PD 是由 v4.0.8 或更低版本滚动升级到新版，详见 [PD issue #3366](https://github.com/tikv/pd/issues/3366)。
+ 对于其他情况，请将上述命令执行结果反馈到 [AskTUG 论坛](https://asktug.com/tags/ticdc)。

## 使用 TiCDC 创建同步任务时将 `enable-old-value` 设置为 `true` 后，为什么上游的 `INSERT`/`UPDATE` 语句经 TiCDC 同步到下游后变为了 `REPLACE INTO`？

TiCDC 创建 changefeed 时会默认指定 `safe-mode` 为 `true`，从而为上游的 `INSERT`/`UPDATE` 语句生成 `REPLACE INTO` 的执行语句。

目前用户暂时无法修改 `safe-mode` 设置，因此该问题暂无解决办法。

## 使用 TiCDC 同步消息到 Kafka 时 Kafka 报错 `Message was too large`

v4.0.8 或更低版本的 TiCDC，仅在 Sink URI 中为 Kafka 配置 `max-message-bytes` 参数不能有效控制输出到 Kafka 的消息大小，需要在 Kafka server 配置中加入如下配置以增加 Kafka 接收消息的字节数限制。

```
# broker 能接收消息的最大字节数
message.max.bytes=2147483648
# broker 可复制的消息的最大字节数
replica.fetch.max.bytes=2147483648
# 消费者端的可读取的最大消息字节数
fetch.message.max.bytes=2147483648
```

## TiCDC 同步时，在下游执行 DDL 语句失败会有什么表现，如何恢复？

如果某条 DDL 语句执行失败，同步任务 (changefeed) 会自动停止，checkpoint-ts 断点时间戳为该条出错 DDL 语句的结束时间戳 (finish-ts) 减去一。如果希望让 TiCDC 在下游重试执行这条 DDL 语句，可以使用 `cdc cli changefeed resume` 恢复同步任务。例如：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed resume -c test-cf --pd=http://10.0.10.25:2379
```

如果希望跳过这条出错的 DDL 语句，可以将 changefeed 的 start-ts 设为报错时的 checkpoint-ts 加上一，然后通过 `cdc cli changefeed resume` 恢复同步任务。假设报错时的 checkpoint-ts 为 `415241823337054209`，可以进行如下操作来跳过该 DDL 语句：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed update -c test-cf --pd=http://10.0.10.25:2379 --start-ts 415241823337054210

cdc cli changefeed resume -c test-cf --pd=http://10.0.10.25:2379
```

## 同步 DDL 到下游 MySQL 5.7 时间类型字段默认值不一致

比如上游 TiDB 的建表语句为 `create table test (id int primary key, ts timestamp)`，TiCDC 同步该语句到下游 MySQL 5.7，MySQL 使用默认配置，同步得到的表结构如下所示，timestamp 字段默认值会变成 `CURRENT_TIMESTAMP`：

{{< copyable "sql" >}}

```sql
mysql root@127.0.0.1:test> show create table test;
+-------+----------------------------------------------------------------------------------+
| Table | Create Table                                                                     |
+-------+----------------------------------------------------------------------------------+
| test  | CREATE TABLE `test` (                                                            |
|       |   `id` int(11) NOT NULL,                                                         |
|       |   `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, |
|       |   PRIMARY KEY (`id`)                                                             |
|       | ) ENGINE=InnoDB DEFAULT CHARSET=latin1                                           |
+-------+----------------------------------------------------------------------------------+
1 row in set
```

产生表结构不一致的原因是 `explicit_defaults_for_timestamp` 的[默认值在 TiDB 和 MySQL 5.7 不同](/mysql-compatibility.md#默认设置)。从 TiCDC v5.0.1/v4.0.13 版本开始，同步到 MySQL 会自动设置 session 变量 `explicit_defaults_for_timestamp = ON`，保证同步时间类型时上下游行为一致。对于 v5.0.1/v4.0.13 以前的版本，同步时间类型时需要注意 `explicit_defaults_for_timestamp` 默认值不同带来的兼容性问题。
