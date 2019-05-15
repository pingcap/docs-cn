---
title: TiKV Control 使用说明
category: reference
aliases: ['/docs-cn/tools/tikv-control/']
---

# TiKV Control 使用说明

TiKV Control (tikv-ctl) 是随 TiKV 附带的一个简单的管理工具，以下简称 tikv-ctl。

在编译 TiKV 时，tikv-ctl 命令也会同时被编译出来，而通过 Ansible 部署的集群，在对应的 `tidb-ansible/resources/bin` 目录下也会有这个二进制文件。

## 通用参数

tikv-ctl 有两种运行模式：远程模式和本地模式。前者通过 `--host` 选项接受 TiKV 的服务地址作为参数，后者则需要 `--db` 选项来指定本地 TiKV 数据目录路径。以下如无特殊说明，所有命令都同时支持这两种模式。对于远程模式，如果 TiKV 启用了 SSL，则 tikv-ctl 也需要指定相关的证书文件，例如：

```
$ tikv-ctl --ca-path ca.pem --cert-path client.pem --key-path client-key.pem --host 127.0.0.1:20160 <subcommands>
```

某些情况下，tikv-ctl 与 PD 进行通信，而不与 TiKV 通信。此时你需要使用 `--pd` 选项而非 `--host` 选项，例如：

```
$ tikv-ctl --pd 127.0.0.1:2379 compact-cluster
store:"127.0.0.1:20160" compact db:KV cf:default range:([], []) success!
```

除此之外，tikv-ctl 还有两个简单的命令 `--to-hex` 和 `--to-escaped`，用于对 key 的形式作简单的变换。一般使用 `escaped` 形式，示例如下：

```bash
$ tikv-ctl --to-escaped 0xaaff
\252\377
$ tikv-ctl --to-hex "\252\377"
AAFF
```

> **注意：**
>
> 在命令行上指定 `escaped` 形式的 key 时，需要用双引号引起来，否则 bash 会将反斜杠吃掉，导致结果错误。

## 各项子命令及部分参数、选项

下面逐一对 tikv-ctl 支持的子命令进行举例说明。有的子命令支持很多可选参数，要查看全部细节，可运行 `tikv-ctl --help <subcommand>`。

### 查看 Raft 状态机的信息

`raft` 子命令可以查看 Raft 状态机在某一时刻的状态，包括 **RegionLocalState**，**RaftLocalState**，**RegionApplyState** 三个结构体，及某一条 log 对应的 Entries。它有 `region` 和 `log` 两个子命令分别做这两件事。

两个子命令都同时支持远程模式和本地模式。它们的用法及输出内容如下所示：

```bash
$ tikv-ctl --host 127.0.0.1:20160 raft region -r 2
region id: 2
region state key: \001\003\000\000\000\000\000\000\000\002\001
region state: Some(region {id: 2 region_epoch {conf_ver: 3 version: 1} peers {id: 3 store_id: 1} peers {id: 5 store_id: 4} peers {id: 7 store_id: 6}})
raft state key: \001\002\000\000\000\000\000\000\000\002\002
raft state: Some(hard_state {term: 307 vote: 5 commit: 314617} last_index: 314617)
apply state key: \001\002\000\000\000\000\000\000\000\002\003
apply state: Some(applied_index: 314617 truncated_state {index: 313474 term: 151})
```

### 查看 Region 的大小

`size` 命令可以查看 Region 的大小：

```bash
$ tikv-ctl --db /path/to/tikv/db size -r 2
region id: 2
cf default region size: 799.703 MB
cf write region size: 41.250 MB
cf lock region size: 27616
```

### 扫描查看给定范围的 MVCC

`scan` 命令的 `--from` 和 `--to` 参数接受两个 escaped 形式的 raw key，并用 `--show-cf` 参数指定只需要查看哪些列族。

```bash
$ tikv-ctl --db /path/to/tikv/db scan --from 'zm' --limit 2 --show-cf lock,default,write
key: zmBootstr\377a\377pKey\000\000\377\000\000\373\000\000\000\000\000\377\000\000s\000\000\000\000\000\372
         write cf value: start_ts: 399650102814441473 commit_ts: 399650102814441475 short_value: "20"
key: zmDB:29\000\000\377\000\374\000\000\000\000\000\000\377\000H\000\000\000\000\000\000\371
         write cf value: start_ts: 399650105239273474 commit_ts: 399650105239273475 short_value: "\000\000\000\000\000\000\000\002"
         write cf value: start_ts: 399650105199951882 commit_ts: 399650105213059076 short_value: "\000\000\000\000\000\000\000\001"
```

