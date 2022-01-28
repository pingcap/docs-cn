---
title: 使用 BR 对 rawKV 进行备份和恢复
summary: 使用 BR 对 rawKV 进行备份和恢复。
---

# RawKV 备份和恢复

BR 支持对单独使用 RawKV（TiKV 和 PD）产品进行备份和恢复，下文介绍可 RawKV 备份恢复的所有相关知识。

## Raw KV 备份（实验性功能）

> **警告：**
>
> Raw KV 备份功能还在实验中，没有经过完备的测试。暂时请避免在生产环境中使用该功能。

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

## Raw KV 恢复（实验性功能）

> **警告：**
>
> Raw KV 恢复功能还在实验中，没有经过完备的测试。暂时请避免在生产环境中使用该功能。

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

### 在线恢复（实验性功能）

> **警告：**
>
> 在线恢复功能还在实验中，没有经过完备的测试，同时还依赖 PD 的不稳定特性 Placement Rules。暂时请避免在生产环境中使用该功能。

在恢复的时候，写入过多的数据会影响在线集群的性能。为了尽量避免影响线上业务，BR 支持通过 [Placement rules](/configure-placement-rules.md) 隔离资源。让下载、导入 SST 的工作仅仅在指定的几个节点（下称“恢复节点”）上进行，具体操作如下：

1. 配置 PD，启动 Placement rules：

    {{< copyable "shell-regular" >}}

    ```shell
    echo "config set enable-placement-rules true" | pd-ctl
    ```

2. 编辑恢复节点 TiKV 的配置文件，在 `server` 一项中指定：

    {{< copyable "" >}}

    ```
    [server]
    labels = { exclusive = "restore" }
    ```

3. 启动恢复节点的 TiKV，使用 BR 恢复备份的文件，和非在线恢复相比，这里只需要加上 `--online` 标志即可：

    {{< copyable "shell-regular" >}}

    ```shell
    br restore full \
        -s "local://$BACKUP_DIR" \
        --ratelimit 128 \
        --pd $PD_ADDR \
        --online
    ```
