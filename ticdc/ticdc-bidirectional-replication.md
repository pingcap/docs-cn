---
title: Bidirectional Replication
summary: Learn how to use bidirectional replication of TiCDC.
---

# Bidirectional Replication

TiCDC supports bi-directional replication (BDR) among two TiDB clusters. Based on this feature, you can create a multi-active TiDB solution using TiCDC.

This section describes how to use bi-directional replication taking two TiDB clusters as an example.

## Deploy bi-directional replication

TiCDC only replicates incremental data changes that occur after a specified timestamp to the downstream cluster. Before starting the bi-directional replication, you need to take the following steps:

1. (Optional) According to your needs, import the data of the two TiDB clusters into each other using the data export tool [Dumpling](/dumpling-overview.md) and data import tool [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md).

2. Deploy two TiCDC clusters between the two TiDB clusters. The cluster topology is as follows. The arrows in the diagram indicate the directions of data flow.

    ![TiCDC bidirectional replication](/media/ticdc/ticdc-bidirectional-replication.png)

3. Specify the starting time point of data replication for the upstream and downstream clusters.

    1. Check the time point of the upstream and downstream clusters. In the case of two TiDB clusters, make sure that data in the two clusters are consistent at certain time points. For example, the data of TiDB A at `ts=1` and the data of TiDB B at `ts=2` are consistent.

    2. When you create the changefeed, set the `--start-ts` of the changefeed for the upstream cluster to the corresponding `tso`. That is, if the upstream cluster is TiDB A, set `--start-ts=1`; if the upstream cluster is TiDB B, set `--start-ts=2`.

4. In the configuration file specified by the `--config` parameter, add the following configuration:

    ```toml
    # Whether to enable the bi-directional replication mode
    bdr-mode = true
    ```

After the configuration takes effect, the clusters can perform bi-directional replication.

## DDL types

Starting from v7.6.0, to support DDL replication as much as possible in bi-directional replication, TiDB divides the [DDLs that TiCDC originally supports](/ticdc/ticdc-ddl.md) into two types: replicable DDLs and non-replicable DDLs, according to the impact of DDLs on the business.

### Replicable DDLs

Replicable DDLs are the DDLs that can be directly executed and replicated to other TiDB clusters in bi-directional replication.

Replicable DDLs include:

- `CREATE DATABASE`
- `CREATE TABLE`
- `ADD COLUMN`: the column can be `null`, or has `not null` and `default value` at the same time
- `ADD NON-UNIQUE INDEX`
- `DROP INDEX`
- `MODIFY COLUMN`: you can only modify the `default value` and `comment` of the column
- `ALTER COLUMN DEFAULT VALUE`
- `MODIFY TABLE COMMENT`
- `RENAME INDEX`
- `ADD TABLE PARTITION`
- `DROP PRIMARY KEY`
- `ALTER TABLE INDEX VISIBILITY`
- `ALTER TABLE TTL`
- `ALTER TABLE REMOVE TTL`
- `CREATE VIEW`
- `DROP VIEW`

### Non-replicable DDLs

Non-replicable DDLs are the DDLs that have a great impact on the business, and might cause data inconsistency between clusters. Non-replicable DDLs cannot be directly replicated to other TiDB clusters in bi-directional replication through TiCDC. Non-replicable DDLs must be executed through specific operations.

Non-replicable DDLs include:

- `DROP DATABASE`
- `DROP TABLE`
- `ADD COLUMN`: the column is `not null` and does not have a `default value`
- `DROP COLUMN`
- `ADD UNIQUE INDEX`
- `TRUNCATE TABLE`
- `MODIFY COLUMN`: you can modify the attributes of the column except `default value` and `comment`
- `RENAME TABLE`
- `DROP PARTITION`
- `TRUNCATE PARTITION`
- `ALTER TABLE CHARACTER SET`
- `ALTER DATABASE CHARACTER SET`
- `RECOVER TABLE`
- `ADD PRIMARY KEY`
- `REBASE AUTO ID`
- `EXCHANGE PARTITION`
- `REORGANIZE PARTITION`

## DDL replication

To solve the problem of replicable DDLs and non-replicable DDLs, TiDB introduces the following BDR roles:

- `PRIMARY`: you can execute replicable DDLs, but cannot execute non-replicable DDLs. Replicable DDLs will be replicated to the downstream by TiCDC.
- `SECONDARY`: you cannot execute replicable DDLs or non-replicable DDLs, but can execute the DDLs replicated by TiCDC.

