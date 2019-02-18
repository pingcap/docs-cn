---
title: 数据迁移概述
category: advanced
---

# 数据迁移概述

## 概述

该文档详细介绍了如何将 MySQL 的数据迁移到 TiDB。

这里我们假定 MySQL 以及 TiDB 服务信息如下：

|Name|Address|Port|User|Password|
|----|-------|----|----|--------|
|MySQL|127.0.0.1|3306|root|*|
|TiDB|127.0.0.1|4000|root|*|

在该数据迁移过程中，会用到下面三个工具：

- mydumper 从 MySQL 导出数据
- loader 导入数据到 TiDB
- syncer 增量同步 MySQL 数据到 TiDB

## 两种迁移场景

- 第一种场景：只全量导入历史数据（需要 mydumper + Loader）；
- 第二种场景：全量导入历史数据后，通过增量的方式同步新的数据（需要 mydumper + Loader + Syncer）。该场景需要提前开启 binlog 且格式必须为 ROW。

## MySQL 开启 binlog

**注意： 只有上文提到的第二种场景才需要在 dump 数据之前先开启 binlog**

+   MySQL 开启 binlog 功能，参考 [Setting the Replication Master Configuration](http://dev.mysql.com/doc/refman/5.7/en/replication-howto-masterbaseconfig.html)
+   Binlog 格式必须使用 `ROW` format，这也是 MySQL 5.7 之后推荐的 binlog 格式，可以使用如下语句打开:

    ```sql
    SET GLOBAL binlog_format = ROW;
    ```

## 下载 TiDB 工具集 (Linux)

```bash
# 下载 tool 压缩包
wget http://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.tar.gz
wget http://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.sha256

# 检查文件完整性，返回 ok 则正确
sha256sum -c tidb-enterprise-tools-latest-linux-amd64.sha256
# 解开压缩包
tar -xzf tidb-enterprise-tools-latest-linux-amd64.tar.gz
cd tidb-enterprise-tools-latest-linux-amd64
```
