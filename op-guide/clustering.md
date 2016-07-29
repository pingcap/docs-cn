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
