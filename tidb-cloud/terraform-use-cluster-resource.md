---
title: Use Cluster Resource
summary: Learn how to use the cluster resource to create and modify a TiDB Cloud cluster.
---

# Use Cluster Resource

You can learn how to manage a TiDB Cloud cluster with the `tidbcloud_cluster` resource in this document.

In addition, you will also learn how to get the necessary information with the `tidbcloud_projects` and `tidbcloud_cluster_specs` data sources.

The features of the `tidbcloud_cluster` resource include the following:

- Create TiDB Serverless and TiDB Dedicated clusters.
- Modify TiDB Dedicated clusters.
- Delete TiDB Serverless and TiDB Dedicated clusters.

## Prerequisites

- [Get TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md).

## Get project IDs using the `tidbcloud_projects` data source

Each TiDB cluster is in a project. Before you create a TiDB cluster, you need to get the ID of the project in which you want to create a cluster.

To view the information of all available projects, you can use the `tidbcloud_projects` data source as follows:

1. In the `main.tf` file that is created when you [Get TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md), add the `data` and `output` blocks as follows:

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

   data "tidbcloud_projects" "example_project" {
     page      = 1
     page_size = 10
   }

   output "projects" {
     value = data.tidbcloud_projects.example_project.items
   }
   ```

   - Use the `data` block to define the data source of TiDB Cloud, including the data source type and the data source name.

      - To use the projects data source, set the data source type as `tidbcloud_projects`.
      - For the data source name, you can define it according to your need. For example, "example_project".
      - For the `tidbcloud_projects` data source, you can use the `page` and `page_size` attributes to limit the maximum number of projects you want to check.

   - Use the `output` block to define the data source information to be displayed in the output, and expose the information for other Terraform configurations to use.

      The `output` block works similarly to returned values in programming languages. See [Terraform documentation](https://www.terraform.io/language/values/outputs) for more details.

   To get all the available configurations for the resources and data sources, see this [configuration documentation](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs).

2. Run the `terraform apply` command to apply the configurations. You need to type `yes` at the confirmation prompt to proceed.

   To skip the prompt, use `terraform apply --auto-approve`:

   ```
   $ terraform apply --auto-approve

   Changes to Outputs:
     + projects = [
         + {
             + cluster_count    = 0
             + create_timestamp = "1649154426"
             + id               = "1372813089191121286"
             + name             = "test1"
             + org_id           = "1372813089189921287"
             + user_count       = 1
           },
         + {
             + cluster_count    = 1
             + create_timestamp = "1640602740"
             + id               = "1372813089189561287"
             + name             = "default project"
             + org_id           = "1372813089189921287"
             + user_count       = 1
           },
       ]

   You can apply this plan to save these new output values to the Terraform state, without changing any real infrastructure.

   Apply complete! Resources: 0 added, 0 changed, 0 destroyed.

   Outputs:

   projects = tolist([
     {
       "cluster_count" = 0
       "create_timestamp" = "1649154426"
       "id" = "1372813089191121286"
       "name" = "test1"
       "org_id" = "1372813089189921287"
       "user_count" = 1
     },
     {
       "cluster_count" = 1
       "create_timestamp" = "1640602740"
       "id" = "1372813089189561287"
       "name" = "default project"
       "org_id" = "1372813089189921287"
       "user_count" = 1
     },
   ])
   ```

Now, you can get all the available projects from the output. Copy one of the project IDs that you need.

## Get cluster specification information using the `tidbcloud_cluster_specs` data source

Before you create a cluster, you need to get the cluster specification information, which contains all available configuration values (such as supported cloud providers, regions, and node sizes).

To get the cluster specification information, you can use the `tidbcloud_cluster_specs` data source as follows:

1. Edit the `main.tf` file as follows:

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
    data "tidbcloud_cluster_specs" "example_cluster_spec" {
    }
    output "cluster_spec" {
      value = data.tidbcloud_cluster_specs.example_cluster_spec.items
    }
    ```

