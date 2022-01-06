---
title: TiFlash 命令行参数
aliases: ['/docs-cn/dev/tiflash/tiflash-command-line-flags/']
---

# TiFlash 命令行参数

本文介绍了 TiFlash 的命令行启动参数。

## `server --config-file`

+ 指定 TiFlash 的配置文件路径
+ 默认：""
+ 必须指定配置文件，详细的配置项请参阅 [TiFlash 配置参数](/tiflash/tiflash-configuration.md)

## `dttool bench`

- 提供 DTFile 的简单 IO 速度测试。
- 参数
    - `--version`：DTFile 的版本，可选值为 1 和 2。1 为传统格式，2 为新版 checksum 对应的 DTFile 格式。
    - `--algorithm`：检验哈希算法，可选值为 xxh3，city128，crc32，crc64，none。
    - `--frame`：校验帧大小，默认为 1048576。
    - `--column`：测试表宽度，默认为 100。
    - `--size`：测试表长度，默认为 1000。
    - `--field`：测试表字段长度上限，默认为 1024。
    - `--random`：随机数种子。如未提供，该值从系统熵池抽取。
    - `--encryption`：启用加密功能。
    - `--repeat`：性能测试采样次数，默认为 5。
    - `--workdir`：临时数据文件夹，应指向需要测试的文件系统化，默认为 /tmp/test。

## `dttool inspect`

- 检查 DTFile 的完整性
- 参数
    - `--config-file` TiFlash 的配置文件，应当与 server 保持一致；当使用配置文件时，本地的 Tiflash 服务器实例需要退出；见 `--imitative` 选项
    - `--check` 进行哈希校验
    - `--file-id` 对应 DTFile 的 ID；如 dmf_123 对应的 ID 是 123
    - `--imitative` 当不使用 DTFile 的加密功能时，可以使用本选项避免使用配置文件和连接PD
    - `--workdir` 指向 dmf_xxx 的父级目录

## `dttool migrate`

- 迁移 DTFile 的文件格式 （用于测试和原地降级）

- 参数
    - `--version` 目标文件格式版本；见 bench 对应参数
    - `--algorithm` 目标检验哈希算法，仅在 version=2 时有用；见 bench 对应参数
    - `--frame` 目标校验帧大小，仅在 version=2 时有用；见 bench 对应参数
    - `--compression` 目标压缩算法，支持 lz4, lz4hc, zstd, none；默认值 lz4
    - `--level` 目标压缩等级，默认值 -1 （表示自动模式）；不同压缩算法取值范围不同。
    - `--file-id` 见 inspect 对应参数
    - `--imitative` 见 inspect 对应参数
    - `--workdir` 见 inspect 对应参数
    - `--config-file` 见 inspect 对应参数
    - `--dry` 空跑模式，只输出迁移过程
    - `--nokeep` 不保留原数据（不开启时会产生 dmf_xxx.old 文件）
