---
title: TiDB 2.1.18 Release Notes
aliases: ['/docs-cn/dev/releases/release-2.1.18/','/docs-cn/dev/releases/2.1.18/']
---

# TiDB 2.1.18 Release Notes

发版日期：2019 年 11 月 4 日

TiDB 版本：2.1.18

TiDB Ansible 版本：2.1.18

## TiDB

+ SQL 优化器
    - 修复 Feedback 切分查询范围出错的问题 [#12172](https://github.com/pingcap/tidb/pull/12172)
    - 修复点查中权限检查不正确的问题 [#12341](https://github.com/pingcap/tidb/pull/12341)
    - 将 Limit 算子下推到 `IndexLookUpReader` 执行逻辑中，优化 `select ... limit ... offset ...` 的执行性能 [#12380](https://github.com/pingcap/tidb/pull/12380)
    - 支持在 `ORDER BY`、`GROUP BY` 和 `LIMIT OFFSET` 中使用参数 [#12514](https://github.com/pingcap/tidb/pull/12514)
    - 修复 partition 表上的 IndexJoin 返回错误结果的问题 [#12713](https://github.com/pingcap/tidb/pull/12713)
    - 修复 TiDB 中 `str_to_date` 函数在日期字符串和格式化字符串不匹配的情况下，返回结果与 MySQL 不一致的问题 [#12757](https://github.com/pingcap/tidb/pull/12757)
    - 修复当查询条件中包含 cast 函数时 outer join 被错误转化为 inner join 的问题 [#12791](https://github.com/pingcap/tidb/pull/12791)
    - 修复 AntiSemiJoin 的 join 条件中错误的表达式传递 [#12800](https://github.com/pingcap/tidb/pull/12800)
+ SQL 执行引擎
    - 修复时间取整不正确的问题，（如 2019-09-11 11:17:47.999999666 应该被取整到 2019-09-11 11:17:48）[#12259](https://github.com/pingcap/tidb/pull/12259)
    - 修复 `PREPARE` 语句类型没有记录在监控中的问题 [#12329](https://github.com/pingcap/tidb/pull/12329)
    - 修复 `FROM_UNIXTIME` 在检查 NULL 值时 panic 的错误 [#12572](https://github.com/pingcap/tidb/pull/12572)
    - 修复 `YEAR` 类型数据插入非法年份时，结果为 `NULL` 而不是 `0000` 的兼容性问题 [#12744](https://github.com/pingcap/tidb/pull/12744)
    - 改进 AutoIncrement 列隐式分配时的行为，与 MySQL 自增锁的默认模式 (["consecutive" lock mode](https://dev.mysql.com/doc/refman/5.7/en/innodb-auto-increment-handling.html)) 保持一致：对于单行 Insert 语句的多个自增 AutoIncrement ID 的隐式分配，TiDB 保证分配值的连续性。该改进保证 JDBC `getGeneratedKeys()` 方法在任意场景下都能得到正确的结果。 [#12619](https://github.com/pingcap/tidb/pull/12619)
    - 修复当 HashAgg 作为 Apply 子节点时查询 hang 住的问题 [#12769](https://github.com/pingcap/tidb/pull/12769)
    - 修复逻辑表达式 AND / OR 在涉及类型转换时返回错误结果的问题 [#12813](https://github.com/pingcap/tidb/pull/12813)
+ Server
    - 修复 `KILL TIDB QUERY` 语法对 `SLEEP()` 语句无效的问题 [#12159](https://github.com/pingcap/tidb/pull/12159)
    - 修复 AUTO INCREMENT 分配 MAX int64 和 MAX uint64 没有报错的问题 [#12210](https://github.com/pingcap/tidb/pull/12210)
    - 修复日志级别设置为 `ERROR` 时，慢日志不会被记录的问题 [#12373](https://github.com/pingcap/tidb/pull/12373)
    - 将缓存 100 个 Schema 变更相关的表信息调整成 1024 个，且支持通过 `tidb_max_delta_schema_count` 系统变量修改 [#12515](https://github.com/pingcap/tidb/pull/12515)
    - 将 SQL 的统计方式开始时间由“开始执行”改为“开始编译”，使得 SQL 性能统计更加准确 [#12638](https://github.com/pingcap/tidb/pull/12638)
    - 在 TiDB 日志中添加 `set session autocommit` 的记录 [#12568](https://github.com/pingcap/tidb/pull/12568)
    - 将 SQL 的开始时间记录在 `SessionVars` 中，避免计划执行时，该时间被重置 [#12676](https://github.com/pingcap/tidb/pull/12676)
    - 在 `Order By`/`Group By`/`Limit Offset` 字句中支持 `?` 占位符 [#12514](https://github.com/pingcap/tidb/pull/12514)
    - 慢日志中添加 `Prev_stmt` 字段，用于最后一条语句是 `COMMIT` 时输出前一条语句 [#12724](https://github.com/pingcap/tidb/pull/12724)
    - 当一个显式提交的事务 `COMMIT` 时出错，在日志中记录 `COMMIT` 前一条语句 [#12747](https://github.com/pingcap/tidb/pull/12747)
    - 优化在 TiDB Server 执行 SQL 时，对前一条语句的保存方式以提升性能 [#12751](https://github.com/pingcap/tidb/pull/12751)
    - 修复 `skip-grant-table=true` 时，`FLUSH PRIVILEGES` 语句导致系统 Panic 的问题 [#12816](https://github.com/pingcap/tidb/pull/12816)
    - 将 AutoID 的最小申请步长从 1000 增加为 30000，避免短时间大量写入时频繁请求 AutoID 造成性能瓶颈 [#12891](https://github.com/pingcap/tidb/pull/12891)
    - 修复 Prepared 语句在 TiDB 发生 panic 时错误日志中未打印出错 SQL 的问题 [#12954](https://github.com/pingcap/tidb/pull/12954)
    - 修复 COM_STMT_FETCH 慢日志时间记录和 MySQL 不一致问题 [#12953](https://github.com/pingcap/tidb/pull/12953)
    - 当遇到写冲突时，在报错信息中添加错误码，以方便对冲突原因进行诊断 [#12878](https://github.com/pingcap/tidb/pull/12878)
+ DDL
    - 为避免误操作，TiDB 默认不再允许删除列的 `AUTO INCREMENT` 属性，当确实需要删除时，请更改系统变量 `tidb_allow_remove_auto_inc`；相关文档请见[系统变量和语法](/system-variables.md) [#12146](https://github.com/pingcap/tidb/pull/12146)
    - 支持 Create Table 语句中建唯一索引时带多个 Unique [#12469](https://github.com/pingcap/tidb/pull/12469)
    - 修复 `CreateTable` 语句中指定外键约束时，外键表在没有指定 Database 时未能使用主表的 Database 导致报错的问题 [#12678](https://github.com/pingcap/tidb/pull/12678)
    - 修复 `ADMIN CANCEL DDL JOBS` 时报 `invalid list index` 错的问题 [#12681](https://github.com/pingcap/tidb/pull/12681)
+ Monitor
    - Backoff 监控添加类型，且补充之前没有统计到的 Backoff，比如 commit 时遇到的 Backoff [#12326](https://github.com/pingcap/tidb/pull/12326)
    - 添加统计 Add Index 操作进度的监控 [#12389](https://github.com/pingcap/tidb/pull/12389)

## PD

- 修复 pd-ctl `--help` 命令输出内容 [#1772](https://github.com/pingcap/pd/pull/1772)

## Tools

+ TiDB Binlog
    - 修复 `ALTER DATABASE` 相关 DDL 会导致 Drainer 异常退出的问题 [#770](https://github.com/pingcap/tidb-binlog/pull/770)
    - 支持对 Commit binlog 查询事务状态信息，提升同步效率 [#761](https://github.com/pingcap/tidb-binlog/pull/761)
    - 修复当 Drainer 的 `start_ts` 大于 Pump 中最大的 `commit_ts` 时候有可能引起 Pump panic 的问题 [#759](https://github.com/pingcap/tidb-binlog/pull/759)

## TiDB Ansible

- TiDB Binlog 增加 queue size 和 query histogram 监控项 [#952](https://github.com/pingcap/tidb-ansible/pull/952)
- 更新 TiDB 告警表达式 [#961](https://github.com/pingcap/tidb-ansible/pull/961)
- 新增配置文件检查功能，部署或者更新前会检查配置是否合理 [#973](https://github.com/pingcap/tidb-ansible/pull/973)
- TiDB 新增加索引速度监控项 [#987](https://github.com/pingcap/tidb-ansible/pull/987)
- 更新 TiDB Binlog 监控 Dashboard，兼容 4.6.3 版本的 Grafana [#993](https://github.com/pingcap/tidb-ansible/pull/993)
