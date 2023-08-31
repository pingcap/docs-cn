---
title: TiDB Cloud Roadmap
summary: Learn about TiDB Cloud's roadmap for the next few months. See the new features or improvements in advance, follow the progress, learn about the key milestones on the way.
---

# TiDB Cloud Roadmap

The TiDB Cloud roadmap brings you what's coming in the near future, so you can see the new features or improvements in advance, follow the progress, and learn about the key milestones on the way. In the course of development, this roadmap is subject to change based on user needs, feedback, and our assessment.

✅: The feature or improvement is already available in TiDB Cloud.

> **Safe harbor statement:**
>
> Any unreleased features discussed or referenced in our documents, roadmaps, blogs, websites, press releases, or public statements that are not currently available ("unreleased features") are subject to change at our discretion and may not be delivered as planned or at all. Customers acknowledge that purchase decisions are solely based on features and functions that are currently available, and that PingCAP is not obliged to deliver aforementioned unreleased features as part of the contractual agreement unless otherwise stated.

## Developer experience and enterprise-grade features

<table>
<thead>
  <tr>
    <th>Domain</th>
    <th>Feature</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td rowspan="3">Developer experience</td>
    <td>✅ Load sample datasets manually.</td>
    <td>Support loading sample datasets into a cluster. You can use this data to quickly get started with testing the features of TiDB Cloud.</td>
  </tr>
  <tr>
    <td>✅ Add Chat2Query (an AI-powered SQL editor).</td>
    <td>In Chat2Query, you can either let AI generate SQL queries automatically or write SQL queries manually, and run SQL queries against databases without a terminal.</td>
  </tr>
  <tr>
    <td>✅ Support Data Service.</td>
    <td>With Data Service (beta), you can read or write TiDB Cloud data via an HTTPS request using a custom API endpoint.</td>
  </tr>
  <tr>
    <td>Cloud provider marketplace</td>
    <td>✅ Improve the user experience from AWS Marketplace and Google Cloud Marketplace.</td>
    <td>Improve the user journey and experience of users who sign up from AWS Marketplace and Google Cloud Marketplace.</td>
  </tr>
  <tr>
    <td rowspan="2">Enterprise-grade features</td>
    <td>✅ Manage users in multiple organizations.</td>
    <td>Allow a user to join multiple organizations by accepting the invitations.</td>
  </tr>
  <tr>
    <td>✅ Support hierarchical user roles and permissions.</td>
    <td>Support role-based access control (RBAC) for the TiDB Cloud console. You can manage user permissions in a fine-grained manner, such as by cluster, billing, and member.</td>
  </tr>
  <tr>
    <td rowspan="3">UI experience</td>
    <td>✅ Provide a more convenient feedback channel.</td>
    <td>Users can quickly get help with and give feedback on the product.</td>
  </tr>
  <tr>
    <td>✅ Add left navigation.</td>
    <td>Present the TiDB Cloud console in the structure of organizations, projects, and users to simplify the layout logic and improve user experience.</td>
  </tr>
  <tr>
    <td>Optimize Playground.</td>
    <td>Deliver context-driven tutorials to facilitate a deeper understanding of TiDB and TiDB Cloud for our users.</td>
  </tr>
</tbody>
</table>

## TiDB kernel

