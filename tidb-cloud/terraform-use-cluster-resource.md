---
title: 使用集群资源
summary: 了解如何使用集群资源创建和修改 TiDB Cloud 集群。
---

# 使用集群资源

本文档介绍如何使用 `tidbcloud_cluster` 资源管理 TiDB Cloud 集群。

此外，你还将学习如何使用 `tidbcloud_projects` 和 `tidbcloud_cluster_specs` 数据源获取必要信息。

`tidbcloud_cluster` 资源的功能包括以下内容：

- 创建 TiDB Cloud Serverless 和 TiDB Cloud Dedicated 集群。
- 修改 TiDB Cloud Dedicated 集群。
- 删除 TiDB Cloud Serverless 和 TiDB Cloud Dedicated 集群。

## 前提条件

- [获取 TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md)。

## 使用 `tidbcloud_projects` 数据源获取项目 ID

每个 TiDB 集群都在一个项目中。在创建 TiDB 集群之前，你需要获取要在其中创建集群的项目 ID。

要查看所有可用项目的信息，你可以按照以下方式使用 `tidbcloud_projects` 数据源：

1. 在[获取 TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md) 时创建的 `main.tf` 文件中，添加 `data` 和 `output` 块，如下所示：

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
     sync = true
   }

   data "tidbcloud_projects" "example_project" {
     page      = 1
     page_size = 10
   }

   output "projects" {
     value = data.tidbcloud_projects.example_project.items
   }
   ```

   - 使用 `data` 块定义 TiDB Cloud 的数据源，包括数据源类型和数据源名称。

      - 要使用项目数据源，请将数据源类型设置为 `tidbcloud_projects`。
      - 对于数据源名称，你可以根据需要定义它。例如，"example_project"。
      - 对于 `tidbcloud_projects` 数据源，你可以使用 `page` 和 `page_size` 属性来限制要检查的最大项目数。

   - 使用 `output` 块定义要在输出中显示的数据源信息，并公开信息供其他 Terraform 配置使用。

      `output` 块的工作方式类似于编程语言中的返回值。有关更多详细信息，请参阅 [Terraform 文档](https://www.terraform.io/language/values/outputs)。

   要获取资源和数据源的所有可用配置，请参阅此[配置文档](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs)。

2. 运行 `terraform apply` 命令以应用配置。你需要在确认提示时输入 `yes` 才能继续。

   要跳过提示，请使用 `terraform apply --auto-approve`：

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

现在，你可以从输出中获取所有可用的项目。复制你需要的项目 ID。
## 使用 `tidbcloud_cluster_specs` 数据源获取集群规格信息

在创建集群之前，你需要获取集群规格信息，其中包含所有可用的配置值（如支持的云服务提供商、区域和节点大小）。

要获取集群规格信息，你可以按照以下方式使用 `tidbcloud_cluster_specs` 数据源：

1. 编辑 `main.tf` 文件，如下所示：

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
      sync = true
    }
    data "tidbcloud_cluster_specs" "example_cluster_spec" {
    }
    output "cluster_spec" {
      value = data.tidbcloud_cluster_specs.example_cluster_spec.items
    }
    ```

2. 运行 `terraform apply --auto-approve` 命令，你将获得集群规格信息。

    点击以下行查看部分示例结果供参考。

    <details>
      <summary>集群规格</summary>

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

在结果中：

- `cloud_provider` 是可以托管 TiDB 集群的云服务提供商。
- `region` 是 `cloud_provider` 的区域。
- `node_quantity_range` 显示最小节点数和扩展节点的步长。
- `node_size` 是节点的大小。
- `storage_size_gib_range` 显示可以为节点设置的最小和最大存储大小。
## 使用集群资源创建集群

> **注意：**
>
> 在开始之前，请确保你已在 TiDB Cloud 控制台中设置了 CIDR。有关更多信息，请参阅[设置 CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region)。

你可以使用 `tidbcloud_cluster` 资源创建集群。

以下示例展示如何创建 TiDB Cloud Dedicated 集群。

1. 为集群创建一个目录并进入该目录。

2. 创建一个 `cluster.tf` 文件：

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
     sync = true
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

    使用 `resource` 块定义 TiDB Cloud 的资源，包括资源类型、资源名称和资源详细信息。

    - 要使用集群资源，请将资源类型设置为 `tidbcloud_cluster`。
    - 对于资源名称，你可以根据需要定义它。例如，`example_cluster`。
    - 对于资源详细信息，你可以根据项目 ID 和集群规格信息进行配置。

3. 运行 `terraform apply` 命令。不建议在应用资源时使用 `terraform apply --auto-approve`。

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

   如上述结果所示，Terraform 为你生成了一个执行计划，描述了 Terraform 将采取的操作：

   - 你可以检查配置和状态之间的差异。
   - 你还可以看到此 `apply` 的结果。它将添加一个新资源，不会更改或销毁任何资源。
   - `known after apply` 表示你将在 `apply` 后获得该值。

4. 如果你的计划看起来没有问题，输入 `yes` 继续：

    ```
    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_cluster.example_cluster: Creating...
    tidbcloud_cluster.example_cluster: Creation complete after 1s [id=1379661944630234067]

    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

    ```

5. 使用 `terraform show` 或 `terraform state show tidbcloud_cluster.${resource-name}` 命令检查资源的状态。前者将显示所有资源和数据源的状态。

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

    集群的状态是 `CREATING`。在这种情况下，你需要等待它变为 `AVAILABLE`，这通常需要至少 10 分钟。

6. 如果你想检查最新状态，运行 `terraform refresh` 命令更新状态，然后运行 `terraform state show tidbcloud_cluster.${resource-name}` 命令显示状态。

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

