---
title: Connect AWS DMS to TiDB Cloud clusters
summary: Learn how to migrate data from or into TiDB Cloud using AWS Database Migration Service (AWS DMS).
---

# Connect AWS DMS to TiDB Cloud clusters

[AWS Database Migration Service (AWS DMS)](https://aws.amazon.com/dms/) is a cloud service that makes it possible to migrate relational databases, data warehouses, NoSQL databases, and other types of data stores. You can use AWS DMS to migrate your data from or into TiDB Cloud clusters. This document describes how to connect AWS DMS to a TiDB Cloud cluster.

## Prerequisites

### An AWS account with enough access

You are expected to have an AWS account with enough access to manage DMS-related resources. If not, refer to the following AWS documents:

- [Sign up for an AWS account](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_GettingStarted.SettingUp.html#sign-up-for-aws)
- [Identity and access management for AWS Database Migration Service](https://docs.aws.amazon.com/dms/latest/userguide/security-iam.html)

### A TiDB Cloud account and a TiDB cluster

You are expected to have a TiDB Cloud account and a TiDB Serverless or TiDB Dedicated cluster. If not, refer to the following documents to create one:

- [Create a TiDB Serverless cluster](/tidb-cloud/create-tidb-cluster-serverless.md)
- [Create a TiDB Dedicated cluster](/tidb-cloud/create-tidb-cluster.md)

## Configure network

Before creating DMS resources, you need to configure network properly to ensure DMS can communicate with TiDB Cloud clusters. If you are unfamiliar with AWS, contact AWS Support. The following provides several possible configurations for your reference.

<SimpleTab>

<div label="TiDB Serverless">

For TiDB Serverless, your clients can connect to clusters via public endpoint or private endpoint.

- To [connect to a TiDB Serverless cluster via public endpoint](/tidb-cloud/connect-via-standard-connection-serverless.md), do one of the following to make sure that the DMS replication instance can access the internet.

    - Deploy the replication instance in public subnets and enable **Public accessible**. For more information, see [Configuration for internet access](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html#vpc-igw-internet-access).

    - Deploy the replication instance in private subnets and route traffic in the private subnets to public subnets. In this case, you need at least three subnets, two private subnets, and one public subnet. The two private subnets form a subnet group where the replication instance lives. Then you need to create a NAT gateway in the public subnet and route traffic of the two private subnets to the NAT gateway. For more information, see [Access the internet from a private subnet](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-scenarios.html#public-nat-internet-access).

- To connect to a TiDB Serverless cluster via private endpoint, [set up a private endpoint](/tidb-cloud/set-up-private-endpoint-connections-serverless.md) first and deploy the replication instance in private subnets.

</div>

<div label="TiDB Dedicated">

For TiDB Dedicated, your clients can connect to clusters via public endpoint, private endpoint, or VPC peering.

- To [connect to a TiDB Dedicated cluster via public endpoint](/tidb-cloud/connect-via-standard-connection.md), do one of the following to make sure that the DMS replication instance can access the internet. In addition, you need to add the public IP address of the replication instance or NAT gateway to the cluster's [IP access list](/tidb-cloud/configure-ip-access-list.md).

    - Deploy the replication instance in public subnets and enable **Public accessible**. For more information, see [Configuration for internet access](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html#vpc-igw-internet-access).

    - Deploy the replication instance in private subnets and route traffic in the private subnets to public subnets. In this case, you need at least three subnets, two private subnets, and one public subnet. The two private subnets form a subnet group where the replication instance lives. Then you need to create a NAT gateway in the public subnet and route traffic of the two private subnets to the NAT gateway. For more information, see [Access the internet from a private subnet](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-scenarios.html#public-nat-internet-access).

- To connect to a TiDB Dedicated cluster via private endpoint, [set up a private endpoint](/tidb-cloud/set-up-private-endpoint-connections.md) first and deploy the replication instance in private subnets.

- To connect to a TiDB Dedicated cluster via VPC peering, [set up a VPC peering connection](/tidb-cloud/set-up-vpc-peering-connections.md) first and deploy the replication instance in private subnets.

</div>
</SimpleTab>

## Create an AWS DMS replication instance

1. In the AWS DMS console, go to the [**Replication instances**](https://console.aws.amazon.com/dms/v2/home#replicationInstances) page and switch to the corresponding region. It is recommended to use the same region for AWS DMS as TiDB Cloud.

   ![Create replication instance](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-connect-replication-instances.png)

2. Click **Create replication instance**.

3. Fill in an instance name, ARN, and description.

4. In the **Instance configuration** section, configure the instance:
    - **Instance class**: select an appropriate instance class. For more information, see [Choosing replication instance types](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_ReplicationInstance.Types.html).
    - **Engine version**: keep the default configuration.
    - **High Availability**: select **Multi-AZ** or **Single-AZ** based on your business needs.

5. Configure the storage in the **Allocated storage (GiB)** field.

6. Configure connectivity and security. You can refer to [the previous section](#configure-network) for network configuration.

    - **Network type - new**: select **IPv4**.
    - **Virtual private cloud (VPC) for IPv4**: select the VPC that you need.
    - **Replication subnet group**: select a subnet group for your replication instance.
    - **Public accessible**: set it based on your network configuration.

    ![Connectivity and security](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-connect-connectivity-security.png)

7. Configure the **Advanced settings**, **Maintenance**, and **Tags** sections if needed, and then click **Create replication instance** to finish the instance creation.

> **Note:**
>
> AWS DMS also supports serverless replications. For detailed steps, see [Creating a serverless replication](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Serverless.Components.html#CHAP_Serverless.create). Unlike replication instances, AWS DMS serverless replications do not provide the **Public accessible** option.

## Create TiDB Cloud DMS endpoints

For connectivity, the steps for using TiDB Cloud clusters as a source or as a target are similar, but DMS does have some different database setting requirements for source and target. For more information, see [Using MySQL as a source](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.MySQL.html) or [Using MySQL as a target](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.MySQL.html). When using a TiDB Cloud cluster as a source, you can only **Migrate existing data** because TiDB does not support MySQL binlog.

1. In the AWS DMS console, go to the [**Endpoints**](https://console.aws.amazon.com/dms/v2/home#endpointList) page and switch to the corresponding region.

    ![Create endpoint](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-connect-create-endpoint.png)

2. Click **Create endpoint** to create the target database endpoint.

3. In the **Endpoint type** section, select **Source endpoint** or **Target endpoint**.

4. In the **Endpoint configuration** section, fill in the **Endpoint identifier** and ARN fields. Then, select **MySQL** as **Source engine** or **Target engine**.

5. For the **Access to endpoint database** field, select the **Provide access information manually** checkbox and fill in cluster information as follows:

    <SimpleTab>

    <div label="TiDB Serverless">

    - **Server name**: `HOST` of TiDB Serverless cluster.
    - **Port**: `PORT` of TiDB Serverless cluster.
    - **User name**: User of TiDB Serverless cluster for migration. Make sure it meets DMS requirements.
    - **Password**: Password of the TiDB Serverless cluster user.
    - **Secure Socket Layer (SSL) mode**: If you are connecting via public endpoint, it is highly recommended to set the mode to **verify-full** to ensure transport security. If you are connecting via private endpoint, you can set the mode to **none**.
    - (Optional) **CA certificate**: Use the [ISRG Root X1 certificate](https://letsencrypt.org/certs/isrgrootx1.pem). For more information, see [TLS Connections to TiDB Serverless](/tidb-cloud/secure-connections-to-serverless-clusters.md).

    </div>

    <div label="TiDB Dedicated">

    - **Server name**: `HOST` of TiDB Dedicated cluster.
    - **Port**: `PORT` of TiDB Dedicated cluster.
    - **User name**: User of TiDB Dedicated cluster for migration. Make sure it meets DMS requirements.
    - **Password**: Password of TiDB Dedicated cluster user.
    - **Secure Socket Layer (SSL) mode**: If you are connecting via public endpoint, it is highly recommended to set the mode to **verify-full** to ensure transport security. If you are connecting via private endpoint, you can set it to **none**.
    - (Optional) **CA certificate**: Get the CA certificate according to [TLS connections to TiDB Dedicated](/tidb-cloud/tidb-cloud-tls-connect-to-dedicated.md).

    </div>
    </SimpleTab>

     ![Provide access information manually](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-connect-configure-endpoint.png)

6. If you want to create the endpoint as a **Target endpoint**, expand the **Endpoint settings** section, select the **Use endpoint connection attributes** checkbox, and then set **Extra connection attributes** to `Initstmt=SET FOREIGN_KEY_CHECKS=0;`.

7. Configure the **KMS Key** and **Tags** sections if needed. Click **Create endpoint** to finish the instance creation.
