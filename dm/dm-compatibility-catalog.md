---
title: Compatibility Catalog of TiDB Data Migration
summary: This document describes the compatibility between DM of different versions and upstream/downstream databases.
---

# Compatibility Catalog of TiDB Data Migration

DM supports migrating data from different sources to TiDB clusters. Based on the data source type, DM has four compatibility levels:

- **Generally available (GA)**: The application scenario has been verified and passed the GA test.
- **Experimental**: Although the application scenario has been verified, the test does not cover all scenarios or involves only a limited number of users. The application scenario might encounter problems occasionally.
- **Not tested**: DM is expected to be always compatible with MySQL during iteration. However, due to resource constraints, not all MySQL forks are tested with DM. Therefore, the *not tested* source or target is technically compatible with DM, but is not fully tested, which means you need to verify its compatibility before you use.
- **Incompatible**: DM is proved to be incompatible with the data source and the application is not recommended for use in production environments.

## Data sources

|Data source|Compatibility level|Remarks|
|-|-|-|
|MySQL ≤ 5.5|Not tested||
|MySQL 5.6|GA||
|MySQL 5.7|GA||
|MySQL 8.0|GA|Does not support binlog transaction compression [Transaction_payload_event](https://dev.mysql.com/doc/refman/8.0/en/binary-log-transaction-compression.html)|
|MariaDB < 10.1.2|Incompatible|Incompatible with binlog of the time type|
|MariaDB 10.1.2 ~ 10.5.10|Experimental||
|MariaDB > 10.5.10|Incompatible|Permission errors reported in the check procedure|

## Target databases

> **Warning:**
>
> DM v5.3.0 is not recommended. If you have enabled GTID replication but do not enable relay log in DM v5.3.0, data replication fails with low probability.

|Target database|Compatibility level|DM version|
|-|-|-|
|TiDB 6.0|GA|≥ 5.3.1|
|TiDB 5.4|GA|≥ 5.3.1|
|TiDB 5.3|GA|≥ 5.3.1|
|TiDB 5.2|GA|≥ 2.0.7, recommended: 5.4|
|TiDB 5.1|GA|≥ 2.0.4, recommended: 5.4|
|TiDB 5.0|GA|≥ 2.0.4, recommended: 5.4|
|TiDB 4.x|GA|≥ 2.0.1, recommended: 2.0.7|
|TiDB 3.x|GA|≥ 2.0.1, recommended: 2.0.7|
|MySQL|Experimental||
|MariaDB|Experimental||