### 查看给定 key 的 MVCC

与上个命令类似，`mvcc` 命令可以查看给定 key 的 MVCC：

```bash
$ tikv-ctl --db /path/to/tikv/db mvcc -k "zmDB:29\000\000\377\000\374\000\000\000\000\000\000\377\000H\000\000\000\000\000\000\371" --show-cf=lock,write,default
key: zmDB:29\000\000\377\000\374\000\000\000\000\000\000\377\000H\000\000\000\000\000\000\371
         write cf value: start_ts: 399650105239273474 commit_ts: 399650105239273475 short_value: "\000\000\000\000\000\000\000\002"
         write cf value: start_ts: 399650105199951882 commit_ts: 399650105213059076 short_value: "\000\000\000\000\000\000\000\001"
```

> **注意：**
>
> 该命令中，key 同样需要是 escaped 形式的 raw key。

### 打印某个 key 的值

打印某个 key 的值需要用到 `print` 命令。示例从略。

### 打印 Region 的 properties 信息

为了记录 Region 的状态信息，TiKV 将一些数据写入 Region 的 SST 文件中。你可以用子命令 `region-properties` 运行 tikv-ctl 来查看这些 properties 信息。例如：

```bash
$ tikv-ctl --host localhost:20160 region-properties -r 2
num_files: 0
num_entries: 0
num_deletes: 0
mvcc.min_ts: 18446744073709551615
mvcc.max_ts: 0
mvcc.num_rows: 0
mvcc.num_puts: 0
mvcc.num_versions: 0
mvcc.max_row_versions: 0
middle_key_by_approximate_size:
```

这些 properties 信息可以用于检查某个 Region 是否健康或者修复不健康的 Region。例如，使用 `middle_key_approximate_size` 可以手动分裂 Region。

### 手动 compact 单个 TiKV 的数据

`compact` 命令可以对单个 TiKV 进行手动 compact。如果指定 `--from` 和 `--to` 选项，那么它们的参数也是 escaped raw key 形式的。`--host` 参数可以指定要 compact 的 TiKV，`-d` 参数可以指定要 compact 的 RocksDB，有 `kv` 和 `raft` 参数值可以选。`--threads` 参数可以指定 compact 的并发数，默认值是 8。一般来说，并发数越大， compact 的速度越快，但是也会对服务造成影响，所以需要根据情况选择合适的并发数。

```bash
$ tikv-ctl --host 127.0.0.1:20160 compact -d kv
success!
```

### 手动 compact 整个 TiKV 集群的数据

`compact-cluster` 命令可以对整个 TiKV 集群进行手动 compact。该命令参数的含义和使用与 `compact` 命令一样。

### 设置一个 Region 为 tombstone

`tombstone` 命令常用于没有开启 sync-log，因为机器掉电导致 Raft 状态机丢失部分写入的情况。它可以在一个 TiKV 实例上将一些 Region 设置为 Tombstone 状态，从而在重启时跳过那些 Region。而那些 Region 应该在其他 TiKV 上有足够多的健康的副本以便能够继续通过 Raft 机制进行读写。

```bash
pd-ctl>> operator add remove-peer <region_id> <peer_id>
$ tikv-ctl --db /path/to/tikv/db tombstone -p 127.0.0.1:2379 -r 2
success!
```

> **注意：**
>
> - `-p` 选项的参数指定 PD 的 endpoints，它没有 `http` 前缀。
> - **这个命令只支持本地模式**。需要指定 PD 的 endpoints 的原因是需要询问 PD 是否可以安全地 tombstone。因此，在 tombstone 之前往往还需要在 `pd-ctl` 中把该 Region 在这台机器上的对应 Peer 拿掉。

### 向 TiKV 发出 consistency-check 请求

**这个命令只支持远程模式**，它可以让某个 Region 对应的 Raft 进行一次副本之间的一致性检查。如果检查失败，TiKV 自身会 panic。如果 `--host` 指定的 TiKV 不是这个 Region 的 Leader，则会报告错误。

```bash
$ tikv-ctl --host 127.0.0.1:20160 consistency-check -r 2
success!
$ tikv-ctl --host 127.0.0.1:21061 consistency-check -r 2
DebugClient::check_region_consistency: RpcFailure(RpcStatus { status: Unknown, details: Some("StringError(\"Leader is on store 1\")") })
```

> **注意：**
>
> 即使这个命令返回了成功，也需要去检查是否有 TiKV panic 了，因为这个命令只是给 Leader 发起一个 Consistency-check 的 propose，至于整个检查流程成功与否并不能在客户端知道。

### Dump snapshot meta

