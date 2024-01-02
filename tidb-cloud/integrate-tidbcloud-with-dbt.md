---
title: Integrate TiDB Cloud with dbt
summary: Learn the use cases of dbt in TiDB Cloud.
---

# Integrate TiDB Cloud with dbt

[Data build tool (dbt)](https://www.getdbt.com/) is a popular open-source data transformation tool that helps analytics engineers transform data in their warehouses through SQL statements. Through the [dbt-tidb](https://github.com/pingcap/dbt-tidb) plugin, analytics engineers working with TiDB Cloud can directly create forms and match data through SQL without having to think about the process of creating tables or views.

This document introduces how to use dbt with TiDB Cloud, taking a dbt project as an example.

## Step 1: Install dbt and dbt-tidb

You can install dbt and dbt-tidb using only one command. In the following command, dbt is installed as a dependency when you install dbt-tidb.

```shell
pip install dbt-tidb
```

You can also install dbt separately. See [How to install dbt](https://docs.getdbt.com/docs/get-started/installation) in the dbt documentation.

## Step 2: Create a demo project

To try out the dbt function, you can use [jaffle_shop](https://github.com/dbt-labs/jaffle_shop), a demo project provided by dbt-lab. You can clone the project directly from GitHub:

```shell
git clone https://github.com/dbt-labs/jaffle_shop && \
cd jaffle_shop
```

All files in the `jaffle_shop` directory are structured as follows:

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

In this directory:

- `dbt_project.yml` is the dbt project configuration file, which holds the project name and database configuration file information.

- The `models` directory contains the project’s SQL models and table schemas. Note that the data analyst writes this section. For more information about models, see [SQL models](https://docs.getdbt.com/docs/build/sql-models).

- The `seeds` directory stores the CSV files that are dumped by the database export tools. For example, you can [export the TiDB Cloud data](https://docs.pingcap.com/tidbcloud/export-data-from-tidb-cloud) into CSV files through Dumpling. In the `jaffle_shop` project, these CSV files are used as raw data to be processed.

## Step 3: Configure the project

To configure the project, take the following steps:

1. Complete the global configuration.

    You can refer to [Description of profile fields](#description-of-profile-fields) and edit the default global profile, `~/.dbt/profiles.yml`, to configure the connection with TiDB Cloud:

    ```shell
    sudo vi ~/.dbt/profiles.yml
    ```

    In the editor, add the following configuration:

   ```yaml
    jaffle_shop_tidb:                                                 # Project name
      target: dev                                                     # Target
      outputs:
        dev:
          type: tidb                                                  # The specific adapter to use
          server: gateway01.ap-southeast-1.prod.aws.tidbcloud.com     # The TiDB Cloud clusters' endpoint to connect to
          port: 4000                                                  # The port to use
          schema: analytics                                           # Specify the schema (database) to normalize data into
          username: xxxxxxxxxxx.root                                  # The username to use to connect to the TiDB Cloud clusters
          password: "your_password"                                   # The password to use for authenticating to the TiDB Cloud clusters
    ```

    You can get the values of `server`, `port`, and `username` from the connection dialog of your cluster. To open this dialog, go to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project, click the name of your target cluster to go to its overview page, and then click **Connect** in the upper-right corner.

2. Complete the project configuration.

    In the jaffle_shop project directory, edit the project configuration file `dbt_project.yml` and change the `profile` field to `jaffle_shop_tidb`. This configuration allows the project to query from the database as specified in the `~/.dbt/profiles.yml` file.

    ```shell
    vi dbt_project.yml
    ```

    In the editor, update the configuration as follows:

    ```yaml
    name: 'jaffle_shop'

    config-version: 2
    version: '0.1'

    profile: 'jaffle_shop_tidb'                   # note the modification here

    model-paths: ["models"]                       # model path
    seed-paths: ["seeds"]                         # seed path
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
          materialized: table            # *.sql which in models/ would be materialized to table
          staging:
            materialized: view           # *.sql which in models/staging/ would bt materialized to view
    ```

3. Verify the configuration.

    Run the following command to check whether the database and project configuration is correct.

    ```shell
    dbt debug
    ```

## Step 4: (optional) Load CSV files

> **Note:**
>
> This step is optional. If the data for processing is already in the target database, you can skip this step.

Now that you have successfully created and configured the project, it’s time to load the CSV data and materialize the CSV as a table in the target database.

1. Load the CSV data and materialize the CSV as a table in the target database.

    ```shell
    dbt seed
    ```

    The following is an example output:

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

    As you can see in the results, the seed file was started and loaded into three tables: `analytics.raw_customers`, `analytics.raw_orders`, and `analytics.raw_payments`.

2. Verify the results in TiDB Cloud.

    The `show databases` command lists the new `analytics` database that dbt has created. The `show tables` command indicates that there are three tables in the `analytics` database, corresponding to the ones you have created.

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

## Step 5: Transform data

Now you are ready to run the configured project and finish the data transformation.

1. Run the dbt project to finish the data transformation:

    ```shell
    dbt run
    ```

    The following is an example output:

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

    The result shows that two tables (`analytics.customers` and `analytics.orders`), and three views (`analytics.stg_customers`, `analytics.stg_orders`, and `analytics.stg_payments`) are created successfully.

2. Go to TiDB Cloud to verify that the transformation is successful.

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

    The output shows that five more tables or views have been added, and the data in the tables or views has been transformed. Only part of the data from the customer table is shown in this example.

## Step 6: Generate the document

dbt lets you generate visual documents that display the overall structure of the project and describe all the tables and views.

To generate visual documents, take the following steps:

1. Generate the document:

    ```shell
    dbt docs generate
    ```

2. Start the server:

    ```shell
    dbt docs serve
    ```

3. To access the document from your browser, go to [http://localhost:8080](http://localhost:8080).

## Description of profile fields

| Option           | Description                                                             | Required? | Example                                           |
|------------------|-------------------------------------------------------------------------|-----------|---------------------------------------------------|
| `type`             | The specific adapter to use                                             | Required  | `tidb`                                            |
| `server`           | The TiDB Cloud clusters' endpoint to connect to                         | Required  | `gateway01.ap-southeast-1.prod.aws.tidbcloud.com` |
| `port`             | The port to use                                                         | Required  | `4000`                                            |
| `schema`           | The schema (database) to normalize data into                      | Required  | `analytics`                                       |
| `username`         | The username to use to connect to the TiDB Cloud clusters               | Required  | `xxxxxxxxxxx.root`                                |
| `password`         | The password to use for authenticating to the TiDB Cloud clusters       | Required  | `"your_password"`                                 |
| `retries`          | The retry times for connection to TiDB Cloud clusters (1 by default)    | Optional  | `2`                                               |

## Supported functions

You can use the following functions directly in dbt-tidb. For information about how to use them, see [dbt-util](https://github.com/dbt-labs/dbt-utils).

The following functions are supported:

- `bool_or`
- `cast_bool_to_text`
- `dateadd`
- `datediff`. Note that `datediff` is a little different from dbt-util. It rounds down rather than rounds up.
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
