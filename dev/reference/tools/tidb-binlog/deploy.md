---
title: TiDB-Binlog Cluster Deployment
summary: Learn how to deploy TiDB-Binlog cluster.
category: reference
aliases: ['/docs/tools/binlog/deploy/']
---

# TiDB-Binlog Cluster Deployment

This document describes two methods of deploying TiDB-Binlog:

- [Deploy TiDB-Binlog using TiDB-Ansible](#deploy-tidb-binlog-using-tidb-ansible)
- [Deploy TiDB-Binlog using a Binary package](#deploy-tidb-binlog-using-a-binary-package)

It is recommended to deploy TiDB-Binlog using TiDB-Ansible. If you just want to do a simple testing, you can deploy TiDB-Binlog using a Binary package.

## Deploy TiDB-Binlog using TiDB-Ansible 

### Step 1: Download TiDB-Ansible

1. Use the TiDB user account to log in to the central control machine and go to the `/home/tidb` directory. The information about the branch of TiDB-Ansible and the corresponding TiDB version is as follows. If you have questions regarding which version to use, email to [info@pingcap.com](mailto:info@pingcap.com) for more information or [file an issue](https://github.com/pingcap/tidb-ansible/issues/new).

    | tidb-ansible branch | TiDB version | Note |
    | ------------------- | ------------ | ---- |
    | release-2.0 | 2.0 version | The latest 2.0 stable version. You can use it in the production environment. |
    | release-2.1 | 2.1 version | The latest 2.1 stable version. You can use it in the production environment (recommended). |
    | master | master version | This version includes the latest features with a daily update. |

2. Use the following command to download the corresponding branch of TiDB-Ansible from the [TiDB-Ansible project](https://github.com/pingcap/tidb-ansible) on GitHub. The default folder name is `tidb-ansible`.

    - Download the 2.0 version:
        
        ```bash
        $ git clone -b release-2.0-new-binlog https://github.com/pingcap/tidb-ansible.git
        ```

    - Download the 2.1 version:

        ```bash
        $ git clone -b release-2.1 https://github.com/pingcap/tidb-ansible.git
        ```

    - Download the master version:

        ```bash
        $ git clone https://github.com/pingcap/tidb-ansible.git
        ```
        
### Step 2: Deploy Pump
1. Modify the `tidb-ansible/inventory.ini` file.

    1. Set `enable_binlog = True` to start `binlog` of the TiDB cluster.

        ```ini
        ## binlog trigger
        enable_binlog = True
        ```

    2. Add the deployment machine IPs for `pump_servers`.

        ```ini
        ## Binlog Part
        [pump_servers]
        172.16.10.72
        172.16.10.73
        172.16.10.74
        ```

        Pump retains the data of the latest 7 days by default. You can modify the value of the `gc` variable in the `tidb-ansible/conf/pump.yml` file and remove the related comments: 
        
        ```yaml
        global:
          # an integer value to control the expiry date of the binlog data, which indicates for how long (in days) the binlog data would be stored
          # must be bigger than 0
          # gc: 7
        ```

        Make sure the space of the deployment directory is sufficient for storing Binlog. For more details, see [Configure the deployment directory](/dev/how-to/deploy/orchestrated/ansible.md#configure-the-deployment-directory). You can also set a separate deployment directory for Pump.

        ```ini
        ## Binlog Part
        [pump_servers]
        pump1 ansible_host=172.16.10.72 deploy_dir=/data1/pump
        pump2 ansible_host=172.16.10.73 deploy_dir=/data2/pump
        pump3 ansible_host=172.16.10.74 deploy_dir=/data3/pump
        ```

2. Deploy and start the TiDB cluster containing Pump.

    After configuring the `inventory.ini` file, you can choose one method from below to deploy the TiDB cluster.

    **Method #1**: Add Pump on the existing TiDB cluster.

    1. Deploy `pump_servers` and `node_exporters`.

        ```
        ansible-playbook deploy.yml -l ${pump1_ip}, ${pump2_ip}, [${alias1_name}, ${alias2_name}]
        ```

    2. Start `pump_servers`.

        ```
        ansible-playbook start.yml --tags=pump
        ```

    3. Update and restart `tidb_servers`.

        ```
        ansible-playbook rolling_update.yml --tags=tidb
        ```

    4. Update the monitoring data.

        ```
        ansible-playbook rolling_update_monitor.yml --tags=prometheus
        ```

    **Method #2**: Deploy a TiDB cluster containing Pump from scratch.

    For how to use Ansible to deploy the TiDB cluster, see [Deploy TiDB Using Ansible](/dev/how-to/deploy/orchestrated/ansible.md).

3. Check the Pump status.

    Use `binlogctl` to check the Pump status. Change the `pd-urls` parameter to the PD address of the cluster. If `State` is `online`, Pump is started successfully.

    ```bash
    $ cd /home/tidb/tidb-ansible
    $ resources/bin/binlogctl -pd-urls=http://172.16.10.72:2379 -cmd pumps
    
    INFO[0000] pump: {NodeID: ip-172-16-10-72:8250, Addr: 172.16.10.72:8250, State: online, MaxCommitTS: 403051525690884099, UpdateTime: 2018-12-25 14:23:37 +0800 CST}
    INFO[0000] pump: {NodeID: ip-172-16-10-73:8250, Addr: 172.16.10.73:8250, State: online, MaxCommitTS: 403051525703991299, UpdateTime: 2018-12-25 14:23:36 +0800 CST}
    INFO[0000] pump: {NodeID: ip-172-16-10-74:8250, Addr: 172.16.10.74:8250, State: online, MaxCommitTS: 403051525717360643, UpdateTime: 2018-12-25 14:23:35 +0800 CST}
    ```

### Step 3: Deploy Drainer

1. Obtain `initial_commit_ts`. 

    Run the following command to use `binlogctl` to generate the `tso` information which is needed for the initial start of Drainer:

    ```bash
    $ cd /home/tidb/tidb-ansible
    $ resources/bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd generate_meta
    INFO[0000] [pd] create pd client with endpoints [http://192.168.199.118:32379]
    INFO[0000] [pd] leader switches to: http://192.168.199.118:32379, previous:
    INFO[0000] [pd] init cluster id 6569368151110378289
    2018/06/21 11:24:47 meta.go:117: [info] meta: &{CommitTS:400962745252184065}
    ```

    This command outputs `meta: &{CommitTS:400962745252184065}`, and the value of `CommitTS` is used as the value of the `initial-commit-ts` parameter needed for the initial start of Drainer.

2. Modify the `tidb-ansible/inventory.ini` file.

    Add the deployment machine IPs for `drainer_servers`. Set `initial_commit_ts` to the value you have obtained, which is only used for the initial start of Drainer.

    - Assume that the downstream is MySQL with the alias `drainer_mysql`:

        ```ini
        [drainer_servers]
        drainer_mysql ansible_host=172.16.10.71 initial_commit_ts="402899541671542785"
        ```

    - Assume that the downstream is `file` with the alias `drainer_file`:

        ```ini
        [drainer_servers]
        drainer_file ansible_host=172.16.10.71 initial_commit_ts="402899541671542785"
        ```

3. Modify the configuration file.

    - Assume that the downstream is MySQL:

        ```bash
        $ cd /home/tidb/tidb-ansible/conf
        $ cp drainer.toml drainer_mysql_drainer.toml
        $ vi drainer_mysql_drainer.toml
        ```

        > **Note:**
        >
        > Name the configuration file as `alias_drainer.toml`. Otherwise, the customized configuration file cannot be found during the deployment process.
        
        Set `db-type` to `mysql` and configure the downstream MySQL information:

        ```toml
        # downstream storage, equal to --dest-db-type
        # Valid values are "mysql", "file", "kafka", and "flash".
        db-type = "mysql"

        # the downstream MySQL protocol database
        [syncer.to]
        host = "172.16.10.72"
        user = "root"
        password = "123456"
        port = 3306
        # Time and size limits for flash batch write
        ```

    - Assume that the downstream is incremental backup data:

        ```bash
        $ cd /home/tidb/tidb-ansible/conf
        $ cp drainer.toml drainer_file_drainer.toml
        $ vi drainer_file_drainer.toml
        ```

        Set `db-type` to `file`.

        ```toml
        # downstream storage, equal to --dest-db-type
        # Valid values are "mysql", "file", "kafka", and "flash".
        db-type = "file"

        # Uncomment this if you want to use `file` as `db-type`. 
        # The value can be `gzip`. Leave it empty to disable compression. 
        [syncer.to]
        # default data directory: "{{ deploy_dir }}/data.drainer"
        dir = "data.drainer"
        ```

4. Deploy Drainer.

    ```bash
    $ ansible-playbook deploy_drainer.yml
    ```

5. Start Drainer.

    ```bash
    $ ansible-playbook start_drainer.yml
    ```

## Deploy TiDB-Binlog using a Binary package

### Download the official Binary package

Run the following commands to download the packages:

```bash
version="latest" for nightly builds
wget https://download.pingcap.org/tidb-latest-linux-amd64.{tar.gz,sha256}

# Check the file integrity. If the result is OK, the file is correct.
sha256sum -c tidb-latest-linux-amd64.sha256
```

For TiDB v2.1.0 GA or later versions, Pump and Drainer are already included in the TiDB download package. For other TiDB versions, you need to download Pump and Drainer separately using the following command:

```bash
wget https://download.pingcap.org/tidb-binlog-$version-linux-amd64.{tar.gz,sha256}

# Check the file integrity. If the result is OK, the file is correct.
sha256sum -c tidb-binlog-$version-linux-amd64.sha256
```

### The usage example

Assuming that you have three PD nodes, one TiDB node, two Pump nodes, and one Drainer node, the information of each node is as follows:

| Node     | IP           |
| ---------|:------------:|
| TiDB     | 192.168.0.10 |
| PD1      | 192.168.0.16 |
| PD2      | 192.168.0.15 |
| PD3      | 192.168.0.14 |
| Pump     | 192.168.0.11 |
| Pump     | 192.168.0.12 |
| Drainer  | 192.168.0.13 |

The following part shows how to use Pump and Drainer based on the nodes above.

1. Deploy Pump using the binary.

    - To view the command line parameters of Pump, execute `./bin/pump -help`:

        ```
        Usage of Pump:
        -L string
            the output information level of logs: debug, info, warn, error, fatal ("info" by default)
        -V
            the print version information
        -addr string
            the RPC address through which Pump provides the service (-addr="192.168.0.11:8250")
        -advertise-addr string
            the RPC address through which Pump provides the external service (-advertise-addr="192.168.0.11:8250")
        -config string
            the path of the configuration file. If you specify the configuration file, Pump reads the configuration in the configuration file first. If the corresponding configuration also exits in the command line parameters, Pump uses the configuration of the command line parameters to cover that of the configuration file.
        -data-dir string
            the path where the Pump data is stored
        -gc int
            the number of days to retain the data in Pump (7 by default)
        -heartbeat-interval int
            the interval of the heartbeats Pump sends to PD (in seconds)
        -log-file string
            the file path of logs
        -log-rotate string
            the switch frequency of logs (hour/day)
        -metrics-addr string
            the Prometheus Pushgateway address. If not set, it is forbidden to report the monitoring metrics.
        -metrics-interval int
            the report frequency of the monitoring metrics (15 by default, in seconds)
        -pd-urls string
            the address of the PD cluster nodes (-pd-urls="http://192.168.0.16:2379,http://192.168.0.15:2379,http://192.168.0.14:2379")
        ```

    - Taking deploying Pump on "192.168.0.11" as an example, the Pump configuration file is as follows:

        ```toml
        # Pump Configuration

        # the bound address of Pump
        addr = "192.168.0.11:8250"

        # the address through which Pump provides the service
        advertise-addr = "192.168.0.11:8250"

        # the number of days to retain the data in Pump (7 by default)
        gc = 7

        # the directory where the Pump data is stored
        data-dir = "data.pump"

        # the interval of the heartbeats Pump sends to PD (in seconds)
        heartbeat-interval = 2
    
        # the address of the PD cluster nodes
        pd-urls = "http://192.168.0.16:2379,http://192.168.0.15:2379,http://192.168.0.14:2379"

        # [storage]
        # Set to true (by default) to guarantee reliability by ensuring binlog data is flushed to the disk
        # sync-log = true
        ```

    - The example of starting Pump:

        ```bash
        ./bin/pump -config pump.toml
        ```
  
        If the command line parameters is the same with the configuration file parameters, the values of command line parameters are used.

2. Deploy Drainer using binary.

    - To view the command line parameters of Drainer, execute `./bin/drainer -help`:

        ```
        Usage of Drainer:
        -L string
            the output information level of logs: debug, info, warn, error, fatal ("info" by default)
        -V
            the print version information
        -addr string
            the address through which Drainer provides the service (-addr="192.168.0.13:8249")
        -c int
            the number of the concurrency of the downstream for synchronization. The bigger the value, the better throughput performance of the concurrency (1 by default).
        -config string
            the directory of the configuration file. Drainer reads the configuration file first.
            If the corresponding configuration exists in the command line parameters, Drainer uses the configuration of the command line parameters to cover that of the configuration file.
        -data-dir string
            the directory where the Drainer data is stored ("data.drainer" by default)
        -dest-db-type string
            the downstream service type of Drainer
            The value can be "mysql", "kafka", "file", and "flash". ("mysql" by default)
        -detect-interval int
            the interval of checking the online Pump in PD (10 by default, in seconds)
        -disable-detect
            whether to disable the conflict monitoring
        -disable-dispatch
            whether to disable the SQL feature of splitting a single binlog file. If it is set to "true", each binlog file is restored to a single transaction for synchronization based on the order of binlogs. 
            It is set to "False", when the downstream is MySQL.
        -ignore-schemas string
            the db filter list ("INFORMATION_SCHEMA,PERFORMANCE_SCHEMA,mysql,test" by default)
            It does not support the Rename DDL operation on tables of `ignore schemas`.
        -initial-commit-ts
            If Drainer does not have the related breakpoint information, you can configure the related breakpoint information using this parameter.
            0 by default
        -log-file string
            the path of the log file
        -log-rotate string
            the switch frequency of log files, hour/day
        -metrics-addr string
            the Prometheus Pushgateway address
            It it is not set, the monitoring metrics are not reported.
        -metrics-interval int
            the report frequency of the monitoring metrics (15 by default, in seconds)
        -pd-urls string
            the address of the PD cluster nodes (-pd-urls="http://192.168.0.16:2379,http://192.168.0.15:2379,http://192.168.0.14:2379")
        -safe-mode
            whether to enable the safe mode (divides the Update statement to Delete + Replace)
        -txn-batch int
            the number of SQL statements of a transaction which are output to the downstream database (1 by default)
        ```

    - Taking deploying Drainer on "192.168.0.13" as an example, the Drainer configuration file is as follows:

        ```toml
        # Drainer Configuration.

        # the address through which Drainer provides the service ("192.168.0.13:8249")
        addr = "192.168.0.13:8249"

        # the interval of checking the online Pump in PD (10 by default, in seconds)
        detect-interval = 10

        # the directory where the Drainer data is stored "data.drainer" by default)
        data-dir = "data.drainer"

        # the address of the PD cluster nodes
        pd-urls = "http://192.168.0.16:2379,http://192.168.0.15:2379,http://192.168.0.14:2379"

        # the directory of the log file
        log-file = "drainer.log"

        # Drainer compresses the data when it gets the binlog from Pump. The value can be "gzip". If it is not configured, it will not be compressed
        # compressor = "gzip"

        # Syncer Configuration
        [syncer]
        # If the item is set, the sql-mode will be used to parse the DDL statement.
        # sql-mode = "STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION"

        # the number of SQL statements of a transaction that are output to the downstream database (20 by default)
        txn-batch = 20
    
        # the number of the concurrency of the downstream for synchronization. The bigger the value,
        # the better throughput performance of the concurrency (16 by default)
        worker-count = 16

        # whether to disable the SQL feature of splitting a single binlog file. If it is set to "true",
        # each binlog file is restored to a single transaction for synchronization based on the order of binlogs.
        # If the downstream service is MySQL, set it to "False".
        disable-dispatch = false

        # the downstream service type of Drainer ("mysql" by default)
        # Valid value: "mysql", "kafka", "file", "flash"
        db-type = "mysql"

        # the db filter list ("INFORMATION_SCHEMA,PERFORMANCE_SCHEMA,mysql,test" by default)
        # Does not support the Rename DDL operation on tables of `ignore schemas`.
        ignore-schemas = "INFORMATION_SCHEMA,PERFORMANCE_SCHEMA,mysql"

        # `replicate-do-db` has priority over `replicate-do-table`. When they have the same `db` name,
        # regular expressions are supported for configuration.
        # The regular expression should start with "~".

        # replicate-do-db = ["~^b.*","s1"]

        # [[syncer.replicate-do-table]]
        # db-name ="test"
        # tbl-name = "log"

        # [[syncer.replicate-do-table]]
        # db-name ="test"
        # tbl-name = "~^a.*"

        # Ignore the replication of some tables
        # [[syncer.ignore-table]]
        # db-name = "test"
        # tbl-name = "log"

        # the server parameters of the downstream database when `db-type` is set to "mysql"
        [syncer.to]
        host = "192.168.0.13"
        user = "root"
        password = ""
        port = 3306

        # the directory where the binlog file is stored when `db-type` is set to `file`
        # [syncer.to]
        # dir = "data.drainer"

        # the Kafka configuration when `db-type` is set to "kafka"
        # [syncer.to]
        # zookeeper-addrs = "127.0.0.1:2181"
        # kafka-addrs = "127.0.0.1:9092"
        # kafka-version = "0.8.2.0"

        # the topic name of the Kafka cluster that saves the binlog data. The default value is <cluster-id>_obinlog
        # To run multiple Drainers to replicate data to the same Kafka cluster, you need to set different `topic-name`s for each Drainer.
        # topic-name = ""
        ```

    - Starting Drainer:

        > **Note:**
        >
        > If the downstream is MySQL/TiDB, to guarantee the data integrity, you need to obtain the `initial-commit-ts` value and make a full backup of the data and restore the data before the initial start of Drainer. For details, see [Deploy Drainer](#step-3-deploy-drainer).

        When Drainer is started for the first time, use the `initial-commit-ts` parameter.

        ```bash
        ./bin/drainer -config drainer.toml -initial-commit-ts {initial-commit-ts}
        ```

        If the command line parameter and the configuration file parameter are the same, the parameter value in the command line is used.

3. Starting TiDB server:
        
    - After starting Pump and Drainer, start TiDB server with binlog enabled by adding this section to your config file for TiDB server:
        ```
        [binlog]
        enable=true
        ```

    - TiDB server will obtain the addresses of registered Pumps from PD and will stream data to all of them. If there are no registered Pump instances, TiDB server will refuse to start or will block starting until a Pump instance comes online.

> **Note:**
> 
> - When TiDB is running, you need to guarantee that at least one Pump is running normally.
> - To enable the TiDB-Binlog service in TiDB server, use the `-enable-binlog` startup parameter in TiDB, or add enable=true to the [binlog] section of the TiDB server configuration file.
> - Make sure that the TiDB-Binlog service is enabled in all TiDB instances in a same cluster, otherwise upstream and downstream data inconsistency might occur during data synchronization. If you want to temporarily run a TiDB instance where the TiDB-Binlog service is not enabled, set `run_ddl=false` in the TiDB configuration file.
> - Drainer does not support the `rename` DDL operation on the table of `ignore schemas` (the schemas in the filter list).
> - If you want to start Drainer in an existing TiDB cluster, generally you need to make a full backup of the cluster data, obtain `savepoint`, import the data to the target database, and then start Drainer to synchronize the incremental data from `savepoint`.
