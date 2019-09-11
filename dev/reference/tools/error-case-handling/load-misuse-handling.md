---
title: Load data 过程常见报错处理
category: reference
---

# Load data 过程常见报错处理

本文介绍了使用 [Loader](/dev/reference/tools/loader.md) 或者 [TiDB Data Migration](/dev/reference/tools/data-migration/overview.md)（以下简称为 DM）进行 load data 过程中常见的因为使用造成的出错场景，以及这些错误发生的原因和处理方式。

## 报错：```Try adjusting the `max_allowed_packet` variable```

在 load data 过程中遇到下面的报错

```
packet for query is too large. Try adjusting the 'max_allowed_packet' variable
```

### 原因

* MySQL client 和 MySQL/TiDB Server 都有 `max_allowed_packet` 配额的限制，如果在使用过程中违反其中任何一个 `max_allowed_packet` 配额，客户端程序就会收到对应的报错。目前最新版本的 Syncer、Loader、DM 和 TiDB Server 的默认 `max_allowed_packet` 配额都为 `64M`。
    * 请使用最新版本，或者最新稳定版本的工具。[下载页面](/dev/reference/tools/download.md)。
* Loader 或 DM 的 load data 处理模块不支持对 dump sqls 文件进行切分，原因是 Mydumper 采用了最简单的编码实现，正如 Mydumper 代码注释 `/* Poor man's data dump code */` 所言。如果在 Loader 或 DM 实现文件切分，那么需要在 `TiDB parser` 基础上实现一个完备的解析器才能正确的处理数据切分，但是随之会带来以下的问题：
    * 工作量大
    * 复杂度高,不容易保证正确性
    * 性能的极大降低

### 解决方案

* 依据上面的原因，在代码层面不能简单的解决这个困扰，我们推荐的方式是：利用 Mydumper 提供的控制 `Insert Statement` 大小的功能 `-s, --statement-size`: `Attempted size of INSERT statement in bytes, default 1000000"`。

    依据默认的 `--statement-size` 设置，Mydumper 默认生成的 `Insert Statement` 大小会尽量接近在 `1M` 左右，使用默认值就可以确保绝大部分情况不会出现该问题。

    有时候在 dump 过程中会出现下面的 `WARN` log，但是这个报错不影响 dump 的过程，只是表达了 dump 的表可能是宽表。

    ```
    Row bigger than statement_size for xxx
    ```

* 如果宽表的单行超过了 `64M`，那么需要修改以下两个配置，并且使之生效。
    * 在 TiDB Server 执行 `set @@global.max_allowed_packet=134217728` （`134217728 = 128M`）
    * 根据实际情况为 Loader 的配置文件或者 `DM task` 配置文件中的 db 配置增加类似 `max-allowed-packet=128M`，然后重启进程或者任务