这条子命令可以用于解析指定路径下的 Snapshot 元文件并打印结果。

### 打印 Raft 状态机出错的 Region

前面 tombstone 命令可以将 Raft 状态机出错的 Region 设置为 Tombstone 状态，避免 TiKV 启动时对它们进行检查。在运行那个命令之前，`bad-regions` 命令可以找出这些出错了的 Region，以便将多个工具组合起来进行自动化的处理。

```bash
$ tikv-ctl --db /path/to/tikv/db bad-regions
all regions are healthy
```

命令执行成功会打印上面的信息，否则会打印出有错误的 Region 列表。目前可以检出的错误包括 last index、commit index 和 apply index 之间的不匹配，以及 Raft log 的丢失。其他一些情况，比如 Snapshot 文件损坏等仍然需要后续的支持。

### 查看 Region 的 properties 信息

本地查看部署在 `/path/to/tikv` 的 tikv 上面 Region 2 的 properties 信息：

```bash
$ tikv-ctl --db /path/to/tikv/data/db region-properties -r 2
```

在线查看运行在 `127.0.0.1:20160` 的 tikv 上面 Region 2 的 properties 信息：

```bash
$ tikv-ctl --host 127.0.0.1:20160 region-properties -r 2
```

### 动态修改 TiKV 的 RocksDB 相关配置

使用 `modify-tikv-config` 命令可以动态修改配置参数，暂时仅支持对于 RocksDB 相关参数的动态更改。

- `-m` 可以指定要修改的 RocksDB，有 `kvdb` 和 `raftdb` 两个值可以选择。
- `-n` 用于指定配置名。配置名可以参考 [TiKV 配置模版](https://github.com/pingcap/tikv/blob/master/etc/config-template.toml#L213-L500)中 `[rocksdb]` 和 `[raftdb]` 下的参数，分别对应 `kvdb` 和 `raftdb`。同时，还可以通过 `default|write|lock + . + 参数名` 的形式来指定的不同 CF 的配置（对于 `kvdb` 有 `default|write|lock` 可以选择，对于 `raftdb` 仅有 `default` 可以选择。
- `-v` 用于指定配置值。

```bash
$ tikv-ctl modify-tikv-config -m kvdb -n max_background_jobs -v 8
success！
$ tikv-ctl modify-tikv-config -m kvdb -n write.block-cache-size -v 256MB
success!
$ tikv-ctl modify-tikv-config -m raftdb -n default.disable_auto_compactions -v true
success!
```

### 强制 Region 从多副本失败状态恢复服务

`unsafe-recover remove-fail-stores` 命令可以将一些失败掉的机器从指定 Region 的 peers 列表中移除。这个命令只有 local 模式，而且需要目标 TiKV 先停掉服务以便释放文件锁。

`-s` 选项接受多个以逗号分隔的 `store_id`，并使用 `-r` 参数来指定包含的 Region。如果要对某一个 store 上的全部 Region 都执行这个操作，则可以简单地指定 `--all-regions`。

```bash
$ tikv-ctl --db /path/to/tikv/db unsafe-recover remove-fail-stores -s 3 -r 1001,1002
success!

$ tikv-ctl --db /path/to/tikv/db unsafe-recover remove-fail-stores -s 4,5 --all-regions
```

之后启动 TiKV，这些 Region 便可以以剩下的健康的副本继续提供服务了。这个命令常用于多个 TiKV store 损坏或被删除的情况。

> **注意：**
>
> - **这个命令只支持本地模式**。在运行成功后，会打印 `success!`。
> - 一般来说，需要使用这个命令的地方，对于指定 Region 的 peers 所在的每个 store，均须运行这个命令。
> - 如果使用 `--all-regions`，通常需要在集群剩余所有健康的 store 上执行这个命令。

### 恢复损坏的 MVCC 数据

`recover-mvcc` 命令用于 MVCC 数据损坏导致 TiKV 无法正常运行的情况。为了从不同种类的不一致情况中恢复，该命令会反复检查 3 个 CF ("default", "write", "lock")。

`-r` 选项可以通过 `region_id` 指定包含的 Region，`-p` 选项可以指定 PD 的 endpoint。

```bash
$ tikv-ctl --db /path/to/tikv/db recover-mvcc -r 1001,1002 -p 127.0.0.1:2379
success!
```

> **注意：**
>
> - **这个命令只支持本地模式**。在运行成功后，会打印 `success!`。
> - `-p` 选项指定 PD 的 endpoint，不使用 `http` 前缀，用于查询指定的 `region_id` 是否有效。
> - 对于指定 Region 的 peers 所在的每个 store，均须执行这个命令。
