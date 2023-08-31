---
title: Deploy Data App Automatically with GitHub
summary: Learn how to deploy your Data App automatically with GitHub.
---

# Deploy Data App Automatically with GitHub

TiDB Cloud provides a Configuration as Code (CaC) approach to represent your entire Data App configurations as code using the JSON syntax.

By connecting your Data App to GitHub, TiDB Cloud can use the CaC approach and push your Data App configurations as [configuration files](/tidb-cloud/data-service-app-config-files.md) to your preferred GitHub repository and branch.

If **Auto Sync & Deployment** is enabled for your GitHub connection, you can also modify your Data App by updating its configuration files on GitHub. After you push the configuration file changes to GitHub, the new configurations will be deployed in TiDB Cloud automatically.

This document introduces how to deploy your Data App automatically with GitHub and how to manage the GitHub connection.

## Before you begin

Before you connect a Data App to GitHub, make sure that you have the following:

- A GitHub account.
- A GitHub repository with your target branch.

> **Note:**
>
> The GitHub repository is used to store [Data App configuration files](/tidb-cloud/data-service-app-config-files.md) after you connect a Data App to it. If the information (such as the cluster ID and endpoint URL) in the configuration files is sensitive, make sure to use a private repository instead of a public one.

## Step 1. Connect your Data App to GitHub

You can connect your Data App to GitHub when you create the App. For more information, see [Create a Data App](/tidb-cloud/data-service-manage-data-app.md).

