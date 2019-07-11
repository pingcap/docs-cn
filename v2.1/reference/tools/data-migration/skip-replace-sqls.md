---
title: 跳过 (skip) 或替代执行 (replace) 异常的 SQL 语句
category: reference
---

# 跳过 (skip) 或替代执行 (replace) 异常的 SQL 语句

本文介绍了如何使用 DM 来处理异常的 SQL 语句。

目前，TiDB 并不完全兼容所有的 MySQL 语法。当使用 DM 从 MySQL 同步数据到 TiDB 时，如果 TiDB 不支持对应的 SQL 语句，可能会造成错误并中断同步任务。在这种情况下，DM 提供以下两种方式来恢复同步：

- 使用 dmctl 来手动跳过该 SQL 语句对应的 binlog event。

- 使用 dmctl 来手动指定其他 SQL 语句来替代该 SQL 语句对应的 binlog event，并向下游执行。

如果提前预知将要同步 TiDB 不支持的 SQL 语句，也可以使用 dmctl 来手动预设跳过/替代执行操作。当 DM 尝试将该 SQL 语句对应的 binlog event 同步到下游时，该预设的操作将自动执行，从而避免同步过程被中断。

#### 使用限制

- 跳过/替代执行操作只适合用于一次性跳过/替代执行**下游 TiDB 不支持执行的 SQL 语句**，其它同步错误请不要使用此方式进行处理。

    - 其它同步错误可尝试使用 [black & white table lists](/reference/tools/data-migration/features/overview.md#black-white-table-lists) 或 [binlog event filter](/reference/tools/data-migration/features/overview.md#binlog-event-filter)。

- 如果业务不能接受下游 TiDB 跳过异常的 DDL 语句，也不接受使用其他 DDL 语句作为替代，则不适合使用此方式进行处理。

    - 比如：`DROP PRIMARY KEY`
    - 这种情况下，只能在下游重建一个（DDL 执行完后的）新表结构对应的表，并将原表的全部数据重新导入该新表。

- 单次跳过/替代执行操作都是针对单个 binlog event 的。

- `--sharding` 仅用于对 sharding group 预设一些操作，并且必须在 DDL 语句执行之前预设，不能在 DDL 语句已经执行后预设。

    - `--sharding` 模式下只支持预设，并只能使用 `--sql-pattern` 来匹配 binlog event。
    - 有关使用 DM 处理 sharding DDL 同步的原理，请参阅[分库分表合并同步原理](/reference/tools/data-migration/features/shard-merge.md#实现原理)。

#### 匹配 binlog event

当同步任务由于执行 SQL 语句出错而中断时，可以使用 `query-error` 命令获取对应 binlog event 的 position 信息。在执行 `sql-skip` / `sql-replace` 时，通过指定该 position 信息，即可与对应的 binlog event 进行匹配。

然而，在同步中断前主动处理不被支持的 SQL 语句的情况下，由于无法提前预知 binlog event 的 position 信息，则需要使用其他方式来确保与后续将到达的 binlog event 进行匹配。

在 DM 中，支持如下两种 binlog event 匹配模式（两种模式只能选择其中一种）：

1. binlog position：binlog event 的 position 信息

    - binlog position 在命令中使用 `--binlog-pos` 参数传入，格式为 `binlog-filename:binlog-pos`，如 `mysql-bin|000001.000003:3270`。
    - DM 中 binlog filename 的格式与上游 MySQL 中 binlog filename 的格式不完全一致。
    - 在同步执行出错后，binlog position 可直接从 `query-error` 返回的 `failedBinlogPosition` 中获得。

2. DDL pattern：（仅限于 DDL 语句的）正则表达式匹配模式

    - DDL pattern 在命令中使用 `--sql-pattern` 参数传入，如要匹配 ``` ALTER TABLE `db2`.`tbl2` DROP COLUMN `c2` ```，则对应的正则表达式为 ``` ~(?i)ALTER\s+TABLE\s+`db2`.`tbl2`\s+DROP\s+COLUMN\s+`c2` ```。
    - 正则表达式必须以 `~` 为前缀，且不包含任何原始空格（正则表达式字符串中的空格均以 `\s` 或 `\s+` 表示）。

对于合库合表场景，如果需要由 DM 自动选择 DDL lock owner 来执行跳过/替代执行操作，则由于不同 DM-worker 上 DDL 语句对应的 binlog position 无逻辑关联且难以确定，因此只能使用 DDL pattern 匹配模式。

> **注意：**
>
> - 一个 binlog event 只能注册一个使用 `--binlog-pos` 指定的 operator，后注册的 operator 会覆盖之前已经注册的 operator。
> - 不要尝试为一个 binlog event 同时使用 `--binlog-pos` 和 `--sql-pattern` 指定 operator。
> - operator 在与 binlog event 匹配成功后（而非执行成功后）即会被删除，后续如果需要再进行（`--sql-pattern`）匹配则必须重新注册。

### 支持场景

- 场景一：同步过程中，上游执行了 TiDB 不支持的 DDL 语句并同步到了 DM，造成同步任务中断。

    - 如果业务能接受下游 TiDB 不执行该 DDL 语句，则使用 `sql-skip` 跳过对该 DDL 语句的同步以恢复同步任务。
    - 如果业务能接受下游 TiDB 执行其他 DDL 语句来作为替代，则使用 `sql-replace` 替代该 DDL 的同步以恢复同步任务。

- 场景二：同步过程中，预先知道了上游将执行 TiDB 不支持的 DDL 语句，则需要提前处理以避免同步任务中断。

    - 如果业务能接受下游 TiDB 不执行该 DDL 语句，则使用 `sql-skip` 预设一个跳过该 DDL 语句的操作，当执行到该 DDL 语句时即自动跳过。
    - 如果业务能接受下游 TiDB 执行其他 DDL 语句来作为替代，则使用 `sql-replace` 预设一个替代该 DDL 语句的操作，当执行到该 DDL 语句时即自动替代。

### 实现原理

DM 在进行增量数据同步时，简化后的流程大致为：

1. relay 处理单元从上游拉取 binlog 存储在本地作为 relay log。

2. binlog 同步单元（sync）读取本地 relay log，获取其中的 binlog event。

3. binlog 同步单元解析该 binlog event 并构造 DDL/DML 语句，然后将这些语句向下游 TiDB 执行。

在 binlog 同步单元解析完 binlog event 并向下游 TiDB 执行时，可能会由于 TiDB 不支持对应的 SQL 语句而报错并造成同步中断。

在 DM 中，可以为 binlog event 注册一些跳过/替代执行操作（operator）。在向下游 TiDB 执行 SQL 语句前，将当前的 binlog event 信息（position、DDL 语句）与注册的 operator 进行比较。如果 position 或 DDL 语句与注册的某个 operator 匹配，则执行该 operator 对应的操作并将该 operator 移除。

**同步中断后使用 `sql-skip` 或 `sql-replace` 恢复同步的流程**

1. 使用 `sql-skip` 或 `sql-replace` 为指定的 binlog position 或 DDL pattern 注册 operator。

2. 使用 `resume-task` 恢复之前由于同步出错导致中断的任务。

3. 重新解析获得之前造成同步出错的 binlog event。

4. 该 binlog event 与第一步注册的 operator 匹配成功。

5. 执行 operator 对应的操作（跳过/替代执行）后，继续执行同步任务。

**同步中断前使用 `sql-skip` 或 `sql-replace` 预设操作以避免同步中断的流程**

1. 使用 `sql-skip` 或 `sql-replace` 为指定的 DDL pattern 注册 operator。

2. 从 relay log 中解析获得 binlog event。

3. （包含 TiDB 不支持 SQL 语句的）binlog event 与第一步注册的 operator 匹配成功。

4. 执行 operator 对应的操作（跳过/替代执行）后，继续执行同步任务，任务不发生中断。

**合库合表同步中断前使用 `sql-skip` 或 `sql-replace` 预设操作以避免同步中断的流程**

1. 使用 `sql-skip` 或 `sql-replace`（在 DM-master 上）为指定的 DDL pattern 注册 operator。

2. 各 DM-worker 从 relay log 中解析获得 binlog event。

3. DM-master 协调各个 DM-worker 进行 DDL lock 同步。

4. DM-master 判断得知 DDL lock 同步成功后，将第一步注册的 operator 发送给 DDL lock owner。

5. DM-master 请求 DDL lock owner 执行 DDL 语句。

6. DDL lock owner 将要执行的 DDL 语句与第四步收到的 operator 匹配成功。

7. 执行 operator 对应的操作（跳过/替代执行）后，继续执行同步任务。

### 命令介绍

使用 dmctl 手动处理 TiDB 不支持的 SQL 语句时，主要使用的命令包括 `query-status`、`query-error`、`sql-skip` 和 `sql-replace`。

#### query-status

`query-status` 命令用于查询当前 DM-worker 内子任务及 relay 单元等的状态，详见[查询状态](/reference/tools/data-migration/query-status.md)。

#### query-error

`query-error` 命令用于查询 DM-worker 内子任务及 relay 单元当前在运行中存在的错误。

##### 命令用法

```bash
query-error [--worker=127.0.0.1:8262] [task-name]
```

##### 参数解释

+ `worker`：
    - flag 参数，string，`--worker`，可选；
    - 不指定时查询所有 DM-worker 上的错误，指定时仅查询特定一组 DM-worker 上的错误。

+ `task-name`：
    - 非 flag 参数，string，可选；
    - 不指定时查询所有任务内的错误，指定时仅查询特定任务内的错误。

##### 结果示例

```bash
» query-error test
{
    "result": true,                              # query-error 操作本身是否成功
    "msg": "",                                   # query-error 操作失败的说明信息
    "workers": [                                 # DM-worker 信息列表
        {
            "result": true,                      # 该 DM-worker 上 query-error 操作是否成功
            "worker": "127.0.0.1:8262",          # 该 DM-worker 的 IP:port（worker-id）
            "msg": "",                           # 该 DM-worker 上 query-error 操作失败的说明信息
            "subTaskError": [                    # 该 DM-worker 上运行子任务的错误信息
                {
                    "name": "test",              # 任务名
                    "stage": "Paused",           # 当前任务的状态
                    "unit": "Sync",              # 当前正在处理任务的处理单元
                    "sync": {                    # binlog 同步单元（sync）的错误信息
                        "errors": [              # 当前处理单元的错误信息列表
                            {
                                // 错误信息描述
                                "msg": "exec sqls[[USE `db1`; ALTER TABLE `db1`.`tbl1` CHANGE COLUMN `c2` `c2` decimal(10,3);]] failed, err:Error 1105: unsupported modify column length 10 is less than origin 11",
                                // 发生错误的 binlog event 的 position
                                "failedBinlogPosition": "mysql-bin|000001.000003:34642",
                                // 发生错误的 SQL 语句
                                "errorSQL": "[USE `db1`; ALTER TABLE `db1`.`tbl1` CHANGE COLUMN `c2` `c2` decimal(10,3);]"
                            }
                        ]
                    }
                }
            ],
            "RelayError": {                      # 该 DM-worker 上 relay 处理单元的错误信息
                "msg": ""                        # 错误信息描述
            }
        }
    ]
}
```

#### sql-skip

`sql-skip` 命令用于预设一个跳过操作，当 binlog event 的 position 或 SQL 语句与指定的 `binlog-pos` 或 `sql-pattern` 匹配时，执行该跳过操作。

##### 命令用法

```bash
sql-skip <--worker=127.0.0.1:8262> [--binlog-pos=mysql-bin|000001.000003:3270] [--sql-pattern=~(?i)ALTER\s+TABLE\s+`db1`.`tbl1`\s+ADD\s+COLUMN\s+col1\s+INT] [--sharding] <task-name>
```

##### 参数解释

+ `worker`：
    - flag 参数，string，`--worker`；
    - 未指定 `--sharding` 时必选，指定 `--sharding` 时禁止使用；
    - `worker` 指定预设操作将生效的 DM-worker。

+ `binlog-pos`：
    - flag 参数，string，`--binlog-pos`；
    - `binlog-pos` 与 `--sql-pattern` 必须指定其中一个，且只能指定其中一个。
    - 在指定时表示操作将在 `binlog-pos` 与 binlog event 的 position 匹配时生效，格式为 `binlog-filename:binlog-pos`，如 `mysql-bin|000001.000003:3270`。
    - 在同步执行出错后，binlog position 可直接从 `query-error` 返回的 `failedBinlogPosition` 中获得。

+ `sql-pattern`：
    - flag 参数，string，`--sql-pattern`；
    - `--sql-pattern` 与 `binlog-pos` 必须指定其中一个，且只能指定其中一个。
    - 在指定时表示操作将在 `sql-pattern` 与 binlog event 对应的（经过可选的 router-rule 转换后的）DDL 语句匹配时生效。格式为以 `~` 为前缀的正则表达式，如 ``` ~(?i)ALTER\s+TABLE\s+`db1`.`tbl1`\s+ADD\s+COLUMN\s+col1\s+INT ```。
        - 暂时不支持正则表达式中包含原始空格，需要使用 `\s` 或 `\s+` 替代空格。
        - 正则表达式必须以 `~` 为前缀，详见[正则表达式语法](https://golang.org/pkg/regexp/syntax/#hdr-Syntax)。
        - 正则表达式中的库名和表名必须是经过可选的 router-rule 转换后的名字，即对应下游的目标库名和表名。如上游为 ``` `shard_db_1`.`shard_tbl_1` ```，下游为 ``` `shard_db`.`shard_tbl` ```，则应该尝试匹配 ``` `shard_db`.`shard_tbl` ```。
        - 正则表达式中的库名、表名及列名需要使用 ``` ` ``` 标记，如 ``` `db1`.`tbl1` ```。

+ `sharding`：
    - flag 参数，boolean，`--sharding`；
    - 未指定 `--worker` 时必选，指定 `--worker` 时禁止使用；
    - 在指定时表示预设的操作将在 sharding DDL 同步过程中的 DDL lock owner 内生效。

+ `task-name`：
    - 非 flag 参数，string，必选；
    - 指定预设的操作将生效的任务。

#### sql-replace

`sql-replace` 命令用于预设一个替代执行操作，当 binlog event 的 position 或 SQL 语句与指定的 `binlog-pos` 或 `sql-pattern` 匹配时，执行该替代执行操作。

##### 命令用法

```bash
sql-replace <--worker=127.0.0.1:8262> [--binlog-pos=mysql-bin|000001.000003:3270] [--sql-pattern=~(?i)ALTER\s+TABLE\s+`db1`.`tbl1`\s+ADD\s+COLUMN\s+col1\s+INT] [--sharding] <task-name> <SQL-1;SQL-2>
```

##### 参数解释

+ `worker`：
    - 与 `sql-skip` 命令的 `--worker` 参数解释一致。

+ `binlog-pos`：
    - 与 `sql-skip` 命令的 `--binlog-pos` 参数解释一致。

+ `sql-pattern`：
    - 与 `sql-skip` 命令的 `--sql-pattern` 参数解释一致。

+ `sharding`：
    - 与 `sql-skip` 命令的 `--sharding` 参数解释一致。

+ `task-name`：
    - 与 `sql-skip` 命令的 `task-name` 参数解释一致。

+ `SQLs`：
    - 非 flag 参数，string，必选；
    - `SQLs` 指定将用于替代原 binlog event 的新的 SQL 语句。多条 SQL 语句间以 `;` 分隔，如 ``` ALTER TABLE shard_db.shard_table drop index idx_c2;ALTER TABLE shard_db.shard_table DROP COLUMN c2; ```。

### 使用示例

#### 同步中断后被动执行跳过操作

##### 应用场景

假设现在需要将上游的 `db1.tbl1` 表同步到下游 TiDB（非合库合表同步场景），初始时表结构为：

```sql
mysql> SHOW CREATE TABLE db1.tbl1;
+-------+--------------------------------------------------+
| Table | Create Table                                     |
+-------+--------------------------------------------------+
| tbl1  | CREATE TABLE `tbl1` (
  `c1` int(11) NOT NULL,
  `c2` decimal(11,3) DEFAULT NULL,
  PRIMARY KEY (`c1`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 |
+-------+--------------------------------------------------+
```

此时，上游执行以下 DDL 操作修改表结构（将列的 DECIMAL(11, 3) 修改为 DECIMAL(10, 3)）：

```sql
ALTER TABLE db1.tbl1 CHANGE c2 c2 DECIMAL (10, 3);
```

则会由于 TiDB 不支持该 DDL 语句而导致 DM 同步任务中断且报如下错误：

```bash
exec sqls[[USE `db1`; ALTER TABLE `db1`.`tbl1` CHANGE COLUMN `c2` `c2` decimal(10,3);]] failed, 
err:Error 1105: unsupported modify column length 10 is less than origin 11
```

此时使用 `query-status` 查询任务状态，可看到 `stage` 转为了 `Paused`，且 `errors` 中有相关的错误描述信息。

使用 `query-error` 可以获取该错误的详细信息。比如，执行 `query-error test` 可获得出错的 binlog event 的 position（`failedBinlogPosition`）为 `mysql-bin|000001.000003:34642`。

##### 被动跳过 SQL 语句

假设业务上可以接受下游 TiDB 不执行此 DDL 语句（即继续保持原有的表结构），则可以通过使用 `sql-skip` 命令跳过该 DDL 语句以恢复同步任务。操作步骤如下：

1. 使用 `query-error` 获取同步出错的 binlog event 的 position 信息。
    - position 信息可直接由 `query-error` 返回的 `failedBinlogPosition` 获得。
    - 本示例中的 position 为 `mysql-bin|000001.000003:34642`。

2. 使用 `sql-skip` 预设一个 binlog event 跳过操作，该操作将在使用 `resume-task` 后同步该 binlog event 到下游时生效。

    ```bash
    » sql-skip --worker=127.0.0.1:8262 --binlog-pos=mysql-bin|000001.000003:34642 test
    {
        "result": true,
        "msg": "",
        "workers": [
            {
                "result": true,
                "worker": "",
                "msg": ""
            }
        ]
    }
    ```

    对应 DM-worker 节点中也可以看到类似如下日志：

    ```bash
    2018/12/28 11:17:51 operator.go:121: [info] [sql-operator] set a new operator 
    uuid: 6bfcf30f-2841-4d70-9a34-28d7082bdbd7, pos: (mysql-bin|000001.000003, 34642), op: SKIP, args:
    on replication unit
    ```

3. 使用 `resume-task` 恢复之前出错中断的同步任务。

    ```bash
    » resume-task --worker=127.0.0.1:8262 test
    {
        "op": "Resume",
        "result": true,
        "msg": "",
        "workers": [
            {
                "op": "Resume",
                "result": true,
                "worker": "127.0.0.1:8262",
                "msg": ""
            }
        ]
    }
    ```

    对应 DM-worker 节点中也可以看到类似如下日志：

    ```bash
    2018/12/28 11:27:46 operator.go:158: [info] [sql-operator] binlog-pos (mysql-bin|000001.000003, 34642) matched, 
    applying operator uuid: 6bfcf30f-2841-4d70-9a34-28d7082bdbd7, pos: (mysql-bin|000001.000003, 34642), op: SKIP, args:
    ```

4. 使用 `query-status` 确认该任务的 `stage` 已经转为 `Running`。

5. 使用 `query-error` 确认原错误信息已不再存在。

#### 同步中断前主动执行替代执行操作

##### 应用场景

假设现在需要将上游的 `db2.tbl2` 表同步到下游 TiDB（非合库合表同步场景），初始时表结构为：

```sql
mysql> SHOW CREATE TABLE db2.tbl2;
+-------+--------------------------------------------------+
| Table | Create Table                                     |
+-------+--------------------------------------------------+
| tbl2  | CREATE TABLE `tbl2` (
  `c1` int(11) NOT NULL,
  `c2` int(11) DEFAULT NULL,
  PRIMARY KEY (`c1`),
  KEY `idx_c2` (`c2`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 |
+-------+--------------------------------------------------+
```

此时，上游执行以下 DDL 操作修改表结构（即 DROP 列 c2）：

```sql
ALTER TABLE db2.tbl2 DROP COLUMN c2;
```

当同步该 DDL 语句对应的 binlog event 到下游时，会由于 TiDB 不支持该 DDL 语句而导致 DM 同步任务中断且报如下错误：

```bash
exec sqls[[USE `db2`; ALTER TABLE `db2`.`tbl2` DROP COLUMN `c2`;]] failed, 
err:Error 1105: can't drop column c2 with index covered now
```

**但如果在上游实际执行该 DDL 语句前，你已提前知道该 DDL 语句不被 TiDB 所支持**。则可以使用 `sql-skip` 或 `sql-replace` 为该 DDL 语句预设一个跳过（skip）或替代执行（replace）操作。

对于本示例中的 DDL 语句，由于 TiDB 暂时不支持 DROP 存在索引的列，因此可以使用两条新的 SQL 语句来进行替代执行操作，即可以先 DROP 索引、然后再 DROP 列 c2。

##### 主动替代执行该 SQL 语句

1. 为将要在上游执行的 DDL 语句（经过可选的 router-rule 转换后的 DDL 语句）设计一个能匹配上的正则表达式。
    - 上游将执行的 DDL 语句为 `ALTER TABLE db2.tbl2 DROP COLUMN c2;`。
    - 由于该 DDL 语句不存在 router-rule 转换，可设计如下正则表达式：

        ```sql
        ~(?i)ALTER\s+TABLE\s+`db2`.`tbl2`\s+DROP\s+COLUMN\s+`c2`
        ```

2. 为该 DDL 语句设计将用于替代执行的新的 DDL 语句：

    ```sql
    ALTER TABLE `db2`.`tbl2` DROP INDEX idx_c2;ALTER TABLE `db2`.`tbl2` DROP COLUMN `c2`
    ```

3. 使用 `sql-replace` 预设一个 binlog event 替代执行操作，该操作将在同步该 binlog event 到下游时生效。

    ```bash
    » sql-replace --worker=127.0.0.1:8262 --sql-pattern=~(?i)ALTER\s+TABLE\s+`db2`.`tbl2`\s+DROP\s+COLUMN\s+`c2` test ALTER TABLE `db2`.`tbl2` DROP INDEX idx_c2;ALTER TABLE `db2`.`tbl2` DROP COLUMN `c2`
    {
        "result": true,
        "msg": "",
        "workers": [
            {
                "result": true,
                "worker": "",
                "msg": ""
            }
        ]
    }
    ```

    对应 DM-worker 节点中也可以看到类似如下日志：

    ```bash
    2018/12/28 15:33:13 operator.go:121: [info] [sql-operator] set a new operator 
    uuid: c699a18a-8e75-47eb-8e7e-0e5abde2053c, pattern: ~(?i)ALTER\s+TABLE\s+`db2`.`tbl2`\s+DROP\s+COLUMN\s+`c2`, 
    op: REPLACE, args: ALTER TABLE `db2`.`tbl2` DROP INDEX idx_c2; ALTER TABLE `db2`.`tbl2` DROP COLUMN `c2`
    on replication unit
    ```

4. 在上游 MySQL 执行该 DDL 语句。

5. 观察下游表结构是否变更成功，对应 DM-worker 节点中也可以看到类似如下日志：

    ```bash
    2018/12/28 15:33:45 operator.go:158: [info] [sql-operator] 
    sql-pattern ~(?i)ALTER\s+TABLE\s+`db2`.`tbl2`\s+DROP\s+COLUMN\s+`c2` matched SQL 
    USE `db2`; ALTER TABLE `db2`.`tbl2` DROP COLUMN `c2`;, 
    applying operator uuid: c699a18a-8e75-47eb-8e7e-0e5abde2053c, 
    pattern: ~(?i)ALTER\s+TABLE\s+`db2`.`tbl2`\s+DROP\s+COLUMN\s+`c2`, 
    op: REPLACE, args: ALTER TABLE `db2`.`tbl2` DROP INDEX idx_c2; ALTER TABLE `db2`.`tbl2` DROP COLUMN `c2`
    ```

6. 使用 `query-status` 确认该任务的 `stage` 持续为 `Running`。

7. 使用 `query-error` 确认不存在 DDL 执行错误。

#### 合库合表场景下同步中断后被动执行跳过操作

##### 应用场景

假设现在通过多个 DM-worker 将上游多个 MySQL 实例内的多个表进行合库合表同步到下游 TiDB 的同一个表，并且上游各分表执行了 TiDB 不支持的 DDL 语句。

DM-master 通过 DDL lock 协调 DDL 同步、并请求 DDL lock owner 向下游 TiDB 执行该 DDL 语句后，由于 TiDB 不支持该 DDL 语句，同步任务会报错并中断。

##### 被动跳过 SQL 语句

合库合表场景下，被动跳过 TiDB 不支持的 DDL 语句的处理方式与非合库合表场景下的[同步中断后被动执行跳过操作](#同步中断后被动执行跳过操作)基本一致。

但在合库合表场景下，只需要 DDL lock owner 向下游同步该 DDL 语句，因此在两种场景下的处理过程主要存在以下区别：

1. 合库合表场景下，仅需要对 DDL lock owner 执行 `sql-skip`（`--worker={DDL-lock-owner}`）。

2. 合库合表场景下，仅需要对 DDL lock owner 执行 `resume-task`（`--worker={DDL-lock-owner}`）。

#### 合库合表场景下同步中断前主动执行替代执行操作

##### 应用场景

假设现在存在如下四个上游表需要合并同步到下游的同一个表 ``` `shard_db`.`shard_table` ```：

- MySQL 实例 1 内有 `shard_db_1` 逻辑库，包括 `shard_table_1` 和 `shard_table_2` 两个表。
- MySQL 实例 2 内有 `shard_db_2` 逻辑库，包括 `shard_table_1` 和 `shard_table_2` 两个表。

初始时表结构为：

```sql
mysql> SHOW CREATE TABLE shard_db_1.shard_table_1;
+---------------+------------------------------------------+
| Table         | Create Table                             |
+---------------+------------------------------------------+
| shard_table_1 | CREATE TABLE `shard_table_1` (
  `c1` int(11) NOT NULL,
  `c2` int(11) DEFAULT NULL,
  PRIMARY KEY (`c1`),
  KEY `idx_c2` (`c2`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 |
+---------------+------------------------------------------+
```

此时，在上游所有分表上都执行以下 DDL 操作修改表结构（即 DROP 列 c2）：

```sql
ALTER TABLE shard_db_*.shard_table_* DROP COLUMN c2;
```

则当 DM 通过 sharding DDL lock 协调两个 DM-worker 同步该 DDL 语句、并请求 DDL lock owner 向下游执行该 DDL 语句时，会由于 TiDB 不支持该 DDL 语句而导致同步任务中断且报如下错误：

```bash
exec sqls[[USE `shard_db`; ALTER TABLE `shard_db`.`shard_table` DROP COLUMN `c2`;]] failed,
err:Error 1105: can't drop column c2 with index covered now
```

**但如果在上游实际执行该 DDL 语句前，你已提前知道该 DDL 语句不被 TiDB 所支持**。则可以使用 `sql-skip` 或 `sql-replace` 命令为该 DDL 语句预设一个跳过/替代执行操作。

对于本示例中的 DDL 语句，由于 TiDB 暂时不支持 DROP 存在索引的列，因此可以使用两条新的 SQL 语句来进行替代执行操作，即可以先 DROP 索引、然后再 DROP c2 列。

##### 主动替代执行该 SQL 语句

1. 为将要在上游执行的（经过可选的 router-rule 转换后的）DDL 语句设计一个能匹配上的正则表达式。
    - 上游将执行的 DDL 语句为 `ALTER TABLE shard_db_*.shard_table_* DROP COLUMN c2`。
    - 由于存在 router-rule 会将表名转换为 ``` `shard_db`.`shard_table` ```，可设计如下正则表达式：

        ```sql
        ~(?i)ALTER\s+TABLE\s+`shard_db`.`shard_table`\s+DROP\s+COLUMN\s+`c2`
        ```

2. 为该 DDL 语句设计将用于替代执行的新的 DDL 语句：

    ```sql
    ALTER TABLE `shard_db`.`shard_table` DROP INDEX idx_c2;ALTER TABLE `shard_db`.`shard_table` DROP COLUMN `c2`
    ```

3. 由于这是合库合表场景，因此使用 `--sharding` 参数来由 DM 自动确定替代执行操作只发生在 DDL lock owner 上。

4. 使用 `sql-replace` 预设一个 binlog event 替代执行操作，该操作将在同步该 binlog event 到下游时生效。

    ```bash
    » sql-replace --sharding --sql-pattern=~(?i)ALTER\s+TABLE\s+`shard_db`.`shard_table`\s+DROP\s+COLUMN\s+`c2` test ALTER TABLE `shard_db`.`shard_table` DROP INDEX idx_c2;ALTER TABLE `shard_db`.`shard_table` DROP COLUMN `c2`
     {
         "result": true,
         "msg": "request with --sharding saved and will be sent to DDL lock's owner when resolving DDL lock",
         "workers": [
         ]
     }
    ```

    **DM-master** 节点中也可以看到类似如下日志：
    
    ```bash
    2018/12/28 16:53:33 operator.go:105: [info] [sql-operator] set a new operator 
    uuid: eba35acd-6c5e-4bc3-b0b0-ae8bd1232351, request: name:"test" 
    op:REPLACE args:"ALTER TABLE `shard_db`.`shard_table` DROP INDEX idx_c2;" 
    args:"ALTER TABLE `shard_db`.`shard_table` DROP COLUMN `c2`" 
    sqlPattern:"~(?i)ALTER\\s+TABLE\\s+`shard_db`.`shard_table`\\s+DROP\\s+COLUMN\\s+`c2`" 
    sharding:true
    ```

5. 在上游 MySQL 实例的分表上执行 DDL 语句。

6. 观察下游表结构是否变更成功，对应的 DDL lock **owner** 节点中也可以看到类似如下日志：

    ```bash
    2018/12/28 16:54:35 operator.go:121: [info] [sql-operator] set a new operator 
    uuid: c959f2fb-f1c2-40c7-a1fa-e73cd51736dd, 
    pattern: ~(?i)ALTER\s+TABLE\s+`shard_db`.`shard_table`\s+DROP\s+COLUMN\s+`c2`, 
    op: REPLACE, args: ALTER TABLE `shard_db`.`shard_table` DROP INDEX idx_c2; ALTER TABLE `shard_db`.`shard_table` DROP COLUMN `c2`
    on replication unit
    ```

    ```bash
    2018/12/28 16:54:35 operator.go:158: [info] [sql-operator] 
    sql-pattern ~(?i)ALTER\s+TABLE\s+`shard_db`.`shard_table`\s+DROP\s+COLUMN\s+`c2` matched SQL 
    USE `shard_db`; ALTER TABLE `shard_db`.`shard_table` DROP COLUMN `c2`;, 
    applying operator uuid: c959f2fb-f1c2-40c7-a1fa-e73cd51736dd, 
    pattern: ~(?i)ALTER\s+TABLE\s+`shard_db`.`shard_table`\s+DROP\s+COLUMN\s+`c2`, 
    op: REPLACE, args: ALTER TABLE `shard_db`.`shard_table` DROP INDEX idx_c2; ALTER TABLE `shard_db`.`shard_table` DROP COLUMN `c2`
    ```

    另外，**DM-master** 节点中也可以看到类似如下日志：

    ```bash
    2018/12/28 16:54:35 operator.go:122: [info] [sql-operator] get an operator 
    uuid: eba35acd-6c5e-4bc3-b0b0-ae8bd1232351, request: name:"test" op:REPLACE 
    args:"ALTER TABLE `shard_db`.`shard_table` DROP INDEX idx_c2;" 
    args:"ALTER TABLE `shard_db`.`shard_table` DROP COLUMN `c2`" 
    sqlPattern:"~(?i)ALTER\\s+TABLE\\s+`shard_db`.`shard_table`\\s+DROP\\s+COLUMN\\s+`c2`" 
    sharding:true  
    with key ~(?i)ALTER\s+TABLE\s+`shard_db`.`shard_table`\s+DROP\s+COLUMN\s+`c2` matched SQL 
    USE `shard_db`; ALTER TABLE `shard_db`.`shard_table` DROP COLUMN `c2`;
    ```

    ```bash
    2018/12/28 16:54:36 operator.go:145: [info] [sql-operator] remove an operator 
    uuid: eba35acd-6c5e-4bc3-b0b0-ae8bd1232351, request: name:"test" op:REPLACE 
    args:"ALTER TABLE `shard_db`.`shard_table` DROP INDEX idx_c2;" 
    args:"ALTER TABLE `shard_db`.`shard_table` DROP COLUMN `c2`" 
    sqlPattern:"~(?i)ALTER\\s+TABLE\\s+`shard_db`.`shard_table`\\s+DROP\\s+COLUMN\\s+`c2`" 
    sharding:true
    ```

7. 使用 `query-status` 确认任务的 `stage` 持续为 `Running`，且不存在正阻塞同步的 DDL 语句（`blockingDDLs`）与待解决的 sharding group（`unresolvedGroups`）。

8. 使用 `query-error` 确认不存在 DDL 执行错误。

9. 使用 `show-ddl-locks` 确认不存在待解决的 DDL lock。
