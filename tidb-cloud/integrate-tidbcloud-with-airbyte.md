---
title: Integrate TiDB Cloud with Airbyte
summary: Learn how to use Airbyte TiDB connector.
---

# Integrate TiDB Cloud with Airbyte

[Airbyte](https://airbyte.com/) is an open-source data integration engine to build Extract, Load, Transform (ELT) pipelines and consolidate your data in your data warehouses, data lakes, and databases. This document describes how to connect Airbyte to TiDB Cloud as a source or a destination.

## Deploy Airbyte

You can deploy Airbyte locally with only a few steps.

1. Install [Docker](https://www.docker.com/products/docker-desktop) on your workspace.

2. Clone the Airbyte source code.

    ```shell
    git clone https://github.com/airbytehq/airbyte.git && \
    cd airbyte
    ```

3. Run the Docker images by docker-compose.

    ```shell
    docker-compose up
    ```

Once you see an Airbyte banner, you can go to [http://localhost:8000](http://localhost:8000) with the username (`airbyte`) and password (`password`) to visit the UI.

```
airbyte-server      |     ___    _      __          __
airbyte-server      |    /   |  (_)____/ /_  __  __/ /____
airbyte-server      |   / /| | / / ___/ __ \/ / / / __/ _ \
airbyte-server      |  / ___ |/ / /  / /_/ / /_/ / /_/  __/
airbyte-server      | /_/  |_/_/_/  /_.___/\__, /\__/\___/
airbyte-server      |                     /____/
airbyte-server      | --------------------------------------
airbyte-server      |  Now ready at http://localhost:8000/
airbyte-server      | --------------------------------------
```

## Set up the TiDB connector

Conveniently, the steps are the same for setting TiDB as the source and the destination.

1. Click **Sources** or **Destinations** in the sidebar and choose TiDB type to create a new TiDB connector.

2. Fill in the following parameters.

    - Host: The endpoint of your TiDB Cloud cluster
    - Port: The port of the database
    - Database: The database that you want to sync the data
    - Username: The username to access the database
    - Password: The password of the username

    You can get the parameter values from the connection dialog of your cluster. To open the dialog, go to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project, click the name of your target cluster to go to its overview page, and then click **Connect** in the upper-right corner.

3. Enable **SSL Connection**, and set TLS protocols to **TLSv1.2** or **TLSv1.3** in **JDBC URL Params**.

    > Note:
    >
    > - TiDB Cloud supports TLS connection. You can choose your TLS protocols in **TLSv1.2** and **TLSv1.3**, for example, `enabledTLSProtocols=TLSv1.2`.
    > - If you want to disable TLS connection to TiDB Cloud via JDBC, you need to set useSSL to `false` in JDBC URL Params specifically and close SSL connection, for example, `useSSL=false`.
    > - TiDB Serverless only supports TLS connections.

4. Click **Set up source** or **destination** to complete creating the connector. The following screenshot shows the configuration of TiDB as the source.

![TiDB source configuration](/media/tidb-cloud/integration-airbyte-parameters.jpg)

You can use any combination of sources and destinations, such as TiDB to Snowflake, and CSV files to TiDB.

For more details about the TiDB connector, see [TiDB Source](https://docs.airbyte.com/integrations/sources/tidb) and [TiDB Destination](https://docs.airbyte.com/integrations/destinations/tidb).

## Set up the connection

After setting up the source and destination, you can build and configure the connection.

The following steps use TiDB as both a source and a destination. Other connectors may have different parameters.

1. Click **Connections** in the sidebar and then click **New Connection**.
2. Select the previously established source and destination.
3. Go to the **Set up** connection panel and create a name for the connection, such as `${source_name} - ${destination-name}`.
4. Set **Replication frequency** to **Every 24 hours**, which means the connection replicates data once a day.
5. Set **Destination Namespace** to **Custom format** and set **Namespace Custom Format** to **test** to store all data in the `test` database.
6. Choose the **Sync mode** to **Full refresh | Overwrite**.

    > **Tip:**
    >
    > The TiDB connector supports both Incremental and Full Refresh syncs.
    >
    > - In Incremental mode, Airbyte only reads records added to the source since the last sync job. The first sync using Incremental mode is equivalent to Full Refresh mode.
    > - In Full Refresh mode, Airbyte reads all records in the source and replicates to the destination in every sync task. You can set the sync mode for every table named **Namespace** in Airbyte individually.

    ![Set up connection](/media/tidb-cloud/integration-airbyte-connection.jpg)

7. Set **Normalization & Transformation** to **Normalized tabular data** to use the default normalization mode, or you can set the dbt file for your job. For more information about normalization, refer to [Transformations and Normalization](https://docs.airbyte.com/operator-guides/transformation-and-normalization/transformations-with-dbt).
8. Click **Set up connection**.
9. Once the connection is established, click **ENABLED** to activate the synchronization task. You can also click **Sync now** to sync immediately.

![Sync data](/media/tidb-cloud/integration-airbyte-sync.jpg)

## Limitations

- The TiDB connector does not support the Change Data Capture (CDC) feature.
- TiDB destination converts the `timestamp` type to the `varchar` type in default normalization mode. It happens because Airbyte converts the timestamp type to string during transmission, and TiDB does not support `cast ('2020-07-28 14:50:15+1:00' as timestamp)`.
- For some large ELT missions, you need to increase the parameters of [transaction restrictions](/develop/dev-guide-transaction-restraints.md#large-transaction-restrictions) in TiDB.

## See also

[Using Airbyte to Migrate Data from TiDB Cloud to Snowflake](https://www.pingcap.com/blog/using-airbyte-to-migrate-data-from-tidb-cloud-to-snowflake/).
