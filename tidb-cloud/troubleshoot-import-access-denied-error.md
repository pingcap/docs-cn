---
title: 排查从 Amazon S3 导入数据时的访问被拒绝错误
summary: 了解如何排查从 Amazon S3 导入数据到 TiDB Cloud 时的访问被拒绝错误。
---

# 排查从 Amazon S3 导入数据时的访问被拒绝错误

本文介绍如何排查从 Amazon S3 导入数据到 TiDB Cloud 时可能出现的访问被拒绝错误。

在 TiDB Cloud 控制台的**数据导入**页面上点击**下一步**并确认导入过程后，TiDB Cloud 开始验证是否可以访问你指定的存储桶 URI 中的数据。如果你看到包含关键字 `AccessDenied` 的错误消息，则表示发生了访问被拒绝错误。

要排查访问被拒绝错误，请在 AWS 管理控制台中执行以下检查。

## 无法承担提供的角色

本节介绍如何排查 TiDB Cloud 无法承担提供的角色来访问指定存储桶的问题。

### 检查信任实体

1. 在 AWS 管理控制台中，转到 **IAM** > **访问管理** > **角色**。
2. 在角色列表中，找到并点击你为目标 TiDB 集群创建的角色。此时会显示角色摘要页面。
3. 在角色摘要页面上，点击**信任关系**标签页，你将看到受信任的实体。

以下是信任实体的示例：

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::380838443567:root"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {
                    "sts:ExternalId": "696e6672612d617069a79c22fa5740944bf8bb32e4a0c4e3fe"
                }
            }
        }
    ]
}
```

在示例信任实体中：

- `380838443567` 是 TiDB Cloud 账户 ID。确保你的信任实体中的此字段与你的 TiDB Cloud 账户 ID 匹配。
- `696e6672612d617069a79c22fa5740944bf8bb32e4a0c4e3fe` 是 TiDB Cloud 外部 ID。确保你的信任实体中的此字段与你的 TiDB Cloud 外部 ID 匹配。

### 检查 IAM 角色是否存在

如果 IAM 角色不存在，请按照[配置 Amazon S3 访问](/tidb-cloud/dedicated-external-storage.md#configure-amazon-s3-access)中的说明创建角色。

### 检查外部 ID 是否正确设置

无法承担提供的角色 `{role_arn}`。检查角色上的信任关系设置。例如，检查信任实体是否已设置为 `TiDB Cloud 账户 ID`，以及信任条件中是否正确设置了 `TiDB Cloud 外部 ID`。请参见[检查信任实体](#检查信任实体)。

## 访问被拒绝

本节介绍如何排查访问问题。

### 检查 IAM 用户的策略

当你使用 IAM 用户的 AWS 访问密钥访问 Amazon S3 存储桶时，可能会遇到以下错误：

- "使用访问密钥 ID '{access_key_id}' 和密钥 '{secret_access_key}' 访问源 '{bucket_uri}' 被拒绝"

这表明 TiDB Cloud 由于权限不足而无法访问 Amazon S3 存储桶。你需要以下权限才能访问 Amazon S3 存储桶：

- `s3:GetObject`
- `s3:ListBucket`
- `s3:GetBucketLocation`

要检查 IAM 用户的策略，请执行以下步骤：

1. 在 AWS 管理控制台中，转到 **IAM** > **访问管理** > **用户**。
2. 在用户列表中，找到并点击你用于向 TiDB Cloud 导入数据的用户。此时会显示用户摘要页面。
3. 在用户摘要页面的**权限策略**区域中，会显示策略列表。对每个策略执行以下步骤：
    1. 点击策略进入策略摘要页面。
    2. 在策略摘要页面上，点击 **{}JSON** 标签页以检查权限策略。确保策略中的 `Resource` 字段配置正确。

以下是策略示例：

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": "arn:aws:s3:::tidb-cloud-source-data/mydata/*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetBucketLocation"
            ],
            "Resource": "arn:aws:s3:::tidb-cloud-source-data"
        },
}
```

