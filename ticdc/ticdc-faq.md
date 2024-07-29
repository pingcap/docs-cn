---
title: TiCDC 常见问题解答
summary: 了解 TiCDC 相关的常见问题。
---

# TiCDC 常见问题解答

本文档总结了使用 TiCDC 时经常遇到的问题。

> **注意：**
>
> 本文档 `cdc cli` 命令中指定 server 地址为 `--server=http://127.0.0.1:8300`，在使用时你需要根据实际地址进行替换。

## TiCDC 创建任务时如何选择 start-ts？

首先需要理解同步任务的 `start-ts` 对应于上游 TiDB 集群的一个 TSO，同步任务会从这个 TSO 开始请求数据。所以同步任务的 `start-ts` 需要满足以下两个条件：

- `start-ts` 的值需要大于 TiDB 集群当前的 `tikv_gc_safe_point`，否则创建任务时会报错。
- 启动任务时，需要保证下游已经具有 `start-ts` 之前的所有数据。对于同步到消息队列等场景，如果不需要保证上下游数据的一致，可根据业务场景放宽此要求。

如果不指定 `start-ts` 或者指定 `start-ts=0`，在启动任务的时候会去 PD 获取一个当前 TSO，并从该 TSO 开始同步。

## 为什么 TiCDC 创建任务时提示部分表不能同步？

