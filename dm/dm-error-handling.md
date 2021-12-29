---
title: 故障及处理方法
summary: 了解 DM 的错误系统及常见故障的处理方法。
aliases: ['/docs-cn/tidb-data-migration/dev/error-handling/','/docs-cn/tidb-data-migration/dev/troubleshoot-dm/','/docs-cn/tidb-data-migration/dev/error-system/']
---

# 故障及处理方法

本文档介绍 DM 的错误系统及常见故障的处理方法。

## DM 错误系统

在 DM 的错误系统中，对于一条特定的错误，通常主要包含以下信息：

- `code`：错误码。

    同一种错误都使用相同的错误码。错误码不随 DM 版本改变。

    在 DM 迭代过程中，部分错误可能会被移除，但错误码不会。新增的错误会使用新的错误码，不会复用已有的错误码。

- `class`：发生错误的类别。

    用于标记出现错误的系统子模块。

    下表展示所有的错误类别、错误对应的系统子模块、错误样例：

    |  <div style="width: 100px;">错误类别</div>    | 错误对应的系统子模块             | 错误样例                                                     |
    | :-------------- | :------------------------------ | :------------------------------------------------------------ |
    | `database`       | 执行数据库操作出现错误         | `[code=10003:class=database:scope=downstream:level=medium] database driver: invalid connection` |
    | `functional`     | 系统底层的基础函数错误           | `[code=11005:class=functional:scope=internal:level=high] not allowed operation: alter multiple tables in one statement` |
    | `config`         | 配置错误                       | `[code=20005:class=config:scope=internal:level=medium] empty source-id not valid` |
    | `binlog-op`      | binlog 操作出现错误            | `[code=22001:class=binlog-op:scope=internal:level=high] empty UUIDs not valid` |
    | `checkpoint`     | checkpoint 相关操作出现错误    | `[code=24002:class=checkpoint:scope=internal:level=high] save point bin.1234 is older than current pos bin.1371` |
    | `task-check`     | 进行任务检查时出现错误       | `[code=26003:class=task-check:scope=internal:level=medium] new table router error` |
    | `relay-event-lib`| 执行 relay 模块基础功能时出现错误 | `[code=28001:class=relay-event-lib:scope=internal:level=high] parse server-uuid.index` |
    | `relay-unit`     | relay 处理单元内出现错误     | `[code=30015:class=relay-unit:scope=upstream:level=high] TCPReader get event: ERROR 1236 (HY000): Could not open log file` |
    | `dump-unit`      | dump 处理单元内出现错误      | `[code=32001:class=dump-unit:scope=internal:level=high] mydumper runs with error: CRITICAL **: 15:12:17.559: Error connecting to database: Access denied for user 'root'@'172.17.0.1' (using password: NO)` |
    | `load-unit`      | load 处理单元内出现错误      | `[code=34002:class=load-unit:scope=internal:level=high] corresponding ending of sql: ')' not found` |
    | `sync-unit`      | sync 处理单元内出现错误      | `[code=36027:class=sync-unit:scope=internal:level=high] Column count doesn't match value count: 9 (columns) vs 10 (values)` |
    | `dm-master`      | DM-master 服务内部出现错误   | `[code=38008:class=dm-master:scope=internal:level=high] grpc request error: rpc error: code = Unavailable desc = all SubConns are in TransientFailure, latest connection error: connection error: desc = "transport: Error while dialing dial tcp 172.17.0.2:8262: connect: connection refused"` |
    | `dm-worker`      | DM-worker 服务内部出现错误   | `[code=40066:class=dm-worker:scope=internal:level=high] ExecuteDDL timeout, try use query-status to query whether the DDL is still blocking` |
    | `dm-tracer`      | DM-tracer 服务内部出现错误   | `[code=42004:class=dm-tracer:scope=internal:level=medium] trace event test.1 not found` |
    | `schema-tracker` | 增量复制时记录 schema 变更出现错误   | `[code=44006:class=schema-tracker:scope=internal:level=high],"cannot track DDL: ALTER TABLE test DROP COLUMN col1"` |
    | `scheduler`      | 数据迁移任务调度相关操作出错操作   | `[code=46001:class=scheduler:scope=internal:level=high],"the scheduler has not started"` |
    | `dmctl`          | dmctl 内部或与其他组件交互出现错误   | `[code=48001:class=dmctl:scope=internal:level=high],"can not create grpc connection"` |

