---
title: App Development for go-sql-driver/mysql
summary: Learn how to build a simple Golang application based on TiDB and go-sql-driver/mysql.
aliases: ['/appdev/dev/for-go-sql-driver-mysql']
---

# App Development for go-sql-driver/mysql

> **Note:**
>
> This document has been archived. This indicates that this document will not be updated thereafter. You can see [Developer Guide Overview](/develop/dev-guide-overview.md) for more details.

This tutorial shows you how to build a simple Golang application based on TiDB and go-sql-driver/mysql. The sample application to build here is a simple CRM tool where you can add, query, and update customer and order information.

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

1. In the SQL shell, create the `go_mysql` database that your application will use:

    {{< copyable "" >}}

    ```sql
    CREATE DATABASE django;
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
    GRANT ALL ON go_mysql.* TO <username>;
    ```

## Step 3. Get and run the application code

The sample application code in this tutorial (`main.go`) uses go-sql-driver/mysql to map Golang methods to SQL operations that are described in the code comments. You can save the example application code as a Golang file named `main.go` on your local machine.

{{< copyable "" >}}

```go
package main

import (
    "database/sql"
    "fmt"

    _ "github.com/go-sql-driver/mysql"
)
// Creates the orders and customer tables.
func init_table(db *sql.DB) (err error) {
    _, err = db.Exec(
        "CREATE TABLE IF NOT EXISTS orders (oid INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT, cid INT UNSIGNED, price FLOAT);")
    if err != nil {
        return
    }

    _, err = db.Exec(
        "CREATE TABLE IF NOT EXISTS customer (cid INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255), gender ENUM ('Male', 'Female') NOT NULL)")
    if err != nil {
        return
    }
    return
}
// Inserts data into the orders and customer tables.
func init_data(db *sql.DB) (err error) {
    sqls := []string{
        "INSERT INTO customer (name, gender) value ('Ben','Male');",
        "INSERT INTO customer (name, gender) value ('Alice','Female');",
        "INSERT INTO customer (name, gender) value ('Peter','Male');",
        "INSERT INTO orders (cid, price) value (1,10.23);",
        "INSERT INTO orders (cid, price) value (2,122);",
        "INSERT INTO orders (cid, price) value (2,72.5);",
    }
    for _, sql := range sqls {
        _, err = db.Exec(sql)
        if err != nil {
            return
        }
    }

    return
}

// Connects to TiDB.
func main() {
    db, err := sql.Open("mysql", "{user}:{password}@{globalhost}:26257/go_mysql?charset=utf8mb4")
    if err != nil {
        fmt.Println(err)
        return
    }

    if err := init_table(db); err != nil {
        panic(err)
    }
    if err := init_data(db); err != nil {
        panic(err)
    }

    // Updates data in orders.
    _, err = db.Exec("UPDATE orders SET price = price + 1 WHERE oid = 1")
    if err != nil {
        panic(err)
    }
    // Deletes data from orders.
    _, err = db.Exec("DELETE FROM orders WHERE oid = 1")
    if err != nil {
        panic(err)
    }
    // Reads data from orders.
    rows, err := db.Query("SELECT * FROM orders")
    if err != nil {
        panic(err)
    }
    defer rows.Close()
    for rows.Next() {
        var oid, cid int
        var price float64
        err := rows.Scan(&oid, &cid, &price)
        if err != nil {
            panic(err)
        }
        fmt.Printf("%d %d %.2f\n", oid, cid, price)
    }
    // Joins orders and customer tables.
    rows, err = db.Query("SELECT customer.name, orders.price FROM customer, orders WHERE customer.cid = orders.cid")
    if err != nil {
        panic(err)
    }
    defer rows.Close()
    for rows.Next() {
        var name string
        var price float64
        err := rows.Scan(&name, &price)
        if err != nil {
            panic(err)
        }
        fmt.Printf("%s %.2f\n", name, price)
    }
}
```

### Step 1. Update the connection parameters and connect to TiDB

In the `main.go` file above, replace the string passed to `sql.Open()` with the connection string you have obtained when creating the database. The `sql.Open()` function call should look similar to the following one:

{{< copyable "" >}}

```go
db, err := sql.Open("mysql", "{user}:{password}@{globalhost}:26257/go_mysql?charset=utf8mb4")
```

### Step 2. Run the application code

1. Initialize the go-sql-driver/mysql module:

    {{< copyable "" >}}

    ```bash
     go mod init mysql-driver-demo
    ```

2. Run the `main.go` code:

    {{< copyable "" >}}

    ```bash
    go run main.go
    ```

    The expected output is as follows:

    ```
    2 2 122.00
    3 2 72.50
    Alice 72.50
    Alice 122.00
    ```