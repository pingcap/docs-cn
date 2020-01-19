---
title: Local Deployment from Binary Tarball
summary: Use the binary to deploy a TiDB cluster.
category: how-to
aliases: ['/docs/op-guide/binary-local-deployment/','/docs/v3.0/how-to/get-started/local-cluster/install-from-binary/']
---

# Local Deployment from Binary Tarball

This guide provides installation instructions for all TiDB components on a single developer machine. It is intended for evaluation purposes, and does not match the recommended usage for production systems.

See also [testing environment](/v3.0/how-to/deploy/from-tarball/testing-environment.md) and [production environment](/v3.0/how-to/deploy/from-tarball/production-environment.md) deployment.

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

{{< copyable "shell-regular" >}}

```bash
tidbuser="tidb"
&&
cat << EOF > /tmp/tidb.conf
$tidbuser        soft        nofile        1000000
$tidbuser        hard        nofile        1000000
EOF
&&
sudo cp /tmp/tidb.conf /etc/security/limits.d/ &&
sudo sysctl -w fs.file-max=1000000
```

See the [production deployment](/v3.0/how-to/deploy/from-tarball/production-environment.md) optional kernel tuning parameters.

## Create a database running user account

1. Log in to the machine using the `root` user account and create a database running user account (`tidb`) using the following command:

    {{< copyable "shell-root" >}}

    ```bash
    useradd tidb -m
    ```

2. Switch the user from `root` to `tidb` by using the following command. You can use this `tidb` user account to deploy your TiDB cluster.

    {{< copyable "shell-root" >}}

    ```bash
    su - tidb
    ```

## Download the official binary package

1. Download the package.

    {{< copyable "shell-regular" >}}

    ```bash
    wget https://download.pingcap.org/tidb-v3.0-linux-amd64.tar.gz https://download.pingcap.org/tidb-v3.0-linux-amd64.sha256
    ```

2. Check the file integrity. If the result is OK, the file is correct.

    {{< copyable "shell-regular" >}}

    ```bash
    sha256sum -c tidb-v3.0-linux-amd64.sha256
    ```

3. Extract the package.

    {{< copyable "shell-regular" >}}

    ```bash
    tar -xzf tidb-v3.0-linux-amd64.tar.gz &&
    cd tidb-v3.0-linux-amd64
    ```

## Start

Follow the steps below to start PD, TiKV and TiDB:

1. Start PD.

    {{< copyable "shell-regular" >}}

    ```bash
    ./bin/pd-server --data-dir=pd \
                    --log-file=pd.log &
    ```

2. Start TiKV.

    {{< copyable "shell-regular" >}}

    ```bash
    ./bin/tikv-server --pd="127.0.0.1:2379" \
                      --data-dir=tikv \
                      --log-file=tikv.log &
    ```

3. Start TiDB.

    {{< copyable "shell-regular" >}}

    ```bash
    ./bin/tidb-server --store=tikv \
                      --path="127.0.0.1:2379" \
                      --log-file=tidb.log &
    ```

4. Use the MySQL client to connect to TiDB.

    {{< copyable "shell-regular" >}}

    ```sh
    mysql -h 127.0.0.1 -P 4000 -u root -D test
    ```