当状态为 `AVAILABLE` 时，表示你的 TiDB 集群已创建完成并可以使用。
## 修改 TiDB Cloud Dedicated 集群

对于 TiDB Cloud Dedicated 集群，你可以使用 Terraform 管理集群资源，如下所示：

- 向集群添加 TiFlash 组件。
- 扩缩容集群。
- 暂停或恢复集群。

### 添加 TiFlash 组件

1. 在[创建集群](#使用集群资源创建集群)时使用的 `cluster.tf` 文件中，将 `tiflash` 配置添加到 `components` 字段。

    例如：

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

2. 运行 `terraform apply` 命令：

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

    如上述执行计划所示，将添加 TiFlash，并且将更改一个资源。

3. 如果你的计划看起来没有问题，输入 `yes` 继续：

    ```
      Enter a value: yes

    tidbcloud_cluster.example_cluster: Modifying... [id=1379661944630234067]
    tidbcloud_cluster.example_cluster: Modifications complete after 2s [id=1379661944630234067]

    Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
    ```

4. 使用 `terraform state show tidbcloud_cluster.${resource-name}` 查看状态：

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

`MODIFYING` 状态表示集群正在更改中。等待一段时间后，状态将变为 `AVAILABLE`。
### 扩缩容 TiDB 集群

当集群状态为 `AVAILABLE` 时，你可以扩缩容集群。

1. 在[创建集群](#使用集群资源创建集群)时使用的 `cluster.tf` 文件中，编辑 `components` 配置。

    例如，要为 TiDB 增加一个节点，为 TiKV 增加 3 个节点（TiKV 节点数需要是 3 的倍数，因为其步长为 3。你可以[从集群规格中获取此信息](#使用-tidbcloud_cluster_specs-数据源获取集群规格信息)），为 TiFlash 增加一个节点，你可以按如下方式编辑配置：

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

2. 运行 `terraform apply` 命令并输入 `yes` 确认：

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

等待状态从 `MODIFYING` 变为 `AVAILABLE`。
### 暂停或恢复集群

当集群状态为 `AVAILABLE` 时，你可以暂停集群，或者当集群状态为 `PAUSED` 时，你可以恢复集群。

- 设置 `paused = true` 暂停集群。
- 设置 `paused = false` 恢复集群。

1. 在[创建集群](#使用集群资源创建集群)时使用的 `cluster.tf` 文件中，将 `pause = true` 添加到 `config` 配置中：

   ```
   config = {
       paused = true
       root_password = "Your_root_password1."
       port          = 4000
       ...
     }
   ```

2. 运行 `terraform apply` 命令并在检查后输入 `yes`：

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

3. 使用 `terraform state show tidbcloud_cluster.${resource-name}` 命令检查状态：

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

4. 当你需要恢复集群时，设置 `paused = false`：

   ```
   config = {
       paused = false
       root_password = "Your_root_password1."
       port          = 4000
       ...
     }
   ```

5. 运行 `terraform apply` 命令并输入 `yes` 确认。如果你使用 `terraform state show tidbcloud_cluster.${resource-name}` 命令检查状态，你会发现它变为 `RESUMING`：

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

6. 等待一段时间，然后使用 `terraform refersh` 命令更新状态。状态最终将变为 `AVAILABLE`。

现在，你已经使用 Terraform 创建和管理了一个 TiDB Cloud Dedicated 集群。接下来，你可以尝试使用我们的[备份资源](/tidb-cloud/terraform-use-backup-resource.md)创建集群的备份。
## 导入集群

对于不是由 Terraform 管理的 TiDB 集群，你可以通过导入它来使用 Terraform 管理它。

例如，你可以导入不是由 Terraform 创建的集群，或导入[使用恢复资源创建](/tidb-cloud/terraform-use-restore-resource.md#create-a-restore-task)的集群。

1. 创建一个 `import_cluster.tf` 文件，如下所示：

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

2. 通过 `terraform import tidbcloud_cluster.import_cluster projectId,clusterId` 导入集群：

   例如：

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

3. 运行 `terraform state show tidbcloud_cluster.import_cluster` 命令检查集群的状态：

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

4. 要使用 Terraform 管理集群，你可以将上一步的输出复制到你的配置文件中。注意，你需要删除 `id` 和 `status` 行，因为它们将由 Terraform 控制：

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

5. 你可以使用 `terraform fmt` 格式化你的配置文件：

    ```
    $ terraform fmt
    ```

6. 为确保配置和状态的一致性，你可以执行 `terraform plan` 或 `terraform apply`。如果你看到 `No changes`，则导入成功。

    ```
    $ terraform apply

    tidbcloud_cluster.import_cluster: Refreshing state... [id=1379661944630264072]

    No changes. Your infrastructure matches the configuration.

    Terraform has compared your real infrastructure against your configuration and found no differences, so no changes are needed.

    Apply complete! Resources: 0 added, 0 changed, 0 destroyed.
    ```

现在你可以使用 Terraform 管理集群了。

## 删除集群

要删除集群，进入包含相应 `cluster.tf` 文件的集群目录，然后运行 `terraform destroy` 命令销毁集群资源：

```
$ terraform destroy

Plan: 0 to add, 0 to change, 1 to destroy.

Do you really want to destroy all resources?
Terraform will destroy all your managed infrastructure, as shown above.
There is no undo. Only 'yes' will be accepted to confirm.

Enter a value: yes
```

现在，如果你运行 `terraform show` 命令，你将得到空输出，因为资源已被清除：

```
$ terraform show
```
