---
title: 将 TiDB Cloud 与 dbt 集成
summary: 了解 dbt 在 TiDB Cloud 中的使用场景。
---

# 将 TiDB Cloud 与 dbt 集成

[数据构建工具 (dbt)](https://www.getdbt.com/) 是一个流行的开源数据转换工具，可帮助分析工程师通过 SQL 语句转换其数据仓库中的数据。通过 [dbt-tidb](https://github.com/pingcap/dbt-tidb) 插件，使用 TiDB Cloud 的分析工程师可以直接通过 SQL 创建表单和匹配数据，而无需考虑创建表或视图的过程。

本文档介绍如何将 dbt 与 TiDB Cloud 一起使用，以一个 dbt 项目为例。

## 步骤 1：安装 dbt 和 dbt-tidb

您可以使用一个命令安装 dbt 和 dbt-tidb。在以下命令中，当您安装 dbt-tidb 时，dbt 会作为依赖项安装。

```shell
pip install dbt-tidb
```

您也可以单独安装 dbt。请参阅 dbt 文档中的[如何安装 dbt](https://docs.getdbt.com/docs/get-started/installation)。

## 步骤 2：创建演示项目

要试用 dbt 功能，您可以使用 dbt-lab 提供的演示项目 [jaffle_shop](https://github.com/dbt-labs/jaffle_shop)。您可以直接从 GitHub 克隆该项目：

```shell
git clone https://github.com/dbt-labs/jaffle_shop && \
cd jaffle_shop
```

`jaffle_shop` 目录中的所有文件结构如下：

```shell
.
├── LICENSE
├── README.md
├── dbt_project.yml
├── etc
│    ├── dbdiagram_definition.txt
│    └── jaffle_shop_erd.png
├── models
│    ├── customers.sql
│    ├── docs.md
│    ├── orders.sql
│    ├── overview.md
│    ├── schema.yml
│    └── staging
│        ├── schema.yml
│        ├── stg_customers.sql
│        ├── stg_orders.sql
│        └── stg_payments.sql
└── seeds
    ├── raw_customers.csv
    ├── raw_orders.csv
    └── raw_payments.csv
```

在此目录中：

- `dbt_project.yml` 是 dbt 项目配置文件，其中包含项目名称和数据库配置文件信息。

- `models` 目录包含项目的 SQL 模型和表结构。请注意，这部分由数据分析师编写。有关模型的更多信息，请参阅 [SQL 模型](https://docs.getdbt.com/docs/build/sql-models)。

- `seeds` 目录存储由数据库导出工具导出的 CSV 文件。例如，您可以通过 Dumpling [导出 TiDB Cloud 数据](https://docs.pingcap.com/tidbcloud/export-data-from-tidb-cloud)到 CSV 文件。在 `jaffle_shop` 项目中，这些 CSV 文件用作要处理的原始数据。

## 步骤 3：配置项目

要配置项目，请执行以下步骤：

1. 完成全局配置。

    您可以参考[配置字段说明](#配置字段说明)并编辑默认的全局配置文件 `~/.dbt/profiles.yml` 来配置与 TiDB Cloud 的连接：

    ```shell
    sudo vi ~/.dbt/profiles.yml
    ```

    在编辑器中，添加以下配置：

   ```yaml
    jaffle_shop_tidb:                                                 # 项目名称
      target: dev                                                     # 目标
      outputs:
        dev:
          type: tidb                                                  # 要使用的特定适配器
          server: gateway01.ap-southeast-1.prod.aws.tidbcloud.com     # 要连接的 TiDB Cloud 集群的端点
          port: 4000                                                  # 要使用的端口
          schema: analytics                                           # 指定要将数据规范化到的架构（数据库）
          username: xxxxxxxxxxx.root                                  # 用于连接 TiDB Cloud 集群的用户名
          password: "your_password"                                   # 用于向 TiDB Cloud 集群进行身份验证的密码
    ```

    您可以从集群的连接对话框中获取 `server`、`port` 和 `username` 的值。要打开此对话框，请转到项目的[**集群**](https://tidbcloud.com/project/clusters)页面，点击目标集群的名称以进入其概览页面，然后点击右上角的**连接**。

2. 完成项目配置。

    在 jaffle_shop 项目目录中，编辑项目配置文件 `dbt_project.yml` 并将 `profile` 字段更改为 `jaffle_shop_tidb`。此配置允许项目从 `~/.dbt/profiles.yml` 文件中指定的数据库进行查询。

    ```shell
    vi dbt_project.yml
    ```

    在编辑器中，更新配置如下：

    ```yaml
    name: 'jaffle_shop'

    config-version: 2
    version: '0.1'

    profile: 'jaffle_shop_tidb'                   # 注意此处的修改

    model-paths: ["models"]                       # 模型路径
    seed-paths: ["seeds"]                         # seed 路径
    test-paths: ["tests"]
    analysis-paths: ["analysis"]
    macro-paths: ["macros"]

    target-path: "target"
    clean-targets:
        - "target"
        - "dbt_modules"
        - "logs"

    require-dbt-version: [">=1.0.0", "<2.0.0"]

    models:
      jaffle_shop:
          materialized: table            # models/ 中的 *.sql 将实体化为表
          staging:
            materialized: view           # models/staging/ 中的 *.sql 将实体化为视图
    ```

3. 验证配置。

    运行以下命令以检查数据库和项目配置是否正确。

    ```shell
    dbt debug
    ```

## 步骤 4：（可选）加载 CSV 文件

> **注意：**
>
> 此步骤是可选的。如果要处理的数据已经在目标数据库中，您可以跳过此步骤。

现在您已成功创建并配置了项目，是时候加载 CSV 数据并将 CSV 实体化为目标数据库中的表了。

1. 加载 CSV 数据并将 CSV 实体化为目标数据库中的表。

    ```shell
    dbt seed
    ```

    以下是示例输出：

    ```shell
    Running with dbt=1.0.1
    Partial parse save file not found. Starting full parse.
    Found 5 models, 20 tests, 0 snapshots, 0 analyses, 172 macros, 0 operations, 3 seed files, 0 sources, 0 exposures, 0 metrics

    Concurrency: 1 threads (target='dev')

    1 of 3 START seed file analytics.raw_customers.................................. [RUN]
    1 of 3 OK loaded seed file analytics.raw_customers.............................. [INSERT 100 in 0.19s]
    2 of 3 START seed file analytics.raw_orders..................................... [RUN]
    2 of 3 OK loaded seed file analytics.raw_orders................................. [INSERT 99 in 0.14s]
    3 of 3 START seed file analytics.raw_payments................................... [RUN]
    3 of 3 OK loaded seed file analytics.raw_payments............................... [INSERT 113 in 0.24s]
    ```

    从结果中可以看到，seed 文件已启动并加载到三个表中：`analytics.raw_customers`、`analytics.raw_orders` 和 `analytics.raw_payments`。

2. 在 TiDB Cloud 中验证结果。

    `show databases` 命令列出了 dbt 创建的新 `analytics` 数据库。`show tables` 命令表明 `analytics` 数据库中有三个表，对应于您创建的表。

    ```sql
    mysql> SHOW DATABASES;
    +--------------------+
    | Database           |
    +--------------------+
    | INFORMATION_SCHEMA |
    | METRICS_SCHEMA     |
    | PERFORMANCE_SCHEMA |
    | analytics          |
    | io_replicate       |
    | mysql              |
    | test               |
    +--------------------+
    7 rows in set (0.00 sec)

    mysql> USE ANALYTICS;
    mysql> SHOW TABLES;
    +---------------------+
    | Tables_in_analytics |
    +---------------------+
    | raw_customers       |
    | raw_orders          |
    | raw_payments        |
    +---------------------+
    3 rows in set (0.00 sec)

    mysql> SELECT * FROM raw_customers LIMIT 10;
    +------+------------+-----------+
    | id   | first_name | last_name |
    +------+------------+-----------+
    |    1 | Michael    | P.        |
    |    2 | Shawn      | M.        |
    |    3 | Kathleen   | P.        |
    |    4 | Jimmy      | C.        |
    |    5 | Katherine  | R.        |
    |    6 | Sarah      | R.        |
    |    7 | Martin     | M.        |
    |    8 | Frank      | R.        |
    |    9 | Jennifer   | F.        |
    |   10 | Henry      | W.        |
    +------+------------+-----------+
    10 rows in set (0.10 sec)
    ```

## 步骤 5：转换数据

现在您已准备好运行配置的项目并完成数据转换。

1. 运行 dbt 项目以完成数据转换：

    ```shell
    dbt run
    ```

    以下是示例输出：

    ```shell
    Running with dbt=1.0.1
    Found 5 models, 20 tests, 0 snapshots, 0 analyses, 170 macros, 0 operations, 3 seed files, 0 sources, 0 exposures, 0 metrics

    Concurrency: 1 threads (target='dev')

    1 of 5 START view model analytics.stg_customers................................. [RUN]
    1 of 5 OK created view model analytics.stg_customers............................ [SUCCESS 0 in 0.31s]
    2 of 5 START view model analytics.stg_orders.................................... [RUN]
    2 of 5 OK created view model analytics.stg_orders............................... [SUCCESS 0 in 0.23s]
    3 of 5 START view model analytics.stg_payments.................................. [RUN]
    3 of 5 OK created view model analytics.stg_payments............................. [SUCCESS 0 in 0.29s]
    4 of 5 START table model analytics.customers.................................... [RUN]
    4 of 5 OK created table model analytics.customers............................... [SUCCESS 0 in 0.76s]
    5 of 5 START table model analytics.orders....................................... [RUN]
    5 of 5 OK created table model analytics.orders.................................. [SUCCESS 0 in 0.63s]

    Finished running 3 view models, 2 table models in 2.27s.

    Completed successfully

    Done. PASS=5 WARN=0 ERROR=0 SKIP=0 TOTAL=5
    ```

    结果显示已成功创建两个表（`analytics.customers` 和 `analytics.orders`）和三个视图（`analytics.stg_customers`、`analytics.stg_orders` 和 `analytics.stg_payments`）。

2. 转到 TiDB Cloud 验证转换是否成功。

    ```sql
    mysql> USE ANALYTICS;
    mysql> SHOW TABLES;
    +---------------------+
    | Tables_in_analytics |
    +---------------------+
    | customers           |
    | orders              |
    | raw_customers       |
    | raw_orders          |
    | raw_payments        |
    | stg_customers       |
    | stg_orders          |
    | stg_payments        |
    +---------------------+
    8 rows in set (0.00 sec)

    mysql> SELECT * FROM customers LIMIT 10;
    +-------------+------------+-----------+-------------+-------------------+------------------+-------------------------+
    | customer_id | first_name | last_name | first_order | most_recent_order | number_of_orders | customer_lifetime_value |
    +-------------+------------+-----------+-------------+-------------------+------------------+-------------------------+
    |           1 | Michael    | P.        | 2018-01-01  | 2018-02-10        |                2 |                 33.0000 |
    |           2 | Shawn      | M.        | 2018-01-11  | 2018-01-11        |                1 |                 23.0000 |
    |           3 | Kathleen   | P.        | 2018-01-02  | 2018-03-11        |                3 |                 65.0000 |
    |           4 | Jimmy      | C.        | NULL        | NULL              |             NULL |                    NULL |
    |           5 | Katherine  | R.        | NULL        | NULL              |             NULL |                    NULL |
    |           6 | Sarah      | R.        | 2018-02-19  | 2018-02-19        |                1 |                  8.0000 |
    |           7 | Martin     | M.        | 2018-01-14  | 2018-01-14        |                1 |                 26.0000 |
    |           8 | Frank      | R.        | 2018-01-29  | 2018-03-12        |                2 |                 45.0000 |
    |           9 | Jennifer   | F.        | 2018-03-17  | 2018-03-17        |                1 |                 30.0000 |
    |          10 | Henry      | W.        | NULL        | NULL              |             NULL |                    NULL |
    +-------------+------------+-----------+-------------+-------------------+------------------+-------------------------+
    10 rows in set (0.00 sec)
    ```

    输出显示已添加了五个表或视图，并且表或视图中的数据已转换。本示例中仅显示了客户表中的部分数据。

## 步骤 6：生成文档

dbt 允许您生成显示项目整体结构并描述所有表和视图的可视化文档。

要生成可视化文档，请执行以下步骤：

1. 生成文档：

    ```shell
    dbt docs generate
    ```

2. 启动服务器：

    ```shell
    dbt docs serve
    ```

3. 要从浏览器访问文档，请转到 [http://localhost:8080](http://localhost:8080)。

## 配置字段说明

| 选项             | 说明                                                             | 是否必需？ | 示例                                              |
|------------------|-------------------------------------------------------------------------|-----------|---------------------------------------------------|
| `type`             | 要使用的特定适配器                                             | 必需      | `tidb`                                            |
| `server`           | 要连接的 TiDB Cloud 集群的端点                         | 必需      | `gateway01.ap-southeast-1.prod.aws.tidbcloud.com` |
| `port`             | 要使用的端口                                                         | 必需      | `4000`                                            |
| `schema`           | 要将数据规范化到的架构（数据库）                      | 必需      | `analytics`                                       |
| `username`         | 用于连接 TiDB Cloud 集群的用户名               | 必需      | `xxxxxxxxxxx.root`                                |
| `password`         | 用于向 TiDB Cloud 集群进行身份验证的密码       | 必需      | `"your_password"`                                 |
| `retries`          | 连接 TiDB Cloud 集群的重试次数（默认为 1）    | 可选      | `2`                                               |

## 支持的函数

您可以在 dbt-tidb 中直接使用以下函数。有关如何使用它们的信息，请参阅 [dbt-util](https://github.com/dbt-labs/dbt-utils)。

支持以下函数：

- `bool_or`
- `cast_bool_to_text`
- `dateadd`
- `datediff`。注意，`datediff` 与 dbt-util 略有不同。它向下取整而不是向上取整。
- `date_trunc`
- `hash`
- `safe_cast`
- `split_part`
- `last_day`
- `cast_bool_to_text`
- `concat`
- `escape_single_quotes`
- `except`
- `intersect`
- `length`
- `position`
- `replace`
- `right`
