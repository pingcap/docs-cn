---
title: TiDB Lightning 常见的错误用法
category: reference
---

# TiDB Lightning 常见的错误用法

本文介绍了 [TiDB Lightning](../tidb-lightning/overview.md) 使用过程中常见的出错场景以及相应的处理方式。

## 报错：`checksum mismatched remote vs local`

在数据导入过程中遇到下面的报错

```log
Error: checksum mismatched remote vs local => (checksum: 3828723015727756136 vs 7895534721177712659) (total_kvs: 1221416844 vs 1501500000) (total_bytes:237660308510 vs 292158203078)
```

### 原因

* 先前使用过 TiDB Lightning 进行数据导入，但是对应的 [checkpoint](../tidb-lightning/checkpoints.md) 的数据没有被清理，存在残留的数据。可以通过查看 TiDB Lightning 第一次启动 log 来确认：
    * `[checkpoint] driver = file`，如果对应 TiDB Lightning 导入时间点的 log 存在 `open checkpoint file failed, going to create a new one`，那么 `checkpoint` 已经被正确清理，否则存在残留数据可能导致导入数据缺失；
    * `[checkpoint] driver = mysql`，可以通过使用 TiDB API `curl http://{TiDBIP}:10080/schema/{checkpoint.schema}/{checkpoint.table}` 来查询对应 `checkpoint table` 的创建时间，从而判断是否正确清理了 `checkpoint`。

* TiDB Lightning 导入的数据源存在冲突的数据
    * 不同行的数据具有相同的主键或唯一键

### 解决方案

* 删除出现 `checksum mismatch` 错误的表的数据

    ```
    tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-error-destroy=all
    ```

* 需要寻找办法检测数据源是否存在冲突数据，TiDB Lightning 一般需要处理大量的数据，所以目前还未提供有效的冲突检测和处理措施。
