---
title: Integrate TiDB with ProxySQL
summary: Introduce how to integrate TiDB with ProxySQL step by step.
---

# Integrate TiDB with ProxySQL

This document describes how to integrate **TiDB** with **ProxySQL** using CentOS 7 as an example. If you want to integrate using other systems, refer to the [Try Out](#4-try-out) section, which introduces how to deploy a test integration environment using **Docker** and **Docker Compose**. For more information, refer to:

- [TiDB Documentation](/overview.md)
- [TiDB Developer Guide](/develop/dev-guide-overview.md)
- [ProxySQL Documentation](https://proxysql.com/documentation/)
- [TiDB with ProxySQL Integration Test](https://github.com/Icemap/tidb-proxysql-integration-test)

## 1. Start TiDB

### Test environment

<SimpleTab groupId="startup-tidb">

<div label="TiDB Cloud" value="tidb-cloud">

You can refer to [Build a TiDB cluster in TiDB Cloud (Developer Tier)](/develop/dev-guide-build-cluster-in-cloud.md).

</div>

<div label="Source compilation" value="source-code">

1. Download the [TiDB](https://github.com/pingcap/tidb) source code, change to the `tidb-server` folder and run the `go build` command.

    ```shell
    git clone git@github.com:pingcap/tidb.git
    cd tidb/tidb-server
    go build
    ```

2. Use the configuration file [`tidb-config.toml`](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/tidb-config.toml) to start TiDB. The command is as follows:

    ```shell
    ${TIDB_SERVER_PATH} -config ./tidb-config.toml -store unistore -path "" -lease 0s > ${LOCAL_TIDB_LOG} 2>&1 &
    ```

    > **Note:**
    >
    > - The preceding command uses `unistore` as the storage engine, which is a test storage engine in TiDB. Make sure that you use it in a test environment only.
    > - `TIDB_SERVER_PATH`: the path of the compiled binary using `go build`. For example, if you execute the previous command under `/usr/local`, `TIDB_SERVER_PATH` is `/usr/local/tidb/tidb-server/tidb-server`.
    > - `LOCAL_TIDB_LOG`: the log file path of TiDB.

</div>

<div label="TiUP" value="tiup">

[TiUP](/tiup/tiup-overview.md), as the TiDB package manager, makes it easier to manage different cluster components in the TiDB ecosystem, such as TiDB, PD, and TiKV.

1. Install TiUP:

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2. Start TiDB in a test environment:

    ```shell
    tiup playground
    ```

</div>

</SimpleTab>

### Production environment

<SimpleTab groupId="startup-tidb">

<div label="TiDB Cloud" value="tidb-cloud">

It is recommended to use [TiDB Cloud](https://en.pingcap.com/tidb-cloud/) directly when you need hosting TiDB services (for example, you cannot manage it yourself, or you need a cloud-native environment). To build a TiDB cluster in a production environment, refer to [Create a TiDB cluster](https://docs.pingcap.com/tidbcloud/create-tidb-cluster).

</div>

<div label="Deploy Locally" value="tiup">

The production environment requires more steps than the test environment. To deploy an on-premises production cluster, it is recommended to refer to [Deploy a TiDB cluster using TiUP](/production-deployment-using-tiup.md) and then deploy it based on hardware conditions.

</div>

</SimpleTab>

## 2. Start ProxySQL

### Install ProxySQL by yum

1. Add the ProxySQL repository:

    ```shell
    cat > /etc/yum.repos.d/proxysql.repo << EOF
    [proxysql]
    name=ProxySQL YUM repository
    baseurl=https://repo.proxysql.com/ProxySQL/proxysql-2.4.x/centos/\$releasever
    gpgcheck=1
    gpgkey=https://repo.proxysql.com/ProxySQL/proxysql-2.4.x/repo_pub_key
    EOF
    ```

2. Install ProxySQL:

    ```shell
    yum install proxysql
    ```

3. Start ProxySQL:

    ```shell
    systemctl start proxysql
    ```

### Other installation ways

To install ProxySQL using other ways, refer to the [ProxySQL README](https://github.com/sysown/proxysql#installation) or the [ProxySQL installation documentation](https://proxysql.com/documentation/).

## 3. Configure ProxySQL

To use ProxySQL as a proxy for TiDB, you need to configure ProxySQL. The required configuration items are listed in the following sections. For more details about other configuration items, refer to the [ProxySQL official documentation](https://proxysql.com/documentation/).

### Simple introduction

ProxySQL uses a port to manage configuration, which is **_ProxySQL Admin interface_**, and a port to proxy, which is **_ProxySQL MySQL Interface_**.

- **_ProxySQL Admin interface_**: To connect to the admin interface, you can use an `admin` user to read and write configuration, or use a `stats` user to read part of statistics (cannot read or write configuration). The default credentials are `admin:admin` and `stats:stats`. For security reasons, you can use the default credentials to connect locally, but to connect remotely, you need to configure a new user, which is often named `radmin`.
- **_ProxySQL MySQL Interface_**: Used as a proxy to forward SQL to the configured service.

![proxysql config flow](/media/develop/proxysql_config_flow.png)

There are three layers in ProxySQL configurations: `runtime`, `memory`, and `disk`. You can change the configuration of the `memory` layer only. After modifying the configuration, you can use `LOAD xxx TO runtime` to make the configuration effective, and/or you can use `SAVE xxx TO DISK` to save to the disk to prevent configuration loss.

![proxysql config layer](/media/develop/proxysql_config_layer.png)

### Configure TiDB server

You can add multiple TiDB servers in ProxySQL. To add TiDB servers, perform the following at **_ProxySQL Admin interface_**:

```sql
INSERT INTO mysql_servers(hostgroup_id, hostname, port) VALUES (0, '127.0.0.1', 4000);
LOAD mysql servers TO runtime;
SAVE mysql servers TO DISK;
```

Field description:

- `hostgroup_id`: ProxySQL manages servers by **hostgroup**. To distribute SQL to these servers evenly, you can configure several servers that need load balancing to the same hostgroup. To distinguish the servers, such as read and write splitting, you can configure them to different hostgroup.
- `hostname`: The IP or domain of the TiDB server.
- `port`: The port of the TiDB server.

### Configure Proxy login users

After adding a TiDB server user to ProxySQL, ProxySQL allows this user to log in **_ProxySQL MySQL Interface_** and create a connection with TiDB. Make sure that the user has appropriate permissions in TiDB. To add a TiDB server user, perform the following at **_ProxySQL Admin interface_**:

```sql
INSERT INTO mysql_users(username, password, active, default_hostgroup, transaction_persistent) VALUES ('root', '', 1, 0, 1);
LOAD mysql users TO runtime;
SAVE mysql users TO DISK;
```

Field description:

- `username`: The user name.
- `password`: The password.
- `active`: Controls whether the user is active. `1` is active, and `0` is inactive. Only when the `active` is `1`, the user can log in.
- `default_hostgroup`: The default hostgroup used by the user, where SQL distributed to unless the query rule routes the traffic to a specific hostgroup.
- `transaction_persistent`: `1` indicates persistent transaction. That is, when the user starts a transaction in a connection, all statements are routed to the same hostgroup until the transaction is committed or rolled back.

### Configure ProxySQL by a configuration file

In addition to configuring using **_ProxySQL Admin interface_**, you can also configure ProxySQL using a configuration file. In the [Configuring ProxySQL through the config file](https://github.com/sysown/proxysql#configuring-proxysql-through-the-config-file) document, the configuration file should only be considered as a secondary way of initializing ProxySQL, not the primary way. The configuration file is only used when the SQLite is not created and will not be used after the SQLite is created. When using the configuration file to configure ProxySQL, you should delete SQLite first using the following command. But this **loses** configuration changes in **_ProxySQL Admin interface_**.

```shell
rm /var/lib/proxysql/proxysql.db
```

Alternatively, you can execute the `LOAD xxx FROM CONFIG` command to overwrite the current configuration.

The path of the configuration file is `/etc/proxysql.cnf`. To configure required configuration items in the preceding sections with the configuration file, the following takes `mysql_servers` and `mysql_users` as an example. To modify other items, refer to the `/etc/proxysql.cnf`.

```
mysql_servers =
(
    {
        address="127.0.0.1"
        port=4000
        hostgroup=0
        max_connections=2000
    }
)

mysql_users:
(
    {
        username = "root"
        password = ""
        default_hostgroup = 0
        max_connections = 1000
        default_schema = "test"
        active = 1
        transaction_persistent = 1
    }
)
```

To make the preceding modifications effective, use the `systemctl restart proxysql` command to restart ProxySQL. Then the SQLite database will be created automatically and the configuration file will not be ignored.

### Other configuration items

The preceding configuration items are required. For optional configuration items, refer to [Global variables](https://proxysql.com/documentation/global-variables/).

## 4. Try out

To quick start the test environment, you can use Docker and Docker Compose. Make sure the ports `4000` and `6033` are not allocated.

```shell
git clone https://github.com/Icemap/tidb-proxysql-integration-test.git
cd tidb-proxysql-integration-test && docker-compose pull # Get the latest Docker images
sudo setenforce 0 # Only on Linux
docker-compose up -d
```

> **Warning:**
>
> **DO NOT** use the preceding commands to create an integration in production environments.

The preceding commands start an environment integrated TiDB with ProxySQL and runs two containers. To log in to the ProxySQL `6033` port, you can use the `root` username with an empty password. For more information about the configuration of containers, see [`docker-compose.yaml`](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/docker-compose.yaml). For more details about the configuration of ProxySQL, see [`proxysql-docker.cnf`](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/proxysql-docker.cnf).

To connect to TiDB, run the following command:

```shell
mysql -u root -h 127.0.0.1 -P 6033 -e "SELECT VERSION()"
```

An example result is as follows:

```sql
+--------------------+
| VERSION()          |
+--------------------+
| 5.7.25-TiDB-v6.1.0 |
+--------------------+
```

## 5. Configuration examples

Dependencies:

- Docker
- Docker Compose
- MySQL Client

Clone the example code repository and change to the sample directory:

```shell
git clone https://github.com/Icemap/tidb-proxysql-integration-test.git
cd tidb-proxysql-integration-test
```

The following sections use `tidb-proxysql-integration-test` as the root directory.

### Use Admin Interface to configure load balancing

Change to the sample directory:

```shell
cd example/load-balance-admin-interface
```

#### Run with a script

To configure load balancing using **_ProxySQL Admin Interface_**, you can run with the `test-load-balance.sh` script using the following command:

```shell
./test-load-balance.sh
```

#### Run step by step

The preceding `test-load-balance.sh` script can be run step by step as follows:

1. Start three TiDB containers and a ProxySQL instance.

    ```shell
    docker-compose up -d
    ```

    - Start three TiDB containers using `docker-compose`. All the ports in the container are `4000` and host ports are `4001`, `4002` and `4003`.
    - After starting TiDB containers, the ProxySQL instance is started. The port of **_ProxySQL MySQL Interface_** in container is `6033` and the host port is `6034`.
    - The port of **_ProxySQL Admin Interface_** is not exposed because it can only be accessed in the container.
    - For more details about the process, refer to [`docker-compose.yaml`](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/example/load-balance-admin-interface/docker-compose.yaml).

2. In the three TiDB containers, create the same table schema with different data (`'tidb-0'`, `'tidb-1'` and `'tidb-2'`) to distinguish TiDB instances.

    ```shell
    mysql -u root -h 127.0.0.1 -P 4001 << EOF
    DROP TABLE IF EXISTS test.test;
    CREATE TABLE test.test (db VARCHAR(255));
    INSERT INTO test.test (db) VALUES ('tidb-0');
    EOF

    mysql -u root -h 127.0.0.1 -P 4002 << EOF
    DROP TABLE IF EXISTS test.test;
    CREATE TABLE test.test (db VARCHAR(255));
    INSERT INTO test.test (db) VALUES ('tidb-1');
    EOF

    mysql -u root -h 127.0.0.1 -P 4003 << EOF
    DROP TABLE IF EXISTS test.test;
    CREATE TABLE test.test (db VARCHAR(255));
    INSERT INTO test.test (db) VALUES ('tidb-2');
    EOF
    ```

3. To execute the [`proxysql-prepare.sql`](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/example/load-balance-admin-interface/proxysql-prepare.sql) in **_ProxySQL Admin Interface_**, execute the `docker-compose exec` command as follows:

    ```shell
    docker-compose exec proxysql sh -c "mysql -uadmin -padmin -h127.0.0.1 -P6032 < ./proxysql-prepare.sql"
    ```

    The preceding SQL file runs and triggers the following operations:

    1. Adds hosts of three TiDB Servers and set all `hostgroup_id` as `0`.
    2. Makes the configuration of TiDb Servers effective and saves it on disk.
    3. Adds a `root` user with an empty password and sets `default_hostgroup` as `0`, corresponding to the preceding `hostgroup_id` of TiDB Servers.
    4. Makes the configuration of the user effective and saves it on disk.

4. Log in to **_ProxySQL MySQL Interface_** with the `root` user and query 5 times using the following statements. The expected output contains `'tidb-0'`, `'tidb-1'`, and `'tidb-2'` three different values.

    ```shell
    mysql -u root -h 127.0.0.1 -P 6034 -t << EOF
    SELECT * FROM test.test;
    SELECT * FROM test.test;
    SELECT * FROM test.test;
    SELECT * FROM test.test;
    SELECT * FROM test.test;
    EOF
    ```

5. To stop and remove containers and networks, you can use the following command:

    ```shell
    docker-compose down
    ```

#### Expected output

There are three different results (`'tidb-0'`, `'tidb-1'`, and `'tidb-2'`) in the expected output, but the exact order cannot be expected. The following is one of the expected outputs:

```
# ./test-load-balance.sh
Creating network "load-balance-admin-interface_default" with the default driver
Creating load-balance-admin-interface_tidb-1_1 ... done
Creating load-balance-admin-interface_tidb-2_1 ... done
Creating load-balance-admin-interface_tidb-0_1 ... done
Creating load-balance-admin-interface_proxysql_1 ... done
+--------+
| db     |
+--------+
| tidb-2 |
+--------+
+--------+
| db     |
+--------+
| tidb-0 |
+--------+
+--------+
| db     |
+--------+
| tidb-1 |
+--------+
+--------+
| db     |
+--------+
| tidb-1 |
+--------+
+--------+
| db     |
+--------+
| tidb-1 |
+--------+
Stopping load-balance-admin-interface_proxysql_1 ... done
Stopping load-balance-admin-interface_tidb-0_1   ... done
Stopping load-balance-admin-interface_tidb-2_1   ... done
Stopping load-balance-admin-interface_tidb-1_1   ... done
Removing load-balance-admin-interface_proxysql_1 ... done
Removing load-balance-admin-interface_tidb-0_1   ... done
Removing load-balance-admin-interface_tidb-2_1   ... done
Removing load-balance-admin-interface_tidb-1_1   ... done
Removing network load-balance-admin-interface_default
```

### Use Admin Interface to configure user split

Change to the sample directory:

```shell
cd example/user-split-admin-interface
```

#### Run with a script

To configure a user split traffic using **_ProxySQL Admin Interface_**, you can run the `test-user-split.sh` script using the following command:

```shell
./test-user-split.sh
```

#### Run step by step

The preceding `test-user-split.sh` script can be run step by step as follows:

1. Start two TiDB containers and a ProxySQL instance.

    ```shell
    docker-compose up -d
    ```

    - Start two TiDB containers using `docker-compose`. All the ports in the container are `4000` and host ports are `4001` and `4002`.
    - After you start TiDB containers, the ProxySQL instance is started. The port of **_ProxySQL MySQL Interface_** in the container is `6033` and the host port is `6034`.
    - The port of **_ProxySQL Admin Interface_** is not exposed because it can only be accessed in the container.
    - For more details about the process, refer to [`docker-compose.yaml`](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/example/user-split-admin-interface/docker-compose.yaml).

2. In the two TiDB containers, create the same table schema with different data (`'tidb-0'` and `'tidb-1'`) to distinguish TiDB instances.

    ```shell
    mysql -u root -h 127.0.0.1 -P 4001 << EOF
    DROP TABLE IF EXISTS test.test;
    CREATE TABLE test.test (db VARCHAR(255));
    INSERT INTO test.test (db) VALUES ('tidb-0');
    EOF

    mysql -u root -h 127.0.0.1 -P 4002 << EOF
    DROP TABLE IF EXISTS test.test;
    CREATE TABLE test.test (db VARCHAR(255));
    INSERT INTO test.test (db) VALUES ('tidb-1');
    EOF
    ```

3. Create a new user for ProxySQL in the `tidb-1` instance:

    ```shell
    mysql -u root -h 127.0.0.1 -P 4002 << EOF
    CREATE USER 'root1' IDENTIFIED BY '';
    GRANT ALL PRIVILEGES ON *.* TO 'root1'@'%';
    FLUSH PRIVILEGES;
    EOF
    ```

4. To execute the [`proxysql-prepare.sql`](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/example/user-split-admin-interface/proxysql-prepare.sql) in **_ProxySQL Admin Interface_**, execute the `docker-compose exec` command as follows:

    ```shell
    docker-compose exec proxysql sh -c "mysql -uadmin -padmin -h127.0.0.1 -P6032 < ./proxysql-prepare.sql"
    ```

    The preceding SQL file runs and triggers the following operations:

    1. Adds hosts of two TiDB Servers. The `hostgroup_id` of `tidb-0` is `0` and `hostgroup_id` of `tidb-1` is `1`.
    2. Makes the configuration of TiDb Servers effective and saves it on disk.
    3. Adds a `root` user with an empty password and sets `default_hostgroup` as `0`. It indicates that the SQL routes to `tidb-0` by default.
    4. Adds a user `root1` with an empty password and sets `default_hostgroup` as `1`. It indicates that the SQL routes to `tidb-1` by default.
    5. Makes the configuration of the user effective and saves it on disk.

5. Log in to **_ProxySQL MySQL Interface_** with the `root` user and `root1` user. The expected output contains `'tidb-0'` and `'tidb-1'` two different values.

    ```shell
    mysql -u root -h 127.0.0.1 -P 6034 -e "SELECT * FROM test.test;"
    mysql -u root1 -h 127.0.0.1 -P 6034 -e "SELECT * FROM test.test;"
    ```

6. To stop and remove containers and networks, you can use the following command:

    ```shell
    docker-compose down
    ```

#### Expected output

The following is one of the expected outputs:

```
# ./test-user-split.sh
Creating network "user-split-admin-interface_default" with the default driver
Creating user-split-admin-interface_tidb-1_1 ... done
Creating user-split-admin-interface_tidb-0_1 ... done
Creating user-split-admin-interface_proxysql_1 ... done
+--------+
| db     |
+--------+
| tidb-0 |
+--------+
+--------+
| db     |
+--------+
| tidb-1 |
+--------+
Stopping user-split-admin-interface_proxysql_1 ... done
Stopping user-split-admin-interface_tidb-0_1   ... done
Stopping user-split-admin-interface_tidb-1_1   ... done
Removing user-split-admin-interface_proxysql_1 ... done
Removing user-split-admin-interface_tidb-0_1   ... done
Removing user-split-admin-interface_tidb-1_1   ... done
Removing network user-split-admin-interface_default
```

### Use Admin Interface to configure proxy rules

Change to the sample directory:

```shell
cd example/proxy-rule-admin-interface
```

#### Run with script

To configure proxy rules to use different TiDB servers for executing read and write SQLs (if not matched, use `default_hostgroup`) using **_ProxySQL Admin Interface_**, you can run `proxy-rule-split.sh` using the following command:

```shell
./proxy-rule-split.sh
```

#### Run step by step

The preceding `proxy-rule-split.sh` script can be run step by step as follows:

1. Start two TiDB containers and a ProxySQL instance.

    ```shell
    docker-compose up -d
    ```

    - Start two TiDB containers using `docker-compose`. All the ports in the container are `4000` and host ports are `4001` and `4002`.
    - After you start TiDB containers, the ProxySQL instance is started. The port of **_ProxySQL MySQL Interface_** in the container is `6033` and the host port is `6034`.
    - The port of **_ProxySQL Admin Interface_** is not exposed because it can only be accessed in the container.
    - For more details about the process, refer to [`docker-compose.yaml`](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/example/proxy-rule-admin-interface/docker-compose.yaml)

2. In the two TiDB containers, create the same table schema with different data (`'tidb-0'` and `'tidb-1'`) to distinguish TiDB instances.

    ```shell
    mysql -u root -h 127.0.0.1 -P 4001 << EOF
    DROP TABLE IF EXISTS test.test;
    CREATE TABLE test.test (db VARCHAR(255));
    INSERT INTO test.test (db) VALUES ('tidb-0');
    EOF

    mysql -u root -h 127.0.0.1 -P 4002 << EOF
    DROP TABLE IF EXISTS test.test;
    CREATE TABLE test.test (db VARCHAR(255));
    INSERT INTO test.test (db) VALUES ('tidb-1');
    EOF
    ```

3. To execute the [`proxysql-prepare.sql`](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/example/proxy-rule-admin-interface/proxysql-prepare.sql) in **_ProxySQL Admin Interface_**, execute the `docker-compose exec` command as follows:

    ```shell
    docker-compose exec proxysql sh -c "mysql -uadmin -padmin -h127.0.0.1 -P6032 < ./proxysql-prepare.sql"
    ```

    The preceding SQL file runs and triggers the following operations:

    1. Adds hosts of two TiDB Servers. The `hostgroup_id` of `tidb-0` is `0` and `hostgroup_id` of `tidb-1` is `1`.
    2. Makes the configuration of TiDB Servers effective and saves it on disk.
    3. Adds a user `root` with an empty password and sets `default_hostgroup` as `0`. It indicates that the SQL routes to `tidb-0` by default.
    4. Makes the configuration of the user effective and save it on disk.
    5. Adds the rule `^SELECT.*FOR UPDATE$` with `rule_id` as `1` and `destination_hostgroup` as `0`. If a SQL statement match this rule, it used the TiDB Server with `hostgroup` as `0` (this rule forwards `SELECT ... FOR UPDATE` to the written database).
    6. Adds the rule `^SELECT` with `rule_id` as `2` and `destination_hostgroup` as `1`. If SQL statements match this rule, it uses the TiDB Server with `hostgroup` as `1`.
    7. Makes the configuration of the rule effective and saves it on disk.

    > **Note:**
    >
    > More details about the matching rules:
    >
    > - ProxySQL tries to match the rules one by one in the order of `rule_id` from smallest to largest.
    > - `^` matches the beginning of a SQL statement and `$` matches the end.
    > - `match_digest` matches the parameterized SQL statement. For more details, see [query_processor_regex](https://proxysql.com/documentation/global-variables/mysql-variables/#mysql-query_processor_regex).
    > - Important parameters:
    >
    >     - `digest`: match the parameterized Hash value.
    >     - `match_pattern`: match the raw SQL statements.
    >     - `negate_match_pattern`: if you set the value to `1`, inverse the match for `match_digest` or `match_pattern`.
    >     - `log`: whether to log the query.
    >     - `replace_pattern`: if it is not empty, this is the pattern with which to replace the matched pattern.
    >
    > - For full parameters, see [mysql_query_rules](https://proxysql.com/documentation/main-runtime/#mysql_query_rules).

4. Log in to **_ProxySQL MySQL Interface_** with the `root` user:

    ```shell
    mysql -u root -h 127.0.0.1 -P 6034
    ```

    You can run the following statements:

    - `SELECT` statement:

        ```sql
        SELECT * FROM test.test;
        ```

        The statement is expected to match rules with `rule_id` of `2` and forward the statement to the TiDB server `tidb-1` with `hostgroup` of `1`.

    - `SELECT ... FOR UPDATE` statement:

        ```sql
        SELECT * FROM test.test for UPDATE;
        ```

        The statement is expected to match rules with `rule_id` of `1` and forward the statement to the TiDB server `tidb-0` with `hostgroup` of `0`.

    - Transaction:

        ```sql
        BEGIN;
        INSERT INTO test.test (db) VALUES ('insert this and rollback later');
        SELECT * FROM test.test;
        ROLLBACK;
        ```

        The `BEGIN` statement is expected to not match all rules. It uses the `default_hostgroup` of the user (It is `0`) and thus forwards to the TiDB server `tidb-0`(`hostgroup` is `0`). And ProxySQL enables user `transaction_persistent` by default, which will cause all statements within the same transaction to run in the same `hostgroup`. So the `INSERT` statement and `SELECT * FROM test.test;` will also be forwarded to the TiDB Server `tidb-0`(`hostgroup` is `0`).

5. To stop and remove containers and networks, you can use the following command:

    ```shell
    docker-compose down
    ```

#### Expected output

```
# ./proxy-rule-split.sh
Creating network "proxy-rule-admin-interface_default" with the default driver
Creating proxy-rule-admin-interface_tidb-1_1 ... done
Creating proxy-rule-admin-interface_tidb-0_1 ... done
Creating proxy-rule-admin-interface_proxysql_1 ... done
+--------+
| db     |
+--------+
| tidb-1 |
+--------+
+--------+
| db     |
+--------+
| tidb-0 |
+--------+
+--------------------------------+
| db                             |
+--------------------------------+
| tidb-0                         |
| insert this and rollback later |
+--------------------------------+
Stopping proxy-rule-admin-interface_proxysql_1 ... done
Stopping proxy-rule-admin-interface_tidb-0_1   ... done
Stopping proxy-rule-admin-interface_tidb-1_1   ... done
Removing proxy-rule-admin-interface_proxysql_1 ... done
Removing proxy-rule-admin-interface_tidb-0_1   ... done
Removing proxy-rule-admin-interface_tidb-1_1   ... done
Removing network proxy-rule-admin-interface_default
```

### Use the configuration file to configure load balancing

To configure load balancing using the configuration file, you can run `test-load-balance.sh` using the following command:

```shell
cd example/load-balance-config-file
./test-load-balance.sh
```

The expected output is the same as that of [Use Admin Interface to configure load balancing](#use-the-configuration-file-to-configure-load-balancing). The only change is using the configuration file to initialize the ProxySQL configuration.

> **Note:**
>
> - The configuration of ProxySQL is stored in SQLite. The configuration file is only used when the SQLite is not created.
> - It is recommended that you use the configuration file only for initialization but not for modifying configuration items, because configuration through the **_ProxySQL Admin Interface_** supports the following features:
>
>     - Input validation.
>     - Remote configuration by any MySQL client.
>     - Runtime configuration for maximum uptime (no need to restart).
>     - Propagation the configuration to other ProxySQL nodes if [ProxySQL Cluster](https://proxysql.com/documentation/proxysql-cluster/) is configured.
