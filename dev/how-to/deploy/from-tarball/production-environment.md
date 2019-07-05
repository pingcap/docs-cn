---
title: Production Deployment from Binary Tarball
summary: Use the binary to deploy a TiDB cluster.
category: how-to
---

# Production Deployment from Binary Tarball

This guide provides installation instructions from a binary tarball on Linux. A complete TiDB cluster contains PD, TiKV, and TiDB. To start the database service, follow the order of PD -> TiKV -> TiDB. To stop the database service, follow the order of stopping TiDB -> TiKV -> PD.

See also [local deployment](/how-to/get-started/deploy-tidb-from-binary.md) and [testing environment](/how-to/deploy/from-tarball/testing-environment.md) deployment.

## Prepare

Before you start, see [TiDB architecture](/architecture.md) and [Software and Hardware Recommendations](/how-to/deploy/hardware-recommendations.md). Make sure the following requirements are satisfied:

### Operating system

For the operating system, it is recommended to use RHEL/CentOS 7.3 or higher. The following additional requirements are recommended:

| Configuration | Description |
| :-- | :-------------------- |
| Supported Platform | RHEL/CentOS 7.3+ ([more details](/how-to/deploy/hardware-recommendations.md)) |
| File System  |  ext4 is recommended |
| Swap Space  |  Should be disabled  |
| Disk Block Size  |  Set the system disk `Block` size to `4096` |

### Network and firewall

| Configuration | Description |
| :-- | :------------------- |
| Firewall/Port | Check whether the ports required by TiDB are accessible between the nodes |

### Operating system parameters

| Configuration | Description |
| :-- | :-------------------------- |
| Nice Limits | For system users, set the default value of `nice` in TiDB to `0` |
| min_free_kbytes | The setting for `vm.min_free_kbytes` in `sysctl.conf` needs to be high enough |
| User Open Files Limit | For database administrators, set the number of TiDB open files to `1000000` |
| System Open File Limits | Set the number of system open files to `1000000` |
| User Process Limits | For TiDB users, set the `nproc` value to `4096` in `limits.conf` |
| Address Space Limits | For TiDB users, set the space to `unlimited` in `limits.conf` |
| File Size Limits | For TiDB users, set the `fsize` value to `unlimited` in `limits.conf` |
| Disk Readahead | Set the value of the `readahead` data disk to `4096` at a minimum |
| NTP service | Configure the NTP time synchronization service for each node |
| SELinux  | Turn off the SELinux service for each node |
| CPU Frequency Scaling | It is recommended to turn on CPU overclocking |
| Transparent Hugepages | For Red Hat 7+ and CentOS 7+ systems, it is required to set the Transparent Hugepages to `always` |
| I/O Scheduler | Set the I/O Scheduler of data disks to the `deadline` mode |
| vm.swappiness | Set `vm.swappiness = 0` in `sysctl.conf` |
| net.core.somaxconn | Set `net.core.somaxconn = 32768` in `sysctl.conf` |
| net.ipv4.tcp_syncookies | Set `net.ipv4.tcp_syncookies = 0` in `sysctl.conf` |

### Database running user settings

| Configuration | Description |
| :-- | :---------------------------- |
| LANG environment | Set `LANG = en_US.UTF8` |
| TZ time zone | Set the TZ time zone of all nodes to the same value |

## TiDB components and default ports