If you did not enable the GitHub connection during the App creation, you can still enable it as follows:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its details.
3. On the **Settings** tab, click **Connect** in the **Connect to GitHub** area. A dialog box for connection settings is displayed.
4. In the dialog box, perform the following steps:

    1. Click **Install on GitHub**, and then follow the on-screen instructions to install **TiDB Cloud Data Service** as an application on your target repository.
    2. Click **Authorize** to authorize access to the application on GitHub.
    3. Specify the target repository, branch, and directory where you want to store the configuration files of your Data App.

        > **Note:**
        >
        > - The directory must start with a slash (`/`). For example, `/mydata`. If the directory you specified does not exist in the target repository and branch, it will be created automatically.
        > - The combination of repository, branch, and directory identifies the path of the configuration files, which must be unique among Data Apps. If your specified path is already used by another Data App, you need to specify a new path instead. Otherwise, the endpoints configured in the TiDB Cloud console for the current Data App will overwrite the files in your specified path.
        > - If your specified path contains configuration files copied from another Data App and you want to import these files to the current Data App, see [Import configurations of an existing Data App](#import-configurations-of-an-existing-data-app).

    4. To allow Data App changes made in either TiDB Cloud console or GitHub are synchronized with each other, enable **Configure Auto Sync & Deployment**.

        - When it is enabled, the changes made in your specified GitHub directory can be automatically deployed in TiDB Cloud, and the changes made in the TiDB Cloud console can be pushed to GitHub as well. You can find the corresponding deployment and commit information in the Data App deployment history.
        - When it is disabled, the changes made in your specified GitHub directory will **NOT** be deployed in TiDB Cloud, and the changes made in the TiDB Cloud console will **NOT** be pushed to GitHub either.

5. Click **Confirm Connect**.

## Step 2. Synchronize Data App configurations with GitHub

If GitHub connection is enabled when you [create a Data App](/tidb-cloud/data-service-manage-data-app.md), TiDB Cloud pushes the configuration files of this Data App to GitHub immediately after the App creation.

If GitHub connection is enabled after the App creation, you need to perform a deployment operation to synchronize the Data App configurations with GitHub. For example, you can click the **Deployments** tab, and then re-deploy a deployment for this Data App.

After the deployment operation, check your specified GitHub directory. You will find that the Data App configuration files have been committed to the directory by `tidb-cloud-data-service`, which means that your Data App is connected to GitHub successfully. The directory structure is as follows:

```
├── <Your Data App directory on GitHub>
│   ├── data_sources
│   │   └── cluster.json  # specifies the linked clusters.
│   ├── dataapp_config.json # specifies the Data APP ID, name, type, version, and description.
│   ├── http_endpoints
│   │   ├── config.json # specifies the endpoints.
│   │   └── sql # contains SQL files of the endpoints.
│   │       ├── <method>-<endpoint-path1>.sql
│   │       ├── <method>-<endpoint-path2>.sql
│   │       └── <method>-<endpoint-path3>.sql
```

## Step 3. Modify your Data App

When **Auto Sync & Deployment** is enabled, you can modify your Data App using either GitHub or the TiDB Cloud console.

- [Option 1: Modify your Data App by updating files on GitHub](#option-1-modify-your-data-app-by-updating-files-on-github)
- [Option 2: Modify your Data App in the TiDB Cloud console](#option-2-modify-your-data-app-in-the-tidb-cloud-console)

> **Note:**
>
> If you have modified your Data App on GitHub and TiDB Cloud console at the same time, to resolve conflicts, you can choose either discard the changes made in the console or let the console changes overwrite the GitHub changes.

### Option 1: Modify your Data App by updating files on GitHub

When updating the configuration files, pay attention to the following:

| File directory  | Notes |
| ---------|---------|
| `data_source/cluster.json`     | When updating this file, make sure that you have access to the linked clusters. You can get the cluster ID from the cluster URL. For example, if the cluster URL is `https://tidbcloud.com/console/clusters/1234567891234567890/overview`, the cluster ID is `1234567891234567890`. |
| `http_endpoints/config.json`     | When modifying the endpoints, make sure that you follow the rules described in [HTTP endpoint configuration](/tidb-cloud/data-service-app-config-files.md#http-endpoint-configuration).   |
| `http_endpoints/sql/method-<endpoint-path>.sql`| To add or remove SQL files in the `http_endpoints/sql` directory, you need to update the corresponding endpoint configurations as well. |
| `datapp_config.json` | Do not change the `app_id` field in this file unless your `dataapp_config.json` file is copied from another Data App and you want to update it to the ID of your current Data App. Otherwise, the deployment triggered by this modification will fail. |

For more information about the field configuration in these files, see [Data App configuration files](/tidb-cloud/data-service-app-config-files.md).

After the file changes are committed and pushed, TiDB Cloud will automatically deploy the Data App with the latest changes on GitHub. You can view the deployment status and commit information in the deployment history.

### Option 2: Modify your Data App in the TiDB Cloud console

After [modifying your Data App endpoints](/tidb-cloud/data-service-manage-endpoint.md) in the TiDB Cloud console (such as modifying endpoints), you can review and deploy the changes to GitHub as follows:

1. Click **Deploy** in the upper-right corner. A dialog is displayed for you to review the changes you made.
2. Depending on your review, do one of the following:

    - If you still want to make further changes based on the current draft, close this dialog and make the changes.
    - If you want to revert the current changes to the last deployment, click **Discard Draft**.
    - If the current changes look fine, write a change description (optional), and then click **Deploy and Push to GitHub**. The deployment status will be displayed in the top banner.

If the deployment is successful, the changes made in the TiDB Cloud console will be pushed to GitHub automatically.

## Import configurations of an existing Data App

To import configurations of an existing Data App to a new Data App, take the following steps:

1. Copy configuration files of the existing Data App to a new branch or directory on GitHub.
2. On the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project, [create a new Data App](/tidb-cloud/data-service-manage-data-app.md#create-a-data-app) without connecting to GitHub.
3. [Connect your new Data App to GitHub](#step-1-connect-your-data-app-to-github) with **Auto Sync & Deployment** enabled. When you specify the target repository, branch, and directory for your new Data App, use your new path with the copied configuration files.
4. Get the ID and name of your new Data App. You can click the name of your new Data App in the left pane and get the App ID and name in the **Data App Properties** area of the right pane.
5. In your new path on GitHub, update the `app_id` and `app_name` in the `datapp_config.json` file to the ID and name you get, and then push the changes.

    After the file changes are pushed to GitHub, TiDB Cloud will automatically deploy your new Data App with the latest changes.

6. To view the imported configurations from GitHub, refresh the webpage of the TiDB Cloud console.

    You can also view the deployment status and commit information in the deployment history.

## Edit GitHub connection

If you want to edit the GitHub connection for your Data App (such as switching the repository, branch, and directory), perform the following steps.

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its details.
3. In the **Connect to GitHub** area, click <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" color="gray.1"><path d="M11 3.99998H6.8C5.11984 3.99998 4.27976 3.99998 3.63803 4.32696C3.07354 4.61458 2.6146 5.07353 2.32698 5.63801C2 6.27975 2 7.11983 2 8.79998V17.2C2 18.8801 2 19.7202 2.32698 20.362C2.6146 20.9264 3.07354 21.3854 3.63803 21.673C4.27976 22 5.11984 22 6.8 22H15.2C16.8802 22 17.7202 22 18.362 21.673C18.9265 21.3854 19.3854 20.9264 19.673 20.362C20 19.7202 20 18.8801 20 17.2V13M7.99997 16H9.67452C10.1637 16 10.4083 16 10.6385 15.9447C10.8425 15.8957 11.0376 15.8149 11.2166 15.7053C11.4184 15.5816 11.5914 15.4086 11.9373 15.0627L21.5 5.49998C22.3284 4.67156 22.3284 3.32841 21.5 2.49998C20.6716 1.67156 19.3284 1.67155 18.5 2.49998L8.93723 12.0627C8.59133 12.4086 8.41838 12.5816 8.29469 12.7834C8.18504 12.9624 8.10423 13.1574 8.05523 13.3615C7.99997 13.5917 7.99997 13.8363 7.99997 14.3255V16Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>. A dialog box for connection settings is displayed.
4. In the dialog box, modify the repository, branch, and directory of your Data App.

    > **Note:**
    >
    > - The directory must start with a slash (`/`). For example, `/mydata`. If the directory you specified does not exist in the target repository and branch, it will be created automatically.
    > - The combination of repository, branch, and directory identifies the path of the configuration files, which must be unique among Data Apps. If your specified path is already used by another Data App, you need to specify a new path instead. Otherwise, the endpoints configured in the TiDB Cloud console for the current Data App will overwrite the files in your specified path.
    > - If your specified path contains configuration files copied from another Data App and you want to import these files to the current Data App, see [Import configurations of an existing Data App](#import-configurations-of-an-existing-data-app).

5. To allow Data App changes made in either TiDB Cloud console or GitHub are synchronized with each other, enable **Configure Auto Sync & Deployment**.

    - When it is enabled, the changes made in your specified GitHub directory can be automatically deployed in TiDB Cloud, and the changes made in the TiDB Cloud console can be pushed to GitHub as well. You can find the corresponding deployment and commit information in the Data App deployment history.
    - When it is disabled, the changes made in your specified GitHub directory will **NOT** be deployed in TiDB Cloud, and the changes made in the TiDB Cloud console will **NOT** be pushed to GitHub either.

6. Click **Confirm Connect**.

## Remove GitHub connection

If you no longer want to connect your Data App to GitHub, take the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its details.
3. On the **Settings** tab, click **Disconnect** in the **Connect to GitHub** area.
4. Click **Disconnect** to confirm the disconnection.

After the disconnection operation, your Data App configuration files will remain in your GitHub directory but will not be synchronized by `tidb-cloud-data-service` anymore.