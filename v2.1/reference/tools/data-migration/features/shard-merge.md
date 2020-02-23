---
title: 分库分表合并同步
category: reference
---

# 分库分表合并同步

本文介绍了 DM 提供的分库分表合并同步功能。此功能用于将上游 MySQL/MariaDB 实例中结构相同的表同步到下游 TiDB 的同一个表中。DM 不仅支持同步上游的 DML 数据，也支持协调同步多个上游分表的 DDL 表结构变更。

> **注意：**
>
> 要执行分库分表合并同步任务，必须在任务配置文件中设置 `is-sharding: true`。

## 使用限制

DM 进行分表 DDL 的同步有以下几点使用限制：

- 在一个逻辑 sharding group（需要合并同步到下游同一个表的所有分表组成的 group）内，所有上游分表必须以相同的顺序执行相同的 DDL 语句（库名和表名可以不同），并且只有在所有分表执行完当前一条 DDL 语句后，下一条 DDL 语句才能执行。

    - 比如，如果在 table_1 表中先增加列 a 后再增加列 b，则在 table_2 表中就不能先增加列 b 后再增加列 a，因为 DM 不支持以不同的顺序来执行相同的 DDL 语句。

- 对于每个逻辑 sharding group，推荐使用一个独立的任务进行同步。

    - 如果一个任务内存在多个 sharding group，则必须等待一个 sharding group 的 DDL 语句同步完成后，才能开始对其他 sharding group 执行 DDL 语句。

- 在一个逻辑 sharding group 内，所有上游分表都应该执行对应的 DDL 语句。

    - 比如，若 DM-worker-2 对应的一个或多个上游分表未执行 DDL 语句，则其他已执行 DDL 语句的 DM-worker 都会暂停同步任务，直到等到 DM-worker-2 收到上游对应的 DDL 语句。

- sharding group 数据同步任务不支持 `DROP DATABASE/TABLE` 语句。

    - DM-worker 中的 binlog 同步单元（sync）会自动忽略掉上游分表的 `DROP DATABASE` 和 `DROP TABLE` 语句。

- sharding group 数据同步任务支持 `RENAME TABLE` 语句，但有如下限制（online DDL 中的 `RENAME` 有特殊方案进行支持）：

    - 只支持 `RENAME TABLE` 到一个不存在的表。
    - 一条 `RENAME TABLE` 语句只能包含一个 `RENAME` 操作。

- 增量同步任务需要确认开始同步的 binlog position 上各分表的表结构必须一致，才能确保来自不同分表的 DML 语句能够同步到表结构确定的下游，并且后续各分表的 DDL 语句能够正确匹配与同步。

