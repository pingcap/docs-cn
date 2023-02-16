---
title: Perform a Proof of Concept (PoC) with TiDB Cloud
summary: Learn about how to perform a Proof of Concept (PoC) with TiDB Cloud.
---

# Perform a Proof of Concept (PoC) with TiDB Cloud

TiDB Cloud is a Database-as-a-Service (DBaaS) product that delivers everything great about TiDB in a fully managed cloud database. It helps you focus on your applications, instead of the complexities of your database. TiDB Cloud is currently available on both Amazon Web Services (AWS) and Google Cloud Platform (GCP).

Initiating a proof of concept (PoC) is the best way to determine whether TiDB Cloud is the best fit for your business needs. It will also get you familiar with the key features of TiDB Cloud in a short time. By running performance tests, you can see whether your workload can run efficiently on TiDB Cloud. You can also evaluate the efforts required to migrate your data and adapt configurations.

This document describes the typical PoC procedures and aims to help you quickly complete a TiDB Cloud PoC. It is a best practice that has been validated by TiDB experts and a large customer base.

If you are interested in doing a PoC, feel free to contact <a href="mailto:tidbcloud-support@pingcap.com">PingCAP</a> before you get started. The support team can help you create a test plan and walk you through the PoC procedures smoothly.

Alternatively, you can [create a Serverless Tier](/tidb-cloud/tidb-cloud-quickstart.md#step-1-create-a-tidb-cluster) to get familiar with TiDB Cloud for a quick evaluation. Note that the Serverless Tier has some [special terms and conditions](/tidb-cloud/select-cluster-tier.md#serverless-tier-special-terms-and-conditions).

## Overview of the PoC procedures

The purpose of a PoC is to test whether TiDB Cloud meets your business requirements. A typical PoC usually lasts 14 days, during which you are expected to focus on completing the PoC.

A typical TiDB Cloud PoC consists of the following steps:

1. Define success criteria and create a test plan
2. Identify characteristics of your workload
3. Sign up and create a dedicated cluster for the PoC
4. Adapt your schemas and SQL
5. Import data
6. Run your workload and evaluate results
7. Explore more features
8. Clean up the environment and finish the PoC

## Step 1. Define success criteria and create a test plan

When evaluating TiDB Cloud through a PoC, it is recommended to decide your points of interest and the corresponding technical evaluation criteria based on your business needs, and then clarify your expectations and goals for the PoC. Clear and measurable technical criteria with a detailed test plan can help you focus on the key aspects, cover the business level requirements, and ultimately get answers through the PoC procedures.

Use the following questions to help identify the goals of your PoC:

- What is the scenario of your workload?
- What is the dataset size or workload of your business? What is the growth rate?
- What are the performance requirements, including the business-critical throughput or latency requirements?
- What are the availability and stability requirements, including the minimum acceptable planned or unplanned downtime?
- What are the necessary metrics for operational efficiency? How do you measure them?
- What are the security and compliance requirements for your workload?

For more information about the success criteria and how to create a test plan, feel free to contact <a href="mailto:tidbcloud-support@pingcap.com">PingCAP</a>.

## Step 2. Identify characteristics of your workload

TiDB Cloud is suitable for various use cases that require high availability and strong consistency with a large volume of data. [TiDB Introduction](https://docs.pingcap.com/tidb/stable/overview) lists the key features and scenarios. You can check whether they apply to your business scenarios:

- Horizontally scaling out or scaling in
- Financial-grade high availability
- Real-time HTAP
- Compatible with the MySQL 5.7 protocol and MySQL ecosystem

You might also be interested in using [TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview), a columnar storage engine that helps speed up analytical processing. During the PoC, you can use the TiFlash feature at any time.

## Step 3. Sign up and create a dedicated cluster for the PoC

To create a dedicated cluster for the PoC, take the following steps:

1. Fill in the PoC application form by doing one of the following:

    - On the PingCAP website, go to the [Apply for PoC](https://pingcap.com/apply-for-poc/) page to fill in the application form.
    - In the [TiDB Cloud console](https://tidbcloud.com/), click <MDSvgIcon name="icon-top-contact-us" /> **Contact Us** in the upper-right corner, and select **Apply for PoC** to fill in the application form.

    Once you submit the form, the TiDB Cloud Support team will review your application, contact you, and transfer credits to your account once the application is approved. You can also contact a PingCAP support engineer to assist with your PoC procedures to ensure the PoC runs as smoothly as possible.

2. Refer to [Quick Start](/tidb-cloud/tidb-cloud-quickstart.md) to create a [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier) cluster for the PoC.

Capacity planning is recommended for cluster sizing before you create a cluster. You can start with estimated numbers of TiDB, TiKV, or TiFlash nodes, and scale out the cluster later to meet performance requirements. You can find more details in the following documents or consult our support team.

- For more information about estimation practice, see [Size Your TiDB](/tidb-cloud/size-your-cluster.md).
- For configurations of the dedicated cluster, see [Create a TiDB Cluster](/tidb-cloud/create-tidb-cluster.md). Configure the cluster size for TiDB, TiKV, and TiFlash (optional) respectively.
- For how to plan and optimize your PoC credits consumption effectively, see [FAQ](#faq) in this document.
- For more information about scaling, see [Scale Your TiDB Cluster](/tidb-cloud/scale-tidb-cluster.md).

Once a dedicated PoC cluster is created, you are ready to load data and perform a series of tests. For how to connect to a TiDB cluster, see [Connect to Your TiDB Cluster](/tidb-cloud/connect-to-tidb-cluster.md).

For a newly created cluster, note the following configurations:

- The default time zone (the **Create Time** column on the Dashboard) is UTC. You can change it to your local time zone by following [Set the Local Time Zone](/tidb-cloud/manage-user-access.md#set-the-time-zone-for-your-organization).
- The default backup setting on a new cluster is full database backup on a daily basis. You can specify a preferred backup time or back up data manually. For the default backup time and more details, see [Back up and Restore TiDB Cluster Data](/tidb-cloud/backup-and-restore.md#backup).

## Step 4. Adapt your schemas and SQL

Next, you can load your database schemas to the TiDB cluster, including tables and indexes.

Because the amount of PoC credits is limited, to maximize the value of credits, it is recommended that you create a [Serverless Tier cluster](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta) (one-year free trial) for compatibility tests and preliminary analysis on TiDB Cloud.

TiDB Cloud is highly compatible with MySQL 5.7. You can directly import your data into TiDB if it is MySQL-compatible or can be adapted to be compatible with MySQL.

For more information about compatibilities, see the following documents:

- [TiDB compatibility with MySQL](https://docs.pingcap.com/tidb/stable/mysql-compatibility).
- [TiDB features that are different from MySQL](https://docs.pingcap.com/tidb/stable/mysql-compatibility#features-that-are-different-from-mysql).
- [TiDB's Keywords and Reserved Words](https://docs.pingcap.com/tidb/stable/keywords).
- [TiDB Limitations](https://docs.pingcap.com/tidb/stable/tidb-limitations).

Here are some best practices:

- Check whether there are inefficiencies in schema setup.
- Remove unnecessary indexes.
- Plan the partitioning policy for effective partitioning.
- Avoid [hotspot issues](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#identify-hotspot-issues) caused by Right-Hand-Side Index Growth, for example, indexes on the timestamp.
- Avoid [hotspot issues](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#identify-hotspot-issues) by using [SHARD_ROW_ID_BITS](https://docs.pingcap.com/tidb/stable/shard-row-id-bits) and [AUTO_RANDOM](https://docs.pingcap.com/tidb/stable/auto-random).

For SQL statements, you might need to adapt them depending on the level of your data source's compatibility with TiDB.

If you have any questions, contact [PingCAP](/tidb-cloud/tidb-cloud-support.md) for consultation.

## Step 5. Import data

You can import a small dataset to quickly test feasibility, or a large dataset to test the throughput of TiDB data migration tools. Although TiDB provides sample data, it is strongly recommended to perform a test with real workloads from your business.

You can import data in various formats to TiDB Cloud:

- [Import sample data in the SQL file format](/tidb-cloud/import-sample-data.md)
- [Migrate from Amazon Aurora MySQL](/tidb-cloud/migrate-from-aurora-bulk-import.md)
- [Import CSV Files from Amazon S3 or GCS](/tidb-cloud/import-csv-files.md)
- [Import Apache Parquet Files](/tidb-cloud/import-parquet-files.md)

> **Note:**
>
> - For information about character collations supported by TiDB Cloud, see [Migrate from MySQL-Compatible Databases](/tidb-cloud/migrate-data-into-tidb.md). Understanding how your data is stored originally will be very helpful.
> - Data import on the **Data Import** page does not generate additional billing fees.

## Step 6. Run your workload and evaluate results

Now you have created the environment, adapted the schemas, and imported data. It is time to test your workload.

Before testing the workload, consider performing a manual backup, so that you can restore the database to its original state if needed. For more information, see [Back up and Restore TiDB Cluster Data](/tidb-cloud/backup-and-restore.md#backup).

After kicking off the workload, you can observe the system using the following methods:

- The commonly used metrics of the cluster can be found on the cluster overview page, including Total QPS, Latency, Connections, TiFlash Request QPS, TiFlash Request Duration, TiFlash Storage Size, TiKV Storage Size, TiDB CPU, TiKV CPU, TiKV IO Read, and TiKV IO Write. See [Monitor a TiDB Cluster](/tidb-cloud/monitor-tidb-cluster.md).
- Go to **Diagnosis > Statements**, where you can observe SQL execution and easily locate performance problems without querying the system tables. See [Statement Analysis](/tidb-cloud/tune-performance.md).
- Go to **Diagnosis > Key Visualizer**, where you can view TiDB data access patterns and data hotspots. See [Key Visualizer](/tidb-cloud/tune-performance.md#key-visualizer).
- You can also integrate these metrics to your own Datadog and Prometheus. See [Third-Party Monitoring Integrations](/tidb-cloud/third-party-monitoring-integrations.md).

Now it is time for evaluating the test results.

To get a more accurate evaluation, determine the metrics baseline before the test, and record the test results properly for each run. By analyzing the results, you can decide whether TiDB Cloud is a good fit for your application. Meanwhile, these results indicate the running status of the system, and you can adjust the system according to the metrics. For example:

- Evaluate whether the system performance meets your requirements. Check the total QPS and latency. If the system performance is not satisfactory, you can tune performance as follows:

    - Monitor and optimize the network latency.
    - Investigate and tune the SQL performance.
    - Monitor and [resolve hotspot issues](https://docs.pingcap.com/tidb/dev/troubleshoot-hot-spot-issues#troubleshoot-hotspot-issues).

- Evaluate the storage size and CPU usage rate, and scale out or scale in the TiDB cluster accordingly. Refer to the [FAQ](#faq) section for scaling details.

The following are tips for performance tuning:

- Improve write performance

    - Increase the write throughput by scaling out the TiDB clusters (see [Scale a TiDB Cluster](/tidb-cloud/scale-tidb-cluster.md)).
    - Reduce lock conflicts by using the [optimistic transaction model](https://docs.pingcap.com/tidb/stable/optimistic-transaction#tidb-optimistic-transaction-model).

- Improve query performance

    - Check the SQL execution plan on the **Diagnostic > Statements** page.
    - Check hotspot issues on the **Dashboard > Key Visualizer** page.
    - Monitor if the TiDB cluster is running out of capacity on the **Overview > Capacity Metrics** page.
    - Use the TiFlash feature to optimize analytical processing. See [Use an HTAP Cluster](/tiflash/tiflash-overview.md).

## Step 7. Explore more features

Now the workload testing is finished, you can explore more features, for example, upgrade and backup.

- Upgrade

    TiDB Cloud regularly upgrades the TiDB clusters, while you can also submit a support ticket to request an upgrade to your clusters. See [Upgrade a TiDB Cluster](/tidb-cloud/upgrade-tidb-cluster.md).

- Backup

    To avoid vendor lock-in, you can use daily full backup to migrate data to a new cluster and use [Dumpling](/dumpling-overview.md) to export data. For more information, see [Export Data from TiDB](/tidb-cloud/export-data-from-tidb-cloud.md).

## Step 8. Clean up the environment and finish the PoC

You have completed the full cycle of a PoC after you test TiDB Cloud using real workloads and get the testing results. These results help you determine if TiDB Cloud meets your expectations. Meanwhile, you have accumulated best practices for using TiDB Cloud.

If you want to try TiDB Cloud on a larger scale, for a new round of deployments and tests, such as deploying with other node storage sizes offered by TiDB Cloud, get full access to TiDB Cloud by creating a [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier).

If your credits are running out and you want to continue with the PoC, contact the [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) for consultation.

You can end the PoC and remove the test environment anytime. For more information, see [Delete a TiDB Cluster](/tidb-cloud/delete-tidb-cluster.md).

Any feedback to our support team is highly appreciated by filling in the [TiDB Cloud Feedback form](https://www.surveymonkey.com/r/L3VVW8R), such as the PoC process, the feature requests, and how we can improve the products.

## FAQ

### 1. How long does it take to back up and restore my data?

TiDB Cloud provides two types of database backup: automatic backup and manual backup. Both methods back up the full database.

The time it takes to back up and restore data might vary, depending on the number of tables, the number of mirror copies, and the CPU-intensive level. The backup and restoring rate in one single TiKV node is approximately 50 MB/s.

Database backup and restore operations are typically CPU-intensive, and always require additional CPU resources. They might have an impact (10% to 50%) on QPS and transaction latency, depending on how CPU-intensive this environment is.

### 2. When do I need to scale out and scale in?

The following are some considerations about scaling:

- During peak hours or data import, if you observe that the capacity metrics on the dashboard have reached the upper limits (see [Monitor a TiDB Cluster](/tidb-cloud/monitor-tidb-cluster.md)), you might need to scale out the cluster.
- If you observe that the resource usage is persistently low, for example, only 10%-20% of CPU usage, you can scale in the cluster to save resources.

You can scale out clusters on the console by yourself. If you need to scale in a cluster, you need to contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) for help. For more information about scaling, see [Scale Your TiDB Cluster](/tidb-cloud/scale-tidb-cluster.md). You can keep in touch with the support team to track the exact progress. You must wait for the scaling operation to finish before starting your test because it can impact the performance due to data rebalancing.

### 3. How to make the best use of my PoC credits?

Once your application for the PoC is approved, you will receive credits in your account. Generally, the credits are sufficient for a 14-day PoC. The credits are charged by the type of nodes and the number of nodes, on an hourly basis. For more information, see [TiDB Cloud Billing](/tidb-cloud/tidb-cloud-billing.md#credits).

To check the credits left for your PoC, go to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your target project, as shown in the following screenshot.

![TiDB Cloud PoC Credits](/media/tidb-cloud/poc-points.png)

Alternatively, you can also click <MDSvgIcon name="icon-top-account-settings" /> **Account** in the upper-right corner of the TiDB Cloud console, click **Billing**, and click **Credits** to see the credit details page.

To save credits, remove the cluster that you are not using. Currently, you cannot stop a cluster. You need to ensure that your backups are up to date before removing a cluster, so you can restore the cluster later when you want to resume your PoC.

If you still have unused credits after your PoC process is completed, you can continue using the credits to pay TiDB cluster fees as long as these credits are not expired.

### 4. Can I take more than 2 weeks to complete a PoC?

If you want to extend the PoC trial period or are running out of credits, [contact PingCAP](https://www.pingcap.com/contact-us/) for help.

### 5. I'm stuck with a technical problem. How do I get help for my PoC?

You can always [contact TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) for help.
