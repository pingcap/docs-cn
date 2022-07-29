---
title: TiDB Cloud FAQs
summary: Learn about the most frequently asked questions (FAQs) relating to TiDB Cloud.
---

# TiDB Cloud FAQs

<!-- markdownlint-disable MD026 -->

This document lists the most frequently asked questions about TiDB Cloud.

## What is TiDB Cloud?

TiDB Cloud makes deploying, managing, and maintaining your TiDB clusters even simpler with a fully managed cloud instance that you control through an intuitive console. You are able to easily deploy on Amazon Web Services or Google Cloud to quickly build mission-critical applications.

TiDB Cloud allows developers and DBAs with little or no training to handle once-complex tasks such as infrastructure management and cluster deployment with ease, to focus on your applications, not the complexities of your database. And by scaling TiDB clusters in or out with a simple click of a button, you no longer waste costly resources because you are able to provision your databases for exactly how much and how long you need them.

## What is the relationship between TiDB and TiDB Cloud?

TiDB is an open-source database and is the best option for organizations who want to run TiDB on-premises in their own data centers, in a self-managed cloud environment, or in a hybrid of the two.

TiDB Cloud is a fully managed cloud Database as a Service of TiDB. It has an easy-to-use web-based management console to let you manage TiDB clusters for mission-critical production environments.

## Is TiDB Cloud compatible with MySQL?

Currently, TiDB Cloud supports the majority of MySQL 5.7 syntax with the exception of triggers, stored procedures, user-defined functions, and foreign keys. For more details, see [Compatibility with MySQL](https://docs.pingcap.com/tidb/stable/mysql-compatibility).

## What programming languages can I use to work with TiDB Cloud?

You can use any language supported by the MySQL client or driver.

## Where can I run TiDB Cloud?

TiDB Cloud is currently available on Amazon Web Services and Google Cloud.

## What versions of TiDB are supported on TiDB Cloud?

For the currently supported TiDB version, see [TiDB Cloud Release Notes](/tidb-cloud/release-notes-2022.md).

## How can I learn more about TiDB Cloud?

The best way to learn about TiDB Cloud is to follow our step-by-step tutorial. Check out the following topics to get started:

- [TiDB Cloud Introduction](/tidb-cloud/tidb-cloud-intro.md)
- [Get Started](/tidb-cloud/tidb-cloud-quickstart.md)
- [Create a TiDB Cluster](/tidb-cloud/create-tidb-cluster.md)

## What companies are using TiDB or TiDB Cloud in production?

TiDB is trusted by over 1500 global enterprises across a variety of industries, such as financial services, gaming, and e-commerce. Our users include Square (US), PayPay (Japan), Shopee (Singapore), and China UnionPay (China). See our [case studies](https://en.pingcap.com/customers/) for specific details.

## How does TiDB Cloud ensure high availability?

TiDB uses the Raft consensus algorithm to ensure that data is highly available and safely replicated throughout storage in Raft Groups. Data is redundantly copied between TiKV nodes and placed in different Availability Zones to protect against machine or data center failure. With automatic failover, TiDB ensures that your service is always on.

As a Software as a Service (SaaS) provider, we take data security seriously. We have established strict information security policies and procedures required by the [Service Organization Control (SOC) 2 Type 1 compliance](https://pingcap.com/blog/pingcap-successfully-completes-soc-2-type-1-examination-for-tidb-cloud). This ensures that your data is secure, available, and confidential.

## What support is available for customers?

TiDB Cloud is supported by the same team behind TiDB, which has run mission-critical use cases for over 1500 global enterprises across industries including financial services, e-commerce, enterprise applications, and gaming. Support is available 24/7 for TiDB Cloud users.

## There are different components in my TiDB Cluster. What are PD, TiDB, TiKV, and TiFlash nodes?

PD, the Placement Driver is “the brain” of the entire TiDB cluster, as it stores the metadata of the cluster. It sends data scheduling commands to specific TiKV nodes according to the data distribution state reported by TiKV nodes in real-time.

TiDB is the SQL computing layer that aggregates data from queries returned from TiKV or TiFlash stores. TiDB is horizontally scalable; increasing the number of TiDB nodes will increase the number of concurrent queries the cluster can handle.

TiKV is the transactional store used to store OLTP data. All the data in TiKV is automatically maintained in multiple replicas (three replicas by default), so TiKV has native high availability and supports automatic failover. TiKV is horizontally scalable; increasing the number of transactional stores will increase OLTP throughput.

TiFlash is the analytical storage that replicates data from the transactional store (TiKV) in real-time and supports real-time OLAP workloads. Unlike TiKV, TiFlash stores data in columns to accelerate analytical processing. TiFlash is also horizontally scalable; increasing TiFlash nodes will increase OLAP storage and computing capacity.

## How does TiDB replicate data between the TiKV nodes?

TiKV divides the key-value space into key ranges, and each key range is treated as a “Region”. In TiKV, data is distributed among all nodes in a cluster and uses the Region as the basic unit. PD is responsible for spreading (scheduling) Regions as evenly as possible across all nodes in a cluster.

TiDB uses the Raft consensus algorithm to replicate data by Regions. Multiple replicas of a Region stored in different nodes form a Raft Group.

Each data change is recorded as a Raft log. Through Raft log replication, data is safely and reliably replicated to multiple nodes of the Raft Group.

## How do I make use of TiDB Cloud’s HTAP capabilities?

Traditionally, there are two types of databases: Online Transactional Processing (OLTP) databases and Online Analytical Processing (OLAP) databases. OLTP and OLAP requests are often processed in different and isolated databases. With this traditional architecture, migrating data from an OLTP database to a data warehouse or data lake for OLAP is a long and error-prone process.

As a Hybrid Transactional Analytical Processing (HTAP) database, TiDB Cloud helps you simplify your system architecture, reduce maintenance complexity, and support real-time analytics on transactional data by automatically replicating data reliably between the OLTP (TiKV) store and OLAP (TiFlash) store. Typical HTAP use cases are user personalization, AI recommendation, fraud detection, business intelligence, and real-time reporting.

For further HTAP scenarios, refer to [How We Build an HTAP Database That Simplifies Your Data Platform](https://pingcap.com/blog/how-we-build-an-htap-database-that-simplifies-your-data-platform).

## Is there an easy migration path from another RDBMS to TiDB Cloud?

TiDB is highly compatible with MySQL. You can migrate data from any MySQL-compatible databases to TiDB smoothly, whether the data is from a self-hosted MySQL instance or RDS service provided by the public cloud. For more information, see [Migrate Data from MySQL-Compatible Databases](/tidb-cloud/migrate-data-into-tidb.md).

## How does TiDB protect data privacy and ensure security?

Transport Layer Security (TLS) and Transparent Data Encryption (TDE) are included for encryption at rest. There are two different network planes: the application to the TiDB server and the plane for data communication. We include extended syntax to compare Subject Alternative Name for verification of certificates and TLS context for internal communication.

## Can I import my data directly to TiFlash?

No. When you import data to TiDB Cloud, the data is imported to TiKV. After the import is complete, you can use SQL statements to specify which tables to be replicated to TiFlash. Then, TiDB will create the replicas of the specified tables in TiFlash accordingly. For more information, see [Create TiFlash Replicas](/tiflash/create-tiflash-replicas.md).

## Can I export TiFlash data in the CSV format?

No. TiFlash data cannot be exported.
