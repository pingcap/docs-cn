---
title: App Development for mysql-connector-python
summary: Learn how to build a simple Python application based on TiDB and mysql-connector-python.
aliases: ['/appdev/dev/for-python-mysql-connector']
---

# App Development for the mysql-connector-python

> **Note:**
>
> This document has been archived. This indicates that this document will not be updated thereafter. You can see [Developer Guide Overview](/develop/dev-guide-overview.md) for more details.

This tutorial shows you how to build a simple Python application based on TiDB and mysql-connector-python. The sample application to build here is a simple CRM tool where you can add, query, and update customer and order information.

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

1. In the SQL shell, create the `tidb_example` database that your application will use:

    {{< copyable "" >}}

    ```sql
    CREATE DATABASE tidb_example;
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
    GRANT ALL ON tidb_example.* TO <username>;
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
    mkdir tidb_example
    cd tidb_example
    poetry init --no-interaction --dependency mysql-connector-python
    ```

## Step 4. Get and run the application code

The sample application code in this tutorial (`main.py`) uses mysql-connector-python to map Python methods to SQL operations that are described in the code comments. You can save the example application code as a Python file named `main.py` on your local machine.

{{< copyable "" >}}

```python
import mysql.connector

# Connects to the database in TiDB.
mydb = mysql.connector.connect(
  host="localhost",
  port="4000",
  user="root",
  passwd="",
  database="tidb_example"
)

# Creates the database cursor.
mycursor = mydb.cursor()

# Created the orders and customer tables.
mycursor.execute("CREATE TABLE IF NOT EXISTS orders (oid INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT, cid INT UNSIGNED, price FLOAT);")
mycursor.execute("CREATE TABLE IF NOT EXISTS customer (cid INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255), gender ENUM ('Male', 'Female') NOT NULL)")


# Inserts data into the orders and customer tables.

add_customer = ("INSERT INTO customer (name, gender) VALUES (%(name)s, %(gender)s);")
add_order = "INSERT INTO orders (cid, price) VALUES ({}, {});"

data_customers = [
    {'name': 'Ben', 'gender': 'Male'},
    {'name': 'Alice', 'gender': 'Female'},
    {'name': 'Peter', 'gender': 'Male'},
]

data_orders = [
    [1.3, 4.0, 52.0, 123.0, 45.0],
    [2.4, 23.4],
    [100.0],
]

# Inserts new employees.
for data_customer in data_customers:
    mycursor.execute(add_customer, data_customer)
    mydb.commit()

cid = 1
for price in data_orders[cid-1]:
    mycursor.execute(add_order.format(cid, price))
    cid = cid + 1
    mydb.commit()

# Queries the customer table.
mycursor.execute("SELECT * FROM customer")
myresult = mycursor.fetchall()
for x in myresult:
  print(x)

# Updates the orders table.
mycursor.execute("UPDATE orders SET price = %s WHERE oid = %s", (100.0, 1))
mydb.commit()

# Joins the two tables.
mycursor.execute("SELECT customer.name, orders.price FROM customer INNER JOIN orders ON customer.cid = orders.cid")

myresult = mycursor.fetchall()
for x in myresult:
  print(x)

# Closes the database connection.
mycursor.close()
mydb.close()
```

### Step 1. Update the connection parameters and connect to TiDB

Replace the string passed to `mysql.connector.connect()` with the connection string you have obtained when creating the database.

{{< copyable "" >}}

```python
mydb = mysql.connector.connect(
  host="localhost",
  port=4000,
  user="root",
  passwd="",
  database="tidb_example"
)
```

### Step 2. Run the application code

Run the following command to run the `main.py` code:

{{< copyable "" >}}

```python
python3 main.py
```

The expected output is as follows:

```
(1, 'Ben', 'Male')
(2, 'Alice', 'Female')
(3, 'Peter', 'Male')
('Ben', 100.0)
('Alice', 4.0)
('Peter', 52.0)
```
