---
title: Serverless Tier FAQs
summary: Learn about the most frequently asked questions (FAQs) relating to TiDB Cloud Serverless Tier.
---

# Serverless Tier FAQs

<!-- markdownlint-disable MD026 -->

This document lists the most frequently asked questions about TiDB Cloud Serverless Tier.

## General FAQs

### What is Serverless Tier?

TiDB Cloud Serverless Tier offers the TiDB database with full HTAP capabilities for you and your organization. It is a fully managed, auto-scaling deployment of TiDB that lets you start using your database immediately, develop and run your application without caring about the underlying nodes, and automatically scale based on your application's workload changes.

### How do I get started with Serverless Tier?

Get started with the 5-minute [TiDB Cloud Quick Start](/tidb-cloud/tidb-cloud-quickstart.md).

### Is Serverless Tier free during beta?

Yes. Serverless Tier is free to use during the beta phase. In the coming months, we intend to offer a usage-based billing plan for additional resources and higher performance, while still keeping offering the free starter plan.

### What does it mean for beta release?

Serverless Tier is in beta while we continuously add new features and improve existing features before it becomes generally available. We do not provide SLA for beta products. Therefore, Serverless Tier should **NOT** be used in production currently.

### What are the limitations of a Serverless Tier cluster in free beta?

- For each TiDB Cloud account, you can create a maximum of five complimentary Serverless Tier clusters during the beta phase.
- Each Serverless Tier cluster has the following limitations:
    - The storage size is limited to 5 GiB (logical size) of OLTP storage and 5 GiB of OLAP storage.
    - The compute resource is limited to 1 vCPU and 1 GiB RAM.
    - The total size of a single transaction is set to no more than 10 MB on Serverless Tier during the beta phase.
    - **Note**: In the coming months, we intend to offer a usage-based billing plan for additional resources and higher performance, while still keeping offering the free starter plan. In the coming releases, the limitations of the free Serverless Tier might be changed.
- Some of TiDB Cloud features are partially supported or not supported on Serverless Tier. See [Serverless Tier Limitations](/tidb-cloud/serverless-tier-limitations.md) for details.

### What can Serverless Tier be used for?

You can use your Serverless Tier cluster for non-production workloads such as prototype applications, development environments, hackathons, and academic courses, or to provide temporary data service for your datasets.

### I created a Developer Tier cluster before Serverless Tier was available. Can I still use my cluster?

Yes, your free Developer Tier cluster will be automatically migrated to the Serverless Tier cluster soon. Your ability to use your cluster should not be affected, and you will have the same improved Serverless Tier user experiences.

## Security FAQs

### Is my Serverless Tier shared or dedicated?

The serverless technology is designed for multi-tenancy and the resources used by all clusters are shared. To get managed TiDB service with isolated infrastructure and resources, you can upgrade it to the [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier).

### How does TiDB Serverless Tier ensure security?

- Your connections are encrypted by Transport Layer Security (TLS). For more information about using TLS to connect to Serverless Tier, see [Secure Connections to Serverless Tier Clusters](/tidb-cloud/secure-connections-to-serverless-tier-clusters.md).
- All persisted data on Serverless Tier is encrypted-at-rest using the tool of the cloud provider that your cluster is running in.

## Maintenance FAQ

### Can I upgrade the version of TiDB that my cluster is running on?

No. Serverless Tier clusters are upgraded automatically as we roll out new TiDB versions on TiDB Cloud. You can see what version of TiDB your cluster is running in the [TiDB Cloud console](https://tidbcloud.com/console/clusters) or in the latest [release note](https://docs.pingcap.com/tidbcloud/tidb-cloud-release-notes). Alternatively, you can also connect to your cluster and use `SELECT version()` or `SELECT tidb_version()` to check the TiDB version.
