---
title: 手动处理 Sharding DDL Lock
aliases: ['/docs-cn/tidb-data-migration/dev/manually-handling-sharding-ddl-locks/','/docs-cn/tidb-data-migration/dev/feature-manually-handling-sharding-ddl-locks/']
---

# 手动处理 Sharding DDL Lock

DM (Data Migration) 目前存在[悲观模式](/dm/feature-shard-merge-pessimistic.md)与[乐观模式](/dm/feature-shard-merge-optimistic.md)两种分库分表合并迁移模式，这两种模式中均存在 `shard-ddl-lock` 的概念，但是其实际作用略有不同。

1. 在悲观模式中，DM 使用 sharding DDL lock 来确保分库分表的 DDL 操作可以正确执行。绝大多数情况下，该锁定机制可自动完成；但在部分异常情况发生时，需要使用 `shard-ddl-lock` 手动处理异常的 DDL lock。
2. 在乐观模式中，DM 使用表结构与 DDL 信息来确保分库分表的 DDL 操作可以正确执行。sharding DDL Lock 在乐观模式中用于表示是否所有分表可以生成兼容表结构。绝大多数情况不需人为干预，仅当分库分表表结构存在不可解冲突时，才可以使用 `shard-ddl-lock` 手动处理异常表结构。

> **注意：**
>
> - 本文档的命令在交互模式中进行，因此在以下命令示例中未添加转义字符。在命令行模式中，你需要添加转义字符，防止报错。
> - 不要轻易使用 `shard-ddl-lock unlock` 命令，除非完全明确当前场景下使用这些命令可能会造成的影响，并能接受这些影响。
> - 在手动处理异常的 DDL lock 前，请确保已经了解 DM 的[分库分表合并迁移原理](/dm/feature-shard-merge-pessimistic.md#实现原理)。

## 命令介绍

### `shard-ddl-lock`

该命令用于查看 DDL lock 和主动请求 DM-master 解除指定的 DDL lock。命令仅在 DM v6.0 及其以后版本支持, 之前版本可使用 `show-ddl-locks` 和 `unlock-ddl-lock` 命令。

{{< copyable "shell-regular" >}}

```bash
shard-ddl-lock -h
```

```
maintain or show shard-ddl locks information

Usage:
  dmctl shard-ddl-lock [task] [flags]
  dmctl shard-ddl-lock [command]

Available Commands:
  unlock      Unlock un-resolved DDL locks forcely

Flags:
  -h, --help   help for shard-ddl-lock

Global Flags:
  -s, --source strings   MySQL Source ID.

Use "dmctl shard-ddl-lock [command] --help" for more information about a command.
```

#### 参数解释

+ `shard-ddl-lock [task] [flags]`:
    - 用于查询当前 DM-master 上存在的 DDL lock 信息

+ `shard-ddl-lock [command]`
    - 用于主动请求 DM-master 解除指定的 DDL lock, `command` 只支持 `unlock`

## 命令示例

### `shard-ddl-lock [task] [flags]`

使用 `shard-ddl-lock [task] [flags]` 命令，查询当前 DM-master 上存在的 DDL lock 信息。

悲观模式：

```bash
shard-ddl-lock test
```

<details>
<summary>期望输出</summary>

```
{
    "result": true,                                        # 查询 lock 操作本身是否成功
    "msg": "",                                             # 查询 lock 操作失败时的原因或其它描述信息（如不存在任务 lock）
    "locks": [                                             # 当前存在的 lock 信息列表
        {
            "ID": "test-`shard_db`.`shard_table`",         # lock 的 ID 标识，当前由任务名与 DDL 对应的 schema/table 信息组成
            "task": "test",                                # lock 所属的任务名
            "mode": "pessimistic"                          # shard DDL 协调模式，可为悲观模式 "pessimistic" 或乐观模式 "optimistic"
            "owner": "mysql-replica-01",                   # lock 的 owner，在悲观模式时为第一个遇到该 DDL 的 source ID
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

</details>

乐观模式：

```bash
shard-ddl-lock test
```

<details>
<summary>期望输出</summary>

```
{
    "result": true,                                        # 查询 lock 操作本身是否成功
    "msg": "",                                             # 查询 lock 操作失败时的原因或其它描述信息（如不存在任务 lock）
    "locks": [                                             # 当前存在的 lock 信息列表
        {
            "ID": "test-`shardddl`.`tb`",                  # lock 的 ID 标识，当前由任务名与 DDL 对应的 schema/table 信息组成
            "task": "test",                                # lock 所属的任务名
            "mode": "optimistic",                          # shard DDL 协调模式，可为悲观模式 "pessimistic" 或乐观模式 "optimistic"
            "owner": "mysql-replica-02-`shardddl1`.`tb1`", # lock 的 owner，在乐观模式时为 DDL 存在冲突的上游分表的 source-`database`.`table` 格式信息
            "DDLs": [                                      # 在乐观模式时为 lock 冲突时的 DDL 列表，未出现冲突时为空
                "ALTER TABLE `shardddl`.`tb` MODIFY COLUMN `b` INT DEFAULT -1"
            ],
            "synced": [                                    # 已经收到对应 MySQL 实例内所有分表 DDL 的上游 source-`database`.`table` 分表列表
                "mysql-replica-01-`shardddl1`.`tb1`"
            ],
            "unsynced": [                                  # 尚未收到对应 MySQL 实例内所有分表 DDL 的上游 source-`database`.`table` 分表列表
                "mysql-replica-02-`shardddl1`.`tb1`",
                "mysql-replica-02-`shardddl1`.`tb2`"
            ]
        }
    ]
}
```

</details>

### `shard-ddl-lock unlock`

用于主动请求 DM-master 解除指定的 DDL lock。
1. 悲观模式 `unlock` 包括操作：请求 owner 执行 DDL 操作，请求其他非 owner 的 DM-worker 跳过 DDL 操作，移除 DM-master 上的 lock 信息。
2. 乐观模式 `unlock` 包括操作：请求指定的处于冲突状态的上游表 执行/跳过 冲突 DDL 操作，对其他非指定的表不会进行任何操作，若操作后 DM-master 可以为所有分表生成兼容表结构，则 DM-master 上的 lock 信息将被自动移除。

> **注意：**
>
> `shard-ddl-lock unlock` 在 DM v6.0 以前版本仅对悲观协调模式 (`pessimistic`) 下产生的 lock 有效。

{{< copyable "shell-regular" >}}

```bash
shard-ddl-lock unlock -h
```

```
Unlock un-resolved DDL locks forcely

Usage:
  dmctl shard-ddl-lock unlock <lock-id> [flags]

Flags:
  -a, --action string     accept skip/exec values which means whether to skip or execute ddls (default "skip")
  -d, --database string   database name of the table
  -f, --force-remove      force to remove DDL lock
  -h, --help              help for unlock
  -o, --owner string      source to replace the default owner
  -t, --table string      table name

Global Flags:
  -s, --source strings   MySQL Source ID.
```

悲观模式相关参数：

+ `-o, --owner`：
    - flag 参数，string，可选
    - 不指定时，请求默认的 owner（`shard-ddl-lock` 返回结果中的 `owner`）执行 DDL 操作；指定时，请求该 MySQL source（替代默认的 owner）执行 DDL 操作
    - 除非原 owner 已经从集群中移除，否则不应该指定新的 owner

+ `-f, --force-remove`：
    - flag 参数，boolean，可选
    - 不指定时，仅在 owner 执行 DDL 成功时移除 lock 信息；指定时，即使 owner 执行 DDL 失败也强制移除 lock 信息（此后将无法再次查询或操作该 lock）

+ `lock-id`：
    - 非 flag 参数，string，必选
    - 指定需要执行 unlock 操作的 DDL lock ID（即 `shard-ddl-lock` 返回结果中的 `ID`）

乐观模式相关参数

+ `-a, --action`：
    - flag 参数，string，可选
    - 不指定时，请求指定的上游表跳过该冲突 DDL 操作；指定为 exec 时，请求该上游表执行引起冲突的 DDL 操作
    - 除非执行前已对下游合表表结构进行了适配修改，否则不应该指定为 exec 执行冲突 DDL。

+ `-s, --source`：
    - flag 参数，string，乐观模式必填且目前只支持写一个
    - 执行需要执行 unlock 操作的上游的 source ID，可通过 `shard-ddl-lock` 命令获取

+ `-d, --database`：
    - flag 参数，string，乐观模式必填且目前只支持写一个
    - 执行需要执行 unlock 操作的上游的数据库名称，可通过 `shard-ddl-lock` 命令获取

+ `-t, --table`：
    - flag 参数，string，乐观模式必填且目前只支持写一个
    - 执行需要执行 unlock 操作的上游的表名称，可通过 `shard-ddl-lock` 命令获取

+ `lock-id`：
    - 非 flag 参数，string，必选
    - 指定需要执行 unlock 操作的 DDL lock ID（即 `shard-ddl-lock` 返回结果中的 `ID`）


以下是一个使用 `shard-ddl-lock unlock` 命令的示例：

{{< copyable "shell-regular" >}}

```bash
shard-ddl-lock unlock test-`shard_db`.`shard_table`
```

```
{
    "result": true,                                        # unlock lock 操作是否成功
    "msg": "",                                             # unlock lock 操作失败时的原因
}
```

## 支持场景

目前，使用 `shard-ddl-lock unlock` 命令仅支持处理以下三种 sharding DDL lock 异常情况。

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
3. 使用 `shard-ddl-lock` 查看当前的 DDL lock 信息。

    {{< copyable "shell-regular" >}}

    ```bash
    shard-ddl-lock test
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

    `shard-ddl-lock` 返回的 `unsynced` 中一直包含 `mysql-replica-02` 的信息。

6. 使用 `shard-ddl-lock unlock` 来请求 DM-master 主动 unlock 该 DDL lock。

    - 如果 DDL lock 的 owner 也已经被移除，可以使用 `--owner` 参数指定其他 MySQL source 作为新 owner 来执行 DDL。
    - 当存在任意 MySQL source 报错时，`result` 将为 `false`，此时请仔细检查各 MySQL source 的错误是否是预期可接受的。

        {{< copyable "shell-regular" >}}

        ```bash
        shard-ddl-lock unlock test-`shard_db`.`shard_table`
        ```

        ```
        {
            "result": true,
            "msg": ""
        ```

7. 使用 `shard-ddl-lock` 确认 DDL lock 是否被成功 unlock。

    ```bash
    shard-ddl-lock test
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

使用 `shard-ddl-lock unlock` 手动执行 unlock 操作后，由于该任务的配置信息中仍然包含了已下线的 MySQL source，如果不进行处理，则当下次 sharding DDL 到达时，仍会出现 lock 无法自动完成迁移的情况。

因此，在手动解锁 DDL lock 后，需要再执行以下操作：

1. 使用 `stop-task` 停止运行中的任务。
2. 更新任务配置文件，将已下线 MySQL source 对应的信息从配置文件中移除。
3. 使用 `start-task` 及新任务配置文件重新启动任务。

> **注意：**
>
> 在 `shard-ddl-lock unlock` 之后，如果已下线的 MySQL source 重新加载并尝试对其中的分表进行数据迁移，则会由于数据与下游的表结构不匹配而发生错误。

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

1. 使用 `shard-ddl-lock` 确认 DM-master 上存在该 DDL 操作对应的 lock。

    应该仅有 `mysql-replica-02` 处于 `synced` 状态：

    {{< copyable "shell-regular" >}}

    ```bash
    shard-ddl-lock
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

2. 使用 `shard-ddl-lock unlock` 请求 DM-master unlock 该 lock。

    - Lock 过程中会尝试再次向下游执行该 DDL 操作（重启前的原 owner 已向下游执行过该 DDL 操作），需要确保该 DDL 操作可被多次执行。

        {{< copyable "shell-regular" >}}

        ```bash
        shard-ddl-lock unlock test-`shard_db`.`shard_table`
        ```

        ```
        {
            "result": true,
            "msg": "",
        }
        ```

3. 使用 `shard-ddl-lock` 确认 DDL lock 是否被成功 unlock。
4. 使用 `query-status` 确认迁移任务是否正常。

#### 手动处理后的影响

手动 unlock sharding DDL lock 后，后续的 sharding DDL 将可以自动正常迁移。

### 场景三：乐观模式协调过程中出现表结构冲突

#### Lock 异常原因

在 DM-master 尝试自动协调乐观 DDL，需要等待所有 MySQL source 的表结构达到一致状态，锁信息才会被清除（详见[乐观分表合并协调原理](/dm/feature-shard-merge-optimistic.md#原理)）。如果 sharding DDL 在迁移过程中出现分表的 DDL 生成了不一致表结构，例如部分分表添加 default 0 的列而部分添加 default 1 的列，将造成 master 无法生成兼容表结构从而使得 lock 无法自动 unlock。

#### 手动处理示例

假设上游有 MySQL-1（`mysql-replica-01`）和 MySQL-2（`mysql-replica-02`）两个实例，其中 MySQL-1 中有 `shardddl1`.`tb1` 一个表，MySQL-2 中有 `shardddl1`.`tb1` 和 `shardddl1`.`tb2` 两个表。现在需要将这 3 个表合并后迁移到下游 TiDB 的 `shardddl`.`tb` 表中。

初始表结构如下：

{{< copyable "sql" >}}

```sql
SHOW CREATE TABLE shardddl1.tb1;
```

```
+---------------+-------------------------------------------+
| Table         | Create Table                              |
+---------------+-------------------------------------------+
| tb1           | CREATE TABLE `tb1` (
  `a` int(11) NOT NULL,
  `b` int(11) NOT NULL,
  PRIMARY KEY (`a`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+---------------+-------------------------------------------+
```

上游 MySQL-1 实例下的分表将执行以下 DDL 语句变更表结构：

{{< copyable "sql" >}}

```sql
ALTER TABLE shardddl*.tb* MODIFY b INT DEFAULT 0;
```

上游 MySQL-2 实例下的分表将执行以下 DDL 语句变更表结构：

{{< copyable "sql" >}}

```sql
ALTER TABLE shardddl*.tb* MODIFY b INT DEFAULT -1;
```

MySQL 及 DM 操作与处理流程如下：

1. `mysql-replica-01` 对应的分表执行了对应的 DDL 操作进行表结构变更。

   {{< copyable "sql" >}}

    ```sql
    ALTER TABLE shardddl1.tb1 MODIFY b INT DEFAULT 0;
    ```

2. DM-worker 接受到 `mysql-replica-01` 分表的 DDL 之后，将对应的 DDL 信息发送给 DM-master，DM-master 创建相应的 DDL lock。
3. 使用 `shard-ddl-lock` 查看当前的 DDL lock 信息。

   {{< copyable "shell-regular" >}}

    ```bash
    shard-ddl-lock test
    ```

    ```
    {
        "result": true,
        "msg": "",
        "locks": [
            {
                "ID": "test-`shardddl`.`tb`",
                "task": "test",
                "mode": "optimistic",
                "owner": "",
                "DDLs": [
                ],
                "synced": [
                    "mysql-replica-01-`shardddl1`.`tb1`"
                ],
                "unsynced": [
                    "mysql-replica-02-`shardddl1`.`tb1`",
                    "mysql-replica-02-`shardddl1`.`tb2`"
                ]
            }
        ]
    }
    ```


4. 由于业务需要，`mysql-replica-02` 对应的分表添加的列默认值为 -1，但下游最终结构希望默认值为 0。
5. DM-worker 接受到 `mysql-replica-02` 分表的 DDL 之后，将对应的 DDL 信息发送给 DM-master，DM-master 无法生成兼容表结构，MySQL-2 上的同步暂停。此时使用 `shard-ddl-lock` 和 `query-status test` 命令可以查到具体问题：

   {{< copyable "shell-regular" >}}

    ```bash
    shard-ddl-lock test
    ```

    ```
    {
        "result": true,
        "msg": "",
        "locks": [
            {
                "ID": "test-`shardddl`.`tb`",
                "task": "test",
                "mode": "optimistic",
                "owner": "mysql-replica-02-`shardddl1`.`tb1`",
                "DDLs": [
                    "ALTER TABLE `shardddl`.`tb` MODIFY COLUMN `b` INT DEFAULT -1"
                ],
                "synced": [
                    "mysql-replica-01-`shardddl1`.`tb1`"
                ],
                "unsynced": [
                    "mysql-replica-02-`shardddl1`.`tb1`",
                    "mysql-replica-02-`shardddl1`.`tb2`"
                ]
            }
        ]
    }
    ```

    ```bash
    query-status test
    ```

    ```
    ...
        {
            "result": true,
            "msg": "",
            "sourceStatus": {
                "source": "mysql-replica-02",
                "worker": "worker2",
                ...
            },
            "subTaskStatus": [
                {
                    "name": "test",
                    "stage": "Running",
                    "unit": "Sync",
                    "result": null,
                    "unresolvedDDLLockID": "",
                    "sync": {
                        ...
                        "synced": false,
                        "binlogType": "local",
                        "secondsBehindMaster": "0",
                        "blockDDLOwner": "mysql-replica-02-`shardddl1`.`tb1`",
                        "conflictMsg": "[code=11111:class=functional:scope=internal:level=medium], Message: fail to try sync the optimistic shard ddl lock test-`shardddl`.`tb`: there will be conflicts if DDLs ALTER TABLE `shardddl`.`tb` MODIFY COLUMN `b` INT DEFAULT -1 are applied to the downstream. old table info: CREATE TABLE `tbl`(`a` INT(11) NOT NULL, `b` INT(11) NOT NULL, PRIMARY KEY (`a`)) CHARSET UTF8MB4 COLLATE UTF8MB4_BIN, new table info: CREATE TABLE `tbl`(`a` INT(11) NOT NULL, `b` INT(11) DEFAULT -1, PRIMARY KEY (`a`)) CHARSET UTF8MB4 COLLATE UTF8MB4_BIN, Workaround: Please use `show-ddl-locks` command for more details."
                    }
                }
            ]
        }
    ...
    ```

6. DM-master 上 ID 为 ```test-`shardddl`.`tb` ``` 的 lock 无法为 `mysql-replica-02` 上的 `shardddl1`.`tb1` 的 DDL 生成兼容表结构，

`shard-ddl-lock` 返回的 `unsynced` 中一直包含 `mysql-replica-02` 的信息。

7. 使用 `shard-ddl-lock unlock` 来请求 DM-master 主动 unlock 该 DDL lock。

    - 在乐观模式执行 `shard-ddl-lock unlock` 时需要指定 `-s,-d,-t` 为上文中的 `blockDDLOwner` 中的信息，每个参数均需要且仅指定一个值。
    - 当存在任意 MySQL source 报错时，`result` 将为 `false`，此时请仔细检查各 MySQL source 的错误是否是预期可接受的。

      {{< copyable "shell-regular" >}}

        ```bash
        shard-ddl-lock unlock 'test-`shardddl`.`tb`' -s mysql-replica-02 -d shardddl1 -t tb1 --action skip
        ```

        ```
        {
            "result": true,
            "msg": ""
        ```

8. 重复该操作跳过第二个分表的 DDL。
9. 使用 `shard-ddl-lock` 确认 DDL lock 是否被成功 unlock。

    ```bash
    shard-ddl-lock test
    ```

    ```
    {
        "result": true,
        "msg": "no DDL lock exists",
        "locks": [
        ]
    }
    ```

10. 查看下游 TiDB 中的表结构是否变更成功。

    {{< copyable "sql" >}}

     ```sql
     SHOW CREATE TABLE shardddl.tb;
     ```

     ```
     +-------------+--------------------------------------------------+
     | Table       | Create Table                                     |
     +-------------+--------------------------------------------------+
     | tb    | CREATE TABLE `tb` (
     `a` int(11) NOT NULL,
     `b` int(11) DEFAULT '0',
     PRIMARY KEY (`a`)
     ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
     +-------------+--------------------------------------------------+
     ```

11. 使用 `query-status` 确认迁移任务是否正常。

#### 手动处理后的影响

使用 `shard-ddl-lock unlock` 手动执行 unlock 操作后，由于出错分表的表结构中仍然包含了不兼容的表信息，如果不进行处理，则当下次 sharding DDL 到达时，仍会出现 lock 无法自动完成迁移的情况。

因此，在手动解锁 DDL lock 后，需要再执行以下操作：

1. 使用 `pause-task` 暂停运行中的任务。
2. 使用 `binlog-schema update` 更新 skip 的表的表结构为兼容的表结构。
3. 使用 `resume-task` 恢复任务运行。

> **注意：**
>
> 在某些场景下 `shard-ddl-lock unlock` 时，如果下游不进行手动处理，可能会引起上下游数据不一致。
