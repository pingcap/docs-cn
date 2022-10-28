---
title: TiDB Cloud Release Notes in 2022
summary: Learn about the release notes of TiDB Cloud in 2022.
aliases: ['/tidbcloud/beta/supported-tidb-versions','/tidbcloud/release-notes']
---

# TiDB Cloud Release Notes in 2022

This page lists the release notes of [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) in 2022.

## October 28, 2022

* Developer Tier is upgraded to [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier). Serverless Tier, a fully-managed, auto-scaling deployment of TiDB, is now available. It is still in beta and free to use.

    * A Serverless Tier cluster still contains fully functional HTAP ability as Dedicated Tier clusters.
    * Serverless Tier offers you faster cluster creation time and instantaneous cold start time. Compared with Developer Tier, the creation time reduces from minutes to seconds.
    * You do not need to worry about deployment topology. Serverless Tier will adjust automatically according to your requests.
    * Serverless Tier [enforces TLS connection to clusters for the sake of security](/tidb-cloud/secure-connections-to-serverless-tier-clusters.md).
    * Existing Developer Tier clusters will be automatically migrated to Serverless Tier in the coming months. Your ability to use your cluster should not be affected, and you will not be charged for the use of your Serverless Tier cluster in beta.

  Get started [here](/tidb-cloud/tidb-cloud-quickstart.md).

## October 25, 2022

**General changes**

