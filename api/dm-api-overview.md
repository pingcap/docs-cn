---
title: Data Migration API Overview
summary: Learn the API of Data Migration (DM) services.
---

# Data Migration API Overview

[TiDB Data Migration](/dm/dm-overview.md) (DM) is an integrated data migration task management platform that supports full data migration and incremental data replication from MySQL-compatible databases (such as MySQL, MariaDB, and Aurora MySQL) into TiDB.

DM provides an OpenAPI for querying and operating the DM cluster, similar to the [dmctl tool](/dm/dmctl-introduction.md).

You can use DM APIs to perform the following maintenance operations on the DM cluster:

- [Cluster management](/dm/dm-open-api.md#apis-for-managing-clusters): Get information about or stop DM-master and DM-worker nodes.
- [Data source management](/dm/dm-open-api.md#apis-for-managing-data-sources): Create, update, delete, enable, or disable data sources; manage relay-log features and bindings.
- [Replication task management](/dm/dm-open-api.md#apis-for-managing-replication-tasks): Create, update, delete, start, or stop replication tasks; manage schemas and migration rules.

For more information about each API, including request parameters, response examples, and usage instructions, see [Maintain DM Clusters Using OpenAPI](/dm/dm-open-api.md).
