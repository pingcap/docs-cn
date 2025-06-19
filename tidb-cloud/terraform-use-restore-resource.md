---
title: 使用恢复资源
summary: 了解如何使用恢复资源。
---

# 使用恢复资源

你可以在本文档中了解如何使用 `tidbcloud_restore` 资源管理恢复任务。

`tidbcloud_restore` 资源的功能包括以下内容：

- 根据你的备份为 TiDB Cloud Dedicated 集群创建恢复任务。

## 前提条件

- [获取 TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md)。
- 备份和恢复功能不适用于 TiDB Cloud Serverless 集群。要使用恢复资源，请确保你已创建了 TiDB Cloud Dedicated 集群。

## 创建恢复任务

创建集群备份后，你可以通过使用 `tidbcloud_restore` 资源创建恢复任务来恢复集群。

> **注意：**
>
> 你只能从较小的节点规格恢复数据到相同或更大的节点规格。

1. 创建一个恢复目录并进入该目录。

2. 创建一个 `restore.tf` 文件。

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
    resource "tidbcloud_restore" "example_restore" {
      project_id = tidbcloud_cluster.example_cluster.project_id
      backup_id  = tidbcloud_backup.example_backup.id
      name       = "restoreCluster"
      config = {
        root_password = "Your_root_password1."
        port          = 4000
        components = {
          tidb = {
            node_size : "8C16G"
            node_quantity : 2
          }
          tikv = {
            node_size : "8C32G"
            storage_size_gib : 500
            node_quantity : 6
          }
          tiflash = {
            node_size : "8C64G"
            storage_size_gib : 500
            node_quantity : 2
          }
        }
      }
    }
    ```

3. 运行 `terraform apply` 命令并输入 `yes` 确认：

    ```
    $ terraform apply
    tidbcloud_cluster.example_cluster: Refreshing state... [id=1379661944630234067]
    tidbcloud_backup.example_backup: Refreshing state... [id=1350048]

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      + create

    Terraform will perform the following actions:

      # tidbcloud_restore.example_restore will be created
      + resource "tidbcloud_restore" "example_restore" {
          + backup_id        = "1350048"
          + cluster          = {
              + id     = (known after apply)
              + name   = (known after apply)
              + status = (known after apply)
            }
          + cluster_id       = (known after apply)
          + config           = {
              + components    = {
                  + tidb    = {
                      + node_quantity = 2
                      + node_size     = "8C16G"
                    }
                  + tiflash = {
                      + node_quantity    = 2
                      + node_size        = "8C64G"
                      + storage_size_gib = 500
                    }
                  + tikv    = {
                      + node_quantity    = 6
                      + node_size        = "8C32G"
                      + storage_size_gib = 500
                    }
                }
              + port          = 4000
              + root_password = "Your_root_password1."
            }
          + create_timestamp = (known after apply)
          + error_message    = (known after apply)
          + id               = (known after apply)
          + name             = "restoreCluster"
          + project_id       = "1372813089189561287"
          + status           = (known after apply)
        }

    Plan: 1 to add, 0 to change, 0 to destroy.

    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_restore.example_restore: Creating...
    tidbcloud_restore.example_restore: Creation complete after 1s [id=780114]

    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
    ```

4. 使用 `terraform state show tidbcloud_restore.${resource-name}` 命令检查恢复任务的状态：

    ```
    $ terraform state show tidbcloud_restore.example_restore

    # tidbcloud_restore.example_restore:
    resource "tidbcloud_restore" "example_restore" {
        backup_id        = "1350048"
        cluster          = {
            id     = "1379661944630264072"
            name   = "restoreCluster"
            status = "INITIALIZING"
        }
        cluster_id       = "1379661944630234067"
        config           = {
            components    = {
                tidb    = {
                    node_quantity = 2
                    node_size     = "8C16G"
                }
                tiflash = {
                    node_quantity    = 2
                    node_size        = "8C64G"
                    storage_size_gib = 500
                }
                tikv    = {
                    node_quantity    = 6
                    node_size        = "8C32G"
                    storage_size_gib = 500
                }
            }
            port          = 4000
            root_password = "Your_root_password1."
        }
        create_timestamp = "2022-08-26T08:16:33Z"
        id               = "780114"
        name             = "restoreCluster"
        project_id       = "1372813089189561287"
        status           = "PENDING"
    }
    ```

    你可以看到恢复任务的状态是 `PENDING`，集群的状态是 `INITIALIZING`。

5. 等待几分钟。然后使用 `terraform refersh` 更新状态。

6. 在集群状态变为 `AVAILABLE` 后，恢复任务将变为 `RUNNING`，最后变为 `SUCCESS`。

注意，恢复的集群不由 Terraform 管理。你可以通过[导入集群](/tidb-cloud/terraform-use-cluster-resource.md#import-a-cluster)来管理恢复的集群。

## 更新恢复任务

恢复任务无法更新。

## 删除恢复任务

恢复任务无法删除。