Before you deploy a TiDB cluster, see the [required components](#tidb-database-components-required) and [optional components](#tidb-database-components-optional).

### TiDB database components (required)

See the following table for the default ports for the TiDB components:

| Component | Default Port | Protocol | Description |
| :-- | :-- | :-- | :----------- |
| ssh | 22 | TCP | the sshd service |
| TiDB|  4000  | TCP | the communication port for the application and DBA tools |
| TiDB| 10080  |  TCP | the communication port to report TiDB status |
| TiKV|  20160 |  TCP | the TiKV communication port  |
| PD | 2379 | TCP | the communication port between TiDB and PD |
| PD | 2380 | TCP | the inter-node communication port within the PD cluster |

### TiDB database components (optional)

See the following table for the default ports for the optional TiDB components:

| Component | Default Port | Protocol | Description |
| :-- | :-- | :-- | :------------------------ |
| Prometheus |  9090| TCP | the communication port for the Prometheus service |
| Pushgateway |  9091 | TCP | the aggregation and report port for TiDB, TiKV, and PD monitor |
| Node_exporter|  9100| TCP | the communication port to report the system information of every TiDB cluster node |
| Grafana | 3000 | TCP | the port for the external Web monitoring service and client (Browser) access |
| alertmanager | 9093 | TCP | the port for the alert service |

## Create a database running user account

1. Log in to the machine using the `root` user account and create a database running user account (`tidb`) using the following command:

    ```bash
    # useradd tidb -m
    ```

2. Switch the user from `root` to `tidb` by using the following command. You can use this `tidb` user account to deploy your TiDB cluster.

    ```bash
    # su - tidb
    ```

## Download the official binary package

```
# Download the package.
$ wget http://download.pingcap.org/tidb-latest-linux-amd64.tar.gz
$ wget http://download.pingcap.org/tidb-latest-linux-amd64.sha256

# Check the file integrity. If the result is OK, the file is correct.
$ sha256sum -c tidb-latest-linux-amd64.sha256

# Extract the package.
$ tar -xzf tidb-latest-linux-amd64.tar.gz
$ cd tidb-latest-linux-amd64
```

## Multiple nodes cluster deployment

For the production environment, multiple nodes cluster deployment is recommended. Before you begin, see [Software and Hardware Recommendations](/how-to/deploy/hardware-recommendations.md).

Assuming that you have six nodes, you can deploy 3 PD instances, 3 TiKV instances, and 1 TiDB instance. See the following table for details:

| Name  | Host IP | Services |
| :-- | :-- | :-------------- |
| Node1 | 192.168.199.113| PD1, TiDB |
| Node2 | 192.168.199.114| PD2 |
| Node3 | 192.168.199.115| PD3 |
| Node4 | 192.168.199.116| TiKV1 |
| Node5 | 192.168.199.117| TiKV2 |
| Node6 | 192.168.199.118| TiKV3 |

Follow the steps below to start PD, TiKV, and TiDB:

1. Start PD on Node1, Node2, and Node3 in sequence.

    ```bash
    $ ./bin/pd-server --name=pd1 \
                    --data-dir=pd \
                    --client-urls="http://192.168.199.113:2379" \
                    --peer-urls="http://192.168.199.113:2380" \
                    --initial-cluster="pd1=http://192.168.199.113:2380,pd2=http://192.168.199.114:2380,pd3=http://192.168.199.115:2380" \
                    -L "info" \
                    --log-file=pd.log &

    $ ./bin/pd-server --name=pd2 \
                    --data-dir=pd \
                    --client-urls="http://192.168.199.114:2379" \
                    --peer-urls="http://192.168.199.114:2380" \
                    --initial-cluster="pd1=http://192.168.199.113:2380,pd2=http://192.168.199.114:2380,pd3=http://192.168.199.115:2380" \
                    -L "info" \
                    --log-file=pd.log &

    $ ./bin/pd-server --name=pd3 \
                    --data-dir=pd \
                    --client-urls="http://192.168.199.115:2379" \
                    --peer-urls="http://192.168.199.115:2380" \
                    --initial-cluster="pd1=http://192.168.199.113:2380,pd2=http://192.168.199.114:2380,pd3=http://192.168.199.115:2380" \
                    -L "info" \
                    --log-file=pd.log &
    ```

2. Start TiKV on Node4, Node5 and Node6.

    ```bash
    $ ./bin/tikv-server --pd="192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379" \
                      --addr="192.168.199.116:20160" \
                      --status-addr="192.168.199.116:20180" \
                      --data-dir=tikv \
                      --log-file=tikv.log &

    $ ./bin/tikv-server --pd="192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379" \
                      --addr="192.168.199.117:20160" \
                      --status-addr="192.168.199.117:20180" \
                      --data-dir=tikv \
                      --log-file=tikv.log &

    $ ./bin/tikv-server --pd="192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379" \
                      --addr="192.168.199.118:20160" \
                      --status-addr="192.168.199.118:20180" \
                      --data-dir=tikv \
                      --log-file=tikv.log &
    ```

3. Start TiDB on Node1.

    ```bash
    $ ./bin/tidb-server --store=tikv \
                      --path="192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379" \
                      --log-file=tidb.log &
    ```

4. Use the MySQL client to connect to TiDB.

    ```sh
    $ mysql -h 192.168.199.113 -P 4000 -u root -D test
    ```

> **Note:**
>
> - If you start TiKV or deploy PD in the production environment, it is highly recommended to specify the path for the configuration file using the `--config` parameter. If the parameter is not set, TiKV or PD does not read the configuration file.
> - To tune TiKV, see [Performance Tuning for TiKV](/reference/performance/tune-tikv.md).
> - If you use `nohup` to start the cluster in the production environment, write the startup commands in a script and then run the script. If not, the `nohup` process might abort because it receives exceptions when the Shell command exits. For more information, see [The TiDB/TiKV/PD process aborts unexpectedly](/how-to/troubleshoot/cluster-setup.md#the-tidbtikvpd-process-aborts-unexpectedly).

For the deployment and use of TiDB monitoring services, see [Monitor a TiDB Cluster](/how-to/monitor/monitor-a-cluster.md).
