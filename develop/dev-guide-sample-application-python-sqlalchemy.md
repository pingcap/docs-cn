---
title: Connect to TiDB with SQLAlchemy
summary: Learn how to connect to TiDB using SQLAlchemy. This tutorial gives Python sample code snippets that work with TiDB using SQLAlchemy.
aliases: ['/tidb/dev/dev-guide-outdated-for-sqlalchemy']
---

# Connect to TiDB with SQLAlchemy

TiDB is a MySQL-compatible database, and [SQLAlchemy](https://www.sqlalchemy.org/) is a popular Python SQL toolkit and Object Relational Mapper (ORM).

In this tutorial, you can learn how to use TiDB and SQLAlchemy to accomplish the following tasks:

- Set up your environment.
- Connect to your TiDB cluster using SQLAlchemy.
- Build and run your application. Optionally, you can find sample code snippets for basic CRUD operations.

> **Note:**
>
> This tutorial works with TiDB Serverless, TiDB Dedicated, and TiDB Self-Hosted clusters.

## Prerequisites

To complete this tutorial, you need:

- [Python 3.8 or higher](https://www.python.org/downloads/).
- [Git](https://git-scm.com/downloads).
- A TiDB cluster.

<CustomContent platform="tidb">

**If you don't have a TiDB cluster, you can create one as follows:**

- (Recommended) Follow [Creating a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster.
- Follow [Deploy a local test TiDB cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) or [Deploy a production TiDB cluster](/production-deployment-using-tiup.md) to create a local cluster.

</CustomContent>
<CustomContent platform="tidb-cloud">

**If you don't have a TiDB cluster, you can create one as follows:**

- (Recommended) Follow [Creating a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster.
- Follow [Deploy a local test TiDB cluster](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) or [Deploy a production TiDB cluster](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) to create a local cluster.

</CustomContent>

## Run the sample app to connect to TiDB

This section demonstrates how to run the sample application code and connect to TiDB.

### Step 1: Clone the sample app repository

Run the following commands in your terminal window to clone the sample code repository:

```shell
git clone https://github.com/tidb-samples/tidb-python-sqlalchemy-quickstart.git
cd tidb-python-sqlalchemy-quickstart
```

### Step 2: Install dependencies

Run the following command to install the required packages (including SQLAlchemy and PyMySQL) for the sample app:

```shell
pip install -r requirements.txt
```

#### Why use PyMySQL?

SQLAlchemy is an ORM library that works with multiple databases. It provides a high-level abstraction of the database, which helps developers write SQL statements in a more object-oriented way. However, SQLAlchemy does not include a database driver. To connect to a database, you need to install a database driver. This sample application uses PyMySQL as the database driver, which is a pure Python MySQL client library that is compatible with TiDB and can be installed on all platforms.

You can also use other database drivers, such as [mysqlclient](https://github.com/PyMySQL/mysqlclient) and [mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/). But they are not pure Python libraries and require the corresponding C/C++ compiler and MySQL client for compiling. For more information, refer to [SQLAlchemy official documentation](https://docs.sqlalchemy.org/en/20/core/engines.html#mysql).

### Step 3: Configure connection information

Connect to your TiDB cluster depending on the TiDB deployment option you've selected.

<SimpleTab>
<div label="TiDB Serverless">

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Ensure the configurations in the connection dialog match your operating environment.

    - **Endpoint Type** is set to `Public`
    - **Connect With** is set to `General`
    - **Operating System** matches your environment.

    > **Tip:**
    >
    > If your program is running in Windows Subsystem for Linux (WSL), switch to the corresponding Linux distribution.

4. Click **Create password** to create a random password.

    > **Tip:**
    > 
    > If you have created a password before, you can either use the original password or click **Reset password** to generate a new one.

5. Run the following command to copy `.env.example` and rename it to `.env`:

    ```shell
    cp .env.example .env
    ```

6. Copy and paste the corresponding connection string into the `.env` file. The example result is as follows:

    ```dotenv
    TIDB_HOST='{host}'  # e.g. gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    TIDB_PORT='4000'
    TIDB_USER='{user}'  # e.g. xxxxxx.root
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    CA_PATH='{ssl_ca}'  # e.g. /etc/ssl/certs/ca-certificates.crt (Debian / Ubuntu / Arch)
    ```

    Be sure to replace the placeholders `{}` with the connection parameters obtained from the connection dialog.

7. Save the `.env` file.

</div>
<div label="TiDB Dedicated">

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Click **Allow Access from Anywhere** and then click **Download TiDB cluster CA** to download the CA certificate.

    For more details about how to obtain the connection string, refer to [TiDB Dedicated standard connection](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection).

4. Run the following command to copy `.env.example` and rename it to `.env`:

    ```shell
    cp .env.example .env
    ```

5. Copy and paste the corresponding connection string into the `.env` file. The example result is as follows:

    ```dotenv
    TIDB_HOST='{host}'  # e.g. tidb.xxxx.clusters.tidb-cloud.com
    TIDB_PORT='4000'
    TIDB_USER='{user}'  # e.g. root
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    CA_PATH='{your-downloaded-ca-path}'
    ```

    Be sure to replace the placeholders `{}` with the connection parameters obtained from the connection dialog, and configure `CA_PATH` with the certificate path downloaded in the previous step.

6. Save the `.env` file.

</div>
<div label="TiDB Self-Hosted">

1. Run the following command to copy `.env.example` and rename it to `.env`:

    ```shell
    cp .env.example .env
    ```

2. Copy and paste the corresponding connection string into the `.env` file. The example result is as follows:

    ```dotenv
    TIDB_HOST='{tidb_server_host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

    Be sure to replace the placeholders `{}` with the connection parameters, and remove the `CA_PATH` line. If you are running TiDB locally, the default host address is `127.0.0.1`, and the password is empty.

3. Save the `.env` file.

</div>
</SimpleTab>

### Step 4: Run the code and check the result

1. Execute the following command to run the sample code:

    ```shell
    python sqlalchemy_example.py
    ```

2. Check the [Expected-Output.txt](https://github.com/tidb-samples/tidb-python-sqlalchemy-quickstart/blob/main/Expected-Output.txt) to see if the output matches.

## Sample code snippets

You can refer to the following sample code snippets to complete your own application development.

For complete sample code and how to run it, check out the [tidb-samples/tidb-python-sqlalchemy-quickstart](https://github.com/tidb-samples/tidb-python-sqlalchemy-quickstart) repository.

### Connect to TiDB

```python
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker

def get_db_engine():
    connect_args = {}
    if ${ca_path}:
        connect_args = {
            "ssl_verify_cert": True,
            "ssl_verify_identity": True,
            "ssl_ca": ${ca_path},
        }
    return create_engine(
        URL.create(
            drivername="mysql+pymysql",
            username=${tidb_user},
            password=${tidb_password},
            host=${tidb_host},
            port=${tidb_port},
            database=${tidb_db_name},
        ),
        connect_args=connect_args,
    )

engine = get_db_engine()
Session = sessionmaker(bind=engine)
```

When using this function, you need to replace `${tidb_host}`, `${tidb_port}`, `${tidb_user}`, `${tidb_password}`, `${tidb_db_name}` and `${ca_path}` with the actual values of your TiDB cluster.

### Define a table

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Player(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True)
    coins = Column(Integer)
    goods = Column(Integer)

    __tablename__ = "players"
```

For more information, refer to [SQLAlchemy documentation: Mapping classes with declarative](https://docs.sqlalchemy.org/en/20/orm/declarative_mapping.html).

### Insert data

```python
with Session() as session:
    player = Player(name="test", coins=100, goods=100)
    session.add(player)
    session.commit()
```

For more information, refer to [Insert data](/develop/dev-guide-insert-data.md).

### Query data

```python
with Session() as session:
    player = session.query(Player).filter_by(name == "test").one()
    print(player)
```

For more information, refer to [Query data](/develop/dev-guide-get-data-from-single-table.md).

### Update data

```python
with Session() as session:
    player = session.query(Player).filter_by(name == "test").one()
    player.coins = 200
    session.commit()
```

For more information, refer to [Update data](/develop/dev-guide-update-data.md).

### Delete data

```python
with Session() as session:
    player = session.query(Player).filter_by(name == "test").one()
    session.delete(player)
    session.commit()
```

For more information, refer to [Delete data](/develop/dev-guide-delete-data.md).

## Next steps

- Learn more usage of SQLAlchemy from [the documentation of SQLAlchemy](https://www.sqlalchemy.org/).
- Learn the best practices for TiDB application development with the chapters in the [Developer guide](/develop/dev-guide-overview.md), such as [Insert data](/develop/dev-guide-insert-data.md), [Update data](/develop/dev-guide-update-data.md), [Delete data](/develop/dev-guide-delete-data.md), [Single table reading](/develop/dev-guide-get-data-from-single-table.md), [Transactions](/develop/dev-guide-transaction-overview.md), and [SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md).
- Learn through the professional [TiDB developer courses](https://www.pingcap.com/education/) and earn [TiDB certifications](https://www.pingcap.com/education/certification/) after passing the exam.

## Need help?

Ask questions on the [Discord](https://discord.gg/vYU9h56kAX), or [create a support ticket](https://support.pingcap.com/).
