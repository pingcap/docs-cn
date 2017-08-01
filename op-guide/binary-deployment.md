---
title: TiDB Binary Deployment
category: deployment
---

# TiDB Binary Deployment

## Overview

A complete TiDB project contains PD, TiKV, TiDB. The start-up sequence is PD -> TiKV -> TiDB.

Before your start, see [TiDB Architecture](../README.md#TiDB-Architecture) and [Deployment Recommendations](op-guide/recommendation.md).

To quickly understand and try TiDB, see [Single Node Cluster Deployment](#single-node-deployment).

To try TiDB out and explore the features, see [Multiple Nodes Cluster Deployment for Test](#multiple-nodes-cluster-deployment-for-test).

To deploy and use TiDB in production, see [Multiple Nodes Cluster Deployment](#multiple-nodes-cluster-deployment).

## Download and Decompress the Official Binary Package

### Linux (CentOS 7+, Ubuntu 14.04+)

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

### CentOS 6 (Not Recommended)

**Warning:** It is not recommended to deploy on CentOS 6 because most of the developments and tests are performed on the CentOS 7+ and Ubuntu 14.04+ platforms. There might not be enough tests on the CentOS 6 platform.

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

## Single Node Cluster Deployment

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

## Multiple Nodes Cluster Deployment

For production environment, multiple nodes cluster deployment is recommended. Before you begin, see [Deployment Recommendations](op-guide/recommendation.md).

Assuming you have six nodes with the following details:

|Name|Host IP|Services|
|----|-------|--------|
|Node1|192.168.199.113|PD1, TiDB|
|Node2|192.168.199.114|PD2|
|Node3|192.168.199.115|PD3|
|Node4|192.168.199.116|TiKV1|
|Node5|192.168.199.117|TiKV2|
|Node6|192.168.199.118|TiKV3|

1. Start PD on Node1, Node2 and Node3 in sequence.

    ```bash
    ./bin/pd-server --name=pd1 \
                    --data-dir=pd1 \
                    --client-urls="http://192.168.199.113:2379" \
                    --peer-urls="http://192.168.199.113:2380" \
                    --initial-cluster="pd1=http://192.168.199.113:2380" \
                    --log-file=pd.log

    ./bin/pd-server --name=pd2 \
                    --data-dir=pd2 \
                    --client-urls="http://192.168.199.114:2379" \
                    --peer-urls="http://192.168.199.114:2380" \
                    --join="http://192.168.199.113:2379" \
                    --log-file=pd.log

    ./bin/pd-server --name=pd3 \
                    --data-dir=pd3 \
                    --client-urls="http://192.168.199.115:2379" \
                    --peer-urls="http://192.168.199.115:2380" \
                    --join="http://192.168.199.113:2379" \
                    --log-file=pd.log
    ```

2. Start TiKV on Node4, Node5 and Node6.

    ```bash
    ./bin/tikv-server --pd="192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379" \
                      --addr="192.168.199.116:20160" \
                      --store=tikv1
    
    ./bin/tikv-server --pd="192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379" \
                      --addr="192.168.199.117:20160" \
                      --store=tikv2
                
    ./bin/tikv-server --pd="192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379" \
                      --addr="192.168.199.118:20160" \
                      --store=tikv3
    ```

3. Start TiDB on Node1.

    ```bash
    ./bin/tidb-server --store=tikv \
                      --path="192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379"
    ```

4. Use the official `mysql` client to connect to TiDB and enjoy it. 

    ```sh
    mysql -h 192.168.199.113 -P 4000 -u root -D test
    ```

**Note:** 
- If you start TiKV or deploy PD in the production environment, it is highly recommended to specify the path for the configuration file using the `--config` flag. If the flag is not set, TiKV or PD does not read the configuration file.
- If you use `nohup` to start the cluster in the production environment, write the startup commands in a script and then run the script. If not, the `nohup` process might abort because it receives exceptions when the Shell command exits. For more information, see [the TiDB/TiKV/PD process aborts unexpectedly](/./trouble-shooting.md#the-tidbtikvpd-process-aborts-unexpectedly).

## Multiple Nodes Cluster Deployment for Test

If you want to test TiDB and you have limited number of nodes, you can use one PD instance to test the entire cluster.

Assuming you have four nodes. You can deploy 1 PD instance, 3 TiKV instances, and 1 TiDB instance. See the following table for the details:

|Name|Host IP|Services|
|----|-------|--------|
|Node1|192.168.199.113|PD1, TiDB|
|Node2|192.168.199.114|TiKV1|
|Node3|192.168.199.115|TiKV2|
|Node4|192.168.199.116|TiKV3|

Start PD, TiKV and TiDB according to the following procedure:

1. Start PD on Node1.

    ```bash
    ./bin/pd-server --name=pd1 \
                    --data-dir=pd1 \
                    --client-urls="http://192.168.199.113:2379" \
                    --peer-urls="http://192.168.199.113:2380" \
                    --initial-cluster="pd1=http://192.168.199.113:2380"
    ```

2. Start TiKV on Node2, Node3 and Node4.

    ```bash
    ./bin/tikv-server --pd="192.168.199.113:2379" \
                      --addr="192.168.199.114:20160" \
                      --store=tikv1
    
    ./bin/tikv-server --pd="192.168.199.113:2379" \
                      --addr="192.168.199.115:20160" \
                      --store=tikv2
                
    ./bin/tikv-server --pd="192.168.199.113:2379" \
                      --addr="192.168.199.116:20160" \
                      --store=tikv3
    ```

3. Start TiDB on Node1.

    ```bash
    ./bin/tidb-server --store=tikv \
                      --path="192.168.199.113:2379"
    ```

4. Use the official `mysql` client to connect to TiDB and enjoy it. 

    ```sh
    mysql -h 192.168.199.113 -P 4000 -u root -D test
    ```
