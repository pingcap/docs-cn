# TiFlash FAQ
问：TiFlash 是否可直接写入？
答：TiFlash 暂时只能通过写入 TiKV 再同步到 TiFlash 而无法直接接受写入

问：如果想在已经存在的集群增加 TiFlash，怎么去估算存储资源？
答：可以衡量哪些表可能需要加速，这些表单副本大小大致就是 TiFlash 两副本所需的空间，再算上计划的余量就行。

问：TiFlash 的数据如何做到高可用？
答：TiFlash 可以通过 TiKV 恢复数据，只要 TiKV 的对应 Region 没有不可用，那么 TiFlash 可以从中恢复数据。

问：TiFlash 推荐设置多少个副本？
答：如果需要 TiFlash 服务本身高可用（并非数据高可用），那么推荐 2 副本；如果可以允许 TiFlash 丢失节点的情况下通过 TiKV 副本继续服务，那么也可以使用单副本。

问：什么时候使用 TiSpark 什么时候使用 TiDB-Server 进行查询？
答：如果查询以单表集合和过滤为主，那么 TiDB-Server 比 TiSpark 在列存上拥有更好的性能；如果查询以表连接为主，那么推荐使用 TiSpark。
