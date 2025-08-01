---
title: DDL 常见问题
summary: 介绍 DDL 相关的常见问题。
---

# DDL 常见问题

本文档介绍 TiDB 中常见的 DDL 问题。

## TiDB DDL 是否支持 DDL 语句间并行？具体的一些运行特征是怎样的？

在 TiDB v6.2 之后，TiDB 提供并发 DDL（concurrent DDL） 执行的能力。 并发 DDL 主要是提供 DDL 语句间的并发执行支持。这里和以前的 DDL 执行将会发生如下变化：

1. 需要判断 DDL 语句间是否有相关性，如果有相关性的 DDL 语句将会按照进入 TiDB 的顺序执行，没有相关性的 DDL 语句可以并发执行。并发判断规则：
   1. 相同表上的 DDL 语句之间具有相关性，需要按照进入 TiDB 的顺序执行；
   2. 对于 Schema 上的操作，可能会对于 schema 中的表上的 DDL 语句建立相关性，目前 Drop Schema 会对于其包含 Schema 上的 DDL 产生相关性；也需要顺序执行；
2. 是否所有的 DDL 语句都会并发执行？
   当前，答案是否定的，在 TiDB 中 DDL 语句被分为两类，
   1. 普通（general）DDL 语句，这类 DDL 语句的执行只需要修改对象的元数据，不需要操作 schema 存储的数据，通常在秒级完成；需要的计算资源相对少；
   2. 需要重组（reorg）DDL 语句， 这类 DDL 语句的执行不仅需要修改对象的元数据，也需要对于 schema 存储的数据进行处理，例如：加索引，需要扫描全表数据，来创建索引，需要比较多的计算资源与较长的执行时间；
   当前我们仅对于需要重组的 DDL 语句启动了并发执行支持。
3. 对于启动了并发 DDL 语句支持的 TiDB 集群，DDL 语句间的并发度是如何确定的？
   目前因为 DDL 等后台任务的执行可能会占用相当的资源，因此我们采取了一个相对保守的策略来确定 DDL 语句执行的并发度
   1. 对于普通 DDL（general DDL） 语句，我们当前语句并发度为 1（后续将会提供并发执行支持）；
   2. 对于需要重组的 DDL（Reorg DDL）语句，我们的并发度设置规则如下（并发度不允许用户自己设置）： 
   TiDB DDL owner 节点容器能够使用的 CPU 资源数量的 1/4 与 1 之间的最大值，例如 8C 规格的 TiDB DDL owner 节点，并发度将会是 2。

## TiDB DDL 的优先级如何定义?
   由于 DDL 语句，特别是需要重组的 DDL 语句在执行的过程中可能会占用较多计算或者存储引擎资源，从而导致对于前端用户业务的影响。通过对 DDL 任务设置 
   - [`tidb_ddl_reorg_priority`](/system-variables.md#tidb_ddl_reorg_priority)
   对与 DDL 等任务如果用户在业务高峰期间，可以将优先级调低，这样 TiDB 集群会通过优先级降低 DDL 对于集群资源的争抢。
   - 其他参数的设置可以参考：
     - [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)
     - [`tidb_ddl_reorg_priority`](/system-variables.md#tidb_ddl_reorg_priority)
     - [`tidb_ddl_error_count_limit`](/system-variables.md#tidb_ddl_error_count_limit)
     - [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)

## 快速加索引方式的启动常见问题：
   从 TiDB v6.3 开始，我们为 TiDB 用户提供了 快速加索引的模式，可以相对于 v6.1 提升 10倍的速度。我们在 TiDB v6.5 快速加索引模式已经 GA。
   这里说明一下从低版本升级上来，的一些检查事项：
   **TiDB 配置参数**：
   - [`temp-dir`](/tidb-configuration-file#temp-dir-new-in-v630) 这个参数用来指定快速加索引模式执行本地磁盘路径。
     - 对于 On Premises 用户， 需要用户提前挂载好 SSD 磁盘，配置好相应路径，然后进行升级操作，重启后检查 TiDB
   ```sql
mysql> SHOW CONFIG WHERE type = 'tidb' AND name = 'temp-dir';
+------+---------------------------------------------------------------------------------------------+----------+-----------+
| Type | Instance                                                                                    | Name     | Value     |
+------+---------------------------------------------------------------------------------------------+----------+-----------+
| tidb | tidb-2:4000 | temp-dir | /tmp/tidb |
| tidb | tidb-1:4000 | temp-dir | /tmp/tidb |
| tidb | tidb-0:4000 | temp-dir | /tmp/tidb |
+------+---------------------------------------------------------------------------------------------+----------+-----------+
3 rows in set (0.52 sec)
```
   **注意：** 这个是一个配置参数，需要重启 TiDB 节点，上面 `Value` 字段查询出来值应该和用户设置的值应该一致。
    - 对于 Cloud 用户，我们对于能够使用快速加索引功能的使用有一些限制：

| 描述                    | 供应商 | TiDB CPU 规格      | 是否支持快速索引模式 | 备注   |
|-----------------------|-----|------------------|------------|------|
| TiDB cloud Dedicated  | AWS | 2C vCPU, 4C vCPU | 不支持        | 成本问题 |
|                       |     | \>= 8C vCPU      | 支持         |      |
|                       | GCP | ALL              | 不支持        |      |

   TiDB 系统变量设置
   - [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入)
   这个系统变量在 TiDB v6.5 默认打开。
   - [`tidb_ddl_disk_quota`](/system-variables.md#tidb_ddl_disk_quota-从-v630-版本开始引入)
   这个系统变量用来控制快速加索引方式本地磁盘能够使用的限额，对于 on Premises 用户来说可以根据实际情况增加这个值。