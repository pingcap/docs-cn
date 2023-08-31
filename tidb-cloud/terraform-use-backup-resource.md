---
title: Use Backup Resource
summary: Learn how to create a backup of a TiDB Cloud cluster using the backup resource.
---

# Use Backup Resource

You can learn how to create a backup of a TiDB Cloud cluster with the `tidbcloud_backup` resource in this document.

The features of the `tidbcloud_backup` resource include the following:

- Create backups for TiDB Dedicated clusters.
- Delete backups for TiDB Dedicated clusters.

## Prerequisites

- [Get TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md).
- The backup and restore feature is unavailable to TiDB Serverless clusters. To use backup resources, make sure that you have created a TiDB Dedicated cluster.

## Create a backup with the backup resource

1. Create a directory for the backup and enter it.

2. Create a `backup.tf` file.

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
    resource "tidbcloud_backup" "example_backup" {
      project_id  = "1372813089189561287"
      cluster_id  = "1379661944630234067"
      name        = "firstBackup"
      description = "create by terraform"
    }
    ```

    You need to replace resource values (such as project ID and cluster ID) in the file with your own.

    If you have maintained a cluster resource (for example, `example_cluster`) using Terraform, you can also configure the backup resource as follows, without specifying the actual project ID and cluster ID.

    ```
    resource "tidbcloud_backup" "example_backup" {
      project_id  = tidbcloud_cluster.example_cluster.project_id
      cluster_id  = tidbcloud_cluster.example_cluster.id
      name        = "firstBackup"
      description = "create by terraform"
    }
    ```

3. Run the `terraform apply` command:

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

4. Type `yes` to create a backup:

    ```
      Enter a value: yes

    tidbcloud_backup.example_backup: Creating...
    tidbcloud_backup.example_backup: Creation complete after 2s [id=1350048]

    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

    ```

5. Use `terraform state show tidbcloud_backup.${resource-name}` to check the status of the backup:

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

6. Wait for some minutes. Then use `terraform refersh` to update the status:

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

When the status turns to `SUCCESS`, it indicates that you have created a backup for your cluster. Pay attention that the backup cannot be updated after the creation.

Now, you have created a backup for the cluster. If you want to use the backup to restore the cluster, you can [use the restore resources](/tidb-cloud/terraform-use-restore-resource.md).

## Update a backup

Backups cannot be updated.

## Delete a backup

To delete a backup, go to the backup directory where the corresponding `backup.tf` file is located, and then run the `terraform destroy` command to destroy the backup resource.

```
$ terraform destroy

Plan: 0 to add, 0 to change, 1 to destroy.

Do you really want to destroy all resources?
Terraform will destroy all your managed infrastructure, as shown above.
There is no undo. Only 'yes' will be accepted to confirm.

Enter a value: yes
```

Now, if you run the `terraform show` command, you will get nothing because the resource has been cleared:

```
$ terraform show
```
