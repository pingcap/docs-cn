---
title: 获取 TiDB Cloud Terraform Provider
summary: 了解如何获取 TiDB Cloud Terraform Provider。
---

# 获取 TiDB Cloud Terraform Provider

本文档将介绍如何获取 TiDB Cloud Terraform Provider。

## 前提条件

确保满足 [TiDB Cloud Terraform Provider 概览](/tidb-cloud/terraform-tidbcloud-provider-overview.md#requirements)中的要求。

## 步骤 1. 安装 Terraform

TiDB Cloud Terraform Provider 已发布到 [Terraform Registry](https://registry.terraform.io/)。您只需要安装 Terraform (>=1.0)。

对于 macOS，您可以按照以下步骤使用 Homebrew 安装 Terraform。

1. 安装 HashiCorp tap，这是一个包含所有必需 Homebrew 包的仓库。

    ```shell
    brew tap hashicorp/tap
    ```

2. 使用 `hashicorp/tap/terraform` 安装 Terraform。

    ```shell
    brew install hashicorp/tap/terraform
    ```

对于其他操作系统，请参阅 [Terraform 文档](https://learn.hashicorp.com/tutorials/terraform/install-cli)获取说明。

## 步骤 2. 创建 API 密钥

TiDB Cloud API 使用 HTTP 摘要认证。它可以防止您的私钥在网络上传输。

目前，TiDB Cloud Terraform Provider 不支持管理 API 密钥。因此，您需要在 [TiDB Cloud 控制台](https://tidbcloud.com/project/clusters)中创建 API 密钥。

详细步骤，请参阅 [TiDB Cloud API 文档](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management)。

## 步骤 3. 下载 TiDB Cloud Terraform Provider

1. 创建 `main.tf` 文件：

   ```
   terraform {
     required_providers {
       tidbcloud = {
         source = "tidbcloud/tidbcloud"
         version = "~> 0.3.0"
       }
     }
     required_version = ">= 1.0.0"
   }
   ```

   - `source` 属性指定要从 [Terraform Registry](https://registry.terraform.io/) 下载的目标 Terraform provider。
   - `version` 属性是可选的，它指定 Terraform provider 的版本。如果未指定，默认使用最新的 provider 版本。
   - `required_version` 是可选的，它指定 Terraform 的版本。如果未指定，默认使用最新的 Terraform 版本。

2. 运行 `terraform init` 命令从 Terraform Registry 下载 TiDB Cloud Terraform Provider。

   ```
   $ terraform init

   Initializing the backend...

   Initializing provider plugins...
   - Reusing previous version of tidbcloud/tidbcloud from the dependency lock file
   - Using previously-installed tidbcloud/tidbcloud v0.1.0

   Terraform has been successfully initialized!

   You may now begin working with Terraform. Try running "terraform plan" to see
   any changes that are required for your infrastructure. All Terraform commands
   should now work.

   If you ever set or change modules or backend configuration for Terraform,
   rerun this command to reinitialize your working directory. If you forget, other
   commands will detect it and remind you to do so if necessary.
   ```

## 步骤 4. 使用 API 密钥配置 TiDB Cloud Terraform Provider

您可以按如下方式配置 `main.tf` 文件：

```
terraform {
  required_providers {
    tidbcloud = {
      source = "tidbcloud/tidbcloud"
    }
  }
}

provider "tidbcloud" {
  public_key = "your_public_key"
  private_key = "your_private_key"
}
```

`public_key` 和 `private_key` 是 API 密钥的公钥和私钥。您也可以通过环境变量传递它们：

```
export TIDBCLOUD_PUBLIC_KEY=${public_key}
export TIDBCLOUD_PRIVATE_KEY=${private_key}
```

现在，您可以使用 TiDB Cloud Terraform Provider 了。

## 步骤 5. 使用同步配置配置 TiDB Cloud Terraform Provider

Terraform provider (>= 0.3.0) 支持一个可选参数 `sync`。

通过将 `sync` 设置为 `true`，您可以同步创建、更新或删除资源。以下是一个示例：

```
provider "tidbcloud" {
  public_key = "your_public_key"
  private_key = "your_private_key"
  sync = true
}
```

建议将 `sync` 设置为 `true`，但请注意，`sync` 目前仅适用于集群资源。如果您需要对其他资源进行同步操作，请[联系 TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

## 下一步

通过[集群资源](/tidb-cloud/terraform-use-cluster-resource.md)开始管理集群。
