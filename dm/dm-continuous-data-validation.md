---
title: DM 增量数据校验
summary: 了解增量数据校验的原理，以及如何使用增量数据校验功能。
---

# DM 增量数据校验

> **警告：**
>
> 增量数据校验目前是实验性功能，不建议在生产环境中使用。

本文介绍了如何使用 DM 增量数据校验功能、DM 增量数据校验的原理以及相关的使用限制。

## 使用场景

在将增量数据从上游迁移到下游数据库的过程中，数据的流转有小概率导致错误或者丢失的情况。对于需要依赖于强数据一致的场景，如信贷、证券等业务，你可以在数据迁移完成之后对数据进行全量校验，确保数据的一致性。然而，在某些增量复制的业务场景下，上游和下游的写入是持续的、不会中断的，因为上下游的数据在不断变化，导致用户难以对表里面的全部数据进行一致性校验（例如使用 [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md)）。

在增量数据复制的场景下，你可以使用 DM 的增量校验功能，**在数据持续写入下游的增量复制过程中确保迁移数据的完整性、一致性**。

## 开启增量数据校验

你可以使用下面任意方法开启增量数据校验：

- 在任务配置中开启
- 通过 dmctl 开启

### 方法 1：在任务配置中开启

你可以在任务配置文件中加入以下内容来开启增量数据校验：

```yaml
# 给需要开启增量校验功能的上游数据库添加增量校验配置
mysql-instances:
  - source-id: "mysql1"
    block-allow-list: "bw-rule-1"
    validator-config-name: "global"
validators:
  global:
    mode: full # 也可以是 fast，默认是 none，即不开启校验
    worker-count: 4 # 后台校验的 validation worker 数量，默认是 4 个
    row-error-delay: 30m # 某一行多久没有验证通过会被标记为 error row，默认是 30m，即 30 分钟
```

示例中各配置项的含义如下：

* `mode`：校验模式，可以是 `none`、`full`、`fast`。
    * `none`：默认值，即不开启校验。
    * `full`：将变动行和下游数据库中获取的行数据进行每列对比。
    * `fast`：只判断这一行在下游数据库是否存在。
* `worker-count`：增量校验功能使用的 worker 数量（每个 worker 都是一个 goroutine）。
* `row-error-delay`：某一行多久没有验证通过会被标记为 error row，默认是 30 分钟。

完整配置请查阅 [DM 任务完整配置文件](/dm/task-configuration-file-full.md)。

### 方法 2：通过 dmctl 开启

你可以使用 `dmctl validation start` 命令来开启增量数据校验：

```
Usage:
  dmctl validation start [--all-task] [task-name] [flags]

Flags:
      --all-task            whether applied to all tasks
  -h, --help                help for start
      --mode string         specify the mode of validation: full (default), fast; this flag will be ignored if the validation task has been ever enabled but currently paused (default "full")
      --start-time string   specify the start time of binlog for validation, e.g. '2021-10-21 00:01:00' or 2021-10-21T00:01:00
```

* `--mode`：指定开启的模式，可以是 fast 或者 full。
* `--start-time`：指定 validator 开启校验的位置，格式是：2021-10-21 00:01:00 或者 2021-10-21T00:01:00。
* `task-name`：需要开启增量数据校验的任务名，你也可以用 `--all-task` 来为当前所有任务开启增量数据校验。

示例：

```shell
dmctl --master-addr=127.0.0.1:8261 validation start --start-time 2021-10-21T00:01:00 --mode full my_dm_task
```

## 使用增量数据校验

在使用增量数据校验时，通过 dmctl 工具，你可以查询到增量校验当前的校验状态，也可以对校验出的错误行（error row）进行及时处理。所谓的错误行，就是在增量校验过程中，被检查出上下游数据不一致的行。

### 查看增量校验的状态

你可以使用两种方式查看增量校验的状态。

