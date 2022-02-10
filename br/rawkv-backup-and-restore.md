---
title: 使用 BR 备份和恢复 RawKV 数据
summary: 了解如何使用 BR 备份和恢复 RawKV 数据。
---

# RawKV 备份和恢复

BR 支持对单独使用 RawKV（TiKV 和 PD）产品进行备份和恢复，下文介绍可 RawKV 备份恢复的所有相关知识。

> **警告：**
>
> RawKV 备份和恢复功能还在实验中，没有经过完备的测试。暂时请避免在生产环境中使用该功能。
> 如果在使用过程中遇到问题，可以在 [AskTUG](https://asktug.com/) 社区中提问。
>

## 备份 RawKV（实验性功能）

在某些使用场景下，TiKV 可能会独立于 TiDB 运行。考虑到这点，BR 提供跳过 TiDB 层直接备份 TiKV 数据的功能：

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

以上命令会将 default CF 上 `[0x31, 0x3130303030303030)` 之间的所有键备份到 `$BACKUP_DIR`。

这里，`--start` 和 `--end` 的参数会先依照 `--format` 指定的方式解码，再被送到 TiKV 上去，目前支持以下解码方式：

- "raw"：不进行任何操作，将输入的字符串直接编码为二进制格式的键。
- "hex"：将输入的字符串视作十六进制数字。这是默认的编码方式。
- "escaped"：对输入的字符串进行转义（backslash-escaped）之后，再编码为二进制格式，格式类似于 'abc\xFF\x00\r\n'。

> **注意：**
>
> 如果使用本地存储，在恢复前**必须**将所有备份的 SST 文件复制到各个 TiKV 节点上 `--storage` 指定的目录下。
>
> 即使每个 TiKV 节点最后只需要读取部分 SST 文件，这些节点也需要有所有 SST 文件的完全访问权限。原因如下：
>
> * 数据被复制到了多个 Peer 中。在读取 SST 文件时，这些文件必须要存在于所有 Peer 中。这与数据的备份不同，在备份时，只需从单个节点读取。
> * 在数据恢复的时候，每个 Peer 分布的位置是随机的，事先并不知道哪个节点将读取哪个文件。
>
> 使用共享存储可以避免这些情况。例如，在本地路径上安装 NFS，或使用 S3。利用这些网络存储，各个节点都可以自动读取每个 SST 文件，此时上述注意事项不再适用。
> 
> 同时，请注意同一时间对同一个集群只能运行一个恢复任务，否则可能会出现非预期的行为，详见 [FAQ](/br/backup-and-restore-faq.md#是否可以同时使用多个-br-进程对单个集群进行恢复)。

## 恢复 RawKV（实验性功能）

和 [备份 RawKV](#备份-rawkv-实验性功能)相似，恢复 RawKV 的命令如下：

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
