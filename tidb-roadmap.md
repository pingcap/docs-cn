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
            <b>Distributed execution framework</b><br /><i>
            In v7.2.0, TiDB introduced the distributed execution framework for background tasks (such as DDL and analyze). This is the foundation for parallelizing these tasks across compute nodes. v7.4.0 introduces global sorting in distributed re-organization tasks (such as DDL and import), which greatly mitigates extra resource consumption in storage. Optionally, external shared storage can be leveraged for simplicity and cost savings.</i>
          </li>
          <br />
          <br />
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Enhancements to performance and generalizability of plan cache</b><br />
          </li>
          <br />
          <li>
            <b>Dynamic node scaling via distributed execution framework</b><br />
            <i>Automatically adjust node allocation to meet resource costs of background tasks, while maintaining stability and performance expectations</i>
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
          <li>
            <b>Federated query</b>
            <br /><i>TiDB query planner support for multiple storage engines in HTAP use cases.</i>
          </li>
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
          <br />
          <li>
            <b>Runaway query control</b><br /><i>
              An operator-controlled way to greatly enhance performance stability for workloads with unexpectedly expensive queries
            </i>
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Disaggregation of Placement Driver (PD)</b>
            <br /><i>Enhance cluster scalability and resilience</i>
          </li>
          <br />
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
    </tr>
    <tr>
      <td>
        <b>Database Operations and Observability</b>
        <br /><i>Enhance DB manageability and its ecosystem</i>
      </td>
      <td>
        <ul>
          <li>
            <b>TiCDC integrations with data warehouse or data lake systems</b>
            <br />
          </li>
          <br />
          <li>
            <b>TiDB node labels</b>
            <br /><i>Assign existing or newly added TiDB nodes for DDL operations to isolate DDL tasks from the compute resources used by online traffic
</i>
          </li>
          <br />
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>SQL plan management</b>
            <br /><i>Mechanism for controlling SQL plan regression</i>
          </li>
          <br />
          <li>
            <b>Index Advisor</b>
            <br /><i>Offer index recommendations to users based on workload, statistics, and execution plans</i>
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>Materialized views</b>
            <br /><i>Store pre-computed results as a persistent data view to boost query performance</i>
          </li>
          <br />
          <li>
            <b>Heterogeneous database migration support</b>
          </li>
          <br />
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
          <br></br>
          <li>
            <b>AWS FIPS support</b>
            <br /><i>Enable FedRAMP compliance</i>
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
