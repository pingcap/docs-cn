---
title: 数据索引一致性错误
summary: 在主动或被动进行数据索引一致性检查时，报出错误。
---

# 数据索引一致性报错

数据索引一致性错误指 record key-value 和 index key-value 不一致，例如多索引、缺索引等。发生此错误时，应当联系 PingCAP 技术支持。

## 错误样例解读

数据索引不一致的错误，在报错信息中会给出行数据和索引数据在哪一项不一致。本节对可能出现的一些报错信息的含义举例进行解释。

数据索引不一致发生时，日志中也会打印相关错误日志，可联系日志内容进行判断。

### 事务中出现

#### Error 8141

`ERROR 8141 (HY000): assertion failed: key: 7480000000000000405f72013300000000000000f8, assertion: NotExist, start_ts: 430590532931813377, existing start ts: 430590532931551233, existing commit ts: 430590532931551234`

上述错误表明，事务提交时断言失败。根据数据索引一致的假设，TiDB 断言 key `7480000000000000405f72013300000000000000f8` 应该不存在，提交事务时发现该 key 存在，是由 start ts 为 `430590532931551233` 的事务写入的。TiDB 会将该 key 的 MVCC 历史输出到日志。

#### Error 8140

`ERROR 8140 (HY000): writing inconsistent data in table: t, index: i2, col: c1, indexed-value:{KindString hellp} != record-value:{KindString hello}`

上述错误表明，即将写入的数据中存在不一致。表 `t` 中的 `i2` 索引，某行修改对应的索引键值对中的数据是 `hellp`，行记录键值对中的数据是`hello`。这行数据将不会被写入。

#### Error 8139

`ERROR 8139 (HY000): writing inconsistent data in table: t, index: i1, index-handle:4 != record-handle:3, index: tables.mutation{key:kv.Key{0x74, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x49, 0x5f, 0x69, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x1, 0x1, 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x0, 0x0, 0x0, 0xfc, 0x1, 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x0, 0x0, 0x0, 0xfc, 0x3, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x4}, flags:0x0, value:[]uint8{0x30}, indexID:1}, record: tables.mutation{key:kv.Key{0x74, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x49, 0x5f, 0x72, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x3}, flags:0xd, value:[]uint8{0x80, 0x0, 0x2, 0x0, 0x0, 0x0, 0x1, 0x2, 0x5, 0x0, 0xa, 0x0, 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x68, 0x65, 0x6c, 0x6c, 0x6f}, indexID:0}`

上述错误表明，即将写入的数据中，handle 值不一致。表 `t` 中的 `i1` 索引，某行修改对应的索引键值对中的 handle 值是 4，行记录键值对中的 handle 值是 3。这行数据将不会被写入。

#### Error 8133

`ERROR 8133 (HY000): data inconsistency in table: admin_test, index: k2, index-count:1 != record-count:0`

上述错误表明，表 `t` 中的 `k2` 索引，表中索引数量为 1，行记录的数量为 0，数量不一致。

### Admin check 中出现

主动执行 `admin check` 系列语句，发现数据索引不一致时可能有类似如下报错。

#### Error 8134

`ERROR 8134 (HY000): data inconsistency in table: t, index: c2, col: c2, handle: "2", index-values:"KindInt64 13" != record-values:"KindInt64 12", compare err:<nil>`

上述错误表明，表 `t` 中的 `c2` 索引，某行对应的索引键值对中的 handle 值是 4，行记录键值对中的 handle 值是 3，存在不一致。

#### Error 8223

`ERROR 8223 (HY000): data inconsistency in table: t2, index: i1, handle: {hello, hello}, index-values:"" != record-values:"handle: {hello, hello}, values: [KindString hello KindString hello]"`

上述错误表明，`index-value` 为空，`record-values` 不为空，说明不存在对应的索引，但存在对应的行，产生了不一致。

## 误报和绕过方法

对于错误代码为 8138，8139 和 8140 的错误，如果通过错误信息判断为误报，可以通过设置 `tidb_mutation_checker` 为 `0` 来跳过检查。

对于错误代码为 8141 的错误，如果通过错误信息判断为误报，可以通过设置 `tidb_txn_assertion_level` 为 `OFF` 来跳过检查。

不论是否误报，一致性检查报错时，请立即联系 PingCAP 技术支持。