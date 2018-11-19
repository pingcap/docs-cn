---
title: Data Migration Overview
summary: Learn about the Data Migration tool, the architecture, the key components and features.
category: tools
---

# Data Migration Overview

Data Migration (DM) is an integrated data synchronization task management platform that supports the full data migration and the incremental data migration from MySQL/MariaDB into TiDB. It can help to reduce the operations cost and simplify the troubleshooting process.

## Architecture

The Data Migration tool includes three components: dm-master, dm-worker, and dmctl.

![Data Migration architecture](../media/dm-architecture.png)

### dm-master

dm-master manages and schedules the operation of data synchronization tasks.

- Storing the topology information of the DM cluster
- Monitoring the running state of dm-worker processes
- Monitoring the running state of data synchronization tasks
- Providing a unified portal for the management of data synchronization tasks
- Coordinating the DDL synchronization of sharded tables in each instance under the sharding scenario

### dm-worker

dm-worker executes specific data synchronization tasks.

- Persisting the binlog data to the local storage
- Storing the configuration information of the data synchronization subtasks
- Orchestrating the operation of the data synchronization subtasks
- Monitoring the running state of the data synchronization subtasks

### dmctl 

dmctl is the command line tool used to control the DM cluster.

- Creating/Updating/Dropping data synchronization tasks
- Checking the state of data synchronization tasks
- Handling the errors during data synchronization tasks
- Verifying the configuration correctness of data synchronization tasks
