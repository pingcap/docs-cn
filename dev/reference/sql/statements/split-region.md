# Split region 使用文档

## 背景

在 TiDB 中新建一个表后，默认会单独切分出 1 个 region 来存储这个表的数据，这个默认行为由配置文件中的 `split-table` 控制。当这个 region 中的数据超过默认 region 大小限制后，这个 region 会开始分裂成 2 个 region。

上述情况中，如果在新建的表上发生大批量写入，则会造成热点，因为开始只有一个 region，所有的写请求都发生在该 region 所在的那台 TiKV 上。

为解决上述场景中的热点问题，TiDB 引入了预切分 region 的功能，即可以根据用户指定的参数，预先为某个表切分出多个 region。

## Split region 的使用

Split region 有 2 种不同的语法，具体如下：

```sql
SPLIT TABLE table_name [INDEX index_name] BETWEEN (lower_value) AND (upper_value) REGIONS region_num

SPLIT TABLE table_name [INDEX index_name] BY (value_list) [, (value_list)] ...
```

`BETWEEN lower_value AND upper_value REGIONS region_num` 语法是通过指定上、下边界和 region 数量，然后在上、下边界之间均匀切分出 `region_num` 个 region。

`BY value_list…` 语法将手动指定一系列的点，然后根据这些指定的点切分 region，适用于数据不均匀分布的场景。

### Split Table region

表中行数据的 key 由 `table_id` 和 `row_id` 编码组成，格式如下：

```go
t[table_id]_r[row_id]
eg:
t22_r11 # table_id 是22， row_id 是11
```

同一表中行数据的 `table_id` 是一样的，但 `row_id` 肯定是不一样的，所以可以根据 `row_id` 来切分 region。

#### 均匀切分

由于 `row_id` 是整数，所以根据用户指定的 `lower_value`、`upper_value` 以及 `region_num`，可以很容易地计算出需要切分的 key。先计算出 step（`step = (upper_value - lower)/num`），然后在 `lower` 和 `upper` 之间每隔 step 区间就切一次，最终切出 `num` 个 region。示例如下：

对于表 t，如果想要从 `minInt64`~`maxInt64` 之间均匀切割出 16 个 region ，可以用以下语句：

```sql
SPLIT TABLE t BETWEEN (-9223372036854775808) AND (9223372036854775807) REGIONS 16;
```

以上 SQL 语句会把表 t 从 minInt64 到 maxInt64 之间均匀切割出 16 个 region。如果已知主键的范围没有这么大，比如只会在 0~1000000000 之间，那可以用 0 和 1000000000 分别代替上面的 minInt64 和 maxInt64 来切分 region。

```sql
SPLIT TABLE t BETWEEN (0) AND (1000000000) REGIONS 16;
```

#### 不均匀切分

如果已知数据不是均匀分布的，比如想要 -inf~10000 切一个 region，10000~90000 切一个 region，90000~+inf 切一个 region ，可以通过手动指定点来切分 region，示例如下：

```sql
SPLIT TABLE t BY (10000), (90000);
```

### Split Index region

表中索引数据的 key 由 `table_id`、`index_id` 以及索引列的值编码组成，格式如下：

```
t[table_id]_i[index_id][index_value]
eg
t22_i5abc # table_id 是22, index_id 是5， index_value 是 abc 
```

同一表中的同一索引数据的 `table_id` 和 `index_id` 是一样的，所以切分索引 region 要根据 `index_value` 来切分 region。

#### 均匀切分

索引均匀切分与行数据均匀切分的原理一样，只是计算 step 的值复杂一些，因为 `index_value` 可能不是整数。 `upper` 和 `lower` 的值会先编码成 byte 数组，去掉 `lower` 和 `upper` byte 数组的最长公共前缀后，从 `lower`, `upper` 各取前 8 字节转成 uint64，再去计算 `step = (upper - lower)/num`。计算出 step 后再将 step 编码成 byte
数组，添加到之前 `upper`和 `lower`的最长公共前缀后面组成一个 key 后去做切分。示例如下：

如果索引 idx 的列也是整数类型，可以用如下 SQL 语句切分索引数据：

```sql
SPLIT TABLE t INDEX idx BETWEEN (-9223372036854775808) AND (9223372036854775807) REGIONS 16;
```

该语句会把表 t 中 idx 索引数据 region 从 `minInt64` 到 `maxInt64` 之间均匀切割出 16 个 region。

