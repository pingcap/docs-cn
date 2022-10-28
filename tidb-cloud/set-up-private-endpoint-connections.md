---
title: Set Up Private Endpoint Connections
summary: Learn how to set up private endpoint connections in TiDB Cloud.
---

# Set Up Private Endpoint Connections

TiDB Cloud supports highly secure and one-way access to the TiDB Cloud service hosted in an AWS VPC via the [AWS PrivateLink](https://aws.amazon.com/privatelink/?privatelink-blogs.sort-by=item.additionalFields.createdDate&privatelink-blogs.sort-order=desc), as if the service were in your own VPC. A private endpoint is exposed in your VPC and you can create a connection to the TiDB Cloud service via the endpoint with permission.

Powered by AWS PrivateLink, the endpoint connection is secure and private, and does not expose your data to the public internet. In addition, the endpoint connection supports CIDR overlap and is easier for network management.

The architecture of the private endpoint is as follows:

![Private endpoint architecture](/media/tidb-cloud/aws-private-endpoint-arch.png)

For more detailed definitions of the private endpoint and endpoint service, see the following AWS documents:

- [What is AWS PrivateLink?](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html)
- [AWS PrivateLink concepts](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html)

## Restrictions

- Currently, TiDB Cloud supports private endpoint connection only when the endpoint service is hosted in AWS. If the service is hosted in Google Cloud Platform (GCP), the private endpoint is not applicable.
- The private endpoint support is provided only for the TiDB Cloud Dedicated Tier, not for the Serverless Tier.
- Private endpoint connection across regions is not supported.

In most scenarios, you are recommended to use private endpoint connection over VPC peering. However, in the following scenarios, you should use VPC peering instead of private endpoint connection:

- You are using a [TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview) cluster to replicate data from a source TiDB cluster to a target TiDB cluster across regions, to get high availability. Currently, private endpoint does not support cross-region connection.
- You are using a TiCDC cluster to replicate data to a downstream cluster (such as Amazon Aurora, MySQL, and Kafka) but you cannot maintain the endpoint service on your own.
- You are connecting to PD or TiKV nodes directly.

## Set up a private endpoint with AWS

This section describes how to set up a private endpoint with AWS PrivateLink.

In addition to the [prerequisites](#prerequisites), there are 5 steps to set up a private endpoint connection with AWS PrivateLink:

1. [Choose a TiDB cluster](#step-1-choose-a-tidb-cluster)
2. [Check the service endpoint region](#step-2-check-the-service-endpoint-region)
3. [Create an AWS interface endpoint](#step-3-create-an-aws-interface-endpoint)
4. [Accept the endpoint connection](#step-4-accept-the-endpoint-connection)
5. [Enable private DNS](#step-5-enable-private-dns)

If you have multiple clusters, you need to repeat these steps for each cluster that you want to connect to using AWS PrivateLink.

### Prerequisites

TiDB Cloud supports private endpoints only for Dedicated Tier clusters. You are expected to create a Dedicated Tier cluster before creating a private endpoint. For detailed instructions, see [Create a TiDB Cluster in TiDB Cloud](/tidb-cloud/create-tidb-cluster.md).

To start setting up a private endpoint, open the private endpoint creation page:

1. Click the **Project Settings** tab in the TiDB Cloud console.
2. Click **Private Endpoint** on the left menu.
3. Click **Add** on the **Private Endpoint** page.

### Step 1. Choose a TiDB cluster

1. Click the drop-down list and choose an available TiDB cluster.
2. Click **Next**.

### Step 2. Check the service endpoint region

Your service endpoint region is selected by default. Have a quick check and click **Next**.

> **Note:**
>
> The default region is where your cluster is located. Do not change it. Cross-region private endpoint is currently not supported.

### Step 3. Create an AWS interface endpoint

TiDB Cloud begins creating an endpoint service, which takes 3 to 4 minutes.

When the endpoint service is created, take a note of your endpoint service name from the command in the lower area of the console.

```bash
aws ec2 create-vpc-endpoint --vpc-id <your_vpc_id> --region <your_region> --service-name <your_endpoint_service_name> --vpc-endpoint-type Interface --subnet-ids <your_application_subnet_ids>
```

Then create an AWS interface endpoint either using the AWS Management Console or using the AWS CLI.

<SimpleTab>
<div label="Use AWS Console">

To use the AWS Management Console to create a VPC interface endpoint, perform the following steps:

1. Go to **VPC** > **Endpoints**.
2. Click **Create Endpoint**.

    The **Create endpoint** page is displayed.

    ![Verify endpoint service](/media/tidb-cloud/private-endpoint/create-endpoint-2.png)

3. Select **Other endpoint services**.
4. Enter the endpoint service name.
5. Click **Verify service**.
6. Select your VPC in the drop-down list.
7. Select the availability zones where your TiDB cluster is located in the **Subnets** area.

    > **Tip:**
    >
    > If your service is spanning across more than three availability zones (AZs), you might not be able to select AZs in the **Subnets** area. This issue occurs when there is an extra AZ in your selected region in addition to the AZs where your TiDB cluster is located. In this case, contact [PingCAP Technical Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support).

8. Select your security group properly in the **Security groups** area.
   
    > **Note:**
    >
    >  Make sure the selected security group allows inbound access from your EC2 instances on Port 4000 or a customer-defined port.
 
9. Click **Create endpoint**.

</div>
<div label="Use AWS CLI">

To use the AWS CLI to create a VPC interface endpoint, perform the following steps:

1. Fill in the **VPC ID** and **Subnet IDs** fields on the private endpoint creation page. You can get the IDs from your AWS Management Console.
2. Copy the command in the lower area of the page and run it in your terminal. Then click **Next**.

> **Tip:**
>
> - Before running the command, you need to have AWS CLI installed and configured. See [AWS CLI configuration basics](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html) for details.
>
> - If your service is spanning across more than three availability zones (AZs), you will get an error message indicating that the VPC endpoint service does not support the AZ of the subnet. This issue occurs when there is an extra AZ in your selected region in addition to the AZs where your TiDB cluster is located. In this case, you can contact [PingCAP Technical Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support).
>
> - You cannot copy the command until TiDB Cloud finishes creating an endpoint service in the background.

</div>
</SimpleTab>

### Step 4. Accept the endpoint connection

1. Go back to the TiDB Cloud console.
2. Fill in the box with your VPC endpoint ID on the **Create Private Endpoint** page.
3. Click **Next**.

### Step 5. Enable private DNS

Enable private DNS in AWS. You can either use the AWS Management Console or the AWS CLI.

<SimpleTab>
<div label="Use AWS Console">

To enable private DNS in your AWS Management Console:

1. Go to **VPC** > **Endpoints**.
2. Right-click your endpoint ID and select **Modify private DNS name**.
3. Select the **Enable for this endpoint** check box.
4. Click **Save changes**.

    ![Enable private DNS](/media/tidb-cloud/private-endpoint/enable-private-dns.png)

</div>
<div label="Use AWS CLI">

To enable private DNS using your AWS CLI, copy the command and run it in your AWS CLI.

```bash
aws ec2 modify-vpc-endpoint --vpc-endpoint-id <your_vpc_endpoint_id> --private-dns-enabled
```

</div>
</SimpleTab>

Click **Create** in the TiDB Cloud console to finalize the creation of the private endpoint.

Then you can connect to the endpoint service. See [Connect to TiDB cluster via private endpoint](/tidb-cloud/connect-to-tidb-cluster.md#connect-via-private-endpoint-recommended) for details.

## Private endpoint status reference

When you use private endpoint connections, the statuses of private endpoints or private endpoint services are displayed on the [**Private Endpoint** page](#prerequisites).

The possible statuses of a private endpoint are explained as follows:

- **Not Configured**: You have just created an endpoint service but have not yet created a private endpoint.
- **Pending**: Waiting for processing.
- **Active**: Your private endpoint is ready to use. You cannot edit the private endpoint of this status.
- **Deleting**: The private endpoint is being deleted.
- **Failed**: The private endpoint creation fails. You can click **Edit** of that row to retry the creation.

The possible statuses of a private endpoint service are explained as follows:

- **Creating**: The endpoint service is being created, which takes 3 to 5 minutes.
- **Active**: The endpoint service is created, no matter whether the private endpoint is created or not.
- **Deleting**: The endpoint service or the cluster is being deleted, which takes 3 to 5 minutes.

## Troubleshooting

### I cannot connect to a TiDB cluster via a private endpoint after enabling private DNS. Why?

You might need to properly set the security group for your VPC endpoint in the AWS Management Console. Go to **VPC** > **Endpoints**. Right-click your VPC endpoint and select the proper **Manage security groups**. A proper security group within your VPC that allows inbound access from your EC2 instances on Port 4000 or a customer-defined port.

![Manage security groups](/media/tidb-cloud/private-endpoint/manage-security-groups.png)

### I cannot enable private DNS. An error is reported indicating that the `enableDnsSupport` and `enableDnsHostnames` VPC attributes are not enabled

Make sure that DNS hostname and DNS resolution are both enabled in your VPC setting. They are disabled by default when you create a VPC in the AWS Management Console.
