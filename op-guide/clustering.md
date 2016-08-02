# Clustering

## Overview

A complete TiDB project contains PD, TiKV, TiDB. The start-up sequence is PD -> TiKV -> TiDB.

## A standalone cluster

1. Start PD.

    ```bash
    pd-server --cluster-id=1 \
              --data-dir=pd
    ```
    
2. Start TiKV.

    ```bash
    tikv-server -I 1 \
                -S raftkv \
                --pd 127.0.0.1:2379 \
                -s tikv
    ```

3. Start TiDB.

    ```bash
    tidb-server --store=tikv \
                --path="127.0.0.1:2379?cluster=1" 
    ```

4. Use the official `mysql` client to connect to TiDB and enjoy it. 

    ```sh
    mysql -h 127.0.0.1 -P 4000 -u root -D test
    ```

## A 3-node multi-machine cluster

Assume we have three machines with the following details:

|Name|Host IP|
|----|-------|
|node1|192.168.199.113|
|node2|192.168.199.114|
|node3|192.168.199.115|

We run PD and TiKV on every node and TiDB on node1 only.

1. Start PD on every node.

    ```bash
    pd-server --cluster-id=1 \
              --name=pd1 \
              --data-dir=pd1 \
              --addr="192.168.199.113:1234" \
              --client-urls="http://192.168.199.113:2379" \
              --peer-urls="http://192.168.199.113:2380" \
              --initial-cluster="pd1=http://192.168.199.113:2380,pd2=http://192.168.199.114:2380,pd3=http://192.168.199.115:2380"
              
    pd-server --cluster-id=1 \
              --name=pd2 \
              --data-dir=pd2 \
              --addr="192.168.199.114:1234" \
              --client-urls="http://192.168.199.114:2379" \
              --peer-urls="http://192.168.199.114:2380" \
              --initial-cluster="pd1=http://192.168.199.113:2380,pd2=http://192.168.199.114:2380,pd3=http://192.168.199.115:2380"
              
    pd-server --cluster-id=1 \
              --name=pd3 \
              --data-dir=pd3 \
              --addr="192.168.199.115:1234" \
              --client-urls="http://192.168.199.115:2379" \
              --peer-urls="http://192.168.199.115:2380" \
              --initial-cluster="pd1=http://192.168.199.113:2380,pd2=http://192.168.199.114:2380,pd3=http://192.168.199.115:2380"
    ```

2. Start TiKV on every node.

    ```bash
    tikv-server -S raftkv \
                -I 1 \
                --pd 192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379 \
                --addr 192.168.199.113:20160 \
                -s tikv1
    
    tikv-server -S raftkv \
                -I 1 \
                --pd 192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379 \
                --addr 192.168.199.114:20160 \
                -s tikv2
                
    tikv-server -S raftkv \
                -I 1 \
                --pd 192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379 \
                --addr 192.168.199.115:20160 \
                -s tikv3
    ```

3. Start TiDB on node1.

    ```bash
    tidb-server --store=tikv \
                --path="192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379?cluster=1"
    ```

4. Use the official `mysql` client to connect to TiDB and enjoy it. 

    ```sh
    mysql -h 192.168.199.113 -P 4000 -u root -D test
    ```
    
## Add/Remove node dynamically

### PD

You can use `join` to start a new PD server and add it to an existing PD cluster. . For example, we have started three PD servers within Cluster ID 1:

|Name|ClientUrls|PeerUrls|
|----|----------|--------|
|pd1|http://host1:2379|http://host1:2380|
|pd2|http://host2:2379|http://host2:2380|
|pd3|http://host3:2379|http://host3:2380|

If you want to add `pd4`, you can use `join` to do it:

```
pd-server --cluster-id=1 \
          --name=pd4 \
          --client-urls="http://host4:2379"
          --peer-urls="http://host4:2380"
          --join="http://host1:2379"
```

### TiKV

Adding a new TiKV server is very simple. After you start a new Store, PD will automatically balance all the TiKV Stores. If PD finds that the new Store has no data, it will try to move some regions from other Stores to the new Store.

You can tell PD to remove a Store explicitly. Then, PD will treat this Store as dead and rebalance the Region whose replicas are in this Store through Region heartbeats.

### TiDB

TiDB server is stateless, and you can add or remove a TiDB server directly. Note that if you put all TiDB servers behind a proxy like HAProxy, you must update the proxy configuration and reload it.