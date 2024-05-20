---
title: TiFlash 命令行参数
aliases: ['/docs-cn/dev/tiflash/tiflash-command-line-flags/']
summary: TiFlash 的命令行启动参数包括 server --config-file、dttool migrate、dttool bench 和 dttool inspect。server --config-file 用于指定配置文件路径，dttool migrate 用于迁移 DTFile 的文件格式，dttool bench 用于提供 DTFile 的简单 IO 速度测试，dttool inspect 用于检查 DTFile 的完整性。每个命令都有对应的参数，可以根据需求进行配置。警告：TiFlash 目前只支持默认压缩等级的 LZ4 算法，自定义压缩参数并未经过大量测试。注意：为保证安全，DTTool 在迁移模式下会尝试对工作目录进行加锁。
---

# TiFlash 命令行参数

本文介绍了 TiFlash 的命令行启动参数。

## `server --config-file`

+ 指定 TiFlash 的配置文件路径
+ 默认：""
+ 必须指定配置文件，详细的配置项请参阅 [TiFlash 配置参数](/tiflash/tiflash-configuration.md)

## `dttool migrate`

- 迁移 DTFile 的文件格式 （用于测试和原地降级）。数据迁移的单位为单个 DTFile。如果想进行整表迁移，通常需要定位到所有形如 `<data dir>/t_<table id>/stable/dmf_<file id>` 的路径，逐一进行迁移。可以结合脚本来自动进行这一操作。

- 使用场景：
    - 当需要从开启了数据校验功能 (`storage.format_version` >= 3) 的 TiFlash v5.4 及以上版本降级回以前的版本时，可以使用此工具完成数据格式降级。
    - 当升级到 TiFlash v5.4 及以上，并希望对存量数据也加上数据校验功能以加固数据检验时，可以使用此工具完成数据格式升级。
    - 测试不同配置的 DTFile 空间占用和读取速度。
    - 当需要从开启了合并小文件功能 (`storage.format_version` >= 5) 的 TiFlash v7.3 及以上版本降级回以前的版本时，可以使用此工具完成数据格式的降级。

- 参数：
    - `--imitative`：当不使用 DTFile 的加密功能时，可以使用本选项避免使用配置文件和连接 PD。
    - `--version`：DTFile 的目标版本，可选值为 1、2、3，默认为 2。1 为传统格式，2 为 checksum 对应的 DTFile 格式，3 为合并小文件后的 DTFile 格式。
    - `--algorithm`：检验哈希算法，可选值为 xxh3，city128，crc32，crc64，none，默认为 xxh3，仅在 version=2 时有用。
    - `--frame`：校验帧大小，默认为 1048576，仅在 version=2 时有用。
    - `--compression`：目标压缩算法，可选值为 LZ4（默认）、LZ4HC、zstd 和 none。
    - `--level`：目标压缩等级，不指定则根据压缩算法默认使用推荐的压缩级别。如果 `compression` 设置为 `LZ4` 或 `zstd`，则默认设置为 1；如果 `compression` 设置为 `LZ4HC`，则默认设置为 9。
    - `--config-file`：dttool migrate 的配置文件应当与 server 模式下的[配置文件](/tiflash/tiflash-command-line-flags.md#server---config-file)保持一致。见 `--imitative` 选项。
    - `--file-id`：对应 DTFile 的 ID，如 `dmf_123` 对应的 ID 是 123。
    - `--workdir`：指向 `dmf_xxx` 的父级目录。
    - `--dry`：空跑模式，只输出迁移过程。
    - `--nokeep`：不保留原数据。不开启该选项时，会产生 `dmf_xxx.old` 文件。

> **警告：**
>
> 虽然 TiFlash 可以读取自定义压缩算法和压缩等级的 DTFile，但目前正式支持的只有默认压缩等级的 LZ4 算法。自定义压缩参数并未经过大量测试，仅作实验。

> **注意：**
>
> 为保证安全 DTTool 在迁移模式下会尝试对工作目录进行加锁，因此同一工作目录下同一时间只能有一个 DTTool 执行迁移工作。如果您在中途强制停止 DTTool，可能会因锁未释放导致后面在运行 DTTool 时工具拒绝进行迁移工作。
> 如果您遇到这种情况，在保证安全的前提下，可以手动删除工作目录下的 LOCK 文件来释放锁。

## `dttool bench`

- 提供 DTFile 的简单 IO 速度测试。
- 参数：
    - `--version`：DTFile 的版本，见 [dttool migrate](#dttool-migrate) 对应参数。
    - `--algorithm`：检验哈希算法，见 [dttool migrate](#dttool-migrate) 对应参数。
    - `--frame`：校验帧大小，见 [dttool migrate](#dttool-migrate) 对应参数。
    - `--column`：测试表宽度，默认为 100。
    - `--size`：测试表长度，默认为 1000。
    - `--field`：测试表字段长度上限，默认为 1024。
    - `--random`：随机数种子。如未提供，该值从系统熵池抽取。
    - `--encryption`：启用加密功能。
    - `--repeat`：性能测试采样次数，默认为 5。
    - `--workdir`：临时数据文件夹，应指向需要测试的文件系统下的路径，默认为 /tmp/test。

## `dttool inspect`

- 检查 DTFile 的完整性。数据校验的单位为单个 DTFile。如果想进行整表校验，通常需要定位到所有形如 `<data dir>/t_<table id>/stable/dmf_<file id>` 的路径，逐一进行校验。可以结合脚本来自动进行这一操作。

- 使用场景：
    - 完成格式升降级后进行完整性检测。
    - 将原有数据文件搬迁至新环境后进行完整性检测。

- 参数：
    - `--config-file`：dttool bench 的配置文件，见 [dttool migrate](#dttool-migrate) 对应参数。
    - `--check`：进行哈希校验。
    - `--file-id`：对应 DTFile 的 ID，见 [dttool migrate](#dttool-migrate) 对应参数。
    - `--imitative`：模拟数据库上下文，见 [dttool migrate](#dttool-migrate) 对应参数。
    - `--workdir`：数据文件夹，见 [dttool migrate](#dttool-migrate) 对应参数。
