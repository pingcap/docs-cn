---
title: TiDB 快照备份与恢复命令行手册
summary: 介绍备份与恢复 TiDB 集群快照的命令行。
---

# TiDB 快照备份与恢复命令行手册

本文按备份恢复的场景介绍快照备份和恢复的命令行，包括：

- [备份集群快照](#备份集群快照)
- [备份 TiDB 集群指定库表的数据](#备份-tidb-集群指定库表的数据)
    - [备份单个数据库的数据](#备份单个数据库的数据)
    - [备份单张表的数据](#备份单张表的数据)
    - [使用表库过滤功能备份多张表的数据](#使用表库过滤功能备份多张表的数据)
- [备份统计信息](#备份统计信息)
- [备份数据加密](#备份数据加密)
- [恢复快照备份数据](#恢复快照备份数据)
- [恢复备份数据中指定库表的数据](#恢复备份数据中指定库表的数据)
    - [恢复单个数据库的数据](#恢复单个数据库的数据)
    - [恢复单张表的数据](#恢复单张表的数据)
    - [使用表库功能过滤恢复数据](#使用表库功能过滤恢复数据)
    - [恢复系统表中存储的执行计划绑定信息](#恢复系统表中存储的执行计划绑定信息)
- [恢复加密的快照备份数据](#恢复加密的快照备份数据)

如果你想了解如何进行快照备份与恢复，可以参考以下教程：

- [TiDB 快照备份与恢复使用指南](/br/br-snapshot-guide.md)
- [TiDB 集群备份与恢复实践示例](/br/backup-and-restore-use-cases.md)

## 备份集群快照

执行 `br backup full` 命令，可以备份 TiDB 最新的或者指定时间点的快照数据。执行 `br backup full --help` 可获取该命令的使用帮助。

```shell
br backup full \
    --pd "${PD_IP}:2379" \
    --backupts '2022-09-08 13:30:00' \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --ratelimit 128 \
    --log-file backupfull.log
```

以上命令中：

- `--backupts`：快照对应的物理时间点。如果该快照的数据已经被 GC，那么 `br backup` 命令会报错退出；如果没有指定该参数，br 命令行工具会选取备份开始的时间点所对应的快照。
- `--ratelimit`：**每个 TiKV** 执行备份任务的速度上限（单位 MiB/s）。
- `--log-file`：备份日志写入的目标文件。

> **注意：**
>
> BR 工具已支持自适应 GC，会自动将 `backupTS`（默认是最新的 PD timestamp）注册到 PD 的 `safePoint`，保证 TiDB 的 GC Safe Point 在备份期间不会向前移动，即可避免手动设置 GC。

备份期间终端会显示进度条，效果如下。当进度条达到 100% 时，表示备份完成。

```shell
Full Backup <---------/................................................> 17.12%.
```

## 备份 TiDB 集群指定库表的数据

br 工具支持只备份集群快照和增量数据中指定库或表的局部数据。在快照备份和增量数据备份的基础上，该功能可过滤掉不需要的数据，只备份关键业务的数据。

### 备份单个数据库的数据

执行 `br backup db` 命令，可备份集群中指定单个数据库的数据。

下面是将数据库 `test` 备份到 Amazon S3 的示例：

```shell
br backup db \
    --pd "${PD_IP}:2379" \
    --db test \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --ratelimit 128 \
    --log-file backuptable.log
```

`db` 子命令的选项为 `--db`，用来指定数据库名。其他选项的含义与[备份 TiDB 集群快照](#备份集群快照)相同。

### 备份单张表的数据

执行 `br backup table` 命令，可备份集群中指定单张表的数据。

下面是将表 `test.usertable` 备份到 Amazon S3 的示例：

```shell
br backup table \
    --pd "${PD_IP}:2379" \
    --db test \
    --table usertable \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --ratelimit 128 \
    --log-file backuptable.log
```

`table` 子命令有 `--db` 和 `--table` 两个选项，分别用来指定数据库名和表名。其他选项的含义与[备份 TiDB 集群快照](#备份集群快照)相同。

### 使用表库过滤功能备份多张表的数据

如果你需要以更复杂的过滤条件来备份多个库或表，执行 `br backup full` 命令，并使用 `--filter` 或 `-f` 来指定[表库过滤](/table-filter.md)规则。

下面是将所有符合 `db*.tbl*` 条件的表的数据备份到 Amazon S3 的示例：

```shell
br backup full \
    --pd "${PD_IP}:2379" \
    --filter 'db*.tbl*' \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --ratelimit 128 \
    --log-file backupfull.log
```

## 备份统计信息

从 TiDB v7.5.0 开始，br 命令行工具引入参数 `--ignore-stats`。当指定该参数值为 `false` 时，br 命令行工具支持备份数据库的列、索引、和表级别的统计信息，因此从备份中恢复的 TiDB 数据库不再需要手动运行统计信息收集任务，也无需等待自动收集任务的完成，从而简化了数据库维护工作，并提升了查询性能。

当未指定该参数值为 `false` 时，br 命令行工具默认 `--ignore-stats=true`，即在备份数据时不备份统计信息。

下面是备份集群快照数据并备份表统计信息的示例，需要设置 `--ignore-stats=false`：

```shell
br backup full \
--storage local:///br_data/ --pd "${PD_IP}:2379" --log-file restore.log \
--ignore-stats=false
```

完成上述配置后，在恢复数据时，如果备份中包含了统计信息，br 命令行工具在恢复数据时会自动恢复备份的统计信息（从 v8.0.0 起，br 命令行工具新增 `--load-stats` 参数来控制是否恢复备份的统计信息，默认恢复，一般情况下无需关闭）：

```shell
br restore full \
--storage local:///br_data/ --pd "${PD_IP}:2379" --log-file restore.log 
```

备份恢复功能在备份时，将统计信息通过 JSON 格式存储在 `backupmeta` 文件中。在恢复时，将 JSON 格式的统计信息导入到集群中。详情请参考 [LOAD STATS](/sql-statements/sql-statement-load-stats.md)。

## 备份数据加密

> **警告：**
>
> 当前该功能为实验特性，不建议在生产环境中使用。

br 命令行工具支持在备份端，或备份到 Amazon S3 的时候在[存储服务端进行备份数据加密](/br/backup-and-restore-storages.md#amazon-s3-存储服务端加密备份数据)，你可以根据自己情况选择其中一种使用。

自 TiDB v5.3.0 起，你可配置下列参数在备份过程中实现数据加密：

- `--crypter.method`：加密算法，支持 `aes128-ctr`、`aes192-ctr` 和 `aes256-ctr` 三种算法，缺省值为 `plaintext`，表示不加密
- `--crypter.key`：加密密钥，十六进制字符串格式，`aes128-ctr` 对应 128 位（16 字节）密钥长度，`aes192-ctr` 为 24 字节，`aes256-ctr` 为 32 字节
- `--crypter.key-file`：密钥文件，可直接将存放密钥的文件路径作为参数传入，此时 `crypter.key` 不需要配置

备份加密的示例如下：

```shell
br backup full\
    --pd ${PD_IP}:2379 \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --crypter.method aes128-ctr \
    --crypter.key 0123456789abcdef0123456789abcdef
```

> **注意：**
>
> - 密钥丢失，备份的数据将无法恢复到集群中。
> - 加密功能需在 br 工具和 TiDB 集群都不低于 v5.3.0 的版本上使用，且加密备份得到的数据无法在低于 v5.3.0 版本的集群上恢复。

## 恢复快照备份数据

执行 `br restore full` 命令，可将集群恢复到快照备份对应的数据状态。

```shell
br restore full \
    --pd "${PD_IP}:2379" \
    --with-sys-table \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --ratelimit 128 \
    --log-file restorefull.log
```

以上命令中，

- `--with-sys-table`：恢复集群数据的同时恢复**部分系统表**的数据，包括恢复账号权限数据、 SQL Binding 信息和统计信息数据(详细参考[备份统计信息](/br/br-snapshot-manual.md#备份统计信息))，但暂不支持恢复统计信息表 (`mysql.stat_*`) 和系统参数 (`mysql.tidb`, `mysql.global_variables`) 等信息，更多信息详见[恢复 `mysql` 数据库下的表](/br/br-snapshot-guide.md#恢复-mysql-数据库下的表)。
- `--ratelimit`：**每个 TiKV** 执行恢复任务的速度上限（单位 MiB/s）。
- `--log-file`：备份日志写入的目标文件。

恢复期间终端会显示进度条，效果如下。当进度条达到 100% 时，表示恢复完成。在完成恢复后，br 工具为了确保数据安全性，还会校验恢复数据。

```shell
Full Restore <---------/...............................................> 17.12%.
```

## 恢复备份数据中指定库表的数据

br 命令行工具支持只恢复备份数据中指定库/表的局部数据。该功能在恢复过程中过滤掉不需要的数据，可以用于往 TiDB 集群上恢复指定库/表的数据。

### 恢复单个数据库的数据

执行 `br restore db` 命令，可将单个数据库恢复到对应的状态。

示例：恢复 S3 中的库 `test` 的数据：

```shell
br restore db \
    --pd "${PD_IP}:2379" \
    --db "test" \
    --ratelimit 128 \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --log-file restore_db.log
```

以上命令中 `--db` 选项指定了需要恢复的数据库名字。其余选项的含义与[恢复快照备份数据](#恢复快照备份数据)相同。

> **注意：**
>
> 由于备份数据的元文件 `backupmeta` 记录了数据库名 `--db`，因此只能将数据恢复到同名的数据库，否则无法恢复成功。推荐把备份文件恢复到另一个集群的同名数据库中。

### 恢复单张表的数据

执行 `br restore table` 命令，可将单张表的数据恢复到对应的状态。

下面是恢复 Amazon S3 中 `test.usertable` 表数据的示例：

```shell
br restore table \
    --pd "${PD_IP}:2379" \
    --db "test" \
    --table "usertable" \
    --ratelimit 128 \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --log-file restore_table.log
```

以上命令中 `--table` 选项指定了需要恢复的表名。其余选项的含义与[恢复单个数据库](#恢复单个数据库的数据)相同。

### 使用表库功能过滤恢复数据

如果你需要用复杂的过滤条件来恢复多个表，执行 `br restore full` 命令，并用 `--filter` 或 `-f` 指定使用[表库过滤](/table-filter.md)。

下面是恢复 Amazon S3 中符合 `db*.tbl*` 条件的表的数据的示例：

```shell
br restore full \
    --pd "${PD_IP}:2379" \
    --filter 'db*.tbl*' \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --log-file restorefull.log
```

### 恢复系统表中存储的执行计划绑定信息

如果你需要恢复原集群的执行计划绑定信息，执行 `br restore full` 命令，设置 `--with-sys-table` 并通过 `--filter` 或 `-f` 指定需要恢复的系统表。

下面是恢复 `mysql.bind_info` 表的示例：

```shell
br restore full \
    --pd "${PD_IP}:2379" \
    --filter 'mysql.bind_info' \
    --with-sys-table \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --log-file restore_system_table.log
```

恢复完成后，可以通过 [`SHOW GLOBAL BINDINGS`](/sql-statements/sql-statement-show-bindings.md) 检查执行计划绑定信息的恢复情况：

```sql
SHOW GLOBAL BINDINGS;
```

当前执行计划绑定信息在备份恢复后的动态加载仍在优化中（相关的 issue 为 [#46527](https://github.com/pingcap/tidb/issues/46527) 和 [#46528](https://github.com/pingcap/tidb/issues/46528)），你需要手动刷新执行计划绑定信息。

```sql
-- 确保 mysql.bind_info 表中 builtin_pseudo_sql_for_bind_lock 的记录仅 1 行，如果多于 1 行，需要手动删除
SELECT count(*) FROM mysql.bind_info WHERE original_sql = 'builtin_pseudo_sql_for_bind_lock';
DELETE FROM bind_info WHERE original_sql = 'builtin_pseudo_sql_for_bind_lock' LIMIT 1;

-- 强制重新加载绑定信息
ADMIN RELOAD BINDINGS;
```

## 恢复加密的快照备份数据

> **警告：**
>
> 当前该功能为实验特性，不建议在生产环境中使用。

在对数据做加密备份后，恢复操作需传入相应的解密参数，解密算法或密钥不正确则无法恢复，解密参数和加密参数一致即可。解密恢复的示例如下：

```shell
br restore full\
    --pd "${PD_IP}:2379" \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --crypter.method aes128-ctr \
    --crypter.key 0123456789abcdef0123456789abcdef
```
