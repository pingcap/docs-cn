---
title: DM safe mode 介绍
summary: 介绍 DM safe mode 作用和原理
---

# DM safe mode 介绍

安全模式（safe mode）是 DM 在进行增量同步时候的一种运行模式，在安全模式中，DM 增量同步组件在同步 binlog event 时，将把所有 INSERT 和 UPDATE 操作强制进行改写后再在下游执行。

安全模式的目的是在增量同步过程中，同一条 binlog event 能够在下游被重复同步且保证幂等性，从而确保增量同步能够“安全”进行。 

最早引入安全模式是为了解决从 DM checkpoint 恢复后，某些 binlog 事件可能被重复执行而产生的问题。在进行增量同步过程中， DML 执行 和写 checkpoint 操作并不是同步的，并且写 checkpoint 操作和写下游数据也并不能保证原子性，当 DM 因为某些原因异常退出时，checkpoint 可能只记录到退出时刻之前的一个恢复点，因此当同步任务重启，从之前保存的 checkpoint 重新开始增量数据同步时，有一些 checkpoint 之后的数据可能已经在异常退出前被处理过了，这里会被重复处理。如果重复执行插入操作，会导致主键 / 唯一索引冲突导致同步中断；如果重复执行更新操作，会导致不能根据筛选条件找到之前对应的更新记录。安全模式通过改写 SQL 的方法能很好解决上述问题。

## safe mode 原理

安全模式原理是通过 SQL 语句改写来完成。具体来说，在安全模式下，所有的 INSERT 语句会被改写成 REPLACE 语句，而 UPDATE 语句会被分析，得到该语句涉及的行的主键 / 唯一索引的值，然后改写成 DELETE + REPLACE 语句 ：先根据主键 / 唯一索引的定位删除对应的行，然后使用REPLACE语句插入一条最新值的行记录。

