---
title: Use Import Resource
summary: Learn how to manage the import task using the import resource.
---

# Use Import Resource

You can learn how to import data to a TiDB Cloud cluster with the `tidbcloud_import` resource in this document.

The features of the `tidbcloud_import` resource include the following:

- Create import tasks for TiDB Serverless and TiDB Dedicated clusters.
- Import data either from local disks or from Amazon S3 buckets.
- Cancel ongoing import tasks.

## Prerequisites

- [Get TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md).
- [Create a TiDB Serverless cluster](/tidb-cloud/create-tidb-cluster-serverless.md) or [Create a TiDB Dedicated cluster](/tidb-cloud/create-tidb-cluster.md).

## Create and run an import task

You can manage either a local import task or an Amazon S3 import task using the import resource.

### Create and run a local import task

> **Note:**
>
> Importing local files is supported only for TiDB Serverless clusters, not for TiDB Dedicated clusters.

1. Create a CSV file for import. For example:

   ```
   id;name;age
   1;Alice;20
   2;Bob;30
   ```

2. Create an `import` directory, and then create a `main.tf` inside it. For example:

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

    resource "tidbcloud_import" "example_local" {
      project_id  = "your_project_id"
      cluster_id  = "your_cluster_id"
      type        = "LOCAL"
      data_format = "CSV"
      csv_format = {
        separator = ";"
      }
      target_table = {
        database = "test"
        table  = "import_test"
      }
      file_name = "your_csv_path"
    }
    ```

   Replace resource values (such as project ID, cluster ID, and CSV path) in the file with your own. And you can find details of `csv_format` on the [configuration page](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/import#nested-schema-for-csv_format).

3. Run the `terraform apply` command to create an import task, and then type `yes` to confirm the creation and start the import:

   ```
   $ terraform apply
   ...
   Plan: 1 to add, 0 to change, 0 to destroy.

   Do you want to perform these actions?
   Terraform will perform the actions described above.
   Only 'yes' will be accepted to approve.

   Enter a value: yes

   tidbcloud_import.example_local: Creating...
   tidbcloud_import.example_local: Creation complete after 6s [id=781074]
   ```

4. Use `terraform state show tidbcloud_import.${resource-name}` to check the status of the import task:

   ```
   $ terraform state show tidbcloud_import.example_local
   # tidbcloud_import.example_local:
   resource "tidbcloud_import" "example_local" {
       all_completed_tables          = [
           {
               message    = ""
               result     = "SUCCESS"
               table_name = "`test`.`import_test`"
           },
       ]
       cluster_id                    = "1379661944641274168"
       completed_percent             = 100
       completed_tables              = 1
       created_at                    = "2023-02-06T05:39:46.000Z"
       csv_format                    = {
           separator = ";"
       }
       data_format                   = "CSV"
       elapsed_time_seconds          = 48
       file_name                     = "./t.csv"
       id                            = "781074"
       new_file_name                 = "2023-02-06T05:39:42Z-t.csv"
       pending_tables                = 0
       post_import_completed_percent = 100
       processed_source_data_size    = "31"
       project_id                    = "1372813089191151295"
       status                        = "IMPORTING"
       target_table                  = {
           database = "test"
           table  = "import_test"
       }
       total_files                   = 0
       total_size                    = "31"
       total_tables_count            = 1
       type                          = "LOCAL"
   }
   ```

5. Use `terraform refresh` to update the status after several minutes:

   ```
   $ terraform refresh && terraform state show tidbcloud_import.example_local
   tidbcloud_import.example_local: Refreshing state... [id=781074]
   # tidbcloud_import.example_local:
   resource "tidbcloud_import" "example_local" {
       all_completed_tables          = [
           {
               message    = ""
               result     = "SUCCESS"
               table_name = "`test`.`import_test`"
           },
       ]
       cluster_id                    = "1379661944641274168"
       completed_percent             = 100
       completed_tables              = 1
       created_at                    = "2023-02-06T05:39:46.000Z"
       csv_format                    = {
           separator = ";"
       }
       data_format                   = "CSV"
       elapsed_time_seconds          = 49
       file_name                     = "./t.csv"
       id                            = "781074"
       new_file_name                 = "2023-02-06T05:39:42Z-t.csv"
       pending_tables                = 0
       post_import_completed_percent = 100
       processed_source_data_size    = "31"
       project_id                    = "1372813089191151295"
       status                        = "COMPLETED"
       target_table                  = {
           database = "test"
           table  = "import_test"
       }
       total_files                   = 0
       total_size                    = "31"
       total_tables_count            = 1
       type                          = "LOCAL"
   }
   ```

   When the status turns to `COMPLETED`, it indicates that the import task is finished.

6. Check the imported data with MySQL CLI:

   ```
   mysql> SELECT * FROM test.import_test;
   +------+-------+------+
   | id   | name  | age  |
   +------+-------+------+
   |    1 | Alice |   20 |
   |    2 | Bob   |   30 |
   +------+-------+------+
   2 rows in set (0.24 sec)
   ```

### Create and run an Amazon S3 import task

> **Note:**
>
> To allow TiDB Cloud to access your files in the Amazon S3 bucket, you need to [configure Amazon S3 access](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access) first.

1. Create an `import` directory, and then create a `main.tf` inside it. For example:

   ```
   terraform {
     required_providers {
       tidbcloud = {
         source = "tidbcloud/tidbcloud"
       }
     }
   }

   provider "tidbcloud" {
     public_key  = "your_public_key"
     private_key = "your_private_key"
   }

   resource "tidbcloud_import" "example_s3_csv" {
     project_id   = "your_project_id"
     cluster_id   = "your_cluster_id"
     type         = "S3"
     data_format  = "CSV"
     aws_role_arn = "your_arn"
     source_url   = "your_url"
   }

   resource "tidbcloud_import" "example_s3_parquet" {
     project_id   = "your_project_id"
     cluster_id   = "your_cluster_id"
     type         = "S3"
     data_format  = "Parquet"
     aws_role_arn = "your_arn"
     source_url   = "your_url"
   }
   ```

2. Run the `terraform apply` command to create an import task, and then type `yes` to confirm the creation and start the import:

   ```
   $ terraform apply
   ...
   Plan: 2 to add, 0 to change, 0 to destroy.

   Do you want to perform these actions?
   Terraform will perform the actions described above.
   Only 'yes' will be accepted to approve.

   Enter a value: yes

   tidbcloud_import.example_s3_csv: Creating...
   tidbcloud_import.example_s3_csv: Creation complete after 3s [id=781075]
   tidbcloud_import.example_s3_parquet: Creating...
   tidbcloud_import.example_s3_parquet: Creation complete after 4s [id=781076]
   ```

3. Use `terraform refresh` and `terraform state show tidbcloud_import.${resource-name}` to update and check the status of the import task.

## Update an import task

Import tasks cannot be updated.

## Delete an import task

For Terraform, deleting an import task means canceling the corresponding import resource.

You cannot cancel a `COMPLETED` import task. Otherwise, you will get a `Delete Error` as in the following example:

```
$ terraform destroy
...
Plan: 0 to add, 0 to change, 1 to destroy.

Do you really want to destroy all resources?
  Terraform will destroy all your managed infrastructure, as shown above.
  There is no undo. Only 'yes' will be accepted to confirm.

  Enter a value: yes

tidbcloud_import.example_local: Destroying... [id=781074]
╷
│ Error: Delete Error
│
│ Unable to call CancelImport, got error: [DELETE /api/internal/projects/{project_id}/clusters/{cluster_id}/imports/{id}][500] CancelImport default  &{Code:59900104 Details:[] Message:failed to cancel
│ import}
╵
```

You can cancel an import task whose status is `IMPORTING`. For example:

```
$ terraform destroy
...
Plan: 0 to add, 0 to change, 1 to destroy.

Do you really want to destroy all resources?
  Terraform will destroy all your managed infrastructure, as shown above.
  There is no undo. Only 'yes' will be accepted to confirm.

  Enter a value: yes

tidbcloud_import.example_local: Destroying... [id=781074]
tidbcloud_import.example_local: Destruction complete after 0s

Destroy complete! Resources: 1 destroyed.
```

## Configurations

See [configuration documentation](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/import) to get all the available configurations for the import resource.
