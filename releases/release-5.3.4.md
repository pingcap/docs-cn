---
title: TiDB 5.3.4 Release Notes
---

# TiDB 5.3.4 Release Notes

Release date: November 24, 2022

TiDB version: 5.3.4

## Improvements

+ TiKV

    - Reload TLS certificate automatically for each update to improve availability [#12546](https://github.com/tikv/tikv/issues/12546)

## Bug fixes

+ TiDB

    - Fix the issue that the Region cache is not cleaned up in time when the Region is merged [#37141](https://github.com/pingcap/tidb/issues/37141)
    - Fix the issue that TiDB writes wrong data due to the wrong encoding of the `ENUM` or `SET` column [#32302](https://github.com/pingcap/tidb/issues/32302)
    - Fix the issue that database-level privileges are incorrectly cleaned up [#38363](https://github.com/pingcap/tidb/issues/38363)
    - Fix the issue that the `grantor` field is missing in the `mysql.tables_priv` table [#38293](https://github.com/pingcap/tidb/issues/38293)
    - Fix the issue that `KILL TIDB` cannot take effect immediately on idle connections [#24031](https://github.com/pingcap/tidb/issues/24031)
    - Fix the issue that the return type of `date_add` and `date_sub` is different between TiDB and MySQL [#36394](https://github.com/pingcap/tidb/issues/36394), [#27573](https://github.com/pingcap/tidb/issues/27573)
    - Fix the incorrect `INSERT_METHOD` value when Parser restores table options [#38368](https://github.com/pingcap/tidb/issues/38368)
    - Fix the issue that authentication fails when a MySQL client of v5.1 or earlier connects to the TiDB server [#29725](https://github.com/pingcap/tidb/issues/29725)
    - Fix wrong results of `GREATEST` and `LEAST` when passing in unsigned `BIGINT` arguments [#30101](https://github.com/pingcap/tidb/issues/30101)
    - Fix the issue that the result of `concat(ifnull(time(3))` in TiDB is different from that in MySQL [#29498](https://github.com/pingcap/tidb/issues/29498)
    - Fix the issue that the `avg()` function returns `ERROR 1105 (HY000): other error for mpp stream: Could not convert to the target type - -value is out of range.` when queried from TiFlash [#29952](https://github.com/pingcap/tidb/issues/29952)
    - Fix the issue that `ERROR 1105 (HY000): close of nil channel` is returned when using `HashJoinExec` [#30289](https://github.com/pingcap/tidb/issues/30289)
    - Fix the issue that TiKV and TiFlash return different results when querying logical operations [#37258](https://github.com/pingcap/tidb/issues/37258)
    - Fix the issue that the `EXPLAIN ANALYZE` statement with DML executors might return result before the transaction commit finishes [#37373](https://github.com/pingcap/tidb/issues/37373)
    - Fix the issue that Region cache is not cleared properly after merging many Regions [#37174](https://github.com/pingcap/tidb/issues/37174)
    - Fix the issue that the `EXECUTE` statement might throw an unexpected error in specific scenarios [#37187](https://github.com/pingcap/tidb/issues/37187)
    - Fix the issue that `GROUP CONCAT` with `ORDER BY` might fail when the `ORDER BY` clause contains a correlated subquery [#18216](https://github.com/pingcap/tidb/issues/18216)
    - Fix wrong results returned when length and width are incorrectly set for Decimal and Real when using plan cache [#29565](https://github.com/pingcap/tidb/issues/29565)

+ PD

    - Fix the issue that PD cannot correctly handle dashboard proxy requests [#5321](https://github.com/tikv/pd/issues/5321)
    - Fix the issue that the TiFlash learner replica might not be created in specific scenarios [#5401](https://github.com/tikv/pd/issues/5401)
    - Fix inaccurate Stream timeout and accelerate leader switchover [#5207](https://github.com/tikv/pd/issues/5207)

+ TiFlash

    - Fix the issue that logical operators return wrong results when the argument type is UInt8 [#6127](https://github.com/pingcap/tiflash/issues/6127)
    - Fix the issue that TiFlash bootstrap fails when `0.0` is used as the default value for integers, for example, `` `i` int(11) NOT NULL DEFAULT '0.0'`` [#3157](https://github.com/pingcap/tiflash/issues/3157)

+ Tools

    + Dumpling

        - Fix the issue that Dumpling cannot dump data when the `--compress` option and the S3 output directory are set simultaneously [#30534](https://github.com/pingcap/tidb/issues/30534)

    + TiCDC

        - Fix the issue that changefeed state is incorrect because a MySQL-related error is not reported to the owner in time [#6698](https://github.com/pingcap/tiflow/issues/6698)
