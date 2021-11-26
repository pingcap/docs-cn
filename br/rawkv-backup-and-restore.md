---
title: 使用 BR 进行 RawKV 的备份恢复
summary: 了解如何使用 BR 进行 RawKV 数据备份和恢复。
---

# 使用 BR 行进行 RawKV 的备份恢复

> **警告：**
>
> Raw KV 备份和恢复功能还在实验中，没有经过完备的测试。暂时请避免在生产环境中使用该功能。
> 如果在使用过程中遇到问题，可以在 [AskTUG](https://asktug.com/) 社区中提问。
>

## Raw KV 备份（实验性功能）

在某些使用场景下，TiKV 可能会独立于 TiDB 运行。考虑到这点，BR 也提供跳过 TiDB 层，直接备份 TiKV 中数据的功能：

{{< copyable "shell-regular" >}}

```shell
br backup raw --pd $PD_ADDR \
    -s "local://$BACKUP_DIR" \
    --start 31 \
    --ratelimit 128 \
    --end 3130303030303030 \
    --format hex \
    --cf default
```

以上命令会备份 default CF 上 `[0x31, 0x3130303030303030)` 之间的所有键到 `$BACKUP_DIR` 去。

这里，`--start` 和 `--end` 的参数会先依照 `--format` 指定的方式解码，再被送到 TiKV 上去，目前支持以下解码方式：

- "raw"：不进行任何操作，将输入的字符串直接编码为二进制格式的键。
- "hex"：将输入的字符串视作十六进制数字。这是默认的编码方式。
- "escape"：对输入的字符串进行转义之后，再编码为二进制格式。


## Raw KV 恢复（实验性功能）

和 [Raw KV 备份](#raw-kv-备份实验性功能)相似地，恢复 Raw KV 的命令如下：

{{< copyable "shell-regular" >}}

```shell
br restore raw --pd $PD_ADDR \
    -s "local://$BACKUP_DIR" \
    --start 31 \
    --end 3130303030303030 \
    --ratelimit 128 \
    --format hex \
    --cf default
```

以上命令会将范围在 `[0x31, 0x3130303030303030)` 的已备份键恢复到 TiKV 集群中。这里键的编码方式和备份时相同。
