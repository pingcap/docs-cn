# Titan 设计文档

[Titan](https://github.com/pingcap/rocksdb/tree/titan-5.15) 是由 [PingCAP](https://pingcap.com/) 研发的一个基于 [RocksDB](https://github.com/facebook/rocksdb) 的高性能单机 key-value 存储引擎，其主要设计灵感来源于 USENIX FAST 2016 上发表的一篇论文 [WiscKey](https://www.usenix.org/system/files/conference/fast16/fast16-papers-lu.pdf)。WiscKey 提出了一种高度基于 SSD 优化的设计，利用 SSD 高效的随机读写性能，通过将 value 分离出 LSM-tree 的方法来达到降低写放大的目的。

我们的基准测试结果显示，当 value 较大的时候，Titan 在写、更新和点读等场景下性能都优于 RocksDB。但是根据 [RUM Conjecture](http://daslab.seas.harvard.edu/rum-conjecture/)，通常某些方面的提升往往是以牺牲其他方面为代价而取得的。Titan 便是以牺牲硬盘空间和范围查询的性能为代价，来取得更高的写性能。随着 SSD 价格的降低，我们认为这种取舍的意义会越来越明显。

## 设计目标

Titan 作为 TiKV 的一个子项目，首要的设计目标便是兼容 RocksDB。因为 TiKV 使用 RocksDB 作为其底层的存储引擎，而 TiKV 作为一个成熟项目已经拥有庞大的用户群体，所以我们需要考虑已有的用户也可以将已有的基于 RocksDB 的 TiKV 平滑地升级到基于 Titan 的 TiKV。

因此，我们总结了四点主要的设计目标：

- 支持将 value 从 LSM-tree 中分离出来单独存储，以降低写放大。
- 已有 RocksDB 实例可以平滑地升级到 Titan，这意味着升级过程不需要人工干预，并且不会影响线上服务。
- 100% 兼容目前 TiKV 所使用的所有 RocksDB 的特性。
- 尽量减少对 RocksDB 的侵入性改动，保证 Titan 更加容易升级到新版本的 RocksDB。

## 架构与实现

Titan 的基本架构如下图所示：

![1-Architecture.png](/media/titan/titan-1.png)

图 1：Titan 在 Flush 和 Compaction 的时候将 value 分离出 LSM-tree，这样做的好处是写入流程可以和 RockDB 保持一致，减少对 RocksDB 的侵入性改动。

Titan 的核心组件主要包括：BlobFile、TitanTableBuilder、Version 和 GC，下面将逐一进行介绍。

### BlobFile

BlobFile 是用来存放从 LSM-tree 中分离出来的 value 的文件，其格式如下图所示：

![2-BlobFile.png](/media/titan/titan-2.png)

图 2：BlobFile 主要由 blob record 、meta block、meta index block 和 footer 组成。其中每个 blob record 用于存放一个 key-value 对；meta block 支持可扩展性，可以用来存放和 BlobFile 相关的一些属性等；meta index block 用于检索 meta block。

BlobFile 有几点值得关注的地方：

1. BlobFile 中的 key-value 是有序存放的，目的是在实现 Iterator 的时候可以通过 prefetch 的方式提高顺序读取的性能。
2. 每个 blob record 都保留了 value 对应的 user key 的拷贝，这样做的目的是在进行 GC 的时候，可以通过查询 user key 是否更新来确定对应 value 是否已经过期，但同时也带来了一定的写放大。
3. BlobFile 支持 blob record 粒度的 compression，并且支持多种 compression algorithm，包括 [Snappy](https://github.com/google/snappy)、[LZ4](https://github.com/lz4/lz4) 和 [Zstd](https://github.com/facebook/zstd) 等，目前 Titan 默认使用的 compression algorithm 是 LZ4 。

### TitanTableBuilder

TitanTableBuilder 是实现分离 key-value 的关键。我们知道 RocksDB 支持使用用户自定义 table builder 创建 SST，这使得我们可以不对 build table 流程做侵入性的改动就可以将 value 从 SST 中分离出来。下面将介绍 TitanTableBuilder 的主要工作流程：

![3-TitanTableBuilder.png](/media/titan/titan-3.png)

图 3：TitanTableBuilder 通过判断 value size 的大小来决定是否将 value 分离到 BlobFile 中去。如果 value size 大于等于 min_blob_size 则将 value 分离到 BlobFile ，并生成 index 写入 SST；如果 value size 小于 min_blob_size 则将 value 直接写入 SST。

反之，这个流程就可以支持 Titan 降级回 RocksDB。在 RocksDB 做 Compaction 的时候，将分离出来的 value 重新写回新生成的 SST 文件中。

Titan 和 [Badger](https://github.com/dgraph-io/badger) 的设计有很大区别。Badger 直接将 WAL 改造成 VLog，这样做的好处是减少一次 Flush 的开销。而 Titan 不这么设计的主要原因有两个：

1. 假设 LSM-tree 的 max level 是 5，放大因子为 10，则 LSM-tree 总的写放大大概为 1 + 1 + 10 + 10 + 10 + 10，其中 Flush 的写放大是 1，其比值是 42 : 1，因此 Flush 的写放大相比于整个 LSM-tree 的写放大可以忽略不计。
2. 在第一点的基础上，保留 WAL 可以使 Titan 极大地减少对 RocksDB 的侵入性改动，而这也正是我们的设计目标之一。

## Garbage Collection

Garbage Collection (GC) 的目的是回收空间。由于在 LSM-Tree Compaction 进行回收 key 时，存在 Blob 文件的 value 并不会一同被删除，因此需要 GC 定期来将已经作废的 value 删除掉。在 Titan 中根据不同的侧重分为两种方式：

- 定期整合重写 Blob 文件将作废的 value 剔除（传统 GC）
- 在 LSM-Tree Compaction 的时候同时进行 Blob 文件的重写 （Level-Merge）

### 传统 GC

在设计 GC 的时候有两个主要的问题需要考虑：

- 何时进行 GC
- 挑选哪些文件进行 GC

Titan 使用 RocksDB 提供的两个特性来解决这两个问题，这两个特性分别是 TablePropertiesCollector 和 EventListener 。下面将讲解我们是如何通过这两个特性来辅助 GC 工作的。

#### BlobFileSizeCollector

RocksDB 允许我们使用自定义的 TablePropertiesCollector 来搜集 SST 上的 properties 并写入到对应文件中去。Titan 通过一个自定义的 TablePropertiesCollector —— BlobFileSizeCollector 来搜集每个 SST 中有多少数据是存放在哪些 BlobFile 上的，我们将它收集到的 properties 命名为 BlobFileSizeProperties，它的工作流程和数据格式如下图所示：

![4-BlobFileSizeProperties.png](/media/titan/titan-4.png)

图 4：左边 SST 中 Index 的格式为：第一列代表 BlobFile 的文件 ID，第二列代表 blob record 在 BlobFile 中的 offset，第三列代表 blob record 的 size。右边 BlobFileSizeProperties 中的每一行代表一个 BlobFile 以及 SST 中有多少数据保存在这个 BlobFile 中，第一列代表 BlobFile 的文件 ID，第二列代表数据大小。

#### EventListener

我们知道 RocksDB 是通过 Compaction 来丢弃旧版本数据以回收空间的，因此每次 Compaction 完成后 Titan 中的某些 BlobFile 中便可能有部分或全部数据过期。因此我们便可以通过监听 Compaction 事件来触发 GC，通过搜集比对 Compaction 中输入输出 SST 的 BlobFileSizeProperties 来决定挑选哪些 BlobFile 进行 GC。其流程大概如下图所示：

![5-EventListener.png](/media/titan/titan-5.png)

图 5：inputs 代表参与 Compaction 的所有 SST 的 BlobFileSizeProperties，outputs 代表 Compaction 生成的所有 SST 的 BlobFileSizeProperties，discardable size 是通过计算 inputs 和 outputs 得出的每个 BlobFile 被丢弃的数据大小，第一列代表 BlobFile 的文件 ID，第二列代表被丢弃的数据大小。

Titan 会为每个有效的 BlobFile 在内存中维护一个 discardable size 变量，每次 Compaction 结束之后都对相应的 BlobFile 的 discardable size 变量进行累加。注意，在每次重启后会扫描一遍所有的 SST 的 BlobFileSizeProperties 重新构建每个有效 BlobFile 的 discardable size 变量。每次 GC 开始时就可以通过挑选 discardable size 最大的几个 BlobFile 来作为候选的文件。为了减小写放大，我们可以容忍一定的空间放大，所以我们只有在 BlobFile 可丢弃的数据达到一定比例之后才会对其进行 GC。

 

GC 的方式就是对于这些选中的 BlobFile 文件，依次通过查询其中每个 value 相应的 key 的 blob index 是否存在或者更新来确定该 value 是否作废，最终将未作废的 value 归并排序生成新的 BlobFile，并将这些 value 更新后的 blob index 通过 WriteCallback 或者 MergeOperator 的方式写回到 SST 中。在完成 GC 后，这些原来的 BlobFile 文件并不会立即被删除，Titan 会在写回 blob index 后记录 RocksDB 最新的 sequence number，等到最旧 snapshot 的 sequence 超过这个记录的 sequence number 时 BlobFile 才能被删除。这个是因为在写回 blob index 后，还是可能通过之前的 snapshot 访问到老的 blob index，因此需要确保没有 snapshot 会访问到这个老的 blob index 后才能安全删除相应 BlobFile。

### Level-Merge

Level-Merge 是 Titan 近期新加入的一种策略，它的核心思想是 LSM-Tree 在进行 Compaction 的同时，对 SST 文件对应的 BlobFile 进行归并重写产生新的 BlobFile。其流程大概如下图所示： 

![6-LevelMerge.png](/media/titan/titan-6.png)图 6: Level z-1 和 Level z 的 SST 进行 Compaction 时会对 KV 对有序读写一遍，这时就可以对这些 SST 中所涉及的 BlobFile 的 value 有序写到新的 BlobFile 中，并在生成新的 SST 时将 key 的 blob index 进行更新。对于 Compaction 中被删除的 key，相应的 value 也不会写到新的 BlobFile 中，相当于完成了 GC。

相比于传统 GC，Level-Merge 这种方式在 LSM-Tree 进行 Compaction 的同时就完成了 Blob GC，不再需要查询 LSM-Tree 的 blob index 情况和写回新 blob index 到 LSM-Tree 中，减小了 GC 对前台操作影响。同时通过不断的重写 BlobFile，减小了 BlobFile 之间的相互重叠，提高系统整体有序性，也就是提高了 Scan 性能。当然将BlobFile 以类似 tiering compaction 的方式分层会带来写放大，考虑到 LSM-Tree 中 99% 的数据都落在最后两层，因此 Titan 仅对 LSM-Tree 中 Compaction 到最后两层数据对应的 BlobFile 进行 Level-Merge。

#### Range-Merge

还需要考虑两种情况，会导致最底层的有序性越来越差：

- 开启 level_compaction_dynamic_level_bytes，此时  LSM-Tree 各层动态增长，随数据量增大最后一层的sorted run会原来越多。

- 某个 range 被频繁 Compaction 导致该 range 的 sorted runs 较多 

![7-RangeMerge.png](/media/titan/titan-7.png)

因此需要通过 Range Merge 操作维持 sorted run 在一定水平，即在 OnCompactionComplete 时统计该 range 的 sorted run 数量，若数量过多则将涉及的 BlobFile 标记为 ToMerge，在下一次的 Compaction 中进行重写