---
title: TiDB Lightning 断点续传
category: reference
---

# TiDB Lightning 断点续传

大量的数据导入一般耗时数小时至数天，长时间运行的进程会有一定机率发生非正常中断。如果每次重启都从头开始，
就会浪费掉之前已成功导入的数据。为此，Lightning 提供了“断点续传”的功能，即使 `tidb-lightning` 崩溃，在重启时仍然接着之前的进度继续工作。

本文主要介绍 TiDB Lightning 断点续传的启用与配置、断点的存储，以及断点续传的控制。

## 断点续传的启用与配置

```toml
[checkpoint]
# 启用断点续传。
# 导入时，Lightning 会记录当前进度。
# 若 Lightning 或其他组件异常退出，在重启时可以避免重复再导入已完成的数据。
enable = true

# 存储断点的方式
#  - file：存放在本地文件系统（要求 v2.1.1 或以上）
#  - mysql：存放在兼容 MySQL 的数据库服务器
driver = "file"

# 存储断点的架构名称（数据库名称）
# 仅在 driver = "mysql" 时生效
# schema = "tidb_lightning_checkpoint"

# 断点的存放位置
#
# 若 driver = "file"，此参数为断点信息存放的文件路径。
# 如果不设置改参数则默认为 `/tmp/CHECKPOINT_SCHEMA.pb`
#
# 若 driver = "mysql"，此参数为数据库连接参数 (DSN)，格式为“用户:密码@tcp(地址:端口)/”。
# 默认会重用 [tidb] 设置目标数据库来存储断点。
# 为避免加重目标集群的压力，建议另外使用一个兼容 MySQL 的数据库服务器。
# dsn = "/tmp/tidb_lightning_checkpoint.pb"

# 导入成功后是否保留断点。默认为删除。
# 保留断点可用于调试，但有可能泄漏数据源的元数据。
# keep-after-success = false
```

## 断点的存储

TiDB Lightning 支持两种存储方式：本地文件或 MySQL 数据库。

* 若 `driver = "file"`，断点会存放在一个本地文件，其路径由 `dsn` 参数指定。由于断点会频繁更新，建议将这个文件放到写入次数不受限制的盘上，例如 RAM disk。

* 若 `driver = "mysql"`，断点可以存放在任何兼容 MySQL 5.7 或以上的数据库中，包括 MariaDB 和 TiDB。在没有选择的情况下，默认会存在目标数据库里。

目标数据库在导入期间会有大量的操作，若使用目标数据库来存储断点会加重其负担，甚至有可能造成通信超时丢失数据。因此，**强烈建议另外部署一台兼容 MySQL 的临时数据库服务器**。此数据库也可以安装在 `tidb-lightning` 的主机上。导入完毕后可以删除。

## 断点续传的控制

若 `tidb-lightning` 因不可恢复的错误而退出（例如数据出错），重启时不会使用断点，而是直接报错离开。为保证已导入的数据安全，这些错误必须先解决掉才能继续。使用 `tidb-lightning-ctl` 工具可以标示已经恢复。

### `--checkpoint-error-destroy`

{{< copyable "shell-regular" >}}

```shell
tidb-lightning-ctl --checkpoint-error-destroy='`schema`.`table`'
```

该命令会让失败的表从头开始整个导入过程。选项中的架构和表名必须以反引号 (`` ` ``) 包裹，而且区分大小写。

- 如果导入 `` `schema`.`table` `` 这个表曾经出错，这条命令会：

    1. 从目标数据库移除 (DROP) 这个表，清除已导入的数据。
    2. 将断点重设到“未开始”的状态。

- 如果 `` `schema`.`table` `` 没有出错，则无操作。

传入 "all" 会对所有表进行上述操作。这是最方便、安全但保守的断点错误解决方法：

{{< copyable "shell-regular" >}}

```shell
tidb-lightning-ctl --checkpoint-error-destroy=all
```

### `--checkpoint-error-ignore`

{{< copyable "shell-regular" >}}

```shell
tidb-lightning-ctl --checkpoint-error-ignore='`schema`.`table`' &&
tidb-lightning-ctl --checkpoint-error-ignore=all
```

如果导入 `` `schema`.`table` `` 这个表曾经出错，这条命令会清除出错状态，如同没事发生过一样。传入 "all" 会对所有表进行上述操作。

> **注意：**
>
> 除非确定错误可以忽略，否则不要使用这个选项。如果错误是真实的话，可能会导致数据不完全。启用校验和 (CHECKSUM) 可以防止数据出错被忽略。

### `--checkpoint-remove`

{{< copyable "shell-regular" >}}

```shell
tidb-lightning-ctl --checkpoint-remove='`schema`.`table`' &&
tidb-lightning-ctl --checkpoint-remove=all
```

无论是否有出错，把表的断点清除。

### `--checkpoint-dump`

{{< copyable "shell-regular" >}}

```shell
tidb-lightning-ctl --checkpoint-dump=output/directory
```

将所有断点备份到传入的文件夹，主要用于技术支持。此选项仅于 `driver = "mysql"` 时有效。
