---
title: TiCDC 常见问题和故障处理
category: reference
aliases: ['/docs-cn/dev/reference/tools/ticdc/troubleshoot/']
---

# TiCDC 常见问题和故障处理

本文档总结了在使用 TiCDC 过程中经常遇到的问题，给出合适的运维方法。本文档还总结了常见的运行故障，并给出相对应的解决方案。

## 启动任务时如何选择 start-ts

首先需要理解同步任务的 `start-ts` 对应于上游 TiDB 集群的一个 TSO，同步任务会从这个 TSO 开始请求数据。所以同步任务的 `start-ts` 需要满足以下两个条件：

- `start-ts` 的值需要大于 TiDB 集群当前的 `tikv_gc_safe_point`，否则创建任务时会报错。
- 启动任务时，需要保证下游已经具有 `start-ts` 之前的所有数据。对于同步到消息队列等场景，如果不需要保证上下游数据的一致，可根据业务场景放宽此要求。

如果不指定 `start-ts` 或者指定 `start-ts=0`，在启动任务的时候会去 PD 获取一个当前 TSO，并从该 TSO 开始同步。

## 启动任务时提示部分表不能同步

在使用 `cdc cli changefeed create` 创建同步任务时会检查上游表是否符合[同步限制](/ticdc/ticdc-overview.md#同步限制)。如果存在表不满足同步限制，会提示 `some tables are not eligible to replicate` 并列出这些不满足的表。用户选择 `Y` 或 `y` 则会继续创建同步任务，并且同步过程中自动忽略这些表的所有更新。用户选择其他输入，则不会创建同步任务。

## 同步中断的处理方法

目前已知可能发生的同步中断包括以下两类场景：

- 下游持续异常，TiCDC 多次重试后仍然失败。

    - 该场景下 TiCDC 会保存任务信息，由于 TiCDC 已经在 PD 中设置的 service GC safepoint，在 `gc-ttl` 的有效期内，同步任务 checkpoint 之后的数据不会被 TiKV GC 清理掉。

    - 处理方法：用户可以在下游恢复正常后，通过 HTTP 接口恢复同步任务。

- 因下游存在不兼容的 SQL 语句，导致同步不能继续。

    - 该场景下 TiCDC 会保存任务信息，由于 TiCDC 已经在 PD 中设置的 service GC safepoint，在 `gc-ttl` 的有效期内，同步任务 checkpoint 之后的数据不会被 TiKV GC 清理掉。
    - 处理方法：
        1. 用户需先通过 `cdc cli changefeed query` 查询同步任务状态信息，记录 `checkpoint-ts` 值。
        2. 使用新的任务配置文件，增加`ignore-txn-start-ts` 参数跳过指定 `start-ts` 对应的事务。
        3. 通过 HTTP API 停止旧的同步任务，使用 `cdc cli changefeed create` ，指定新的任务配置文件，指定 `start-ts` 为刚才记录的 `checkpoint-ts`，启动新的同步任务恢复同步。

## `gc-ttl` 和文件排序

从 TiDB v4.0.0-rc.1 版本起，PD 支持外部服务设置服务级别 GC safepoint。任何一个服务可以注册更新自己服务的 GC safepoint。PD 会保证任何小于该 GC safepoint 的 KV 数据不会在 TiKV 中被 GC 清理掉。在 TiCDC 中启用了这一功能，用来保证 TiCDC 在不可用、或同步任务中断情况下，可以在 TiKV 内保留 TiCDC 需要消费的数据不被 GC 清理掉。

启动 TiCDC server 时可以通过 `gc-ttl` 指定 GC safepoint 的 TTL，这个值的含义是当 TiCDC 服务全部挂掉后，由 TiCDC 在 PD 所设置的 GC safepoint 保存的最长时间，该值默认为 86400 秒。

如果同步任务长时间中断，累积未消费的数据比较多，初始启动 TiCDC 可能会发生 OOM。这种情况下可以启用 TiCDC 提供的文件排序功能，该功能会使用文件系统文件进行排序。启用的方式是创建同步任务时在 `cdc cli` 内传入 `--sort-engine=file` 和 `--sort-dir=/path/to/sort_dir`，使用示例如下：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --pd=http://10.0.10.25:2379 --start-ts=415238226621235200 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --sort-engine="file" --sort-dir="/data/cdc/sort"
```

> **注意：**
>
> TiCDC（4.0 发布版本）还不支持动态修改文件排序和内存排序。

## 创建同步任务或同步到 MySQL 时遇到 `Error 1298: Unknown or incorrect time zone: 'UTC'` 错误

这是因为下游 MySQL 没有加载时区，可以通过 [mysql_tzinfo_to_sql](https://dev.mysql.com/doc/refman/8.0/en/mysql-tzinfo-to-sql.html) 命令加载时区，加载后就可以正常创建任务或同步任务。

{{< copyable "shell-regular" >}}

```shell
mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root mysql -p
```

```
Enter password:
Warning: Unable to load '/usr/share/zoneinfo/iso3166.tab' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/leap-seconds.list' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/zone.tab' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/zone1970.tab' as time zone. Skipping it.
```

如果是在特殊的公有云环境使用 MySQL，譬如阿里云 RDS 并且没有修改 MySQL 的权限，就需要通过 `--tz` 参数指定时区。可以首先在 MySQL 查询其使用的时区，然后在创建同步任务和创建 TiCDC 服务时使用该时区。

{{< copyable "shell-regular" >}}

```shell
show variables like '%time_zone%';
```

```
+------------------+--------+
| Variable_name    | Value  |
+------------------+--------+
| system_time_zone | CST    |
| time_zone        | SYSTEM |
+------------------+--------+
```

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --sink-uri="mysql://root@127.0.0.1:3306/" --tz=Asia/Shanghai
```

> **注意：**
>
> 在 MySQL 中 CST 时区通常实际代表的是 China Standard Time (UTC+08:00)，通常系统中不能直接使用 `CST`，而是用 `Asia/Shanghai` 来替换。

> **注意：**
>
> 请谨慎设置 TiCDC server 的时区，因为该时区会用于时间类型的转换。推荐上下游数据库使用相同的时区，并且启动 TiCDC server 时通过 `--tz` 参数指定该时区。TiCDC server 时区使用的优先级如下：
>
> - 最优先使用 `--tz` 传入的时区
> - 没有 `--tz` 参数，会尝试读取 `TZ` 环境变量设置的时区
> - 如果还没有 `TZ` 环境变量，会从 TiCDC server 运行机器的默认时区
