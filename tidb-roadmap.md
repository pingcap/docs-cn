---
title: TiDB Roadmap
summary: Learn about what's coming in the future for TiDB.
---

# TiDB Roadmap

This roadmap provides a look into the proposed future. This will be continually updated as we release long-term stable (LTS) versions. The purpose is to provide visibility into what is coming, so that you can more closely follow the progress, learn about the key milestones on the way, and give feedback as the development work goes on.

In the course of development, this roadmap is subject to change based on user needs and feedback. As expected, as the columns move right, the items under them are less committed. If you have a feature request or want to prioritize a feature, please file an issue on [GitHub](https://github.com/pingcap/tidb/issues).

## Rolling roadmap highlights

<table>
  <thead>
    <tr>
      <th>Category</th>
      <th>End of CY23 LTS release</th>
      <th>Mid of CY24 LTS release</th>
      <th>Future releases</th>
    </tr>
  </thead>
  <tbody valign="top">
    <tr>
      <td>
        <b>Scalability and Performance</b><br /><i>Enhance horsepower</i>
      </td>
      <td>
        <ul>
          <li>
            <b>GA of Partitioned Raft KV storage engine</b><br /><i
              >PB-scale clusters, increased write velocity, faster scaling operations, and improved compaction stability</i
            >
          </li>
          <br />
          <li>
            <b>Augmented replica read</b><br /><i>
              Reduced cross-AZ data transfer costs in TiKV
            </i>
          </li>
          <br />
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Performance optimization framework for all applicable background tasks, like DDL, TTL, and cluster analysis</b><br />
            <i>This distributes the workload of these operations throughout the cluster, leading to accelerated performance and reduced resource utilization on individual nodes. This framework already applies to the <code>ADD INDEX</code> operation</i>
          </li>
          <br />
          <li>
            <b>GA of disaggregated storage and compute architecture and S3 shared storage in TiFlash</b><br />
            <i>Enable more cost-effective and elastic HTAP</i>
          </li>
          <br />
          <br />
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Unlimited transaction size</b>
          </li>
          <br />
          <br />
        </ul>
      </td>
    </tr>
    <tr>
      <td>
        <b>Reliability and Availability</b>
        <br /><i>Enhance dependability</i>
      </td>
      <td>
        <ul>
          <li>
            <b>Resource control for background tasks</b><br />
            <i>
              Control over how background tasks, such as imports, DDL, TTL, auto-analyze, and compactions, can affect foreground traffic
            </i>
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Multi-tenancy</b>
            <br /><i>Resource isolation on top of resource control</i>
          </li>
          <br />
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Enhanced TiDB memory management</b>
          </li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>
        <b>SQL</b>
        <br /><i>Enhance functionality and compatibility</i>
      </td>
      <td>
        <ul>
          <li>
            <b>MySQL 8.0 compatibility</b>
          </li>
          <br />
                    <li>
            <b>Unified SQL interface for import, Backup & Restore, and PITR</b>
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Cascades framework for optimizer</b>
            <br /><i>Improved framework for query optimization, and make the optimizer more extensible and future-proof</i>
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Federated query</b>
          </li>
          <br />
          <li>
            <b>Full text search & GIS support</b>
          </li>
          <br />
          <li>
            <b>User-defined functions</b>
          </li>
          <br />
        </ul>
      </td>
    </tr>
    <tr>
      <td>
        <b>Database Operations and Observability</b>
        <br /><i>Enhance DB manageability and its ecosystem</i>
      </td>
      <td>
        <ul>
          <li>
            <b>Distributed TiCDC single table replication</b>
            <br /><i>
              Dramatically improve TiDB-TiDB replication throughput
            </i>
          </li>
          <br />
          <li>
            <b
              >Automatic pause/resume DDL during upgrade</b
            >
            <br /><i>Ensure a smooth upgrade experience</i>
          </li>
          <br />
          <li>
            <b>TiCDC native integrations with big data systems</b>
            <br /><i
              >Such as Snowflake and Iceburg</i
            >
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Multiple upstreams for TiCDC</b>
            <br /><i>Support N:1 TiDB to TiCDC</i>
          </li>
          <br />
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>AI-indexing</b>
          </li>
          <br />
          <li>
            <b>Heterogeneous database migration support</b>
          </li>
          <br />
          <li>
            <b>Re-invented AI-SQL performance advisor</b>
          </li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>
        <b>Security</b>
        <br /><i>Enhance data safety and privacy</i>
      </td>
      <td>
        <ul>
          <li>
            <b>Key management via Azure Key Vault</b>
            <br /><i>Static encryption managed by Azure Key Vault</i>
          </li>
          <br />
          <li>
            <b>Column-level access control</b>
            <br /><i>Grant and restrict access to specific columns</i>
          </li>
          <br />
          <li>
            <b>Database-level encryption</b>
            <br /><i>At-rest encryption configured at database level</i>
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>IAM authentication for AWS</b>
            <br /><i>TiDB as AWS third-party ARN for AWS IAM access</i>
          </li>
          <br />
          <li>
            <b>Unified TLS CA/Key rotation policy</b>
            <br /><i>Unified certificate management mechanism for all TiDB components</i>
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Label-based access control</b>
            <br /><i>Access permissions granted by configured labels</i>
          </li>
          <br />
          <li>
            <b>Enhanced client-side encryption</b>
          </li>
          <br />
          <li>
            <b>Enhanced data masking</b>
          </li>
          <br />
          <li>
            <b>Enhanced data lifecycle management</b>
          </li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>

These are non-exhaustive plans and are subject to change. Features might differ per service subscriptions.

## Previously delivered roadmap items

You might have been waiting on some items from the last version. The following lists some previously delivered features. For more details, refer to the [v7.1.0 release notes](/releases/release-7.1.0.md).

- Foundation of multi-tenancy framework: resource control quotas and scheduling for resource groups
- TiCDC supports object storage sink, including Amazon S3 and Azure Blob Storage (GA)
- Fastest online `ADD INDEX` (GA)
- TiFlash late materialization (GA)
- TiFlash supports spill to disk (GA)
- LDAP authentication
- SQL audit log enhancement (Enterprise-only)
- Partitioned Raft KV storage engine (experimental)
- General session-level plan cache (experimental)
- TiCDC distributed per table with Kafka downstream (experimental)

## Recently shipped

- [TiDB 7.4.0 Release Notes](https://docs.pingcap.com/tidb/v7.4/release-7.4.0)
- [TiDB 7.3.0 Release Notes](https://docs.pingcap.com/tidb/v7.3/release-7.3.0)
- [TiDB 7.2.0 Release Notes](https://docs.pingcap.com/tidb/v7.2/release-7.2.0)
- [TiDB 7.1.0 Release Notes](https://docs.pingcap.com/tidb/v7.1/release-7.1.0)
- [TiDB 7.0.0 Release Notes](https://docs.pingcap.com/tidb/v7.0/release-7.0.0)
- [TiDB 6.6.0 Release Notes](https://docs.pingcap.com/tidb/v6.6/release-6.6.0)
- [TiDB 6.5.0 Release Notes](https://docs.pingcap.com/tidb/v6.5/release-6.5.0)
