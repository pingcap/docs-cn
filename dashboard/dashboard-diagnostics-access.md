---
title: TiDB Dashboard Cluster Diagnostic Page
summary: Learn how to use the cluster diagnostic page.
aliases: ['/docs/dev/dashboard/dashboard-diagnostics-access/']
---

# TiDB Dashboard Cluster Diagnostics Page

> **Warning:**
>
> Diagnostics in TiDB Dashboard is still an experimental feature. It is **NOT** recommended that you use it in the production environment.

The cluster diagnostics feature in TiDB Dashboard diagnoses the problems that might exist in a cluster within a specified time range, and summarizes the diagnostic results and the cluster-related load monitoring information into a diagnostic report. This diagnostic report is in the form of a web page. You can browse the page offline and circulate this page link after saving the page from a browser.

> **Note:**
>
> The cluster diagnostics feature depends on Prometheus deployed in the cluster. For details about how to deploy this monitoring component, see [TiUP](/tiup/tiup-overview.md) or [TiDB Ansible](/online-deployment-using-ansible.md) deployment document. If no monitoring component is deployed in the cluster, the generated diagnostic report will indicate a failure.

## Access the page

You can use one of the following methods to access the cluster diagnostics page:

- After logging into TiDB Dashboard, click **Cluster Diagnostics** on the left navigation menu:

  ![Access Cluster Diagnostics page](/media/dashboard/dashboard-diagnostics-access.png)

- Visit `http://127.0.0.1:2379/dashboard/#/diagnose` in your browser. Replace `127.0.0.1:2379` with the actual PD address and port number.

## Generate diagnostic report

To diagnose a cluster within a specified time range and check the cluster load, you can take the following steps to generate a diagnostic report:

1. Set the **Range Start Time**, such as `2020-05-21 14:40:00`.
2. Set the **Range Duration**, such as `10 min`.
3. Click **Start**.

![Generate diagnostic report](/media/dashboard/dashboard-diagnostics-gen-report.png)

> **Note:**
>
> It is recommended that the **Range Duration** of the report is between 1 minute and 60 minutes. This **Range Duration** cannot exceed 60 minutes.

The steps above generate a diagnostic report for the time range from `2020-05-21 14:40:00` to `2020-05-21 14:50:00`. After clicking **Start**, you can see the interface below. **Progress** is the progress bar of the diagnostic report. After the report is generated, click **View Full Report**.

![Report progress](/media/dashboard/dashboard-diagnostics-gen-process.png)

## Generate comparison report

If a system exception occurs at a certain point, for example, QPS jitter or higher latency, a diagnostic report can be generated. Particularly, this report compares the system in the abnormal time range with the system in the normal time range. For example:

- Abnormal time range: `2020-05-21 14:40:00`-`2020-05-21 14:45:00`. Within this time range, the system is abnormal.
- Normal time range: `2020-05-21 14:30:00` - `2020-05-21 14:35:00`. Within this time range, the system is normal.

You can take the following steps to generate a comparison report for the two time ranges above:

1. Set the **Range Start Time**, which is the start time of the range in which the system becomes abnormal, such as `2020-05-21 14:40:00`.
2. Set the **Range Duration**. Generally, this duration is the duration of system anomalies, such as 5 minutes.
3. Enable **Compare by baseline**.
4. Set the **Baseline Range Start Time**, which is the start time of the range (to be compared with) in which the system is normal, such as `2020-05-21 14:30:00`.
5. Click **Start**.

![Generate comparison report](/media/dashboard/dashboard-diagnostics-gen-compare-report.png)

Then wait for the report to be generated and click **View Full Report**.

In addition, the historical diagnostic report is displayed in the list on the main page of the diagnostic report. You can click to view these historical reports directly.
