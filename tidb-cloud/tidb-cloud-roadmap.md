---
title: TiDB Cloud Roadmap
summary: Learn about TiDB Cloud's roadmap for the next few months. See the new features or improvements in advance, follow the progress, learn about the key milestones on the way.
---

# TiDB Cloud Roadmap

The TiDB Cloud roadmap brings you what's coming in the near future, so you can see the new features or improvements in advance, follow the progress, and learn about the key milestones on the way. In the course of development, this roadmap is subject to change based on user needs, feedback, and our assessment.

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
    <td rowspan="2">Developer experience</td>
    <td>Load sample datasets manually.</td>
    <td>Support loading sample datasets into a cluster. You can use this data to quickly get started with testing the features of TiDB Cloud.</td>
  </tr>
  <tr>
    <td>Add SQL Editor.</td>
    <td>Write and run SQL queries, and view the results in the TiDB console.</td>
  </tr>
  <tr>
    <td>Cloud provider marketplace</td>
    <td>Improve the user experience from AWS Marketplace and GCP Marketplace.</td>
    <td>Improve the user journey and experience of users who sign up from AWS Marketplace and GCP Marketplace.</td>
  </tr>
  <tr>
    <td rowspan="2">Enterprise-grade features</td>
    <td>Manage multiple organizations.</td>
    <td>Support managing multiple organizations. A user can create and join more than one organization.</td>
  </tr>
  <tr>
    <td>Support hierarchical user roles and permissions.</td>
    <td>Support role-based access control (RBAC) for the TiDB Cloud console. You can manage user permissions in a fine-grained manner, such as by cluster, billing, and member.</td>
  </tr>
  <tr>
    <td rowspan="2">UI experience</td>
    <td>Provide a more convenient feedback channel.</td>
    <td>Users can quickly get help with and give feedback on the product.</td>
  </tr>
  <tr>
    <td>Add left navigation.</td>
    <td>Present the TiDB Cloud console in the structure of organizations, projects, and users to simplify the layout logic and improve user experience.</td>
  </tr>
</tbody>
</table>

