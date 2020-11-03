---
title: TiDB Roadmap
aliases: ['/docs/ROADMAP/','/docs/roadmap/','/docs/stable/roadmap/','/docs/v4.0/roadmap/','/tidb/stable/roadmap','/docs/v3.1/roadmap/','/tidb/v3.1/roadmap','/docs/v3.0/roadmap/','/tidb/v3.0/roadmap','/docs/v2.1/roadmap/','/tidb/v2.1/roadmap']
---

<!-- markdownlint-disable MD001 -->

# TiDB Roadmap

## Improve system stability

- [ ] Create bindings for `UPDATE`/`DELETE`/`INSERT` queries [#15827](https://github.com/pingcap/tidb/issues/15827)
- [ ] Optimize transaction commits to avoid commit failures caused by DDL execution [#18098](https://github.com/pingcap/tidb/issues/18098)
- [ ] Reduce latency jitter [#18005](https://github.com/pingcap/tidb/issues/18005)

## Improve system performance and reduce latency

- [ ] Optimize the performance and efficiency of bulk deletion [#18028](https://github.com/pingcap/tidb/issues/18028)
- [ ] Improve memory management [#17479](https://github.com/pingcap/tidb/issues/17479)
- [ ] Improve the accuracy and robustness of index selection [#18065](https://github.com/pingcap/tidb/issues/18065)
- [ ] Improve the performance of partition pruning and data access on the partitioned table [#18016](https://github.com/pingcap/tidb/issues/18016)
- [ ] Async Commit. This feature means that the statement being written can return to the client as soon as possible after the prewrite stage finishes, which reduces system latency. [#8316](https://github.com/tikv/tikv/issues/8316)
- [ ] Clustered index [#4841](https://github.com/pingcap/tidb/issues/4841)
- [ ] Support cross-region deployment and geo-partition [#18273](https://github.com/pingcap/tidb/issues/18273)

## Improve system security

### Authentication

- [ ] Transport Layer Security (TLS) for TiFlash [#18080](https://github.com/pingcap/tidb/issues/18080)
- [ ] TLS for internal communication in the TiDB cluster [#529](https://github.com/pingcap/tiup/issues/529)
- [ ] SSH LDAP extension for TiUP [#528](https://github.com/pingcap/tiup/issues/528)

### Transparent Data Encryption (TDE)

- [ ] Transparent Data Encryption (TDE) for TiFlash [#18082](https://github.com/pingcap/tidb/issues/18082)
- [ ] TDE for PD [#18262](https://github.com/pingcap/tidb/issues/18262)

### Mask

- [ ] Desensitize the TiDB general log [#18034](https://github.com/pingcap/tidb/issues/18034)

## Cost-effectiveness

- [ ] Optimize the performance and stability of TiDB running on AWS i3.xlarge/i3.2xlarge [#18025](https://github.com/pingcap/tidb/issues/18025)
- [ ] Optimize the performance and stability of TiDB running on non-NVMe SSD or on cloud disk (such as AWS EBS gp2) [#18024](https://github.com/pingcap/tidb/issues/18024)

## New features

- [ ] Point-in-time recovery [#325](https://github.com/pingcap/br/issues/325)
- [ ] Change column types [#17526](https://github.com/pingcap/tidb/issues/17526)
- [ ] Easier to discover performance issues and diagnose the causes [#18867](https://github.com/pingcap/tidb/issues/18867)
- [ ] Support the collations of `utf8mb4_unicode_ci` and `utf8_unicode_ci` [#17596](https://github.com/pingcap/tidb/issues/17596)
- [ ] Make TiCDC a complete alternative to TiDB Binlog [#690](https://github.com/pingcap/ticdc/issues/690)
    - [ ] Support distinguishing `UPDATE` and `INSERT` in a row changed event.
    - [ ] Support providing old values in the row changed event, including old values before the `DELETE` or `UPDATE` execution.
- [ ] Support snapshot-level consistent replication for disaster recovery [#691](https://github.com/pingcap/ticdc/issues/691)
    - [ ] Support MySQL sink in replicating the upstream to a snapshot-level consistent state when the upstream meets a disaster
- [ ] Manage TiCDC using API [#736](https://github.com/pingcap/ticdc/issues/736)
- [ ] Support the SQL-based `import` command [#18089](https://github.com/pingcap/tidb/issues/18089)
- [ ] Support Avro sink and make TiCDC compatible with Kafka connect [#660](https://github.com/pingcap/ticdc/issues/660)
- [ ] Support Spark 3.0 [#1173](https://github.com/pingcap/tispark/issues/1173)
- [ ] Support `EXCEPT`/`INTERSECT` operators [#18031](https://github.com/pingcap/tidb/issues/18031)
- [ ] Support migrating the RDS (such as MySQL/Aurora) on cloud to TiDB [#18629](https://github.com/pingcap/tidb/issues/18629)

## TiDB Operator

See [TiDB Operator Roadmap](https://docs.pingcap.com/tidb-in-kubernetes/dev/roadmap).
