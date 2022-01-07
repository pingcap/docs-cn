---
title: 手动处理 Sharding DDL Lock
aliases: ['/docs-cn/tidb-data-migration/dev/manually-handling-sharding-ddl-locks/','/docs-cn/tidb-data-migration/dev/feature-manually-handling-sharding-ddl-locks/']
---

# 手动处理 Sharding DDL Lock

DM (Data Migration) 使用 sharding DDL lock 来确保分库分表的 DDL 操作可以正确执行。绝大多数情况下，该锁定机制可自动完成；但在部分异常情况发生时，需要使用 `unlock-ddl-lock` 手动处理异常的 DDL lock。

> **注意：**
> 
> - 本文档只适用于悲观协调模式下 sharding DDL lock 的处理。
> - 本文档的命令在交互模式中进行，因此在以下命令示例中未添加转义字符。在命令行模式中，你需要添加转义字符，防止报错。
> - 不要轻易使用 `unlock-ddl-lock` 命令，除非完全明确当前场景下使用这些命令可能会造成的影响，并能接受这些影响。
> - 在手动处理异常的 DDL lock 前，请确保已经了解 DM 的[分库分表合并迁移原理](/dm/feature-shard-merge-pessimistic.md#实现原理)。

## 命令介绍

### `show-ddl-locks`

该命令用于查询当前 DM-master 上存在的 DDL lock 信息。

#### 命令示例

{{< copyable "shell-regular" >}}

```bash
show-ddl-locks [--source=mysql-replica-01] [task-name | task-file]
```

#### 参数解释

+ `source`：
    - flag 参数，string，`--source`，可选
    - 不指定时，查询所有 MySQL source 相关的 lock 信息；指定时，仅查询与该 MySQL source 相关的 lock 信息，可重复多次指定

+ `task-name | task-file`：
    - 非 flag 参数，string，可选
    - 不指定时，查询与所有任务相关的 lock 信息；指定时，仅查询特定任务相关的 lock 信息

#### 返回结果示例

{{< copyable "shell-regular" >}}

```bash
show-ddl-locks test
```

```
{
    "result": true,                                        # 查询 lock 操作本身是否成功
    "msg": "",                                             # 查询 lock 操作失败时的原因或其它描述信息（如不存在任务 lock）
    "locks": [                                             # 当前存在的 lock 信息列表
        {
            "ID": "test-`shard_db`.`shard_table`",         # lock 的 ID 标识，当前由任务名与 DDL 对应的 schema/table 信息组成
            "task": "test",                                # lock 所属的任务名
            "mode": "pessimistic"                          # shard DDL 协调模式，可为悲观模式 "pessimistic" 或乐观模式 "optimistic"
            "owner": "mysql-replica-01",                   # lock 的 owner（在悲观模式时为第一个遇到该 DDL 的 source ID），在乐观模式时总为空
            "DDLs": [                                      # 在悲观模式时为 lock 对应的 DDL 列表，在乐观模式时总为空
                "USE `shard_db`; ALTER TABLE `shard_db`.`shard_table` DROP COLUMN `c2`;"
            ],
            "synced": [                                    # 已经收到对应 MySQL 实例内所有分表 DDL 的 source 列表
                "mysql-replica-01"
            ],
            "unsynced": [                                  # 尚未收到对应 MySQL 实例内所有分表 DDL 的 source 列表
                "mysql-replica-02"
            ]
        }
    ]
}
```

### `unlock-ddl-lock`

该命令用于主动请求 DM-master 解除指定的 DDL lock，包括的操作：请求 owner 执行 DDL 操作，请求其他非 owner 的 DM-worker 跳过 DDL 操作，移除 DM-master 上的 lock 信息。

> **注意：**
>
> `unlock-ddl-lock` 当前仅对悲观协调模式 (`pessimistic`) 下产生的 lock 有效。

#### 命令示例

{{< copyable "shell-regular" >}}

```bash
unlock-ddl-lock [--owner] [--force-remove] <lock-ID>
```

#### 参数解释

+ `owner`：
    - flag 参数，string，`--owner`，可选
    - 不指定时，请求默认的 owner（`show-ddl-locks` 返回结果中的 `owner`）执行 DDL 操作；指定时，请求该 MySQL source（替代默认的 owner）执行 DDL 操作
    - 除非原 owner 已经从集群中移除，否则不应该指定新的 owner

+ `force-remove`：
    - flag 参数，boolean，`--force-remove`，可选
    - 不指定时，仅在 owner 执行 DDL 成功时移除 lock 信息；指定时，即使 owner 执行 DDL 失败也强制移除 lock 信息（此后将无法再次查询或操作该 lock）

+ `lock-ID`：
    - 非 flag 参数，string，必选
    - 指定需要执行 unlock 操作的 DDL lock ID（即 `show-ddl-locks` 返回结果中的 `ID`）

#### 返回结果示例

{{< copyable "shell-regular" >}}

```bash
unlock-ddl-lock test-`shard_db`.`shard_table`
```

```
{
    "result": true,                                        # unlock lock 操作是否成功
    "msg": "",                                             # unlock lock 操作失败时的原因
}
```

## 支持场景

目前，使用 `unlock-ddl-lock` 命令仅支持处理以下两种 sharding DDL lock 异常情况。

### 场景一：部分 MySQL source 被移除

#### Lock 异常原因

在 DM-master 尝试自动 unlock sharding DDL lock 之前，需要等待所有 MySQL source 的 sharding DDL events 全部到达（详见[分库分表合并迁移原理](/dm/feature-shard-merge-pessimistic.md#实现原理)）。如果 sharding DDL 已经在迁移过程中，同时有部分 MySQL source 被移除，且不再计划重新加载它们（按业务需求移除了这部分 MySQL source），则会由于永远无法等齐所有的 DDL 而造成 lock 无法自动 unlock。

#### 手动处理示例

假设上游有 MySQL-1（`mysql-replica-01`）和 MySQL-2（`mysql-replica-02`）两个实例，其中 MySQL-1 中有 `shard_db_1`.`shard_table_1` 和 `shard_db_1`.`shard_table_2` 两个表，MySQL-2 中有 `shard_db_2`.`shard_table_1` 和 `shard_db_2`.`shard_table_2` 两个表。现在需要将这 4 个表合并后迁移到下游 TiDB 的 `shard_db`.`shard_table` 表中。

初始表结构如下：

{{< copyable "sql" >}}

```sql
SHOW CREATE TABLE shard_db_1.shard_table_1;
```

```
+---------------+------------------------------------------+
| Table         | Create Table                             |
+---------------+------------------------------------------+
| shard_table_1 | CREATE TABLE `shard_table_1` (
  `c1` int(11) NOT NULL,
  PRIMARY KEY (`c1`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 |
+---------------+------------------------------------------+
```

上游分表将执行以下 DDL 语句变更表结构：

{{< copyable "sql" >}}

```sql
ALTER TABLE shard_db_*.shard_table_* ADD COLUMN c2 INT;
```

MySQL 及 DM 操作与处理流程如下：

1. `mysql-replica-01` 对应的两个分表执行了对应的 DDL 操作进行表结构变更。

    {{< copyable "sql" >}}

    ```sql
    ALTER TABLE shard_db_1.shard_table_1 ADD COLUMN c2 INT;
    ```

    {{< copyable "sql" >}}

    ```sql
    ALTER TABLE shard_db_1.shard_table_2 ADD COLUMN c2 INT;
    ```

2. DM-worker 接受到 `mysql-replica-01` 两个分表的 DDL 之后，将对应的 DDL 信息发送给 DM-master，DM-master 创建相应的 DDL lock。
3. 使用 `show-ddl-lock` 查看当前的 DDL lock 信息。

    {{< copyable "shell-regular" >}}

    ```bash
    show-ddl-locks test
    ```

    ```
    {
        "result": true,
        "msg": "",
        "locks": [
            {
                "ID": "test-`shard_db`.`shard_table`",
                "task": "test",
                "mode": "pessimistic"
                "owner": "mysql-replica-01",
                "DDLs": [
                    "USE `shard_db`; ALTER TABLE `shard_db`.`shard_table` ADD COLUMN `c2` int(11);"
                ],
                "synced": [
                    "mysql-replica-01"
                ],
                "unsynced": [
                    "mysql-replica-02"
                ]
            }
        ]
    }
    ```

4. 由于业务需要，`mysql-replica-02` 对应的数据不再需要迁移到下游 TiDB，对 `mysql-replica-02` 执行了移除操作。
5. DM-master 上 ID 为 ```test-`shard_db`.`shard_table` ``` 的 lock 无法等到 `mysql-replica-02` 的 DDL 操作信息。

    `show-ddl-locks` 返回的 `unsynced` 中一直包含 `mysql-replica-02` 的信息。

6. 使用 `unlock-dll-lock` 来请求 DM-master 主动 unlock 该 DDL lock。

    - 如果 DDL lock 的 owner 也已经被移除，可以使用 `--owner` 参数指定其他 MySQL source 作为新 owner 来执行 DDL。
    - 当存在任意 MySQL source 报错时，`result` 将为 `false`，此时请仔细检查各 MySQL source 的错误是否是预期可接受的。

        {{< copyable "shell-regular" >}}

        ```bash
        unlock-ddl-lock test-`shard_db`.`shard_table`
        ```

        ```
        {
            "result": true,
            "msg": ""
        ```

7. 使用 `show-dd-locks` 确认 DDL lock 是否被成功 unlock。

    ```bash
    show-ddl-locks test
    ```

    ```
    {
        "result": true,
        "msg": "no DDL lock exists",
        "locks": [
        ]
    }
    ```

8. 查看下游 TiDB 中的表结构是否变更成功。

    {{< copyable "sql" >}}

    ```sql
    SHOW CREATE TABLE shard_db.shard_table;
    ```

    ```
    +-------------+--------------------------------------------------+
    | Table       | Create Table                                     |
    +-------------+--------------------------------------------------+
    | shard_table | CREATE TABLE `shard_table` (
      `c1` int(11) NOT NULL,
      `c2` int(11) DEFAULT NULL,
      PRIMARY KEY (`c1`)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin |
    +-------------+--------------------------------------------------+
    ```

9. 使用 `query-status` 确认迁移任务是否正常。

#### 手动处理后的影响

使用 `unlock-ddl-lock` 手动执行 unlock 操作后，由于该任务的配置信息中仍然包含了已下线的 MySQL source，如果不进行处理，则当下次 sharding DDL 到达时，仍会出现 lock 无法自动完成迁移的情况。

因此，在手动解锁 DDL lock 后，需要再执行以下操作：

1. 使用 `stop-task` 停止运行中的任务。
2. 更新任务配置文件，将已下线 MySQL source 对应的信息从配置文件中移除。
3. 使用 `start-task` 及新任务配置文件重新启动任务。

> **注意：**
>
> 在 `unlock-ddl-lock` 之后，如果已下线的 MySQL source 重新加载并尝试对其中的分表进行数据迁移，则会由于数据与下游的表结构不匹配而发生错误。

### 场景二：unlock 过程中部分 DM-worker 异常停止或网络中断

#### Lock 异常原因

在 DM-master 收到所有 DM-worker 的 DDL 信息后，执行自动 unlock DDL lock 的操作主要包括以下步骤：

1. 请求 lock owner 执行 DDL 操作，并更新对应分表的 checkpoint。
2. 在 owner 执行 DDL 操作成功后，移除 DM-master 上保存的 DDL lock 信息。
3. 在 owner 执行 DDL 操作成功后，请求其他所有非 owner 跳过 DDL 操作并更新对应分表的 checkpoint。
4. DM-master 在所有 owner/非 owner 操作成功后，移除对应的 DDL lock 信息。

上述 unlock DDL lock 的操作不是原子的。如果非 owner 跳过 DDL 操作成功后，所在的 DM-worker 异常停止或与下游 TiDB 发生网络异常，造成无法成功更新 checkpoint。

当非 owner 对应的 MySQL source 恢复数据迁移时，会尝试请求 DM-master 重新协调异常发生前已经协调过的 DDL、且永远无法等到其他 MySQL source 的对应 DDL，造成该 DDL 操作对应 lock 的自动 unlock。

#### 手动处理示例

仍然假设是 [部分 MySQL source 被移除](#场景一部分-mysql-source-被移除) 示例中的上下游表结构及合表迁移需求。

当在 DM-master 自动执行 unlock 操作的过程中，owner（`mysql-replica-01`）成功执行了 DDL 操作且开始继续进行后续迁移，但在请求非 owner（`mysql-replica-02`）跳过 DDL 操作的过程中，由于对应的 DM-worker 发生了重启在跳过 DDL 后未能更新 checkpoint。

`mysql-replica-02` 对应的数据迁移子任务恢复后，将在 DM-master 上创建一个新的 lock，但其他 MySQL source 此时已经执行或跳过 DDL 操作并在进行后续迁移。

处理流程如下：

1. 使用 `show-ddl-locks` 确认 DM-master 上存在该 DDL 操作对应的 lock。

    应该仅有 `mysql-replica-02` 处于 `synced` 状态：

    {{< copyable "shell-regular" >}}

    ```bash
    show-ddl-locks
    ```

    ```
    {
        "result": true,
        "msg": "",
        "locks": [
            {
                "ID": "test-`shard_db`.`shard_table`",
                "task": "test",
                "mode": "pessimistic"
                "owner": "mysql-replica-02",
                "DDLs": [
                    "USE `shard_db`; ALTER TABLE `shard_db`.`shard_table` ADD COLUMN `c2` int(11);"
                ],
                "synced": [
                    "mysql-replica-02"
                ],
                "unsynced": [
                    "mysql-replica-01"
                ]
            }
        ]
    }
    ```

2. 使用 `unlock-ddl-lock` 请求 DM-master unlock 该 lock。

    - Lock 过程中会尝试再次向下游执行该 DDL 操作（重启前的原 owner 已向下游执行过该 DDL 操作），需要确保该 DDL 操作可被多次执行。

        {{< copyable "shell-regular" >}}

        ```bash
        unlock-ddl-lock test-`shard_db`.`shard_table`
        ```

        ```
        {
            "result": true,
            "msg": "",
        }
        ```

3. 使用 `show-ddl-locks` 确认 DDL lock 是否被成功 unlock。
4. 使用 `query-status` 确认迁移任务是否正常。

#### 手动处理后的影响

手动 unlock sharding DDL lock 后，后续的 sharding DDL 将可以自动正常迁移。
