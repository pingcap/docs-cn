---
title: TiDB 5.0 RC Release Notes
---

# TiDB 5.0 RC Release Notes

发版日期：2021 年 1 月 12 日

TiDB 版本：5.0.0-rc

TiDB 5.0.0-rc 版本是 5.0 版本的前序版本。在 5.0 版本中，我们专注于帮助企业基于 TiDB 数据库快速构建应用程序，使企业在构建过程中无需担心数据库的性能、性能抖动、安全、高可用、容灾、SQL 语句的性能问题排查等问题。

在 TiDB 5.0 版本中，你可以获得以下关键特性：

+ 开启聚簇索引功能，提升数据库的性能。例如：TPC-C tpmC 测试下的性能提升了 39%。
+ 开启异步提交事务功能，降低写入数据的延迟。例如：Sysbench oltp-insert 测试中延迟降低了 37.3%。
+ 通过提升优化器的稳定性及限制系统任务对 I/O、网络、CPU、内存等资源的占用，降低系统的抖动。例如：长期测试 72 小时，衡量 Sysbench TPS 抖动标准差的值从 11.09% 降低到 3.36%。
+ 引入 Raft Joint Consensus 算法，确保 Region 成员变更时系统的可用性。
+ 优化 `EXPLAIN` 功能、引入不可见索引等功能帮助提升 DBA 调试及 SQL 语句的效率。
+ 通过备份文件到 AWS S3、Google Cloud GCS 或者从 AWS S3、Google Cloud GCS 恢复到 TiDB，确保企业数据的可靠性。
+ 提升从 AWS S3 或者 TiDB/MySQL导入导出数据的性能，帮忙企业在云上快速构建应用。例如：导入 1TiB TPC-C 数据性能提升了 40%，由 254 GiB/h 提升到 366 GiB/h。

## SQL

### 支持聚簇索引（实验特性）

开启聚簇索引功能后，TiDB 性能在以下条件下会有较大幅度的提升，例如：TPC-C tpmC 的性能提升了 39%。聚簇索引主要在以下条件时会有性能提升：

+ 插入数据时会减少一次从网络写入索引数据。
+ 等值条件查询仅涉及主键时会减少一次从网络读取数据。
+ 范围条件查询仅涉及主键时会减少多次从网络读取数据。
+ 等值或范围条件查询涉及主键的前缀时会减少多次从网络读取数据。

聚簇索引定义了数据在表中的物理存储顺序，表的数据只能按照聚簇索引的定义进行排序，每个表只能有一个聚簇索引。

用户可通过修改 `tidb_enable_clustered_index` 变量的方式开启聚簇索引功能。开启后仅在创建新表时生效，适用于主键是多个列或者单个列的非整数类型。如果主键是单列整数类型或者表没有主键，系统会按照原有的方式进行数据排序，不受聚簇索引的影响。

例如，可通过 `select tidb_pk_type from information_schema.tables where table_name = '{tbl_name}'` 语名可查询 `tbl_name` 是否有聚簇索引。

