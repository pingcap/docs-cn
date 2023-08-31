---
title: Manage TiDB Serverless Branches
summary: Learn How to manage TiDB Serverless branches.
---

# Manage TiDB Serverless Branches

This document describes how to manage TiDB Serverless branches using the [TiDB Cloud console](https://tidbcloud.com). To manage it using the TiDB Cloud CLI, see [`ticloud branch`](/tidb-cloud/ticloud-branch-create.md).

## Required access

- To [create a branch](#create-a-branch) or [connect to a branch](#connect-to-a-branch), you must be in the `Organization Owner` role of your organization or the `Project Owner` role of the target project.
- To [view branches](#create-a-branch) for clusters in a project, you must belong to that project.

For more information about permissions, see [User roles](/tidb-cloud/manage-user-access.md#user-roles).

## Create a branch

> **Note:**
>
> You can only create branches for TiDB Serverless clusters that are created after July 5, 2023. See [Limitations and quotas](/tidb-cloud/branch-overview.md#limitations-and-quotas) for more limitations.

To create a branch, perform the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project, and then click the name of your target TiDB Serverless cluster to go to its overview page.
2. Click **Branches** in the left navigation pane.
3. Click **Create Branch** in the upper-right corner.
4. Enter the branch name, and then click **Create**.

Depending on the data size in your cluster, the branch creation will be completed in a few minutes.

## View branches

To view branches for your cluster, perform the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project, and then click the name of your target TiDB Serverless cluster to go to its overview page.
2. Click **Branches** in the left navigation pane.

    The branch list of the cluster is displayed in the right pane.

## Connect to a branch

To connect to a branch, perform the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project, and then click the name of your target TiDB Serverless cluster to go to its overview page.
2. Click **Branches** in the left navigation pane.
3. In the row of your target branch to be connected, click **...** in the **Action** column.
4. Click **Connect** in the drop-down list. The dialog for the connection information is displayed.
5. Click **Create password** or **Reset password** to create or reset the root password.
6. Connect to the branch using the connection information.

> **Note:**
>
> Currently, branches do not support [private endpoints](/tidb-cloud/set-up-private-endpoint-connections-serverless.md).

## Delete a branch

To delete a branch, perform the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project, and then click the name of your target TiDB Serverless cluster to go to its overview page.
2. Click **Branches** in the left navigation pane.
3. In the row of your target branch to be deleted, click **...** in the **Action** column.
4. Click **Delete** in the drop-down list.
5. Confirm the deletion.

## What's next

- [Integrate TiDB Serverless branching into your GitHub CI/CD pipeline](/tidb-cloud/branch-github-integration.md)