方式 1：用 `dmctl query-status <task-name>` 命令查看任务状态，如果开启了增量校验，校验结果会显示在每个 subtask 的 validation 字段里面。示例输出：

```json
"subTaskStatus": [
    {
        "name": "test",
        "stage": "Running",
        "unit": "Sync",
        "result": null,
        "unresolvedDDLLockID": "",
        "sync": {
            ...
        },
        "validation": {
            "task": "test", // 任务名
            "source": "mysql-01", // source id
            "mode": "full", // 校验模式
            "stage": "Running", // 当前状态，Running 或者 Stopped
            "validatorBinlog": "(mysql-bin.000001, 5989)", // 校验到的 binlog 位置
            "validatorBinlogGtid": "1642618e-cf65-11ec-9e3d-0242ac110002:1-30", // 同上，用 GTID 表示
            "result": null, // 当增量校验异常时，显示异常信息
            "processedRowsStatus": "insert/update/delete: 0/0/0", // 已经处理的 binlog 数据行的统计信息
            "pendingRowsStatus": "insert/update/delete: 0/0/0", // 还未校验或者校验失败，但还没标记为`错误行`的数据行统计信息
            "errorRowsStatus": "new/ignored/resolved: 0/0/0" // `错误行`统计信息，三种状态的错误会在下文讲解
        }
    }
]
```

方式 2：使用 `dmctl validation status <taskname>` 来查询增量校验的状态：

```
dmctl validation status [--table-stage stage] <task-name> [flags]
Flags:
  -h, --help                 help for status
      --table-stage string   filter validation tables by stage: running/stopped
```

在上述命令中，你可以设置 `--table-stage` 来过滤正在校验或者已经停止校验的表。示例输出：

```json
{
    "result": true,
    "msg": "",
    "validators": [
        {
            "task": "test",
            "source": "mysql-01",
            "mode": "full",
            "stage": "Running",
            "validatorBinlog": "(mysql-bin.000001, 6571)",
            "validatorBinlogGtid": "",
            "result": null,
            "processedRowsStatus": "insert/update/delete: 2/0/0",
            "pendingRowsStatus": "insert/update/delete: 0/0/0",
            "errorRowsStatus": "new/ignored/resolved: 0/0/0"
        }
    ],
    "tableStatuses": [
        {
            "source": "mysql-01", // source id
            "srcTable": "`db`.`test1`", // 源表名
            "dstTable": "`db`.`test1`", // 目标表名
            "stage": "Running", // 校验状态
            "message": "" // 具体错误信息显示
        }
    ]
}
```

如果你想要查询错误行的详细信息，比如错误原因、错误时间等，可以使用 `dmctl validation show-error` 命令：

```
Usage:
  dmctl validation show-error [--error error-state] <task-name> [flags]

Flags:
      --error string   filtering type of error: all, ignored, or unprocessed (default "unprocessed")
  -h, --help           help for show-error
```

示例输出：

```json
{
    "result": true,
    "msg": "",
    "error": [
        {
            "id": "1", // 错误行标识符，在后续的处理错误行中用到
            "source": "mysql-replica-01", // source id
            "srcTable": "`validator_basic`.`test`", // 错误行源表
            "srcData": "[0, 0]", // 错误行具体数据
            "dstTable": "`validator_basic`.`test`", // 错误行目标表
            "dstData": "[]", // 错误行在下游的数据
            "errorType": "Expected rows not exist", // 错误原因
            "status": "NewErr", // 错误状态
            "time": "2022-07-04 13:33:02", // 错误行发现时间
            "message": "" // 额外信息
        }
    ]
}
```

### 处理增量校验错误行

当增量数据校验发现错误行后，你需要手动处理这些错误行。

在增量校验出现错误行时，增量校验不会停下，而是会把这些错误行记录下来，让用户自己去发现处理。错误行没有被处理时，默认状态是 `unprocessed`。如果你在下游手动矫正了该错误行的错误，增量校验也不会去自动获取矫正后的信息，仍会将该错误行记录在 error 中。

