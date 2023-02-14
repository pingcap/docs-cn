---
title: Deploy TiDB Dashboard
summary: Learn how to deploy TiDB Dashboard.
aliases: ['/docs/dev/dashboard/dashboard-ops-deploy/']
---

# Deploy TiDB Dashboard

The TiDB Dashboard UI is built into the PD component for v4.0 or higher versions, and no additional deployment is required. Simply deploy a standard TiDB cluster, and TiDB Dashboard will be there.

> **Note:**
>
> TiDB v6.5.0 (and later) and TiDB Operator v1.4.0 (and later) support deploying TiDB Dashboard as an independent Pod on Kubernetes. For details, see [Deploy TiDB Dashboard independently in TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/dev/get-started#deploy-tidb-dashboard-independently).

See the following documents to learn how to deploy a standard TiDB cluster:

+ [Quick Start Guide for the TiDB Database Platform](/quick-start-with-tidb.md)
+ [Deploy TiDB in Production Environment](/production-deployment-using-tiup.md)
+ [Kubernetes environment deployment](https://docs.pingcap.com/tidb-in-kubernetes/stable/access-dashboard)

> **Note:**
>
> You cannot deploy TiDB Dashboard in a TiDB cluster earlier than v4.0.

## Deployment with multiple PD instances

When multiple PD instances are deployed in the cluster, only one of these instances serves the TiDB Dashboard.

When PD instances are running for the first time, they automatically negotiate with each other to choose one instance to serve the TiDB Dashboard. TiDB Dashboard will not run on other PD instances. The TiDB Dashboard service will always be provided by the chosen PD instance no matter PD instances are restarted or new PD instances are joined. However, there will be a re-negotiation when the PD instance that serves TiDB Dashboard is removed from the cluster (scaled-in). The negotiation process does not need user intervention.

When you access a PD instance that does not serve TiDB Dashboard, the browser will be redirected automatically to guide you to access the PD instance that serves the TiDB Dashboard, so that you can access the service normally. This process is illustrated in the image below.

![Process Schematic](/media/dashboard/dashboard-ops-multiple-pd.png)

> **Note:**
>
> The PD instance that serves TiDB Dashboard might not be a PD leader.

### Check the PD instance that actually serves TiDB Dashboard

For a running cluster deployed using TiUP, you can use the `tiup cluster display` command to see which PD instance serves TiDB Dashboard. Replace `CLUSTER_NAME` with the cluster name.

{{< copyable "shell-regular" >}}

```bash
tiup cluster display CLUSTER_NAME --dashboard
```

A sample output is as follows:

```bash
http://192.168.0.123:2379/dashboard/
```

> **Note:**
>
> This feature is available only in the later version of the `tiup cluster` deployment tool (v1.0.3 or later).
>
> <details>
> <summary>Upgrade TiUP Cluster</summary>
>
> ```bash
> tiup update --self
> tiup update cluster --force
> ```
>
> </details>

### Switch to another PD instance to serve TiDB Dashboard

For a running cluster deployed using TiUP, you can use the `tiup ctl:v<CLUSTER_VERSION> pd` command to change the PD instance that serves TiDB Dashboard, or re-specify a PD instance to serve TiDB Dashboard when it is disabled:

{{< copyable "shell-regular" >}}

```bash
tiup ctl:v<CLUSTER_VERSION> pd -u http://127.0.0.1:2379 config set dashboard-address http://9.9.9.9:2379
```

In the command above:

- Replace `127.0.0.1:2379` with the IP and port of any PD instance.
- Replace `9.9.9.9:2379` with the IP and port of the new PD instance that you desire to run the TiDB Dashboard service.

You can use the `tiup cluster display` command to see whether the modification is taking effect (replace `CLUSTER_NAME` with the cluster name):

{{< copyable "shell-regular" >}}

```bash
tiup cluster display CLUSTER_NAME --dashboard
```

> **Warning:**
>
> If you change the instance to run TiDB Dashboard, the local data stored in the previous TiDB Dashboard instance will be lost, including the Key Visualize history and search history.

## Disable TiDB Dashboard

For a running cluster deployed using TiUP, use the `tiup ctl:v<CLUSTER_VERSION> pd` command to disable TiDB Dashboard on all PD instances (replace `127.0.0.1:2379` with the IP and port of any PD instance):

{{< copyable "shell-regular" >}}

```bash
tiup ctl:v<CLUSTER_VERSION> pd -u http://127.0.0.1:2379 config set dashboard-address none
```

After disabling TiDB Dashboard, checking which PD instance provides the TiDB Dashboard service will fail:

```
Error: TiDB Dashboard is disabled
```

Visiting the TiDB Dashboard address of any PD instance via the browser will also fail:

```
Dashboard is not started.
```

## Re-enable TiDB Dashboard

For a running cluster deployed using TiUP, use the `tiup ctl:v<CLUSTER_VERSION> pd` command to request PD to renegotiate an instance to run TiDB Dashboard (replace `127.0.0.1:2379` with the IP and port of any PD instance):

{{< copyable "shell-regular" >}}

```bash
tiup ctl:v<CLUSTER_VERSION> pd -u http://127.0.0.1:2379 config set dashboard-address auto
```

After executing the command above, you can use the `tiup cluster display` command to view the TiDB Dashboard instance address automatically negotiated by PD (replace `CLUSTER_NAME` with the cluster name):

{{< copyable "shell-regular" >}}

```bash
tiup cluster display CLUSTER_NAME --dashboard
```

You can also re-enable TiDB Dashboard by manually specifying the PD instance that serves TiDB Dashboard. See [Switch to another PD instance to serve TiDB Dashboard](#switch-to-another-pd-instance-to-serve-tidb-dashboard).

> **Warning:**
>
> If the newly enabled TiDB Dashboard instance is different with the previous instance that served the TiDB Dashboard, the local data stored in the previous TiDB Dashboard instance will be lost, including Key Visualize history and search history.

## What's next

- To learn how to access and log into the TiDB Dashboard UI, see [Access TiDB Dashboard](/dashboard/dashboard-access.md).

- To learn how to enhance the security of TiDB Dashboard, such as configuring a firewall, see [Secure TiDB Dashboard](/dashboard/dashboard-ops-security.md).
