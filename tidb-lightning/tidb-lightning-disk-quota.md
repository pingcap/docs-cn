---
title: TiDB Lightning Disk Quota
summary: 介绍 TiDB Lightning 磁盘配额使用方法
---
# TiDB Lightning Disk Quota 原理
TiDB Lightning 的 local-backend 模式在导入数据的时候，会在本地磁盘创建大量的临时文件，用来对原始数据编码、排序、分割等操作，当用户本地磁盘空间不足的时候，TiDB Lightning 会因为写入文件失败而报错退出。为了减少这种情况的发生，TiDB Lightning 可以配置磁盘配额，当磁盘配额不足的时候，TiDB Lightning 会暂停读取源数据以及写入临时文件的过程，优先将已经排好序的 key-value 写入到 TiKV，删除本地临时文件，再继续导入过程。

# TiDB Lightning Disk Quota 的开启
在配置文件中加入配置项：
```toml
[tikv-importer]
disk-quota = "10GB"
backend = "local"

[cron]
check-disk-quota = "30s"
```
disk-quota 配置项可以设置磁盘配额，默认为 MaxInt64（即 9223372036854775807 字节，这个值太大了，相当于没开启）；check-disk-quota 配置项是检查磁盘配额的时间间隔，默认为 60 秒。由于检查临时文件使用空间的过程需要加锁，会使所有的导入线程都暂停，如果在每次写入之前都检查一次磁盘空间的使用情况，则会大大降低写入文件的效率（相当于单线程写入）；为了维持高效的写入，磁盘配额不会在每次写入之前检查，而是每隔一段时间暂停所有线程的写入并检查当前磁盘空间的使用情况。也就是说，当 check-disk-quota 配置项设置一个非常大的值时，磁盘的使用空间有可能会大大超出磁盘配额，这样的情况下，磁盘配额功能可以说是不生效的。因此，这个值建议不要设置太大，而具体设置多少则需要由 Lightning 具体运行的环境决定，因为不同的环境下，Lightning 写入临时文件的速度是不一样的。理论上来说，写入临时文件的速度越快，check-disk-quota 需要设置得越小。