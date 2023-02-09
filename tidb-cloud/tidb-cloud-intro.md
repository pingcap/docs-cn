---
title: TiDB Cloud Introduction
summary: Learn about TiDB Cloud and its architecture.
category: intro
---

# TiDB Cloud Introduction

[TiDB Cloud](https://www.pingcap.com/tidb-cloud/) is a fully-managed Database-as-a-Service (DBaaS) that brings [TiDB](https://docs.pingcap.com/tidb/stable/overview), an open-source Hybrid Transactional and Analytical Processing (HTAP) database, to your cloud. TiDB Cloud offers an easy way to deploy and manage databases to let you focus on your applications, not the complexities of the databases. You can create TiDB Cloud clusters to quickly build mission-critical applications on Google Cloud Platform (GCP) and Amazon Web Services (AWS).

![TiDB Cloud Overview](/media/tidb-cloud/tidb-cloud-overview.png)

## Why TiDB Cloud

TiDB Cloud allows you with little or no training to handle complex tasks such as infrastructure management and cluster deployment easily.

- Developers and database administrators (DBAs) can handle a large amount of online traffic effortlessly and rapidly analyze a large volume of data across multiple datasets.

- Enterprises of all sizes can easily deploy and manage TiDB Cloud to adapt to your business growth without prepayment.

Watch the following video to learn more about TiDB Cloud:

<iframe width="600" height="450" src="https://www.youtube.com/embed/skCV9BEmjbo?enablejsapi=1" title="Why TiDB Cloud?" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

With TiDB Cloud, you can get the following key features:

- **Fast and Customized Scaling**

    Elastically and transparently scale to hundreds of nodes for critical workloads while maintaining ACID transactions. No need to bother with sharding. And you can scale your performance and storage nodes separately according to your business needs.

- **MySQL Compatibility**

    Increase productivity and shorten time-to-market for your applications with TiDB's MySQL compatibility. Easily migrate data from existing MySQL instances without the need to rewrite code. Feel free to write and run your SQL in TiDB Cloud [Playground](/tidb-cloud/tidb-cloud-glossary.md#playground) instantly, which contains a pre-loaded dataset of GitHub events.

- **High Availability and Reliability**

    Naturally high availability by design. Data replication across multiple Availability Zones, daily backups, and auto-failover ensure business continuity, regardless of hardware failure, network partition, or data center loss.

- **Real-Time Analytics**

    Get real-time analytical query results with a built-in analytics engine. TiDB Cloud runs consistent analytical queries on current data without disturbing mission-critical applications. Feel free to experience TiDB Cloud's speed in [Playground](/tidb-cloud/tidb-cloud-glossary.md#playground), without loading your data or connecting to your client.

- **Enterprise Grade Security**

    Secure your data in dedicated networks and machines, with support for encryption both in-flight and at-rest. TiDB Cloud is certified by SOC 2 Type 2, ISO 27001:2013, ISO 27701, and fully compliant with GDPR.

- **Fully-Managed Service**

    Deploy, scale, monitor, and manage TiDB clusters with a few clicks, through an easy-to-use web-based management platform.

- **Multi-Cloud Support**

    Stay flexible without cloud vendor lock-in. TiDB Cloud is currently available on AWS and GCP.

- **Simple Pricing Plans**

    Pay only for what you use, with transparent and upfront pricing with no hidden fees.

- **World-Class Support**

    Get world-class support through our support portal, <a href="mailto:tidbcloud-support@pingcap.com">email</a>, chat, or video conferencing.

## Architecture

![TiDB Cloud architecture](/media/tidb-cloud/tidb-cloud-architecture.png)

- TiDB VPC (Virtual Private Cloud)

    For each TiDB Cloud cluster, all TiDB nodes and auxiliary nodes, including TiDB Operator nodes and logging nodes, are deployed in an independent VPC.

- TiDB Cloud Central Services

    Central Services, including billing, alerts, meta storage, dashboard UI, are deployed independently. You can access the dashboard UI to operate the TiDB cluster via the internet.

- Your VPC

    You can connect to your TiDB cluster via private endpoint connection or VPC peering connection. Refer to [Set Up Private Endpoint Connections](/tidb-cloud/set-up-private-endpoint-connections.md) or [Set up VPC Peering Connection](/tidb-cloud/set-up-vpc-peering-connections.md) for details.