+ [用户文档](/system-variables.md#tidb_enable_clustered_index-从-v50-版本开始引入)
+ 相关 issue：[#4841](https://github.com/pingcap/tidb/issues/4841)

### 支持不可见索引

DBA 调试和选择相对最优的索引时，可以通过 SQL 语句将某个索引设置成 `Visible` 或者 `Invisible`，避免执行消耗资源较多的操作，例如：`DROP INDEX` 或 `ADD INDEX`。

DBA 通过 `ALTER INDEX` 语句来修改某个索引的可见性。修改后优化器会根据索引的可见性决定是否将此索引加入到索引列表中。

+ [用户文档](/sql-statements/sql-statement-alter-index.md)
+ 相关 issue：[#9246](https://github.com/pingcap/tidb/issues/9246)

### 支持 `EXCEPT`/`INTERSECT` 操作符

`INTERSECT` 操作符是一个集合操作符，返回两个或者多个查询结果集的交集。一定程度上可以替代 `Inner Join` 操作符。

`EXCEPT` 操作符是一个集合操作符，将两个查询语句的结果合并在一起，并返回在第一个查询语句中有但在第二个查询句中不存在的结果集。

+ [用户文档](/functions-and-operators/set-operators.md)
+ 相关 issue：[#18031](https://github.com/pingcap/tidb/issues/18031)

## 事务

### 提升悲观事务执行成功的概率

悲观事务模式下，如果事务所涉及到的表存在并发 DDL 操作和 `SCHEMA VERSION` 变更，系统会自动将该事务的 `SCHEMA VERSION` 更新到最新版本，确保事务会提交成功，避免事务因 DDL 操作而中断。事务中断时客户端会收到 `Information schema is changed` 的错误信息。

+ [用户文档](/system-variables.md#tidb_enable_amend_pessimistic_txn-从-v407-版本开始引入)
+ 相关 issue：[#18005](https://github.com/pingcap/tidb/issues/18005)

## 字符集和排序规则

使用 `utf8mb4_unicode_ci` 和 `utf8_unicode_ci` 排序规则和字符集比较排序时不区分大小写。

+ [用户文档](/character-set-and-collation.md#新框架下的排序规则支持)
+ 相关 issue：[#17596](https://github.com/pingcap/tidb/issues/17596)

## 安全

### 错误信息和日志信息的脱敏

系统在输出错误信息和日志信息时，支持对敏感信息进行脱敏处理，避免敏感信息泄露。敏感信息可能是身份证信息、信用卡号等。

+ 通过 SQL 语句修改 `tidb_redact_log=1` 开启 tidb-server 的错误信息和日志信息脱敏功能
+ 通过修改 tikv-server 的 `security.redact-info-log = true` 配置项开启错误信息和日志信息脱敏功能
+ 通过修改 pd-server 的 `security.redact-info-log = true` 配置项开启错误信息和日志信息脱敏功能 [#2852](https://github.com/tikv/pd/issues/2852) [#3011](https://github.com/tikv/pd/pull/3011)
+ 通过修改 tiflash-server 的 `security.redact_info_log = true` 以及 tiflash-learner 的 `security.redact-info-log = true` 配置项开启错误信息和日志信息脱敏功能

[用户文档](/log-redaction.md)

相关 issue：[#18566](https://github.com/pingcap/tidb/issues/18566)

## 性能提升

### 支持异步提交事务（实验特性）

开启异步提交事务可使延迟有较大幅度的降低，例如：Sysbench oltp-insert 测试中开启异步提交事务的延迟与不开启时相比降低了 37.3%。

数据库的客户端会同步等待数据库通过两阶段 (2PC) 完成事务的提交。开启 Async Commit 特性后事务两阶段提交在第一阶段提交成功后就会返回结果给客户端，第二阶段会在后台异步执行。通过事务两阶段异步提交的方式降低事务提交的延迟。

此特性只能显式地修改 `tidb_guarantee_external_consistency = ON` 变量后才能保证事务的外部一致性。开启后性能有较大幅度的下降。

用户可通过修改 `tidb_enable_async_commit = ON` 全局变量开启此功能。

+ [用户文档](/system-variables.md#tidb_enable_async_commit-从-v50-版本开始引入)
+ 相关 issue：[#8316](https://github.com/tikv/tikv/issues/8316)

### 提升优化器选择索引的稳定性（实验特性）

优化器若无法长期稳定地选择相对合适的索引，会在很大程度上决定着查询语句的延迟是否有抖动。为确保相同的 SQL 语句不会因为统计信息缺失、不准确等因素导致优化器每次都从多个候选索引选持不同的索引，我们对统计信息模块进行了完善和重构。主要完善如下：

+ 扩展统计信息功能，收集多列 NDV、多列顺序依赖性、多列函数依赖性等信息，帮助优化器选择相对较优的索引。
+ 重构统计信息模块，帮助优化器选择相对较优的索引。
    + 从 `CMSKetch` 中删除 `TopN` 值。
    + 重构 `TopN` 搜索逻辑。
    + 从直方图中删除 `TopN` 信息，建立直方图的索引，方便维护 Bucket NDV。

相关 issue：[#18065](https://github.com/pingcap/tidb/issues/18065)

### 优化因调度功能不完善或者 I/O 限流不完善引起的性能抖动问题

TiDB 调度过程中会占用 I/O、Network、CPU、Memory 等资源，若不对调度的任务进行控制，QPS 和延时会因为资源被抢占而出现性能抖动问题。通过以下几项的优化，长期测试 72 小时，衡量 Sysbench TPS 抖动标准差的值从 11.09% 降低到 3.36%。

+ 减少节点的容量总是在水位线附近波动引起的调度及 PD 的 `store-limit` 配置项设置过大引起的调度，引入一套新的调度算分公式并通过 `region-score-formula-version = v2` 配置项启用新的调度算分公式 [#3269](https://github.com/tikv/pd/pull/3269)
+ 通过修改 `enable-cross-table-merge = true` 开启跨 Region 合并功能，减少空 Region 的数量 [#3129](https://github.com/tikv/pd/pull/3129)
+ TiKV 后台压缩数据会占用大量 I/O 资源，系统通过自动调整压缩的速度来平衡后台任务与前端的数据读写对 I/O 资源的争抢，通过 `rate-limiter-auto-tuned` 配置项开启此功能后，延迟抖动比未开启此功能时的抖动大幅减少 [#18011](https://github.com/pingcap/tidb/issues/18011)
+ TiKV 在进行垃圾数据回收和数据压缩时，分区会占用 CPU、I/O 资源，系统执行这两个任务过程中存在数据重叠。GC Compaction Filter 特性将这两个任务合二为一在同一个任务中完成，减 I/O 的占用。此特性为实验性特性，通过 `gc.enable-compaction-filter = ture` 开启 [#18009](https://github.com/pingcap/tidb/issues/18009)
+ TiFlash 压缩或者整理数据会占用大量 I/O 资源，系统通过限制压缩或整理数据占用的 I/O 量缓解资源争抢。此特性为实验性特性，通过 `bg_task_io_rate_limit` 配置项开启限制压缩或整理数据 I/O 资源。

相关 issue：[#18005](https://github.com/pingcap/tidb/issues/18005)

### 提升 Real-time BI / Data Warehousing 场景下 TiFlash 的稳定性

+ 限制 DeltaIndex 的内存使用量，避免大数据量下内存使用过多导致系统 OOM。
+ 限制后台数据整理任务使用的 I/O 写流量，降低对前台任务的影响。
+ 新增加线程池，排队处理 coprocessor 任务，避免高并发处理 coprocessor 时内存占用过多导致系统 OOM。

### 其他性能优化

+ 提升 `delete * from table where id < ?` 语句执行的性能，p99 性能提升了 4 倍 [#18028](https://github.com/pingcap/tidb/issues/18028)
+ TiFlash 支持同时向本地多块磁盘并发读、写数据，充分利用本地多块磁盘并发的读、写数据的能力，提升性能

## 高可用和容灾

### 提升 Region 成员变更时的可用性（实验特性）

Region 在完成成员变更时，由于“添加”和“删除”成员操作分成两步，如果此时有故障发生会引起 Region 不可用并且会返回前端业务的错误信息。引入的 Raft Joint Consensus 算法，可提升 Region 成员变更时的可用性，将成员变更操作中的“添加”和“删除”合并为一个操作，并发送给所有成员。在变更过程中，Region 处于中间的状态，如果任何被修改的成员失败，系统仍然可以使用。用户可通过 `pd-ctl config set enable-joint-consensus true` 修改成员变量的方式开启此功能。

+ [用户文档](/pd-configuration-file.md#enable-joint-consensus-从-v50-版本开始引入)
+ 相关 issue：[#18079](https://github.com/pingcap/tidb/issues/18079) [#7587](https://github.com/tikv/tikv/issues/7587) [#2860](https://github.com/tikv/pd/issues/2860)

### 优化内存管理模块，降低系统内存溢出的风险

+ 减少缓存统计信息的内存消耗。
+ 减少使用 Dumpling 工具导出数据时的内存消耗。
+ 通过将数据加密码的中间结果存储到磁盘，减少内存消耗。

## 备份与恢复

+ BR 支持将数据备份到 AWS S3、Google Cloud GCS（[用户文档](/br/use-br-command-line-tool.md#备份数据到-amazon-s3-后端存储)）
+ BR 支持从 AWS S3、Google Cloud GCS 恢复数据到 TiDB（[用户文档](/br/use-br-command-line-tool.md#从-amazon-s3-后端存储恢复数据)）
+ 相关 issue：[#89](https://github.com/pingcap/br/issues/89)

## 数据的导入和导出

+ TiDB Lightning 支持从 AWS S3 将 Aurora Snapshot 数据导入 TiDB（相关 issue：[#266](https://github.com/pingcap/tidb-lightning/issues/266)）
+ 使用 TiDB Lightning 在 DBaaS T1.standard 中导入 1TiB TPCC 数据，性能提升了 40%，由 254 GiB/h 提升到 366 GiB/h
+ Dumpling 支持将 TiDB/MySQL 数据导出到 AWS S3（实验特性）（相关 issue：[#8](https://github.com/pingcap/dumpling/issues/8)，[用户文档](/dumpling-overview.md#导出到-amazon-s3-云盘)）

## 问题诊断

### 优化 `EXPLAIN` 功能，收集更多的信息，方便 DBA 排查性能问题

DBA 在排查 SQL 语句性能问题时，需要比较详细的信息来判断引起性能问题的原因。之前版本中 `EXPLAIN` 收集的信息不够完善，DBA 只能通过日志信息、监控信息或者盲猜的方式来判断问题的原因，效率比较低。此版本通过以下几项优化事项提升排查问题效率：

+ 支持对所有 DML 语句使用 `EXPLAIN ANALYZE` 语句以查看实际的执行计划及各个算子的执行详情 [#18056](https://github.com/pingcap/tidb/issues/18056)
+ 支持对正在执行的 SQL 语句使用 `EXPLAIN FOR CONNECTION` 语句以查看实时执行状态，如各个算子的执行时间、已处理的数据行数等 [#18233](https://github.com/pingcap/tidb/issues/18233)
+ `EXPLAIN ANALYZE` 语句显示的算子执行详情中新增算子发送的 RPC 请求数、处理锁冲突耗时、网络延迟、RocksDB 已删除数据的扫描量、RocksDB 缓存命中情况等 [#18663](https://github.com/pingcap/tidb/issues/18663)
+ 慢查询日志中自动记录 SQL 语句执行时的详细执行状态，输出的信息与 `EXPLAIN ANALYZE` 语句输出信息保持一致，例如各个算子消耗的时间、处理数据行数、发送的 RPC 请求数等 [#15009](https://github.com/pingcap/tidb/issues/15009)

[用户文档](/sql-statements/sql-statement-explain.md)

## 部署及运维

+ TiUP 支持将 TiDB Ansible 的配置信息导入到 TiUP。以前导入 Ansible 集群的时候 TiUP 会将用户的配置放在 `ansible-imported-configs` 目录下面。用户后续修改配置执行 `tiup cluster edit-config` 时，配置编辑界面中不显示导入的配置，会给用户造成困扰。现在导入 TiDB Ansible 配置信息的时候 TiUP 不仅会放一份到 ansible-imported-configs 目录下面，还会导入到 `tiup cluster edit` 的配置编辑界面，这样用户以后编辑集群配置时就能够看到导入的配置了。
+ 增强 TiUP `mirror`命令的功能，支持将多个镜像合并成一个，支持在本地镜像发布组件，支持添加组件所有者到本地镜像 [#814](https://github.com/pingcap/tiup/issues/814)
    + 金融行业或者大型企业生产环境的变更是一项非常严肃的事情，若每个版本都采用光盘安装一次，用户使用起来不是很方便。TiUP 提升 `merge` 命令将多个安装包合并成一个，方便 DBA 安装部署。
    + 在 v4.0 中，用户发布自建的镜像时需要启动 tiup-server，使用起来不是很方便。在 v5.0 中，执行 `tiup mirror set` 将当前镜像设置成本地的镜像就可以方便发布自建镜像。
