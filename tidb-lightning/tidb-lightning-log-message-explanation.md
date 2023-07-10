---
title: TiDB Lightning 日志信息详解
summary: 了解使用 TiDB Lightning 导入数据的过程中生成的日志消息的详细解释。
---

# TiDB Lightning 日志信息详解

本文档描述了使用 **TiDB Lightning v5.4** 的 **local backend** 成功导入数据时的日志消息，并详细解释了日志的来源和含义。你可以参考本文档更好地理解 TiDB Lightning 日志。

在阅读本文档之前，请确保你已经熟悉 TiDB Lightning，并已了解 [TiDB Lightning 简介](/tidb-lightning/tidb-lightning-overview.md)中描述的整体架构和工作流。如果你遇到不熟悉的术语，可以参考[术语表](/tidb-lightning/tidb-lightning-glossary.md)。

通过本文档，您可以快速浏览 TiDB Lightning 源代码，并更好地了解其内部工作原理以及日志消息的确切含义。

需要注意的是，本文档仅包含重要信息，省略了一些不重要的日志。

## 日志信息详解

```
[INFO] [info.go:49] ["Welcome to TiDB-Lightning"] [release-version=v5.4.0] [git-hash=55f3b24c1c9f506bd652ef1d162283541e428872] [git-branch=HEAD] [go-version=go1.16.6] [utc-build-time="2022-04-21 02:07:55"] [race-enabled=false]
```

