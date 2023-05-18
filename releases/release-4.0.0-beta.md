---
title: TiDB 4.0 Beta Release Notes
aliases: ['/docs-cn/dev/releases/release-4.0.0-beta/','/docs-cn/dev/releases/4.0.0-beta/']
---

# TiDB 4.0 Beta Release Notes

发版日期：2020 年 1 月 17 日

TiDB 版本：4.0.0-beta

TiDB Ansible 版本：4.0.0-beta

## TiDB

+ 当 `Insert`/`Replace`/`Delete`/`Update` 在执行过程中所使用的内存空间超过启动配置项 `MemQuotaQuery` 的限制时，输出日志或取消本次执行过程，具体行为取决于启动配置项 `OOMAction` [#14179](https://github.com/pingcap/tidb/pull/14179) [#14289](https://github.com/pingcap/tidb/pull/14289) [#14299](https://github.com/pingcap/tidb/pull/14299)
+ 估算 `Index Join` 的代价时由仅考虑驱动表的行数调整为考虑驱动表和被驱动表的行数，提升估算的准确性 [#12085](https://github.com/pingcap/tidb/pull/12085)
+ 新增 15 个 SQL hint，用于控制优化器行为，提升优化器稳定性
    - [#11253](https://github.com/pingcap/tidb/pull/11253) [#11364](https://github.com/pingcap/tidb/pull/11364) [#11673](https://github.com/pingcap/tidb/pull/11673) [#11740](https://github.com/pingcap/tidb/pull/11740) [#11746](https://github.com/pingcap/tidb/pull/11746)
    - [#11809](https://github.com/pingcap/tidb/pull/11809) [#11996](https://github.com/pingcap/tidb/pull/11996) [#12043](https://github.com/pingcap/tidb/pull/12043) [#12059](https://github.com/pingcap/tidb/pull/12059) [#12246](https://github.com/pingcap/tidb/pull/12246)
    - [#12382](https://github.com/pingcap/tidb/pull/12382)
+ 提升查询中所涉及到的列能被索引全覆盖时的性能 [#12022](https://github.com/pingcap/tidb/pull/12022)
+ 对表上的 `OR` 表达式过滤条件，使用多个索引组合进行表访问，提升查询性能 [#10121](https://github.com/pingcap/tidb/pull/10121) [#10512](https://github.com/pingcap/tidb/pull/10512) [#11245](https://github.com/pingcap/tidb/pull/11245) [#12225](https://github.com/pingcap/tidb/pull/12225) [#12248](https://github.com/pingcap/tidb/pull/12248) [#12305](https://github.com/pingcap/tidb/pull/12305) [#12843](https://github.com/pingcap/tidb/pull/12843)
+ 优化 Range 计算流程，缓存并去重索引计算的结果，减少 CPU 开销，提升 range 计算的性能 [#12856](https://github.com/pingcap/tidb/pull/12856)
+ Slow Log 日志的级别与普通日志的级别解耦 [#12359](https://github.com/pingcap/tidb/pull/12359)
+ 新增 `oom-use-tmp-storage` 参数，默认值为 `true`，用于控制当单条 SQL 执行过程中占用内存使用超过 `mem-quota-query` 且 SQL 中包含 `Hash Join` 时，系统会采用临时文件来缓存中间结果 [#11832](https://github.com/pingcap/tidb/pull/11832) [#11937](https://github.com/pingcap/tidb/pull/11937) [#12116](https://github.com/pingcap/tidb/pull/12116) [#12067](https://github.com/pingcap/tidb/pull/12067)
+ 支持使用 `create index`/`alter table add index` 语句创建表达式索引，使用 `drop index` 语句删除表达式索引 [#14117](https://github.com/pingcap/tidb/pull/14117)
+ `query-log-max-len` 参数默认值调大为 `4096`，减少输出被截断 SQL 的数量，此参数可通过 SQL 动态调整 [#12491](https://github.com/pingcap/tidb/pull/12491)
+ 支持在列属性上添加 `AutoRandom` 关键字，用于控制系统自动为主键分配随机整数，避免 `AutoIncrement` 自增主键带来的写入热点问题 [#13127](https://github.com/pingcap/tidb/pull/13127)
+ 支持表级锁 (Table Locks) [#11038](https://github.com/pingcap/tidb/pull/11038)
+ `ADMIN SHOW DDL JOBS` 支持 `LIKE` 或 `WHERE` 语法进行条件过滤 [#12484](https://github.com/pingcap/tidb/pull/12484)
+ `information_schema.tables` 表新增 `TIDB_ROW_ID_SHARDING_INFO` 列，输出列的 RowID 打散相关的信息（例如：表 `A` 指定 `SHARD_ROW_ID_BITS`，该列的值为 `"SHARD_BITS={bit_number}"`）[#13418](https://github.com/pingcap/tidb/pull/13418)
+ 优化 SQL 错误信息的错误码，避免出现多个错误信息的错误码都是 `ERROR 1105 (HY000)`（即类型为 `Unknown Error`）的情况
    - [#14002](https://github.com/pingcap/tidb/pull/14002) [#13874](https://github.com/pingcap/tidb/pull/13874) [#13733](https://github.com/pingcap/tidb/pull/13733) [#13654](https://github.com/pingcap/tidb/pull/13654) [#13646](https://github.com/pingcap/tidb/pull/13646)
    - [#13540](https://github.com/pingcap/tidb/pull/13540) [#13366](https://github.com/pingcap/tidb/pull/13366) [#13329](https://github.com/pingcap/tidb/pull/13329) [#13300](https://github.com/pingcap/tidb/pull/13300) [#13233](https://github.com/pingcap/tidb/pull/13233)
    - [#13033](https://github.com/pingcap/tidb/pull/13033) [#12866](https://github.com/pingcap/tidb/pull/12866) [#14054](https://github.com/pingcap/tidb/pull/14054)
+ 在估算行数时将离散类型的很窄的 range 转化为 `point set` 然后用 CM-Sketch 提升估算精度 [#11524](https://github.com/pingcap/tidb/pull/11524)
+ 支持普通 `Analyze` 得到的 CM-Sketch 维护 `TopN` 信息，将出现次数较多的值单独维护 [#11409](https://github.com/pingcap/tidb/pull/11409)
+ 支持动态调整 CM-Sketch 长宽和 `TopN` 数目 [#11278](https://github.com/pingcap/tidb/pull/11278)
+ 新增 SQL Binding 的自动捕获和自动演进功能 [#13199](https://github.com/pingcap/tidb/pull/13199) [#12434](https://github.com/pingcap/tidb/pull/12434)
+ 优化与 TiKV 之间通信息编码格式，采用 `Chunk` 格式编码，提升网络通信性能 [#12023](https://github.com/pingcap/tidb/pull/12023) [#12536](https://github.com/pingcap/tidb/pull/12536) [#12613](https://github.com/pingcap/tidb/pull/12613) [#12621](https://github.com/pingcap/tidb/pull/12621) [#12899](https://github.com/pingcap/tidb/pull/12899) [#13060](https://github.com/pingcap/tidb/pull/13060) [#13349](https://github.com/pingcap/tidb/pull/13349)
+ 支持新的行存储格式，提升宽表性能 [#12634](https://github.com/pingcap/tidb/pull/12634)
+ 优化 `Recover Binlog` 接口，确保等待当前正在提交的事务都提交完成再返回 [#13740](https://github.com/pingcap/tidb/pull/13740)
+ 新增通过 HTTP `info/all` 接口，查询集群中所有 TiDB server 开启 binlog 的状态 [#13025](https://github.com/pingcap/tidb/pull/13025)
+ 新增在事务模式是悲观事务时，支持使用 MySQL 兼容的 Read Committed 事务隔离级别 [#14087](https://github.com/pingcap/tidb/pull/14087)
+ 支持超大事务，事务大小的限制受限于物理内存大小
    - [#11999](https://github.com/pingcap/tidb/pull/11999) [#11986](https://github.com/pingcap/tidb/pull/11986) [#11974](https://github.com/pingcap/tidb/pull/11974) [#11817](https://github.com/pingcap/tidb/pull/11817) [#11807](https://github.com/pingcap/tidb/pull/11807)
    - [#12133](https://github.com/pingcap/tidb/pull/12133) [#12223](https://github.com/pingcap/tidb/pull/12223) [#12980](https://github.com/pingcap/tidb/pull/12980) [#13123](https://github.com/pingcap/tidb/pull/13123) [#13299](https://github.com/pingcap/tidb/pull/13299)
    - [#13432](https://github.com/pingcap/tidb/pull/13432) [#13599](https://github.com/pingcap/tidb/pull/13599)
+ 提升 `Kill` 稳定性 [#10841](https://github.com/pingcap/tidb/pull/10841)
+ `LOAD DATA` 支持十六进制和二进制表达式作为分隔符 [#11029](https://github.com/pingcap/tidb/pull/11029)
+ `IndexLookupJoin` 拆分为 `IndexHashJoin` 与 `IndexMergeJoin`，提升 `IndexLookupJoin` 的执行性能，减少执行过程中的内存消耗 [#8861](https://github.com/pingcap/tidb/pull/8861) [#12139](https://github.com/pingcap/tidb/pull/12139) [#12349](https://github.com/pingcap/tidb/pull/12349) [#13238](https://github.com/pingcap/tidb/pull/13238) [#13451](https://github.com/pingcap/tidb/pull/13451) [#13714](https://github.com/pingcap/tidb/pull/13714)
+ 修复 RBAC 若干问题 [#13896](https://github.com/pingcap/tidb/pull/13896) [#13820](https://github.com/pingcap/tidb/pull/13820) [#13940](https://github.com/pingcap/tidb/pull/13940) [#14090](https://github.com/pingcap/tidb/pull/14090) [#13940](https://github.com/pingcap/tidb/pull/13940) [#13014](https://github.com/pingcap/tidb/pull/13014)
+ 修复创建视图时，由于 `select` 语句包含 `union` 视图无法创建成功的问题 [#12595](https://github.com/pingcap/tidb/pull/12595)
+ 修复 `CAST` 函数若干问题
    - [#12858](https://github.com/pingcap/tidb/pull/12858) [#11968](https://github.com/pingcap/tidb/pull/11968) [#11640](https://github.com/pingcap/tidb/pull/11640) [#11483](https://github.com/pingcap/tidb/pull/11483) [#11493](https://github.com/pingcap/tidb/pull/11493)
    - [#11376](https://github.com/pingcap/tidb/pull/11376) [#11355](https://github.com/pingcap/tidb/pull/11355) [#11114](https://github.com/pingcap/tidb/pull/11114) [#14405](https://github.com/pingcap/tidb/pull/14405) [#14323](https://github.com/pingcap/tidb/pull/14323)
    - [#13837](https://github.com/pingcap/tidb/pull/13837) [#13401](https://github.com/pingcap/tidb/pull/13401) [#13334](https://github.com/pingcap/tidb/pull/13334) [#12652](https://github.com/pingcap/tidb/pull/12652) [#12864](https://github.com/pingcap/tidb/pull/12864)
    - [#12623](https://github.com/pingcap/tidb/pull/12623) [#11989](https://github.com/pingcap/tidb/pull/11989)
+ Slow log 输出 TiKV RPC 的 `backoff` 具体信息，方便排查问题 [#13770](https://github.com/pingcap/tidb/pull/13770)
+ 优化统一 expensive log 中内存统计信息的格式 [#12809](https://github.com/pingcap/tidb/pull/12809)
+ 优化 `explain` 显式格式，支持输出算子占用内存和磁盘的信息 [#13914](https://github.com/pingcap/tidb/pull/13914) [#13692](https://github.com/pingcap/tidb/pull/13692) [#13686](https://github.com/pingcap/tidb/pull/13686) [#11415](https://github.com/pingcap/tidb/pull/11415) [#13927](https://github.com/pingcap/tidb/pull/13927) [#13764](https://github.com/pingcap/tidb/pull/13764) [#13720](https://github.com/pingcap/tidb/pull/13720)
+ 优化 `LOAD DATA` 重复值检查，按照事务粒度进行且事务大小可通过 `tidb_dml_batch_size` 配置 [#11132](https://github.com/pingcap/tidb/pull/11132)
+ 优化 `LOAD DATA` 性能，将数据读取处理和批量提交分离，且分派到不同的 Worker 处理 [#11533](https://github.com/pingcap/tidb/pull/11533) [#11284](https://github.com/pingcap/tidb/pull/11284)

## TiKV

+ 升级 RocksDB 的版本到 6.4.6
+ 系统启动时自动创建 2GB 大小的空文件，解决磁盘空间被写满时系统无法正常进行 Compaction 的问题 [#6321](https://github.com/tikv/tikv/pull/6321)
+ 新增快速备份恢复功能
    - [#6462](https://github.com/tikv/tikv/pull/6462) [#6395](https://github.com/tikv/tikv/pull/6395) [#6378](https://github.com/tikv/tikv/pull/6378) [#6374](https://github.com/tikv/tikv/pull/6374) [#6349](https://github.com/tikv/tikv/pull/6349)
    - [#6339](https://github.com/tikv/tikv/pull/6339) [#6308](https://github.com/tikv/tikv/pull/6308) [#6295](https://github.com/tikv/tikv/pull/6295) [#6286](https://github.com/tikv/tikv/pull/6286) [#6283](https://github.com/tikv/tikv/pull/6283)
    - [#6261](https://github.com/tikv/tikv/pull/6261) [#6222](https://github.com/tikv/tikv/pull/6222) [#6209](https://github.com/tikv/tikv/pull/6209) [#6204](https://github.com/tikv/tikv/pull/6204) [#6202](https://github.com/tikv/tikv/pull/6202)
    - [#6198](https://github.com/tikv/tikv/pull/6198) [#6186](https://github.com/tikv/tikv/pull/6186) [#6177](https://github.com/tikv/tikv/pull/6177) [#6146](https://github.com/tikv/tikv/pull/6146) [#6071](https://github.com/tikv/tikv/pull/6071)
    - [#6042](https://github.com/tikv/tikv/pull/6042) [#5877](https://github.com/tikv/tikv/pull/5877) [#5806](https://github.com/tikv/tikv/pull/5806) [#5803](https://github.com/tikv/tikv/pull/5803) [#5800](https://github.com/tikv/tikv/pull/5800)
    - [#5781](https://github.com/tikv/tikv/pull/5781) [#5772](https://github.com/tikv/tikv/pull/5772) [#5689](https://github.com/tikv/tikv/pull/5689) [#5683](https://github.com/tikv/tikv/pull/5683)
+ 新增从 Follower 副本读取数据的功能
    - [#5051](https://github.com/tikv/tikv/pull/5051) [#5118](https://github.com/tikv/tikv/pull/5118) [#5213](https://github.com/tikv/tikv/pull/5213) [#5316](https://github.com/tikv/tikv/pull/5316) [#5401](https://github.com/tikv/tikv/pull/5401)
    - [#5919](https://github.com/tikv/tikv/pull/5919) [#5887](https://github.com/tikv/tikv/pull/5887) [#6340](https://github.com/tikv/tikv/pull/6340) [#6348](https://github.com/tikv/tikv/pull/6348) [#6396](https://github.com/tikv/tikv/pull/6396)
+ 提升 TiDB 通过索引读取数据的性能 [#5682](https://github.com/tikv/tikv/pull/5682)
+ 修复 `CAST` 函数在 TiDB 和 TiKV 中行为不一致性的问题
    - [#6459](https://github.com/tikv/tikv/pull/6459) [#6461](https://github.com/tikv/tikv/pull/6461) [#6458](https://github.com/tikv/tikv/pull/6458) [#6447](https://github.com/tikv/tikv/pull/6447) [#6440](https://github.com/tikv/tikv/pull/6440)
    - [#6425](https://github.com/tikv/tikv/pull/6425) [#6424](https://github.com/tikv/tikv/pull/6424) [#6390](https://github.com/tikv/tikv/pull/6390) [#5842](https://github.com/tikv/tikv/pull/5842) [#5528](https://github.com/tikv/tikv/pull/5528)
    - [#5334](https://github.com/tikv/tikv/pull/5334) [#5199](https://github.com/tikv/tikv/pull/5199) [#5167](https://github.com/tikv/tikv/pull/5167) [#5146](https://github.com/tikv/tikv/pull/5146) [#5141](https://github.com/tikv/tikv/pull/5141)
    - [#4998](https://github.com/tikv/tikv/pull/4998) [#5029](https://github.com/tikv/tikv/pull/5029) [#5099](https://github.com/tikv/tikv/pull/5099) [#5006](https://github.com/tikv/tikv/pull/5006) [#5095](https://github.com/tikv/tikv/pull/5095)
    - [#5093](https://github.com/tikv/tikv/pull/5093) [#5090](https://github.com/tikv/tikv/pull/5090) [#4987](https://github.com/tikv/tikv/pull/4987) [#5066](https://github.com/tikv/tikv/pull/5066) [#5038](https://github.com/tikv/tikv/pull/5038)
    - [#4962](https://github.com/tikv/tikv/pull/4962) [#4890](https://github.com/tikv/tikv/pull/4890) [#4727](https://github.com/tikv/tikv/pull/4727) [#6060](https://github.com/tikv/tikv/pull/6060) [#5761](https://github.com/tikv/tikv/pull/5761)
    - [#5793](https://github.com/tikv/tikv/pull/5793) [#5468](https://github.com/tikv/tikv/pull/5468) [#5540](https://github.com/tikv/tikv/pull/5540) [#5548](https://github.com/tikv/tikv/pull/5548) [#5455](https://github.com/tikv/tikv/pull/5455)
    - [#5543](https://github.com/tikv/tikv/pull/5543) [#5433](https://github.com/tikv/tikv/pull/5433) [#5431](https://github.com/tikv/tikv/pull/5431) [#5423](https://github.com/tikv/tikv/pull/5423) [#5179](https://github.com/tikv/tikv/pull/5179)
    - [#5134](https://github.com/tikv/tikv/pull/5134) [#4685](https://github.com/tikv/tikv/pull/4685) [#4650](https://github.com/tikv/tikv/pull/4650) [#6463](https://github.com/tikv/tikv/pull/6463)

## PD

+ 新增根据存储节点负载信息优化热点调度的功能
    - [#1870](https://github.com/pingcap/pd/pull/1870) [#1982](https://github.com/pingcap/pd/pull/1982) [#1998](https://github.com/pingcap/pd/pull/1998) [#1843](https://github.com/pingcap/pd/pull/1843) [#1750](https://github.com/pingcap/pd/pull/1750)
+ 新增 Placement Rules 功能，通过组合不同的调度规则，精细控制任意一段数据的副本的数量、存放位置、存储主机类型、角色等信息
    - [#2051](https://github.com/pingcap/pd/pull/2051) [#1999](https://github.com/pingcap/pd/pull/1999) [#2042](https://github.com/pingcap/pd/pull/2042) [#1917](https://github.com/pingcap/pd/pull/1917) [#1904](https://github.com/pingcap/pd/pull/1904)
    - [#1897](https://github.com/pingcap/pd/pull/1897) [#1894](https://github.com/pingcap/pd/pull/1894) [#1865](https://github.com/pingcap/pd/pull/1865) [#1855](https://github.com/pingcap/pd/pull/1855) [#1834](https://github.com/pingcap/pd/pull/1834)
+ 支持插件功能 (experimental) [#1799](https://github.com/pingcap/pd/pull/1799)
+ 新增调度器支持自定义配置功能，支持配置调度器的作用范围 (experimental) [#1735](https://github.com/pingcap/pd/pull/1735) [#1783](https://github.com/pingcap/pd/pull/1783) [#1791](https://github.com/pingcap/pd/pull/1791)
+ 新增根据集群负载信息自动调整调度速度的功能（experimental，默认不打开）[#1875](https://github.com/pingcap/pd/pull/1875) [#1887](https://github.com/pingcap/pd/pull/1887) [#1902](https://github.com/pingcap/pd/pull/1902)

## Tools

+ TiDB Lightning
    - 命令行增加配置下游数据库密码的参数 [#253](https://github.com/pingcap/tidb-lightning/pull/253)

## TiDB Ansible

+ 下载包增加 Checksum 检查，防止下载到不完整的包 [#1002](https://github.com/pingcap/tidb-ansible/pull/1002)
+ 新增检查 systemd 版本功能，systemd 版本最低要求 `systemd-219-52` [#1020](https://github.com/pingcap/tidb-ansible/pull/1020) [#1074](https://github.com/pingcap/tidb-ansible/pull/1074)
+ 修复 TiDB Lightning 启动时未正确创建日志目录的问题 [#1103](https://github.com/pingcap/tidb-ansible/pull/1103)
+ 修复 TiDB Lightning 自定义端口不生效的问题 [#1107](https://github.com/pingcap/tidb-ansible/pull/1107)
+ 新增支持部署运维 TiFlash 的功能 [#1119](https://github.com/pingcap/tidb-ansible/pull/1119)
