---
title: Connect to TiDB Dedicated via VPC Peering
summary: Learn how to connect to TiDB Dedicated via VPC peering.
---

# Connect to TiDB Dedicated via VPC Peering

> **Note:**
>
> VPC peering connection is only available for TiDB Dedicated clusters. You cannot connect to [TiDB Serverless clusters](/tidb-cloud/select-cluster-tier.md#tidb-serverless) using VPC peering.

To connect your application to TiDB Cloud via VPC peering, you need to set up [VPC peering](/tidb-cloud/tidb-cloud-glossary.md#vpc-peering) with TiDB Cloud. This document walks you through setting up VPC peering connections [on AWS](#set-up-vpc-peering-on-aws) and [on Google Cloud](#set-up-vpc-peering-on-google-cloud) and connecting to TiDB Cloud via a VPC peering.

VPC peering connection is a networking connection between two VPCs that enables you to route traffic between them using private IP addresses. Instances in either VPC can communicate with each other as if they are within the same network.

Currently, TiDB Cloud only supports VPC peering in the same region for the same project. TiDB clusters of the same project in the same region are created in the same VPC. Therefore, once VPC peering is set up in a region of a project, all the TiDB clusters created in the same region of this project can be connected in your VPC. VPC peering setup differs among cloud providers.

> **Tip:**
>
> To connect your application to TiDB Cloud, you can also set up [private endpoint connection](/tidb-cloud/set-up-private-endpoint-connections.md) with TiDB Cloud, which is secure and private, and does not expose your data to the public internet. It is recommended to use private endpoints over VPC peering connections.

## Prerequisite: Set a Project CIDR

Project CIDR (Classless Inter-Domain Routing) is the CIDR block used for network peering in a project.

Before adding VPC Peering requests to a region, you need to set a project CIDR for your project's cloud provider (AWS or Google Cloud) to establish a peering link to your application's VPC.

You can set the project CIDR when creating the first TiDB Dedicated of your project. If you want to set the project CIDR before creating the cluster, perform the following operations:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com).
2. Click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner, switch to the target project if you have multiple projects, and then click **Project Settings**.
3. On the **Project Settings** page of your project, click **Network Access** in the left navigation pane, and then click the **Project CIDR** tab.
4. Click **Add a project CIDR for AWS** or **Add a project CIDR for Google Cloud** according to your cloud provider, specify one of the following network addresses in the **Project CIDR** field, and then click **Confirm**.

    > **Note:**
    >
    > To avoid any conflicts with the CIDR of the VPC where your application is located, you need to set a different project CIDR in this field.

    - 10.250.0.0/16
    - 10.250.0.0/17
    - 10.250.128.0/17
    - 172.30.0.0/16
    - 172.30.0.0/17
    - 172.30.128.0/17

    ![Project-CIDR4](/media/tidb-cloud/Project-CIDR4.png)

5. View the CIDR of the cloud provider and the specific region.

    The region CIDR is inactive by default. To activate the region CIDR, you need to create a cluster in the target region. When the region CIDR is active, you can create VPC Peering for the region.

    ![Project-CIDR2](/media/tidb-cloud/Project-CIDR2.png)

## Set up VPC peering on AWS

This section describes how to set up VPC peering connections on AWS. For Google Cloud, see [Set up VPC peering on Google Cloud](#set-up-vpc-peering-on-google-cloud).

### Step 1. Add VPC peering requests

1. Log in to the [TiDB Cloud console](https://tidbcloud.com).
2. Click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner, switch to the target project if you have multiple projects, and then click **Project Settings**.
3. On the **Project Settings** page of your project, click **Network Access** in the left navigation pane, and then click the **VPC Peering** tab.

    The **VPC Peering** configuration is displayed by default.

4. Click **Add**, choose the AWS icon, and then fill in the required information of your existing AWS VPC:

    - Region
    - AWS Account ID
    - VPC ID
    - VPC CIDR

    You can get these information from your VPC details on the VPC dashboard.

    ![VPC peering](/media/tidb-cloud/vpc-peering/vpc-peering-creating-infos.png)

5. Click **Initialize**. The **Approve VPC Peerings** dialog is displayed.

### Step 2. Approve and configure the VPC peering

Use either of the following two options to approve and configure the VPC peering connection:

- [Option 1: Use AWS CLI](#option-1-use-aws-cli)
- [Option 2: Use the AWS dashboard](#option-2-use-the-aws-dashboard)

#### Option 1. Use AWS CLI

1. Install AWS Command Line Interface (AWS CLI).

    {{< copyable "shell-regular" >}}

    ```bash
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
    ```

2. Configure AWS CLI according to your account information. To get the information required by AWS CLI, see [AWS CLI configuration basics](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html).

    {{< copyable "shell-regular" >}}

    ```bash
    aws configure
    ```

3. Replace the following variable values with your account information.

    {{< copyable "shell-regular" >}}

    ```bash
    # Sets up the related variables.
    pcx_tidb_to_app_id="<TiDB peering id>"
    app_region="<APP Region>"
    app_vpc_id="<Your VPC ID>"
    tidbcloud_project_cidr="<TiDB Cloud Project VPC CIDR>"
    ```

    For example:

    ```
    # Sets up the related variables
    pcx_tidb_to_app_id="pcx-069f41efddcff66c8"
    app_region="us-west-2"
    app_vpc_id="vpc-0039fb90bb5cf8698"
    tidbcloud_project_cidr="10.250.0.0/16"
    ```

4. Run the following commands.

    {{< copyable "shell-regular" >}}

    ```bash
    # Accepts the VPC peering connection request.
    aws ec2 accept-vpc-peering-connection --vpc-peering-connection-id "$pcx_tidb_to_app_id"
    ```

    {{< copyable "shell-regular" >}}

    ```bash
    # Creates route table rules.
    aws ec2 describe-route-tables --region "$app_region" --filters Name=vpc-id,Values="$app_vpc_id" --query 'RouteTables[*].RouteTableId' --output text | tr "\t" "\n" | while read row
    do
        app_route_table_id="$row"
        aws ec2 create-route --route-table-id "$app_route_table_id" --destination-cidr-block "$tidbcloud_project_cidr" --vpc-peering-connection-id "$pcx_tidb_to_app_id"
    done
    ```

    > **Note:**
    >
    > Sometimes, even if the route table rules are successfully created, you might still get the `An error occurred (MissingParameter) when calling the CreateRoute operation: The request must contain the parameter routeTableId` error. In this case, you can check the created rules and ignore the error.

    {{< copyable "shell-regular" >}}

    ```bash
    # Modifies the VPC attribute to enable DNS-hostname and DNS-support.
    aws ec2 modify-vpc-attribute --vpc-id "$app_vpc_id" --enable-dns-hostnames
    aws ec2 modify-vpc-attribute --vpc-id "$app_vpc_id" --enable-dns-support
    ```

After finishing the configuration, the VPC peering has been created. You can [connect to the TiDB cluster](#connect-to-the-tidb-cluster) to verify the result.

#### Option 2. Use the AWS dashboard

You can also use the AWS dashboard to configure the VPC peering connection.

1. Confirm to accept the peer connection request in your AWS console.

    1. Sign in to the AWS console and click **Services** on the top menu bar. Enter `VPC` in the search box and go to the VPC service page.

        ![AWS dashboard](/media/tidb-cloud/vpc-peering/aws-vpc-guide-1.jpg)

    2. From the left navigation bar, open the **Peering Connections** page. On the **Create Peering Connection** tab, a peering connection is in the **Pending Acceptance** status.

    3. Confirm the requester owner is TiDB Cloud (`380838443567`). Right-click the peering connection and select **Accept Request** to accept the request in the **Accept VPC peering connection request** dialog.

        ![AWS VPC peering requests](/media/tidb-cloud/vpc-peering/aws-vpc-guide-3.png)

2. Add a route to the TiDB Cloud VPC for each of your VPC subnet route tables.

    1. From the left navigation bar, open the **Route Tables** page.

    2. Search all the route tables that belong to your application VPC.

        ![Search all route tables related to VPC](/media/tidb-cloud/vpc-peering/aws-vpc-guide-4.png)

    3. Right-click each route table and select **Edit routes**. On the edit page, add a route with a destination to the Project CIDR (by checking the **VPC Peering** configuration page in the TiDB Cloud console) and fill in your peering connection ID in the **Target** column.

        ![Edit all route tables](/media/tidb-cloud/vpc-peering/aws-vpc-guide-5.png)

3. Make sure you have enabled private DNS hosted zone support for your VPC.

    1. From the left navigation bar, open the **Your VPCs** page.

    2. Select your application VPC.

    3. Right click on the selected VPC. The setting drop-down list displays.

    4. From the setting drop-down list, click **Edit DNS hostnames**. Enable DNS hostnames and click **Save**.

    5. From the setting drop-down list, click **Edit DNS resolution**. Enable DNS resolution and click **Save**.

Now you have successfully set up the VPC peering connection. Next, [connect to the TiDB cluster via VPC peering](#connect-to-the-tidb-cluster).

## Set up VPC peering on Google Cloud

1. Log in to the [TiDB Cloud console](https://tidbcloud.com).
2. Click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner, switch to the target project if you have multiple projects, and then click **Project Settings**.
3. On the **Project Settings** page of your project, click **Network Access** in the left navigation pane, and then click the **VPC Peering** tab.

    The **VPC Peering** configuration is displayed by default.

4. Click **Add**, choose the Google Cloud icon, and then fill in the required information of your existing Google Cloud VPC:

    > **Tip:**
    >
    > You can follow instructions next to the **Application Google Cloud Project ID** and **VPC Network Name** fields to find the project ID and VPC network name.

    - Region
    - Application Google Cloud Project ID
    - VPC Network Name
    - VPC CIDR

5. Click **Initialize**. The **Approve VPC Peerings** dialog is displayed.

6. Check the connection information of your TiDB VPC peerings.

    ![VPC-Peering](/media/tidb-cloud/VPC-Peering3.png)

7. Execute the following command to finish the setup of VPC peerings:

    {{< copyable "shell-regular" >}}

    ```bash
    gcloud beta compute networks peerings create <your-peer-name> --project <your-project-id> --network <your-vpc-network-name> --peer-project <tidb-project-id> --peer-network <tidb-vpc-network-name>
    ```

    > **Note:**
    >
    > You can name `<your-peer-name>` as you like.

Now you have successfully set up the VPC peering connection. Next, [connect to the TiDB cluster via VPC peering](#connect-to-the-tidb-cluster).

## Connect to the TiDB cluster

1. On the [**Clusters**](https://tidbcloud.com/console/clusters) page, click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner, and select the **VPC Peering** tab in the connection dialog.

    You can see the **Status** of the VPC peering is **active**. If **Status** is still **system checking**, wait for about 5 minutes and open the dialog again.

3. Click **Get Endpoint** and wait for a few minutes. Then the connection command is displayed in the dialog.

4. Under **Step 2: Connect with a SQL client** in the dialog box, click the tab of your preferred connection method, and then connect to your cluster with the connection string.
