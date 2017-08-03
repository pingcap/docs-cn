---
title: SQL 语法
category: faq-sql
---

# SQL 语法

## 出现 transaction too large 报错怎么办？ 	
由于分布式事务要做两阶段提交，并且底层还需要做 Raft 复制，如果一个事务非常大，会使得提交过程非常慢，并且会卡住下面的 Raft 复制流程。为了避免系统出现被卡住的情况，我们对事务的大小做了限制：

- 单条 KV entry 不超过 6MB

- KV entry 的总条数不超过 30w

- KV entry 的总大小不超过 100MB

在 Google 的 Cloud Spanner 上面，也有类似的限制（https://cloud.google.com/spanner/docs/limits）。

#### 解决方案：

##### 导入：
分批插入时一批最好别超过1w行，性能会好点。
##### insert select ：
我们内部有一个隐藏参数，当开启这个参数的时候，insert 会把大事务分批执行。好处是就不会因为事务太大导致超时了，坏处是语句就没有原子性了，假如中间报错，会造成“插一半”的情况，所以只有在需要的时候，使用这个功能。

	set @@session.tidb_batch_insert=1;

建议：

1.建议在 session 中使用，不影响其他语句 

2.使用以后可以关闭 `set @@session.tidb_batch_insert=0`

##### delete && update：
可以使用 limit 加循环的方式进行操作。

## 查看当时运行的 ddl job

admin show ddl 

注意： ddl 除非是遇到错误，否则目前是不能取消的