---
title: Connect to TiDB Serverless via Private Endpoint
summary: Learn how to connect to your TiDB Cloud cluster via private endpoint.
---

# Connect to TiDB Serverless via Private Endpoint

This document describes how to connect to your TiDB Serverless cluster via private endpoint.

> **Tip:**
>
> To learn how to connect to a TiDB Dedicated cluster via private endpoint with AWS, see [Connect to TiDB Dedicated via Private Endpoint with AWS](/tidb-cloud/set-up-private-endpoint-connections.md).
> To learn how to connect to a TiDB Dedicated cluster via private endpoint with Google Cloud, see [Connect to TiDB Dedicated via Private Service Connect with Google Cloud](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md).

TiDB Cloud supports highly secure and one-way access to the TiDB Cloud service hosted in an AWS VPC via the [AWS PrivateLink](https://aws.amazon.com/privatelink/?privatelink-blogs.sort-by=item.additionalFields.createdDate&privatelink-blogs.sort-order=desc), as if the service were in your own VPC. A private endpoint is exposed in your VPC and you can create a connection to the TiDB Cloud service via the endpoint with permission.

Powered by AWS PrivateLink, the endpoint connection is secure and private, and does not expose your data to the public internet. In addition, the endpoint connection supports CIDR overlap and is easier for network management.

The architecture of the private endpoint is as follows:

![Private endpoint architecture](/media/tidb-cloud/aws-private-endpoint-arch.png)

For more detailed definitions of the private endpoint and endpoint service, see the following AWS documents:

- [What is AWS PrivateLink?](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html)
- [AWS PrivateLink concepts](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html)

## Restrictions

- Currently, TiDB Cloud supports private endpoint connection to TiDB Serverless only when the endpoint service is hosted in AWS. If the service is hosted in Google Cloud, the private endpoint is not applicable.
- Private endpoint connection across regions is not supported.

## Set up a private endpoint with AWS

To connect to your TiDB Serverless cluster via a private endpoint, follow these steps:

1. [Choose a TiDB cluster](#step-1-choose-a-tidb-cluster)
2. [Create an AWS interface endpoint](#step-2-create-an-aws-interface-endpoint)
3. [Connect to your TiDB cluster](#step-3-connect-to-your-tidb-cluster)

### Step 1. Choose a TiDB cluster

1. On the [**Clusters**](https://tidbcloud.com/console/clusters) page, click the name of your target TiDB Serverless cluster to go to its overview page.
2. Click **Connect** in the upper-right corner. A connection dialog is displayed.
3. In the **Endpoint Type** drop-down list, select **Private**.
4. Take a note of **Service Name**, **Availability Zone ID**, and **Region ID**.

    > **Note:**
    >
    >  You only need to create one private endpoint per AWS region, which can be shared by all TiDB Serverless clusters located in the same region.

### Step 2. Create an AWS interface endpoint

<SimpleTab>
<div label="Use AWS Console">

To use the AWS Management Console to create a VPC interface endpoint, perform the following steps:

1. Sign in to the [AWS Management Console](https://aws.amazon.com/console/) and open the Amazon VPC console at <https://console.aws.amazon.com/vpc/>.
2. Click **Endpoints** in the navigation pane, and then click **Create Endpoint** in the upper-right corner.

    The **Create endpoint** page is displayed.

    ![Verify endpoint service](/media/tidb-cloud/private-endpoint/create-endpoint-2.png)

3. Select **Other endpoint services**.
4. Enter the service name that you found in [step 1](#step-1-choose-a-tidb-cluster).
5. Click **Verify service**.
6. Select your VPC in the drop-down list. Expand **Additional settings** and select the **Enable DNS name** checkbox.
7. In the **Subnets** area, select the availability zone where your TiDB cluster is located, and select the Subnet ID.
8. Select your security group properly in the **Security groups** area.

    > **Note:**
    >
    >  Make sure the selected security group allows inbound access from your EC2 instances on port 4000.

9. Click **Create endpoint**.

</div>
<div label="Use AWS CLI">

To use the AWS CLI to create a VPC interface endpoint, perform the following steps:

1. To get the **VPC ID** and **Subnet ID**, navigate to your AWS Management Console, and locate them in the relevant sections. Make sure that you fill in the **Availability Zone ID** that you found in [step 1](#step-1-choose-a-tidb-cluster).
2. Copy the command provided below, replace the relevant arguments with the information you obtained, and then execute it in your terminal.

```bash
aws ec2 create-vpc-endpoint --vpc-id ${your_vpc_id} --region ${region_id} --service-name ${service_name} --vpc-endpoint-type Interface --subnet-ids ${your_subnet_id}
```

> **Tip:**
>
> Before running the command, you need to have AWS CLI installed and configured. See [AWS CLI configuration basics](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html) for details.

</div>
</SimpleTab>

Then you can connect to the endpoint service with the private DNS name.

### Step 3: Connect to your TiDB cluster

After you have created the interface endpoint, go back to the TiDB Cloud console and take the following steps:

1. On the [**Clusters**](https://tidbcloud.com/console/clusters) page, click the name of your target cluster to go to its overview page.
2. Click **Connect** in the upper-right corner. A connection dialog is displayed.
3. In the **Endpoint Type** drop-down list, select **Private**.
4. In the **Connect With** drop-down list, select your preferred connection method. The corresponding connection string is displayed at the bottom of the dialog.
5. Connect to your cluster with the connection string.

> **Tip:**
>
> If you cannot connect to the cluster, the reason might be that the security group of your VPC endpoint in AWS is not properly set. See [this FAQ](#troubleshooting) for solutions.
>
> When creating a VPC endpoint, if you encounter an error `private-dns-enabled cannot be set because there is already a conflicting DNS domain for gatewayXX-privatelink.XX.prod.aws.tidbcloud.com in the VPC vpc-XXXXX`, it is due to that a private endpoint has already been created, and creating a new one is unnecessary.

## Troubleshooting

### I cannot connect to a TiDB cluster via a private endpoint after enabling private DNS. Why?

You might need to properly set the security group for your VPC endpoint in the AWS Management Console. Go to **VPC** > **Endpoints**. Right-click your VPC endpoint and select the proper **Manage security groups**. A proper security group within your VPC that allows inbound access from your EC2 instances on Port 4000 or a customer-defined port.

![Manage security groups](/media/tidb-cloud/private-endpoint/manage-security-groups.png)

### I cannot enable private DNS. An error is reported indicating that the `enableDnsSupport` and `enableDnsHostnames` VPC attributes are not enabled

Make sure that DNS hostname and DNS resolution are both enabled in your VPC setting. They are disabled by default when you create a VPC in the AWS Management Console.
