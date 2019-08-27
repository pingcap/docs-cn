---
title: TiDB Lightning 错误排解
category: reference
aliases: ['/docs-cn/tools/lightning/errors/']
---

# TiDB Lightning 错误排解

当 Lightning 遇到不可恢复的错误时便会异常退出，并在日志中记下错误原因。一般可在日志底部找到，也可以搜索 `[error]` 字符串找出中间发生的错误。本文主要描述一些常见的错误及其解决方法。

## 导入速度太慢

Lightning 的正常速度为每条线程每 2 分钟导入一个 256 MB 的数据文件，如果速度远慢于这个数值就是有问题。导入的速度可以检查日志提及 `restore chunk … takes` 的记录，或者观察 Grafana 的监控信息。

导入速度太慢一般有几个原因：

**原因 1**：`region-concurrency` 设定太高，线程间争用资源反而减低了效率。

1. 从日志的开头搜寻 `region-concurrency` 能知道 Lightning 读到的参数是多少。
2. 如果 Lightning 与其他服务（如 Importer）共用一台服务器，必需**手动**将 `region-concurrency` 设为该服务器 CPU 数量的 75%。
3. 如果 CPU 设有限额（例如从 K8s 指定的上限），Lightning 可能无法自动判断出来，此时亦需要**手动**调整 `region-concurrency`。

**原因 2**：表结构太复杂。

每条索引都会额外增加 KV 对。如果有 N 条索引，实际导入的大小就差不多是 mydumper 文件的 N+1 倍。如果索引不太重要，可以考虑先从 schema 去掉，待导入完成后再使用 `CREATE INDEX` 加回去。

**原因 3**：Lightning 版本太旧。

试试最新的版本吧！可能会有改善。

## checksum failed: checksum mismatched remote vs local

**原因**：本地数据源跟目标数据库某个表的校验和不一致。这通常有更深层的原因：

1. 这张表可能本身已有数据，影响最终结果。
2. 如果目标数据库的校验和全是 0，表示没有发生任何导入，有可能是集群太忙无法接收任何数据。
3. 如果数据源是由机器生成而不是从 mydumper 备份的，需确保数据符合表的限制，例如：

    * 自增 (AUTO_INCREMENT) 的列需要为正数，不能为 0。
    * 单一键和主键 (UNIQUE and PRIMARY KEYs) 不能有重复的值。

**解决办法**：

1. 使用 `tidb-lightning-ctl` 把出错的表删除，然后重启 Lightning 重新导入那些表。

    ```sh
    tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-error-destroy=all
    ```

2. 把断点存放在外部数据库（修改 `[checkpoint] dsn`），减轻目标集群压力。

## Checkpoint for … has invalid status: （错误码）

**原因**: [断点续传](/reference/tools/tidb-lightning/checkpoints.md)已启用。Lightning 或 Importer 之前发生了异常退出。为了防止数据意外损坏，Lighting 在错误解决以前不会启动。

错误码是小于 25 的整数，可能的取值是 0、3、6、9、12、14、15、17、18、20、21。整数越大，表示异常退出发生在导入流程越晚的步骤。

**解决办法**:

如果错误原因是非法数据源，使用 `tidb-lightning-ctl` 删除已导入数据，并重启 Lightning。

```sh
tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-error-destroy=all
```

其他解决方法请参考[断点续传的控制](/reference/tools/tidb-lightning/checkpoints.md#断点续传的控制)。

## ResourceTemporarilyUnavailable("Too many open engines …: 8")

**原因**：并行打开的引擎文件 (engine files) 超出 `tikv-importer` 里的限制。这可能由配置错误引起。即使配置没问题，如果 `tidb-lightning` 曾经异常退出，也有可能令引擎文件残留在打开的状态，占据可用的数量。

**解决办法**：

1. 提高 `tikv-importer.toml` 内 `max-open-engines` 的值。这个设置主要由内存决定，计算公式为：

    最大内存使用量 ≈ `max-open-engines` × `write-buffer-size` × `max-write-buffer-number`

2. 降低 `table-concurrency` + `index-concurrency`，使之低于 `max-open-engines`。

3. 重启 `tikv-importer` 来强制移除所有引擎文件 (默认值为 `./data.import/`)。这样也会丢弃导入了一半的表，所以启动 Lightning 前必须清除过期的断点记录：

    ```sh
    tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-error-destroy=all
    ```

## cannot guess encoding for input file, please convert to UTF-8 manually

**原因**：Lightning 只支持 UTF-8 和 GB-18030 编码的表架构。此错误代表数据源不是这里任一个编码。也有可能是文件中混合了不同的编码，例如，因为在不同的环境运行过 `ALTER TABLE`，使表架构同时出现 UTF-8 和 GB-18030 的字符。

**解决办法**：

1. 编辑数据源，保存为纯 UTF-8 或 GB-18030 的文件。
2. 手动在目标数量库创建所有的表，然后设置 `[mydumper] no-schema = true` 跳过创建表的步骤。
3. 设置 `[mydumper] character-set = "binary"` 跳过这个检查。但是这样可能使数据库出现乱码。

## [sql2kv] sql encode error = [types:1292]invalid time format: '{1970 1 1 0 45 0 0}'

**原因**: 一个 `timestamp` 类型的时间戳记录了不存在的时间值。时间值不存在是由于夏时制切换或超出支持的范围（1970 年 1 月 1 日至 2038 年 1 月 19 日）。

**解决办法**:

1. 确保 Lightning 与数据源时区一致。

    * 使用 Ansible 部署的话，修正 [`inventory.ini`] 下的 `timezone` 变量。

        ```ini
        # inventory.ini
        [all:vars]
        timezone = Asia/Shanghai
        ```

    * 手动部署的话，通过设定 `$TZ` 环境变量强制时区设定。

        ```sh
        # 强制使用 Asia/Shanghai 时区
        TZ='Asia/Shanghai' bin/tidb-lightning -config tidb-lightning.toml
        ```

2. 导出数据时，必须加上 `--skip-tz-utc` 选项。