REPLACE 操作是 MySQL 特有的数据插入语法，它在插入数据时，如果发现新插入的数据和现有数据存在主键或唯一约束冲突，它会把所有冲突的记录先删除，然后再执行插入记录操作。相当于“强制插入”的操作。具体请参考[MySQL 官方文档的 REPLACE 语句相关介绍](https://dev.mysql.com/doc/refman/8.0/en/replace.html) 。

比如，如果假设一张表`dummydb.dummytbl`，主键是`id`，并且下面的 SQL 被重复执行：

```
INSERT INTO dummydb.dummytbl (id, int_value, str_value) VALUES (123, 999, 'abc');
UPDATE dummydb.dummytbl SET int_value = 888999 WHERE int_value = 999；   # 假设没有其他 int_value = 999的数据
UPDATE dummydb.dummytbl SET id = 999 WHERE id = 888；    # 更新主键操作
```

经过安全模式的 SQL 改写，再次在下游执行时会变成执行下面的 SQL 语句：

```
REPLACE INTO dummydb.dummytbl (id, int_value, str_value) VALUES (123, 999, 'abc');
DELETE FROM dummydb.dummytbl WHERE id = 123;
REPLACE INTO dummydb.dummytbl (id, int_value, str_value) VALUES (123, 888999, 'abc')；
DELETE FROM dummydb.dummytbl WHERE id = 888;
REPLACE INTO dummydb.dummytbl (id, int_value, str_value) VALUES (999, 888888, 'abc888');    # 更新主键的改写解释了为什么 UPDATE 要 替换为 DELETE + REPLACE, 而不是 DELETE + INSERT ：如果这里使用INSERT，那么id = 999 的记录在已经存在的情况下重复插入时会报错主键冲突，而REPLACE则会替换之前已经插入的记录
```

通过这样的语句改写，在进行重复的插入或更新操作时，都会把执行该操作后的行数据覆盖之前已经存在的行数据。这样保证了插入和更新操作的可重复执行。

## 如何开启 safe mode

### 自动开启

当 DM 从 checkpoint 恢复增量同步任务(例如 worker 重启，网络中断重连等)时，都会自动开启一段时间的安全模式，原因会在下面详细分析。在 checkpoint 中，有一个叫做 safemode_exit_point 的信息和安全模式的开启逻辑息息相关。当上一个增量同步任务异常暂停时，DM 会先尝试将内存中所有的 DML 全部同步到下游，然后 DM 记录当前内存中从上游拉取到的最新的 binlog 位置点，记作 safemode_exit_point，把这个额外信息保存在异常暂停之前最后一个 checkpoint 当中。

从 checkpoint 进行恢复增量同步任务时，DM 会根据下面的判断逻辑来开启安全模式：

- 如果 checkpoint 信息里面额外记录了 safemode_exit_point ，说明之前是异常暂停。如果恢复时发现待恢复的 checkpoint 的 binlog 位置点 < safemode_exit_point，那么说明从这个 checkpoint 到 safemode_exit_point 之间的 binlog 可能已经在下游被执行了，在这里要被重复执行。所以这段 binlog 范围内需要开启安全模式。直到当前的binlog 位置点超过了 safemode_exit_point，DM 才会关闭安全模式（未手动开启 safe-moded 情况下）。

- 如果 checkpoint 信息里面没有 safemode_exit_point 信息，一种可能是说明这是一个全新的任务或者之前该任务是正常暂停。但是，还有一种可能是之前异常暂停时，记录 safemode_exit_point 的时候失败了，甚至可能是之前 DM 进程异常退出了。这种情况下，DM 并不知道哪些 checkpoint 之后的 binlog 已经被执行过了。所以，这种情况下，为了保险起见，只要没有在 checkpoint 找到 safemode_exit_point 信息，DM 就会在前2个 checkpoint 间隔中都开启安全模式，确保这段时间的重复执行 binlog 都没有问题。默认的 checkpoint 间隔是30秒，也就是说，一个正常的增量同步任务开始时，前 2 * 30 = 60秒会自动强制开启安全模式。通过设置任务配置中 syncer的配置 “checkpoint-flush-interval” 来调整 checkpoint 的间隔，从而影响增量同步任务开始时安全模式的持续时间（一般情况下不建议调整，如有需要应优先使用后文所述的`手动开启`）。


### 手动开启

除了上述场景，通过增量任务配置中 syncer 的配置`safe-mode`可以控制是否需要全程开启安全模式。它的配置值是一个布尔类型值，默认是 “false”。如果设置为 “true”，那么表示在增量同步的全过程中都会开启安全模式。比如，下面是一个开启了安全模式的任务配置示例：

```
syncers:                             # sync 处理单元的运行配置参数
  global:                            # 配置名称
    # 其他配置省略
    safe-mode: true                  # 增量同步任务全程开启"安全模式"
    # 其他配置省略
# ----------- 实例配置 -----------
mysql-instances:
  -
    source-id: "mysql-replica-01"
    # 其他配置省略
    syncer-config-name: "global"            # syncers 配置的名称
```

## 注意事项

使用安全模式主要解决的是由于之前同步任务的异常退出而导致的恢复后 binlog 重复执行的问题。有一些用户为了安全起见，可能会通过配置全程开启安全模式。但是，如果全程开启安全模式，有一些问题需要注意：

- 安全模式对于增量同步有额外开销。这是因为频繁的 DELETE + REPLACE 操作会带来主键 / 唯一索引的频繁变化，带来了比单纯 UPDATE 语句更大的性能开销。
- 由于安全模式会强制替换主键相同的记录，带来的问题就是之前的记录数据丢失。如果由于上游分片表合并导入下游的配置不当，可能导致在上游合并导入到下游数据库的时候，出现大量的主键 / 唯一索引冲突。如果此时全程开启安全模式，会导致下游大量的数据丢失，并且可能无法从任务中看到有任何的异常，导致数据的大量不一致。
- 安全模式依赖于通过主键 / 唯一索引来判断冲突。如果下游 DB 对应的表没有主键 / 唯一索引，会导致 REPLACE 语句起不到替换插入的目的，这样即使开启了安全模式，对于INSERT语句的改写成REPLACE并执行后，依旧会向下游插入重复记录。

因此，如果上游存在主键重复的数据，业务对于重复数据的丢失和性能损失可以接受，可以开启 safe mode 忽略数据重复错误。