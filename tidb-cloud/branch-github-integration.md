---
title: Integrate TiDB Serverless Branching (Beta) with GitHub 
summary: Learn how to integrate the TiDB Serverless branching feature with GitHub.
---

# Integrate TiDB Serverless Branching (Beta) with GitHub 

> **Note:**
>
> The integration is built upon [TiDB Serverless branching](/tidb-cloud/branch-overview.md). Make sure that you are familiar with TiDB Serverless branching before reading this document.

If you use GitHub for application development, you can integrate TiDB Serverless branching into your GitHub CI/CD pipeline, which lets you automatically test your pull requests with branches without affecting the production database.

In the integration process, you will be prompted to install the [TiDB Cloud Branching](https://github.com/apps/tidb-cloud-branching) GitHub App. The app can automatically manage TiDB Serverless branches according to pull requests in your GitHub repository. For example, when you create a pull request, the app will create a corresponding branch for your TiDB Serverless cluster, in which you can work on new features or bug fixes in isolation without affecting the production database.

This document covers the following topics:

1. How to integrate TiDB Serverless branching with GitHub
2. How does the TiDB Cloud Branching app work
3. How to build a branching-based CI workflow to test every pull request using branches rather than the production cluster

## Before you begin

Before the integration, make sure that you have the following:

- A GitHub account
- A GitHub repository for your application
- A [TiDB Serverless cluster](/tidb-cloud/create-tidb-cluster-serverless.md)

## Integrate TiDB Serverless branching with your GitHub repository

To integrate TiDB Serverless branching with your GitHub repository, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project, and then click the name of your target TiDB Serverless cluster to go to its overview page.

2. Click **Branches** in the left navigation pane.

3. In the upper-right corner of the **Branches** page, click **Connect to GitHub**.

    - If you have not logged into GitHub, you will be asked to log into GitHub first.
    - If it is the first time you use the integration, you will be asked to authorize the **TiDB Cloud Branching** app.

   <img src="https://download.pingcap.com/images/docs/tidb-cloud/branch/github-authorize.png" width="80%" />

4. In the **Connect to GitHub** dialog, select a GitHub account in the **GitHub Account** drop-down list.

    If your account does not exist in the list, click **Install Other Account**, and then follow the on-screen instructions to install the account.

5. Select your target repository in the **GitHub Repository** drop-down list. If the list is long, you can search the repository by typing the name.

6. Click **Connect** to connect between your TiDB Serverless cluster and your GitHub repository.

   <img src="https://download.pingcap.com/images/docs/tidb-cloud/branch/github-connect.png" width="40%" />

## TiDB Cloud Branching app behaviors

After you connect your TiDB Serverless cluster to your GitHub repository, for each pull request in this repository, the [TiDB Cloud Branching](https://github.com/apps/tidb-cloud-branching) GitHub App can automatically manage its corresponding TiDB Serverless branch. The following lists the default behaviors for pull request changes:

| Pull request changes               | TiDB Cloud Branching app behaviors                                                                                                                                                                                                                                                                                                                                        |
|------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Create a pull request              | When you create a pull request in the repository, the [TiDB Cloud Branching](https://github.com/apps/tidb-cloud-branching) app creates a branch for your TiDB Serverless cluster. The branch name is in the `${github_branch_name}_${pr_id}_${commit_sha}` format. Note that the number of branches has a [limit](/tidb-cloud/branch-overview.md#limitations-and-quotas). |
| Push new commits to a pull request | Every time you push a new commit to a pull request in the repository, the [TiDB Cloud Branching](https://github.com/apps/tidb-cloud-branching) app deletes the previous TiDB Serverless branch and creates a new branch for the latest commit.                                                                                                                            |
| Close or merge a pull request      | When you close or merge a pull request, the [TiDB Cloud Branching](https://github.com/apps/tidb-cloud-branching) app deletes the branch for this pull request.                                                                                                                                                                                                            |
| Reopen a pull request              | When you reopen a pull request, the [TiDB Cloud Branching](https://github.com/apps/tidb-cloud-branching) app creates a branch for the lasted commit of the pull request.                                                                                                                                                                                                  |

## Configure TiDB Cloud Branching app

To configure the behaviors of [TiDB Cloud Branching](https://github.com/apps/tidb-cloud-branching) app, you can add a `tidbcloud.yml` file to the root directory of your repository, and then add the desired configurations to this file according to the following instructions.

### branch.blockList

**Type:** array of string. **Default:** `[]`.

Specify the GitHub branches that forbid the TiDB Cloud Branching app, even if they are in the `allowList`.

```yaml
github:
    branch:
        blockList:
            - ".*_doc"
            - ".*_blackList"
```

### branch.allowList

**type:** array of string. **Default:** `[.*]`.

Specify the GitHub branches that allow the TiDB Cloud Branching app.

```yaml
github:
    branch:
        allowList:
            - ".*_db"
```

### branch.autoReserved

**Type:** boolean. **Default:** `false`.

If it is set to `true`, the TiDB Cloud Branching app will not delete the TiDB Serverless branch that is created in the previous commit.

```yaml
github:
    branch:
        autoReserved: false
```

### branch.autoDestroy

**Type:** boolean. **Default:** `true`.

If it is set to `false`, the TiDB Cloud Branching app will not delete the TiDB Serverless branch when a pull request is closed or merged.

```yaml
github:
    branch:
        autoDestroy: true
```

## Create a branching CI workflow

One of the best practices for using branches is to create a branching CI workflow. With the workflow, you can test your code using a TiDB Serverless branch instead of using the production cluster before merging the pull request. You can find a live demo [here](https://github.com/shiyuhang0/tidbcloud-branch-gorm-example).

Here are the main steps to create the workflow:

1. [Integrate TiDB Serverless branching with your GitHub repository](#integrate-tidb-serverless-branching-with-your-github-repository).

2. Get the branch connection information.

   You can use the [wait-for-tidbcloud-branch](https://github.com/tidbcloud/wait-for-tidbcloud-branch) action to wait for the readiness of the TiDB Serverless branch and get the connection information of the branch.

    Example usage:

   ```yaml
   steps:
     - name: Wait for TiDB Serverless branch to be ready
       uses: tidbcloud/wait-for-tidbcloud-branch@v0
       id: wait-for-branch
       with:
         token: ${{ secrets.GITHUB_TOKEN }}
         public-key: ${{ secrets.TIDB_CLOUD_API_PUBLIC_KEY }}
         private-key: ${{ secrets.TIDB_CLOUD_API_PRIVATE_KEY }}

     - name: Test with TiDB Serverless branch
        run: |
           echo "The host is ${{ steps.wait-for-branch.outputs.host }}"
           echo "The user is ${{ steps.wait-for-branch.outputs.user }}"
           echo "The password is ${{ steps.wait-for-branch.outputs.password }}"
   ```
   
   - `token`: GitHub will automatically create a [GITHUB_TOKEN](https://docs.github.com/en/actions/security-guides/automatic-token-authentication) secret. You can use it directly.
   - `public-key` and `private-key`: The TiDB Cloud [API key](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management).

3. Modify your test code.

   Modify your test code to accept the connection information from GitHub Actions. For example, you can accept the connection information through the environment, as demonstrated in the [live demo](https://github.com/shiyuhang0/tidbcloud-branch-gorm-example).

## What's next

Learn how to use the branching GitHub integration with the following examples:

- [branching-gorm-example](https://github.com/tidbcloud/branching-gorm-example)
- [branching-django-example](https://github.com/tidbcloud/branching-django-example)
- [branching-rails-example](https://github.com/tidbcloud/branching-rails-example)

You can also build your branching CI/CD workflow without the branching GitHub integration. For example, you can use [`setup-tidbcloud-cli`](https://github.com/tidbcloud/setup-tidbcloud-cli) and GitHub Actions to customize your CI/CD workflows.
