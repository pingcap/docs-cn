---
title: 行为变更说明
summary: 记录 TiCDC changefeed 行为变更，说明变更原因，以及影响范围。
---

# Update 事件拆分为 Delete 和 Insert 事件

## 含有单条 Update 变更的事物拆分

从 v6.5.3、v7.1.1 和 v7.2.0 开始，使用非 MySQL Sink 时。对于只含有一条 Update 变更的事物，如果 Update 事件的主键或者非空唯一索引的列值发生改变，TiCDC 会将该条事件拆分为 Delete 和 Insert 两条事件。详情见 GitHub issue [#9086](https://github.com/pingcap/tiflow/issues/9086)。

该变更主要为了解决如下问题：

* CSV 和 AVRO 协议，只输出新值，不输出旧值。当主键或者非空唯一索引的列值发生改变时，消费者只能收到变化后的新值，不知道旧值，也就无法处理变更之前的值（如删除旧值）。
* 使用 Index value dispatcher，将数据按照 Key 分发到不同的 Kafka partitions。下游消费者组中的多个消费者进程独立地消费Kafka Topic partition，由于消费进度不同，可能导致数据不一致的问题。

考虑如下 SQL：

```sql
create table t (a int primary key, b int);

insert into t values (1, 1);

update t set a = 2 where a = 1;
```

上述例子中，主键 a = 1 被修改为 a = 2。如果不做拆分。使用 CSV 和 AVRO 协议时，只能看到新值 a = 2，无法知道旧值 a = 1。下游消费者可能只插入了新值 2，而没有删除旧值 1。使用 Index value dispatcher 时，插入记录 (1, 1) 的事件可能被发送到 Partition 0，而变更事件 (2, 1) 可能被发送到 Partition 1，如果 Partition 1 的消费进度快于 Partition 0，则可能因为在下游数据系统中找不到相应数据而出错。因此，TiCDC 会将该条事件拆分为 Delete 和 Insert 两条事件，即删除记录 (1, 1)，写入记录 (2, 1)，前者被写入到 Partition 0，后者写入到 Partition 1，无论消费者进度如何，都能被消费成功。

## 含有多条 Update 变更的事物拆分

从 v6.5.4、v7.1.2 和 v7.4.0 开始。对于一个含有多条变更的事物，如果 Update 事件的主键或者非空唯一索引的列值发生改变，TiCDC 会将该其拆分为 Delete 和 Insert 两条事件，并且将所有事件排序，保证 Delete 事件在 Insert 事件之前。详情见 GitHub issue[#9430](https://github.com/pingcap/tiflow/pull/9437)

该变更主要为了解决如下问题：

* 使用 MySQL Sink 直接写入这两条事件到下游，下会出现主键冲突的问题，导致 changefeed 报错。

考虑如下 SQL：

```sql
create table t (a int primary key, b int);
insert into t values (1, 1);
insert into t values (2, 2);

begin;
update t set a = 1 where a = 3;
update t set a = 2 where a = 1;
update t set a = 3 where a = 2;
commit;
```

上述例子中给出的交换两行数据的主键的事物，执行了 3 条 SQL 语句，但是 TiCDC 只会收到 2 条 Update 变更事件，即将主键 1 变更为 2，将主键 2 变更为 1，这会导致 changefeed 报错。因此，TiCDC 会将这两条事件拆分为 4 条事件，即删除记录 (1, 1), (2, 2), 写入记录 (2, 1), (1, 2)。
