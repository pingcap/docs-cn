---
title: TiDB Introduction
summary: An introduction to the TiDB database platform
category: introduction
---

# TiDB Introduction

TiDB (The pronunciation is: /'taɪdiːbi:/ tai-D-B, etymology: titanium) is an open-source distributed scalable Hybrid Transactional and Analytical Processing (HTAP) database. It features horizontal scalability, strong consistency, and high availability. TiDB is MySQL compatible and serves as a one-stop data warehouse for both OLTP (Online Transactional Processing) and OLAP (Online Analytical Processing) workloads.

- __Horizontal scalability__

    TiDB provides horizontal scalability simply by adding new nodes. Never worry about infrastructure capacity ever again.

- __MySQL compatibility__

    Easily replace MySQL with TiDB to power your applications without changing a single line of code [in most cases](https://pingcap.com/docs/sql/mysql-compatibility/) and still benefit from the MySQL ecosystem.

- __Distributed transaction__

    TiDB is your source of truth, guaranteeing ACID compliance, so your data is accurate and reliable anytime, anywhere.

- __Cloud Native__

    TiDB is designed to work in the cloud -- public, private, or hybrid -- making deployment, provisioning, and maintenance drop-dead simple.

- __Minimize ETL__

    ETL (Extract, Transform and Load) is no longer necessary with TiDB's hybrid OLTP/OLAP architecture, enabling you to create new values for your users, easier and faster.

- __High availability__

    With TiDB, your data and applications are always on and continuously available, so your users are never disappointed.

TiDB is designed to support both OLTP and OLAP scenarios. For complex OLAP scenarios, use [TiSpark](tispark/tispark-user-guide.md).

Read the following three articles to understand TiDB techniques:

- [Data Storage](https://pingcap.github.io/blog/2017/07/11/tidbinternal1/)
- [Computing](https://pingcap.github.io/blog/2017/07/11/tidbinternal2/)
- [Scheduling](https://pingcap.github.io/blog/2017/07/20/tidbinternal3/)