在使用 `cdc cli changefeed create` 创建同步任务时会检查上游表是否符合[同步要求](/ticdc/ticdc-overview.md#最佳实践)。如果存在表不满足同步限制，会提示 `some tables are not eligible to replicate` 并列出这些不满足的表。如果选择 `Y` 或 `y` 则会继续创建同步任务，并且同步过程中自动忽略这些表的所有更新。如果选择其他输入，则不会创建同步任务。

## 如何查看 TiCDC 同步任务的状态？

可以使用 `cdc cli` 查询同步任务的状态。例如：

```shell
cdc cli changefeed list --server=http://127.0.0.1:8300
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
* `state` 为该同步任务的状态，状态的值和含义参考 [TiCDC 同步任务状态](/ticdc/ticdc-changefeed-overview.md#changefeed-状态流转)。

> **注意：**
>
> 该功能在 TiCDC 4.0.3 版本引入。

## TiCDC 的 `gc-ttl` 是什么？

从 TiDB v4.0.0-rc.1 版本起，PD 支持外部服务设置服务级别 GC safepoint。任何一个服务可以注册更新自己服务的 GC safepoint。PD 会保证任何晚于该 GC safepoint 的 KV 数据不会在 TiKV 中被 GC 清理掉。

在 TiCDC 中启用了这一功能，用来保证 TiCDC 在不可用、或同步任务中断情况下，可以在 TiKV 内保留 TiCDC 需要消费的数据不被 GC 清理掉。

启动 TiCDC server 时可以通过 `gc-ttl` 指定 GC safepoint 的 TTL，也可以[通过 TiUP 修改](/ticdc/deploy-ticdc.md#使用-tiup-变更-ticdc-集群配置) TiCDC 的 `gc-ttl`，默认值为 24 小时。在 TiCDC 中这个值有如下两重含义：

- 当 TiCDC 服务全部停止后，由 TiCDC 在 PD 所设置的 GC safepoint 保存的最长时间。
- TiCDC 中某个同步任务中断或者被手动停止时所能停滞的最长时间，若同步任务停滞时间超过 `gc-ttl` 所设置的值，那么该同步任务就会进入 `failed` 状态，无法被恢复，并且不会继续影响 GC safepoint 的推进。

以上第二种行为是在 TiCDC v4.0.13 版本及之后版本中新增的。目的是为了防止 TiCDC 中某个同步任务停滞时间过长，导致上游 TiKV 集群的 GC safepoint 长时间不推进，保留的旧数据版本过多，进而影响上游集群性能。

> **注意：**
>
> 在某些应用场景中，比如使用 Dumpling/BR 全量同步后使用 TiCDC 接增量同步时，默认的 `gc-ttl` 为 24 小时可能无法满足需求。此时应该根据实际情况，在启动 TiCDC server 时指定 `gc-ttl` 的值。

## TiCDC GC safepoint 的完整行为是什么？

TiCDC 服务启动后，如果有任务开始同步，TiCDC owner 会根据所有同步任务最小的 checkpoint-ts 更新到 PD service GC safepoint，service GC safepoint 可以保证该时间点及之后的数据不被 GC 清理掉。如果 TiCDC 中某个同步任务中断、或者被用户主动停止，则该任务的 checkpoint-ts 不会再改变，PD 对应的 service GC safepoint 最终会停滞在该任务的 checkpoint-ts 处不再更新。

如果该同步任务停滞的时间超过了 `gc-ttl` 指定的时长，那么该同步任务就会进入 `failed` 状态，并且无法被恢复，PD 对应的 service GC safepoint 就会继续推进。

TiCDC 为 service GC safepoint 设置的存活有效期为 24 小时，即 TiCDC 服务中断 24 小时内恢复能保证数据不因 GC 而丢失。

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
* 只同步包含[有效索引](/ticdc/ticdc-overview.md#最佳实践)的表

## TiCDC 是否支持输出 Canal 协议的变更数据？

支持。注意：对于 Canal 协议，TiCDC 只支持 JSON 输出格式，对 protobuf 格式尚未提供官方支持。要开启 Canal 协议的输出，只需在 `--sink-uri` 配置中指定 `protocol` 为 `canal-json` 即可。例如：

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --sink-uri="kafka://127.0.0.1:9092/cdc-test?kafka-version=2.4.0&protocol=canal-json" --config changefeed.toml
```

> **注意：**
>
> * 该功能在 TiCDC 4.0.2 版本引入。
> * 目前 TiCDC 仅支持将 Canal-JSON 格式的变更数据输出到 MQ 类的 Sink（例如 Kafka）。

更多信息请参考 [TiCDC Changefeed 配置参数](/ticdc/ticdc-changefeed-config.md)。

## 为什么 TiCDC 到 Kafka 的同步任务延时越来越大？

* 请参考[如何查看 TiCDC 同步任务的状态？](#如何查看-ticdc-同步任务的状态)检查下同步任务的状态是否正常。
* 请适当调整 Kafka 的以下参数：
    * `message.max.bytes`，将 Kafka 的 `server.properties` 中该参数调大到 `1073741824` (1 GB)。
    * `replica.fetch.max.bytes`，将 Kafka 的 `server.properties` 中该参数调大到 `1073741824` (1 GB)。
    * `fetch.message.max.bytes`，适当调大 `consumer.properties` 中该参数，确保大于 `message.max.bytes`。

## TiCDC 把数据同步到 Kafka 时，能在 TiDB 中控制单条消息大小的上限吗？

对于 Avro 和 Canal-JSON 格式，消息是以行变更为单位发送的，一条 Kafka Message 仅包含一条行变更。一般情况下，消息的大小不会超过 Kafka 单条消息上限，因此，一般不需要限制单条消息大小。如果单条 Kafka 消息大小确实超过 Kakfa 上限，请参考[为什么 TiCDC 到 Kafka 的同步任务延时越来越大](/ticdc/ticdc-faq.md#为什么-ticdc-到-kafka-的同步任务延时越来越大)。

对于 Open Protocol 格式，一条 Kafka Message 可能包含多条行变更。因此，有可能存在某条 Kafka Message 消息过大。可以通过 `max-message-bytes` 控制每次向 Kafka broker 发送消息的最大数据量（可选，默认值 10 MB），通过 `max-batch-size` 参数指定每条 kafka 消息中变更记录的最大数量（可选，默认值 `16`）。

## 在一个事务中对一行进行多次修改，TiCDC 会输出多条行变更事件吗？

不会，在进行事务操作时，对于在一个事务内多次修改同一行的情况，TiDB 仅会将最新一次的修改结果发送给 TiKV。因此 TiCDC 仅能获取到最新一次修改的结果。

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

## 如何区分 TiCDC Open Protocol 中的 Row Changed Event 是 `INSERT` 事件还是 `UPDATE` 事件？

如果没有开启 Old Value 功能，你无法区分 TiCDC Open Protocol 中的 Row Changed Event 是 `INSERT` 事件还是 `UPDATE` 事件。如果开启了 Old Value 功能，则可以通过事件中的字段判断事件类型：

* 如果同时存在 `"p"` 和 `"u"` 字段为 `UPDATE` 事件
* 如果只存在 `"u"` 字段则为 `INSERT` 事件
* 如果只存在 `"d"` 字段则为 `DELETE` 事件

更多信息请参考 [Open protocol Row Changed Event 格式定义](/ticdc/ticdc-open-protocol.md#row-changed-event)。

## TiCDC 占用多少 PD 的存储空间

TiCDC 使用 PD 内部的 etcd 来存储元数据并定期更新。因为 etcd 的多版本并发控制 (MVCC) 以及 PD 默认的 compaction 间隔是 1 小时，TiCDC 占用的 PD 存储空间与 1 小时内元数据的版本数量成正比。在 v4.0.5、v4.0.6、v4.0.7 三个版本中 TiCDC 存在元数据写入频繁的问题，如果 1 小时内有 1000 张表创建或调度，就会用尽 etcd 的存储空间，出现 `etcdserver: mvcc: database space exceeded` 错误。出现这种错误后需要清理 etcd 存储空间，参考 [etcd maintenance space-quota](https://etcd.io/docs/v3.4.0/op-guide/maintenance/#space-quota)。如果你的 TiCDC 版本为 v4.0.5、v4.0.6 或 v4.0.7，建议升级到 v4.0.9 及以后版本。

## TiCDC 支持同步大事务吗？有什么风险吗？

TiCDC 对大事务（大小超过 5 GB）提供部分支持，根据场景不同可能存在以下风险：

- 可能导致主从同步延迟大幅增高。
- 当 TiCDC 内部处理能力不足时，可能出现同步任务报错 `ErrBufferReachLimit`。
- 当 TiCDC 内部处理能力不足或 TiCDC 下游吞吐能力不足时，可能出现内存溢出 (OOM)。

从 v6.2 版本开始，TiCDC 支持拆分单表事务功能，可大幅降低同步大事务的延时和内存消耗。因此，在业务对事务原子性要求不高的场景下，建议通过设置 sink uri 参数 [`transaction-atomicity`](/ticdc/ticdc-sink-to-mysql.md#sink-uri-配置-mysqltidb) 打开拆分事务功能以解决可能出现的同步延迟和 OOM 问题。

如果实际同步过程中仍然遇到了上述错误，建议将包含大事务部分的增量数据通过 BR 进行增量恢复，具体操作如下：

1. 记录因为大事务而终止的 changefeed 的 `checkpoint-ts`，将这个 TSO 作为 BR 增量备份的 `--lastbackupts`，并执行[增量备份](/br/br-incremental-guide.md#对集群进行增量备份)。
2. 增量备份结束后，可以在 BR 日志输出中找到类似 `["Full backup Failed summary : total backup ranges: 0, total success: 0, total failed: 0"] [BackupTS=421758868510212097]` 的日志，记录其中的 `BackupTS`。
3. 执行[增量恢复](/br/br-incremental-guide.md#恢复增量备份数据)。
4. 建立一个新的 changefeed，从 `BackupTS` 开始同步任务。
5. 删除旧的 changefeed。

## 同步 DDL 到下游 MySQL 5.7 时为什么时间类型字段默认值不一致？

比如上游 TiDB 的建表语句为 `create table test (id int primary key, ts timestamp)`，TiCDC 同步该语句到下游 MySQL 5.7，MySQL 使用默认配置，同步得到的表结构如下所示，timestamp 字段默认值会变成 `CURRENT_TIMESTAMP`：

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

## 使用 TiCDC 创建同步任务时将 `safe-mode` 设置为 `true` 后，为什么上游的 `INSERT`/`UPDATE` 语句经 TiCDC 同步到下游后变为了 `REPLACE INTO`？

TiCDC 提供至少一次的数据同步保证，当下游有重复数据时，会引起写冲突。为了避免该问题，TiCDC 会将 `INSERT` 和 `UPDATE` 语句转成 `REPLACE INTO` 语句。该行为由 `safe-mode` 参数来控制。

在 v6.1.3 版本之前，`safe-mode` 默认为 `true`，即所有的 `INSERT` 和 `UPDATE` 语句都转成 `REPLACE INTO` 语句。在 v6.1.3 及之后版本，系统能自动判断下游是否存在重复数据，`safe-mode` 默认更改为 `false`，当系统判断下游无重复数据时，会直接同步 `INSERT` 和 `UPDATE` 语句。

## 数据同步下游的 Sink 为 TiDB 或 MySQL 时，下游数据库的用户需要哪些权限？

Sink 为 TiDB 或 MySQL 时，下游数据库的用户需要以下权限：

- `Select`
- `Index`
- `Insert`
- `Update`
- `Delete`
- `Create`
- `Drop`
- `Alter`
- `Create View`

如果要同步 `recover table` 到下游 TiDB，需要有 `Super` 权限。

## 为什么 TiCDC 需要使用磁盘，什么时候会写磁盘，TiCDC 能否利用内存缓存提升同步性能？

TiCDC 需要磁盘是为了缓冲上游写入高峰时下游消费不及时堆积的数据。TiCDC 正常运行期间都需要写入磁盘，但这通常不是同步吞吐和同步延时的瓶颈，写磁盘对延时影响在百毫秒内。TiCDC 也利用了内存来提升加速读取磁盘中的数据，以提升同步性能。

## 为什么在上游使用了 TiDB Lightning 和 BR 恢复了数据之后，TiCDC 同步会出现卡顿甚至卡住？

目前 TiCDC 尚未完全适配 TiDB Lightning 和 BR，请避免在使用 TiCDC 同步的表上使用 TiDB Lightning 和 BR。否则，可能会出现未知的错误，例如 TiCDC 同步卡住、同步延迟大幅增加、或者同步数据丢失。

如果有某些使用 TiCDC 同步的表需要使用 TiDB Lightning 或者 BR 恢复数据，可以这么做：

1. 删除涉及这些表的 TiCDC 同步任务。

2. 使用 TiDB Lightning 或 BR 在 TiCDC 的上游集群和下游集群分别恢复数据。

3. 恢复完成并检查了上下游集群对应表的数据一致性之后，使用上游备份的时间点 (TSO) 作为 TiCDC 同步任务的 `start-ts`，创建新的 TiCDC 同步任务，进行增量同步。例如，假设上游集群的 BR 备份的 snapshot 时间点为 `431434047157698561`，那么可以使用以下命令创建新的 TiCDC 同步任务：

    ```shell
    cdc cli changefeed create -c "upstream-to-downstream-some-tables" --start-ts=431434047157698561 --sink-uri="mysql://root@127.0.0.1:4000? time-zone="
    ```

## 为什么恢复暂停的 changefeed 后，changefeed 同步延迟越来越高，数分钟后才恢复正常？

当 changefeed 启动时，为了补齐 changefeed 暂停期间产生的增量数据日志，TiCDC 需要扫描 TiKV 中数据的历史版本，待扫描完毕后，才能够继续推进复制过程，扫描过程可能长达数分钟到数十分钟。

## 在两个异地 TiDB 集群之间同步数据，如何部署 TiCDC？

对于 v6.5.2 之前的版本，建议将 TiCDC 部署在下游 TiDB 集群。这是因为，如果上下游网络延迟较大，例如超过 100 ms 时，由于 MySQL 传输协议的原因，TiCDC 向下游执行 SQL 的延迟会急剧增加，导致系统的吞吐下降。部署在下游能够极大缓解该问题。经过优化后，v6.5.2 及之后的版本建议将 TiCDC 部署在上游集群。

## 如何理解 DML 和 DDL 语句之间的执行顺序？

目前，TiCDC 采用了以下执行顺序：

1. TiCDC 阻塞受 DDL 影响的表的同步进度，直到 DDL `commitTS` 的时间点，以确保在 DDL `commitTS` 之前执行的 DML 先成功同步到下游。
2. TiCDC 继续同步 DDL。当存在多个 DDL 时，TiCDC 是以串行的方式进行同步的。
3. 当 DDL 在下游执行完成之后，TiCDC 继续同步 DDL `commitTS` 之后执行的 DML。

## 如何对比上下游数据的一致性？

如果下游是 TiDB 集群或者 MySQL，我们推荐使用 [sync diff inspector](/sync-diff-inspector/sync-diff-inspector-overview.md) 工具进行数据对比。

## 单表数据同步只能在一个 TiCDC 节点上运行，TiCDC 是否考虑使用多个节点同步多表数据？

目前正在开发中，未来 TiCDC 会支持按照 TiKV Region 粒度来同步数据变更日志，实现处理能力上的可扩展性。

## 上游有运行时间比较长的未提交事务，TiCDC 同步是否会被卡住？

TiDB 有事务超时的机制，当事务运行超过 [`max-txn-ttl`](/tidb-configuration-file.md#max-txn-ttl) 后，会被 TiDB 强制回滚。TiCDC 遇到未提交的事务，会等待其提交后再继续同步其数据，因此会出现同步延迟。

## TiCDC 在开启 Old Value 功能后更新事件格式有何变化？

在下面的说明中，有效索引的定义如下：

- 主键 (`PRIMARY KEY`) 为有效索引。
- 唯一索引 (`UNIQUE INDEX`) 中每一列在表结构中明确定义非空 (`NOT NULL`) 且不存在虚拟生成列 (`VIRTUAL GENERATED COLUMNS`)。

聚簇索引指的是 TiDB 从 v5.0 开始支持的特性，用于控制含有主键的表数据的存储方式。详见[聚簇索引](/clustered-indexes.md)。

在开启 [Old Value 功能](/ticdc/ticdc-manage-changefeed.md#输出行变更的历史值-从-v405-版本开始引入)后，TiCDC 的表现如下：

- 对于非有效索引列的更新事件，输出的数据中会同时包含新值和旧值。
- 对于有效索引列的更新事件，输出的数据视不同情况而定：
    - 更新唯一索引列 (`UNIQUE INDEX`)，并且该表不存在主键时，输出的数据中会同时包含新值和旧值。
    - 当上游 TiDB 集群未开启聚簇索引，更新非 INT 类型的主键列时，输出的数据中会同时包含新值和旧值。
    - 在其他情况下，更新事件会被拆分为对旧数据的删除事件和对新数据的插入事件。

以上行为的变化可能导致以下问题：

### 当更新有效索引列的事件同时包含新值和旧值时，Kafka Sink 的分发行为可能无法保证将具有相同索引列的更新事件分发到同一分区

Kafka Sink 的 index-value 分发行为是根据索引列的值来分发的。当更新事件同时包含新值和旧值时，索引列的值会发生变化，从而导致相同索引列的更新事件被分发到不同的分区。下面是一个示例：

在关闭 TiDB 聚簇索引功能时，创建表 `t`：

```sql
CREATE TABLE t (a VARCHAR(255) PRIMARY KEY NONCLUSTERED);
```

执行如下 DML 语句：

```sql
INSERT INTO t VALUES ("2");
UPDATE t SET a="1" WHERE a="2";
INSERT INTO t VALUES ("2");
UPDATE t SET a="3" WHERE a="2";
```

- 在未开启 Old Value 功能时，更新事件被拆分为删除旧值事件和插入新值事件。Kafka Sink 的 index-value 分发模式针对每个事件计算相应的分区。上述 DML 产生的事件会被发送到如下分区：

    | partition-1  | partition-2  | partition-3  |
    | ------------ | ------------ | ------------ |
    | INSERT a = 2 | INSERT a = 1 | INSERT a = 3 |
    | DELETE a = 2 |              |              |
    | INSERT a = 2 |              |              |
    | DELETE a = 2 |              |              |

    因为 Kafka 的每个分区内可以保证消息的顺序，Kafka 消费者可以独立地消费每个分区中的数据，最终结果和 DML 执行顺序相同。

- 在开启 Old Value 功能时，Kafka Sink 的 index-value 分发模式会将相同索引列的更新事件分发到不同的分区。因此上述 DML 会被分发到如下分区（更新事件同时包含新值和旧值）：

    | partition-1  | partition-2              | partition-3              |
    | ------------ | ------------------------ | ------------------------ |
    | INSERT a = 2 | UPDATE a = 1 WHERE a = 2 | UPDATE a = 3 WHERE a = 2 |
    | INSERT a = 2 |                          |                          |

    因为 Kafka 的各个分区之间不能保证消息的顺序，因此上述 DML 在消费过程中可能无法保证索引列的更新顺序。如果需要在输出的数据中会同时包含新值和旧值时保证索引列的更新顺序，建议在开启 Old Value 功能时，使用 default 分发模式。

### 对于非有效索引列的更新事件和有效索引列的更新事件同时包含新值和旧值时，Kafka Sink 的 Avro 格式无法正确输出旧值

在 Avro 实现中，Kafka 消息的 Value 格式只包含当前列值，因此当一个事件既有新值也有旧值时，无法正确输出旧值。如果需要输出旧值，建议关闭 Old Value 功能以获取拆分后的删除和插入事件。

### 对于非有效索引列的更新事件和有效索引列的更新事件同时包含新值和旧值时，Cloud Storage Sink 的 CSV 格式无法正确输出旧值

因为 CSV 文件的列数是固定的，当一个事件既有新值也有旧值时，无法正确输出旧值。如果需要输出旧值，建议使用 Canal-JSON 格式。

## 为什么通过 TiDB Operator 部署的 TiCDC 集群无法使用 cdc cli 命令进行操作？

因为通过 TiDB Operator 部署的 TiCDC 集群的默认端口号为 8301, 而 cdc cli 命令默认连接的 cdc 服务器的端口号是 8300。在使用 cdc cli 操作 TiCDC 集群时，你需要显式地指定 `--server` 参数，如下：

```shell
./cdc cli changefeed list --server "127.0.0.1:8301"
[
  {
    "id": "4k-table",
    "namespace": "default",
    "summary": {
      "state": "stopped",
      "tso": 441832628003799353,
      "checkpoint": "2023-05-30 22:41:57.910",
      "error": null
    }
  },
  {
    "id": "big-table",
    "namespace": "default",
    "summary": {
      "state": "normal",
      "tso": 441872834546892882,
      "checkpoint": "2023-06-01 17:18:13.700",
      "error": null
    }
  }
]
```
