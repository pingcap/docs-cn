---
title: App Development for GORM
summary: Learn how to build a simple Golang application based on TiDB and GORM.
aliases: ['/appdev/dev/for-gorm']
---

# App Development for GORM

> **Note:**
>
> This document has been archived. This indicates that this document will not be updated thereafter. You can see [Developer Guide Overview](/develop/dev-guide-overview.md) for more details.

This tutorial shows you how to build a simple Golang application based on TiDB and GORM. The sample application to build here is a simple CRM tool where you can add, query, and update customer and order information.

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

1. In the SQL shell, create the `gorm` database that your application will use:

    {{< copyable "" >}}

    ```sql
    CREATE DATABASE gorm;
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
    GRANT ALL ON gorm.* TO <username>;
    ```

## Step 3. Get and run the application code

The sample application code in this tutorial (`main.go`) uses GORM to map Golang methods to SQL operations that are described in the code comments. You can save the example application code as a Golang file named `main.go` on your local machine.

{{< copyable "" >}}

```go
package main

import (
    "fmt"

    "gorm.io/driver/mysql"
    "gorm.io/gorm"
)
// The schema of the Order table to be created.
type Order struct {
    Oid   int     `gorm:"primary_key;autoIncrement:true"`
    Uid   int     `gorm:"column:uid"`
    Price float64 `gorm:"column:price"`
}

type GenderModel string

const (
    Female GenderModel = "Female"
    Male   GenderModel = "Male"
)
// The schema of the User table to be created.
type User struct {
    Uid    int         `gorm:"primary_key;autoIncrement:true"`
    Name   string      `gorm:"column:name"`
    Gender GenderModel `sql:"type:gender_model"`
}

func PrintResult(tx *gorm.DB, result []Order) {
    if tx.Error == nil && tx.RowsAffected > 0 {
        for _, order := range result {
            fmt.Printf("%+v\n", order)
        }
    }
}

type JoinResult struct {
    Name  string  `json:"name"`
    Price float64 `json:"price"`
}

func PrintJoinResult(tx *gorm.DB, result []JoinResult) {
    if tx.Error == nil && tx.RowsAffected > 0 {
        for _, order := range result {
            fmt.Printf("%+v\n", order)
        }
    }
}
// Connects to TiDB.
func main() {
    dsn := "{user}:{password}@{host}:4000/{database}?charset=utf8&parseTime=True&loc=Local"
    db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
    if err != nil {
        panic("failed to connect database")
    }

    // Creates the Order table and the User table.
    db.AutoMigrate(&Order{})
    db.AutoMigrate(&User{})

    // Inserts data into the Order and User tables.
    db.Create(&Order{Uid: 1, Price: 100})
    db.Create(&Order{Uid: 2, Price: 200})
    db.Create(&Order{Uid: 2, Price: 300})
    db.Create(&Order{Uid: 3, Price: 400})
    db.Create(&Order{Uid: 4, Price: 500})

    db.Create(&User{Name: "Alice", Gender: Female})
    db.Create(&User{Name: "John", Gender: Male})
    db.Create(&User{Name: "Ben", Gender: Male})
    db.Create(&User{Name: "Aileen", Gender: Female})

    // Deletes data from the Order table.
    db.Delete(&Order{}, 1)
    db.Where("uid = ?", 2).Delete(&Order{})

    // Updates data to the Order table.
    db.Model(&Order{}).Where("oid = ?", 2).Update("price", gorm.Expr("price * ? + ?", 2, 100))

    var orders []Order
    // Gets all records.
    result := db.Find(&orders)
    PrintResult(result, orders)

    // Gets records with conditions.
    result = db.Where("uid IN ?", []int{2, 3}).Find(&orders)
    PrintResult(result, orders)

    result = db.Where("price >= ?", 300).Find(&orders)
    PrintResult(result, orders)

    result = db.Raw("SELECT * FROM orders WHERE price = ?", 500).Scan(&orders)
    PrintResult(result, orders)

    var join_result []JoinResult
    // Joins orders and users.
    result = db.Table("users").Select("orders.price as price, users.name as name").Joins("INNER JOIN orders ON orders.uid = users.uid").Where("users.uid = ?", 4).Find(&join_result)
    PrintJoinResult(result, join_result)
}
```

### Step 1. Update the connection parameters and connect to TiDB

In the `main.go` file above, replace the string passed to `sql.Open()` with the connection string you have obtained when creating the database. The `sql.Open()` function call is expected to look similar to the following one:

{{< copyable "" >}}

```go
dsn := "root:@tcp(localhost:4000)/gorm?charset=utf8&parseTime=True&loc=Local"
```

### Step 2. Run the code

1. Initialize the GORM module:

    {{< copyable "" >}}

    ```bash
    go mod init gorm_demo
    ```

2. Run the `main.go` code:

    {{< copyable "" >}}

    ```bash
    go run main.go
    ```

    The expected output is as follows:

    ```
    {Oid:4 Uid:3 Price:400}
    {Oid:5 Uid:4 Price:500}
    {Oid:4 Uid:3 Price:400}
    {Oid:4 Uid:3 Price:400}
    {Oid:5 Uid:4 Price:500}
    {Oid:5 Uid:4 Price:500}
    {Name:Aileen Price:500}
    ```
