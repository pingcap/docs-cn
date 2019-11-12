---
title: BR 使用说明
category: reference
---

# BR 使用说明

Backup and Restore（以下简称 BR）是 TiDB 分布式备份恢复的命令行工具。本文档简单介绍了 BR 的工作原理和它的使用方法。

## 功能介绍

目前，BR 包含以下命令，各个命令的具体用法可以使用 `br SUBCOMMAND --help` 获取使用帮助：

* `br backup` 备份 TiDB 集群
* `br restore` 恢复 TiDB 集群

## 原理介绍

BR 是分布式备份恢复的工具，它将备份和恢复操作下发到各个 TiKV 节点，TiKV 收到命令后执行相应的备份和恢复。在一次备份或恢复中各个 TiKV 都会有个项目的备份路径，TiKV 备份时产生的备份文件将会保存在该路径下，恢复时也会从该路径读取相应的备份文件。

![br-arch](/media/br-arch.png)

## 使用介绍

`br` 的使用由命令（包括子命令）、选项和参数组成。命令即不带 `-` 或者 `--` 的字符，选项即带有 `-` 或者 `--` 的字符，参数即命令或选项字符后紧跟的传递给命令和选项的字符。

如：`br --pd "${PDIP}:2379" backup full -s "local:///tmp/backup"`

* backup: 命令
* full: backup 的子命令
* -s/--storage: 备份保存的路径
* `"local:///tmp/backup"`: -s 的参数，保存的路径为本地磁盘的 `/tmp/backup`。
* --pd: PD 服务地址
* `"${PDIP}:2379"`: --pd 的参数

### 获取帮助

br 由多层命令组成，br 及其所有子命令都可以通过 `-h/--help` 来获取使用帮助，例如 `br backup --help`。

### 连接

`br` 与连接相关的选项有 2 个，分别为：

- `--pd` PD 服务地址，例如 `"${PDIP}:2379"``"${PDIP}:2379"`
- `--connect` TiDB 服务地址，例如 `"root:@tcp(${TiDBIP}:4000)/"`

其中 `--connect` 只适用于 `restore` 子命令，使用 br 恢复功能时必须指定这个选项，否则会报错退出。例如：`br restore table --connect "root:@tcp(${TiDBIP}:4000)/"`。

### 其他全局选项

- `--ca` 指定 PEM 格式的受信任 CA 的证书文件路径。
- `--cert` 指定 PEM 格式的 SSL 证书文件路径。
- `--key` 指定 PEM 格式的 SSL 证书密钥文件路径。
- `--status-addr` 指定 BR metric 信息。

### 备份使用举例

我们可以用 `br backup` 命令来备份 TiDB 集群。backup 有两个子命令，full 和 table。full 用来备份整个数据库，table 用来备份指定的单个表。

#### full 子命令

我们可以通过 `br backup full -h` 或 `br backup full --help` 来获取子命令 full 的使用帮助。

##### 基本用法

例：将集群数据备份到各个 tikv 节点的 `/tmp/backup` 路径

{{< copyable "shell-regular" >}}

```shell
br --pd ${PDIP}:2379 backup full \
    --storage "local:///tmp/backup" \
    --ratelimit 120 \
    --concurrency 4 \
    --log-file backupfull.log
```

上述命令限制了 **每个 TiKV** 执行备份任务的并发数上限和速度上限，同时把 BR 的 log 写到 `backupfull.log` 文件中。

备份期间还有进度条会在终端中显示，当进度条前进到 100% 时，说明备份已完成。在完成备份后，BR 为了确保数据安全性，还会校验备份数据。

进度条效果如下，

```shell
br --pd ${PDIP}:2379 backup full
    --storage "local:///tmp/backup" \
    --ratelimit 120 \
    --concurrency 4 \
    --log-file backupfull.log
Full Backup <---------↖................................................> 17.12%.
```

#### table 子命令

同样可以通过 `br backup table -h` 或 `br backup table --help` 来获取子命令 table 的使用帮助。

##### 基本用法

例：将表 `test.usertable` 备份到各个 tikv 节点的 `/tmp/backup` 路径

{{< copyable "shell-regular" >}}

```shell
br --pd ${PDIP}:2379 backup table \
    --db test \
    --table usertable \
    --storage "local:///tmp/backup" \
    --ratelimit 120 \
    --concurrency 4 \
    --log-file backuptable.log
```

table 命令与 full 命令相比，多了 `--db` 和 `--table`，分别用来指定数据库名和表名，其余选项含义一致。

备份期间还有进度条会在终端中显示，当进度条前进到 100% 时，说明备份已完成。在完成备份后，BR 为了确保数据安全性，还会校验备份数据。