- Support dynamically changing and persisting a subset of TiDB system variables (beta).

    You can use the standard SQL statement to set a new value for a supported system variable.

    ```sql
    SET [GLOBAL|SESSION] <variable>
    ```

    For example:

    ```sql
    SET GLOBAL tidb_committer_concurrency = 127;
    ```

    If a variable is set at the `GLOBAL` level, the variable will be applied to the cluster and persistent (keep effective even after you restart or reload the server). A variable at the `SESSION` level is not persistent and is only effective in the current session.

    **This feature is still in beta**, and only a limited number of variables are supported. It is not recommended to modify other [system variables](/system-variables.md) due to uncertainty of the side effects. See the following list for all supported variables based on TiDB v6.1:

    - [`require_secure_transport`](/system-variables.md#require_secure_transport-new-in-v610)
    - [`tidb_committer_concurrency`](/system-variables.md#tidb_committer_concurrency-new-in-v610)
    - [`tidb_enable_batch_dml`](/system-variables.md#tidb_enable_batch_dml)
    - [`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610)
    - [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610)
    - [`tidb_mem_oom_action`](/system-variables.md#tidb_mem_oom_action-new-in-v610)
    - [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)
    - [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-new-in-v610)
    - [`tidb_query_log_max_len`](/system-variables.md#tidb_query_log_max_len)

- Upgrade the default TiDB version of new [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier) clusters from [v6.1.1](https://docs.pingcap.com/tidb/stable/release-6.1.1) to [v6.1.2](https://docs.pingcap.com/tidb/stable/release-6.1.2).

## October 19, 2022

**Integration changes**

* Publish [TiDB Cloud Vercel Integration](https://vercel.com/integrations/tidb-cloud) in [Vercel Integration Marketplace](https://vercel.com/integrations#databases).

    [Vercel](https://vercel.com) is the platform for frontend developers, providing the speed and reliability innovators need to create at the moment of inspiration. Using TiDB Cloud Vercel Integration, you can easily connect your Vercel projects to TiDB Cloud clusters. For details, see the document [Integrate TiDB Cloud with Vercel](/tidb-cloud/integrate-tidbcloud-with-vercel.md).

* Publish [TiDB Cloud Starter Template](https://vercel.com/templates/next.js/tidb-cloud-starter) in [Vercel template list](https://vercel.com/templates).

    You can use this template as a start to try out Vercel and TiDB Cloud. Before using this template, you need to [import data into your TiDB Cloud cluster](https://github.com/pingcap/tidb-prisma-vercel-demo#2-import-table-structures-and-data) first.

## October 18, 2022

**General changes**

* For Dedicated Tier clusters, the minimum storage size of a TiKV or TiFlash node is changed from 500 GiB to 200 GiB. This will be more cost-effective for users whose workloads are in small data volumes.

    For more details, see [TiKV node storage](/tidb-cloud/size-your-cluster.md#tikv-node-storage) and [TiFlash node storage](/tidb-cloud/size-your-cluster.md#tiflash-node-storage).

* Introduce online contracts to customize TiDB Cloud subscriptions and meet compliance requirements.

    A [**Contract** tab](/tidb-cloud/tidb-cloud-billing.md#contract) is added to the **Billing** page of the TiDB Cloud console. If you have agreed with our sales on a contract and received an email to process the contract online, you can go to the **Contract** tab to review and accept the contract. To learn more about contracts, feel free to [contact our sales](https://www.pingcap.com/contact-us/).

**Documentation changes**

* Add [documentation](/tidb-cloud/terraform-tidbcloud-provider-overview.md) for [TiDB Cloud Terraform Provider](https://registry.terraform.io/providers/tidbcloud/tidbcloud).

    TiDB Cloud Terraform Provider is a plugin that allows you to use [Terraform](https://www.terraform.io/) to manage TiDB Cloud resources, such as clusters, backups, and restores. If you are looking for a simple way to automate resource provisioning and your infrastructure workflow, you can try out TiDB Cloud Terraform Provider according to the [documentation](/tidb-cloud/terraform-tidbcloud-provider-overview.md).

## October 11, 2022

**General changes**

* Upgrade the default TiDB version of new [Developer Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier) clusters from [v6.2.0](https://docs.pingcap.com/tidb/v6.2/release-6.2.0) to [v6.3.0](https://docs.pingcap.com/tidb/v6.3/release-6.3.0).

**Console changes**

* Optimize billing information on the [billing details page](/tidb-cloud/tidb-cloud-billing.md#billing-details):

    * Provide more fine-grained billing information at the node level in the **Summary By Service** section.
    * Add a **Usage Details** section. You can also download usage details as a CSV file.

## September 27, 2022

**General changes**

* Support joining multiple organizations by invitation.

    In the TiDB Cloud console, you can view all organizations you have joined and switch between them. For details, see [Switch between organizations](/tidb-cloud/manage-user-access.md#switch-between-organizations).

* Add the [Slow Query](/tidb-cloud/tune-performance.md#slow-query) page for SQL diagnosis.

    On the Slow Query page, you can search and view all slow queries in your TiDB cluster, and explore the bottlenecks of each slow query by viewing its [execution plan](https://docs.pingcap.com/tidbcloud/explain-overview), SQL execution information, and other details.

* When you reset the password for your account, TiDB Cloud will check your new password input against your last four passwords, and remind you to avoid using any of them. Any of the four used passwords will not be permitted.

    For details, see [Manage user passwords](/tidb-cloud/manage-user-access.md#manage-user-passwords).

## September 20, 2022

**General changes**

* Introduce the [cost quota-based invoice](/tidb-cloud/tidb-cloud-billing.md#invoices) for self-service users.

    TiDB Cloud will generate an invoice once your cost reaches a quota. To raise the quota or to receive invoices per month, contact [our sales](https://www.pingcap.com/contact-us/).

* Exempt the storage operation fee from the Data Backup Cost. See [TiDB Cloud Pricing Details](https://www.pingcap.com/tidb-cloud-pricing-details/) for the latest pricing information.

**Console changes**

* Provide a new web UI for data import. The new UI provides better user experience and makes data import more efficient.

    Using the new UI, you can preview the data to be imported, view the import process, and manage all import tasks easily.

**API changes**

* The TiDB Cloud API (beta) is now available to all users.

    You can start using the API by creating an API key on the TiDB Cloud console. For more information, refer to [API documentation](/tidb-cloud/api-overview.md).

## September 15, 2022

**General changes**

* Support connecting to TiDB Cloud [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier) clusters via TLS.

    For Dedicated Tier clusters, the **Standard Connection** tab in the [Connect](/tidb-cloud/connect-to-tidb-cluster.md#connect-via-standard-connection) dialog now provides a link to download the TiDB cluster CA and also provides the connection string and sample code for TLS connection. You can [connect to your Dedicated Tier cluster via TLS](/tidb-cloud/connect-to-tidb-cluster.md#connect-via-standard-connection) using third-party MySQL clients, MyCLI, and multiple connection methods for your applications, such as JDBC, Python, Go, and Node.js. This feature ensures the security of data transmission from your applications to TiDB clusters.

## September 14, 2022

**Console changes**

* Optimize the UI of the [Clusters](https://tidbcloud.com/console/clusters) page and the cluster overview page for better user experience.

    In the new design, the entrances of upgrade to Dedicated Tier, cluster connection, and data import are highlighted.

* Introduce Playground for [Developer Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier) clusters.

    Playground contains a pre-loaded dataset of GitHub events, which allows you to get started with TiDB Cloud by running queries instantly, without importing your data or connecting to a client.

## September 13, 2022

**General changes**

* Support a new Google Cloud region for [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier) clusters: `N. Virginia (us-east4)`.

## September 9, 2022

**General changes**

* Provide [more metrics](/tidb-cloud/monitor-datadog-integration.md#metrics-available-to-datadog) of Dedicated Tier clusters in Datadog to help you better understand the cluster performance status.

    If you have [integrated TiDB Cloud with Datadog](/tidb-cloud/monitor-datadog-integration.md), you can view these metrics in your Datadog dashboards directly.

## September 6, 2022

**General changes**

* Upgrade the default TiDB version of new [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier) clusters from [v6.1.0](https://docs.pingcap.com/tidb/stable/release-6.1.0) to [v6.1.1](https://docs.pingcap.com/tidb/stable/release-6.1.1).

**Console changes**

* Now you can [apply for a PoC](/tidb-cloud/tidb-cloud-poc.md) from the entry in the upper-right corner of the TiDB Cloud console.

**API changes**

* Support increasing the storage of a TiKV or TiFlash node through the [TiDB Cloud API](/tidb-cloud/api-overview.md). You can use the `storage_size_gib` field of the API endpoint to do the scaling.

    Currently, TiDB Cloud API is still in beta and only available upon request.

    For details, see [Modify a Dedicated Tier cluster](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster).

## August 30, 2022

**General changes**

* Support AWS PrivateLink-powered endpoint connection as a new network access management option for TiDB Cloud [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier) clusters.

    The endpoint connection is secure and private, and does not expose your data to the public internet. In addition, the endpoint connection supports CIDR overlap and is easier for network management.

    For more information, see [Set Up Private Endpoint Connections](/tidb-cloud/set-up-private-endpoint-connections.md).

**Console changes**

* Provide sample connection strings of MySQL, MyCLI, JDBC, Python, Go, and Node.js in the **VPC Peering** tab and **Private Endpoint** tab of the [Connect](/tidb-cloud/connect-to-tidb-cluster.md) dialog for [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier) clusters.

    You can easily connect to your Dedicated Tier cluster by simply copying and pasting the connection codes to your apps.

## August 24, 2022

**General changes**

* Support pausing or resuming a Dedicated Tier cluster.

    You can [pause or resume your Dedicated Tier cluster](/tidb-cloud/pause-or-resume-tidb-cluster.md) in TiDB Cloud. When a cluster is paused, Node Compute Cost will not be charged.

## August 23, 2022

**General changes**

* Upgrade the default TiDB version of new [Developer Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier) clusters from [v6.1.0](https://docs.pingcap.com/tidb/stable/release-6.1.0) to [v6.2.0](https://docs.pingcap.com/tidb/v6.2/release-6.2.0).

**API changes**

* Introduce TiDB Cloud API as beta.

    Through this API, you can manage TiDB Cloud resources such as clusters automatically and efficiently. For more information, see [TiDB Cloud API Documentation](https://docs.pingcap.com/tidbcloud/api/v1beta).

    Currently, TiDB Cloud API is still in beta and only available upon request. You can apply for API access by submitting a request:

    * Click **Help** in the lower-right corner of [TiDB Cloud console](https://tidbcloud.com/console/clusters).
    * In the dialog, fill in "Apply for TiDB Cloud API" in the **Description** field and click **Send**.

## August 16, 2022

* Add `2 vCPU, 8 GiB (Beta)` node size of TiDB and TiKV as beta.

    * For each `2 vCPU, 8 GiB (Beta)` TiKV node, the storage size is between 200 GiB and 500 GiB.

    * Suggested usage scenarios:

        * Low-workload production environments for SMB
        * PoC and staging environments
        * Development environments

* Introduce [Credits](/tidb-cloud/tidb-cloud-billing.md#credits) (previously named as trail points) for PoC users.

    You can now view information about your organization's credits on the **Credits** tab of the **Billing** page, the credits can be used to pay for TiDB Cloud fees. You can [contact us](https://en.pingcap.com/apply-for-poc/) to get credits.

## August 9, 2022

* Add the support of the GCP region `Osaka` for [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier) cluster creation.

## August 2, 2022

* The `4 vCPU, 16 GiB` node size of TiDB and TiKV is now in General Availability (GA).

    * For each `4 vCPU, 16 GiB` TiKV node, the storage size is between 200 GiB and 2 TiB.
    * Suggested usage scenarios:

        * Low workload production environments for SMB
        * PoC and staging environments
        * Development environments

* Add a [Monitoring page](/tidb-cloud/built-in-monitoring.md) to the **Diagnosis** tab for [Dedicated Tier clusters](/tidb-cloud/select-cluster-tier.md#dedicated-tier).

    The Monitoring page provides a system-level entry for overall performance diagnosis. According to the top-down performance analysis methodology, the Monitoring page organizes TiDB performance metrics based on database time breakdown and displays these metrics in different colors. By checking these colors, you can identify performance bottlenecks of the entire system at the first glance, which significantly reduces performance diagnosis time and simplifies performance analysis and diagnosis.

* Add a switch to enable or disable **Custom Pattern** on the **Data Import** page for CSV and Parquet source files.

    The **Custom Pattern** feature is disabled by default. You can enable it when you are going to import CSV or Parquet files whose filenames match a certain pattern to a single target table.

    For more information, see [Import CSV Files](/tidb-cloud/import-csv-files.md) and [Import Apache Parquet Files](/tidb-cloud/import-parquet-files.md).

* Add TiDB Cloud Support Plans (Basic, Standard, Enterprise, and Premium) to meet different support needs of customers' organizations. For more information, see [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

* Optimize the UI of the [Clusters](https://tidbcloud.com/console/clusters) page and the cluster details page:

    * Add **Connect** and **Import data** buttons to the **Clusters** page.
    * Move **Connect** and **Import data** buttons to the upper-right corner on the cluster details page.

## July 28, 2022

* Add the **Allow Access from Anywhere** button to the **Security Quick Start** dialog, which allows your cluster to be accessible by any IP addresses. For more information, see [Configure Cluster Security Settings](/tidb-cloud/configure-security-settings.md).

## July 26, 2022

* Support automatic hibernation and resuming for new [Developer Tier clusters](/tidb-cloud/select-cluster-tier.md#serverless-tier).

    A Developer Tier cluster will not be deleted after 7 days of inactivity so you can still use it at any time until the one-year free trial ends. After 24 hours of inactivity, the Developer Tier cluster will hibernate automatically. To resume the cluster, either send a new connection to the cluster or click the **Resume** button in the TiDB Cloud console. The cluster will be resumed within 50 seconds and back to service automatically.

* Add a user name prefix limitation for new [Developer Tier clusters](/tidb-cloud/select-cluster-tier.md#serverless-tier).

    Whenever you use or set a database user name, you must include the prefix for your cluster in the user name. For more information, see [User name prefix](/tidb-cloud/select-cluster-tier.md#user-name-prefix).

* Disable the backup and restore feature for [Developer Tier clusters](/tidb-cloud/select-cluster-tier.md#serverless-tier).

    The backup and restore feature (including both automatic backup and manual backup) is disabled for Developer Tier clusters. You can still use [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) to export your data as a backup.

* Increase the storage size of a [Developer Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier) cluster from 500 MiB to 1 GiB.
* Add breadcrumbs to the TiDB Cloud console to improve the navigation experience.
* Support configuring multiple filter rules when you import data into TiDB Cloud.
* Remove the **Traffic Filters** page from **Project Settings**, and remove the **Add Rules from Default Set** button from the **Connect to TiDB** dialog.

## July 19, 2022

* Provide a new option for [TiKV node size](/tidb-cloud/size-your-cluster.md#tikv-node-size): `8 vCPU, 32 GiB`. You can choose either `8 vCPU, 32 GiB` or `8 vCPU, 64 GiB` for an 8 vCPU TiKV node.
* Support syntax highlighting in sample code provided in the [**Connect to TiDB**](/tidb-cloud/connect-to-tidb-cluster.md#connect-via-standard-connection) dialog to improve code readability. You can easily identify the parameters that you need to replace in the sample code.
* Support automatically validating whether TiDB Cloud can access your source data after you confirm the import task on the [**Data Import Task**](/tidb-cloud/import-sample-data.md) page.
* Change the theme color of the TiDB Cloud console to make it consistent with that of [PingCAP website](https://en.pingcap.com/).

## July 12, 2022

* Add the **Validate** button to the [**Data Import Task**](/tidb-cloud/import-sample-data.md) page for Amazon S3, which helps you detect data access issues before the data import starts.
* Add **Billing Profile** under the [**Payment Method**](/tidb-cloud/tidb-cloud-billing.md#payment-method) tab. By providing your tax registration number in **Billing Profile**, certain taxes might be exempted from your invoice. For more information, see [Edit billing profile information](/tidb-cloud/tidb-cloud-billing.md#edit-billing-profile-information).

## July 05, 2022

* The columnar storage [TiFlash](/tiflash/tiflash-overview.md) is now in General Availability (GA).

    - TiFlash makes TiDB essentially an Hybrid Transactional/Analytical Processing (HTAP) database. Your application data is first stored in TiKV and then replicated to TiFlash via the Raft consensus algorithm. So it is real time replication from the row storage to the columnar storage.
    - For tables with TiFlash replicas, the TiDB optimizer automatically determines whether to use either TiKV or TiFlash replicas based on the cost estimation.

    To experience the benefits brought by TiFlash, see [TiDB Cloud HTAP Quick Start Guide](/tidb-cloud/tidb-cloud-htap-quickstart.md).

* Support [increasing the storage size](/tidb-cloud/scale-tidb-cluster.md#increase-node-storage) of TiKV and TiFlash for a Dedicated Tier cluster.
* Support showing the memory information in the node size field.

## June 28, 2022

* Upgrade TiDB Cloud Dedicated Tier from [TiDB v5.4.1](https://docs.pingcap.com/tidb/stable/release-5.4.1) to [TiDB v6.1.0](https://docs.pingcap.com/tidb/stable/release-6.1.0).

## June 23, 2022

* Increase the maximum [storage capacity of TiKV](/tidb-cloud/size-your-cluster.md#tikv-node-storage) on TiDB Cloud.

    * 8 vCPU or 16 vCPU TiKV: support up to 4 TiB storage capacity.
    * 4 vCPU TiKV: support up to 2 TiB storage capacity.

## June 21, 2022

* Add the support of the GCP region `Taiwan` for [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier) cluster creation.
* Support [updating user profiles](/tidb-cloud/manage-user-access.md#manage-user-profiles) on the TiDB Cloud console, including first name, last time, company name, country, and phone number.
* Provide the connection strings for MySQL, MyCLI, JDBC, Python, Go, and Node.js in the [**Connect to TiDB**](/tidb-cloud/connect-to-tidb-cluster.md#connect-via-standard-connection) dialog so you can easily connect to your TiDB cluster.
* Support obtaining bucket regions from bucket URIs automatically during data import to save your effort to fill in such information.

## June 16, 2022

* Simplify the [cluster creation process](/tidb-cloud/create-tidb-cluster.md).

    - When you create a cluster, TiDB Cloud provides a default cluster name. You can either use the default name or update it.
    - When you create a cluster, you do not need to set the password on the **Create a Cluster** page.
    - During or after the cluster creation, you can set the root password to access the cluster and also the IP addresses to connect to the cluster in the **Security Quick Start** dialog box.

## June 14, 2022

* Upgrade TiDB Cloud to [TiDB v6.1.0](https://docs.pingcap.com/tidb/stable/release-6.1.0) for Developer Tier.
* Optimize the entrance of **Project Settings**. From the TiDB Cloud console, you can choose a target project and go to its settings easily by clicking the **Project Settings** tab.
* Optimize the experience of password expiration by providing expiration messages in the TiDB Cloud console.

## June 7, 2022

* Add the [Try Free](https://tidbcloud.com/free-trial) registration page to quickly sign up for TiDB Cloud.
* Remove the **Proof of Concept plan** option from the plan selection page. If you want to apply for a 14-day PoC trial for free, go to the [Apply for PoC](https://en.pingcap.com/apply-for-poc/) page. For more information, see [Perform a Proof of Concept (PoC) with TiDB Cloud](/tidb-cloud/tidb-cloud-poc.md).
* Improve the system security by prompting users who sign up for TiDB Cloud with emails and passwords to reset their passwords every 90 days. For more information, see [Manage user passwords](/tidb-cloud/manage-user-access.md#manage-user-passwords).

## May 24, 2022

* Support customizing TiDB port number when you [create](/tidb-cloud/create-tidb-cluster.md) or [restore](/tidb-cloud/backup-and-restore.md#restore) a Dedicated Tier cluster.

## May 19, 2022

* Add the support of the AWS region `Frankfurt` for [Developer Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier) cluster creation.

## May 18, 2022

* Support [signing up](https://tidbcloud.com/signup) TiDB Cloud with a GitHub account.

## May 13, 2022

* Support [signing up](https://tidbcloud.com/signup) TiDB Cloud with a Google account.

## May 1, 2022

* Support configuring vCPU size of TiDB, TiKV, and TiFlash when you [create](/tidb-cloud/create-tidb-cluster.md) or [restore](/tidb-cloud/backup-and-restore.md#restore) a [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier) cluster.
* Add the support of the AWS region `Mumbai` for cluster creation.
* Update the compute, storage, and data transfer cost for [TiDB Cloud billing](/tidb-cloud/tidb-cloud-billing.md).

## April 7, 2022

* Upgrade TiDB Cloud to [TiDB v6.0.0](https://docs.pingcap.com/tidb/v6.0/release-6.0.0-dmr) for Developer Tier.

## March 31, 2022

TiDB Cloud is now in General Availability. You can [sign up](https://tidbcloud.com/signup) and select one of the following options:

* Get started with [Developer Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier) for free.
* Apply for [a 14-day PoC trial for free](https://en.pingcap.com/apply-for-poc/).
* Get full access with [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier).

## March 25, 2022

New feature:

* Support [TiDB Cloud built-in alerting](/tidb-cloud/monitor-built-in-alerting.md).

    With the TiDB Cloud built-in alerting feature, you can be notified by emails whenever a TiDB Cloud cluster in your project triggers one of TiDB Cloud built-in alert conditions.

## March 15, 2022

General changes:

* No cluster tier with the fixed cluster size any more. You can customize the [cluster size](/tidb-cloud/size-your-cluster.md) of TiDB, TiKV, and TiFlash easily.
* Support adding [TiFlash](/tiflash/tiflash-overview.md) nodes for an existing cluster without TiFlash.
* Support specifying the storage size (500 to 2048 GiB) when [creating a new cluster](/tidb-cloud/create-tidb-cluster.md). The storage size cannot be changed after the cluster is created.
* Introduce a new public region: `eu-central-1`.
* Deprecate 8 vCPU TiFlash and provide 16 vCPU TiFlash.
* Separate the price of CPU and storage (both have 30% public preview discount).
* Update the [billing information](/tidb-cloud/tidb-cloud-billing.md) and the [price table](https://en.pingcap.com/tidb-cloud/#pricing).

New features:

* Support [the Prometheus and Grafana integration](/tidb-cloud/monitor-prometheus-and-grafana-integration.md).

    With the Prometheus and Grafana integration, you can configure a [Prometheus](https://prometheus.io/) service to read key metrics from the TiDB Cloud endpoint and view the metrics using [Grafana](https://grafana.com/).

* Support assigning a default backup time based on the selected region of your new cluster.

    For more information, see [Back up and Restore TiDB Cluster Data](/tidb-cloud/backup-and-restore.md).

## March 04, 2022

New feature:

* Support [the Datadog integration](/tidb-cloud/monitor-datadog-integration.md).

    With the Datadog integration, you can configure TiDB Cloud to send metric data about your TiDB clusters to [Datadog](https://www.datadoghq.com/). After that, you can view these metrics in your Datadog dashboards directly.

## February 15, 2022

General change:

* Upgrade TiDB Cloud to [TiDB v5.4.0](https://docs.pingcap.com/tidb/stable/release-5.4.0) for Developer Tier.

Improvement:

* Support using custom file names when importing [CSV files](/tidb-cloud/import-csv-files.md) or [Apache Parquet files](/tidb-cloud/import-parquet-files.md) into TiDB Cloud.

## January 11, 2022

General change:

* Upgrade TiDB Operator to [v1.2.6](https://docs.pingcap.com/tidb-in-kubernetes/stable/release-1.2.6).

Improvement:

* Add a suggested option `--connect-timeout 15` to the MySQL client on the [**Connect**](/tidb-cloud/connect-to-tidb-cluster.md#connect-via-standard-connection) page.

Bug fixes:

* Fix the issue that a user cannot create a cluster if the password contains a single quote.
* Fix the issue that even an organization only has one owner, the owner can be deleted or changed to another role.