2. Run the `terraform apply --auto-approve` command and you will get the cluster specification information.

    Click the following line to get a part of the example results for your reference.

    <details>
      <summary>Cluster specification</summary>

    ```
    {
        "cloud_provider" = "AWS"
        "cluster_type" = "DEDICATED"
        "region" = "eu-central-1"
        "tidb" = tolist([
          {
            "node_quantity_range" = {
              "min" = 1
              "step" = 1
            }
            "node_size" = "2C8G"
          },
          {
            "node_quantity_range" = {
              "min" = 1
              "step" = 1
            }
            "node_size" = "4C16G"
          },
          {
            "node_quantity_range" = {
              "min" = 1
              "step" = 1
            }
            "node_size" = "8C16G"
          },
          {
            "node_quantity_range" = {
              "min" = 1
              "step" = 1
            }
            "node_size" = "16C32G"
          },
        ])
        "tiflash" = tolist([
          {
            "node_quantity_range" = {
              "min" = 0
              "step" = 1
            }
            "node_size" = "8C64G"
            "storage_size_gib_range" = {
              "max" = 2048
              "min" = 500
            }
          },
          {
            "node_quantity_range" = {
              "min" = 0
              "step" = 1
            }
            "node_size" = "16C128G"
            "storage_size_gib_range" = {
              "max" = 2048
              "min" = 500
            }
          },
        ])
        "tikv" = tolist([
          {
            "node_quantity_range" = {
              "min" = 3
              "step" = 3
            }
            "node_size" = "2C8G"
            "storage_size_gib_range" = {
              "max" = 500
              "min" = 200
            }
          },
          {
            "node_quantity_range" = {
              "min" = 3
              "step" = 3
            }
            "node_size" = "4C16G"
            "storage_size_gib_range" = {
              "max" = 2048
              "min" = 200
            }
          },
          {
            "node_quantity_range" = {
              "min" = 3
              "step" = 3
            }
            "node_size" = "8C32G"
            "storage_size_gib_range" = {
              "max" = 4096
              "min" = 500
            }
          },
          {
            "node_quantity_range" = {
              "min" = 3
              "step" = 3
            }
            "node_size" = "8C64G"
            "storage_size_gib_range" = {
              "max" = 4096
              "min" = 500
            }
          },
          {
            "node_quantity_range" = {
              "min" = 3
              "step" = 3
            }
            "node_size" = "16C64G"
            "storage_size_gib_range" = {
              "max" = 4096
              "min" = 500
            }
          },
        ])
      }
    ```

    </details>

In the results:

- `cloud_provider` is the cloud provider on which a TiDB cluster can be hosted.
- `region` is the region of `cloud_provider`.
- `node_quantity_range` shows the minimum node number and the step to scale a node.
- `node_size` is the size of a node.
- `storage_size_gib_range` shows the minimum and maximum storage size you can set for a node.

## Create a cluster using the cluster resource

> **Note:**
>
> Before you begin, make sure that you have set a Project CIDR in the TiDB Cloud console. For more information, see [Set a Project CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-project-cidr).

You can create a cluster using the `tidbcloud_cluster` resource.

The following example shows how to create a TiDB Dedicated cluster.

1. Create a directory for the cluster and enter it.

