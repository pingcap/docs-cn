---
title: 将集群资源迁移到 Serverless 或 Dedicated 集群资源
summary: 了解如何将集群资源迁移到 serverless 或 dedicated 集群资源。
---

# 将集群资源迁移到 Serverless 或 Dedicated 集群资源

从 TiDB Cloud Terraform Provider v0.4.0 开始，`tidbcloud_cluster` 资源被两个新资源替代：`tidbcloud_serverless_cluster` 和 `tidbcloud_dedicated_cluster`。如果你正在使用 TiDB Cloud Terraform Provider v0.4.0 或更高版本，可以按照本文档将你的 `tidbcloud_cluster` 资源迁移到 `tidbcloud_serverless_cluster` 或 `tidbcloud_dedicated_cluster` 资源。

> **提示：**
>
> 本文档中的步骤使用 Terraform 的配置生成功能来简化迁移过程，通过自动重新创建集群资源的 `.tf` 配置。要了解更多信息，请参阅 Terraform 文档中的[生成配置](https://developer.hashicorp.com/terraform/language/import/generating-configuration)。

## 前提条件

- 升级到 [TiDB Cloud Terraform Provider v0.4.0 或更高版本](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest)

## 步骤 1. 确定要迁移的 `tidbcloud_cluster` 资源

1. 列出所有 `tidbcloud_cluster` 资源：

    ```shell
    terraform state list | grep "tidbcloud_cluster"
    ```

2. 选择要迁移的目标集群资源，并获取其集群 `id` 以供后续使用：

    ```shell
    terraform state show ${your_target_cluster_resource} | grep ' id '
    ```

## 步骤 2. 从 Terraform 状态中移除现有资源

从 Terraform 状态中移除目标集群资源：

```shell
terraform state rm ${your_target_cluster_resource}
```

## 步骤 3. 删除目标集群资源的配置

在你的 `.tf` 文件中，找到目标集群资源的配置并删除相应的代码。

## 步骤 4. 为新的 serverless 或 dedicated 集群资源添加导入块

- 如果你的目标集群是 TiDB Cloud Serverless，将以下导入块添加到你的 `.tf` 文件中，将 `example` 替换为所需的资源名称，并将 `${id}` 替换为你在[步骤 1](#步骤-1-确定要迁移的-tidbcloud_cluster-资源)中获取的集群 ID：

    ```
    # TiDB Cloud Serverless
    import {
      to = tidbcloud_serverless_cluster.example
      id = "${id}"
    }
    ```

- 如果你的目标集群是 TiDB Cloud Dedicated，将以下导入块添加到你的 `.tf` 文件中，将 `example` 替换为所需的资源名称，并将 `${id}` 替换为你在[步骤 1](#步骤-1-确定要迁移的-tidbcloud_cluster-资源)中获取的集群 ID：

    ```
    # TiDB Cloud Dedicated
    import {
      to = tidbcloud_dedicated_cluster.example
      id = "${id}"
    }
    ```

## 步骤 5. 生成新的配置文件

根据导入块为新的 serverless 或 dedicated 集群资源生成新的配置文件：

```shell
terraform plan -generate-config-out=generated.tf
```

不要在上述命令中指定现有的 `.tf` 文件名。否则，Terraform 将返回错误。

## 步骤 6. 审查并应用生成的配置

审查生成的配置文件以确保它满足你的需求。你可以选择将此文件的内容移动到你喜欢的位置。

然后，运行 `terraform apply` 来导入你的基础设施。应用后，示例输出如下：

```shell
tidbcloud_serverless_cluster.example: Importing... 
tidbcloud_serverless_cluster.example: Import complete 

Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed.
```
