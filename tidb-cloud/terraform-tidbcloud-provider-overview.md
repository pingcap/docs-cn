---
title: Terraform Integration Overview
summary: Create, manage, and update your TiDB Cloud resources through Terraform.
---

# Terraform Integration Overview

[Terraform](https://www.terraform.io/) is an infrastructure as code tool that lets you define both cloud and self-hosted resources in human-readable configuration files that you can version, reuse, and share.

[TiDB Cloud Terraform Provider](https://registry.terraform.io/providers/tidbcloud/tidbcloud) is a plugin that allows you to use Terraform to manage TiDB Cloud resources, such as clusters, backups, and restores.

If you are looking for a simple way to automate resource provisioning and your infrastructure workflow, you can try out TiDB Cloud Terraform Provider, which provides you with the following capacities:

- Get your project information.
- Get cluster specification information, such as supported cloud providers, regions, and node sizes.
- Manage your TiDB cluster, including creating, scaling, pausing, and resuming a cluster.
- Create and delete a backup for your cluster.
- Create a restore task for your cluster.

## Requirements

- [A TiDB Cloud account](https://tidbcloud.com/free-trial)
- [Terraform version](https://www.terraform.io/downloads.html) >= 1.0
- [Go version](https://golang.org/doc/install) >= 1.18 (required only if you want to build [TiDB Cloud Terraform Provider](https://github.com/tidbcloud/terraform-provider-tidbcloud) locally)

## Supported resources and data sources

[Resources](https://www.terraform.io/language/resources) and [Data sources](https://www.terraform.io/language/data-sources) are the two most important elements in the Terraform language.

TiDB Cloud supports the following resources and data sources:

- Resources

    - `tidbcloud_cluster`
    - `tidbcloud_backup`
    - `tidbcloud_restore`
    - `tidbcloud_import`

- Data sources

    - `tidbcloud_projects`
    - `tidbcloud_cluster_specs`
    - `tidbcloud_clusters`
    - `tidbcloud_restores`
    - `tidbcloud_backups`

To get all the available configurations for the resources and data sources, see this [configuration documentation](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs).

## Next step

- [Learn more about Terraform](https://www.terraform.io/docs)
- [Get TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md)
- [Use Cluster Resource](/tidb-cloud/terraform-use-cluster-resource.md)
- [Use Backup Resource](/tidb-cloud/terraform-use-backup-resource.md)
- [Use Restore Resource](/tidb-cloud/terraform-use-restore-resource.md)