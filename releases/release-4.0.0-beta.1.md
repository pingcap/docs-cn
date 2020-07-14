---
title: TiDB 4.0.0 Beta.1 Release Notes
aliases: ['/docs/dev/releases/release-4.0.0-beta.1/','/docs/dev/releases/4.0.0-beta.1/']
---

# TiDB 4.0.0 Beta.1 Release Notes

Release date: February 28, 2020

TiDB version: 4.0.0-beta.1

TiDB Ansible version: 4.0.0-beta.1

## Compatibility Changes

* TiDB
    + Modify the type of the `log.enable-slow-log` configuration item from integer to Boolean [#14864](https://github.com/pingcap/tidb/pull/14864)
    + Modify the `password` field name to `authentication_string` in the `mysql.user` system table to make it consistent with MySQL 5.7 (**This compatibility change means that you cannot roll back to earlier versions.**) [#14598](https://github.com/pingcap/tidb/pull/14598)
    + Adjust the default value of the `txn-total-size-limit` configuration item from `1GB` to `100MB` [#14522](https://github.com/pingcap/tidb/pull/14522)
    + Support dynamically modifying or updating configuration items read from PD [#14750](https://github.com/pingcap/tidb/pull/14750) [#14303](https://github.com/pingcap/tidb/pull/14303) [#14830](https://github.com/pingcap/tidb/pull/14830)

* TiKV
    + Add the `readpool.unify-read-pool` configuration item (`True` by default) to control whether point queries use the same threads with Coprocessor [#6375](https://github.com/tikv/tikv/pull/6375) [#6401](https://github.com/tikv/tikv/pull/6401) [#6534](https://github.com/tikv/tikv/pull/6534) [#6582](https://github.com/tikv/tikv/pull/6582) [#6585](https://github.com/tikv/tikv/pull/6585) [#6593](https://github.com/tikv/tikv/pull/6593) [#6597](https://github.com/tikv/tikv/pull/6597) [#6677](https://github.com/tikv/tikv/pull/6677)

* PD
    + Optimize the HTTP API to make it compatible with the configuration manager [#2080](https://github.com/pingcap/pd/pull/2080)

* TiDB Lightning
    + Use the default configurations specified in the document for certain items not configured in the configuration file [#255](https://github.com/pingcap/tidb-lightning/pull/255)

* TiDB Ansible
    + Rename `theflash` to `tiflash` [#1130](https://github.com/pingcap/tidb-ansible/pull/1130)
    + Optimize the default values and related configurations in TiFlash's configuration file [#1138](https://github.com/pingcap/tidb-ansible/pull/1138)

## New Features

* TiDB
    + Support querying slow logs of any time in the `SLOW_QUERY / CLUSTER_SLOW_QUERY` system table [#14840](https://github.com/pingcap/tidb/pull/14840) [#14878](https://github.com/pingcap/tidb/pull/14878)
    + Support SQL performance diagnosis
        - [#14843](https://github.com/pingcap/tidb/pull/14843) [#14810](https://github.com/pingcap/tidb/pull/14810) [#14835](https://github.com/pingcap/tidb/pull/14835) [#14801](https://github.com/pingcap/tidb/pull/14801) [#14743](https://github.com/pingcap/tidb/pull/14743)
        - [#14718](https://github.com/pingcap/tidb/pull/14718) [#14721](https://github.com/pingcap/tidb/pull/14721) [#14670](https://github.com/pingcap/tidb/pull/14670) [#14663](https://github.com/pingcap/tidb/pull/14663) [#14668](https://github.com/pingcap/tidb/pull/14668)
        - [#14896](https://github.com/pingcap/tidb/pull/14896)
    + Support the `Sequence` function [#14731](https://github.com/pingcap/tidb/pull/14731) [#14589](https://github.com/pingcap/tidb/pull/14589) [#14674](https://github.com/pingcap/tidb/pull/14674) [#14442](https://github.com/pingcap/tidb/pull/14442) [#14303](https://github.com/pingcap/tidb/pull/14303) [#14830](https://github.com/pingcap/tidb/pull/14830)
    + Support dynamically modifying or updating configuration items read from PD [#14750](https://github.com/pingcap/tidb/pull/14750) [#14303](https://github.com/pingcap/tidb/pull/14303) [#14830](https://github.com/pingcap/tidb/pull/14830)
    + Add a feature of automatically reading data from different roles according to the load balancing policy and add the `leader-and-follower` system variable to enable this feature [#14761](https://github.com/pingcap/tidb/pull/14761)
    + Add the `Coercibility` function [#14739](https://github.com/pingcap/tidb/pull/14739)
    + Support setting TiFlash replicas in the partitioned table [#14735](https://github.com/pingcap/tidb/pull/14735) [#14713](https://github.com/pingcap/tidb/pull/14713) [#14644](https://github.com/pingcap/tidb/pull/14644)
    + Improve the privilege check for the `SLOW_QUERY` table [#14451](https://github.com/pingcap/tidb/pull/14451)
    + Support automatically write the intermediate results to the disk file if the memory is insufficient when using a SQL join [#14708](https://github.com/pingcap/tidb/pull/14708) [#14279](https://github.com/pingcap/tidb/pull/14279)
    + Support checking table partitions by querying the `information_schema.PARTITIONS` system table [#14347](https://github.com/pingcap/tidb/pull/14347)
    + Add the `json_objectagg` aggregate function [#11154](https://github.com/pingcap/tidb/pull/11154)
    + Support logging rejected connection attempts in the audit log [#14594](https://github.com/pingcap/tidb/pull/14594)
    + Add the `max-server-connections` configuration item (`4096` by default) to control the number of connections to a single server [#14409](https://github.com/pingcap/tidb/pull/14409)
    + Support the isolation read specifying multiple storage engines at the server level [#14440](https://github.com/pingcap/tidb/pull/14440)
    + Optimize the cost model of the `Apply` operator and the `Sort` operator to improve stability [#13550](https://github.com/pingcap/tidb/pull/13550) [#14708](https://github.com/pingcap/tidb/pull/14708)

* TiKV
    + Support fetching configuration items from the status port via HTTP API [#6480](https://github.com/tikv/tikv/pull/6480)
    + Optimize the performance of `Chunk Encoder` in Coprocessor [#6341](https://github.com/tikv/tikv/pull/6341)

* PD
    + Support accessing to the distribution of hotspots in the cluster through Dashboard UI [#2086](https://github.com/pingcap/pd/pull/2086)
    + Support capturing and displaying `START_TIME` and `UPTIME` of cluster components [#2116](https://github.com/pingcap/pd/pull/2116)
    + Add the information of deployment path and component version in the returned message of the `member` API [#2130](https://github.com/pingcap/pd/pull/2130)
    + Add the `component` sub-command in pd-ctl to modify and check the configuration of other components (experimental) [#2092](https://github.com/pingcap/pd/pull/2092)

* TiDB Binlog
    + Support TLS between the components [#904](https://github.com/pingcap/tidb-binlog/pull/904) [#894](https://github.com/pingcap/tidb-binlog/pull/894)
    + Add the `kafka-client-id` configuration item in Drainer to configure Kafka's client ID [#902](https://github.com/pingcap/tidb-binlog/pull/902)
    + Support purging the incremental backup data in Drainer [#885](https://github.com/pingcap/tidb-binlog/pull/885)

* TiDB Ansible
    + Support deploying multiple Grafana/Prometheus/Alertmanagers in one cluster [#1142](https://github.com/pingcap/tidb-ansible/pull/1142)
    + Add the `metric_port` configuration item (`8234` by default) in TiFlash's configuration file [#1145](https://github.com/pingcap/tidb-ansible/pull/1145)
    + Add the `flash_proxy_status_port` configuration item (`20292` by default) in TiFlash's configuration file [#1141](https://github.com/pingcap/tidb-ansible/pull/1141)
    + Add the TiFlash monitoring dashboard [#1147](https://github.com/pingcap/tidb-ansible/pull/1147) [#1151](https://github.com/pingcap/tidb-ansible/pull/1151)

## Bug Fixes

* TiDB
    + Fix the issue that an error is reported when creating `view` with a column name that exceeds 64 characters [#14850](https://github.com/pingcap/tidb/pull/14850)
    + Fix the issue that duplicate data exists in `information_schema.views` because the `create or replace view` statement is incorrectly processed [#14832](https://github.com/pingcap/tidb/pull/14832)
    + Fix the incorrect results of `BatchPointGet` when `plan cache` is enabled [#14855](https://github.com/pingcap/tidb/pull/14855)
    + Fix the issue that data is inserted into the wrong partitioned table after the timezone is modified [#14370](https://github.com/pingcap/tidb/pull/14370)
    + Fix the panic occurred when rebuilding expression using the invalid name of the `IsTrue` function during the outer join simplification [#14515](https://github.com/pingcap/tidb/pull/14515)
    + Fix the the incorrect privilege check for the`show binding` statement [#14443](https://github.com/pingcap/tidb/pull/14443)

* TiKV
    + Fix the inconsistent behaviors of the `CAST` function in TiDB and TiKV [#6463](https://github.com/tikv/tikv/pull/6463) [#6461](https://github.com/tikv/tikv/pull/6461) [#6459](https://github.com/tikv/tikv/pull/6459) [#6474](https://github.com/tikv/tikv/pull/6474) [#6492](https://github.com/tikv/tikv/pull/6492) [#6569](https://github.com/tikv/tikv/pull/6569)

* TiDB Lightning
    + Fix the bug that the web interface does not work outside the Server mode [#259](https://github.com/pingcap/tidb-lightning/pull/259)
