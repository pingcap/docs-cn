---
title: TiCDC 故障处理
summary: 了解如何解决使用 TiCDC 时经常遇到的问题。
---

# TiCDC 故障处理

本文档总结了使用 TiCDC 过程中常见的运行故障及解决方案。

> **注意：**
>
> 本文档 `cdc cli` 命令中指定 TiCDC Server 地址为 `--server=http://127.0.0.1:8300`，在使用时需根据实际地址进行替换。

## TiCDC 同步任务出现中断

### 如何判断 TiCDC 同步任务出现中断？

- 通过 Grafana 检查同步任务的 `changefeed checkpoint` 监控项。注意选择正确的 `changefeed id`。如果该值不发生变化或者查看 `checkpoint lag` 是否不断增大，可能同步任务出现中断。
- 通过 Grafana 检查 `exit error count` 监控项，该监控项大于 0 代表同步任务出现错误。
- 通过 `cdc cli changefeed list` 和 `cdc cli changefeed query` 命令查看同步任务的状态信息。任务状态为 `stopped` 代表同步中断，`error` 项会包含具体的错误信息。任务出错后可以在 TiCDC server 日志中搜索 `error on running processor` 查看错误堆栈，帮助进一步排查问题。
- 部分极端异常情况下 TiCDC 出现服务重启，可以在 TiCDC server 日志中搜索 `FATAL` 级别的日志排查问题。

### 如何查看 TiCDC 同步任务是否被人为终止？

可以使用 `cdc cli` 查询同步任务是否被人为终止。例如：

```shell
cdc cli changefeed query --server=http://127.0.0.1:8300 --changefeed-id 28c43ffc-2316-4f4f-a70b-d1a7c59ba79f
```

