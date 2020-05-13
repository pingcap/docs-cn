---
title: Deploy and use TiCDC
summary: Learn how to deploy and use TiCDC to replicate incremental data.
category: reference
---

# Deploy and use TiCDC

This document introduces how to deploy and use TiCDC to replicate incremental data.

## Step 1: Deploy TiCDC cluster

This section describes how to deploy TiCDC in the following different scenarios:

- [Fresh deploy TiCDC using TiUP](#fresh-deploy-ticdc-using-tiup)
- [Add TiCDC component to an existing TiDB cluster using TiUP](#add-ticdc-component-to-an-existing-tidb-cluster-using-tiup)
- [Manually add TiCDC component to an existing TiDB cluster](#manually-add-ticdc-component-to-an-existing-tidb-cluster)

### Fresh deploy TiCDC using TiUP

TiUP cluster is a deployment tool for TiDB 4.0 and later versions. You must deploy and run TiCDC on TiDB v4.0.0-rc.1 or a later version.

To deploy TiCDC, take the following steps:

1. [Install TiUP](/how-to/deploy/orchestrated/tiup.md).

2. Install the TiUP cluster component:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster
    ```

3. Edit the topology configuration file, and save it as `topology.yaml`:

    Refer to the [full configuration file template](https://github.com/pingcap-incubator/tiup-cluster/blob/master/examples/topology.example.yaml).

    In addition to configuring the TiDB cluster deployment, you also need to configure the CDC server IP under the `cdc_servers` section. Currently the configuration only supports IP, not domain name.

    {{< copyable "" >}}

    ```ini
    pd_servers:
      - host: 172.19.0.101
      - host: 172.19.0.102
      - host: 172.19.0.103
    
    tidb_servers:
      - host: 172.19.0.101
    
    tikv_servers:
      - host: 172.19.0.101
      - host: 172.19.0.102
      - host: 172.19.0.103
    
    cdc_servers:
      - host: 172.19.0.101
      - host: 172.19.0.102
      - host: 172.19.0.103
    ```

4. Finish the following steps according to the TiUP deployment process:

    Deploy the TiDB cluster. `test` is the cluster name:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster deploy test v4.0.0-rc.1 topology.yaml -i ~/.ssh/id_rsa
    ```
    
    Start the TiDB cluster:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster start test
    ```

5. View the cluster status:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster display test
    ```

### Add TiCDC component to an existing TiDB cluster using TiUP

1. Check if your TiDB version supports TiCDC. If not, upgrade the TiDB cluster to 4.0.0 rc.1 or later versions.

2. Refer to [Scale out a TiDB/TiKV/PD/TiCDC node](/how-to/scale/with-tiup.md#scale-out-a-tidbtikvpdticdc-node) and deploy TiCDC.

    This is an example of the scale-out configuration file:

    ```shell
   vi scale-out.yaml
   ```

   ```
   cdc_servers:
    - host: 10.0.1.5
    - host: 10.0.1.6
    - host: 10.0.1.7
   ```

   Run the scale-out command:

   {{< copyable "shell-regular" >}}

   ```shell
   tiup cluster scale-out <cluster-name> scale-out.yaml
   ```

### Manually add TiCDC component to an existing TiDB cluster

Suppose that there is a PD node (the client URL is `10.0.10.25:2379`) in the PD cluster that can provide services. If you want to deploy three TiCDC nodes, start the TiCDC cluster using the following commands. You only need to specify the same PD address, and the newly started TiCDC nodes will automatically be added to the TiCDC cluster.

{{< copyable "shell-regular" >}}

```shell
cdc server --pd=http://10.0.10.25:2379 --log-file=ticdc_1.log --addr 0.0.0.0:8301 --advertise-addr=127.0.0.1:8301
cdc server --pd=http://10.0.10.25:2379 --log-file=ticdc_2.log --addr 0.0.0.0:8302 --advertise-addr=127.0.0.1:8302
cdc server --pd=http://10.0.10.25:2379 --log-file=ticdc_3.log --addr 0.0.0.0:8303 --advertise-addr=127.0.0.1:8303
```

## Step 2: Create replication task

To replicate all upstream database schemas and tables (except system tables) to the downstream MySQL, use the following command to create a replication task:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --pd=http://10.0.10.25:2379 --start-ts=415238226621235200 --sink-uri="mysql://root:123456@127.0.0.1:3306/"
```

The parameters in the above command are described as follows:

- `pd`: The URL of the PD client.
- `start-ts`: Specifies the starting TSO of the replication task. If this parameter is not specified or specified as `0`, the current TSO is used as the starting TSO of the replication task.
- `sink-uri`: The sink address. Currently, the address can be configured to `mysql`, `tidb`, or `kafka`. For how to configure sink URI, refer to [Configure Sink URI](/reference/tools/ticdc/sink.md).
- `config`: The configuration of the replication task. Currently, this configuration supports the black & white lists and skipping specific transaction of certain `commit-ts`.

After executing the above command, TiCDC starts to replicate data to the downstream MySQL (`127.0.0.1:3306`) from the specified `start-ts` (`415238226621235200`).

If you want to replicate data to a Kafka cluster, first create the topic in the Kafka cluster (for example, `cdc-test` in the following example is a topic), create partitions, and use the following command to create a replication task:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --pd=http://10.0.10.25:2379 --start-ts=415238226621235200 --sink-uri="kafka://10.0.10.30:9092/cdc-test"
```

After executing the above command, TiCDC starts to replicate data to the downstream Kafka (`10.0.10.30:9092`) from the specified `start-ts`.
