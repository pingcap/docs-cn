---
title: 使用 TiDB Cloud(DevTier) 构建 TiDB 集群
---

# 使用 TiDB Cloud(DevTier) 构建 TiDB 集群

本页将指导您以最快的方式开始使用 TiDB 。您将使用 TiDB Cloud ，创建并启动一个免费的 TiDB 集群，使用 TiDB SQL 客户端，插入数据。随后将从示例程序读取出数据。
若您需要在本地计算机上启动 TiDB，请参阅 [本地启动 TiDB](https://docs.pingcap.com/zh/tidb/stable/quick-start-with-tidb)

## 步骤 1. 创建免费集群

1. 如果你还未拥有 TiDB Cloud 账号，请先在此[注册](https://tidbcloud.com/signup)
2. 使用您的 TiDB Cloud 账号[登录](https://tidbcloud.com/)
3. 在[方案](https://tidbcloud.com/console/plans)内选择一年内免费的 Developer Tier 方案，或直接点击[这里](https://tidbcloud.com/console/create-cluster?tier=dev)，进入 `Create a Cluster (Dev Tier)` 页面
4. 请在 `Create a Cluster (Dev Tier)` 页面填写集群名称/密码/云服务商(暂时仅可选择 AWS)/可用区(建议就近选择)后，点击 `Create` 按钮创建集群。
5. 稍作等待，在 5-15 分钟后，将创建完毕，可在 [Active Clusters](https://tidbcloud.com/console/clusters) 查看创建进度
6. 创建完毕后，在 `Active Clusters` 页面，点击集群名称，进入该集群控制面板

![active clusters](/media/develop/IMG_20220331-232643794.png)

7. 点击 `Connect`，创建流量过滤器（允许连接的客户端 IP 列表）

![connect](/media/develop/IMG_20220331-232726165.png)

8. 在弹出框内点击 `Add Your Current IP Address`， 此项将由 TiDB Cloud 解析你当前的网络 IP 填入。点击 `Create Filter`，进行流量过滤器的创建
9. 复制弹出框 `Step 2: Connect with a SQL client` 中的连接字符串，供后续步骤使用

![SQL string](/media/develop/IMG_20220331-232800929.png)

## 步骤 2. 连接到集群

1. 若未安装 MySQL 客户端，请选择自己的操作系统，按以下步骤安装

<SimpleTab>

<div label="Mac">

如果你没有 homebrew，请移步[官网](https://brew.sh/index_zh-cn)进行安装

```bash
brew install mysql-client
```

在安装完成的命令行输出中，得到以下信息：

```bash
mysql-client is keg-only, which means it was not symlinked into /opt/homebrew,
because it conflicts with mysql (which contains client libraries).

If you need to have mysql-client first in your PATH, run:
  echo 'export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"' >> ~/.zshrc

For compilers to find mysql-client you may need to set:
  export LDFLAGS="-L/opt/homebrew/opt/mysql-client/lib"
  export CPPFLAGS="-I/opt/homebrew/opt/mysql-client/include"
```

请运行其中的此行（命令行输出若与此处文档不一致，请以命令行输出为准）：

```bash
echo 'export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"' >> ~/.zshrc
```

完成后，生效该配置文件(例如 `~/.zshrc`)，并验证 MySQL 客户端是否安装成功：

```bash
source ~/.zshrc
mysql --version
```

预期会得到形如以下的输出：

```bash
mysql  Ver 8.0.28 for macos12.0 on arm64 (Homebrew)
```

</div>

<div label="Linux">

以 CentOS7 为例：

```bash
yum install mysql
```

完成后，请验证 MySQL 客户端是否安装成功：

```bash
mysql --version
```

预期会得到形如以下的输出：

```bash
mysql  Ver 15.1 Distrib 5.5.68-MariaDB, for Linux (x86_64) using readline 5.1
```

</div>

</SimpleTab>

2. 运行步骤 1 中得到的连接字符串

```bash
mysql --connect-timeout 15 -u root -h <host> -P 4000 -p
```

3. 填写密码，完成登录

## 步骤 3. 运行示例应用程序

1. 克隆 tidb-example-java 项目

```bash
git clone https://github.com/pingcap-inc/tidb-example-java.git
```

2. 更改连接参数

### 本地默认集群

无需更改

### 非本地默认集群、TiDB Cloud 或其他远程集群

更改 plain-java-jdbc/src/main/java/com/pingcap/JDBCExample.java 内关于 Host / Post / User / Password 的参数：

```java
mysqlDataSource.setServerName("localhost");
mysqlDataSource.setPortNumber(4000);
mysqlDataSource.setDatabaseName("test");
mysqlDataSource.setUser("root");
mysqlDataSource.setPassword("");
```

若你设定的密码为 `123456`，在 TiDB Cloud 得到的连接字符串为：

```java
mysql --connect-timeout 15 -u root -h tidb.e049234d.d40d1f8b.us-east-1.prod.aws.tidbcloud.com -P 4000 -p
```

那么此处应将参数更改为：

```java
mysqlDataSource.setServerName("tidb.e049234d.d40d1f8b.us-east-1.prod.aws.tidbcloud.com");
mysqlDataSource.setPortNumber(4000);
mysqlDataSource.setDatabaseName("test");
mysqlDataSource.setUser("root");
mysqlDataSource.setPassword("123456");
```

3. 运行 `make plain-java-jdbc`

输出应如[预期](https://github.com/pingcap-inc/tidb-example-java/blob/main/Expected-Output.md#plain-java-jdbc)所示
