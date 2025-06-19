---
title: 为 TiDB Cloud Dedicated 配置外部存储访问
summary: 了解如何配置 Amazon Simple Storage Service (Amazon S3)、Google Cloud Storage (GCS) 和 Azure Blob Storage 访问。
aliases: ['/tidb-cloud/config-s3-and-gcs-access']
---

# 为 TiDB Cloud Dedicated 配置外部存储访问

如果你的源数据存储在 Amazon S3 存储桶、Azure Blob Storage 容器或 Google Cloud Storage (GCS) 存储桶中，在将数据导入或迁移到 TiDB Cloud 之前，你需要配置对这些存储桶的跨账户访问。本文档介绍如何为 TiDB Cloud Dedicated 集群进行此配置。

如果你需要为 TiDB Cloud Serverless 集群配置这些外部存储，请参阅[为 TiDB Cloud Serverless 配置外部存储访问](/tidb-cloud/serverless-external-storage.md)。

## 配置 Amazon S3 访问

要允许 TiDB Cloud Dedicated 集群访问你的 Amazon S3 存储桶中的源数据，可以使用以下任一方法为集群配置存储桶访问：

- [使用 Role ARN](#使用-role-arn-配置-amazon-s3-访问)（推荐）：使用 Role ARN 访问你的 Amazon S3 存储桶。
- [使用 AWS 访问密钥](#使用-aws-访问密钥配置-amazon-s3-访问)：使用 IAM 用户的访问密钥访问你的 Amazon S3 存储桶。

### 使用 Role ARN 配置 Amazon S3 访问

按照以下步骤为 TiDB Cloud 配置存储桶访问并获取 Role ARN：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，获取目标 TiDB 集群对应的 TiDB Cloud 账户 ID 和外部 ID。

    1. 导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。

        > **提示：**
        >
        > 你可以使用左上角的组合框在组织、项目和集群之间切换。

    2. 点击目标集群的名称进入其概览页面，然后在左侧导航栏中点击**数据** > **导入**。

    3. 选择**从云存储导入数据**，然后点击 **Amazon S3**。

    4. 在**从 Amazon S3 导入数据**页面，点击 **Role ARN** 下的链接。此时会显示**添加新的 Role ARN** 对话框。

    5. 展开**手动创建 Role ARN**以获取 TiDB Cloud 账户 ID 和 TiDB Cloud 外部 ID。记下这些 ID 以供后续使用。

2. 在 AWS 管理控制台中，为你的 Amazon S3 存储桶创建托管策略。

    1. 登录 AWS 管理控制台，打开 Amazon S3 控制台：[https://console.aws.amazon.com/s3/](https://console.aws.amazon.com/s3/)。
    2. 在**存储桶**列表中，选择包含源数据的存储桶名称，然后点击**复制 ARN**以获取你的 S3 存储桶 ARN（例如，`arn:aws:s3:::tidb-cloud-source-data`）。记下存储桶 ARN 以供后续使用。

        ![复制存储桶 ARN](/media/tidb-cloud/copy-bucket-arn.png)

    3. 打开 IAM 控制台：[https://console.aws.amazon.com/iam/](https://console.aws.amazon.com/iam/)，在左侧导航栏中点击**策略**，然后点击**创建策略**。

        ![创建策略](/media/tidb-cloud/aws-create-policy.png)

    4. 在**创建策略**页面，点击 **JSON** 选项卡。
    5. 复制以下访问策略模板并将其粘贴到策略文本字段中。

        ```json
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "VisualEditor0",
                    "Effect": "Allow",
                    "Action": [
                        "s3:GetObject",
                        "s3:GetObjectVersion"
                    ],
                    "Resource": "<你的 S3 存储桶 ARN>/<源数据目录>/*"
                },
                {
                    "Sid": "VisualEditor1",
                    "Effect": "Allow",
                    "Action": [
                        "s3:ListBucket",
                        "s3:GetBucketLocation"
                    ],
                    "Resource": "<你的 S3 存储桶 ARN>"
                }
            ]
        }
        ```

        在策略文本字段中，将以下配置更新为你自己的值。

        - `"Resource": "<你的 S3 存储桶 ARN>/<源数据目录>/*"`

            例如，如果你的源数据存储在 `tidb-cloud-source-data` 存储桶的根目录中，使用 `"Resource": "arn:aws:s3:::tidb-cloud-source-data/*"`。如果你的源数据存储在存储桶的 `mydata` 目录中，使用 `"Resource": "arn:aws:s3:::tidb-cloud-source-data/mydata/*"`。确保在目录末尾添加 `/*`，以便 TiDB Cloud 可以访问此目录中的所有文件。

        - `"Resource": "<你的 S3 存储桶 ARN>"`

            例如，`"Resource": "arn:aws:s3:::tidb-cloud-source-data"`。

        - 如果你启用了带有客户管理密钥加密的 AWS Key Management Service 密钥（SSE-KMS），请确保策略中包含以下配置。`"arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"` 是存储桶的示例 KMS 密钥。

            ```json
            {
                "Sid": "AllowKMSkey",
                "Effect": "Allow",
                "Action": [
                    "kms:Decrypt"
                ],
                "Resource": "arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"
            }
            ```

            如果你的存储桶中的对象是从另一个加密存储桶复制的，KMS 密钥值需要包含两个存储桶的密钥。例如，`"Resource": ["arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f","arn:aws:kms:ap-northeast-1:495580073302:key/0d7926a7-6ecc-4bf7-a9c1-a38f0faec0cd"]`。

    6. 点击**下一步**。
    7. 设置策略名称，添加策略标签（可选），然后点击**创建策略**。

3. 在 AWS 管理控制台中，为 TiDB Cloud 创建访问角色并获取角色 ARN。

    1. 在 IAM 控制台 [https://console.aws.amazon.com/iam/](https://console.aws.amazon.com/iam/) 中，点击左侧导航栏中的**角色**，然后点击**创建角色**。

        ![创建角色](/media/tidb-cloud/aws-create-role.png)

    2. 填写以下信息以创建角色：

        - 在**可信实体类型**下，选择 **AWS 账户**。
        - 在 **AWS 账户**下，选择**其他 AWS 账户**，然后将 TiDB Cloud 账户 ID 粘贴到**账户 ID**字段中。
        - 在**选项**下，点击**需要外部 ID**以避免[混淆代理问题](https://docs.aws.amazon.com/IAM/latest/UserGuide/confused-deputy.html)，然后将 TiDB Cloud 外部 ID 粘贴到**外部 ID**字段中。如果创建角色时没有"需要外部 ID"，任何拥有你的 S3 存储桶 URI 和 IAM 角色 ARN 的人都可能访问你的 Amazon S3 存储桶。如果创建角色时同时使用账户 ID 和外部 ID，只有在同一项目和同一区域中运行的 TiDB 集群才能访问存储桶。

    3. 点击**下一步**打开策略列表，选择你刚刚创建的策略，然后点击**下一步**。
    4. 在**角色详细信息**下，为角色设置名称，然后点击右下角的**创建角色**。创建角色后，将显示角色列表。
    5. 在角色列表中，点击你刚刚创建的角色名称进入其摘要页面，然后复制角色 ARN。

        ![复制 AWS 角色 ARN](/media/tidb-cloud/aws-role-arn.png)

4. 在 TiDB Cloud 控制台中，转到获取 TiDB Cloud 账户 ID 和外部 ID 的**数据导入**页面，然后将角色 ARN 粘贴到 **Role ARN** 字段中。

### 使用 AWS 访问密钥配置 Amazon S3 访问

建议使用 IAM 用户（而不是 AWS 账户根用户）创建访问密钥。

按照以下步骤配置访问密钥：

1. 创建具有以下策略的 IAM 用户：

   - `AmazonS3ReadOnlyAccess`
   - [`CreateOwnAccessKeys`（必需）和 `ManageOwnAccessKeys`（可选）](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#access-keys_required-permissions)

   建议这些策略仅适用于存储源数据的存储桶。

   有关更多信息，请参阅[创建 IAM 用户](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console)。

2. 使用你的 AWS 账户 ID 或账户别名以及 IAM 用户名和密码登录 [IAM 控制台](https://console.aws.amazon.com/iam)。

3. 创建访问密钥。有关详细信息，请参阅[为 IAM 用户创建访问密钥](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)。

> **注意：**
>
> TiDB Cloud 不会存储你的访问密钥。建议在导入完成后[删除访问密钥](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)。

## 配置 GCS 访问

要允许 TiDB Cloud 访问你的 GCS 存储桶中的源数据，你需要为存储桶配置 GCS 访问。一旦为项目中的一个 TiDB 集群完成配置，该项目中的所有 TiDB 集群都可以访问该 GCS 存储桶。

1. 在 TiDB Cloud 控制台中，获取目标 TiDB 集群的 Google Cloud 服务账户 ID。

    1. 导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。

        > **提示：**
        >
        > 你可以使用左上角的组合框在组织、项目和集群之间切换。

    2. 点击目标集群的名称进入其概览页面，然后在左侧导航栏中点击**数据** > **导入**。

    3. 选择**从云存储导入数据**，然后点击 **Google Cloud Storage**。

    4. 点击**显示 Google Cloud 服务账户 ID**，然后复制服务账户 ID 以供后续使用。

2. 在 Google Cloud 控制台中，为你的 GCS 存储桶创建 IAM 角色。

    1. 登录 [Google Cloud 控制台](https://console.cloud.google.com/)。
    2. 转到[角色](https://console.cloud.google.com/iam-admin/roles)页面，然后点击**创建角色**。

        ![创建角色](/media/tidb-cloud/gcp-create-role.png)

    3. 为角色输入名称、描述、ID 和角色启动阶段。角色名称在创建后不能更改。
    4. 点击**添加权限**。
    5. 为角色添加以下只读权限，然后点击**添加**。

        - storage.buckets.get
        - storage.objects.get
        - storage.objects.list

        你可以将权限名称复制到**输入属性名称或值**字段作为筛选查询，然后在筛选结果中选择该名称。要添加这三个权限，你可以在权限名称之间使用 **OR**。

        ![添加权限](/media/tidb-cloud/gcp-add-permissions.png)

3. 转到[存储桶](https://console.cloud.google.com/storage/browser)页面，点击你希望 TiDB Cloud 访问的 GCS 存储桶的名称。

4. 在**存储桶详情**页面，点击**权限**选项卡，然后点击**授予访问权限**。

    ![授予存储桶访问权限](/media/tidb-cloud/gcp-bucket-permissions.png)

5. 填写以下信息以授予对存储桶的访问权限，然后点击**保存**。

    - 在**新主体**字段中，粘贴目标 TiDB 集群的 Google Cloud 服务账户 ID。
    - 在**选择角色**下拉列表中，输入你刚刚创建的 IAM 角色名称，然后从筛选结果中选择该名称。

    > **注意：**
    >
    > 要删除对 TiDB Cloud 的访问权限，你可以简单地删除你已授予的访问权限。

6. 在**存储桶详情**页面，点击**对象**选项卡。

    如果你想复制文件的 gsutil URI，选择该文件，点击**打开对象溢出菜单**，然后点击**复制 gsutil URI**。

    ![获取存储桶 URI](/media/tidb-cloud/gcp-bucket-uri01.png)

    如果你想使用文件夹的 gsutil URI，打开该文件夹，然后点击文件夹名称后面的复制按钮以复制文件夹名称。之后，你需要在名称开头添加 `gs://`，在末尾添加 `/` 以获取文件夹的正确 URI。

    例如，如果文件夹名称是 `tidb-cloud-source-data`，你需要使用 `gs://tidb-cloud-source-data/` 作为 URI。

    ![获取存储桶 URI](/media/tidb-cloud/gcp-bucket-uri02.png)

7. 在 TiDB Cloud 控制台中，转到获取 Google Cloud 服务账户 ID 的**数据导入**页面，然后将 GCS 存储桶 gsutil URI 粘贴到**存储桶 gsutil URI** 字段中。例如，粘贴 `gs://tidb-cloud-source-data/`。

## 配置 Azure Blob Storage 访问

要允许 TiDB Cloud Dedicated 访问你的 Azure Blob 容器，你需要为容器配置 Azure Blob 访问。你可以使用账户 SAS 令牌配置容器访问：

1. 在 [Azure Storage 账户](https://portal.azure.com/#browse/Microsoft.Storage%2FStorageAccounts)页面，点击容器所属的存储账户。

2. 在存储账户的导航栏中，点击**安全性 + 网络** > **共享访问签名**。

    ![sas-position](/media/tidb-cloud/dedicated-external-storage/azure-sas-position.png)

3. 在**共享访问签名**页面，按照以下步骤创建具有必要权限的[账户 SAS 令牌](https://docs.microsoft.com/en-us/azure/storage/common/storage-sas-overview)：

    1. 在**允许的服务**下，选择**Blob**。
    2. 在**允许的资源类型**下，选择**容器**和**对象**。
    3. 在**允许的权限**下，选择所需的权限。例如，将数据导入到 TiDB Cloud Dedicated 需要**读取**和**列出**权限。
    4. 根据需要调整**开始和到期日期/时间**。出于安全考虑，建议设置与数据导入时间表相符的到期日期。
    5. 保留其他设置的默认值。

    ![sas-create](/media/tidb-cloud/dedicated-external-storage/azure-sas-create.png)

4. 点击**生成 SAS 和连接字符串**以生成 SAS 令牌。

5. 复制生成的 **SAS 令牌**。在 TiDB Cloud 中配置数据导入时，你将需要此令牌字符串。

> **注意：**
>
> 在开始数据导入之前，请测试连接和权限，以确保 TiDB Cloud Dedicated 可以访问指定的 Azure Blob 容器和文件。
