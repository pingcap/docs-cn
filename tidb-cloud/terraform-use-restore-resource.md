---
title: Use Restore Resource
summary: Learn how to use restore resource.
---

# Use Restore Resource

You can learn how to manage a restore task with the `tidbcloud_restore` resource in this document.

The features of the `tidbcloud_restore` resource include the following:

- Create restore tasks for TiDB Dedicated clusters according to your backup.

## Prerequisites

- [Get TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md).
- The backup and restore feature is unavailable for TiDB Serverless clusters. To use restore resources, make sure that you have created a TiDB Dedicated cluster.

## Create a restore task

After creating a backup of a cluster, you can restore the cluster by creating a restore task with the `tidbcloud_restore` resource.

> **Note:**
>
> You can only restore data from a smaller node size to the same or larger node size.

1. Create a directory for the restore and enter it.

2. Create a `restore.tf` file.

    For example:

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

3. Run the `terraform apply` command and type `yes` for confirmation:

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

4. Use the `terraform state show tidbcloud_restore.${resource-name}` command to check the status of the restore task:

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

    You can see the restore task's status is `PENDING` and the cluster's status is `INITIALIZING`.

5. Wait for some minutes. Then use `terraform refersh` to update the status.

6. After the cluster status changes to `AVAILABLE`, the restore task will be `RUNNING` and turn to `SUCCESS` at last.

Note that the restored cluster is not managed by Terraform. You can manage the restored cluster by [importing it](/tidb-cloud/terraform-use-cluster-resource.md#import-a-cluster).

## Update a restore task

Restore tasks cannot be updated.

## Delete a restore task

Restore tasks cannot be deleted.
