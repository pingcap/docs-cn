# tidb事务隔离级别
事务隔离级别是数据库事务处理的基础，ACID中I，即isolation，指的就是事务的隔离性。

sql 92标准定义了4种隔离级别，读未提交，读一提交，可重复读，串行化，见下表。

| isolation Level  | Dirty Read   | Nonrepeatable Read | Phantom Read          | Serialization Anomaly |
| ---------------- | ------------ | ------------------ | --------------------- | --------------------- |
| Read uncommitted | Possible     | Possible           | Possible              | Possible              |
| Read committed   | Not possible | Possible           | Possible              | Possible              |
| Repeatable read  | Not possible | Not possible       | Not possible in  tidb | Possible              |
| Serializable     | Not possible | Not possible       | Not possible          | Not possible          |

tidb实现了其中的两种，读已提交和串行化。

tidb使用[percolator事务模型](https://research.google.com/pubs/pub36726.html)，当事务启动时会获取全局读时间戳，事务提交时或获取全局提交时间戳，并以此确定事务的执行顺序，如果想了解tidb事务模型的实现可以详细阅读以下两篇文章[TiKV 的 MVCC（Multi-Version Concurrency Control）机制](https://pingcap.com/blog-cn/mvcc-in-tikv/)，[Percolator 和 TiDB 事务算法](https://pingcap.com/blog-cn/percolator-and-txn/)。

可以通过```SET SESSION TRANSACTION ISOLATION LEVEL [read committed|repeatable read]```的命令设置事务的隔离级别。


## 可重复读

可重复读是tidb的默认隔离级别，当事务隔离级别为可重复读时，只能读到该事务启动时已经提交的其他事务修改的数据，未提交的数据或在事务启动后其他事务提交的数据是不可见的。对于本事务而言，事务语句可以看到之前的语句做出的修改。

对于运行于不同节点的事务而言，不同事务启动和提交的顺序取决于从pd获取时间戳的顺序。

处于可重复读隔离级别的事务不能并发的更新同一行，当时事务提交时发现改行在该事务启动后，已经被另一个已提交的事务更新过，那么该事务会回滚并启动自动重试。见下面这个例子。

```
create table t1(id int);
insert into t1 values(0);

start transaction;			|		start transaction;
select * from t1;			|		select * from t1;
update t1 set id=id+1;		|		update t1 set id=id+1;
commit;
							|		commit;	--回滚并自动重试
```

### 与ANSI可重复读隔离级别的区别

尽管名称是可重复读隔离级别，但是tidb中可重复读隔离级别和ANSI可重复隔离级别是不同的，按照[A Critique of ANSI SQL Isolation Levels](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-95-51.pdf)论文中所说，tidb实现的其实是snapshot隔离级别，该隔离级别不会出现幻读，但是会出现写偏斜，而ANSI可重复读隔离级别不会出现写偏斜，会出现幻读

### 与mysql可重复读隔离级别的区别

mysql可重复读隔离级别在更新时并不检验当前版本是否是可见的，也就是说，即使该行在事务启动后被更新过，同样可以继续更新。这种情况在tidb会导致事务回滚并后台重试，重试最终可能会失败，导致事务最终失败，而mysql是可以更新成功的。

## 读已提交

读已提交隔离剂和可重复读隔离级别不同，它仅仅保证不能读到未提交事务的数据，需要注意的是，事务提交是一个动态的过程，因此读已提交隔离级别可能读到某个事务部分提交的数据。

不推荐在有严格一致要求的数据库中使用读已提交隔离级别。


## 事务重试

对于insert/delete/update操作，如果事务执行失败，并且系统判断该错误为可重试，会在后台自动重试事务。

你可以通过配置参数```retry-limit```控制自动重试的次数

```
[performance]
...
# The maximum number of retries when commit a transaction.
retry-limit = 10
```



