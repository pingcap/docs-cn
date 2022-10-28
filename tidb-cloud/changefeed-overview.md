---
title: Changefeed
---

# Changefeed

TiDB Cloud provides the following changefeeds to help you stream data from TiDB Cloud:

- [Sink to Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md)
- [Sink to MySQL](/tidb-cloud/changefeed-sink-to-mysql.md)

To learn the billing for changefeeds in TiDB Cloud, see [Changefeed billing](/tidb-cloud/tidb-cloud-billing-tcu.md).

> **Note:**
>
> You cannot [pause your cluster](/tidb-cloud/pause-or-resume-tidb-cluster.md) if it has any changefeeds. You need to delete the existing changefeeds ([Delete Sink to Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md#manage-the-changefeed) or [Delete Sink to MySQL](/tidb-cloud/changefeed-sink-to-mysql.md#delete-a-sink)) before pausing the cluster.