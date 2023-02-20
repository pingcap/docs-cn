---
title: Quick Start Guide for the TiDB Database Platform
summary: Learn how to quickly get started with the TiDB platform and see if TiDB is the right choice for you.
aliases: ['/docs/dev/quick-start-with-tidb/','/docs/dev/test-deployment-using-docker/']
---

# Quick Start Guide for the TiDB Database Platform

This guide walks you through the quickest way to get started with TiDB. For non-production environments, you can deploy your TiDB database by either of the following methods:

- [Deploy a local test cluster](#deploy-a-local-test-cluster) (for macOS and Linux)
- [Simulate production deployment on a single machine](#simulate-production-deployment-on-a-single-machine) (for Linux only)

> **Note:**
>
> The deployment method provided in this guide is **ONLY FOR** quick start, **NOT FOR** production.
>
> - To deploy an on-premises production cluster, see [production installation guide](/production-deployment-using-tiup.md).
> - To deploy TiDB on Kubernetes, see [Get Started with TiDB on Kubernetes](https://docs.pingcap.com/tidb-in-kubernetes/stable/get-started).
> - To manage TiDB in the cloud, see [TiDB Cloud Quick Start](https://docs.pingcap.com/tidbcloud/tidb-cloud-quickstart).

## Deploy a local test cluster

- Scenario: Quickly deploy a local TiDB cluster for testing using a single macOS or Linux server. By deploying such a cluster, you can learn the basic architecture of TiDB and the operation of its components, such as TiDB, TiKV, PD, and the monitoring components.

<SimpleTab>
<div label="macOS">

As a distributed system, a basic TiDB test cluster usually consists of 2 TiDB instances, 3 TiKV instances, 3 PD instances, and optional TiFlash instances. With TiUP Playground, you can quickly build the test cluster by taking the following steps:

1. Download and install TiUP:

    {{< copyable "shell-regular" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

    If the following message is displayed, you have installed TiUP successfully:

    ```log
    Successfully set mirror to https://tiup-mirrors.pingcap.com
    Detected shell: zsh
    Shell profile:  /Users/user/.zshrc
    /Users/user/.zshrc has been modified to add tiup to PATH
    open a new terminal or source /Users/user/.zshrc to use it
    Installed path: /Users/user/.tiup/bin/tiup
    ===============================================
    Have a try:     tiup playground
    ===============================================
    ```

    Note the Shell profile path in the output above. You need to use the path in the next step.

2. Declare the global environment variable:

    > **Note:**
    >
    > After the installation, TiUP displays the absolute path of the corresponding Shell profile file. You need to modify `${your_shell_profile}` in the following `source` command according to the path. In this case, `${your_shell_profile}` is `/Users/user/.zshrc` from the output of Step 1.

    {{< copyable "shell-regular" >}}

    ```shell
    source ${your_shell_profile}
    ```

3. Start the cluster in the current session:

    - If you want to start a TiDB cluster of the latest version with 1 TiDB instance, 1 TiKV instance, 1 PD instance, and 1 TiFlash instance, run the following command:

        {{< copyable "shell-regular" >}}

        ```shell
        tiup playground
        ```

    - If you want to specify the TiDB version and the number of the instances of each component, run a command like this:

        {{< copyable "shell-regular" >}}

        ```shell
        tiup playground v6.6.0 --db 2 --pd 3 --kv 3
        ```

        The command downloads a version cluster to the local machine and starts it, such as v6.6.0. To view the latest version, run `tiup list tidb`.

        This command returns the access methods of the cluster:

        ```log
        CLUSTER START SUCCESSFULLY, Enjoy it ^-^
        To connect TiDB: mysql --comments --host 127.0.0.1 --port 4001 -u root -p (no password)
        To connect TiDB: mysql --comments --host 127.0.0.1 --port 4000 -u root -p (no password)
        To view the dashboard: http://127.0.0.1:2379/dashboard
        PD client endpoints: [127.0.0.1:2379 127.0.0.1:2382 127.0.0.1:2384]
        To view Prometheus: http://127.0.0.1:9090
        To view Grafana: http://127.0.0.1:3000
        ```

        > **Note:**
        >
        > + Since v5.2.0, TiDB supports running `tiup playground` on the machine that uses the Apple M1 chip.
        > + For the playground operated in this way, after the test deployment is finished, TiUP will clean up the original cluster data. You will get a new cluster after re-running the command.
        > + If you want the data to be persisted on storage, run `tiup --tag <your-tag> playground ...`. For details, refer to [TiUP Reference Guide](/tiup/tiup-reference.md#-t---tag).

4. Start a new session to access TiDB:

    + Use the TiUP client to connect to TiDB.

        {{< copyable "shell-regular" >}}

        ```shell
        tiup client
        ```

    + You can also use the MySQL client to connect to TiDB.

        {{< copyable "shell-regular" >}}

        ```shell
        mysql --host 127.0.0.1 --port 4000 -u root
        ```

5. Access the Prometheus dashboard of TiDB at <http://127.0.0.1:9090>.

6. Access the [TiDB Dashboard](/dashboard/dashboard-intro.md) at <http://127.0.0.1:2379/dashboard>. The default username is `root`, with an empty password.

7. Access the Grafana dashboard of TiDB through <http://127.0.0.1:3000>. Both the default username and password are `admin`.

8. (Optional) [Load data to TiFlash](/tiflash/tiflash-overview.md#use-tiflash) for analysis.

9. Clean up the cluster after the test deployment:

    1. Stop the above TiDB service by pressing <kbd>Control+C</kbd>.

    2. Run the following command after the service is stopped:

        {{< copyable "shell-regular" >}}

        ```shell
        tiup clean --all
        ```

> **Note:**
>
> TiUP Playground listens on `127.0.0.1` by default, and the service is only locally accessible. If you want the service to be externally accessible, specify the listening address using the `--host` parameter to bind the network interface card (NIC) to an externally accessible IP address.

</div>
<div label="Linux">

As a distributed system, a basic TiDB test cluster usually consists of 2 TiDB instances, 3 TiKV instances, 3 PD instances, and optional TiFlash instances. With TiUP Playground, you can quickly build the test cluster by taking the following steps:

1. Download and install TiUP:

    {{< copyable "shell-regular" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

    If the following message is displayed, you have installed TiUP successfully:

    ```log
    Successfully set mirror to https://tiup-mirrors.pingcap.com
    Detected shell: zsh
    Shell profile:  /Users/user/.zshrc
    /Users/user/.zshrc has been modified to add tiup to PATH
    open a new terminal or source /Users/user/.zshrc to use it
    Installed path: /Users/user/.tiup/bin/tiup
    ===============================================
    Have a try:     tiup playground
    ===============================================
    ```

    Note the Shell profile path in the output above. You need to use the path in the next step.

2. Declare the global environment variable:

    > **Note:**
    >
    > After the installation, TiUP displays the absolute path of the corresponding Shell profile file. You need to modify `${your_shell_profile}` in the following `source` command according to the path.

    {{< copyable "shell-regular" >}}

    ```shell
    source ${your_shell_profile}
    ```

3. Start the cluster in the current session:

    - If you want to start a TiDB cluster of the latest version with 1 TiDB instance, 1 TiKV instance, 1 PD instance, and 1 TiFlash instance, run the following command:

        {{< copyable "shell-regular" >}}

        ```shell
        tiup playground
        ```

    - If you want to specify the TiDB version and the number of the instances of each component, run a command like this:

        {{< copyable "shell-regular" >}}

        ```shell
        tiup playground v6.6.0 --db 2 --pd 3 --kv 3
        ```

        The command downloads a version cluster to the local machine and starts it, such as v6.6.0. To view the latest version, run `tiup list tidb`.

        This command returns the access methods of the cluster:

        ```log
        CLUSTER START SUCCESSFULLY, Enjoy it ^-^
        To connect TiDB: mysql --host 127.0.0.1 --port 4000 -u root -p (no password) --comments
        To view the dashboard: http://127.0.0.1:2379/dashboard
        PD client endpoints: [127.0.0.1:2379]
        To view the Prometheus: http://127.0.0.1:9090
        To view the Grafana: http://127.0.0.1:3000
        ```

        > **Note:**
        >
        > For the playground operated in this way, after the test deployment is finished, TiUP will clean up the original cluster data. You will get a new cluster after re-running the command.
        > If you want the data to be persisted on storage, run `tiup --tag <your-tag> playground ...`. For details, refer to [TiUP Reference Guide](/tiup/tiup-reference.md#-t---tag).

4. Start a new session to access TiDB:

    + Use the TiUP client to connect to TiDB.

        {{< copyable "shell-regular" >}}

        ```shell
        tiup client
        ```

    + You can also use the MySQL client to connect to TiDB.

        {{< copyable "shell-regular" >}}

        ```shell
        mysql --host 127.0.0.1 --port 4000 -u root
        ```

5. Access the Prometheus dashboard of TiDB at <http://127.0.0.1:9090>.

6. Access the [TiDB Dashboard](/dashboard/dashboard-intro.md) at <http://127.0.0.1:2379/dashboard>. The default username is `root`, with an empty password.

7. Access the Grafana dashboard of TiDB through <http://127.0.0.1:3000>. Both the default username and password are `admin`.

8. (Optional) [Load data to TiFlash](/tiflash/tiflash-overview.md#use-tiflash) for analysis.

9. Clean up the cluster after the test deployment:

    1. Stop the process by pressing <kbd>Control+C</kbd>.

    2. Run the following command after the service is stopped:

        {{< copyable "shell-regular" >}}

        ```shell
        tiup clean --all
        ```

> **Note:**
>
> TiUP Playground listens on `127.0.0.1` by default, and the service is only locally accessible. If you want the service to be externally accessible, specify the listening address using the `--host` parameter to bind the network interface card (NIC) to an externally accessible IP address.

</div>
</SimpleTab>

## Simulate production deployment on a single machine

- Scenario: Experience the smallest TiDB cluster with the complete topology and simulate the production deployment steps on a single Linux server.

This section describes how to deploy a TiDB cluster using a YAML file of the smallest topology in TiUP.

### Prepare

Prepare a target machine that meets the following requirements:

- CentOS 7.3 or a later version is installed
- The Linux OS has access to the Internet, which is required to download TiDB and related software installation packages

The smallest TiDB cluster topology is as follows:

> **Note:**
>
> The IP address of the following instances only serves as an example IP. In your actual deployment, you need to replace the IP with your actual IP.

| Instance | Count | IP | Configuration |
|:-- | :-- | :-- | :-- |
| TiKV | 3 | 10.0.1.1 <br/> 10.0.1.1 <br/> 10.0.1.1 | Avoid conflict between the port and the directory |
| TiDB | 1 | 10.0.1.1 | The default port <br/> Global directory configuration |
| PD | 1 | 10.0.1.1 | The default port <br/> Global directory configuration |
| TiFlash | 1 | 10.0.1.1 | The default port <br/> Global directory configuration |
| Monitor | 1 | 10.0.1.1 | The default port <br/> Global directory configuration |

Other requirements for the target machine:

- The `root` user and its password is required
- [Stop the firewall service of the target machine](/check-before-deployment.md#check-and-stop-the-firewall-service-of-target-machines), or open the port needed by the TiDB cluster nodes
- Currently, the TiUP cluster supports deploying TiDB on the x86_64 (AMD64) and ARM architectures:

    - It is recommended to use CentOS 7.3 or later versions on AMD64
    - It is recommended to use CentOS 7.6 1810 on ARM

### Deploy

> **Note:**
>
> You can log in to the target machine as a regular user or the `root` user. The following steps use the `root` user as an example.

1. Download and install TiUP:

    {{< copyable "shell-regular" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2. Declare the global environment variable.

    > **Note:**
    >
    > After the installation, TiUP displays the absolute path of the corresponding Shell profile file. You need to modify `${your_shell_profile}` in the following `source` command according to the path.

    {{< copyable "shell-regular" >}}

    ```shell
    source ${your_shell_profile}
    ```

3. Install the cluster component of TiUP:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster
    ```

4. If the TiUP cluster is already installed on the machine, update the software version:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup update --self && tiup update cluster
    ```

5. Use the root user privilege to increase the connection limit of the `sshd` service. This is because TiUP needs to simulate deployment on multiple machines.

    1. Modify `/etc/ssh/sshd_config`, and set `MaxSessions` to `20`.
    2. Restart the `sshd` service:

        {{< copyable "shell-root" >}}

        ```shell
        service sshd restart
        ```

6. Create and start the cluster:

    Edit the configuration file according to the following template, and name it as `topo.yaml`:

    {{< copyable "" >}}

    ```yaml
    # # Global variables are applied to all deployments and used as the default value of
    # # the deployments if a specific deployment value is missing.
    global:
     user: "tidb"
     ssh_port: 22
     deploy_dir: "/tidb-deploy"
     data_dir: "/tidb-data"

    # # Monitored variables are applied to all the machines.
    monitored:
     node_exporter_port: 9100
     blackbox_exporter_port: 9115

    server_configs:
     tidb:
       log.slow-threshold: 300
     tikv:
       readpool.storage.use-unified-pool: false
       readpool.coprocessor.use-unified-pool: true
     pd:
       replication.enable-placement-rules: true
       replication.location-labels: ["host"]
     tiflash:
       logger.level: "info"

    pd_servers:
     - host: 10.0.1.1

    tidb_servers:
     - host: 10.0.1.1

    tikv_servers:
     - host: 10.0.1.1
       port: 20160
       status_port: 20180
       config:
         server.labels: { host: "logic-host-1" }

     - host: 10.0.1.1
       port: 20161
       status_port: 20181
       config:
         server.labels: { host: "logic-host-2" }

     - host: 10.0.1.1
       port: 20162
       status_port: 20182
       config:
         server.labels: { host: "logic-host-3" }

    tiflash_servers:
     - host: 10.0.1.1

    monitoring_servers:
     - host: 10.0.1.1

    grafana_servers:
     - host: 10.0.1.1
    ```

    - `user: "tidb"`: Use the `tidb` system user (automatically created during deployment) to perform the internal management of the cluster. By default, use port 22 to log in to the target machine via SSH.
    - `replication.enable-placement-rules`: This PD parameter is set to ensure that TiFlash runs normally.
    - `host`: The IP of the target machine.

7. Execute the cluster deployment command:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster deploy <cluster-name> <version> ./topo.yaml --user root -p
    ```

    - `<cluster-name>`: Set the cluster name
    - `<version>`: Set the TiDB cluster version, such as `v6.5.0`. You can see all the supported TiDB versions by running the `tiup list tidb` command
    - `-p`: Specify the password used to connect to the target machine.

        > **Note:**
        >
        > If you use secret keys, you can specify the path of the keys through `-i`. Do not use `-i` and `-p` at the same time.

    Enter "y" and the `root` user's password to complete the deployment:

    ```log
    Do you want to continue? [y/N]:  y
    Input SSH password:
    ```

8. Start the cluster:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster start <cluster-name>
    ```

9. Access the cluster:

    - Install the MySQL client. If it is already installed, skip this step.

        {{< copyable "shell-regular" >}}

        ```shell
        yum -y install mysql
        ```

    - Access TiDB. The password is empty:

        {{< copyable "shell-regular" >}}

        ```shell
        mysql -h 10.0.1.1 -P 4000 -u root
        ```

    - Access the Grafana monitoring dashboard at <http://{grafana-ip}:3000>. The default username and password are both `admin`.

    - Access the [TiDB Dashboard](/dashboard/dashboard-intro.md) at <http://{pd-ip}:2379/dashboard>. The default username is `root`, and the password is empty.

    - To view the currently deployed cluster list:

        {{< copyable "shell-regular" >}}

        ```shell
        tiup cluster list
        ```

    - To view the cluster topology and status:

         {{< copyable "shell-regular" >}}

        ```shell
        tiup cluster display <cluster-name>
        ```

## What's next

- If you have just deployed a TiDB cluster for the local test environment:

    - Learn [Basic SQL operations in TiDB](/basic-sql-operations.md)
    - [Migrate data to TiDB](/migration-overview.md)

- If you are ready to deploy a TiDB cluster for the production environment:

    - [Deploy TiDB using TiUP](/production-deployment-using-tiup.md)
    - [Deploy TiDB on Cloud using TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/stable)

- If you're looking for analytics solution with TiFlash:

    - [Use TiFlash](/tiflash/tiflash-overview.md#use-tiflash)
    - [TiFlash Overview](/tiflash/tiflash-overview.md)