有关如何授予用户权限并测试权限的更多信息，请参见[使用用户策略控制对存储桶的访问](https://docs.aws.amazon.com/AmazonS3/latest/userguide/walkthrough1.html)。

### 检查 IAM 角色的策略

1. 在 AWS 管理控制台中，转到 **IAM** > **访问管理** > **角色**。
2. 在角色列表中，找到并点击你为目标 TiDB 集群创建的角色。此时会显示角色摘要页面。
3. 在角色摘要页面的**权限策略**区域中，会显示策略列表。对每个策略执行以下步骤：
    1. 点击策略进入策略摘要页面。
    2. 在策略摘要页面上，点击 **{}JSON** 标签页以检查权限策略。确保策略中的 `Resource` 字段配置正确。

以下是策略示例：

```
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
            "Resource": "arn:aws:s3:::tidb-cloud-source-data/mydata/*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetBucketLocation"
            ],
            "Resource": "arn:aws:s3:::tidb-cloud-source-data"
        },
        {
            "Sid": "AllowKMSkey",
            "Effect": "Allow",
            "Action": [
                "kms:Decrypt"
            ],
            "Resource": "arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"
        }
    ]
}
```

在此示例策略中，请注意以下几点：

- 在 `"arn:aws:s3:::tidb-cloud-source-data/mydata/*"` 中，`"arn:aws:s3:::tidb-cloud-source-data"` 是示例 S3 存储桶 ARN，`/mydata/*` 是你可以在 S3 存储桶根级别自定义的用于数据存储的目录。目录需要以 `/*` 结尾，例如 `"<你的 S3 存储桶 ARN>/<源数据目录>/*"`。如果未添加 `/*`，则会出现 `AccessDenied` 错误。

- 如果你已启用带有客户管理密钥加密的 AWS Key Management Service 密钥（SSE-KMS），请确保策略中包含以下配置。`"arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"` 是存储桶的示例 KMS 密钥。

    ```
        {
            "Sid": "AllowKMSkey",
            "Effect": "Allow",
            "Action": [
                "kms:Decrypt"
            ],
            "Resource": "arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f"
        }
    ```

    如果你的存储桶中的对象是从另一个加密的存储桶复制的，则 KMS 密钥值需要包含两个存储桶的密钥。例如，`"Resource": ["arn:aws:kms:ap-northeast-1:105880447796:key/c3046e91-fdfc-4f3a-acff-00597dd3801f","arn:aws:kms:ap-northeast-1:495580073302:key/0d7926a7-6ecc-4bf7-a9c1-a38f0faec0cd"]`。

如果你的策略未按照上述示例正确配置，请更正策略中的 `Resource` 字段，然后重试导入数据。

> **提示：**
>
> 如果你多次更新权限策略后在数据导入期间仍然收到 `AccessDenied` 错误，可以尝试撤销活动会话。转到 **IAM** > **访问管理** > **角色**，点击目标角色进入角色摘要页面。在角色摘要页面上，找到**撤销活动会话**并点击按钮以撤销活动会话。然后，重试数据导入。
>
> 请注意，这可能会影响你的其他应用程序。

### 检查存储桶策略

1. 在 AWS 管理控制台中，打开 Amazon S3 控制台，然后转到**存储桶**页面。此时会显示存储桶列表。
2. 在列表中，找到并点击目标存储桶。此时会显示存储桶信息页面。
3. 点击**权限**标签页，然后向下滚动到**存储桶策略**区域。默认情况下，此区域没有策略值。如果在此区域显示任何拒绝策略，则在数据导入期间可能会出现 `AccessDenied` 错误。

如果你看到拒绝策略，请检查该策略是否与当前数据导入相关。如果是，请从该区域删除它，然后重试数据导入。

### 检查对象所有权

1. 在 AWS 管理控制台中，打开 Amazon S3 控制台，然后转到**存储桶**页面。此时会显示存储桶列表。
2. 在存储桶列表中，找到并点击目标存储桶。此时会显示存储桶信息页面。
3. 在存储桶信息页面上，点击**权限**标签页，然后向下滚动到**对象所有权**区域。确保"对象所有权"配置为"强制执行存储桶所有者"。

    如果配置不是"强制执行存储桶所有者"，则会出现 `AccessDenied` 错误，因为你的账户对此存储桶中的所有对象没有足够的权限。

要处理此错误，请点击对象所有权区域右上角的**编辑**，并将所有权更改为"强制执行存储桶所有者"。请注意，这可能会影响正在使用此存储桶的其他应用程序。

### 检查存储桶加密类型

加密 S3 存储桶的方式不止一种。当你尝试访问存储桶中的对象时，你创建的角色必须具有访问加密密钥以进行数据解密的权限。否则，会出现 `AccessDenied` 错误。

要检查存储桶的加密类型，请执行以下步骤：

1. 在 AWS 管理控制台中，打开 Amazon S3 控制台，然后转到**存储桶**页面。此时会显示存储桶列表。
2. 在存储桶列表中，找到并点击目标存储桶。此时会显示存储桶信息页面。
3. 在存储桶信息页面上，点击**属性**标签页，向下滚动到**默认加密**区域，然后检查此区域中的配置。

有两种类型的服务器端加密：Amazon S3 托管密钥（SSE-S3）和 AWS Key Management Service（SSE-KMS）。对于 SSE-S3，不需要进一步检查，因为此加密类型不会导致访问被拒绝错误。对于 SSE-KMS，你需要检查以下内容：

- 如果区域中的 AWS KMS 密钥 ARN 以黑色显示且没有下划线，则 AWS KMS 密钥是 AWS 托管密钥（aws/s3）。
- 如果区域中的 AWS KMS 密钥 ARN 以蓝色显示并带有链接，请点击密钥 ARN 以打开密钥信息页面。检查左侧导航栏以查看具体的加密类型。它可能是 AWS 托管密钥（aws/s3）或客户托管密钥。

<details>
<summary>对于 SSE-KMS 中的 AWS 托管密钥（aws/s3）</summary>

在这种情况下，如果出现 `AccessDenied` 错误，原因可能是密钥是只读的，并且不允许跨账户权限授予。有关详细信息，请参见 AWS 文章[为什么跨账户用户在尝试访问由自定义 AWS KMS 密钥加密的 S3 对象时会收到访问被拒绝错误](https://aws.amazon.com/premiumsupport/knowledge-center/cross-account-access-denied-error-s3/)。

要解决访问被拒绝错误，请点击**默认加密**区域右上角的**编辑**，并将 AWS KMS 密钥更改为"从你的 AWS KMS 密钥中选择"或"输入 AWS KMS 密钥 ARN"，或将服务器端加密类型更改为"AWS S3 托管密钥（SSE-S3）"。除了此方法外，你还可以创建新的存储桶并使用自定义托管密钥或 SSE-S3 加密方法。
</details>

<details>
<summary>对于 SSE-KMS 中的客户托管密钥</summary>

要解决这种情况下的 `AccessDenied` 错误，请点击密钥 ARN 或手动在 KMS 中找到密钥。此时会显示**密钥用户**页面。点击区域右上角的**添加**以添加你用于向 TiDB Cloud 导入数据的角色。然后，重试导入数据。

</details>

> **注意：**
>
> 如果你的存储桶中的对象是从现有的加密存储桶复制的，你还需要在 AWS KMS 密钥 ARN 中包含源存储桶的密钥。这是因为你的存储桶中的对象使用与源对象加密相同的加密方法。有关更多信息，请参见 AWS 文档[将默认加密与复制一起使用](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-encryption.html)。

### 查看 AWS 文章获取说明

如果你已执行上述所有检查但仍收到 `AccessDenied` 错误，可以查看 AWS 文章[如何排查来自 Amazon S3 的 403 访问被拒绝错误](https://aws.amazon.com/premiumsupport/knowledge-center/s3-troubleshoot-403/)以获取更多说明。