When no BDR role is set, you can execute any DDL. But after you set `bdr_mode=true` on TiCDC, the executed DDL will not be replicated by TiCDC.

> **Warning:**
>
> This feature is experimental. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

### Replication scenarios of replicable DDLs

1. Choose a TiDB cluster and execute `ADMIN SET BDR ROLE PRIMARY` to set it as the primary cluster.
2. On other TiDB clusters, execute `ADMIN SET BDR ROLE SECONDARY` to set them as the secondary clusters.
3. Execute **replicable DDLs** on the primary cluster. The successfully executed DDLs will be replicated to the secondary clusters by TiCDC.

> **Note:**
>
> To prevent misuse:
>
> - If you try to execute **non-replicable DDLs** on the primary cluster, you will get the [Error 8263](/error-codes.md).
> - If you try to execute **replicable DDLs** or **non-replicable DDLs** on the secondary clusters, you will get the [Error 8263](/error-codes.md).

### Replication scenarios of non-replicable DDLs

1. Execute `ADMIN UNSET BDR ROLE` on all TiDB clusters to unset the BDR role.
2. Stop writing data to the tables that need to execute DDLs in all clusters.
3. Wait until all writes to the corresponding tables in all clusters are replicated to other clusters, and then manually execute all DDLs on each TiDB cluster.
4. Wait until the DDLs are completed, and then resume writing data.
5. Follow the steps in [Replication scenarios of replicable DDLs](#replication-scenarios-of-replicable-ddls) to switch back to the replication scenario of replicable DDLs.

> **Warning:**
>
> After you execute `ADMIN UNSET BDR ROLE` on all TiDB clusters, none of the DDLs are replicated by TiCDC. You need to manually execute the DDLs on each cluster separately.

## Stop bi-directional replication

After the application has stopped writing data, you can insert a special record into each cluster. By checking the two special records, you can make sure that data in two clusters are consistent.

After the check is completed, you can stop the changefeed to stop bi-directional replication, and execute `ADMIN UNSET BDR ROLE` on all TiDB clusters.

## Limitations

- Use BDR role only in the following scenarios:

    - 1 `PRIMARY` cluster and n `SECONDARY` clusters (replication scenarios of replicable DDLs)
    - n clusters that have no BDR roles (replication scenarios in which you can manually execute non-replicable DDLs on each cluster)

    > **Note:**
    >
    > Do not set the BDR role in other scenarios, for example, setting `PRIMARY`, `SECONDARY`, and no BDR roles at the same time. If you set the BDR role incorrectly, TiDB cannot guarantee data correctness and consistency during data replication.

- Usually do not use `AUTO_INCREMENT` or `AUTO_RANDOM` to avoid data conflicts in the replicated tables. If you need to use `AUTO_INCREMENT` or `AUTO_RANDOM`, you can set different `auto_increment_increment` and `auto_increment_offset` for different clusters to ensure that different clusters can be assigned different primary keys. For example, if there are three TiDB clusters (A, B, and C) in bi-directional replication, you can set them as follows:

    - In Cluster A, set `auto_increment_increment=3` and `auto_increment_offset=2000`
    - In Cluster B, set `auto_increment_increment=3` and `auto_increment_offset=2001`
    - In Cluster C, set `auto_increment_increment=3` and `auto_increment_offset=2002`

    This way, A, B, and C will not conflict with each other in the implicitly assigned `AUTO_INCREMENT` ID and `AUTO_RANDOM` ID. If you need to add a cluster in BDR mode, you need to temporarily stop writing data of the related application, set the appropriate values for `auto_increment_increment` and `auto_increment_offset` on all clusters, and then resume writing data of the related application.

- Bi-directional replication clusters cannot detect write conflicts, which might cause undefined behaviors. Therefore, you must ensure that there are no write conflicts from the application side.

- Bi-directional replication supports more than two clusters, but does not support multiple clusters in cascading mode, that is, a cyclic replication like TiDB A -> TiDB B -> TiDB C -> TiDB A. In such a topology, if one cluster fails, the whole data replication will be affected. Therefore, to enable bi-directional replication among multiple clusters, you need to connect each cluster with every other clusters, for example, `TiDB A <-> TiDB B`, `TiDB B <-> TiDB C`, `TiDB C <-> TiDB A`.