- `scope`：错误作用域。

    用于标识错误发生时 DM 作用对象的范围和来源，包括未设置 (`not-set`)、上游数据库 (`upstream`)、下游数据库 (`downstream`)、内部 (`internal`) 四种类型。

    如果错误发生的逻辑直接涉及到上下游数据库请求，作用域会设置为 `upstream` 或 `downstream`，其他出错场景目前都设置为 `internal`。

- `level`：错误级别。

    错误的严重级别，包括低级别 (`low`)、中级别 (`medium`)、高级别 (`high`) 三种。

    低级别通常是用户操作、输入错误，不影响正常迁移任务；中级别通常是用户配置等错误，会影响部分新启动服务，不影响已有系统迁移状态；高级别通常是用户需要关注的一些错误，可能存在迁移任务中断等风险，需要用户进行处理。

- `message`：错误描述。

    错误的详细描述信息。对于错误调用链上每一层额外增加的错误 message，采用 [errors.Wrap](https://godoc.org/github.com/pkg/errors#hdr-Adding_context_to_an_error) 的模式来叠加和保存错误 message。wrap 最外层的 message 是 DM 内部对该错误的描述，wrap 最内层的 message 是该错误最底层出错位置的错误描述。

- `workaround`: 错误处理方法（可选）。

    对该错误的处理方法。对于部分明确的错误（如：配置信息错误等），DM 会在 `workaround` 中给出相应的人为处理方法。

- 错误堆栈信息（可选）。

    DM 根据错误的严重程度和必要性来选择是否输出错误堆栈。错误堆栈记录了错误发生时完整的堆栈调用信息。如果用户通过错误基本信息和错误 message 描述不能完全诊断出错误发生的原因，可以通过错误堆栈进一步跟进出错时代码的运行路径。

可在 DM 代码仓库 [已发布的错误码](https://github.com/pingcap/dm/blob/master/_utils/terror_gen/errors_release.txt) 中查询完整的错误码列表。

## DM 故障诊断

如果在运行 DM 工具时出现了错误，请尝试以下解决方案：

1. 执行 `query-status` 命令查看任务运行状态以及相关错误输出。

2. 查看与该错误相关的日志文件。日志文件位于 DM-master、DM-worker 部署节点上，通过 [DM 错误系统](#dm-错误系统) 获取错误的关键信息，然后查看 [常见故障处理方法](#常见故障处理方法)以寻找相应的解决方案。

3. 如果该错误还没有相应的解决方案，并且你无法通过查询日志或监控指标自行解决此问题，你可以联系相关技术支持人员。

4. 一般情况下，错误处理完成后，只需使用 dmctl 重启任务即可。

    {{< copyable "shell-regular" >}}

    ```bash
    resume-task ${task name}
    ```

但在某些情况下，你还需要重置数据迁移任务。有关何时需要重置以及如何重置，详见[重置数据迁移任务](/dm/dm-faq.md#如何重置数据迁移任务)。

## 常见故障处理方法

| <div style="width: 100px;">错误码</div>       | 错误说明                                                     | 解决方法                                                     |
| :----------- | :------------------------------------------------------------ | :----------------------------------------------------------- |
| `code=10001` | 数据库操作异常                                               | 进一步分析错误信息和错误堆栈                                 |
| `code=10002` | 数据库底层的 `bad connection` 错误，通常表示 DM 到下游 TiDB 的数据库连接出现了异常（如网络故障、TiDB 重启等）且当前请求的数据暂时未能发送到 TiDB。 | DM 提供针对此类错误的自动恢复。如果长时间未恢复，需要用户检查网络或 TiDB 状态。 |
| `code=10003` | 数据库底层 `invalid connection` 错误，通常表示 DM 到下游 TiDB 的数据库连接出现了异常（如网络故障、TiDB 重启、TiKV busy 等）且当前请求已有部分数据发送到了 TiDB。 | DM 提供针对此类错误的自动恢复。如果未能正常恢复，需要用户进一步检查错误信息并根据具体场景进行分析。 |
| `code=10005` | 数据库查询类语句出错                                         |                                                              |
| `code=10006` | 数据库 `EXECUTE` 类型语句出错，包括 DDL 和 `INSERT`/`UPDATE`/`DELETE` 类型的 DML。更详细的错误信息可通过错误 message 获取。错误 message 中通常包含操作数据库所返回的错误码和错误信息。 |                                                              |
| `code=11006` |  DM 内置的 parser 解析不兼容的 DDL 时出错              |  可参考 [Data Migration 故障诊断-处理不兼容的 DDL 语句](/dm/dm-faq.md#如何处理不兼容的-ddl-语句) 提供的解决方案 |
| `code=20010` | 处理任务配置时，解密数据库的密码出错                             |  检查任务配置中提供的下游数据库密码是否有[使用 dmctl 正确加密](/dm/dm-manage-source.md#加密数据库密码) |
| `code=26002` | 任务检查创建数据库连接失败。更详细的错误信息可通过错误 message 获取。错误 message 中包含操作数据库所返回的错误码和错误信息。 |  检查 DM-master 所在的机器是否有权限访问上游 |
| `code=32001` | dump 处理单元异常                                            | 如果报错 `msg` 包含 `mydumper: argument list too long.`，则需要用户根据 block-allow-list，在 `task.yaml` 的 dump 处理单元的 `extra-args` 参数中手动加上 `--regex` 正则表达式设置要导出的库表。例如，如果要导出所有库中表名字为 `hello` 的表，可加上 `--regex '.*\\.hello$'`，如果要导出所有表，可加上 `--regex '.*'`。 |
| `code=38008` | DM 组件间的 gRPC 通信出错                                      |  检查 `class`， 定位错误发生在哪些组件的交互环节，根据错误 message 判断是哪类通信错误。如果是 gRPC 建立连接出错，可检查通信服务端是否运行正常。 |

### 迁移任务中断并包含 `invalid connection` 错误

#### 原因

发生 `invalid connection` 错误时，通常表示 DM 到下游 TiDB 的数据库连接出现了异常（如网络故障、TiDB 重启、TiKV busy 等）且当前请求已有部分数据发送到了 TiDB。

#### 解决方案

由于 DM 中存在迁移任务并发向下游复制数据的特性，因此在任务中断时可能同时包含多个错误（可通过 `query-status` 查询当前错误）。

- 如果错误中仅包含 `invalid connection` 类型的错误且当前处于增量复制阶段，则 DM 会自动进行重试。
- 如果 DM 由于版本问题等未自动进行重试或自动重试未能成功，则可尝试先使用 `stop-task` 停止任务，然后再使用 `start-task` 重启任务。

### 迁移任务中断并包含 `driver: bad connection` 错误

#### 原因

发生 `driver: bad connection` 错误时，通常表示 DM 到下游 TiDB 的数据库连接出现了异常（如网络故障、TiDB 重启等）且当前请求的数据暂时未能发送到 TiDB。

#### 解决方案

当前版本 DM 会自动进行重试，如果由于版本问题等未自动重试，可先使用 `stop-task` 停止任务后再使用 `start-task` 重启任务。

### relay 处理单元报错 `event from * in * diff from passed-in event *` 或迁移任务中断并包含 `get binlog error ERROR 1236 (HY000)`、`binlog checksum mismatch, data may be corrupted` 等 binlog 获取或解析失败错误

#### 原因

在 DM 进行 relay log 拉取与增量复制过程中，如果遇到了上游超过 4GB 的 binlog 文件，就可能出现这两个错误。

原因是 DM 在写 relay log 时需要依据 binlog position 及文件大小对 event 进行验证，且需要保存迁移的 binlog position 信息作为 checkpoint。但是 MySQL binlog position 官方定义使用 uint32 存储，所以超过 4G 部分的 binlog position 的 offset 值会溢出，进而出现上面的错误。

#### 解决方案

对于 relay 处理单元，可通过以下步骤手动恢复：

1. 在上游确认出错时对应的 binlog 文件的大小超出了 4GB。
2. 停止 DM-worker。
3. 将上游对应的 binlog 文件复制到 relay log 目录作为 relay log 文件。
4. 更新 relay log 目录内对应的 `relay.meta` 文件以从下一个 binlog 开始拉取。如果 DM worker 已开启 `enable_gtid`，那么在修改 `relay.meta` 文件时，同样需要修改下一个 binlog 对应的 GTID。如果未开启 `enable_gtid` 则无需修改 GTID。

    例如：报错时有 `binlog-name = "mysql-bin.004451"` 与 `binlog-pos = 2453`，则将其分别更新为 `binlog-name = "mysql-bin.004452"` 和 `binlog-pos = 4`，同时更新 `binlog-gtid = "f0e914ef-54cf-11e7-813d-6c92bf2fa791:1-138218058"`。

5. 重启 DM-worker。

对于 binlog replication 处理单元，可通过以下步骤手动恢复：

1. 在上游确认出错时对应的 binlog 文件的大小超出了 4GB。
2. 通过 `stop-task` 停止迁移任务。
3. 将下游 `dm_meta` 数据库中 global checkpoint 与每个 table 的 checkpoint 中的 `binlog_name` 更新为出错的 binlog 文件，将 `binlog_pos` 更新为已迁移过的一个合法的 position 值，比如 4。

    例如：出错任务名为 `dm_test`，对应的 `source-id` 为 `replica-1`，出错时对应的 binlog 文件为 `mysql-bin|000001.004451`，则执行 `UPDATE dm_test_syncer_checkpoint SET binlog_name='mysql-bin|000001.004451', binlog_pos = 4 WHERE id='replica-1';`。

4. 在迁移任务配置中为 `syncers` 部分设置 `safe-mode: true` 以保证可重入执行。
5. 通过 `start-task` 启动迁移任务。
6. 通过 `query-status` 观察迁移任务状态，当原造成出错的 relay log 文件迁移完成后，即可还原 `safe-mode` 为原始值并重启迁移任务。

### 执行 `query-status` 或查看日志时出现 `Access denied for user 'root'@'172.31.43.27' (using password: YES)`

在所有 DM 配置文件中，数据库相关的密码都推荐使用经 dmctl 加密后的密文（若数据库密码为空，则无需加密）。有关如何使用 dmctl 加密明文密码，参见[使用 dmctl 加密数据库密码](/dm/dm-manage-source.md#加密数据库密码)。

此外，在 DM 运行过程中，上下游数据库的用户必须具备相应的读写权限。在启动迁移任务过程中，DM 会自动进行相应权限的前置检查，详见[上游 MySQL 实例配置前置检查](/dm/dm-precheck.md)。

### load 处理单元报错 `packet for query is too large. Try adjusting the 'max_allowed_packet' variable`

#### 原因

* MySQL client 和 MySQL/TiDB Server 都有 `max_allowed_packet` 配额的限制，如果在使用过程中违反其中任何一个 `max_allowed_packet` 配额，客户端程序就会收到对应的报错。目前最新版本的 DM 和 TiDB Server 的默认 `max_allowed_packet` 配额都为 `64M`。

* DM 的全量数据导入处理模块不支持对 dump 处理模块导出的 SQL 文件进行切分。

#### 解决方案

* 推荐在 DM 的 dump 处理单元提供的配置 `extra-args` 中设置 `statement-size`:

    依据默认的 `--statement-size` 设置，DM 的 dump 处理单元默认生成的 `Insert Statement` 大小一般会在 `1M` 左右，使用默认值就可以确保绝大部分情况 load 处理单元不会报错 `packet for query is too large. Try adjusting the 'max_allowed_packet' variable`。

    有时候在 dump 过程中会出现下面的 `WARN` log。这个 `WARN` log 不影响 dump 的过程，只是说明 dump 的表可能是宽表。

    ```
    Row bigger than statement_size for xxx
    ```

* 如果宽表的单行超过了 `64M`，需要修改以下两项配置，并且确保其生效。

    * 在 TiDB Server 执行 `set @@global.max_allowed_packet=134217728` （`134217728 = 128M`）

    * 根据实际情况为 DM 的任务配置文件中的 `target-database` 增加配置 `max-allowed-packet: 134217728` (128M)，执行 `stop-task` 后再重新 `start-task`。
