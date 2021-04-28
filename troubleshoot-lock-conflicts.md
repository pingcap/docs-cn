---
title: TiDB 锁冲突问题处理
summary: 了解 TiDB 锁冲突问题以及处理方式。
aliases: ['/docs-cn/dev/troubleshoot-lock-conflicts/']
---

# TiDB 锁冲突问题处理

TiDB 支持完整的分布式事务，自 v3.0 版本起，提供乐观事务与悲观事务两种事务模型。本文介绍在使用乐观事务或者悲观事务的过程中常见的锁冲突问题以及解决思路。

## 乐观锁

TiDB 中事务使用两阶段提交，分为 Prewrite 和 Commit 两个阶段，示意图如下。

![TiDB 中乐观事务的两阶段提交](/media/troubleshooting-lock-pic-01.png)

相关细节本节不再赘述，详情可阅读 [Percolator 和 TiDB 事务算法](https://pingcap.com/blog-cn/percolator-and-txn/)。

### Prewrite 阶段

在两阶段提交的 Prewrite 阶段，TiDB 会对目标 key 分别上 primary lock 和 secondary lock。在冲突严重的场景中，会出现写冲突 (write conflict)、keyislocked 等报错。具体而言，这个阶段可能会遇到的锁相关的报错信息如下。

#### 读写冲突

在 TiDB 中，读取数据时，会获取一个包含当前物理时间且全局唯一递增的时间戳作为当前事务的 start_ts。事务在读取时，需要读到目标 key 的 commit_ts 小于这个事务的 start_ts 的最新的数据版本。当读取时发现目标 key 上存在 lock 时，因为无法知道上锁的那个事务是在 Commit 阶段还是 Prewrite 阶段，所以就会出现读写冲突的情况，如下图：

![读写冲突](/media/troubleshooting-lock-pic-04.png)

分析：

Txn0 完成了 Prewrite，在 Commit 的过程中 Txn1 对该 key 发起了读请求，Txn1 需要读取 start_ts > commit_ts 最近的 key 的版本。此时，Txn1 的 `start_ts > Txn0` 的 lock_ts，需要读取的 key 上的锁信息仍未清理，故无法判断 Txn0 是否提交成功，因此 Txn1 与 Txn0 出现读写冲突。

你可以通过如下两种途径来检测当前环境中是否存在读写冲突：

1. TiDB 监控及日志

    * 通过 TiDB Grafana 监控分析：

        观察 KV Errors 下 Lock Resolve OPS 面板中的 not_expired/resolve 监控项以及 KV Backoff OPS 面板中的 txnLockFast 监控项，如果有较为明显的上升趋势，那么可能是当前的环境中出现了大量的读写冲突。其中，not_expired 是指对应的锁还没有超时，resolve 是指尝试清锁的操作，txnLockFast 代表出现了读写冲突。

        ![KV-backoff-txnLockFast-optimistic](/media/troubleshooting-lock-pic-09.png)
        ![KV-Errors-resolve-optimistic](/media/troubleshooting-lock-pic-08.png)

    * 通过 TiDB 日志分析：

        在 TiDB 的日志中可以看到下列信息：

        ```log
        [INFO] [coprocessor.go:743] ["[TIME_COP_PROCESS] resp_time:406.038899ms txnStartTS:416643508703592451 region_id:8297 store_addr:10.8.1.208:20160 backoff_ms:255 backoff_types:[txnLockFast,txnLockFast] kv_process_ms:333 scan_total_write:0 scan_processed_write:0 scan_total_data:0 scan_processed_data:0 scan_total_lock:0 scan_processed_lock:0"]
        ```

        * txnStartTS：发起读请求的事务的 start_ts，如上面示例中的 416643508703592451
        * backoff_types：读写发生了冲突，并且读请求进行了 backoff 重试，重试的类型为 txnLockFast
        * backoff_ms：读请求 backoff 重试的耗时，单位为 ms ，如上面示例中的 255
        * region_id：读请求访问的目标 region 的 id

2. 通过 TiKV 日志分析：

    在 TiKV 的日志可以看到下列信息：

    ```log
    [ERROR] [endpoint.rs:454] [error-response] [err=""locked primary_lock:7480000000000004D35F6980000000000000010380000000004C788E0380000000004C0748 lock_version: 411402933858205712 key: 7480000000000004D35F7280000000004C0748 lock_ttl: 3008 txn_size: 1""]
    ```

    这段报错信息表示出现了读写冲突，当读数据时发现 key 有锁阻碍读，这个锁包括未提交的乐观锁和未提交的 prewrite 后的悲观锁。

    * primary_lock：锁对应事务的 primary lock。
    * lock_version：锁对应事务的 start_ts。
    * key：表示被锁的 key。
    * lock_ttl: 锁的 TTL。
    * txn_size：锁所在事务在其 Region 的 key 数量，指导清锁方式。

处理建议：

* 在遇到读写冲突时会有 backoff 自动重试机制，如上述示例中 Txn1 会进行 backoff 重试，单次初始 100 ms，单次最大 3000 ms，总共最大 20000 ms

* 可以使用 TiDB Control 的子命令 [decoder](/tidb-control.md#decoder-命令) 来查看指定 key 对应的行的 table id 以及 rowid：

    ```sh
    ./tidb-ctl decoder -f table_row -k "t\x00\x00\x00\x00\x00\x00\x00\x1c_r\x00\x00\x00\x00\x00\x00\x00\xfa"
    
    table_id: -9223372036854775780
    row_id: -9223372036854775558
    ```

#### KeyIsLocked 错误

事务在 Prewrite 阶段的第一步就会检查是否有写写冲突，第二步会检查目标 key 是否已经被另一个事务上锁。当检测到该 key 被 lock 后，会在 TiKV 端报出 KeyIsLocked。目前该报错信息没有打印到 TiDB 以及 TiKV 的日志中。与读写冲突一样，在出现 KeyIsLocked 时，后台会自动进行 backoff 重试。

你可以通过 TiDB Grafana 监控检测 KeyIsLocked 错误：

观察 KV Errors 下 Lock Resolve OPS 面板中的 resolve 监控项以及 KV Backoff OPS 面板中的 txnLock 监控项，会有比较明显的上升趋势，其中 resolve 是指尝试清锁的操作，txnLock 代表出现了写冲突。

![KV-backoff-txnLockFast-optimistic-01](/media/troubleshooting-lock-pic-07.png)
![KV-Errors-resolve-optimistic-01](/media/troubleshooting-lock-pic-08.png)

处理建议：

* 监控中出现少量 txnLock，无需过多关注。后台会自动进行 backoff 重试，单次初始 200 ms，单次最大 3000 ms。
* 如果出现大量的 txnLock，需要从业务的角度评估下冲突的原因。
* 使用悲观锁模式。

### Commit 阶段

当 Prewrite 全部完成时，客户端便会取得 commit_ts，然后继续两阶段提交的第二阶段。这里需要注意的是，由于 primary key 是否提交成功标志着整个事务是否提交成功，因而客户端需要在单独 commit primary key 之后再继续 commit 其余的 key。

#### 锁被清除 (LockNotFound) 错误

TxnLockNotFound 错误是由于事务提交的慢了，超过了 TTL 的时间。当要提交时，发现被其他事务给 Rollback 掉了。在开启 TiDB [自动重试事务](/system-variables.md#tidb_retry_limit)的情况下，会自动在后台进行事务重试（注意显示和隐式事务的差别）。

你可以通过如下两种途径来查看 LockNotFound 报错信息：

1. 查看 TiDB 日志

    如果出现了 TxnLockNotFound 的报错，会在 TiDB 的日志中看到下面的信息：

    ```log
    [WARN] [session.go:446] ["commit failed"] [conn=149370] ["finished txn"="Txn{state=invalid}"] [error="[kv:6]Error: KV error safe to retry tikv restarts txn: Txn(Mvcc(TxnLockNotFound{ start_ts: 412720515987275779, commit_ts: 412720519984971777, key: [116, 128, 0, 0, 0, 0, 1, 111, 16, 95, 114, 128, 0, 0, 0, 0, 0, 0, 2] })) [try again later]"]
    ```

    * start_ts：出现 TxnLockNotFound 报错的事务的 start_ts，如上例中的 412720515987275779
    * commit_ts：出现 TxnLockNotFound 报错的事务的 commit_ts，如上例中的 412720519984971777

2. 查看 TiKV 日志

    如果出现了 TxnLockNotFound 的报错，在 TiKV 的日志中同样可以看到相应的报错信息：

    ```log
    Error: KV error safe to retry restarts txn: Txn(Mvcc(TxnLockNotFound)) [ERROR [Kv.rs:708] ["KvService::batch_raft send response fail"] [err=RemoteStoped]
    ```

处理建议：

* 通过检查 start_ts 和 commit_ts 之间的提交间隔，可以确认是否超过了默认的 TTL 的时间。

    查看提交间隔：

    ```shell
    ./pd-ctl tso [start_ts]
    ./pd-ctl tso [commit_ts]
    ```

* 建议检查下是否是因为写入性能的缓慢导致事务提交的效率差，进而出现了锁被清除的情况。

* 在关闭 TiDB 事务重试的情况下，需要在应用端捕获异常，并进行重试。

## 悲观锁

在 v3.0.8 之前，TiDB 默认使用的乐观事务模式会导致事务提交时因为冲突而失败。为了保证事务的成功率，需要修改应用程序，加上重试的逻辑。悲观事务模式可以避免这个问题，应用程序无需添加重试逻辑，就可以正常执行。

TiDB 悲观锁复用了乐观锁的两阶段提交逻辑，重点在 DML 执行时做了改造。

![TiDB 悲观事务的提交逻辑](/media/troubleshooting-lock-pic-05.png)

在两阶段提交之前增加了 Acquire Pessimistic Lock 阶段，简要步骤如下。

1. （同乐观锁）TiDB 收到来自客户端的 begin 请求，获取当前版本号作为本事务的 StartTS。
2. TiDB 收到来自客户端的更新数据的请求：TiDB 向 TiKV 发起加悲观锁请求，该锁持久化到 TiKV。
3. （同乐观锁）客户端发起 commit，TiDB 开始执行与乐观锁一样的两阶段提交。

![TiDB 中的悲观事务](/media/troubleshooting-lock-pic-06.png)

相关细节本节不再赘述，详情可阅读 [TiDB 悲观锁实现原理](https://asktug.com/t/topic/33550)。

### Prewrite 阶段

在悲观锁模式下，在事务的提交阶段沿用的仍然是乐观锁模式，所以在 Prewrite 阶段乐观锁遇到的锁相关的一些报错，在悲观锁模式同样会遇到。

#### 读写冲突

报错信息以及处理建议同乐观锁模式。

### Commit 阶段

在乐观模型下，会出现 TxnLockNotFound 错误，而在悲观锁模型下，不会出现这个问题。同样的，悲观锁也有一个 TTL 的时间。txn heartbeat 会自动的更新事务的 TTL，以确保第二个事务不会将第一个事务的锁清掉。

### 其他锁相关错误

#### pessimistic lock retry limit reached

在冲突非常严重的场景下，或者当发生 write conflict 时，乐观事务会直接终止，而悲观事务会尝试用最新数据重试该语句直到没有 write conflict。因为 TiDB 的加锁操作是一个写入操作，且操作过程是先读后写，需要 2 次 RPC。如果在这中间发生了 write conflict，那么会重试。每次重试都会打印日志，不用特别关注。重试次数由 [pessimistic-txn.max-retry-count](/tidb-configuration-file.md#max-retry-count) 定义。

可通过查看 TiDB 日志查看报错信息：

悲观事务模式下，如果发生 write conflict，并且重试的次数达到了上限，那么在 TiDB 的日志中会出现含有下述关键字的报错信息。如下：

```log
err="pessimistic lock retry limit reached"
```

处理建议：

* 如果上述报错出现的比较频繁，建议从业务的角度进行调整。

#### Lock wait timeout exceeded

在悲观锁模式下，事务之间出现会等锁的情况。等锁的超时时间由 TiDB 的 [innodb_lock_wait_timeout](/system-variables.md#innodb_lock_wait_timeout) 参数来定义，这个是 SQL 语句层面的最大允许等锁时间，即一个 SQL 语句期望加锁，但锁一直获取不到，超过这个时间，TiDB 不会再尝试加锁，会向客户端返回相应的报错信息。

可通过查看 TiDB 日志查看报错信息：

当出现等锁超时的情况时，会向客户端返回下述报错信息：

```log
ERROR 1205 (HY000): Lock wait timeout exceeded; try restarting transaction
```

处理建议：

* 如果出现的次数非常频繁，建议从业务逻辑的角度来进行调整。

#### TTL manager has timed out

除了有不能超出 GC 时间的限制外，悲观锁的 TTL 有上限，默认为 1 小时，所以执行时间超过 1 小时的悲观事务有可能提交失败。这个超时时间由 TiDB 参数 [performance.max-txn-ttl](https://github.com/pingcap/tidb/blob/master/config/config.toml.example) 指定。

可通过查看 TiDB 日志查看报错信息：

当悲观锁的事务执行时间超过 TTL 时，会出现下述报错：

```log
TTL manager has timed out, pessimistic locks may expire, please commit or rollback this transaction
```

处理建议：

* 当遇到该报错时，建议确认下业务逻辑是否可以进行优化，如将大事务拆分为小事务。在未使用[大事务](/tidb-configuration-file.md#txn-total-size-limit)的前提下，大事务可能会触发 TiDB 的事务限制。

* 可适当调整相关参数，使其符合事务要求。

#### Deadlock found when trying to get lock

死锁是指两个或两个以上的事务在执行过程中，由于竞争资源而造成的一种阻塞的现象，若无外力作用，它们都将无法推进下去，将永远在互相等待。此时，需要终止其中一个事务使其能够继续推进下去。

TiDB 在使用悲观锁的情况下，多个事务之间出现了死锁，必定有一个事务 abort 来解开死锁。在客户端层面行为和 MySQL 一致，在客户端返回表示死锁的 Error 1213。如下：

```log
[err="[executor:1213]Deadlock found when trying to get lock; try restarting transaction"]
```

处理建议：

* 如果出现非常频繁，需要调整业务代码来降低死锁发生概率。
