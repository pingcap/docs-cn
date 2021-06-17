
## Bug 修复

+ TiDB

    - 修复投影消除在投影结果为空时执行结果可能错误的问题 [#24093](https://github.com/pingcap/tidb/pull/24093)
    - 修复列包含 `NULL` 值时查询结果在某些情况下可能错误的问题 [#24063](https://github.com/pingcap/tidb/pull/24063)
    - 当有虚拟列参与扫描时不允许生成 MPP 计划 [#24058](https://github.com/pingcap/tidb/pull/24058)
    - 修复 Plan Cache 中对 `PointGet` 和 `TableDual` 错误的重复使用 [#24043](https://github.com/pingcap/tidb/pull/24043)
    - 修复优化器在为聚簇索引构建 `IndexMerge` 执行计划时出现的错误 [#24042](https://github.com/pingcap/tidb/pull/24042)
    - 修复 BIT 类型相关错误的类型推导 [#24027](https://github.com/pingcap/tidb/pull/24027)
    - 修复某些优化器 Hint 在 `PointGet` 算子存在时无法生效的问题 [#23685](https://github.com/pingcap/tidb/pull/23685)
    - 修复 DDL 遇到错误回滚时可能失败的问题 [#24080](https://github.com/pingcap/tidb/pull/24080)
    - 修复二进制字面值常量的索引范围构造错误的问题 [#24041](https://github.com/pingcap/tidb/pull/24041)
    - 修复某些情况下 `IN` 语句的执行结果可能错误的问题 [#24023](https://github.com/pingcap/tidb/pull/24023)
    - 修复某些字符串函数的返回结果错误的问题 [#23879](https://github.com/pingcap/tidb/pull/23879)
    - 执行 `REPLACE` 语句需要用户同时拥有 `INSERT` 和 `DELETE` 权限 [#23939](https://github.com/pingcap/tidb/pull/23939)
    - 修复点查时出现的的性能回退 [#24070](https://github.com/pingcap/tidb/pull/24070)
    - 修复因错误比较二进制与字节而导致的 `TableDual` 计划错误的问题 [#23918](https://github.com/pingcap/tidb/pull/23918)
    - 修复了在某些情况下，使用前缀索引和 Index Join 导致的 panic 的问题 [#24547](https://github.com/pingcap/tidb/issues/24547) [#24716](https://github.com/pingcap/tidb/issues/24716) [#24717](https://github.com/pingcap/tidb/issues/24717)
    - 修复了 `point get` 的 prepare plan cache 被事务中的 `point get` 语句不正确使用的问题 [#24741](https://github.com/pingcap/tidb/issues/24741)
    - 修复了当排序规则为 `ascii_bin` 或 `latin1_bin` 时，写入错误的前缀索引值的问题 [#24569](https://github.com/pingcap/tidb/issues/24569)
    - 修复了正在执行的事务被 GC worker 中断的问题 [#24591](https://github.com/pingcap/tidb/issues/24591))
    - 修复了当 `new-collation` 开启且 `new-row-format` 关闭的情况下，点查在聚簇索引下可能出错的问题 [#24541](https://github.com/pingcap/tidb/issues/24541)
    - 为 Shuffle Hash Join 重构分区键的转换功能 [#24490](https://github.com/pingcap/tidb/pull/24490)
    - 修复了当查询包含 `HAVING` 子句时，在构建计划的过程中 panic 的问题 [#24045](https://github.com/pingcap/tidb/issues/24045)
    - 修复了列裁剪优化导致 `Apply` 算子和 `Join` 算子执行结果错误的问题 [#23887](https://github.com/pingcap/tidb/issues/23887)
    - 修复了从 Async Commit 回退的主锁无法被清除的问题 [#24384](https://github.com/pingcap/tidb/issues/24384)
    - 修复了一个统计信息 GC 的问题，该问题可能导致重复的 fm-sketch 记录 [#24357](https://github.com/pingcap/tidb/pull/24357)
    - 当悲观锁事务收到 `ErrKeyExists` 错误时，避免不必要的悲观事务回滚 [#23799](https://github.com/pingcap/tidb/issues/23799)
    - 修复了当 sql_mode 包含 `ANSI_QUOTES` 时，数值字面值无法被识别的问题 [#25015](https://github.com/pingcap/tidb/pull/25015)
    - 禁止如 `INSERT INTO table PARTITION (<partitions>) ... ON DUPLICATE KEY UPDATE` 的语句从 non-listed partitions 读取数据 [#24746](https://github.com/pingcap/tidb/issues/24746)
    - 修复了当 SQL 语句包含 `GROUP BY` 以及 `UNION` 时，可能会出现的 `index out of range` 的问题 [#24281](https://github.com/pingcap/tidb/issues/24281)
    - 修复了 `CONCAT` 函数错误处理排序规则的问题 [#24296](https://github.com/pingcap/tidb/issues/24296)
    - 修复了全局变量 `collation_server` 对新会话无法生效的问题 [#24156](https://github.com/pingcap/tidb/pull/24156)

+ TiKV

    - 修复了 Coprocessor 未正确处理 `IN` 表达式有符号整数或无符号整数类型数据的问题 [#10018](https://github.com/tikv/tikv/pull/10018)
    - 修复了在批量 ingest SST 文件后产生大量空 Region 的问题 [#10015](https://github.com/tikv/tikv/pull/10015)
    - 修复了 file dictionary 文件损坏之后 TiKV 无法启动的问题 [#9992](https://github.com/tikv/tikv/pull/9992)
    - 修复了由于读取旧值而导致的 TiCDC OOM 问题 [#9996](https://github.com/tikv/tikv/issues/9996) [#9981](https://github.com/tikv/tikv/issues/9981)
    - 修复了聚簇主键列在次级索引上的 `latin1_bin` 字符集出现空值的问题 [#24548](https://github.com/pingcap/tidb/issues/24548)
    - 新增 `abort-on-panic` 配置，允许 TiKV 在 panic 时生成 core dump 文件。用户仍需正确配置环境以开启 core dump。 [#10216](https://github.com/tikv/tikv/pull/10216)
    - 修复了 TiKV 不繁忙时 `point get` 查询性能回退的问题 [#10046](https://github.com/tikv/tikv/issues/10046)

+ PD

    - 修复在 store 数量多的情况下，切换 PD Leader 慢的问题 [#3697](https://github.com/tikv/pd/issues/3697)
    - 修复删除不存在的 evict leader 调度器时出现 panic 的问题 [#3660](https://github.com/tikv/pd/issues/3660)
    - 修复 offline peer 在合并完后未更新统计的问题 [#3611](https://github.com/tikv/pd/issues/3611)

+ TiFlash

    - 修复 `TIME` 类型转换为 `INT` 类型时产生错误结果的问题
    - 修复 `receiver` 可能无法在 10 秒内找到对应任务的问题
    - 修复 `cancelMPPQuery` 中可能存在无效迭代器的问题
    - 修复 `bitwise` 算子和 TiDB 行为不一致的问题
    - 修复当使用 `prefix key` 时出现范围重叠报错的问题
    - 修复字符串转换为 `INT` 时产生错误结果的问题
    - 修复连续快速写入可能导致 TiFlash 内存溢出的问题
    - 修复 Table GC 时会引发空指针的问题
    - 修复向已被删除的表写数据时 TiFlash 进程崩溃的问题
    - 修复当使用 BR 恢复数据时 TiFlash 进程可能崩溃的问题
    - 修复并发复制共享 Delta 索引导致结果错误的问题
    - 修复 TiFlash 在 Compaction Filter 特性开启时可能崩溃的问题
    - 修复了从 Async Commit 回退的锁无法被 TiFlash 清除的问题
    - 修复当 `TIMEZONE` 类型的转换结果包含 `TIMESTAMP` 类型时返回错误结果的问题
    - 修复 TiFlash 在 Segment Split 期间异常退出的问题

+ Tools

    + TiDB Lightning

        - 修复在生成 KV 数据时可能发生的 panic 问题 [#1127](https://github.com/pingcap/br/pull/1127)
        - 修复数据导入期间 Batch Split Region 因键的总大小超过 Raft 条目限制而可能失败的问题 [#969](https://github.com/pingcap/br/issues/969)

            - 修复在导入 CSV 文件时，如果文件的最后一行未包含换行符(`\r\n`)会导入报错的问题 [#1134](https://github.com/pingcap/br/pull/1134)
        - 修复在导入目标表包含 double 类型的自增列会导致表的 auto_Increment 值异常的问题 [#1178](https://github.com/pingcap/br/pull/1178)

    + Backup & Restore (BR)

        - 修复备份期间少数 TiKV 节点不可用导致的备份中断问题 [#1019](https://github.com/pingcap/br/pull/1019)

    + TiCDC

        - 修复 Unified Sorter 中的并发问题并过滤无用的错误消息 [#1678](https://github.com/pingcap/ticdc/pull/1678)
        - 修复同步到 MinIO 时，重复创建目录会导致同步中断的问题 [#1672](https://github.com/pingcap/ticdc/pull/1672)
        - 默认开启会话变量 `explicit_defaults_for_timestamp`，使得下游 MySQL 5.7 和上游 TiDB 的行为保持一致 [#1659](https://github.com/pingcap/ticdc/pull/1659)
        - 修复错误地处理 `io.EOF` 可能导致同步中断的问题 [#1648](https://github.com/pingcap/ticdc/pull/1648)
        - 修正 TiCDC 面板中的 TiKV CDC endpoint CPU 统计信息 [#1645](https://github.com/pingcap/ticdc/pull/1645)
        - 增加 `defaultBufferChanSize` 来避免某些情况下同步阻塞的问题 [#1632](https://github.com/pingcap/ticdc/pull/1632)
        - 修复 Avro 输出中丢失时区信息的问题 [#1712](https://github.com/pingcap/ticdc/pull/1712)
        - 支持清理 Unified Sorter 过期的文件并禁止共享 `sort-dir` 目录 [#1742](https://github.com/pingcap/ticdc/pull/1742)
        - 修复存在大量过期 Region 信息时 KV 客户端可能锁死的问题 [#1801](https://github.com/pingcap/ticdc/pull/1801)
        - 修复 `--cert-allowed-cn` 参数中错误的帮助消息 [#1697](https://github.com/pingcap/ticdc/pull/1697)
        - 修复因更新 `explicit_defaults_for_timestamp` 而需要 MySQL `SUPER` 权限的问题 [#1750](https://github.com/pingcap/ticdc/pull/1750)
        - 添加 sink 流控以降低内存溢出的风险 [#1840](https://github.com/pingcap/ticdc/pull/1840)
        - 修复调度数据表时可能发生的同步终止问题 [#1828](https://github.com/pingcap/ticdc/pull/1828)
        - 修复 TiCDC changefeed 断点卡住导致 TiKV GC safe point 不推进的问题 [#1759](https://github.com/pingcap/ticdc/pull/1759)