For the roadmap of TiDB kernel, refer to [TiDB Roadmap](https://docs.pingcap.com/tidb/dev/tidb-roadmap).

## Diagnosis and maintenance

<table>
<thead>
  <tr>
    <th>Domain</th>
    <th>Feature</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td rowspan="3">Self-service cluster analysis and diagnosis using reports</td>
    <td>✅ Cluster health report.</td>
    <td>Provide diagnosis and analysis reports for several different usage scenarios.</td>
  </tr>
  <tr>
    <td>✅ Cluster status comparison report.</td>
    <td>Locate cluster failures for some scenarios and provide recommended solutions.</td>
  </tr>
  <tr>
    <td>✅ Cluster system check report.</td>
    <td>Provide cluster key status summary for some scenarios.</td>
  </tr>
  <tr>
    <td rowspan="2">SQL tuning for HTAP workloads</td>
    <td>Provide suggestions on optimizing SQL for TiFlash and TiKV in HTAP workloads.</td>
    <td>Provide a dashboard that displays a SQL execution overview from the perspective of applications in HTAP workloads.</td>
  </tr>
  <tr>
    <td>Provide SQL execution information from the perspective of applications.</td>
    <td>For one or several HTAP scenarios, provide suggestions on SQL optimization.</td>
  </tr>
  <tr>
    <td rowspan="3">Cluster diagnosis data accessibility </td>
    <td>✅ Access diagnosis data online in real time.</td>
    <td>Integrate with various monitoring and diagnosis systems to improve the real-time data access capability.</td>
  </tr>
  <tr>
    <td>✅ Access diagnosis data offline.</td>
    <td>Provide offline data access for large-scale diagnosis, analysis, and tuning.</td>
  </tr>
  <tr>
    <td>Build logic for data reconstruction.</td>
    <td>Improve data stability and build logic for data reconstruction.</td>
  </tr>
  <tr>
    <td>TiDB Cloud service tracing</td>
    <td>Build the monitoring links for each component of TiDB Cloud service.</td>
    <td>
      <ul><li>Build the tracing links for each component of TiDB Cloud service in user scenarios.</li>
      <li>Provide assessment on service availability from the perspective of users.</li></ul>
    </td>
  </tr>
</tbody>
</table>

## Data backup and migration

<table>
<thead>
  <tr>
    <th>Domain</th>
    <th>Feature</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>Data replication to Kafka/MySQL</td>
    <td>✅ TiDB Cloud supports replicating data to Kafka/MySQL.</td>
    <td>TiDB Cloud supports TiCDC-based data replication to Kafka and MySQL compatible databases.</td>
  </tr>
  <tr>
    <td>Backup and Restore</td>
    <td>✅ Support EBS snapshot-based backup and restore.</td>
    <td>BR service on TiDB Cloud uses EBS snapshot-based backup and restore.</td>
  </tr>
  <tr>
    <td>Backup and restore</td>
    <td>Backup and restore service based on AWS EBS or Google Cloud persistent disk snapshots.</td>
    <td>Provide backup and restore service on the cloud based on AWS EBS or Google Cloud persistent disk snapshots.</td>
  </tr>
  <tr>
    <td rowspan="2">Online data migration</td>
    <td>✅ Support full data migration from Amazon Relational Database Service (RDS).</td>
    <td>Full data migration from RDS to TiDB Cloud.</td>
  </tr>
  <tr>
    <td>Support incremental data migration from RDS.</td>
    <td>Full and incremental data migration from MySQL services such as Amazon RDS and Aurora to TiDB Cloud.</td>
  </tr>
</tbody>
</table>

## Security

<table>
<thead>
  <tr>
    <th>Domain</th>
    <th>Feature</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>TLS rotation</td>
    <td>Support TLS rotation for TiDB clusters.</td>
    <td>Support internal TLS rotation settings and automatic updates in TiDB clusters.</td>
  </tr>
  <tr>
    <td>Data Encryption</td>
    <td>Enablement of customer-managed encryption keys.</td>
    <td>Allow customers to use their own KMS encryption keys on TiDB Cloud.</td>
  </tr>
  <tr>
    <td>Database audit logging</td>
    <td>✅ Enhance the database audit logging.</td>
    <td>Enhance the ability of database audit logging.</td>
  </tr>
  <tr>
    <td>Console audit logging</td>
    <td>✅ Support auditing TiDB Cloud console operations.</td>
    <td>Support reliable auditing capabilities for various operations in the TiDB Cloud console.</td>
  </tr>
</tbody>
</table>
