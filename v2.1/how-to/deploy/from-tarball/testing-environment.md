---
title: Testing Deployment from Binary Tarball
summary: Use the binary to deploy a TiDB cluster.
category: how-to
---

# Testing Deployment from Binary Tarball

This guide provides installation instructions for all TiDB components across multiple nodes for testing purposes. It does not match the recommended usage for production systems.

See also [local deployment](/v2.1/how-to/get-started/deploy-tidb-from-binary.md) and [production environment](/v2.1/how-to/deploy/from-tarball/production-environment.md) deployment.

## Prepare

Before you start, see [TiDB architecture](/v2.1/architecture.md) and [Software and Hardware Recommendations](/v2.1/how-to/deploy/hardware-recommendations.md). Make sure the following requirements are satisfied:

### Operating system

For the operating system, it is recommended to use RHEL/CentOS 7.3 or higher. The following additional requirements are recommended:

| Configuration | Description |
| :-- | :-------------------- |
| Supported Platform | RHEL/CentOS 7.3+ ([more details](/v2.1/how-to/deploy/hardware-recommendations.md)) |
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

## Multiple nodes cluster deployment for test

If you want to test TiDB but have a limited number of nodes, you can use one PD instance to test the entire cluster.

Assuming that you have four nodes, you can deploy 1 PD instance, 3 TiKV instances, and 1 TiDB instance. See the following table for details:

| Name | Host IP | Services |
| :-- | :-- | :------------------- |
| Node1 | 192.168.199.113 | PD1, TiDB |
| Node2 | 192.168.199.114 | TiKV1 |
| Node3 | 192.168.199.115 | TiKV2 |
| Node4 | 192.168.199.116 | TiKV3 |

Follow the steps below to start PD, TiKV and TiDB:

1. Start PD on Node1.

    ```bash
    $ ./bin/pd-server --name=pd1 \
                    --data-dir=pd \
                    --client-urls="http://192.168.199.113:2379" \
                    --peer-urls="http://192.168.199.113:2380" \
                    --initial-cluster="pd1=http://192.168.199.113:2380" \
                    --log-file=pd.log &
    ```

2. Start TiKV on Node2, Node3 and Node4.

    ```bash
    $ ./bin/tikv-server --pd="192.168.199.113:2379" \
                      --addr="192.168.199.114:20160" \
                      --data-dir=tikv \
                      --log-file=tikv.log &

    $ ./bin/tikv-server --pd="192.168.199.113:2379" \
                      --addr="192.168.199.115:20160" \
                      --data-dir=tikv \
                      --log-file=tikv.log &

    $ ./bin/tikv-server --pd="192.168.199.113:2379" \
                      --addr="192.168.199.116:20160" \
                      --data-dir=tikv \
                      --log-file=tikv.log &
    ```

3. Start TiDB on Node1.

    ```bash
    $ ./bin/tidb-server --store=tikv \
                      --path="192.168.199.113:2379" \
                      --log-file=tidb.log
    ```

4. Use the MySQL client to connect to TiDB.

    ```sh
    $ mysql -h 192.168.199.113 -P 4000 -u root -D test
    ```
