---
title: Integrate TiDB with Amazon AppFlow
summary: Introduce how to integrate TiDB with Amazon AppFlow step by step.
---

# Integrate TiDB with Amazon AppFlow

[Amazon AppFlow](https://aws.amazon.com/appflow/) is a fully managed API integration service that you use to connect your software as a service (SaaS) applications to AWS services, and securely transfer data. With Amazon AppFlow, you can import and export data from and to TiDB into many types of data providers, such as Salesforce, Amazon S3, LinkedIn, and GitHub. For more information, see [Supported source and destination applications](https://docs.aws.amazon.com/appflow/latest/userguide/app-specific.html) in AWS documentation.

This document describes how to integrate TiDB with Amazon AppFlow and takes integrating a TiDB Serverless cluster as an example.

If you do not have a TiDB cluster, you can create a [TiDB Serverless](https://tidbcloud.com/console/clusters) cluster, which is free and can be created in approximately 30 seconds.

## Prerequisites

- [Git](https://git-scm.com/)
- [JDK](https://openjdk.org/install/) 11 or above
- [Maven](https://maven.apache.org/install.html) 3.8 or above
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) version 2
- [AWS Serverless Application Model Command Line Interface (AWS SAM CLI)](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) 1.58.0 or above
- An AWS [Identity and Access Management (IAM) user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html) with the following requirements:

    - The user can access AWS using an [access key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html).
    - The user has the following permissions:

        - `AWSCertificateManagerFullAccess`: used for reading and writing the [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/).
        - `AWSCloudFormationFullAccess`: SAM CLI uses [AWS CloudFormation](https://aws.amazon.com/cloudformation/) to proclaim the AWS resources.
        - `AmazonS3FullAccess`: AWS CloudFormation uses [Amazon S3](https://aws.amazon.com/s3/?nc2=h_ql_prod_fs_s3) to publish.
        - `AWSLambda_FullAccess`: currently, [AWS Lambda](https://aws.amazon.com/lambda/?nc2=h_ql_prod_fs_lbd) is the only way to implement a new connector for Amazon AppFlow.
        - `IAMFullAccess`: SAM CLI needs to create a `ConnectorFunctionRole` for the connector.

- A [SalesForce](https://developer.salesforce.com) account.

## Step 1. Register a TiDB connector

### Clone the code

Clone the [integration example code repository](https://github.com/pingcap-inc/tidb-appflow-integration) for TiDB and Amazon AppFlow:

```bash
git clone https://github.com/pingcap-inc/tidb-appflow-integration
```

### Build and upload a Lambda

1. Build the package:

    ```bash
    cd tidb-appflow-integration
    mvn clean package
    ```

2. (Optional) Configure your AWS access key ID and secret access key if you have not.

    ```bash
    aws configure
    ```

3. Upload your JAR package as a Lambda:

    ```bash
    sam deploy --guided
    ```

    > **Note:**
    >
    > - The `--guided` option uses prompts to guide you through the deployment. Your input will be stored in a configuration file, which is `samconfig.toml` by default.
    > - `stack_name` specifies the name of AWS Lambda that you are deploying.
    > - This prompted guide uses AWS as the cloud provider of TiDB Serverless. To use Amazon S3 as the source or destination, you need to set the `region` of AWS Lambda as the same as that of Amazon S3.
    > - If you have already run `sam deploy --guided` before, you can just run `sam deploy` instead, and SAM CLI will use the configuration file `samconfig.toml` to simplify the interaction.

    If you see a similar output as follows, this Lambda is successfully deployed.

    ```
    Successfully created/updated stack - <stack_name> in <region>
    ```

4. Go to the [AWS Lambda console](https://console.aws.amazon.com/lambda/home), and you can see the Lambda that you just uploaded. Note that you need to select the correct region in the upper-right corner of the window.

    ![lambda dashboard](/media/develop/aws-appflow-step-lambda-dashboard.png)

### Use Lambda to register a connector

1. In the [AWS Management Console](https://console.aws.amazon.com), navigate to [Amazon AppFlow > Connectors](https://console.aws.amazon.com/appflow/home#/gallery) and click **Register new connector**.

    ![register connector](/media/develop/aws-appflow-step-register-connector.png)

2. In the **Register a new connector** dialog, choose the Lambda function you uploaded and specify the connector label using the connector name.

    ![register connector dialog](/media/develop/aws-appflow-step-register-connector-dialog.png)

3. Click **Register**. Then, a TiDB connector is registered successfully.

## Step 2. Create a flow

Navigate to [Amazon AppFlow > Flows](https://console.aws.amazon.com/appflow/home#/list) and click **Create flow**.

![create flow](/media/develop/aws-appflow-step-create-flow.png)

### Set the flow name

Enter the flow name, and then click **Next**.

![name flow](/media/develop/aws-appflow-step-name-flow.png)

### Set the source and destination tables

Choose the **Source details** and **Destination details**. TiDB connector can be used in both of them.

1. Choose the source name. This document uses **Salesforce** as an example source.

    ![salesforce source](/media/develop/aws-appflow-step-salesforce-source.png)

    After you register to Salesforce, Salesforce will add some example data to your platform. The following steps will use the **Account** object as an example source object.

    ![salesforce data](/media/develop/aws-appflow-step-salesforce-data.png)

2. Click **Connect**.

    1. In the **Connect to Salesforce** dialog, specify the name of this connection, and then click **Continue**.

        ![connect to salesforce](/media/develop/aws-appflow-step-connect-to-salesforce.png)

    2. Click **Allow** to confirm that AWS can read your Salesforce data.

        ![allow salesforce](/media/develop/aws-appflow-step-allow-salesforce.png)

    > **Note:**
    >
    > If your company has already used the Professional Edition of Salesforce, the REST API is not enabled by default. You might need to register a new Developer Edition to use the REST API. For more information, refer to [Salesforce Forum Topic](https://developer.salesforce.com/forums/?id=906F0000000D9Y2IAK).

3. In the **Destination details** area, choose **TiDB-Connector** as the destination. The **Connect** button is displayed.

    ![tidb dest](/media/develop/aws-appflow-step-tidb-dest.png)

4. Before clicking **Connect**, you need to create a `sf_account` table in TiDB for the Salesforce **Account** object. Note that this table schema is different from the sample data in [Tutorial of Amazon AppFlow](https://docs.aws.amazon.com/appflow/latest/userguide/flow-tutorial-set-up-source.html).

    ```sql
    CREATE TABLE `sf_account` (
        `id` varchar(255) NOT NULL,
        `name` varchar(150) NOT NULL DEFAULT '',
        `type` varchar(150) NOT NULL DEFAULT '',
        `billing_state` varchar(255) NOT NULL DEFAULT '',
        `rating` varchar(255) NOT NULL DEFAULT '',
        `industry` varchar(255) NOT NULL DEFAULT '',
        PRIMARY KEY (`id`)
    );
    ```

5. After the `sf_account` table is created, click **Connect**. A connection dialog is displayed.
6. In the **Connect to TiDB-Connector** dialog, enter the connection properties of the TiDB cluster. If you use a TiDB Serverless cluster, you need to set the **TLS** option to `Yes`, which lets the TiDB connector use the TLS connection. Then, click **Connect**.

    ![tidb connection message](/media/develop/aws-appflow-step-tidb-connection-message.png)

7. Now you can get all tables in the database that you specified for connection. Choose the **sf_account** table from the drop-down list.

    ![database](/media/develop/aws-appflow-step-database.png)

    The following screenshot shows the configurations to transfer data from the Salesforce **Account** object to the `sf_account` table in TiDB:

    ![complete flow](/media/develop/aws-appflow-step-complete-flow.png)

8. In the **Error handling** area, choose **Stop the current flow run**. In the **Flow trigger** area, choose the **Run on demand** trigger type, which means you need to run the flow manually. Then, click **Next**.

    ![complete step1](/media/develop/aws-appflow-step-complete-step1.png)

### Set mapping rules

Map the fields of the **Account** object in Salesforce to the `sf_account` table in TiDB, and then click **Next**.

- The `sf_account` table is newly created in TiDB and it is empty.

    ```sql
    test> SELECT * FROM sf_account;
    +----+------+------+---------------+--------+----------+
    | id | name | type | billing_state | rating | industry |
    +----+------+------+---------------+--------+----------+
    +----+------+------+---------------+--------+----------+
    ```

- To set a mapping rule, you can select a source field name on the left, and select a destination field name on the right. Then, click **Map fields**, and a rule is set.

    ![add mapping rule](/media/develop/aws-appflow-step-add-mapping-rule.png)

- The following mapping rules (Source field name -> Destination field name) are needed in this document:

    - Account ID -> id
    - Account Name -> name
    - Account Type -> type
    - Billing State/Province -> billing_state
    - Account Rating -> rating
    - Industry -> industry

    ![mapping a rule](/media/develop/aws-appflow-step-mapping-a-rule.png)

    ![show all mapping rules](/media/develop/aws-appflow-step-show-all-mapping-rules.png)

### (Optional) Set filters

If you want to add some filters to your data fields, you can set them here. Otherwise, skip this step and click **Next**.

![filters](/media/develop/aws-appflow-step-filters.png)

### Confirm and create the flow

Confirm the information of the flow to be created. If everything looks fine, click **Create flow**.

![review](/media/develop/aws-appflow-step-review.png)

## Step 3. Run the flow

On the page of the newly created flow, click **Run flow** in the upper-right corner.

![run flow](/media/develop/aws-appflow-step-run-flow.png)

The following screenshot shows an example that the flow runs successfully:

![run success](/media/develop/aws-appflow-step-run-success.png)

Query the `sf_account` table, and you can see that the records from the Salesforce **Account** object have been written to it:

```sql
test> SELECT * FROM sf_account;
+--------------------+-------------------------------------+--------------------+---------------+--------+----------------+
| id                 | name                                | type               | billing_state | rating | industry       |
+--------------------+-------------------------------------+--------------------+---------------+--------+----------------+
| 001Do000003EDTlIAO | Sample Account for Entitlements     | null               | null          | null   | null           |
| 001Do000003EDTZIA4 | Edge Communications                 | Customer - Direct  | TX            | Hot    | Electronics    |
| 001Do000003EDTaIAO | Burlington Textiles Corp of America | Customer - Direct  | NC            | Warm   | Apparel        |
| 001Do000003EDTbIAO | Pyramid Construction Inc.           | Customer - Channel | null          | null   | Construction   |
| 001Do000003EDTcIAO | Dickenson plc                       | Customer - Channel | KS            | null   | Consulting     |
| 001Do000003EDTdIAO | Grand Hotels & Resorts Ltd          | Customer - Direct  | IL            | Warm   | Hospitality    |
| 001Do000003EDTeIAO | United Oil & Gas Corp.              | Customer - Direct  | NY            | Hot    | Energy         |
| 001Do000003EDTfIAO | Express Logistics and Transport     | Customer - Channel | OR            | Cold   | Transportation |
| 001Do000003EDTgIAO | University of Arizona               | Customer - Direct  | AZ            | Warm   | Education      |
| 001Do000003EDThIAO | United Oil & Gas, UK                | Customer - Direct  | UK            | null   | Energy         |
| 001Do000003EDTiIAO | United Oil & Gas, Singapore         | Customer - Direct  | Singapore     | null   | Energy         |
| 001Do000003EDTjIAO | GenePoint                           | Customer - Channel | CA            | Cold   | Biotechnology  |
| 001Do000003EDTkIAO | sForce                              | null               | CA            | null   | null           |
+--------------------+-------------------------------------+--------------------+---------------+--------+----------------+
```

## Noteworthy things

- If anything goes wrong, you can navigate to the [CloudWatch](https://console.aws.amazon.com/cloudwatch/home) page on the AWS Management Console to get logs.
- The steps in this document are based on [Building custom connectors using the Amazon AppFlow Custom Connector SDK](https://aws.amazon.com/blogs/compute/building-custom-connectors-using-the-amazon-appflow-custom-connector-sdk/).
- [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless) is **NOT** a production environment.
- To prevent excessive length, the examples in this document only show the `Insert` strategy, but `Update` and `Upsert` strategies are also tested and can be used.