[info.go:49](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/version/build/info.go#L49)：打印 TiDB Lightning 的版本信息。

```
[INFO] [lightning.go:233] [cfg] [cfg="{\"id\":1650510440481957437,\"lightning\":{\"table-concurrency\":6,\"index-concurrency\":2,\"region-concurrency\":8,\"io-concurrency\":5,\"check-requirements\":true,\"meta-schema-name\":\"lightning_metadata\", ...
```

[lightning.go:233](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/lightning.go#L233)：打印 TiDB Lightning 的配置信息。

```
[INFO] [lightning.go:312] ["load data source start"]
```

[lightning.go:312](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/lightning.go#L312)：开始扫描 TiDB Lightning [mydumper `data-source-dir` 配置项](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/config/config.go#L447)中定义的[数据源目录或外部存储](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/loader.go#L205)，并将所有数据源文件元信息加载到[内部数据结构](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/loader.go#L82)中以供将来使用。

```
[INFO] [loader.go:289] ["[loader] file is filtered by file router"] [path=metadata]
```

[loader.go:289](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/loader.go#L289)：打印根据[文件路由规则](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/loader.go#L139)跳过的数据源文件。文件路由规则由 TiDB Lightning [mydumper `files` 配置项](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/config/config.go#L452)中定义，如果 [`files` 规则未定义](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/config/config.go#L847)，则使用内部[默认文件路由规则](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/router.go#L105)。

```
[INFO] [lightning.go:315] ["load data source completed"] [takeTime=273.964µs] []
```

[lightning.go:315](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/lightning.go#L315)：完成将数据源文件信息加载到 [Mydumper 文件加载器](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/loader.go#L73)中，以供将来导入。

```
[INFO] [checkpoints.go:977] ["open checkpoint file failed, going to create a new one"] [path=/tmp/tidb_lightning_checkpoint.pb] [error="open /tmp/tidb_lightning_checkpoint.pb: no such file or directory"]
```

[checkpoints.go:977](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/checkpoints/checkpoints.go#L977)：如果 TiDB Lightning 使用文件存储检查点，并且找不到任何本地检查点文件，则 TiDB Lightning 将创建一个新的检查点。

```
[INFO] [restore.go:444] ["the whole procedure start"]
```

[restore.go:444](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L444)：开始导入过程。

```
[INFO] [restore.go:748] ["restore all schema start"]
```

[restore.go:748](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L748)：根据数据源的 schema 信息，开始创建数据库和表。

```
[INFO] [restore.go:767] ["restore all schema completed"] [takeTime=189.766729ms]
```

[restore.go:767](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L767)：完成创建数据库和表。

```
[INFO] [check_info.go:680] ["datafile to check"] [db=sysbench] [table=sbtest1] [path=sysbench.sbtest1.000000000.sql]
```

[check_info.go:680](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/check_info.go#L680)：作为预检查的一部分，TiDB Lightning 使用每个表的第一个数据文件来检查源数据文件和目标集群表结构是否匹配。

```
[INFO] [version.go:360] ["detect server version"] [type=TiDB] [version=5.4.0]
```

[version.go:360](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/version/version.go#L360)：检测并打印当前 TiDB server 版本。要在 local 后端模式下导入数据，TiDB 版本必须高于 4.0。此外，还需要检查服务器版本以[检测数据冲突](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/version/version.go#L224)。

```
[INFO] [check_info.go:995] ["sample file start"] [table=sbtest1]
```

[check_info.go:995](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/check_info.go#L995)：作为预检查的一部分，估算源数据的大小以确定下列信息：

- [如果 TiDB Lightning 使用 local 后端模式，检查本地盘是否有足够的空间](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/check_info.go#L462)。
- [目标集群是否有足够的空间来存储转换后的 KV 对](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/check_info.go#L102)。

TiDB Lightning 通过对每个表的第一个源数据文件进行采样，计算文件大小与 KV 对大小的比率，并使用该比率乘以源数据文件大小来估算转换后的 KV 对的大小。

```
[INFO] [check_info.go:1080] ["Sample source data"] [table=sbtest1] [IndexRatio=1.3037832180660969] [IsSourceOrder=true]
```

[check_info.go:1080](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/check_info.go#L1080)：已计算表源数据文件大小与 KV 对大小的比率。

```
[INFO] [pd.go:415] ["pause scheduler successful at beginning"] [name="[balance-region-scheduler,balance-leader-scheduler,balance-hot-region-scheduler]"]
[INFO] [pd.go:423] ["pause configs successful at beginning"] [cfg="{\"enable-location-replacement\":\"false\",\"leader-schedule-limit\":4,\"max-merge-region-keys\":0,\"max-merge-region-size\":0,\"max-pending-peer-count\":2147483647,\"max-snapshot-count\":40,\"region-schedule-limit\":40}"]
```

[pd.go:415](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#L415)，[pd.go:423](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#L423)：在 Local 后端模式下，禁用了一些 [PD 调度器](https://docs.pingcap.com/zh/tidb/stable/tidb-scheduling)，并且更改了一些[配置项](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#L417)，以分裂和打散 TiKV region 并导入 SST。

```
[INFO] [restore.go:1683] ["switch to import mode"]
```

[restore.go:1683](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1683)：在 local 后端模式下，TiDB Lightning 将每个 TiKV 节点切换到导入模式以加快导入过程，但这一操作会牺牲其存储空间。如果使用 tidb 后端模式，则不需要切换 TiKV 到[导入模式](https://docs.pingcap.com/zh/tidb/stable/tidb-lightning-glossary#import-mode)。

```
[INFO] [restore.go:1462] ["restore table start"] [table=`sysbench`.`sbtest1`]
```

[restore.go:1462](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1462)：开始恢复表 `sysbench`.`sbtest1`。TiDB Lightning 根据 [`index-concurrency`](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1459) 配置项并发地恢复多个表。对于每个表，TiDB Lightning 根据 [`region-concurrency`](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/region.go#L157) 配置项并发地恢复表中的数据文件。

```
[INFO] [table_restore.go:91] ["load engines and files start"] [table=`sysbench`.`sbtest1`]
```

[table_restore.go:91](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L91)：开始将每个表的[源数据文件](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/region.go#L145)按逻辑[拆分为多个 chunk 或表 region](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/region.go#L283)。每个表的源数据文件将[分配给一个 engine](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/region.go#L246) 以在不同的 engine 中并行处理数据文件。

```
[INFO] [region.go:241] [makeTableRegions] [filesCount=8] [MaxRegionSize=268435456] [RegionsCount=8] [BatchSize=107374182400] [cost=53.207µs]
```

[region.go:241](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/region.go#L241)：打印已处理的表数据文件的数量 (`filesCount`)、CSV 文件的最大 chunk 大小 (`MaxRegionSize`)、生成的表 region 或 chunk 的数量 (`RegionsCount`) 以及用来分配不同的 engine 来处理数据文件的 `batchSize`。

```
[INFO] [table_restore.go:129] ["load engines and files completed"] [table=`sysbench`.`sbtest1`] [enginesCnt=2] [ime=75.563µs] []
```

[table_restore.go:129](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L129)：完成了将表数据文件进行逻辑拆分。

```
[INFO] [backend.go:346] ["open engine"] [engineTag=`sysbench`.`sbtest1`:-1] [engineUUID=3942bab1-bd60-52e2-bf53-e17aebf962c6]
```

[backend.go:346](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L346)：Engine id `-1` 代表索引引擎。在[恢复引擎过程](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L199)开始时，TiDB Lightning 会打开索引引擎以存储转换后的索引 KV 对。

```
[INFO] [table_restore.go:270] ["import whole table start"] [table=`sysbench`.`sbtest1`]
```

[table_restore.go:270](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L270)：开始并发地[恢复指定的表中的不同数据引擎](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L318)。

```
[INFO] [table_restore.go:317] ["restore engine start"] [table=`sysbench`.`sbtest1`] [engineNumber=0]
```

[table_restore.go:317](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L317)：开始恢复 engine `0`，非 `-1` 的 engine id 表示数据引擎。需要注意的是 "restore engine" 和 "import engine"（稍后在日志中出现）指的是不同的过程。"restore engine" 表示将 KV 对发送到分配的 engine 并对其进行排序的过程，而 "import engine" 表示将 engine 文件中已排序的 KV 对导入到 TiKV 节点的过程。

```
[INFO] [table_restore.go:422] ["encode kv data and write start"] [table=`sysbench`.`sbtest1`] [engineNumber=0]
```

[table_restore.go:422](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L422)：开始[按 chunk 恢复表数据](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L386)。

```
[INFO] [backend.go:346] ["open engine"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7]
```

[backend.go:346](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L346)：打开 engine id 为 `0` 的数据引擎以存储转换后的数据 KV 对。

```
[INFO] [restore.go:2482] ["restore file start"] [table=`sysbench`.`sbtest1`] [engineNumber=0] [fileIndex=0] [path=sysbench.sbtest1.000000000.sql:0]
```

[restore.go:2482](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L2482)：这个日志可能会根据导入表数据的大小而出现多次。每一条这样的日志表示开始恢复一个 chunk/table region。TiDB Lightning 会根据内部的 [region workers](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L532) 并发地[恢复 chunks](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L386)，region workers 的数量由 [region concurrency](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L402) 定义。对于每个 chunk，恢复的过程如下：

1. [将 SQL 编码为 KV 对](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L2389)。
2. [将 KV 对写入数据引擎和索引引擎](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L2179)。

```
[INFO] [engine.go:777] ["write data to local DB"] [size=134256327] [kvs=621576] [files=1] [sstFileSize=108984502] [file=/home/centos/tidb-lightning-temp-data/sorted-kv-dir/d173bb2e-b753-5da9-b72e-13a49a46f5d7.sst/11e65bc1-04d0-4a39-9666-cae49cd013a9.sst] [firstKey=74800000000000003F5F728000000000144577] [lastKey=74800000000000003F5F7280000000001DC17E]
```

[engine.go:777](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/engine.go#L777)：开始将生成的 SST 文件导入到 embeded engine 中。TiDB Lightning 将[并发地导入 SST 文件](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/local.go#L624)。

```
[INFO] [restore.go:2492] ["restore file completed"] [table=`sysbench`.`sbtest1`] [engineNumber=0] [fileIndex=1] [path=sysbench.sbtest1.000000001.sql:0] [readDur=3.123667511s] [encodeDur=5.627497136s] [deliverDur=6.653498837s] [checksum="{cksum=6610977918434119862,size=336040251,kvs=2646056}"] [takeTime=15.474211783s] []
```

[restore.go:2492](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L2492)：一个指定的表的一个 chunk（由 `fileIndex=1` 定义的数据源文件）已经被编码并存储到引擎中。

```
[INFO] [table_restore.go:584] ["encode kv data and write completed"] [table=`sysbench`.`sbtest1`] [engineNumber=0] [read=16] [written=2539933993] [takeTime=23.598662501s] []
[source code]
```

[table_restore.go:584](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L584)：所有属于引擎 `engineNumber=0` 的 chunk/table region 已经被编码并存储到引擎 `engineNumber=0` 中。

```
[INFO] [backend.go:438] ["engine close start"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7]
[INFO] [backend.go:440] ["engine close completed"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7] [takeTime=2.879906ms] []
```

[backend.go:438](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L438)：作为[引擎恢复的最后阶段](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L628)，数据引擎被关闭并准备导入到 TiKV 节点。

```
[INFO] [table_restore.go:319] ["restore engine completed"] [table=`sysbench`.`sbtest1`] [engineNumber=0] [takeTime=27.031916498s] []
```

[table_restore.go:319](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L319)：完成了将 KV 对编码并写入数据引擎 `0`。

```
[INFO] [table_restore.go:927] ["import and cleanup engine start"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7]
[INFO] [backend.go:452] ["import start"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7] [retryCnt=0]
```

[table_restore.go:927](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L927)，[backend.go:452](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L452)：开始将存储在引擎中的 KV 对[导入](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/local.go#L1311)到目标 TiKV 节点。

```
[INFO] [local.go:1023] ["split engine key ranges"] [engine=d173bb2e-b753-5da9-b72e-13a49a46f5d7] [totalSize=2159933993] [totalCount=10000000] [firstKey=74800000000000003F5F728000000000000001] [lastKey=74800000000000003F5F728000000000989680] [ranges=22]
```

[local.go:1023](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/local.go#L1023)：在[导入引擎](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/local.go#L1331)前，根据 [`RegionSplitSize`](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L927) 配置项将引擎数据逻辑拆分为更小的范围。

```
[INFO] [local.go:1336] ["start import engine"] [uuid=d173bb2e-b753-5da9-b72e-13a49a46f5d7] [ranges=22] [count=10000000] [size=2159933993]
```

[local.go:1336](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/local.go#L1336)：开始按照拆分范围将 KV 对导入引擎中。

```
[INFO] [localhelper.go:89] ["split and scatter region"] [minKey=7480000000000000FF3F5F728000000000FF0000010000000000FA] [maxKey=7480000000000000FF3F5F728000000000FF9896810000000000FA] [retry=0]
```

[localhelper.go:89](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/localhelper.go#L89)：开始根据引擎范围的最小键和最大键[拆分和打散](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/localhelper.go#L65) TiKV region。

```
[INFO] [localhelper.go:108] ["paginate scan regions"] [count=1] [start=7480000000000000FF3F5F728000000000FF0000010000000000FA] [end=7480000000000000FF3F5F728000000000FF9896810000000000FA]
[INFO] [localhelper.go:116] ["paginate scan region finished"] [minKey=7480000000000000FF3F5F728000000000FF0000010000000000FA] [maxKey=7480000000000000FF3F5F728000000000FF9896810000000000FA] [regions=1]
```

[localhelper.go:108](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/localhelper.go#L108)，[localhelper.go:116](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/localhelper.go#L108)：在 PD 上分页[扫描一批 region 信息](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/restore/split.go#L413)。

```
[INFO] [split_client.go:460] ["checking whether need to scatter"] [store=1] [max-replica=3]
[INFO] [split_client.go:113] ["skipping scatter because the replica number isn't less than store count."]
```

[split_client.go:460](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/restore/split_client.go#L460), [split_client.go:113](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/restore/split_client.go#L113)：因为 max-replica >= TiKV store 数量，所以跳过打散 region 阶段。打散 region 是指 PD 调度器将 region 和副本分散到不同的 TiKV store 的过程。

```
[INFO] [localhelper.go:240] ["batch split region"] [region_id=2] [keys=23] [firstKey="dIAAAAAAAAA/X3KAAAAAAAAAAQ=="] [end="dIAAAAAAAAA/X3KAAAAAAJiWgQ=="]
```

[localhelper.go:240](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/localhelper.go#L240)：完成了批量拆分 TiKV region。

```
[INFO] [localhelper.go:319] ["waiting for scattering regions done"] [skipped_keys=0] [regions=23] [take=6.505195ms]
```

[localhelper.go:319](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/localhelper.go#L319): 完成了打散 TiKV region。

```
[INFO] [local.go:1371] ["import engine success"] [uuid=d173bb2e-b753-5da9-b72e-13a49a46f5d7] [size=2159933993] [kvs=10000000] [importedSize=2159933993] [importedCount=10000000]
[INFO] [backend.go:455] ["import completed"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7] [retryCnt=0] [takeTime=20.179184481s] []
```

[local.go:1371](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/local.go#L1371)，[backend.go:455](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L455)：完成了将特定引擎中的 KV 对导入 TiKV store。

```
[INFO] [backend.go:467] ["cleanup start"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7]
[INFO] [backend.go:469] ["cleanup completed"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7] [takeTime=209.800004ms] []
```

[backend.go:467](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L467)，[backend.go:469](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L469)：清理导入阶段的中间数据。这一操作将[清理](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/engine.go#L158)引擎相关的元信息和数据库文件。

```
[INFO] [table_restore.go:946] ["import and cleanup engine completed"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7] [takeTime=20.389269402s] []
```

[table_restore.go:946](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L946)：完成了导入和清理。

```
[INFO] [table_restore.go:345] ["import whole table completed"] [table=`sysbench`.`sbtest1`] [takeTime=47.421324969s] []
```

[table_restore.go:345](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L345)：完成了导入表数据。TiDB Lightning 将所有表数据转换为 KV 对，并将其导入到 TiKV 集群中。

```
[INFO] [tidb.go:401] ["alter table auto_increment start"] [table=`sysbench`.`sbtest1`] [auto_increment=10000002]
[INFO] [tidb.go:403] ["alter table auto_increment completed"] [table=`sysbench`.`sbtest1`] [auto_increment=10000002] [takeTime=82.225557ms] []
```

[tidb.go:401](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/tidb.go#L401)，[tidb.go:403](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/tidb.go#L403)：在 [post process](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L680) 阶段，TiDB Lightning 会[调整表的自增 ID](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L703) 以避免新添加的数据引入冲突。

```
[INFO] [restore.go:1466] ["restore table completed"] [table=`sysbench`.`sbtest1`] [takeTime=53.280464651s] []
```

[restore.go:1466](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1466)：完成了表的恢复。

```
[INFO] [restore.go:1396] ["add back PD leader&region schedulers"]
[INFO] [pd.go:462] ["resume scheduler"] [schedulers="[balance-region-scheduler,balance-leader-scheduler,balance-hot-region-scheduler]"]
[INFO] [pd.go:448] ["exit pause scheduler and configs successful"]
[INFO] [pd.go:482] ["resume scheduler successful"] [scheduler=balance-region-scheduler]
[INFO] [pd.go:573] ["restoring config"] [config="{\"enable-location-replacement\":\"true\",\"leader-schedule-limit\":4,\"max-merge-region-keys\":200000,\"max-merge-region-size\":20,\"max-pending-peer-count\":64,\"max-snapshot-count\":64,\"region-schedule-limit\":2048}"]
```

[restore.go:1396](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1396)，[pd.go:462](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#L462)，[pd.go:448](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#L448)，[pd.go:482](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#482)，[pd.go:573](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#573)：在导入之前恢复处于暂停状态的 PD 调度器，并重置 PD 配置。

```
[INFO] [restore.go:1244] ["cancel periodic actions"] [do=true]
```

[restore.go:1244](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1244)：开始取消[周期性操作](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1087)，该操作周期性地打印导入进度，并检查 TiKV 是否仍处于导入模式。

```
[INFO] [restore.go:1688] ["switch to normal mode"]
```

[restore.go:1688](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1688)：将 TiKV 从导入模式切换到正常模式。

```
[INFO] [table_restore.go:736] ["local checksum"] [table=`sysbench`.`sbtest1`] [checksum="{cksum=9970490404295648092,size=2539933993,kvs=20000000}"]
[INFO] [checksum.go:172] ["remote checksum start"] [table=sbtest1]
[INFO] [checksum.go:175] ["remote checksum completed"] [table=sbtest1] [takeTime=2.817086758s] []
[INFO] [table_restore.go:971] ["checksum pass"] [table=`sysbench`.`sbtest1`] [local="{cksum=9970490404295648092,size=2539933993,kvs=20000000}"]
```

[table_restore.go:736](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L736)，[checksum.go:172](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/checksum.go#L172)，[checksum.go:175](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/checksum.go#L175)，[table_restore.go:971](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L971)：[比较本地和远程的校验和](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L736)，以验证导入的数据。

```
[INFO] [table_restore.go:976] ["analyze start"] [table=`sysbench`.`sbtest1`]
[INFO] [table_restore.go:978] ["analyze completed"] [table=`sysbench`.`sbtest1`] [takeTime=26.410378251s] []
```

[table_restore.go:976](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L976)，[table_restore.go:978](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L978)：TiDB 分析表以更新 TiDB 在表和索引上构建的统计信息。建议在执行大批量更新或导入记录后，或者在你注意到查询执行计划不太理想时，运行 `ANALYZE` 更新统计信息。

```
[INFO] [restore.go:1440] ["cleanup task metas"]
```

[restore.go:1440](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1440)：清理导入任务元数据、表元数据和 schema db（如果需要）。

```
[INFO] [restore.go:1842] ["clean checkpoints start"] [keepAfterSuccess=remove] [taskID=1650516927467320997]
[INFO] [restore.go:1850] ["clean checkpoints completed"] [keepAfterSuccess=remove] [taskID=1650516927467320997] [takeTime=18.543µs] []
```

[restore.go:1842](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1842)，[restore.go:1850](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1850)：清理检查点。

```
[INFO] [restore.go:473] ["the whole procedure completed"] [takeTime=1m22.804337152s] []
```

[restore.go:473](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L473)：完成了整个导入过程。

```
[INFO] [restore.go:1143] ["everything imported, stopping periodic actions"]
```

[restore.go:1143](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1143)：在导入完成后，停止所有[周期性操作](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1087)。