如果索引 idx1 的列是 varchar 类型，希望根据前缀字母来切分索引数据：

```sql
SPLIT TABLE t INDEX idx1 BETWEEN ("a") AND ("z") REGIONS 26;
```

该 SQL 语句会把表 t 中 idx1 索引数据的 region 从 a~z 切成 26 个 region，region1 的范围是 [minIndexValue, b)，region 2 的范围是 [b, c)...... region 26 的范围是 [y, minIndexValue]。对于 idx 索引以 a 为前缀的数据都会写到 region1，以 b 为前缀的索引数据都会写到 region 2，以此类推。

如果索引 idx2 的列是 timestamp/datatime 等时间类型，希望根据时间区间来切分索引数据：

```sql
SPLIT TABLE t INDEX idx2 BETWEEN ("2010-01-01 00:00:00") AND ("2020-01-01 00:00:00") REGIONS 10;

```

该 SQL 语句会把表 t 中 idx2 的索引数据 region 从 `2010-01-01 00:00:00` 到  `2020-01-01 00:00:00` 切成 10 个 region。region1 的范围是从 `[minIndexValue,  2011-01-01 00:00:00)`，region2 的范围是 `[2011-01-01 00:00:00, 2012-01-01 00:00:00)`......

其他索引列类型的切分方法也是类似的。

对于联合索引的数据 region 切分，唯一不同的是指定的值可以指定多个 column 的值。

比如对于索引 `idx3 (a, b)`，他包含2列，a 是 timestamp, b 是 int。 如果只想根据 a 列做时间范围的切分，可以用切分单列时间索引的SQL 语句来切分，`lower_value` 和 `upper_velue` 中不指定 b 列的值即可。

```sql
SPLIT TABLE t INDEX idx3 BETWEEN ("2010-01-01 00:00:00") AND ("2020-01-01 00:00:00") REGIONS 10;

```

如果想在时间相同的情况下，根据 b 列再做一次切分，在切分时指定 b 列的值即可。

```sql
SPLIT TABLE t INDEX idx3 BETWEEN ("2010-01-01 00:00:00", "a") AND ("2010-01-01 00:00:00", "z") REGIONS 10;
```

上面 SQL 在a 列时间前缀相同的情况下，根据 b 列的值从 a ~ z 切了 10 个 region。如果指定的 a 列的值不相同，那么 b 列的值可能不会用到。

#### 不均匀切分

索引数据也可以根据用用户指定的索引值来做切分。
假如 idx4 (a,b), a 列是 varchar 类型， b 列是 timestamp 类型。

```sql
SPLIT TABLE t1 INDEX idx4 ("a", "2000-01-01 00:00:01"),  ("b", "2019-04-17 14:26:19"),  ("c", "");  

```

上面 SQL 指定了3个值，会切分出4个region， 每个region 的范围如下。

```
region1  [ minIndexValue               , ("a", "2000-01-01 00:00:01"))
region2  [("a", "2000-01-01 00:00:01") , ("b", "2019-04-17 14:26:19"))
region3  [("b", "2019-04-17 14:26:19") , ("c", "")                   )
region4  [("c", "")                    , maxIndexValue               )
```

## pre_split_regions

使用带有 `shard_row_id_bits` 的表时，如果希望建表时就做均匀切分 region，可以考虑配合 `pre_split_regions` 一起使用，用来在建表成功后就开始预均匀切分 `2^(pre_split_regions-1)` 个 regions。

> **注意：**
>
> `pre_split_regions` 必须小于等于 `shard_row_id_bits`。

### 示例

```sql
create table t (a int, b int,index idx1(a)) shard_row_id_bits = 4 pre_split_regions=3;
```

该语句在建表后，会对这个表 t 预切分出 4 + 1 个 region。4 (4=2^(3-1)) 个 regions 是用来存 table 的行数据的，1 个 region 是用来存 idx1 索引的数据。

4 个 table region 的范围区间如下：

```
region1:   [ -inf      ,  1<<61 )  
region2:   [ 1<<61     ,  2<<61 )
region3:   [ 2<<61     ,  3<<61 )
region4:   [ 3<<61     ,  +inf  )
```

关于为什么是切割 2^(pre_split_regions-1) 个 regions，因为使用 shard_row_id_bits 时，只会分配正数给 `_tidb_rowid`，所以就没有必要给负数的那段区间做 split region 了。
