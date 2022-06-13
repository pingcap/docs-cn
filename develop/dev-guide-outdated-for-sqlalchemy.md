---
title: App Development for SQLAlchemy
summary: Learn how to build a simple Python application based on TiDB and SQLAlchemy.
aliases: ['/appdev/dev/for-sqlalchemy']
---

# App Development for SQLAlchemy

> **Note:**
>
> This document has been archived. This indicates that this document will not be updated thereafter. You can see [Developer Guide Overview](/develop/dev-guide-overview.md) for more details.

This tutorial shows you how to build a simple Python application based on TiDB and SQLAlchemy. The sample application to build here is a simple CRM tool where you can add, query, and update customer and order information.

## Step 1. Start a TiDB cluster

Start a pseudo TiDB cluster on your local storage:

{{< copyable "" >}}

```bash
docker run -p 127.0.0.1:$LOCAL_PORT:4000 pingcap/tidb:v5.1.0
```

The above command starts a temporary and single-node cluster with mock TiKV. The cluster listens on the port `$LOCAL_PORT`. After the cluster is stopped, any changes already made to the database are not persisted.

> **Note:**
>
> To deploy a "real" TiDB cluster for production, see the following guides:
>
> + [Deploy TiDB using TiUP for On-Premises](https://docs.pingcap.com/tidb/v5.1/production-deployment-using-tiup)
> + [Deploy TiDB on Kubernetes](https://docs.pingcap.com/tidb-in-kubernetes/stable)
>
> You can also [use TiDB Cloud](https://pingcap.com/products/tidbcloud/), a fully-managed Database-as-a-Service (DBaaS), which offers free trial.

## Step 2. Create a database

1. In the SQL shell, create the `test_sqlalchemy` database that your application will use:

    {{< copyable "" >}}

    ```sql
    CREATE DATABASE test_sqlalchemy;
    ```

2. Create a SQL user for your application:

    {{< copyable "" >}}

    ```sql
    CREATE USER <username> IDENTIFIED BY <password>;
    ```

    Take note of the username and password. You will use them in your application code when initializing the project.

3. Grant necessary permissions to the SQL user you have just created:

    {{< copyable "" >}}

    ```sql
    GRANT ALL ON test_sqlalchemy.* TO <username>;
    ```

## Step 3. Set virtual environments and initialize the project

1. Use [Poetry](https://python-poetry.org/docs/), a dependency and package manager in Python, to set virtual environments and initialize the project.

    Poetry can isolate system dependencies from other dependencies and avoid dependency pollution. Use the following command to install Poetry.

    {{< copyable "" >}}

    ```bash
    pip install --user poetry
    ```

2. Initialize the development environment using Poetry:

    {{< copyable "" >}}

    ```bash
    poetry init --no-interaction --dependency sqlalchemy

    poetry add git+https://github.com/pingcap/sqlalchemy-tidb.git#main
    ```

## Step 4. Get and run the application code

The sample application code in this tutorial (`main.py`) uses SQLAlchemy to map Python methods to SQL operations. You can save the example application code as a Python file named `main.py` on your local machine.

The code performs the following operations:

1. Creates the `users` and `orders` tables in the `test_sqlalchemy` database as specified by the `User` and `Order` mapping classes.
2. Inserts data to the `users` and `orders` tables.
3. Deletes data from orders by `oid`.
4. Updates `orders` by `oid`.
5. Joins the `users` and `orders` tables.
6. Queries the `users` and `orders` tables using the same `uid`.

{{< copyable "" >}}

```python
from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import enum
engine = create_engine(
    'tidb://{username}:{password}@{hostname}:{port}/test_sqlalchemy?charset=utf8mb4',
    echo=False)

# The base class on which the objects will be defined.
Base = declarative_base()

class Gender(enum.Enum):
    Female = 1
    Male = 2

class User(Base):
    __tablename__ = 'users'
    uid = Column(Integer, primary_key=True)
    name = Column(String(50))
    gender = Column(Enum(Gender))

    def __repr__(self):
        return "<User(name='%s', gender='%s')>" % (
            self.name, self.gender)

class Order(Base):
    __tablename__ = 'orders'

    # Every SQLAlchemy table should have a primary key named 'id'.
    oid = Column(Integer, primary_key=True, autoincrement=True)

    uid = Column(Integer)
    price = Column(Float)

    # Prints out a user object conveniently.
    def __repr__(self):
        return "<User(oid='%d', uid='%d', price'%f')>" % (
            self.name, self.uid, self.price)

# Creates all tables by issuing CREATE TABLE commands to the database.
Base.metadata.create_all(engine)

# Creates a new session to the database by using the described engine.
Session = sessionmaker(bind=engine)
session = Session()

# Inserts users into the database.
session.add_all([
    User(name='Alice', gender=Gender.Female),
    User(name='Peter', gender=Gender.Male),
    User(name='Ben', gender=Gender.Male),
])
session.commit()

# Inserts Order into the database.
ed_user = Order(uid=1, price=2.5)

# Adds the created users to the DB and commit.
session.add(ed_user)
session.commit()

# Inserts Orders into the database.
session.add_all([
    Order(uid=1, price=0.5),
    Order(uid=2, price=4.5),
    Order(uid=2, price=2123.87),
    Order(uid=3, price=212.5),
    Order(uid=3, price=8.5),
]
)
session.commit()

# Deletes orders by oid.
session.query(Order).filter(Order.oid == 4).delete()
session.commit()

# Updates orders.
session.query(Order).filter(Order.oid == 1).update({'price': 3.5})
session.commit()

# Joins orders and users tables.
print(
    session.query(User.name, Order.price)
    .select_from(User)
    .filter(User.uid == Order.uid)
    .filter(Order.uid == 3)
    .all()
)
```

### Step 1. Update the connection parameters and connect to TiDB

In the `main.py` file above, replace the string passed to `create_engine()` with the connection string you have obtained when creating the database.

{{< copyable "" >}}

```python
engine = create_engine(
    'tidb://{username}:{password}@{hostname}:{port}/test_sqlalchemy?charset=utf8mb4',
    echo=False)
```

By default, you can set the string as follows:

{{< copyable "" >}}

```python
engine = create_engine(
    'tidb://root:@127.0.0.1:4000/test_sqlalchemy?charset=utf8mb4',
    echo=False)
```

### Step 2. Run the application code

After the connection string is correctly set, run the application code:

{{< copyable "" >}}

```bash
python3 main.py
```

The expected output is as follows:

```
[('Ben', 212.5), ('Ben', 8.5)]
```
