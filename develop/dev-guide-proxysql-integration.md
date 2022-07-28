---
title: TiDB 与 ProxySQL 集成方案
summary: 叙述 TiDB 与 ProxySQL 集成方案。
---

# TiDB 与 ProxySQL 集成方案

此文档以 CentOS 7 为例，简单介绍 **_TiDB_** 与 **_ProxySQL_** 的集成方法，如果你有其他系统的集成需求，可查看[快速体验](#4-快速体验)一节，这是使用 Docker 及 Docker Compose 部署测试集成环境的介绍。你也可以自行参阅以下链接，以获得更多信息：

- [TiDB 文档](/overview.md)
- [TiDB 开发者文档](/develop/dev-guide-overview.md)
- [ProxySQL 官方文档](https://proxysql.com/documentation/)
- [TiDB 与 ProxySQL 的集成测试](https://github.com/Icemap/tidb-proxysql-integration-test)

## 1. 启动 TiDB

### 1.1 测试环境 - 源码编译启动

1. 下载 [TiDB](https://github.com/pingcap/tidb) 源码，进入 `tidb-server` 目录后，进行编译。

    ```sh
    git clone git@github.com:pingcap/tidb.git
    cd tidb/tidb-server
    go build
    ```

2. 随后，你可以使用配置文件 [tidb-config.toml](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/tidb-config.toml) 来启动 TiDB。注意:

    - 此处使用 `unistore` 作为存储引擎，这是 TiDB 的测试存储引擎，请仅在测试时使用它。
    - `TIDB_SERVER_PATH`: 上一步中，使用 `go build` 编译的二进制文件位置，如你在 `/usr/local` 下进行上一步操作，那么此处的 `TIDB_SERVER_PATH` 应为：`/usr/local/tidb/tidb-server/tidb-server`
    - `LOCAL_TIDB_LOG`: 输出 TiDB 日志的位置

    ```sh
    ${TIDB_SERVER_PATH} -config ./tidb-config.toml -store unistore -path "" -lease 0s > ${LOCAL_TIDB_LOG} 2>&1 &
    ```

### 1.2 测试环境 - TiUP 启动

[TiUP](/tiup/tiup-overview.md) 在 TiDB 中承担着包管理器的角色，管理着 TiDB 生态下众多的组件，如 TiDB、PD、TiKV 等。

1. 安装 TiUP

    ```sh
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2. 启动测试环境 TiDB

    ```sh
    tiup playground
    ```

### 1.3 测试环境 - TiDB Cloud Developer Tier

请参考 [使用 TiDB Cloud (DevTier) 构建 TiDB 集群](/develop/dev-guide-build-cluster-in-cloud.md)。

### 1.4 正式环境 - TiDB Cloud

在需要托管 TiDB 服务的前提下（如无法自行运维，或需要云原生环境等），我们建议直接使用 TiDB Cloud。你可以查看 [TiDB Cloud 的 Create a TiDB Cluster 文档](https://docs.pingcap.com/tidbcloud/create-tidb-cluster)，用以在 TiDB Cloud 中部署正式环境下的 TiDB。

### 1.5 正式环境 - 本地安装

正式环境相对测试环境会复杂许多，建议详阅[使用 TiUP 部署 TiDB 集群](/production-deployment-using-tiup.md)一文，后根据硬件条件部署。

## 2. 启动 ProxySQL

### 2.1 yum 安装

1. 添加 RPM 仓库：

    ```sh
    cat > /etc/yum.repos.d/proxysql.repo << EOF
    [proxysql]
    name=ProxySQL YUM repository
    baseurl=https://repo.proxysql.com/ProxySQL/proxysql-2.4.x/centos/\$releasever
    gpgcheck=1
    gpgkey=https://repo.proxysql.com/ProxySQL/proxysql-2.4.x/repo_pub_key
    EOF
    ```

2. 安装：

    ```sh
    yum install proxysql
    ```

3. 启动：

    ```sh
    systemctl start proxysql
    ```

### 2.2 其他安装

请参阅 ProxySQL 的 [Github 页面](https://github.com/sysown/proxysql#installation)或[官方文档](https://proxysql.com/documentation/)进行安装。

## 3. 配置 ProxySQL

我们需要将 ProxySQL 内的配置指向 TiDB，以此将 ProxySQL 作为 TiDB 的代理。此处将列举必需的配置项，其余配置项可参考 ProxySQL [官方文档](https://proxysql.com/documentation/)。

### 3.1 ProxySQL 配置的简单介绍

ProxySQL 使用一个单独的端口进行配置管理，另一个端口进行代理。我们把配置管理的入口，称为 **_ProxySQL Admin interface_**，把代理的入口，称为 **_ProxySQL MySQL interface_**。

- **_ProxySQL Admin interface_**: 可以使用具有 `admin` 权限的用户连接到管理界面，以读取和写入配置，或者使用具有 `stats` 权限的用户，只能读取某些统计数据（不读取或写入配置）。默认凭证是 `admin:admin` 和 `stats:stats`，但出于安全考虑，可以使用默认凭证进行本地连接。要远程连接，需要配置一个新的用户，通常它被命名为 `radmin`。
- **_ProxySQL MySQL interface_**: 用于代理，将 SQL 转发到配置的服务中。

![proxysql config flow](/media/develop/proxysql_config_flow.png)

ProxySQL 有三层配置：`runtime`、`memory`、`disk`。你仅能更改 `memory` 层的配置。在更改配置后，可以使用 `load xxx to runtime` 来生效这个配置，也可以使用 `save xxx to disk` 落盘，防止配置丢失。

![proxysql config layer](/media/develop/proxysql_config_layer.png)

### 3.2 配置 TiDB 后端

在 ProxySQL 中添加 TiDB 后端，此处如果有多个 TiDB 后端，可以添加多条。请在 **_ProxySQL Admin interface_** 进行此操作：

```sql
insert into mysql_servers(hostgroup_id,hostname,port) values(0,'127.0.0.1',4000);
load mysql servers to runtime;
save mysql servers to disk;
```

字段解释：

- `hostgroup_id`: ProxySQL 是以 **hostgroup** 为单位管理后端服务的，可以将需要负载均衡的几个服务配置为同一个 hostgroup，这样 ProxySQL 将均匀的分发 SQL 到这些服务上。而在需要区分不同后端服务时（如读写分离场景等），可将其配置为不同的 hostgroup，以此配置不同的代理条件。
- `hostname`: 后端服务的 IP 或域名。
- `port`: 后端服务的端口。

### 3.3 配置 Proxy 登录账号

在 ProxySQL 中添加 TiDB 后端的登录账号。ProxySQL 将允许此账号来登录 **_ProxySQL MySQL interface_**，而且 ProxySQL 将以此创建与 TiDB 之间的连接，因此，请确保此账号在 TiDB 中拥有相应权限。请在 **_ProxySQL Admin interface_** 进行此操作：

```sql
insert into mysql_users(username,password,active,default_hostgroup,transaction_persistent) values('root','',1,0,1);
load mysql users to runtime;
save mysql users to disk;
```

字段解释：

- `username`: 用户名
- `password`: 密码
- `active`: 是否生效，`1` 为生效，`0` 为不生效，仅 `active = 1` 的用户可登录。
- `default_hostgroup`: 此账号默认使用的 **hostgroup**，SQL 将被发送至此 **hostgroup** 中，除非查询规则将流量发送到不同的 **hostgroup**。
- `transaction_persistent`: 值为 `1` 时，表示事务持久化，即：当某连接使用该用户开启了一个事务后，那么在事务提交或回滚之前，
所有的语句都路由到同一个 **hostgroup** 中，避免语句分散到不同 **hostgroup**。

### 3.4 配置文件配置

除了使用 **_ProxySQL Admin interface_** 配置，也可以使用配置文件进行配置。[官方解释](https://github.com/sysown/proxysql#configuring-proxysql-through-the-config-file)中，配置文件仅应该被视为是一种辅助初始化的方式，而并非主要配置的手段。配置文件仅在 SQLite 数据库未被创建时读取，后续将不会继续读取配置文件。因此，使用配置文件配置时，你应进行 SQLite 数据库的删除，这将***丢失***你在 **_ProxySQL Admin interface_** 中对配置进行的更改：

```sh
rm /var/lib/proxysql/proxysql.db
```

另外，也可以运行`LOAD xxx FROM CONFIG`，用配置文件中的配置覆盖当前内存中的配置。

配置文件的位置为 `/etc/proxysql.cnf`，我们将上方的必需配置翻译为配置文件方式，仅更改 `mysql_servers`、`mysql_users` 这两个配置节点，其余配置可自行查看 `/etc/proxysql.cnf`：

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

随后使用 `systemctl restart proxysql` 进行服务重启后即可生效，配置生效后将自动创建 SQLite 数据库，后续将不会再次读取配置文件。

### 3.5 其余配置项

仅以上配置为必需配置项，其余配置项并非必需。你可在 ProxySQL 文档中的 [Global Variables](https://proxysql.com/documentation/global-variables/) 一文中获取全部配置项名称及其作用。

## 4. 快速体验

你可以使用 Docker 及 Docker Compose 快速进行集成后的环境体验，请确认 `4000`、`6033` 端口的空闲：

```sh
docker-compose up -d
```

这样就已经完成了一个集成了 TiDB 与 ProxySQL 环境的启动，这将启动两个容器，***请勿***在生产环境使用此快速体验方式创建集成。你可以使用用户名`root`，密码为空的账号，登录到本机的 `6033` 端口 (ProxySQL)。容器具体配置可见 [docker-compose.yaml](/docker-compose.yaml)，ProxySQL 具体配置可见 [proxysql-docker.cnf](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/proxysql-docker.cnf)。

## 5. 使用

### 5.1 MySQL Client 连接 ProxySQL

可运行:

```sh
mysql -u root -h 127.0.0.1 -P 6033 -e "SELECT VERSION()"
```

运行结果:

```sql
+--------------------+
| VERSION()          |
+--------------------+
| 5.7.25-TiDB-v6.1.0 |
+--------------------+
```

### 5.2 运行集成测试

如果你满足以下依赖项：

- 测试用例代码仓库 [tidb-test](https://github.com/pingcap/tidb-test) 的权限
- 测试机器需连接网络
- Golang SDK
- Git
- 以下两者其一：
    1. 本地启动

        - CentOS 7 机器（可为实体机或虚拟机）
        - Yum
        
    2. Docker 启动

        - Docker
        - Docker Compose

那么你可以本地运行 `./proxysql-initial.sh && ./test-local.sh` 或使用 Docker 运行 `./test-docker.sh` 来运行集成测试。

在[集成测试文档](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/README-zh.md)中有更多信息可供查看。

### 5.3 配置负载均衡示例 - 使用 Admin Interface 进行配置

#### 5.3.1 示例操作步骤

以 **_ProxySQL Admin Interface_** 为配置入口，配置负载均衡场景为例。示例将进行以下操作：

1. 通过 Docker Compose 启动三个 TiDB 容器实例，容器内部端口均为 4000，映射宿主机端口为 4001、4002、4003。
2. 通过 Docker Compose 启动一个 ProxySQL 实例，容器内部 **_ProxySQL MySQL Interface_** 端口为 6033，映射宿主机端口为 6034。不暴露 **_ProxySQL Admin Interface_** 端口，因为其仅可在本地（即容器内）登录 **_ProxySQL Admin Interface_**。
3. 在 3 个 TiDB 实例内，创建相同的表结构，但写入不同的数据：`'tidb-0'`、`'tidb-1'`、`'tidb-2'`，以便分辨不同的数据库实例。
4. 使用 `docker-compose exec` 命令，在 **_ProxySQL Admin Interface_** 中运行事先准备好的配置 ProxySQL 的 SQL 文件，此 SQL 文件将会运行：

    1. 添加 3 个 TiDB 后端的地址，并且 `hostgroup_id` 均为 `0`。
    2. 生效 TiDB 后端配置，并落盘保存。
    3. 添加用户 `root`，密码为空，`default_hostgroup` 为 `0`，对应上方的 TiDB 后端 `hostgroup_id`。
    4. 生效用户配置，并落盘保存。

5. 使用 `root` 用户登录 **_ProxySQL MySQL Interface_**，连续查询 5 次数据，预期结果将有 `'tidb-0'`、`'tidb-1'`、`'tidb-2'` 三种不同的返回。
6. 停止并清除 Docker Compose 启动的容器、网络拓扑等资源。

#### 5.3.2 示例运行

依赖：

- Docker
- Docker Compose
- MySQL Client

```sh
cd example/load-balance-admin-interface/
./test-load-balance.sh
```

#### 5.3.3 预期输出

因为负载均衡的原因，预期输出将有 `'tidb-0'`、`'tidb-1'`、`'tidb-2'` 三种不同的返回。但具体顺序未知。其中一种预期输出为：

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

### 5.4 配置用户分离 - 使用 Admin Interface 进行配置

#### 5.4.1 示例操作步骤

以 **_ProxySQL Admin Interface_** 为配置入口，配置负载均衡配置用户分离场景为例，不同用户将使用不同的 TiDB 后端。示例将进行以下操作：

1. 通过 Docker Compose 启动两个 TiDB 容器实例，容器内部端口均为 4000，映射宿主机端口为 4001、4002。
2. 通过 Docker Compose 启动一个 ProxySQL 实例，容器内部 **_ProxySQL MySQL Interface_** 端口为 6033，映射宿主机端口为 6034。不暴露 **_ProxySQL Admin Interface_** 端口，因为其仅可在本地（即容器内）登录 **_ProxySQL Admin Interface_**。
3. 在 2 个 TiDB 实例内，创建相同的表结构，但写入不同的数据：`'tidb-0'`、`'tidb-1'`，以便分辨不同的数据库实例。
4. 使用 `docker-compose exec` 命令，在 **_ProxySQL Admin Interface_** 中运行事先准备好的配置 ProxySQL 的 SQL 文件，此 SQL 文件将会运行：

    1. 添加 2 个 TiDB 后端的地址，其中，`tidb-0` 的`hostgroup_id` 为 `0`，`tidb-1` 的`hostgroup_id` 为 `1`。
    2. 生效 TiDB 后端配置，并落盘保存。
    3. 添加用户 `root`，密码为空，`default_hostgroup` 为 `0`，即默认将路由至 `tidb-0`。
    4. 添加用户 `root1`，密码为空，`default_hostgroup` 为 `1`，即默认将路由至 `tidb-1`。
    5. 生效用户配置，并落盘保存。

5. 分别使用 `root` 用户及 `root1` 用户登录 **_ProxySQL MySQL Interface_**，预期结果将为 `'tidb-0'`、`'tidb-1'`。
6. 停止并清除 Docker Compose 启动的容器、网络拓扑等资源。

#### 5.4.2 示例运行

依赖：

- Docker
- Docker Compose
- MySQL Client

```sh
cd example/user-split-admin-interface/
./test-user-split.sh
```

#### 5.4.3 预期输出

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

### 5.5 配置代理规则 - 使用 Admin Interface 进行配置

#### 5.5.1 示例操作步骤

以 **_ProxySQL Admin Interface_** 为配置入口，代理规则场景中，常见的读写分离配置为例，将使用规则匹配将要运行的 SQL，从而将读、写 SQL 转发至不同的 TiDB 后端（若均未匹配，则使用用户的 `default_hostgroup`）。示例将进行以下操作：

1. 通过 Docker Compose 启动两个 TiDB 容器实例，容器内部端口均为 4000，映射宿主机端口为 4001、4002。
2. 通过 Docker Compose 启动一个 ProxySQL 实例，容器内部 **_ProxySQL MySQL Interface_** 端口为 6033，映射宿主机端口为 6034。不暴露 **_ProxySQL Admin Interface_** 端口，因为其仅可在本地（即容器内）登录 **_ProxySQL Admin Interface_**。
3. 在 2 个 TiDB 实例内，创建相同的表结构，但写入不同的数据：`'tidb-0'`、`'tidb-1'`，以便分辨不同的数据库实例。
4. 使用 `docker-compose exec` 命令，在 **_ProxySQL Admin Interface_** 中运行事先准备好的配置 ProxySQL 的 SQL 文件，此 SQL 文件将会运行：

    1. 添加 2 个 TiDB 后端的地址，其中，`tidb-0` 的`hostgroup_id` 为 `0`，`tidb-1` 的`hostgroup_id` 为 `1`。
    2. 生效 TiDB 后端配置，并落盘保存。
    3. 添加用户 `root`，密码为空，`default_hostgroup` 为 `0`，即默认将路由至 `tidb-0`。
    4. 生效用户配置，并落盘保存。
    5. 添加规则 `^SELECT.*FOR UPDATE$`，`rule_id`  为 `1`，`destination_hostgroup` 为 `0`，即匹配此规则的 SQL 语句将被转发至 `hostgroup` 为 `0` 的 TiDB 中（这条规则是为了将 `SELECT ... FOR UPDATE` 语句转发至写的数据库中）。
    6. 添加规则 `^SELECT`，`rule_id`  为 `2`，`destination_hostgroup` 为 `1`，即匹配此规则的 SQL 语句将被转发至 `hostgroup` 为 `1` 的 TiDB 中。
    7. 生效规则配置，并落盘保存。

    > **Note:**
    > 
    > 关于匹配规则：
    > 
    > - ProxySQL 将按照 `rule_id` 从小到大的顺序逐一尝试匹配规则。
    > - `^` 匹配 SQL 语句的开头，`$` 匹配 SQL 语句的结尾。
    > - 此处使用的 `match_digest` 进行匹配，用于匹配参数化后的 SQL 语句，语法见 [query_processor_regex](https://proxysql.com/documentation/global-variables/mysql-variables/#mysql-query_processor_regex)。
    > - 重要参数： 
    > 
    >     - `digest`: 用于匹配参数化后的 Hash 值。
    >     - `match_pattern`: 用于匹配原始 SQL 语句。
    >     - `negate_match_pattern`: 设置为 1 时，对 `match_digest` 或 `match_pattern` 匹配取反。
    >     - `log`: 将记录查询日志。
    >     - `replace_pattern`: 将匹配到的内容，替换为此字段的值，如为空，则不做替换。
    > 
    > - 完整参数，请见 [mysql_query_rules](https://proxysql.com/documentation/main-runtime/#mysql_query_rules)。

5. 使用 `root` 用户登录 **_ProxySQL MySQL Interface_**，运行以下语句：
    - `select * from test.test;`: 预计匹配 `rule_id`  为 `2` 的规则，从而转发至 `hostgroup` 为 `1` 的 TiDB 后端 `tidb-1` 中。
    - `select * from test.test for update;`: 预计匹配 `rule_id`  为 `1` 的规则，从而转发至 `hostgroup` 为 `0` 的 TiDB 后端 `tidb-0` 中。
    - `begin;insert into test.test (db) values ('insert this and rollback later'); select * from test.test; rollback;`: `insert` 语句预计不会匹配所有规则，因此将使用用户的 `default_hostgroup`（为 `0`），从而转发至 `hostgroup` 为 `0` 的 TiDB 后端 `tidb-0` 中。而因为 ProxySQL 默认开启用户的 `transaction_persistent`，这将使同一个事务内的所有语句运行在同一个 `hostgroup` 中，因此，这里的 `select * from test.test;` 也将转发至 `hostgroup` 为 `0` 的 TiDB 后端 `tidb-0` 中。
6. 停止并清除 Docker Compose 启动的容器、网络拓扑等资源。

#### 5.5.2 示例运行

依赖：

- Docker
- Docker Compose
- MySQL Client

```sh
cd example/proxy-rule-admin-interface/
./proxy-rule-split.sh
```

#### 5.5.3 预期输出

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

### 5.6 配置负载均衡示例 - 使用配置文件进行配置

以配置文件为配置入口，配置负载均衡场景为例。此配置实现效果与 [5.3 配置负载均衡示例 - 使用 Admin Interface 进行配置](#53-配置负载均衡示例---使用-admin-interface-进行配置)完全一致，仅改为使用配置文件进行 ProxySQL 初始化配置。

> **Note:**
>
> - ProxySQL 的配置保存在 SQLite 中。配置文件仅在 SQLite 不存在时读取。
> - ProxySQL 不建议使用配置文件进行配置更改，仅作为初始化配置时使用，请勿过度依赖配置文件。

**运行**

```sh
cd example/load-balance-config-file/
./test-load-balance.sh
```