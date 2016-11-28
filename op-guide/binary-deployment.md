# TiDB Binary Deployment

## Overview

A complete TiDB project contains PD, TiKV, TiDB. The start-up sequence is PD -> TiKV -> TiDB.

To learn the TiDB architecture, see [TiDB Architecture](../README.md#TiDB-Architecture).

To quickly understand and try TiDB, follow [Standalone Cluster Deployment](#standalone-cluster-deployment).

To deploy and use TiDB in production, follow [Multi Nodes Deployment](#multi-nodes-deployment).

## Download and Decompress the Official Binary Package

### Linux

Note: The Linux package does not support the CentOS 6 platform. See [CentOS 6](#centos-6) to download and decompress the CentOS 6 package.

```bash
# Download package
wget http://download.pingcap.org/tidb-latest-linux-amd64.tar.gz
wget http://download.pingcap.org/tidb-latest-linux-amd64.sha256

# Verify the integrity
sha256sum -c tidb-latest-linux-amd64.sha256

# Decompress the package
tar -xzf tidb-latest-linux-amd64.tar.gz
cd tidb-latest-linux-amd64
```

#### CentOS 6

```bash
# Download CentOS 6 package
wget http://download.pingcap.org/tidb-latest-linux-amd64-centos6.tar.gz
wget http://download.pingcap.org/tidb-latest-linux-amd64-centos6.sha256

# Verify the integrity
sha256sum -c tidb-latest-linux-amd64-centos6.sha256

# Decompress the package
tar -xzf tidb-latest-linux-amd64-centos6.tar.gz
cd tidb-latest-linux-amd64-centos6
```

## Standalone Cluster Deployment

1. Start PD.

    ```bash
    ./bin/pd-server --data-dir=pd
    ```
    
2. Start TiKV.

    ```bash
    ./bin/tikv-server --pd="127.0.0.1:2379" \
                      --store=tikv
    ```

3. Start TiDB.

    ```bash
    ./bin/tidb-server --store=tikv \
                      --path="127.0.0.1:2379" 
    ```

4. Use the official `mysql` client to connect to TiDB and enjoy it. 

    ```sh
    mysql -h 127.0.0.1 -P 4000 -u root -D test
    ```

## Multi Nodes Deployment

Assume we have three machines with the following details:

|Name|Host IP|Services|
|----|-------|--------|
|node1|192.168.199.113|PD1, TiKV1, TiDB|
|node2|192.168.199.114|PD2, TiKV2|
|node3|192.168.199.115|PD3, TiKV3|

We run PD and TiKV on every node and TiDB on node1 only.

**Note: This is just for demonstration, follow [Recommendation](./recommendation.md) to deploy the cluster in production.**

1. Start PD on every node.

    ```bash
    ./bin/pd-server --name=pd1 \
                    --data-dir=pd1 \
                    --client-urls="http://192.168.199.113:2379" \
                    --peer-urls="http://192.168.199.113:2380" \
                    --initial-cluster="pd1=http://192.168.199.113:2380,pd2=http://192.168.199.114:2380,pd3=http://192.168.199.115:2380"
              
    ./bin/pd-server --name=pd2 \
                    --data-dir=pd2 \
                    --client-urls="http://192.168.199.114:2379" \
                    --peer-urls="http://192.168.199.114:2380" \
                    --initial-cluster="pd1=http://192.168.199.113:2380,pd2=http://192.168.199.114:2380,pd3=http://192.168.199.115:2380"
              
    ./bin/pd-server --name=pd3 \
                    --data-dir=pd3 \
                    --client-urls="http://192.168.199.115:2379" \
                    --peer-urls="http://192.168.199.115:2380" \
                    --initial-cluster="pd1=http://192.168.199.113:2380,pd2=http://192.168.199.114:2380,pd3=http://192.168.199.115:2380"
    ```

2. Start TiKV on every node.

    ```bash
    ./bin/tikv-server --pd="192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379" \
                      --addr="192.168.199.113:20160" \
                      --store=tikv1
    
    ./bin/tikv-server --pd="192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379" \
                      --addr="192.168.199.114:20160" \
                      --store=tikv2
                
    ./bin/tikv-server --pd="192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379" \
                      --addr="192.168.199.115:20160" \
                      --store=tikv3
    ```

3. Start TiDB on node1.

    ```bash
    ./bin/tidb-server --store=tikv \
                      --path="192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379"
    ```

4. Use the official `mysql` client to connect to TiDB and enjoy it. 

    ```sh
    mysql -h 192.168.199.113 -P 4000 -u root -D test
    ```
    
## Add/Remove node dynamically

### PD

You can use `join` to start a new PD server and add it to an existing PD cluster. For example, we have started three PD servers:

|Name|ClientUrls|PeerUrls|
|----|----------|--------|
|pd1|http://host1:2379|http://host1:2380|
|pd2|http://host2:2379|http://host2:2380|
|pd3|http://host3:2379|http://host3:2380|

If you want to add `pd4`, you can use `join` to do it:

```bash
./bin/pd-server --name=pd4 \
                --client-urls="http://host4:2379"
                --peer-urls="http://host4:2380"
                --join="http://host1:2379"
```

### TiKV
It is very simple to add a new TiKV server (which is also called a TiKV Store) to a TiKV cluster dynamically. You can directly start a TiKV Store and PD will automatically detect it. After you start the new Store, PD will automatically balance all the TiKV Stores in the cluster. If PD finds that the new Store has no data, it will try to move some regions from other Stores to the newly added Store.

You can also ask PD to remove a Store explicitly. To remove the Store:

1. PD marks the Store as `offline`.
2. PD migrates the data from the Store to other Stores.
3. After all the data are migrated, PD marks the Store as `tombstone`.
4. The Store can be safely removed from the cluster.

You can use the following command to call the HTTP API of PD to remove a TiKV Store whose store ID is `1`:

```
curl -X DELETE http://host:port/pd/api/v1/store/1
```
You can check the state of the Store by using the following command:

```
curl http://host:port/pd/api/v1/store/1
```
+ If the result is `state = 1`, the Store is `offline`.
+ If the result is `state = 2`, the Store is `tombstone`.
+ If the result is `state = 0`, the Store is `up`.

For detailed API documents, see [PD API v1](https://cdn.rawgit.com/pingcap/docs/master/op-guide/pd-api-v1.html).

### TiDB

TiDB server is stateless, and you can add or remove a TiDB server directly. Note that if you put all TiDB servers behind a proxy like HAProxy, you must update the proxy configuration and reload it.
