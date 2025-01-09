---
title: 压缩日志备份
summary: 了解如何通过将日志备份压缩成 SST 格式来加速未来的时间点恢复（Point in Time Restore, PiTR）。
---

# 压缩日志备份

Log Backup 会以一种高度非结构化的方式备份下来所有写入。这些写入未经排序，因此只能通过 Raft 协议将他们一个个写入到集群。这个过程中会遇到诸多问题：例如写放大或恢复后续的集群性能不及预期。

因此，目前建议尽量不要让某次 PiTR 中包含过多的 Log 部分，为了减少 Log 部分，需要多次进行全量备份，全量备份对于业务又会有一定影响，所以多次全量备份并不令人愉悦。在 v8.5.0 之后，压缩日志备份（Compact Log Backup）将提供一种新的解决方案：离线地将 Log 部分的非结构化数据重写为结构化的 SST，以期在提升恢复的性能的同时降低需求全量备份的频率。

## 使用限制

压缩日志备份并不能完全替代定期全量备份——为了保证能进行 PiTR，日志部分的 MVCC 并不会在压缩过程中被清除，因此日志部分会无限增大。如果完全不进行全量备份，恢复如此巨大的增量数据会导致问题。

**目前压缩日志备份功能还处在高度试验阶段**，在 `v8.5.0` 中，只有“压缩日志”本身这个功能被提供，一些重要的配套还需等到后续版本发布：

- 恢复被压缩的日志
- 清理被压缩的日志
- 使用 TiDB operator 轻易地创建临时节点来离线压缩日志

## 使用方法

目前仅仅支持手动压缩日志备份，这个流程颇为复杂。**建议在生产中使用后续发布的 TiDB operator 方案来进行压缩**。

### 手动压缩

手动压缩日志备份需要两个工具：`tikv-ctl` 和 `br`。

#### 第一步：编码 Storage 为 Base64

TiKV 并不能直接接受并解析一个像是 `s3://astro/tpcc-1000-incr-with-boundaries` 这样的 URL；但是生成 SST 的工作暂时又非它不可。因此第一步是把 Storage 编码成它可以识别的形式。

```shell
br operator base64ify --storage "s3://your/log/backup/storage/here" --load-creds
```

注意其中的 `--load-cerds` 选项。如果带上了这个选项，编码出来的 base64 中会包含从 BR 当前环境中加载的密钥信息，请注意保护。

此处的 storage 应该和 Log Backup 任务的 `log status` 命令输出的 storage 相同。

该命令的输出看起来像是：

```text
Credientials are encoded to the base64 string. DON'T share this with untrusted people!
Gl8KEWh0dHA6Ly9taW5pbzo5MDAwEgl1cy1lYXN0LTEaBWFzdHJvIh50cGNjLTEwMDAtaW5jci13aXRoLWJvdW5kYXJpZXNCCm1pbmlvYWRtaW5KCm1pbmlvYWRtaW5QAQ==
```

#### 第二步：开始压缩日志

有了 storage 的 base64 之后，你可以通过 `tikv-ctl` 发起压缩：

```shell
tikv-ctl compact-log-backup \
    --from "<start-tso>" --until "<end-tso>" \
    -s 'bAsE64==' -N 8
```

这些参数的含义如下：

- `-s`：前文获得的 Storage 的 base64。
- `-N`：最大同时进行的压缩日志任务的数量。
- `--from`: 压缩开始的时间戳。
- `--until`: 压缩结束的时间戳。

`--from` 和 `--until` 这对参数用于选择将要压缩的文件，任何包含了**至少一个**在该时间区间内的写入的 Log 将会被**整个**送去压缩。
因此最终 Compact 的结果中可能包含该时间范围以外的写入。

其中，某个特定时间点的 TSO 可以通过如下 shell 脚本获取：

```shell
echo $(( $(date --date '2004-05-06 15:02:01Z' +%s%3N) << 18 ))
```

> **提示**:
>
> 如果你是 macOS 用户，执行上述脚本时，你可能需要预先通过 Homebrew 安装 `coreutils`，并且使用 `gdate` 而非 `date`。