上述命令的输出中 `state` 标志这个同步任务的状态，状态的值和含义参考 [TiCDC 同步任务状态](/ticdc/ticdc-changefeed-overview.md#changefeed-状态流转)。

### 如何处理 TiCDC 同步任务的中断？

目前已知可能发生的同步中断包括以下场景：

- 下游持续异常，TiCDC 多次重试后仍然失败。

    - 该场景下 TiCDC 会保存任务信息，由于 TiCDC 已经在 PD 中设置的 service GC safepoint，在 `gc-ttl` 的有效期内，同步任务 checkpoint 之后的数据不会被 TiKV GC 清理掉。
    - 处理方法：在下游恢复正常后，通过 `cdc cli changefeed resume` 恢复同步任务。

- 因下游存在不兼容的 SQL 语句，导致同步不能继续。

    - 该场景下 TiCDC 会保存任务信息，由于 TiCDC 已经在 PD 中设置的 service GC safepoint，在 `gc-ttl` 的有效期内，同步任务 checkpoint 之后的数据不会被 TiKV GC 清理掉。
    - 处理方法：
        1. 先通过 `cdc cli changefeed query` 查询同步任务状态信息，记录 `checkpoint-ts` 值。
        2. 使用新的任务配置文件，增加 `ignore-txn-start-ts` 参数跳过指定 `start-ts` 对应的事务。
        3. 通过 `cdc cli changefeed pause -c <changefeed-id>` 暂停同步任务。
        4. 通过 `cdc cli changefeed update -c <changefeed-id> --config <config-file-path>` 指定新的任务配置文件。
        5. 通过 `cdc cli changefeed resume -c <changefeed-id>` 恢复同步任务。

### 同步任务中断，尝试再次启动后 TiCDC 发生 OOM，应该如何处理？

升级 TiDB 集群和 TiCDC 集群到最新版本。该 OOM 问题在 **v4.0.14 及之后的 v4.0 版本，v5.0.2 及之后的 v5.0 版本，更新的版本**上已得到缓解。

## 如何处理 TiCDC 创建同步任务或同步到 MySQL 时遇到 `Error 1298: Unknown or incorrect time zone: 'UTC'` 错误？

这是因为下游 MySQL 没有加载时区，可以通过 [mysql_tzinfo_to_sql](https://dev.mysql.com/doc/refman/8.0/en/mysql-tzinfo-to-sql.html) 命令加载时区，加载后就可以正常创建任务或同步任务。

```shell
mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root mysql -p
```

显示类似于下面的输出则表示导入已经成功：

```shell
Enter password:
Warning: Unable to load '/usr/share/zoneinfo/iso3166.tab' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/leap-seconds.list' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/zone.tab' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/zone1970.tab' as time zone. Skipping it.
```

如果下游是特殊的 MySQL 环境（某种公有云 RDS 或某些 MySQL 衍生版本等），使用上述方式导入时区失败，则可以通过设置 `time-zone` 为空值来使用下游默认时区，例如：`time-zone=""`。

在 TiCDC 中使用时区时，建议显式指定时区，例如：`time-zone="Asia/Shanghai"`。同时，请确保 TiCDC Server 的 `tz` 时区配置、Sink URI 中的 `time-zone` 时区配置和下游数据库的时区配置保持一致。这样可以避免因时区不一致导致的数据不一致问题。

## 如何处理升级 TiCDC 后配置文件不兼容的问题？

请参阅[配置文件兼容注意事项](/ticdc/ticdc-compatibility.md#命令行参数和配置文件兼容性)。

## TiCDC 启动任务的 start-ts 时间戳与当前时间差距较大，任务执行过程中同步中断，出现错误 `[CDC:ErrBufferReachLimit]`，怎么办？

自 v4.0.9 起可以尝试开启 unified sorter 特性进行同步；或者使用 BR 工具进行一次增量备份和恢复，然后从新的时间点开启 TiCDC 同步任务。TiCDC 将会在后续版本中对该问题进行优化。

## 当 changefeed 的下游为类 MySQL 数据库时，TiCDC 执行了一个耗时较长的 DDL 语句，阻塞了所有其他 changefeed，应该怎样处理？

1. 首先暂停执行耗时较长的 DDL 的 changefeed。此时可以观察到，这个 changefeed 暂停后，其他的 changefeed 不再阻塞了。
2. 在 TiCDC log 中搜寻 `apply job` 字段，确认耗时较长的 DDL 的 `start-ts`。
3. 手动在下游执行该 DDL 语句，执行完毕后进行下面的操作。
4. 修改 changefeed 配置，将上述 `start-ts` 添加到 `ignore-txn-start-ts` 配置项中。
5. 恢复被暂停的 changefeed。

## TiCDC 集群升级到 v4.0.8 之后，changefeed 报错 `[CDC:ErrKafkaInvalidConfig]Canal requires old value to be enabled`，为什么？

自 v4.0.8 起，如果 changefeed 使用 `canal-json` 协议输出，TiCDC 会自动开启 Old Value 功能。但是，当 TiCDC 是从较旧版本升级到 v4.0.8 或以上版本时，在 changefeed 使用 `canal-json` 协议的同时 TiCDC 的 Old Value 功能会被禁用。此时，会出现该报错。可以按照以下步骤解决该报错：

1. 将 changefeed 配置文件中 `enable-old-value` 的值设为 `true`。
2. 使用 `cdc cli changefeed pause` 暂停同步任务。

    ```shell
    cdc cli changefeed pause -c test-cf --server=http://127.0.0.1:8300
    ```

3. 使用 `cdc cli changefeed update` 更新原有 changefeed 的配置。

    ```shell
    cdc cli changefeed update -c test-cf --server=http://127.0.0.1:8300 --sink-uri="mysql://127.0.0.1:3306/?max-txn-row=20&worker-number=8" --config=changefeed.toml
    ```

4. 使用 `cdc cli changefeed resume` 恢复同步任务。

    ```shell
    cdc cli changefeed resume -c test-cf --server=http://127.0.0.1:8300
    ```

## 使用 TiCDC 创建 changefeed 时报错 `[tikv:9006]GC life time is shorter than transaction duration, transaction starts at xx, GC safe point is yy`，该如何处理？

执行 `pd-ctl service-gc-safepoint --pd <pd-addrs>` 命令查询当前的 GC safepoint 与 service GC safepoint。如果 GC safepoint 小于 TiCDC changefeed 同步任务的开始时间戳 `start-ts`，可以直接在 `cdc cli create changefeed` 命令后加上 `--disable-gc-check` 参数创建 changefeed。

如果 `pd-ctl service-gc-safepoint --pd <pd-addrs>` 的结果中没有 `gc_worker service_id`：

- 如果 PD 的版本 <= v4.0.8，详见 [PD issue #3128](https://github.com/tikv/pd/issues/3128)。
- 如果 PD 是由 v4.0.8 或更低版本滚动升级到新版，详见 [PD issue #3366](https://github.com/tikv/pd/issues/3366)。
- 对于其他情况，请将上述命令执行结果反馈到 [AskTUG 论坛](https://asktug.com/tags/ticdc)。

## 使用 TiCDC 同步消息到 Kafka 时 Kafka 报错 `Message was too large`，该如何处理？

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

如果某条 DDL 语句执行失败，同步任务 (changefeed) 会自动停止，checkpoint-ts 断点时间戳为该条出错 DDL 语句的结束时间戳 (finish-ts)。如果希望让 TiCDC 在下游重试执行这条 DDL 语句，可以使用 `cdc cli changefeed resume` 恢复同步任务。例如：

```shell
cdc cli changefeed resume -c test-cf --server=http://127.0.0.1:8300
```

如果希望跳过这条出错的 DDL 语句，可以通过配置 `ignore-txn-start-ts` 参数跳过指定的 `start-ts` 对应的事务。例如：

1. 首先在 TiCDC 日志中搜寻 `apply job` 字段，确认耗时较长的 DDL 操作的 `start-ts`。
2. 修改 changefeed 配置，将上述 `start-ts` 添加到 `ignore-txn-start-ts` 配置项中。
3. 恢复被暂停的 changefeed。

> **注意：**
> 
> 虽然将 changefeed 的 `start-ts` 设为报错时的 `checkpoint-ts` 值加上 1，然后重建任务也可以跳过该 DDL 语句，但同时会导致 TiCDC 丢失 `checkpointTs+1` 时刻对应的 DML 数据变更。严禁在生产环境执行这样的操作。

```shell
cdc cli changefeed remove --server=http://127.0.0.1:8300 --changefeed-id simple-replication-task
cdc cli changefeed create --server=http://127.0.0.1:8300 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --changefeed-id="simple-replication-task" --sort-engine="unified" --start-ts 415241823337054210
```