### 恢复使用举例

我们可以用 `br restore` 命令来恢复 TiDB 集群。restore 有三个子命令，full，db 和 table。full 用来恢复整个数据库，db 用来恢复指定的数据库，table 用来恢复指定的单个表。

#### full 子命令

同样可以通过 `br restore full -h` 或 `br restore full --help` 来获取子命令 full 的使用帮助。

##### 基本用法

例：将 `/tmp/backup` 路径中备份数据 **全部** 恢复到集群中

{{< copyable "shell-regular" >}}

```shell
br --pd ${PDIP}:2379 restore full \
    --storage "local:///tmp/backup" \
    --connect "root:@tcp(${TiDBIP}:4000)/" \
    --concurrency 128 \
    --log-file restorefull.log
```

上述命令 `--connect` 指定了需要恢复的集群地址，`--concurrency` 指定了这个恢复任务内部的子任务的并发数，同时把 BR 的 log 写到 `restorefull.log` 文件中。

恢复期间还有进度条会在终端中显示，当进度条前进到 100% 时，说明恢复已完成。在完成恢复后，BR 为了确保数据安全性，还会校验恢复数据。

进度条效果如下：

```shell
br --pd ${PDIP}:2379 restore full \
    --storage "local:///tmp/backup" \
    --connect "root:@tcp(${TiDBIP}:4000)/" \
    --log-file restorefull.log
Full Restore <---------↖...............................................> 17.12%.
```

#### db 子命令

同样可以通过 `br restore db -h` 或 `br restore db --help` 来获取子命令 db 的使用帮助。

##### 基本用法

例：将 `/tmp/backup` 路径中备份数据中的 **某个数据库** 恢复到集群中

{{< copyable "shell-regular" >}}

```shell
br --pd ${PDIP}:2379 restore db \
    --db "test" \
    --storage "local:///tmp/backup" \
    --connect "root:@tcp(${TiDBIP}:4000)/" \
    --log-file restorefull.log
```

上述命令 `--db` 指定了需要恢复的数据库名字，其余选项含义与 retstore full 一致。

#### table 子命令

同样可以通过 `br restore table -h` 或 `br restore table --help` 来获取子命令 table 的使用帮助。

##### 基本用法

例：将 `/tmp/backup` 路径中备份数据中的 **某个数据表** 恢复到集群中

{{< copyable "shell-regular" >}}

```shell
br --pd ${PDIP}:2379 restore table \
    --db "test" \
    --table "usertable" \
    --storage "local:///tmp/backup" \
    --connect "root:@tcp(${TiDBIP}:4000)/" \
    --log-file restorefull.log
```

上述命令 `--table` 指定了需要恢复的表名字，其余选项含义与 retore db 一致。

## 最佳实践

- 我们推荐在 `-s` 指定的备份路径上挂载一个共享存储，比如 NFS。这样能方便收集和管理备份。
- 在使用共享存储时，我们推荐使用高吞吐的存储硬件，存储的吞吐限制了备份/恢复的速度。
- 我们推荐在业务低峰起执行备份，这样能最大程度地减少对业务的影响。

## 注意事项

- TiDB 执行 DDL 期间不能执行备份。
- 目前只支持在全新的集群上执行。
- 当备份时间可能超过 10 分钟时，我们需要调整 GC lifetime。在备份完成后，需要将 GC lifetime 调整为默认值 10 分钟。

    {{< copyable "sql" >}}

    ```
    mysql -h${TiDBIP} -P4000 -u${TIDB_USER} ${password_str} -Nse \
        "update mysql.tidb set variable_value='720h' where variable_name='tikv_gc_life_time'";
    ```

- 为了加快恢复速度，可以在恢复前，使用 pd-ctl 关闭相关的 scheduler。在恢复完成后，需要将 这些 scheduler 加回来。

    关闭 scheduler：

    {{< copyable "shell-regular" >}}

    ```shell
    ./pd-ctl -u ${PDIP}:2379 scheduler remove balance-hot-region-scheduler
    ./pd-ctl -u ${PDIP}:2379 scheduler remove balance-leader-scheduler
    ./pd-ctl -u ${PDIP}:2379 scheduler remove balance-region-scheduler
    ```

    添加 scheduler：

    {{< copyable "shell-regular" >}}

    ```shell
    ./pd-ctl -u ${PDIP}:2379 scheduler add balance-hot-region-scheduler
    ./pd-ctl -u ${PDIP}:2379 scheduler add balance-leader-scheduler
    ./pd-ctl -u ${PDIP}:2379 scheduler add balance-region-scheduler
    ```
