---
title: Data Migration Configuration File Overview
summary: This document gives an overview of Data Migration configuration files.
aliases: ['/docs/tidb-data-migration/dev/config-overview/']
---

# Data Migration Configuration File Overview

This document gives an overview of configuration files of DM (Data Migration).

## DM process configuration files

- `dm-master.toml`: The configuration file of running the DM-master process, including the topology information and the logs of the DM-master. For more details, refer to [DM-master Configuration File](/dm/dm-master-configuration-file.md).
- `dm-worker.toml`: The configuration file of running the DM-worker process, including the topology information and the logs of the DM-worker. For more details, refer to [DM-worker Configuration File](/dm/dm-worker-configuration-file.md).
- `source.yaml`: The configuration of the upstream database such as MySQL and MariaDB. For more details, refer to [Upstream Database Configuration File](/dm/dm-source-configuration-file.md).

## DM migration task configuration

### Data migration task creation

You can take the following steps to create a data migration task:

1. [Load the data source configuration into the DM cluster using dmctl](/dm/dm-manage-source.md#operate-data-source).
2. Refer to the description in the [Task Configuration Guide](/dm/dm-task-configuration-guide.md) and create the configuration file `your_task.yaml`.
3. [Create the data migration task using dmctl](/dm/dm-create-task.md).

### Important concepts

This section shows description of some important concepts.

| Concept  | Description  | Configuration File  |
| :------ | :--------- | :------------- |
| `source-id`  | Uniquely represents a MySQL or MariaDB instance, or a migration group with the primary-secondary structure. The maximum length of `source-id` is 32. | `source_id` of `source.yaml`;<br/> `source-id` of `task.yaml` |
| DM-master ID | Uniquely represents a DM-master (by the `master-addr` parameter of `dm-master.toml`) | `master-addr` of `dm-master.toml` |
| DM-worker ID | Uniquely represents a DM-worker (by the `worker-addr` parameter of `dm-worker.toml`) | `worker-addr` of `dm-worker.toml` |