如果你不想在 validation status 中再看到这个错误行、或者你需要给已经解决的错误行打上标记，你可以使用 `validation show-error` 找到错误行的 id，然后使用错误处理命令来对这些错误行进行处理或者标记。

dmctl 提供了三种错误处理命令：

- `clear-error`：清理掉错误行，`show-error`命令将不再展示该`error row`。

    ```
    Usage:
      dmctl validation clear-error <task-name> <error-id|--all> [flags]

    Flags:
          --all    all errors
      -h, --help   help for clear-error
    ```

- `ignore-error`：忽略该错误行，将这个错误行标记为 ignored。

    ```
    Usage:
      dmctl validation ignore-error <task-name> <error-id|--all> [flags]

    Flags:
          --all    all errors
      -h, --help   help for ignore-error
    ```

- `resolve-error`：已手动解决该错误行，将这个错误行标记为 resolved。

    ```
    Usage:
      dmctl validation resolve-error <task-name> <error-id|--all> [flags]

    Flags:
          --all    all errors
      -h, --help   help for resolve-error
    ```

## 停止增量数据校验

如果你需要停止增量数据校验，可以使用 `validation stop` 命令：

```
Usage:
  dmctl validation stop [--all-task] [task-name] [flags]

Flags:
      --all-task   whether applied to all tasks
  -h, --help       help for stop
```

用法可参考 [`dmctl validation start` 命令](#方法-2通过-dmctl-开启)。

## 原理

DM 增量校验（validator）的简要架构如下所示：

![validator summary](/media/dm/dm-validator-summary.jpg)

增量数据校验的工作生命周期如下所示：

![validator lifecycle](/media/dm/dm-validator-lifecycle.jpg)

增量数据校验的具体处理流程如下：

1. validator 从上游拉取 binlog 事件，获取到发生变更的数据行：
    - validator 只会校验增量复制 (syncer) 完成的事件，如果该事件还没有被 syncer 处理，则 validator 会暂停，等待 syncer 处理完成。
    - 如果该事件已被 syncer 处理完成，则进行下面的步骤。
2. validator 将 binlog 解析，并通过黑白名单、过滤器的筛选，表路由的重定向（和 syncer 保持一致）之后，将这些行变动交给在后台运行的 validation worker。
3. validation worker 合并相同表、相同主键的行变动，避免进行“过期”的校验，并将这些行先缓存到内存中。
4. 当 validation worker 积攒了一定数量的行或者到了某个时间间隔之后，validation worker 根据这些行的主键信息在下游数据库中查询当下的数据，并和变动行期望的数据进行对比。
5. validation worker 进行数据校验。如果当前配置是 full mode，会将变动行和下游数据库中获取的行数据进行每列对比；如果当前配置是 fast mode，则只会判断这一行是否还存在。
    - 如果校验成功，则将该行从内存中删除。
    - 如果校验失败，不会马上报错，而是在一定间隔之后继续校验。
    - 对于某些已经在很长时间（由用户定义）内都没有校验成功的行，则将这些行定义为错误行（error row），写入到下游的 meta 库中。你可以通过查询迁移任务信息来获取错误行的数量等信息，详见[查看增量校验的状态](#查看增量校验的状态)以及[处理增量校验错误行](#处理增量校验错误行)。

## 使用限制

- 校验目标表必须有主键或者 not null 的唯一键。
- 上游迁移 DDL 时有以下限制：
    - DDL 不能变更主键，不能调整列顺序，不能删除已有列。
    - 该表不能被 DROP。
- 不支持按照 expression 过滤事件的任务。
- 由于 TiDB 和 MySQL 的浮点数精度有差异，精度范围内误差也会判断为相等（即绝对误差小于 10^-6)。
- 不支持校验的数据类型：
    - JSON
    - 二进制数据