- 如果需要变更 [table routing 规则](/v2.1/reference/tools/data-migration/features/overview.md#table-routing)，必须先等所有 sharding DDL 语句同步完成。

    - 在 sharding DDL 语句同步过程中，使用 dmctl 尝试变更 router-rules 会报错。

- 如果需要创建新表加入到一个正在执行 DDL 语句的 sharding group 中，则必须保持新表结构和最新更改的表结构一致。

    - 比如，原 table_1, table_2 表初始时有 (a, b) 两列，sharding DDL 语句执行后有 (a, b, c) 三列，则同步完成后新创建的表也应当有 (a, b, c) 三列。

- 由于已经收到 DDL 语句的 DM-worker 会暂停任务以等待其他 DM-worker 收到对应的 DDL 语句，因此数据同步延迟会增加。

## 背景

目前，DM 使用 ROW 格式的 binlog 进行数据同步，且 binlog 中不包含表结构信息。在 ROW 格式的 binlog 同步过程中，如果不需要将多个上游表合并同步到下游的同一个表，则只存在一个上游表的 DDL 语句会更新对应下游表结构。ROW 格式的 binlog 可以认为是具有 self-description 属性。

分库分表合并同步过程中，可以根据 column values 及下游的表结构构造出相应的 DML 语句，但此时若上游的分表执行 DDL 语句进行了表结构变更，则必须对该 DDL 语句进行额外同步处理，以避免因为表结构和 binlog 数据不一致而造成同步出错的问题。

以下是一个简化后的例子：

![shard-ddl-example-1](/media/shard-ddl-example-1.png)

在上图的例子中，分表的合库合表过程简化成了上游只有两个 MySQL 实例，每个实例内只有一个表。假设在数据同步开始时，将两个分表的表结构版本记为 schema V1，将 DDL 语句执行完后的表结构版本记为 schema V2。

现在，假设数据同步过程中，DM-worker 内的 binlog 同步单元（sync）从两个上游分表收到的 binlog 数据有如下时序：

1. 开始同步时，sync 从两个分表收到的都是 schema V1 版本的 DML 语句。

2. 在 t1 时刻，sync 收到实例 1 上分表的 DDL 语句。

3. 从 t2 时刻开始，sync 从实例 1 收到的是 schema V2 版本的 DML 语句；但从实例 2 收到的仍是 schema V1 版本的 DML 语句。

4. 在 t3 时刻，sync 收到实例 2 上分表的 DDL 语句。

5. 从 t4 时刻开始，sync 从实例 2 收到的也是 schema V2 版本的 DML 语句。

假设在数据同步过程中，不对分表的 DDL 语句进行额外处理。当实例 1 的 DDL 语句同步到下游后，下游的表结构会变更成为 schema V2 版本。但在 t2 到 t3 这段时间内，sync 从实例 2 上收到的仍是 schema V1 版本的 DML 语句。当尝试把这些 schema V1 版本的 DML 语句同步到下游时，就会由于 DML 语句与表结构的不一致而发生错误，从而无法正确同步数据。

## 实现原理

基于上述例子，本部分介绍了 DM 在合库合表过程中进行 DDL 同步的实现原理。

![shard-ddl-flow](/media/shard-ddl-flow.png)

在这个例子中，DM-worker-1 负责同步来自 MySQL 实例 1 的数据，DM-worker-2 负责同步来自 MySQL 实例 2 的数据，DM-master 负责协调多个 DM-worker 间的 DDL 同步。

从 DM-worker-1 收到 DDL 语句开始，简化后的 DDL 同步流程为：

1. 在 t1 时刻，DM-worker-1 收到来自 MySQL 实例 1 的 DDL 语句，自身暂停该 DDL 语句对应任务的 DDL 及 DML 数据同步，并将 DDL 相关信息发送给 DM-master。

2. DM-master 根据收到的 DDL 信息判断得知需要协调该 DDL 语句的同步，于是为该 DDL 语句创建一个锁，并将 DDL 锁信息发回给 DM-worker-1，同时将 DM-worker-1 标记为这个锁的 owner。

3. DM-worker-2 继续进行 DML 语句的同步，直到在 t3 时刻收到来自 MySQL 实例 2 的 DDL 语句，自身暂停该 DDL 语句对应任务的数据同步，并将 DDL 相关信息发送给 DM-master。

4. DM-master 根据收到的 DDL 信息判断得知该 DDL 语句对应的锁信息已经存在，于是直接将对应锁信息发回给 DM-worker-2。

5. 根据任务启动时的配置信息、上游 MySQL 实例分表信息、部署拓扑信息等，DM-master 判断得知自身已经收到了来自待合表的所有上游分表的 DDL 语句，于是请求 DDL 锁的 owner（DM-worker-1）向下游同步执行该 DDL。

6. DM-worker-1 根据第二步收到的 DDL 锁信息验证 DDL 语句执行请求；向下游执行 DDL，并将执行结果反馈给 DM-master；若 DDL 语句执行成功，则自身开始继续同步后续的（从 t2 时刻对应的 binlog 开始的）DML 语句。

7. DM-master 收到来自 owner 执行 DDL 语句成功的响应，于是请求在等待该 DDL 锁的所有其他 DM-worker（DM-worker-2）忽略该 DDL 语句，直接继续同步后续的（从 t4 时刻对应的 binlog 开始的）DML 语句。

根据上面的流程，可以归纳出 DM 协调多个 DM-worker 间 sharding DDL 同步的特点：

- 根据任务配置与 DM 集群部署拓扑信息，DM-master 内部也会建立一个逻辑 sharding group 来协调 DDL 同步，group 中的成员为负责处理该同步任务拆解后的各子任务的 DM-worker。

- 各 DM-worker 从 binlog event 中收到 DDL 语句后，会将 DDL 信息发送给 DM-master。

- DM-master 根据来自 DM-worker 的 DDL 信息及 sharding group 信息创建或更新 DDL 锁。

- 如果 sharding group 的所有成员都收到了某一条相同的 DDL 语句，则表明上游分表在该 DDL 执行前的 DML 语句都已经同步完成，此时可以执行该 DDL 语句，并继续后续的 DML 同步。

- 上游所有分表的 DDL 在经过 [table router](/v2.1/reference/tools/data-migration/features/overview.md#table-routing) 转换后需要保持一致，因此仅需 DDL 锁的 owner 执行一次该 DDL 语句即可，其他 DM-worker 可直接忽略对应的 DDL 语句。

在上面的示例中，每个 DM-worker 对应的上游 MySQL 实例中只有一个待合并的分表。但在实际场景下，一个 MySQL 实例可能有多个分库内的多个分表需要进行合并，这种情况下，sharding DDL 的协调同步过程将更加复杂。

假设同一个 MySQL 实例中有 table_1 和 table_2 两个分表需要进行合并：

![shard-ddl-example-2](/media/shard-ddl-example-2.png)

在这个例子中，由于数据来自同一个 MySQL 实例，因此所有数据都是从同一个 binlog 流中获得，时序如下：

1. 开始同步时，DM-worker 内的 sync 从两个分表收到的数据都是 schema V1 版本的 DML 语句。

2. 在 t1 时刻，sync 收到 table_1 分表的 DDL 语句。

3. 从 t2 到 t3 时刻，sync 收到的数据同时包含 table_1 的 DML 语句（schema V2 版本）及 table_2 的 DML 语句（schema V1 版本）。

4. 在 t3 时刻，sync 收到 table_2 分表的 DDL 语句。

5. 从 t4 时刻开始，sync 从两个分表收到的数据都是 schema V2 版本的 DML 语句。

假设在数据同步过程中，不对分表的 DDL 语句进行额外处理。当 table_1 的 DDL 语句同步到下游从而变更下游表结构后，table_2 的 DML 语句（schema V1 版本）将无法正常同步。因此，在单个 DM-worker 内部，我们也构造了与 DM-master 内类似的逻辑 sharding group，但 group 的成员是同一个上游 MySQL 实例的不同分表。

DM-worker 内协调处理 sharding group 的同步与 DM-master 处理 DM-worker 之间的同步不完全一致，主要原因包括：

- 当 DM-worker 收到 table_1 分表的 DDL 语句时，同步不能暂停，需要继续解析 binlog 才能获得后续 table_2 分表的 DDL 语句，即需要从 t2 时刻继续解析直到 t3 时刻。

- 在继续解析 t2 到 t3 时刻的 binlog 的过程中，table_1 分表的 DML 语句（schema V2 版本）不能向下游同步；但当 sharding DDL 同步并执行成功后，这些 DML 语句则需要同步到下游。

DM-worker 内部 sharding DDL 同步的简化流程为：

1. 在 t1 时刻，DM-worker 收到 table_1 的 DDL 语句，并记录 DDL 信息及此时的 binlog 位置点信息。

2. DM-worker 继续向前解析 t2 到 t3 时刻的 binlog。

3. 对于 table_1 的 DML 语句（schema V2 版本），忽略；对于 table_2 的 DML 语句（schema V1 版本），正常同步到下游。

4. 在 t3 时刻，DM-worker 收到 table_2 的 DDL 语句，并记录 DDL 信息及此时的 binlog 位置点信息。

5. 根据同步任务配置信息、上游库表信息等，DM-worker 判断得知该 MySQL 实例上所有分表的 DDL 语句都已收到；于是将该 DDL 语句同步到下游执行并变更下游表结构。

6. DM-worker 设置 binlog 流的新解析起始位置点为第一步时保存的位置点。

7. DM-worker 重新开始解析从 t2 到 t3 时刻的 binlog。

8. 对于 table_1 的 DML 语句（schema V2 版本），正常同步到下游；对于 table_2 的 DML 语句（schema V1 版本），忽略。

9. 解析到达第四步时保存的 binlog 位置点，可得知在第三步时被忽略的所有 DML 语句都已经重新同步到下游。

10. DM-worker 继续从 t4 时刻对应的 binlog 位置点开始正常同步。

综上可知，DM 在处理 sharding DDL 同步时，主要通过两级 sharding group 来进行协调控制，简化的流程为：

1. 各 DM-worker 独立地协调对应上游 MySQL 实例内多个分表组成的 sharding group 的 DDL 同步。

2. 当 DM-worker 收到所有分表的 DDL 语句时，向 DM-master 发送 DDL 相关信息。

3. DM-master 根据 DM-worker 发来的 DDL 信息，协调由各 DM-worker 组成的 sharing group 的 DDL 同步。

4. 当 DM-master 收到所有 DM-worker 的 DDL 信息时，请求 DDL 锁的 owner（某个 DM-worker） 执行该 DDL 语句。

5. DDL 锁的 owner 执行 DDL 语句，并将结果反馈给 DM-master；自身开始重新同步在内部协调 DDL 同步过程中被忽略的 DML 语句。

6. 当 DM-master 收到 owner 执行 DDL 成功的消息后，请求其他所有 DM-worker 继续开始同步。

7. 其他所有 DM-worker 各自开始重新同步在内部协调 DDL 同步过程中被忽略的 DML 语句。

8. 在完成被忽略的 DML 语句的重新同步后，所有 DM-worker 继续正常同步。
