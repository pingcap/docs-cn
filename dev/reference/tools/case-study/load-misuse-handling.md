---
title: load data 常见的错误用法
category: reference
---

# Load data 常见的报错处理

本片文章主要介绍一些在使用 [loader]() 或者 [dm]() 进行 load data 过程中常见的错误使用造成的出错场景，以及这些错误发生的原因和处理方式。


## Try adjusting the `max_allowed_packet` variable

在 load data 过程中遇到下面的报错

```
packet for query is too large. Try adjusting the 'max_allowed_packet' variable
```

### 原因

* MySQL client 和 MySQL/TiDB Server 都对 `max_allowed_packet` 有配额限制，如果违反其中任何一个 `max_allowed_packet` 配额就会收到对应的报错。目前 syncer/loader/dm 和 TiDB server 的默认 `max_allowed_packet` 配额都为 `64M`。
  * 使用最新版本，或者最新稳定版本的对应工具，[dowload page](/reference/tools/download.md)
* loader/dm 的 load data 处理模块不支持对 dump 文件进行切分，原因是 MyDumper 的编码简单设计，正如 MyDumper 代码注释 `/* Poor man's data dump code */`，需要实现在 TiDB parser 基础上实现一个完备的解析器才能正确的处理数据切分，但是会带来工作量、复杂度提高，以及性能的极大降低。


### 解决方案

* 依据上面的原因，在代码层面不能简单的解决这个困扰，我们推荐的方式是：利用 `MyDumper` 提供的控制 `Insert Statement` 大小的功能 `-s, --statement-size`: `Attempted size of INSERT statement in bytes, default 1000000"`。

  依据默认的 `--statement-size` 设置，`MyDumper` 默认生成的 `Insert Statement` 大小会尽量接近在 `1M` 左右，使用默认值就可以杜绝绝大部分这种问题的发生。

  有时候在 dump 过程中会出现下面的 `WARN` log, 这个报错不影响 dump 的过程，只是提示了 dump 的表可能是是宽表。

  ```
  Row bigger than statement_size for xxx
  ```

* 如果宽表的单行超过了 `64M`, 那么需要修改两个配置
  * 根据实际情况为配置 loader/dm 的 db 配置增加类似 `max-allowed-packet=128M`
  * 修改 TiDB server 的 `max_allowed_packet` 为 `128M`