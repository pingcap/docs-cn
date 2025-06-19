---
title: 使用备份资源
summary: 了解如何使用备份资源创建 TiDB Cloud 集群的备份。
---

# 使用备份资源

你可以在本文档中了解如何使用 `tidbcloud_backup` 资源创建 TiDB Cloud 集群的备份。

`tidbcloud_backup` 资源的功能包括以下内容：

- 为 TiDB Cloud Dedicated 集群创建备份。
- 删除 TiDB Cloud Dedicated 集群的备份。

## 前提条件

- [获取 TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md)。
- 备份和恢复功能不适用于 TiDB Cloud Serverless 集群。要使用备份资源，请确保你已创建了 TiDB Cloud Dedicated 集群。

## 使用备份资源创建备份

1. 创建一个备份目录并进入该目录。

2. 创建一个 `backup.tf` 文件。

    例如：

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
    resource "tidbcloud_backup" "example_backup" {
      project_id  = "1372813089189561287"
      cluster_id  = "1379661944630234067"
      name        = "firstBackup"
      description = "create by terraform"
    }
    ```

    你需要将文件中的资源值（如项目 ID 和集群 ID）替换为你自己的值。

    如果你已经使用 Terraform 维护了一个集群资源（例如 `example_cluster`），你也可以按如下方式配置备份资源，而无需指定实际的项目 ID 和集群 ID。

    ```
    resource "tidbcloud_backup" "example_backup" {
      project_id  = tidbcloud_cluster.example_cluster.project_id
      cluster_id  = tidbcloud_cluster.example_cluster.id
      name        = "firstBackup"
      description = "create by terraform"
    }
    ```

3. 运行 `terraform apply` 命令：

    ```
    $ terraform apply

    tidbcloud_cluster.example_cluster: Refreshing state... [id=1379661944630234067]

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      + create

    Terraform will perform the following actions:

      # tidbcloud_backup.example_backup will be created
      + resource "tidbcloud_backup" "example_backup" {
          + cluster_id       = "1379661944630234067"
          + create_timestamp = (known after apply)
          + description      = "create by terraform"
          + id               = (known after apply)
          + name             = "firstBackup"
          + project_id       = "1372813089189561287"
          + size             = (known after apply)
          + status           = (known after apply)
          + type             = (known after apply)
        }

    Plan: 1 to add, 0 to change, 0 to destroy.

    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value:
    ```

4. 输入 `yes` 创建备份：

    ```
      Enter a value: yes

    tidbcloud_backup.example_backup: Creating...
    tidbcloud_backup.example_backup: Creation complete after 2s [id=1350048]

    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

    ```

5. 使用 `terraform state show tidbcloud_backup.${resource-name}` 检查备份状态：

    ```
    $ terraform state show tidbcloud_backup.example_backup

    # tidbcloud_backup.example_backup:
    resource "tidbcloud_backup" "example_backup" {
        cluster_id       = "1379661944630234067"
        create_timestamp = "2022-08-26T07:56:10Z"
        description      = "create by terraform"
        id               = "1350048"
        name             = "firstBackup"
        project_id       = "1372813089189561287"
        size             = "0"
        status           = "PENDING"
        type             = "MANUAL"
    }
    ```

6. 等待几分钟。然后使用 `terraform refersh` 更新状态：

    ```
    $ terraform refresh
    tidbcloud_cluster.example_cluster: Refreshing state... [id=1379661944630234067]
    tidbcloud_backup.example_backup: Refreshing state... [id=1350048]
    $ terraform state show tidbcloud_backup.example_backup
    # tidbcloud_backup.example_backup:
    resource "tidbcloud_backup" "example_backup" {
        cluster_id       = "1379661944630234067"
        create_timestamp = "2022-08-26T07:56:10Z"
        description      = "create by terraform"
        id               = "1350048"
        name             = "firstBackup"
        project_id       = "1372813089189561287"
        size             = "198775"
        status           = "SUCCESS"
        type             = "MANUAL"
    }
    ```

当状态变为 `SUCCESS` 时，表示你已经为集群创建了备份。请注意，备份在创建后无法更新。

现在，你已经为集群创建了备份。如果你想使用备份来恢复集群，可以[使用恢复资源](/tidb-cloud/terraform-use-restore-resource.md)。

## 更新备份

备份无法更新。

## 删除备份

要删除备份，请转到包含相应 `backup.tf` 文件的备份目录，然后运行 `terraform destroy` 命令来销毁备份资源。

```
$ terraform destroy

Plan: 0 to add, 0 to change, 1 to destroy.

Do you really want to destroy all resources?
Terraform will destroy all your managed infrastructure, as shown above.
There is no undo. Only 'yes' will be accepted to confirm.

Enter a value: yes
```

现在，如果你运行 `terraform show` 命令，你将得不到任何内容，因为资源已被清除：

```
$ terraform show
```
