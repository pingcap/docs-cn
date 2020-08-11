---
title: TiDB  Roadmap
category: Roadmap
aliases: ['/docs-cn/ROADMAP/','/docs-cn/roadmap/']
---

<!-- markdownlint-disable MD001 -->

# TiDB Roadmap

## Improve System Stability

- [ ] Create binding for `update`/`delete`/`insert` queries.
- [ ] Optimized the pessimistic transaction model when the DDL and DML were executed at the same time, the system error problem, improved the stability of the system.
- [ ] Reduce latency jitter.

## Improve System Performance and Reduce Latency

- [ ] Optimize the performance and efficiency of bulk deletion.
- [ ] Improve Memory Management .
- [ ] Improve the Accuracy and Robustness of Index Selection.
- [ ] Improve partition pruning and data access performance on the partition table.
- [ ] Async Commit.
- [ ] Clustered Index.
- [ ] Support Cross-Region Deployment & Geo-Partition.

## Improve System Security

### Authentication

- [ ] Transport Layer Security(TLS) for TiFlash.
- [ ] TLS in the internal communication of TiDB cluster.
- [ ] SSH LDAP extension for TiUP

### Transparent Data Encryption(TDE)

- [ ] Transparent Data Encryption(TDE) for TiFlash.
- [ ] Transparent Data Encryption(TDE) for PD.

### Mask

- [ ] De-Sensitization TiDB General Log.

## Cost-Effective

- [ ] Optimize the performance and stability of TiDB running on AWS i3.xlarge/i3.2xlarge.
- [ ] Optimize the performance and stability of TiDB running on No-NVME SSD or Cloud disk (like AWS EBS gp2).
- [ ] Easier discover performance issues and diagnose causes.

## New Feature

- [ ] Point-in-Time Recovery.
- [ ] Changing Column Types.
- [ ] Auto-Scaling on DBaaS.
- [ ] Support collation `utf8mb4_unicode_ci` and `utf8_unicode_ci`.
- [ ] Make TiCDC a complete alternative to TiDB-Binlog.
    - [ ] Support distinguish update and insert in a row changed event.
    - [ ] Support to provide old values in the row changed event, including old values in delete or update SQL.
- [ ] snapshot level consistent replication in disasters
    - [ ] Support MySQL sink can replicate to a snapshot level consistent state when upstream meets a disaster.
- [ ] Management TiCDC by SQL statements.
- [ ] Management TiCDC by API.
- [ ] SQL based import command.
- [ ] Support Avro sink and make TiCDC compatible with Kafka connect.
- [ ] Support Spark-3.0.
- [ ] Support `EXCEPT`/`INTERSECT` Operators.
- [ ] Direct write into TiFlash without going through TiKV.
- [ ] TiUP/Operator deployment and management DM 2.0.
- [ ] TiDB-Operator deploying one TiDB Cluster across multiple regions or data centers.
- [ ] TiDB operator supports heterogeneous design
- [ ] Support the migration of RDS (for example: MySQL/Aurora) on the cloud to TiDB.
