---
title: 使用 Django 构建 TiDB 应用程序
summary: 给出一个 Django 构建 TiDB 应用程序示例。
---

<!-- markdownlint-disable MD029 -->

# 使用 Django 构建 TiDB 应用程序

本教程向你展示如何使用 TiDB 构建 [Django](https://www.djangoproject.com/) Web 应用程序。使用 [django-tidb](https://github.com/pingcap/django-tidb) 模块作为数据访问能力的框架。此示例应用程序的代码仓库可在 [Github](https://github.com/pingcap-inc/tidb-example-python) 下载。

这是一个较为完整的构建 Restful API 的示例应用程序，展示了一个使用 **TiDB** 作为数据库的通用 **Django** 后端服务。设计了以下过程，用于还原一个现实场景：

这是一个关于游戏的例子，每个玩家有两个属性：金币数 `coins` 和货物数 `goods`。且每个玩家都拥有一个字段 `id`，作为玩家的唯一标识。玩家在金币数和货物数充足的情况下，可以自由的交易。

你可以以此示例为基础，构建自己的应用程序。

> **建议：**
>
> 在[云原生开发环境](/develop/dev-guide-playground-gitpod.md)中尝试 Django 构建 TiDB 应用程序。
> 预配置完成的环境，自动启动 TiDB 集群，获取和运行代码，只需要一个链接。
>
> [现在就试试](https://gitpod.io/#/https://github.com/pingcap-inc/tidb-example-python)

## 第 1 步：启动你的 TiDB 集群

本节将介绍 TiDB 集群的启动方法。

### 使用 TiDB Cloud Serverless Tier 集群

[创建 Serverless Tier 集群](/develop/dev-guide-build-cluster-in-cloud.md#第-1-步创建-serverless-tier-集群)

### 使用本地集群

此处将简要叙述启动一个测试集群的过程，若需查看正式环境集群部署，或查看更详细的部署内容，请查阅[本地启动 TiDB](/quick-start-with-tidb.md)。

**部署本地测试集群**

适用场景：利用本地 macOS 或者单机 Linux 环境快速部署 TiDB 测试集群，体验 TiDB 集群的基本架构，以及 TiDB、TiKV、PD、监控等基础组件的运行

1. 下载并安装 TiUP。

    {{< copyable "shell-regular" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2. 声明全局环境变量。

    > **注意：**
    >
    > TiUP 安装完成后会提示对应 profile 文件的绝对路径。在执行以下 source 命令前，需要根据 profile 文件的实际位置修改命令。

    {{< copyable "shell-regular" >}}

    ```shell
    source .bash_profile
    ```

3. 在当前 session 执行以下命令启动集群。

    - 直接执行`tiup playground` 命令会运行最新版本的 TiDB 集群，其中 TiDB、TiKV、PD 和 TiFlash 实例各 1 个：

        {{< copyable "shell-regular" >}}

        ```shell
        tiup playground
        ```

    - 也可以指定 TiDB 版本以及各组件实例个数，命令类似于：

        {{< copyable "shell-regular" >}}

        ```shell
        tiup playground v5.4.0 --db 2 --pd 3 --kv 3
        ```

    上述命令会在本地下载并启动某个版本的集群（例如 v5.4.0）。最新版本可以通过执行`tiup list tidb` 来查看。运行结果将显示集群的访问方式：

    ```
    CLUSTER START SUCCESSFULLY, Enjoy it ^-^
    To connect TiDB: mysql --comments --host 127.0.0.1 --port 4001 -u root -p (no password)
    To connect TiDB: mysql --comments --host 127.0.0.1 --port 4000 -u root -p (no password)
    To view the dashboard: http://127.0.0.1:2379/dashboard
    PD client endpoints: [127.0.0.1:2379 127.0.0.1:2382 127.0.0.1:2384]
    To view the Prometheus: http://127.0.0.1:9090
    To view the Grafana: http://127.0.0.1:3000
    ```

> **注意：**
>
> - 支持 v5.2.0 及以上版本的 TiDB 在 Apple M1 芯片的机器上运行 `tiup playground`。
> - 以这种方式执行的 playground，在结束部署测试后 TiUP 会清理掉原集群数据，重新执行该命令后会得到一个全新的集群。
> - 若希望持久化数据，可以执行 TiUP 的 `--tag` 参数：`tiup --tag <your-tag> playground ...`，详情参考 [TiUP 参考手册](/tiup/tiup-reference.md#-t---tag-string)。

## 第 2 步：安装 Python

请在你的计算机上下载并安装 **Python**。我们将使用 **[Django 3.2.16](https://github.com/pingcap-inc/tidb-example-python/blob/main/requirement.txt#L2)** 版本完成此示例，依照 [Django 文档](https://docs.djangoproject.com/en/4.1/faq/install/#what-python-version-can-i-use-with-django)，其在 3.2.16 版本中支持版本为 **3.6, 3.7, 3.8, 3.9, 3.10 (added in 3.2.9)** 的 Python 环境，推荐使用 Python 3.10 版本 。

## 第 3 步：获取应用程序代码

请下载或克隆[示例代码库](https://github.com/pingcap-inc/tidb-example-python)，并进入到目录`django_example`中。

### 创建相同依赖空白程序（可选）

本程序使用 **django-admin** 构建。你可以安装并使用这个 CLI 工具来快速完成 Django 项目的初始化。如你需要快速得到一个与 **django_example** 示例程序相同依赖的可运行空白应用程序，你可以跟随如下步骤：

1. 初始化

    ```bash
    pip install -r requirement.txt
    django-admin startproject copy_django_example
    cd copy_django_example
    ```

2. 更改配置

    1. 请进入当前文件夹内 `copy_django_example/settings.py`.
    2. 请更改 `DATABASES` 部分内容：

        从原本指向本地的 SQLite 的配置：

        ```python
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
        ```

        更改为：

        ```python
        DATABASES = {
            'default': {
                'ENGINE': 'django_tidb',
                'NAME': 'django',
                'USER': 'root',
                'PASSWORD': '',
                'HOST': '127.0.0.1',
                'PORT': 4000,
            },
        }
        DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
        ```

    3. 此外，我们不需要跨域校验，请将 `MIDDLEWARE` 中的 `CsrfViewMiddleware` 进行注释或删除：

        即，将：

        ```python
        MIDDLEWARE = [
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ]
        ```

        改为：

        ```python
        MIDDLEWARE = [
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            # 'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ]
        ```

至此，你已经完成了一个空白的应用程序，此应用程序与示例应用程序的依赖完全相同。其他关于 Django 的使用方法，可参考：

- [Django 文档（中文版）](https://docs.djangoproject.com/zh-hans/3.2/)
- [Django 入门 Tutorial（中文版）](https://docs.djangoproject.com/zh-hans/3.2/intro/tutorial01/)

## 第 4 步：运行应用程序

此处对应用程序代码进行运行，将产生一个 Web 应用程序。你可以在使用 `python manage.py migrate` 命令，要求 Django 创建一个在数据库 `django` 内的表 `player`。如果你想应用程序的 Restful API 进行请求，这些请求将会在 TiDB 集群上运行[数据库事务](/develop/dev-guide-transaction-overview.md)。

如果你想了解有关此应用程序的代码的详细信息，可参阅本教程下方的[实现细节](#实现细节)。

### 第 4 步第 1 部分：TiDB Cloud 更改参数

若你使用 TiDB Cloud Serverless Tier 集群，更改 `settings.py`（位于 `example_project` 内）关于 `DATABASES` 的参数：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django_tidb',
        'NAME': 'django',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': 4000,
    },
}
```

若你设定的密码为 `123456`，而且从 TiDB Cloud Serverless Tier 集群面板中得到的连接信息为：

- Endpoint: `xxx.tidbcloud.com`
- Port: `4000`
- User: `2aEp24QWEDLqRFs.root`

另外，由于 TiDB Cloud Serverless Tier 需要使用 SSL 连接。因此，CA 证书路径是必要的。你可以在 [Where is the CA root path on my system?](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-tier-clusters#where-is-the-ca-root-path-on-my-system) 一节中得到建议。

此处将以 MacOS 为例，应将参数更改为：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django_tidb',
        'NAME': 'django',
        'USER': '2aEp24QWEDLqRFs.root',
        'PASSWORD': '123456',
        'HOST': 'xxx.tidbcloud.com',
        'PORT': 4000,
        'OPTIONS': {
            'ssl': {
                "ca": "/etc/ssl/cert.pem"
            },
        },
    },
}
```

### 第 4 步第 2 部分：运行

打开终端，确保你已经进入 tidb-example-python 目录，若还未在此目录，请使用命令进入：

{{< copyable "shell-regular" >}}

```shell
cd <path>/tidb-example-python
```

#### 安装依赖并进入目录

```bash
pip install -r requirement.txt
cd django_example
```

#### 运行数据库迁移

这将在你连接的数据库内生成 Django 所需的相应数据表。

```bash
python3 manage.py migrate
```

#### 运行应用程序

```bash
python manage.py runserver
```

### 第 4 步第 3 部分：输出

输出的最后部分应如下所示：

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
December 12, 2022 - 08:21:50
Django version 3.2.16, using settings 'example_project.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

如果你想了解有关此应用程序的代码的详细信息，可参阅本教程下方的[实现细节](#实现细节)。

## 第 5 步：HTTP 请求

服务完成运行后，即可使用 HTTP 接口请求后端程序。`http://localhost:8000` 是服务提供根地址。此处使用一系列的 HTTP 请求来演示如何使用该服务。

### 第 6 步第 1 部分：使用 Postman 请求(推荐)

你可下载[此配置文件](https://raw.githubusercontent.com/pingcap-inc/tidb-example-python/main/django_example/Player.postman_collection.json)到本地，并导入 [Postman](https://www.postman.com/)，导入后如图所示：

![postman import](/media/develop/IMG_20220402-003303222.png)

#### 增加玩家

点击 **Create** 标签，点击 **Send** 按钮，发送 Post 形式的 `http://localhost:8000/player/` 请求。返回值为增加的玩家个数，预期为 1。

#### 使用 ID 获取玩家信息

点击 **GetByID** 标签，点击 **Send** 按钮，发送 Get 形式的 `http://localhost:8000/player/1` 请求。返回值为 ID 为 1 的玩家信息。

#### 使用 Limit 批量获取玩家信息

点击 **GetByLimit** 标签，点击 **Send** 按钮，发送 Get 形式的 `http://localhost:8000/player/limit/3` 请求。返回值为最多 3 个玩家的信息列表。

#### 分页获取玩家信息

点击 **GetByPage** 标签，点击 **Send** 按钮，发送 Get 形式的 `http://localhost:8000/player/page?index=0&size=2` 请求。返回值为 index 为 0 的页，每页有 2 个玩家信息列表。此外，还包含了分页信息，如偏移量、总页数、是否排序等。

#### 获取玩家个数

点击 **Count** 标签，点击 **Send** 按钮，发送 Get 形式的 `http://localhost:8000/player/count` 请求。返回值为玩家个数。

#### 玩家交易

点击 **Trade** 标签，点击 **Send** 按钮，发送 Put 形式的 `http://localhost:8000/player/trade` 请求，请求参数为售卖玩家 ID `sellID`、购买玩家 ID `buyID`、购买货物数量 `amount`、购买消耗金币数 `price`。返回值为交易是否成功。当出现售卖玩家货物不足、购买玩家金币不足或数据库错误时，交易将不成功，且由于[数据库事务](/develop/dev-guide-transaction-overview.md)保证，不会有玩家的金币或货物丢失的情况。

### 第 6 步第 2 部分：使用 curl 请求

当然，你也可以直接使用 curl 进行请求。

#### 增加玩家

使用 **Post** 方法请求 `/player` 端点请求来增加玩家，即：

{{< copyable "shell-regular" >}}

```shell
curl --location --request POST 'http://localhost:8000/player/' --header 'Content-Type: application/json' --data-raw '[{"coins":100,"goods":20}]'
```

这里使用 JSON 作为信息的载荷。表示需要创建一个金币数 `coins` 为 100，货物数 `goods` 为 20 的玩家。返回值为创建的玩家个数。

```json
1
```

#### 使用 ID 获取玩家信息

使用 **Get** 方法请求 `/player` 端点请求来获取玩家信息，额外的需要在路径上给出玩家的 `id` 参数，即 `/player/{id}` ，例如在请求 `id` 为 1 的玩家时：

{{< copyable "shell-regular" >}}

```shell
curl --location --request GET 'http://localhost:8000/player/1'
```

返回值为玩家的信息：

```json
{
  "coins": 200,
  "goods": 10,
  "id": 1
}
```

#### 使用 Limit 批量获取玩家信息

使用 **Get** 方法请求 `/player/limit` 端点请求来获取玩家信息，额外的需要在路径上给出限制查询的玩家信息的总数，即 `/player/limit/{limit}` ，例如在请求最多 3 个玩家的信息时：

{{< copyable "shell-regular" >}}

```shell
curl --location --request GET 'http://localhost:8000/player/limit/3'
```

返回值为玩家信息的列表：

```json
[
  {
    "coins": 200,
    "goods": 10,
    "id": 1
  },
  {
    "coins": 0,
    "goods": 30,
    "id": 2
  },
  {
    "coins": 100,
    "goods": 20,
    "id": 3
  }
]
```

#### 分页获取玩家信息

使用 **Get** 方法请求 `/player/page` 端点请求来分页获取玩家信息，额外的需要使用 URL 参数 ，例如在请求页面序号 `index` 为 0，每页最大请求量 `size` 为 2 时：

{{< copyable "shell-regular" >}}

```shell
curl --location --request GET 'http://localhost:8000/player/page?index=0&size=2'
```

返回值为 `index` 为 0 的页，每页有 2 个玩家信息列表。此外，还包含了分页信息，如偏移量、总页数、是否排序等。

```json
{
  "content": [
    {
      "coins": 200,
      "goods": 10,
      "id": 1
    },
    {
      "coins": 0,
      "goods": 30,
      "id": 2
    }
  ],
  "empty": false,
  "first": true,
  "last": false,
  "number": 0,
  "numberOfElements": 2,
  "pageable": {
    "offset": 0,
    "pageNumber": 0,
    "pageSize": 2,
    "paged": true,
    "sort": {
      "empty": true,
      "sorted": false,
      "unsorted": true
    },
    "unpaged": false
  },
  "size": 2,
  "sort": {
    "empty": true,
    "sorted": false,
    "unsorted": true
  },
  "totalElements": 4,
  "totalPages": 2
}
```

#### 获取玩家个数

使用 **Get** 方法请求 `/player/count` 端点请求来获取玩家个数：

{{< copyable "shell-regular" >}}

```shell
curl --location --request GET 'http://localhost:8000/player/count'
```

返回值为玩家个数

```json
4
```

#### 玩家交易

使用 **Put** 方法请求 `/player/trade` 端点请求来发起玩家间的交易，即：

{{< copyable "shell-regular" >}}

```shell
curl --location --request PUT 'http://localhost:8000/player/trade' \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'sellID=1' \
  --data-urlencode 'buyID=2' \
  --data-urlencode 'amount=10' \
  --data-urlencode 'price=100'
```

这里使用 **Form Data** 作为信息的载荷。表示售卖玩家 ID `sellID` 为 1、购买玩家 ID `buyID` 为 2、购买货物数量 `amount` 为 10、购买消耗金币数 `price` 为 100。返回值为交易是否成功。当出现售卖玩家货物不足、购买玩家金币不足或数据库错误时，交易将不成功，且由于[数据库事务](/develop/dev-guide-transaction-overview.md)保证，不会有玩家的金币或货物丢失的情况。

```json
true
```

### 第 6 步第 3 部分：使用 Shell 脚本请求

这里已经将请求过程编写为 [Shell](https://github.com/pingcap-inc/tidb-example-java/blob/main/spring-jpa-hibernate/request.sh) 脚本，以方便大家的测试，脚本将会做以下操作：

1. 循环创建 10 名玩家
2. 获取 `id` 为 1 的玩家信息
3. 获取至多 3 名玩家信息列表
4. 获取 `index` 为 0 ，`size` 为 2 的一页玩家信息
5. 获取玩家总数
6. `id` 为 1 的玩家作为售出方，id 为 2 的玩家作为购买方，购买 10 个货物，耗费 100 金币

你可以使用 `make request` 或 `./request.sh` 命令运行此脚本，结果应如下所示：

```
> make request
./request.sh
loop to create 10 players:
1111111111

get player 1:
{"id":1,"coins":200,"goods":10}

get players by limit 3:
[{"id":1,"coins":200,"goods":10},{"id":2,"coins":0,"goods":30},{"id":3,"coins":100,"goods":20}]

get first players:
{"content":[{"id":1,"coins":200,"goods":10},{"id":2,"coins":0,"goods":30}],"pageable":{"sort":{"empty":true,"unsorted":true,"sorted":false},"offset":0,"pageNumber":0,"pageSize":2,"paged":true,"unpaged":false},"last":false,"totalPages":7,"totalElements":14,"first":true,"size":2,"number":0,"sort":{"empty":true,"unsorted":true,"sorted":false},"numberOfElements":2,"empty":false}

get players count:
14

trade by two players:
false
```

## 实现细节

本小节介绍示例应用程序项目中的组件。

### 总览

本示例项目的大致目录树如下所示（删除了有碍理解的部分）：

```
.
├── pom.xml
└── src
    └── main
        ├── java
        │   └── com
        │       └── pingcap
        │           ├── App.java
        │           ├── controller
        │           │   └── PlayerController.java
        │           ├── dao
        │           │   ├── PlayerBean.java
        │           │   └── PlayerRepository.java
        │           └── service
        │               ├── PlayerService.java
        │               └── impl
        │                   └── PlayerServiceImpl.java
        └── resources
            └── application.yml
```

其中：

- `pom.xml` 内声明了项目的 Maven 配置，如依赖，打包等
- `application.yml` 内声明了项目的用户配置，如数据库地址、密码、使用的数据库方言等
- `App.java` 是项目的入口
- `controller` 是项目对外暴露 HTTP 接口的包
- `service` 是项目实现接口与逻辑的包
- `dao` 是项目实现与数据库连接并完成数据持久化的包

### 配置

本节将简要介绍 `pom.xml` 文件中的 Maven 配置，及 `application.yml` 文件中的用户配置。

#### Maven 配置

`pom.xml` 文件为 Maven 配置，在文件内声明了项目的 Maven 依赖，打包方法，打包信息等，你可以通过[创建相同依赖空白程序](#创建相同依赖空白程序可选) 这一节来复刻此配置文件的生成流程，当然，也可直接复制至你的项目来使用。

{{< copyable "" >}}

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
   <modelVersion>4.0.0</modelVersion>
   <parent>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-parent</artifactId>
      <version>3.0.0-M1</version>
      <relativePath/> <!-- lookup parent from repository -->
   </parent>

   <groupId>com.pingcap</groupId>
   <artifactId>spring-jpa-hibernate</artifactId>
   <version>0.0.1</version>
   <name>spring-jpa-hibernate</name>
   <description>an example for spring boot, jpa, hibernate and TiDB</description>

   <properties>
      <java.version>17</java.version>
      <maven.compiler.source>17</maven.compiler.source>
      <maven.compiler.target>17</maven.compiler.target>
   </properties>

   <dependencies>
      <dependency>
         <groupId>org.springframework.boot</groupId>
         <artifactId>spring-boot-starter-data-jpa</artifactId>
         <exclusions>
            <exclusion>
               <groupId>org.hibernate</groupId>
               <artifactId>hibernate-core-jakarta</artifactId>
            </exclusion>
         </exclusions>
      </dependency>

      <dependency>
         <groupId>org.springframework.boot</groupId>
         <artifactId>spring-boot-starter-web</artifactId>
      </dependency>

      <dependency>
         <groupId>mysql</groupId>
         <artifactId>mysql-connector-java</artifactId>
         <scope>runtime</scope>
      </dependency>

      <dependency>
         <groupId>org.springframework.boot</groupId>
         <artifactId>spring-boot-starter-test</artifactId>
         <scope>test</scope>
      </dependency>

      <dependency>
         <groupId>org.hibernate.orm</groupId>
         <artifactId>hibernate-core</artifactId>
         <version>6.0.0.CR2</version>
      </dependency>
   </dependencies>

   <build>
      <plugins>
         <plugin>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-maven-plugin</artifactId>
         </plugin>
      </plugins>
   </build>

   <repositories>
      <repository>
         <id>spring-milestones</id>
         <name>Spring Milestones</name>
         <url>https://repo.spring.io/milestone</url>
         <snapshots>
            <enabled>false</enabled>
         </snapshots>
      </repository>
   </repositories>
   <pluginRepositories>
      <pluginRepository>
         <id>spring-milestones</id>
         <name>Spring Milestones</name>
         <url>https://repo.spring.io/milestone</url>
         <snapshots>
            <enabled>false</enabled>
         </snapshots>
      </pluginRepository>
   </pluginRepositories>
</project>
```

#### 用户配置

`application.yml` 此配置文件声明了用户配置，如数据库地址、密码、使用的数据库方言等。

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:4000/test
    username: root
    #    password: xxx
    driver-class-name: com.mysql.cj.jdbc.Driver
  jpa:
    show-sql: true
    database-platform: org.hibernate.dialect.TiDBDialect
    hibernate:
      ddl-auto: create-drop
```

此配置格式为 [YAML](https://yaml.org/) 格式。其中：

- `spring.datasource.url` : 数据库连接的 URL。
- `spring.datasource.url` : 数据库用户名。
- `spring.datasource.password` : 数据库密码，此项为空，需注释或删除。
- `spring.datasource.driver-class-name` : 数据库驱动，因为 TiDB 与 MySQL 兼容，则此处使用与 mysql-connector-java 适配的驱动类 `com.mysql.cj.jdbc.Driver`。
- `jpa.show-sql` : 为 true 时将打印 JPA 运行的 SQL。
- `jpa.database-platform` : 选用的数据库方言，此处连接了 TiDB，自然选择 TiDB 方言，注意，此方言在 6.0.0.Beta2 版本后的 Hibernate 中才可选择，请注意依赖版本。
- `jpa.hibernate.ddl-auto` : 此处选择的 create-drop 将会在程序开始时创建表，退出时删除表。请勿在正式环境使用，但此处为示例程序，希望尽量不影响数据库数据，因此选择了此选项。

### 入口文件

入口文件 `App.java`：

{{< copyable "" >}}

```java
package com.pingcap;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.ApplicationPidFileWriter;

@SpringBootApplication
public class App {
   public static void main(String[] args) {
      SpringApplication springApplication = new SpringApplication(App.class);
      springApplication.addListeners(new ApplicationPidFileWriter("spring-jpa-hibernate.pid"));
      springApplication.run(args);
   }
}
```

入口类比较简单，首先，有一个 Spring Boot 应用程序的标准配置注解 [@SpringBootApplication](https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/autoconfigure/SpringBootApplication.html)。有关详细信息，请参阅 Spring Boot 官方文档中的 [Using the @SpringBootApplication Annotation](https://docs.spring.io/spring-boot/docs/current/reference/html/using-spring-boot.html#using-boot-using-springbootapplication-annotation) 。随后，使用 `ApplicationPidFileWriter` 在程序启动过程中，写下一个名为 `spring-jpa-hibernate.pid` 的 PID (process identification number) 文件，可从外部使用此 PID 文件关闭此应用程序。

### 数据库持久层

数据库持久层，即 `dao` 包内，实现了数据对象的持久化。

#### 实体对象

`PlayerBean.java` 文件为实体对象，这个对象对应了数据库的一张表。

{{< copyable "" >}}

```java
package com.pingcap.dao;

import jakarta.persistence.*;

/**
 * it's core entity in hibernate
 * @Table appoint to table name
 */
@Entity
@Table(name = "player_jpa")
public class PlayerBean {
    /**
     * @ID primary key
     * @GeneratedValue generated way. this field will use generator named "player_id"
     * @SequenceGenerator using `sequence` feature to create a generator,
     *    and it named "player_jpa_id_seq" in database, initial form 1 (by `initialValue`
     *    parameter default), and every operator will increase 1 (by `allocationSize`)
     */
    @Id
    @GeneratedValue(generator="player_id")
    @SequenceGenerator(name="player_id", sequenceName="player_jpa_id_seq", allocationSize=1)
    private Long id;

    /**
     * @Column field
     */
    @Column(name = "coins")
    private Integer coins;
    @Column(name = "goods")
    private Integer goods;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Integer getCoins() {
        return coins;
    }

    public void setCoins(Integer coins) {
        this.coins = coins;
    }

    public Integer getGoods() {
        return goods;
    }

    public void setGoods(Integer goods) {
        this.goods = goods;
    }
}
```

这里可以看到，实体类中有很多注解，这些注解给了 Hibernate 额外的信息，用以绑定实体类和表：

- `@Entity` 声明 `PlayerBean` 是一个实体类。
- `@Table` 使用注解属性 `name` 将此实体类和表 `player_jpa` 关联。
- `@Id` 声明此属性关联表的主键列。
- `@GeneratedValue` 表示自动生成该列的值，而不应手动设置，使用属性 `generator` 指定生成器的名称为 `player_id`。
- `@SequenceGenerator` 声明一个使用[序列](/sql-statements/sql-statement-create-sequence.md)的生成器，使用注解属性 `name` 声明生成器的名称为 `player_id` （与 `@GeneratedValue` 中指定的名称需保持一致）。随后使用注解属性 `sequenceName` 指定数据库中序列的名称。最后，使用注解属性 `allocationSize` 声明序列的步长为 1。
- `@Column` 将每个私有属性声明为表 `player_jpa` 的一列，使用注解属性 `name` 确定属性对应的列名。

#### 存储库

为了抽象数据库层，Spring 应用程序使用 [Repository](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/#repositories) 接口，或者 Repository 的子接口。 这个接口映射到一个数据库对象，常见的，比如会映射到一个表上。JPA 会实现一些预制的方法，比如 [INSERT](/sql-statements/sql-statement-insert.md) ，或使用主键的 [SELECT](/sql-statements/sql-statement-select.md) 等。

{{< copyable "" >}}

```java
package com.pingcap.dao;

import jakarta.persistence.LockModeType;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Lock;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface PlayerRepository extends JpaRepository<PlayerBean, Long> {
    /**
     * use HQL to query by page
     * @param pageable a pageable parameter required by hibernate
     * @return player list package by page message
     */
    @Query(value = "SELECT player_jpa FROM PlayerBean player_jpa")
    Page<PlayerBean> getPlayersByPage(Pageable pageable);

    /**
     * use SQL to query by limit, using named parameter
     * @param limit sql parameter
     * @return player list (max size by limit)
     */
    @Query(value = "SELECT * FROM player_jpa LIMIT :limit", nativeQuery = true)
    List<PlayerBean> getPlayersByLimit(@Param("limit") Integer limit);

    /**
     * query player and add a lock for update
     * @param id player id
     * @return player
     */
    @Lock(value = LockModeType.PESSIMISTIC_WRITE)
    @Query(value = "SELECT player FROM PlayerBean player WHERE player.id = :id")
    // @Query(value = "SELECT * FROM player_jpa WHERE id = :id FOR UPDATE", nativeQuery = true)
    PlayerBean getPlayerAndLock(@Param("id") Long id);
}
```

`PlayerRepository` 拓展了 Spring 用于 JPA 数据访问所使用的接口 `JpaRepository`。使用 `@Query` 注解，告诉 Hibernate 此接口如何实现查询。在此处使用了两种查询语句的语法，其中，在接口 `getPlayersByPage` 中的查询语句使用的是一种被 Hibernate 称为 [HQL](https://docs.jboss.org/hibernate/orm/6.0/userguide/html_single/Hibernate_User_Guide.html#hql) (Hibernate Query Language) 的语法。而接口 `getPlayersByLimit` 中使用的是普通的 SQL，在使用 SQL 语法时，需要将 `@Query` 的注解参数 `nativeQuery` 设置为 true。

在 `getPlayersByLimit` 注解的 SQL 中，`:limit` 在 Hibernate 中被称为[命名参数](https://docs.jboss.org/hibernate/orm/6.0/userguide/html_single/Hibernate_User_Guide.html#jpql-query-parameters)，Hibernate 将按名称自动寻找并拼接注解所在接口内的参数。你也可以使用 `@Param` 来指定与参数不同的名称用于注入。

在 `getPlayerAndLock` 中，使用了一个注解 [@Lock](https://docs.spring.io/spring-data/jpa/docs/current/api/org/springframework/data/jpa/repository/Lock.html)，此注解声明此处使用悲观锁进行锁定，如需了解更多其他锁定方式，可查看[实体锁定](https://openjpa.apache.org/builds/2.2.2/apache-openjpa/docs/jpa_overview_em_locking.html)文档。此处的 `@Lock` 仅可与 HQL 搭配使用，否则将会产生错误。当然，如果你希望直接使用 SQL 进行锁定，可直接使用注释部分的注解：

{{< copyable "" >}}

```java
@Query(value = "SELECT * FROM player_jpa WHERE id = :id FOR UPDATE", nativeQuery = true)
```

直接使用 SQL 的 `FOR UPDATE` 来增加锁。你也可通过 TiDB [SELECT 文档](/sql-statements/sql-statement-select.md) 进行更深层次的原理学习。

### 逻辑实现

逻辑实现层，即 `service` 包，内含了项目实现的接口与逻辑

#### 接口

`PlayerService.java` 文件内定义了逻辑接口，实现接口，而不是直接编写一个类的原因，是尽量使例子贴近实际使用，体现设计的开闭原则。你也可以省略掉此接口，在依赖类中直接注入实现类，但并不推荐这样做。

{{< copyable "" >}}

```java
package com.pingcap.service;

import com.pingcap.dao.PlayerBean;
import org.springframework.data.domain.Page;

import java.util.List;

public interface PlayerService {
    /**
     * create players by passing in a List of PlayerBean
     *
     * @param players will create players list
     * @return The number of create accounts
     */
    Integer createPlayers(List<PlayerBean> players);

    /**
     * buy goods and transfer funds between one player and another in one transaction
     * @param sellId sell player id
     * @param buyId buy player id
     * @param amount goods amount, if sell player has not enough goods, the trade will break
     * @param price price should pay, if buy player has not enough coins, the trade will break
     */
    void buyGoods(Long sellId, Long buyId, Integer amount, Integer price) throws RuntimeException;

    /**
     * get the player info by id.
     *
     * @param id player id
     * @return the player of this id
     */
    PlayerBean getPlayerByID(Long id);

    /**
     * get a subset of players from the data store by limit.
     *
     * @param limit return max size
     * @return player list
     */
    List<PlayerBean> getPlayers(Integer limit);

    /**
     * get a page of players from the data store.
     *
     * @param index page index
     * @param size page size
     * @return player list
     */
    Page<PlayerBean> getPlayersByPage(Integer index, Integer size);

    /**
     * count players from the data store.
     *
     * @return all players count
     */
    Long countPlayers();
}
```

#### 实现 (重要)

`PlayerService.java` 文件内实现了 `PlayerService` 接口，所有数据操作逻辑都编写在这里。

{{< copyable "" >}}

```java
package com.pingcap.service.impl;

import com.pingcap.dao.PlayerBean;
import com.pingcap.dao.PlayerRepository;
import com.pingcap.service.PlayerService;
import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * PlayerServiceImpl implements PlayerService interface
 * @Transactional it means every method in this class, will package by a pair of
 *     transaction.begin() and transaction.commit(). and it will be call
 *     transaction.rollback() when method throw an exception
 */
@Service
@Transactional
public class PlayerServiceImpl implements PlayerService {
    @Autowired
    private PlayerRepository playerRepository;

    @Override
    public Integer createPlayers(List<PlayerBean> players) {
        return playerRepository.saveAll(players).size();
    }

    @Override
    public void buyGoods(Long sellId, Long buyId, Integer amount, Integer price) throws RuntimeException {
        PlayerBean buyPlayer = playerRepository.getPlayerAndLock(buyId);
        PlayerBean sellPlayer = playerRepository.getPlayerAndLock(sellId);
        if (buyPlayer == null || sellPlayer == null) {
            throw new RuntimeException("sell or buy player not exist");
        }

        if (buyPlayer.getCoins() < price || sellPlayer.getGoods() < amount) {
            throw new RuntimeException("coins or goods not enough, rollback");
        }

        buyPlayer.setGoods(buyPlayer.getGoods() + amount);
        buyPlayer.setCoins(buyPlayer.getCoins() - price);
        playerRepository.save(buyPlayer);

        sellPlayer.setGoods(sellPlayer.getGoods() - amount);
        sellPlayer.setCoins(sellPlayer.getCoins() + price);
        playerRepository.save(sellPlayer);
    }

    @Override
    public PlayerBean getPlayerByID(Long id) {
        return playerRepository.findById(id).orElse(null);
    }

    @Override
    public List<PlayerBean> getPlayers(Integer limit) {
        return playerRepository.getPlayersByLimit(limit);
    }

    @Override
    public Page<PlayerBean> getPlayersByPage(Integer index, Integer size) {
        return playerRepository.getPlayersByPage(PageRequest.of(index, size));
    }

    @Override
    public Long countPlayers() {
        return playerRepository.count();
    }
}
```

这里使用了 `@Service` 这个注解，声明此对象的生命周期交由 Spring 管理。

注意，除了有 `@Service` 注解之外，PlayerServiceImpl 实现类还有一个 [@Transactional](https://docs.spring.io/spring-framework/docs/current/reference/html/data-access.html#transaction-declarative-annotations) 注解。当在应用程序中启用事务管理时 (可使用 [@EnableTransactionManagement](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/transaction/annotation/EnableTransactionManagement.html) 打开，但 Spring Boot 默认开启，无需再次手动配置)，Spring 会自动将所有带有 `@Transactional` 注释的对象包装在一个代理中，使用该代理对对象的调用进行处理。

你可以简单的认为，代理在带有 `@Transactional` 注释的对象内的函数调用时：在函数顶部将使用 `transaction.begin()` 开启事务，函数返回后，调用 `transaction.commit()` 进行事务提交，而出现任何运行时错误时，代理将会调用 `transaction.rollback()` 来回滚。

你可参阅[数据库事务](/develop/dev-guide-transaction-overview.md)来获取更多有关事务的信息，或者阅读 Spring 官网中的文章 [理解 Spring 框架的声明式事务实现](https://docs.spring.io/spring-framework/docs/current/reference/html/data-access.html#tx-decl-explained)。

整个实现类中，`buyGoods` 函数需重点关注，其在不符合逻辑时将抛出异常，引导 Hibernate 进行事务回滚，防止出现错误数据。

### 外部接口

`controller` 包对外暴露 HTTP 接口，可以通过 [REST API](https://www.redhat.com/en/topics/api/what-is-a-rest-api#) 来访问服务。

{{< copyable "" >}}

```java
package com.pingcap.controller;

import com.pingcap.dao.PlayerBean;
import com.pingcap.service.PlayerService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.lang.NonNull;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/player")
public class PlayerController {
    @Autowired
    private PlayerService playerService;

    @PostMapping
    public Integer createPlayer(@RequestBody @NonNull List<PlayerBean> playerList) {
        return playerService.createPlayers(playerList);
    }

    @GetMapping("/{id}")
    public PlayerBean getPlayerByID(@PathVariable Long id) {
        return playerService.getPlayerByID(id);
    }

    @GetMapping("/limit/{limit_size}")
    public List<PlayerBean> getPlayerByLimit(@PathVariable("limit_size") Integer limit) {
        return playerService.getPlayers(limit);
    }

    @GetMapping("/page")
    public Page<PlayerBean> getPlayerByPage(@RequestParam Integer index, @RequestParam("size") Integer size) {
        return playerService.getPlayersByPage(index, size);
    }

    @GetMapping("/count")
    public Long getPlayersCount() {
        return playerService.countPlayers();
    }

    @PutMapping("/trade")
    public Boolean trade(@RequestParam Long sellID, @RequestParam Long buyID, @RequestParam Integer amount, @RequestParam Integer price) {
        try {
            playerService.buyGoods(sellID, buyID, amount, price);
        } catch (RuntimeException e) {
            return false;
        }

        return true;
    }
}
```

`PlayerController` 中使用了尽可能多的注解方式来作为示例展示功能，在实际项目中，请尽量保持风格的统一，同时遵循你公司或团体的规则。`PlayerController` 有许多注解，下方将进行逐一解释：

- [@RestController](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/RestController.html) 将 `PlayerController` 声明为一个 [Web Controller](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller)，且将返回值序列化为 JSON 输出。
- [@RequestMapping](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/RequestMapping.html) 映射 URL 端点为 `/player` ，即此 `Web Controller` 仅监听 `/player` URL 下的请求。
- `@Autowired` 用于 Spring 的自动装配，可以看到，此处声明需要一个 `PlayerService` 对象，此对象为接口，并未指定使用哪一个实现类，这是由 Spring 自动装配的，有关此装配规则，可查看 Spirng 官网中的 [The IoC container](https://docs.spring.io/spring-framework/docs/3.2.x/spring-framework-reference/html/beans.html) 一文。
- [@PostMapping](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/PostMapping.html) 声明此函数将响应 HTTP 中的 [POST](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST) 类型请求。
    - `@RequestBody` 声明此处将 HTTP 的整个载荷解析到参数 `playerList` 中。
    - `@NonNull` 声明参数不可为空，否则将校验并返回错误。
- [@GetMapping](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/GetMapping.html) 声明此函数将响应 HTTP 中的 [GET](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET) 类型请求。
    - [@PathVariable](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/PathVariable.html) 可以看到注解中有形如 `{id}` 、`{limit_size}` 这样的占位符，这种占位符将被绑定到 `@PathVariable` 注释的变量中，绑定的依据是注解中的注解属性 `name` （变量名可省略，即 `@PathVariable(name="limit_size")` 可写成 `@PathVariable("limit_size")` ），不特殊指定时，与变量名名称相同。
- [@PutMapping](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/PutMapping.html) 声明此函数将响应 HTTP 中的 [PUT](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT) 类型请求。
- [@RequestParam](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/RequestParam.html) 此声明将解析请求中的 URL 参数、表单参数等参数，绑定至注解的变量中。
