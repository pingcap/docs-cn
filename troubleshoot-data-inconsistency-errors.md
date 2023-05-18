---
title: 数据索引一致性错误
summary: 了解如何处理数据索引一致性检查的报错。
---

# 数据索引一致性报错

当执行事务或执行 [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) 命令时，TiDB 会对数据索引的一致性进行检查。如果检查发现 record key-value 和 index key-value 不一致，即存储行数据的键值对和存储其对应索引的键值对之间不一致（例如多索引或缺索引），TiDB 会报数据索引一致性错误，并在日志文件中打印相关错误日志。

本文对数据索引一致性的报错信息进行了说明，并提供了一些绕过检查的方法。遇到报错时，你可以前往 [AskTUG 论坛](https://asktug.com/)，与社区用户交流；如果是订阅用户，请联系 [PingCAP 服务与支持](https://cn.pingcap.com/support/)。

## 错误样例解读

当数据索引不一致时，你可以通过查看 TiDB 的报错信息了解行数据和索引数据在哪一项不一致，或者查看相关错误日志进行判断。

### 执行事务中的报错

本节列出了 TiDB 在执行事务过程中可能出现的数据索引不一致性的报错，并通过举例对这些信息的含义进行了解释。

#### Error 8133

`ERROR 8133 (HY000): data inconsistency in table: t, index: k2, index-count:1 != record-count:0`

上述错误表明，对于表 `t` 中的 `k2` 索引，表中索引数量为 1，行记录的数量为 0，数量不一致。

#### Error 8138

`ERROR 8138 (HY000): writing inconsistent data in table: t, expected-values:{KindString green} != record-values:{KindString GREEN}`

上述错误表明，事务试图写入的行值有误。即将写入的数据中，编码后的行数据与编码前的原始数据不符。

#### Error 8139

`ERROR 8139 (HY000): writing inconsistent data in table: t, index: i1, index-handle:4 != record-handle:3, index: tables.mutation{key:kv.Key{0x74, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x49, 0x5f, 0x69, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x1, 0x1, 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x0, 0x0, 0x0, 0xfc, 0x1, 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x0, 0x0, 0x0, 0xfc, 0x3, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x4}, flags:0x0, value:[]uint8{0x30}, indexID:1}, record: tables.mutation{key:kv.Key{0x74, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x49, 0x5f, 0x72, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x3}, flags:0xd, value:[]uint8{0x80, 0x0, 0x2, 0x0, 0x0, 0x0, 0x1, 0x2, 0x5, 0x0, 0xa, 0x0, 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x68, 0x65, 0x6c, 0x6c, 0x6f}, indexID:0}`

上述错误表明，即将写入的数据中，handle（即行数据的 key）值不一致。对于表 `t` 中的 `i1` 索引，该事务即将写入的某行在索引键值对中的 handle 值是 4，在行记录键值对中的 handle 值是 3。这行数据将不会被写入。

#### Error 8140

`ERROR 8140 (HY000): writing inconsistent data in table: t, index: i2, col: c1, indexed-value:{KindString hellp} != record-value:{KindString hello}`

上述错误表明，事务试图写入的行和索引的值不一致。对于表 `t` 中的 `i2` 索引，该事务即将写入的某行在索引键值对中的数据是 `hellp`，在行记录键值对中的数据是`hello`。这行数据将不会被写入。

#### Error 8141

`ERROR 8141 (HY000): assertion failed: key: 7480000000000000405f72013300000000000000f8, assertion: NotExist, start_ts: 430590532931813377, existing start ts: 430590532931551233, existing commit ts: 430590532931551234`

上述错误表明，事务提交时断言失败。根据数据索引一致的假设，TiDB 断言 key `7480000000000000405f72013300000000000000f8` 不存在，提交事务时发现该 key 存在，是由 start ts 为 `430590532931551233` 的事务写入的。TiDB 会将该 key 的 MVCC (Multi-Version Concurrency Control) 历史输出到日志。

### Admin check 中的报错

本节列出了执行 [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) 系列语句时 TiDB 可能出现的数据索引不一致报错，并通过举例对这些信息的含义进行了解释。

#### Error 8003

`ERROR 8003 (HY000): table count 3 != index(idx) count 2`

上述错误表明，在 [`ADMIN CHECK`](/sql-statements/sql-statement-admin-check-table-index.md) 语句所执行的表上有 3 个行键值对，但只有 2 个索引键值对。

#### Error 8134

`ERROR 8134 (HY000): data inconsistency in table: t, index: c2, col: c2, handle: "2", index-values:"KindInt64 13" != record-values:"KindInt64 12", compare err:<nil>`

上述错误表明，对于表 `t` 中的 `c2` 索引，handle 为 2 的行对应的索引键值对中列 c2 的值是 13，行记录键值对中列 c2 的值是 12。

#### Error 8223

`ERROR 8223 (HY000): data inconsistency in table: t2, index: i1, handle: {hello, hello}, index-values:"" != record-values:"handle: {hello, hello}, values: [KindString hello KindString hello]"`

上述错误表明，`index-values` 为空，`record-values` 不为空，说明不存在对应的索引，但存在对应的行。

## 报错处理

发生报错时，不要自行处理，请从 PingCAP 官方或 TiDB 社区[获取支持](/support.md)。如果业务急需跳过此类报错，可以使用以下方法绕过检查。

### 改写 SQL

如果只有某一条 SQL 语句报错，可以尝试将其改写为其它等价的 SQL 形式，以使用不同的执行算子来尝试绕过。

### 关闭错误检查

对于事务执行中出现的一些报错，可以使用以下方法绕过检查：

- 对于错误代码为 8138、8139 和 8140 的错误，可以通过设置 `set @@tidb_enable_mutation_checker=0` 跳过检查。
- 对于错误代码为 8141 的错误，可以通过设置 `set @@tidb_txn_assertion_level=OFF` 跳过检查。

> **注意：**
>
> 关闭 `tidb_enable_mutation_checker` 和 `tidb_txn_assertion_level` 开关会关闭对所有 SQL 语句的对应检查。

对于其它错误代码，包括执行 [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) 系列语句或执行事务中的报错，由于数据中已经存在不一致，无法跳过对应的检查。