## TiDB kernel

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
<td rowspan="3">
<p>SQL</p>
</td>
<td>
<p>Support the JSON function.</p>
<ul>
<li>Expression index</li>
<li>Multi-value index</li>
<li>Partial index</li>
</ul>
</td>
<td>
<p>In business scenarios that require flexible schema definitions, the application can use JSON to store information for ODS, transaction indicators, commodities, game characters, and props.</p>
</td>
</tr>
<tr>
<td>
<p>Support cluster-level flashback.</p>
</td>
<td>
<p>In game rollback scenarios, the flashback can be used to achieve a fast rollback of the current cluster. This solves the common problems in the gaming industry such as version errors and bugs.</p>
</td>
</tr>
<tr>
<td>
<p>Support time to live (TTL).</p>
</td>
<td>
<p>This feature enables automatic data cleanup in limited data archiving scenarios.</p>
</td>
</tr>
<tr>
<td rowspan="2">
<p>Hybrid Transactional and Analytical Processing (HTAP)</p>
</td>
<td>
<p>Support TiFlash result write-back.</p>
</td>
<td>
<p>Support <code>INSERT INTO SELECT</code>.</p>
<ul>
<li>Easily write analysis results in TiFlash back to TiDB.</li>
<li>Provide complete ACID transactions, more convenient and reliable than general ETL solutions.</li>
<li>Set a hard limit on the threshold of intermediate result size, and report an error if the threshold is exceeded.</li>
<li>Support fully distributed transactions, and remove or relax the limit on the intermediate result size.</li>
</ul>
<p>These features combined enable a way to materialize intermediate results. The analysis results can be easily reused, which reduces unnecessary ad-hoc queries, improves the performance of BI and other applications (by pulling results directly) and reduces system load (by avoiding duplicated computation), thereby improving the overall data pipeline efficiency and reducing costs. It will make TiFlash an online service.</p>
</td>
</tr>
<tr>
<td>
<p>Support FastScan for TiFlash.</p>
</td>
<td>
<ul>
<li>FastScan provides weak consistency but faster table scan capability.</li>
<li>Further optimize the join order, shuffle, and exchange algorithms to improve computing efficiency and boost performance for complex queries.</li>
<li>Add a fine-grained data sharding mechanism to optimize the <code>COUNT(DISTINCT)</code> function and high cardinality aggregation.</li>
</ul>
<p>This feature improves the basic computing capability of TiFlash, and optimizes the performance and reliability of the underlying algorithms of the columnar storage and MPP engine.</p>
</td>
</tr>
<tr>
<td>
<p>Proxy</p>
</td>
<td>
<p>Support TiDB proxy.</p>
</td>
<td>
<p>Implement automatic load balancing so that upgrading a cluster or modifying configurations does not affect the application. After scaling out or scaling in the cluster, the application can automatically rebalance the connection without reconnecting.</p>
<p>In scenarios such as upgrades and configuration changes, TiDB proxy is more business-friendly.</p>
</td>
</tr>
</tbody>
</table>

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
    <td>Self-service cluster analysis and diagnosis using reports</td>
    <td><ul><li>Cluster health report.</li><li>Cluster status comparison report.</li><li>Cluster performance analysis report.</li><li>Cluster system check report.</li></ul></td>
    <td><ul><li>Provide diagnosis and analysis reports for several different usage scenarios.</li><li>Locate cluster failures for some scenarios and provide recommended solutions.</li><li>Provide cluster key status summary for some scenarios.</li></ul></td>
  </tr>
  <tr>
    <td>SQL tuning for HTAP workloads</td>
    <td><ul><li>Provide SQL execution information from the perspective of applications.</li><li>Provide suggestions on optimizing SQL for TiFlash and TiKV in HTAP workloads.</li></ul></td>
    <td><ul><li>Provide a dashboard that displays a SQL execution overview from the perspective of applications in HTAP workloads.</li><li>For one or several HTAP scenarios, provide suggestions on SQL optimization.</li></ul></td>
  </tr>
  <tr>
    <td>Cluster diagnosis data accessibility </td>
    <td><ul><li>Access diagnosis data online in real time.</li><li>Access diagnosis data offline.</li><li>Build logic for data reconstruction.</li></ul></td>
    <td><ul><li>Integrate with various monitoring and diagnosis systems to improve the real-time data access capability.</li><li>Provide offline data access for large-scale diagnosis, analysis, and tuning.</li><li>Improve data stability and build logic for data reconstruction.</li></ul></td>
  </tr>
  <tr>
    <td>TiDB Cloud service tracing</td>
    <td>Build the monitoring links for each component of TiDB Cloud service.</td>
    <td><ul><li>Build the tracing links for each component of TiDB Cloud service in user scenarios.</li><li>Provide assessment on service availability from the perspective of users.</li></ul></td>
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
    <td>Data replication to Kafka via TiCDC</td>
    <td>Reduce TiCDC replication latency in daily operations.</td>
    <td>When TiKV, TiDB, PD, or TiCDC nodes are offline in a planned maintenance window, the replication latency of TiCDC can be reduced to less than 10 seconds.</td>
  </tr>
  <tr>
    <td>Data disaster recovery</td>
    <td>TiCDC provides cross-region disaster recovery on the cloud.</td>
    <td>TiCDC provides disaster recovery that ensures data eventual consistency with lower cost on TiDB Cloud.</td>
  </tr>
  <tr>
    <td>Point-in-time recovery (PITR)</td>
    <td>Support PITR on the cloud.</td>
    <td>Support cluster-level PITR on the cloud.</td>
  </tr>
  <tr>
    <td>Backup and restore</td>
    <td>Backup and restore service based on AWS EBS or GCP persistent disk snapshots.</td>
    <td>Provide backup and restore service on the cloud based on AWS EBS or GCP persistent disk snapshots.</td>
  </tr>
  <tr>
    <td rowspan="2">Online data migration</td>
    <td>Support full data migration from Amazon Relational Database Service (RDS).</td>
    <td>Full data migration from RDS to TiDB Cloud</td>
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
    <td>Key rotation</td>
    <td>Support key rotation on TiDB clusters for AWS.</td>
    <td>Support key rotation on TiDB clusters to improve the security of encrypted data.</td>
  </tr>
  <tr>
    <td>Key management</td>
    <td>Support making your own key manageable (BYOK from AWS).</td>
    <td>Allow you to use your own data encryption keys on AWS.</td>
  </tr>
   <tr>
    <td>Audit logging</td>
    <td>Enhance the database audit logging.</td>
    <td>Enhance the ability of database audit logging and provide the visual UI access.</td>
  </tr>
</tbody>
</table>