2. Create a `cluster.tf` file:

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

    resource "tidbcloud_cluster" "example_cluster" {
      project_id     = "1372813089189561287"
      name           = "firstCluster"
      cluster_type   = "DEDICATED"
      cloud_provider = "AWS"
      region         = "eu-central-1"
      config = {
        root_password = "Your_root_password1."
        port = 4000
        components = {
          tidb = {
            node_size : "8C16G"
            node_quantity : 1
          }
          tikv = {
            node_size : "8C32G"
            storage_size_gib : 500,
            node_quantity : 3
          }
        }
      }
    }
    ```

    Use the `resource` block to define the resource of TiDB Cloud, including the resource type, resource name, and resource details.

    - To use the cluster resource, set the resource type as `tidbcloud_cluster`.
    - For the resource name, you can define it according to your need. For example, `example_cluster`.
    - For the resource details, you can configure them according to the Project ID and the cluster specification information.

3. Run the `terraform apply` command. It is not recommended to use `terraform apply --auto-approve` when you apply a resource.

    ```shell
    $ terraform apply

    Terraform will perform the following actions:

      # tidbcloud_cluster.example_cluster will be created
      + resource "tidbcloud_cluster" "example_cluster" {
          + cloud_provider = "AWS"
          + cluster_type   = "DEDICATED"
          + config         = {
              + components     = {
                  + tidb = {
                      + node_quantity = 1
                      + node_size     = "8C16G"
                    }
                  + tikv = {
                      + node_quantity    = 3
                      + node_size        = "8C32G"
                      + storage_size_gib = 500
                    }
                }
              + ip_access_list = [
                  + {
                      + cidr        = "0.0.0.0/0"
                      + description = "all"
                    },
                ]
              + port           = 4000
              + root_password  = "Your_root_password1."
            }
          + id             = (known after apply)
          + name           = "firstCluster"
          + project_id     = "1372813089189561287"
          + region         = "eu-central-1"
          + status         = (known after apply)
        }

    Plan: 1 to add, 0 to change, 0 to destroy.

    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value:
    ```

   As in the above result, Terraform generates an execution plan for you, which describes the actions Terraform will take:

   - You can check the difference between the configurations and the states.
   - You can also see the results of this `apply`. It will add a new resource, and no resource will be changed or destroyed.
   - The `known after apply` shows that you will get the value after `apply`.

4. If everything in your plan looks fine, type `yes` to continue:

    ```
    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_cluster.example_cluster: Creating...
    tidbcloud_cluster.example_cluster: Creation complete after 1s [id=1379661944630234067]

    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

    ```

5. Use the `terraform show` or `terraform state show tidbcloud_cluster.${resource-name}` command to inspect the state of your resource. The former will show the states of all resources and data sources.

    ```shell
    $ terraform state show tidbcloud_cluster.example_cluster

    # tidbcloud_cluster.example_cluster:
    resource "tidbcloud_cluster" "example_cluster" {
        cloud_provider = "AWS"
        cluster_type   = "DEDICATED"
        config         = {
            components     = {
                tidb = {
                    node_quantity = 1
                    node_size     = "8C16G"
                }
                tikv = {
                    node_quantity    = 3
                    node_size        = "8C32G"
                    storage_size_gib = 500
                }
            }
            ip_access_list = [
                # (1 unchanged element hidden)
            ]
            port           = 4000
            root_password  = "Your_root_password1."
        }
        id             = "1379661944630234067"
        name           = "firstCluster"
        project_id     = "1372813089189561287"
        region         = "eu-central-1"
        status         = "CREATING"
    }
    ```

    The status of the cluster is `CREATING`. In this case, you need to wait until it changes to `AVAILABLE`, which usually takes 10 minutes at least.

6. If you want to check the latest status, run the `terraform refresh` command to update the state, and then run the `terraform state show tidbcloud_cluster.${resource-name}` command to display the state.

    ```
    $ terraform refresh

    tidbcloud_cluster.example_cluster: Refreshing state... [id=1379661944630234067]

    $ terraform state show tidbcloud_cluster.example_cluste

    # tidbcloud_cluster.example_cluster:
    resource "tidbcloud_cluster" "example_cluster" {
        cloud_provider = "AWS"
        cluster_type   = "DEDICATED"
        config         = {
            components     = {
                tidb = {
                    node_quantity = 1
                    node_size     = "8C16G"
                }
                tikv = {
                    node_quantity    = 3
                    node_size        = "8C32G"
                    storage_size_gib = 500
                }
            }
            ip_access_list = [
                # (1 unchanged element hidden)
            ]
            port           = 4000
            root_password  = "Your_root_password1."
        }
        id             = "1379661944630234067"
        name           = "firstCluster"
        project_id     = "1372813089189561287"
        region         = "eu-central-1"
        status         = "AVAILABLE"
    }
    ```

When the status is `AVAILABLE`, it indicates that your TiDB cluster is created and ready for use.

## Modify a TiDB Dedicated cluster

For a TiDB Dedicated cluster, you can use Terraform to manage cluster resources as follows:

- Add a TiFlash component to the cluster.
- Scale the cluster.
- Pause or resume the cluster.

### Add a TiFlash component

1. In the `cluster.tf` file that is used when you [create the cluster](#create-a-cluster-using-the-cluster-resource), add the `tiflash` configurations to the `components` field.

    For example:

    ```
        components = {
          tidb = {
            node_size : "8C16G"
            node_quantity : 1
          }
          tikv = {
            node_size : "8C32G"
            storage_size_gib : 500
            node_quantity : 3
          }
          tiflash = {
            node_size : "8C64G"
            storage_size_gib : 500
            node_quantity : 1
          }
        }
    ```

2. Run the `terraform apply` command:

    ```
    $ terraform apply

    tidbcloud_cluster.example_cluster: Refreshing state... [id=1379661944630234067]

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      ~ update in-place

    Terraform will perform the following actions:

      # tidbcloud_cluster.example_cluster will be updated in-place
      ~ resource "tidbcloud_cluster" "example_cluster" {
          ~ config         = {
              ~ components     = {
                  + tiflash = {
                      + node_quantity    = 1
                      + node_size        = "8C64G"
                      + storage_size_gib = 500
                    }
                    # (2 unchanged attributes hidden)
                }
                # (3 unchanged attributes hidden)
            }
            id             = "1379661944630234067"
            name           = "firstCluster"
          ~ status         = "AVAILABLE" -> (known after apply)
            # (4 unchanged attributes hidden)
        }

    Plan: 0 to add, 1 to change, 0 to destroy.

    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value:

    ```

    As in the above execution plan, TiFlash will be added, and one resource will be changed.

3. If everything in your plan looks fine, type `yes` to continue:

    ```
      Enter a value: yes

    tidbcloud_cluster.example_cluster: Modifying... [id=1379661944630234067]
    tidbcloud_cluster.example_cluster: Modifications complete after 2s [id=1379661944630234067]

    Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
    ```

4. Use `terraform state show tidbcloud_cluster.${resource-name}` to see the status:

    ```
    $ terraform state show tidbcloud_cluster.example_cluster

    # tidbcloud_cluster.example_cluster:
    resource "tidbcloud_cluster" "example_cluster" {
        cloud_provider = "AWS"
        cluster_type   = "DEDICATED"
        config         = {
            components     = {
                tidb    = {
                    node_quantity = 1
                    node_size     = "8C16G"
                }
                tiflash = {
                    node_quantity    = 1
                    node_size        = "8C64G"
                    storage_size_gib = 500
                }
                tikv    = {
                    node_quantity    = 3
                    node_size        = "8C32G"
                    storage_size_gib = 500
                }
            }
            ip_access_list = [
                # (1 unchanged element hidden)
            ]
            port           = 4000
            root_password  = "Your_root_password1."
        }
        id             = "1379661944630234067"
        name           = "firstCluster"
        project_id     = "1372813089189561287"
        region         = "eu-central-1"
        status         = "MODIFYING"
    }
    ```

The `MODIFYING` status indicates that the cluster is changing now. Wait for a moment. The status will be changed to `AVAILABLE`.

### Scale a TiDB cluster

You can scale a TiDB cluster when its status is `AVAILABLE`.

1. In the `cluster.tf` file that is used when you [create the cluster](#create-a-cluster-using-the-cluster-resource), edit the `components` configurations.

    For example, to add one more node for TiDB, 3 more nodes for TiKV (The number of TiKV nodes needs to be a multiple of 3 for its step is 3. You can [get this information from the cluster specifcation](#get-cluster-specification-information-using-the-tidbcloud_cluster_specs-data-source)), and one more node for TiFlash, you can edit the configurations as follows:

   ```
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
   ```

2. Run the `terraform apply` command and type `yes` for confirmation:

   ```
   $ terraform apply

   tidbcloud_cluster.example_cluster: Refreshing state... [id=1379661944630234067]

   Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
     ~ update in-place

   Terraform will perform the following actions:

     # tidbcloud_cluster.example_cluster will be updated in-place
     ~ resource "tidbcloud_cluster" "example_cluster" {
         ~ config         = {
             ~ components     = {
                 ~ tidb    = {
                     ~ node_quantity = 1 -> 2
                       # (1 unchanged attribute hidden)
                   }
                 ~ tiflash = {
                     ~ node_quantity    = 1 -> 2
                       # (2 unchanged attributes hidden)
                   }
                 ~ tikv    = {
                     ~ node_quantity    = 3 -> 6
                       # (2 unchanged attributes hidden)
                   }
               }
               # (3 unchanged attributes hidden)
           }
           id             = "1379661944630234067"
           name           = "firstCluster"
         ~ status         = "AVAILABLE" -> (known after apply)
           # (4 unchanged attributes hidden)
       }

   Plan: 0 to add, 1 to change, 0 to destroy.

   Do you want to perform these actions?
     Terraform will perform the actions described above.
     Only 'yes' will be accepted to approve.

     Enter a value: yes

   tidbcloud_cluster.example_cluster: Modifying... [id=1379661944630234067]
   tidbcloud_cluster.example_cluster: Modifications complete after 2s [id=1379661944630234067]

   Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
   ```

Wait for the status to turn from `MODIFYING` to `AVAILABLE`.

### Pause or resume a cluster

You can pause a cluster when its status is `AVAILABLE` or resume a cluster when its status is `PAUSED`.

- Set `paused = true` to pause a cluster.
- Set `paused = false` to resume a cluster.

1. In the `cluster.tf` file that is used when you [create the cluster](#create-a-cluster-using-the-cluster-resource), add `pause = true` to the `config` configurations:

   ```
   config = {
       paused = true
       root_password = "Your_root_password1."
       port          = 4000
       ...
     }
   ```

2. Run the `terraform apply` command and type `yes` after check:

   ```
   $ terraform apply

   tidbcloud_cluster.example_cluster: Refreshing state... [id=1379661944630234067]

   Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
     ~ update in-place

   Terraform will perform the following actions:

     # tidbcloud_cluster.example_cluster will be updated in-place
     ~ resource "tidbcloud_cluster" "example_cluster" {
         ~ config         = {
             + paused         = true
               # (4 unchanged attributes hidden)
           }
           id             = "1379661944630234067"
           name           = "firstCluster"
         ~ status         = "AVAILABLE" -> (known after apply)
           # (4 unchanged attributes hidden)
       }

   Plan: 0 to add, 1 to change, 0 to destroy.

   Do you want to perform these actions?
     Terraform will perform the actions described above.
     Only 'yes' will be accepted to approve.

     Enter a value: yes

   tidbcloud_cluster.example_cluster: Modifying... [id=1379661944630234067]
   tidbcloud_cluster.example_cluster: Modifications complete after 2s [id=1379661944630234067]

   Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
   ```

3. Use the `terraform state show tidbcloud_cluster.${resource-name}` command to check the status:

   ```
   $ terraform state show tidbcloud_cluster.example_cluster

   # tidbcloud_cluster.example_cluster:
   resource "tidbcloud_cluster" "example_cluster" {
       cloud_provider = "AWS"
       cluster_type   = "DEDICATED"
       config         = {
           components     = {
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
           ip_access_list = [
               # (1 unchanged element hidden)
           ]
           paused         = true
           port           = 4000
           root_password  = "Your_root_password1."
       }
       id             = "1379661944630234067"
       name           = "firstCluster"
       project_id     = "1372813089189561287"
       region         = "eu-central-1"
       status         = "PAUSED"
   }
   ```

4. When you need to resume the cluster, set `paused = false`:

   ```
   config = {
       paused = false
       root_password = "Your_root_password1."
       port          = 4000
       ...
     }
   ```

5. Run the `terraform apply` command and type `yes` for confirmation. If you use the `terraform state show tidbcloud_cluster.${resource-name}` command to check the status, you will find it turns to `RESUMING`:

   ```
   # tidbcloud_cluster.example_cluster:
   resource "tidbcloud_cluster" "example_cluster" {
       cloud_provider = "AWS"
       cluster_type   = "DEDICATED"
       config         = {
           components     = {
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
           ip_access_list = [
               # (1 unchanged element hidden)
           ]
           paused         = false
           port           = 4000
           root_password  = "Your_root_password1."
       }
       id             = "1379661944630234067"
       name           = "firstCluster"
       project_id     = "1372813089189561287"
       region         = "eu-central-1"
       status         = "RESUMING"
   }
   ```

6. Wait for a moment, then use the `terraform refersh` command to update the state. The status will be changed to `AVAILABLE` finally.

Now, you have created and managed a TiDB Dedicated cluster with Terraform. Next, you can try creating a backup of the cluster by our [backup resource](/tidb-cloud/terraform-use-backup-resource.md).

## Import a cluster

For a TiDB cluster that is not managed by Terraform, you can use Terraform to manage it just by importing it.

For example, you can import a cluster that is not created by Terraform or import a cluster that is [created with the restore resource](/tidb-cloud/terraform-use-restore-resource.md#create-a-restore-task).

1. Create a `import_cluster.tf` file as follows:

    ```
    terraform {
     required_providers {
       tidbcloud = {
         source = "tidbcloud/tidbcloud"
       }
     }
   }
    resource "tidbcloud_cluster" "import_cluster" {}
    ```

2. Import the cluster by `terraform import tidbcloud_cluster.import_cluster projectId,clusterId`:

   For example:

    ```
    $ terraform import tidbcloud_cluster.import_cluster 1372813089189561287,1379661944630264072

    tidbcloud_cluster.import_cluster: Importing from ID "1372813089189561287,1379661944630264072"...
    tidbcloud_cluster.import_cluster: Import prepared!
      Prepared tidbcloud_cluster for import
    tidbcloud_cluster.import_cluster: Refreshing state... [id=1379661944630264072]

    Import successful!

    The resources that were imported are shown above. These resources are now in
    your Terraform state and will henceforth be managed by Terraform.
    ```

3. Run the `terraform state show tidbcloud_cluster.import_cluster` command to check the status of the cluster:

    ```
    $ terraform state show tidbcloud_cluster.import_cluster

    # tidbcloud_cluster.import_cluster:
    resource "tidbcloud_cluster" "import_cluster" {
        cloud_provider = "AWS"
        cluster_type   = "DEDICATED"
        config         = {
            components = {
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
            port       = 4000
        }
        id             = "1379661944630264072"
        name           = "restoreCluster"
        project_id     = "1372813089189561287"
        region         = "eu-central-1"
        status         = "AVAILABLE"
    }
    ```

4. To manage the cluster using Terraform, you can copy the output of the previous step to your configuration file. Note that you need to delete the lines of `id` and `status`, because they will be controlled by Terraform instead:

    ```
    resource "tidbcloud_cluster" "import_cluster" {
          cloud_provider = "AWS"
          cluster_type   = "DEDICATED"
          config         = {
              components = {
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
              port       = 4000
          }
          name           = "restoreCluster"
          project_id     = "1372813089189561287"
          region         = "eu-central-1"
    }
    ```

5. You can use `terraform fmt` to format your configuration file:

    ```
    $ terraform fmt
    ```

6. To ensure the consistency of the configuration and state, you can execute `terraform plan` or `terraform apply`. If you see `No changes`, the import is successful.

    ```
    $ terraform apply

    tidbcloud_cluster.import_cluster: Refreshing state... [id=1379661944630264072]

    No changes. Your infrastructure matches the configuration.

    Terraform has compared your real infrastructure against your configuration and found no differences, so no changes are needed.

    Apply complete! Resources: 0 added, 0 changed, 0 destroyed.
    ```

Now you can use Terraform to manage the cluster.

## Delete a cluster

To delete a cluster, go to the cluster directory where the corresponding `cluster.tf` file is located, and then run the `terraform destroy` command to destroy the cluster resource:

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
