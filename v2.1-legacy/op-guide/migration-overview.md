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

在这个数据迁移过程中，我们会用到下面四个工具:

- checker 检查 schema 能否被 TiDB 兼容
- mydumper 从 MySQL 导出数据
- loader 导入数据到 TiDB
- syncer 增量同步 MySQL 数据到 TiDB

## 两种迁移场景

- 第一种场景：只全量导入历史数据 （需要 checker + mydumper + loader）；
- 第二种场景：全量导入历史数据后，通过增量的方式同步新的数据 （需要 checker + mydumper + loader + syncer）。该场景需要提前开启 binlog 且格式必须为 ROW。

## MySQL 开启 binlog

> **注意：**
>
> 只有上文提到的第二种场景才需要在 dump 数据之前先开启 binlog**

+   MySQL 开启 binlog 功能，参考 [Setting the Replication Master Configuration](http://dev.mysql.com/doc/refman/5.7/en/replication-howto-masterbaseconfig.html)
+   Binlog 格式必须使用 `ROW` format，这也是 MySQL 5.7 之后推荐的 binlog 格式，可以使用如下语句打开:

    ```sql
    SET GLOBAL binlog_format = ROW;
    ```

## 使用 checker 进行 Schema 检查

在迁移之前，我们可以使用 TiDB 的 checker 工具，来预先检查 TiDB 是否能支持需要迁移的 table schema。如果 check 某个 table schema 失败，表明 TiDB 当前并不支持，我们不能对该 table 里面的数据进行迁移。checker 包含在 TiDB 工具集里面，我们可以直接下载。

### 下载 TiDB 工具集 (Linux)

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

### 使用 checker 检查的一个示范

+   在 MySQL 的 test database 里面创建几张表，并插入数据:

    ```sql
    USE test;
    CREATE TABLE t1 (id INT, age INT, PRIMARY KEY(id)) ENGINE=InnoDB;
    CREATE TABLE t2 (id INT, name VARCHAR(256), PRIMARY KEY(id)) ENGINE=InnoDB;

    INSERT INTO t1 VALUES (1, 1), (2, 2), (3, 3);
    INSERT INTO t2 VALUES (1, "a"), (2, "b"), (3, "c");
    ```

+   使用 checker 检查 test database 里面所有的 table

    ```bash
    ./bin/checker -host 127.0.0.1 -port 3306 -user root test
    2016/10/27 13:11:49 checker.go:48: [info] Checking database test
    2016/10/27 13:11:49 main.go:37: [info] Database DSN: root:@tcp(127.0.0.1:3306)/test?charset=utf8
    2016/10/27 13:11:49 checker.go:63: [info] Checking table t1
    2016/10/27 13:11:49 checker.go:69: [info] Check table t1 succ
    2016/10/27 13:11:49 checker.go:63: [info] Checking table t2
    2016/10/27 13:11:49 checker.go:69: [info] Check table t2 succ
    ```

+   使用 checker 检查 test database 里面某一个 table

    这里，假设我们只需要迁移 table `t1`。

    ```bash
    ./bin/checker -host 127.0.0.1 -port 3306 -user root test t1
    2016/10/27 13:13:56 checker.go:48: [info] Checking database test
    2016/10/27 13:13:56 main.go:37: [info] Database DSN: root:@tcp(127.0.0.1:3306)/test?charset=utf8
    2016/10/27 13:13:56 checker.go:63: [info] Checking table t1
    2016/10/27 13:13:56 checker.go:69: [info] Check table t1 succ
    Check database succ!
    ```

### 一个无法迁移的 table 例子

我们在 MySQL 里面创建如下表：

```sql
CREATE TABLE t_error ( a INT NOT NULL, PRIMARY KEY (a))
ENGINE=InnoDB TABLESPACE ts1
PARTITION BY RANGE (a) PARTITIONS 3 (
PARTITION P1 VALUES LESS THAN (2),
PARTITION P2 VALUES LESS THAN (4) TABLESPACE ts2,
PARTITION P3 VALUES LESS THAN (6) TABLESPACE ts3);
```

使用 `checker` 进行检查，会报错，表明我们没法迁移 `t_error` 这张表。

```bash
./bin/checker -host 127.0.0.1 -port 3306 -user root test t_error
2017/08/04 11:14:35 checker.go:48: [info] Checking database test
2017/08/04 11:14:35 main.go:39: [info] Database DSN: root:@tcp(127.0.0.1:3306)/test?charset=utf8
2017/08/04 11:14:35 checker.go:63: [info] Checking table t1
2017/08/04 11:14:35 checker.go:67: [error] Check table t1 failed with err: line 3 column 29 near " ENGINE=InnoDB DEFAULT CHARSET=latin1
/*!50100 PARTITION BY RANGE (a)
(PARTITION P1 VALUES LESS THAN (2) ENGINE = InnoDB,
 PARTITION P2 VALUES LESS THAN (4) TABLESPACE = ts2 ENGINE = InnoDB,
 PARTITION P3 VALUES LESS THAN (6) TABLESPACE = ts3 ENGINE = InnoDB) */" (total length 354)
github.com/pingcap/tidb/parser/yy_parser.go:96:
github.com/pingcap/tidb/parser/yy_parser.go:109:
/home/jenkins/workspace/build_tidb_tools_master/go/src/github.com/pingcap/tidb-tools/checker/checker.go:122:  parse CREATE TABLE `t1` (
  `a` int(11) NOT NULL,
  PRIMARY KEY (`a`)
) /*!50100 TABLESPACE ts1 */ ENGINE=InnoDB DEFAULT CHARSET=latin1
/*!50100 PARTITION BY RANGE (a)
(PARTITION P1 VALUES LESS THAN (2) ENGINE = InnoDB,
 PARTITION P2 VALUES LESS THAN (4) TABLESPACE = ts2 ENGINE = InnoDB,
 PARTITION P3 VALUES LESS THAN (6) TABLESPACE = ts3 ENGINE = InnoDB) */ error
/home/jenkins/workspace/build_tidb_tools_master/go/src/github.com/pingcap/tidb-tools/checker/checker.go:114:
2017/08/04 11:14:35 main.go:83: [error] Check database test with 1 errors and 0 warnings.
```
