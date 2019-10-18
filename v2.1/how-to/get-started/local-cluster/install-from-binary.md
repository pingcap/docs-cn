---
title: Local Deployment from Binary Tarball
summary: Use the binary to deploy a TiDB cluster.
category: how-to
---

# Local Deployment from Binary Tarball

This guide provides installation instructions for all TiDB components on a single developer machine. It is intended for evaluation purposes, and does not match the recommended usage for production systems.

See also [testing environment](/v2.1/how-to/deploy/from-tarball/testing-environment.md) and [production environment](/v2.1/how-to/deploy/from-tarball/production-environment.md) deployment.

The following local TCP ports will be used:

| Component | Port  | Protocol | Description |
| --------- | ----- | -------- | ----------- |
| TiDB      | 4000  | TCP      | the communication port for the application and DBA tools |
| TiDB      | 10080 | TCP      | the communication port to report TiDB status |
| TiKV      | 20160 | TCP      | the TiKV communication port  |
| PD        | 2379  | TCP      | the communication port between TiDB and PD |
| PD        | 2380  | TCP      | the inter-node communication port within the PD cluster |

## Prepare

This guide is for deployment on Linux only. It is recommended to use RHEL/CentOS 7.3 or higher. TiKV requires you to raise the open files limit:

```bash
tidbuser="tidb"

cat << EOF > /tmp/tidb.conf
$tidbuser        soft        nofile        1000000
$tidbuser        hard        nofile        1000000
EOF

sudo cp /tmp/tidb.conf /etc/security/limits.d/
sudo sysctl -w fs.file-max=1000000
```

See the [production deployment](/v2.1/how-to/deploy/from-tarball/production-environment.md) optional kernel tuning parameters.

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

## Start

Follow the steps below to start PD, TiKV and TiDB:

1. Start PD.

    ```bash
    $ ./bin/pd-server --data-dir=pd \
                    --log-file=pd.log &
    ```

2. Start TiKV.

    ```bash
    $ ./bin/tikv-server --pd="127.0.0.1:2379" \
                      --data-dir=tikv \
                      --log-file=tikv.log &
    ```

3. Start TiDB.

    ```bash
    $ ./bin/tidb-server --store=tikv \
                      --path="127.0.0.1:2379" \
                      --log-file=tidb.log &
    ```

4. Use the MySQL client to connect to TiDB.

    ```sh
    $ mysql -h 127.0.0.1 -P 4000 -u root -D test
    ```
