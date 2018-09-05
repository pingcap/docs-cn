---
title: TiDB Quick Start Guide
summary: Learn how to quickly start a TiDB cluster.
category: quick start
---

# TiDB Quick Start Guide

This guide introduces how to deploy and monitor a TiDB cluster on your local drive using Docker Compose for experimenting and testing.

> **Warning:** Deploying TiDB using Docker Compose can only be used for experimental purposes. For production usage, [use Ansible to deploy the TiDB cluster](op-guide/ansible-deployment.md).

## Prerequisites

Before you begin, make sure to install the following tools:

- [Git](https://git-scm.com/downloads)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [MySQL Client](https://dev.mysql.com/downloads/mysql/)

## Deploy a TiDB cluster

1. Download `tidb-docker-compose`:

    ```bash
    git clone https://github.com/pingcap/tidb-docker-compose.git
    ```

2. Change the directory to tidb-docker-compose and get the latest TiDB Docker Images:

    ```bash
    cd tidb-docker-compose && docker-compose pull
    ```

3. Start the TiDB cluster:

    ```bash
    docker-compose up -d
    ```

Congratulations! You have deployed a TiDB cluster! You can see messages in your terminal of the default components of a TiDB cluster: 

- 1 TiDB instance
- 3 TiKV instances
- 3 Placement Driver (PD) instances
- Prometheus
- Grafana
- 2 TiSpark instances (one master, one slave)
- 1 TiDB-Vision instance

You can now test your TiDB server using one of the following methods:

- Use the MySQL client to connect to TiDB:

    ```
    mysql -h 127.0.0.1 -P 4000 -u root
    ```
    
    You can [try TiDB](try-tidb.md) to explore the SQL statements.
    
- Use Grafana to view the status of the cluster via [http://localhost:3000](http://localhost:3000) with the default account name and password:  `admin` and `admin`.
- Use [TiDB-Vision](https://github.com/pingcap/tidb-vision), a cluster visualization tool, to see data transfer and load-balancing inside your cluster via [http://localhost:8010](http://localhost:8010).
