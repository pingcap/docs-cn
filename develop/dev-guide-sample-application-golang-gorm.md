---
title: Build a Simple CRUD App with TiDB and GORM
summary: Learn how to build a simple CRUD application with TiDB and GORM.
---

<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD029 -->

# Build a Simple CRUD App with TiDB and GORM

[GORM](https://gorm.io/) is a popular open-source ORM library for Golang.

This document describes how to use TiDB and GORM to build a simple CRUD application.

> **Note:**
>
> It is recommended to use Golang 1.20 or a later version.

## Step 1. Launch your TiDB cluster

<CustomContent platform="tidb">

The following introduces how to start a TiDB cluster.

**Use a TiDB Serverless cluster**

For detailed steps, see [Create a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-tidb-serverless-cluster).

**Use a local cluster**

For detailed steps, see [Deploy a local test cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) or [Deploy a TiDB Cluster Using TiUP](/production-deployment-using-tiup.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

See [Create a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-tidb-serverless-cluster).

</CustomContent>

## Step 2. Get the code

```shell
git clone https://github.com/pingcap-inc/tidb-example-golang.git
```

The following instructions take `v1.23.5` as an example.

To adapt TiDB transactions, write a toolkit [util](https://github.com/pingcap-inc/tidb-example-golang/tree/main/util) according to the following code:

```go
package util

import (
    "gorm.io/gorm"
)

// TiDBGormBegin start a TiDB and Gorm transaction as a block. If no error is returned, the transaction will be committed. Otherwise, the transaction will be rolled back.
func TiDBGormBegin(db *gorm.DB, pessimistic bool, fc func(tx *gorm.DB) error) (err error) {
    session := db.Session(&gorm.Session{})
    if session.Error != nil {
        return session.Error
    }

    if pessimistic {
        session = session.Exec("set @@tidb_txn_mode=pessimistic")
    } else {
        session = session.Exec("set @@tidb_txn_mode=optimistic")
    }

    if session.Error != nil {
        return session.Error
    }
    return session.Transaction(fc)
}
```

Change to the `gorm` directory:

```shell
cd gorm
```

The structure of this directory is as follows:

```
.
├── Makefile
├── go.mod
├── go.sum
└── gorm.go
```

`gorm.go` is the main body of the `gorm`. Compared with go-sql-driver/mysql, GORM avoids differences in database creation between different databases. It also implements a lot of operations, such as AutoMigrate and CRUD of objects, which greatly simplifies the code.

`Player` is a data entity struct that is a mapping for tables. Each property of a `Player` corresponds to a field in the `player` table. Compared with go-sql-driver/mysql, `Player` in GORM adds struct tags to indicate mapping relationships for more information, such as `gorm:"primaryKey;type:VARCHAR(36);column:id"`.

```go

package main

import (
    "fmt"
    "math/rand"

    "github.com/google/uuid"
    "github.com/pingcap-inc/tidb-example-golang/util"

    "gorm.io/driver/mysql"
    "gorm.io/gorm"
    "gorm.io/gorm/clause"
    "gorm.io/gorm/logger"
)

type Player struct {
    ID    string `gorm:"primaryKey;type:VARCHAR(36);column:id"`
    Coins int    `gorm:"column:coins"`
    Goods int    `gorm:"column:goods"`
}

func (*Player) TableName() string {
    return "player"
}

func main() {
    // 1. Configure the example database connection.
    db := createDB()

    // AutoMigrate for player table
    db.AutoMigrate(&Player{})

    // 2. Run some simple examples.
    simpleExample(db)

    // 3. Explore more.
    tradeExample(db)
}

func tradeExample(db *gorm.DB) {
    // Player 1: id is "1", has only 100 coins.
    // Player 2: id is "2", has 114514 coins, and 20 goods.
    player1 := &Player{ID: "1", Coins: 100}
    player2 := &Player{ID: "2", Coins: 114514, Goods: 20}

    // Create two players "by hand", using the INSERT statement on the backend.
    db.Clauses(clause.OnConflict{UpdateAll: true}).Create(player1)
    db.Clauses(clause.OnConflict{UpdateAll: true}).Create(player2)

    // Player 1 wants to buy 10 goods from player 2.
    // It will cost 500 coins, but player 1 cannot afford it.
    fmt.Println("\nbuyGoods:\n    => this trade will fail")
    if err := buyGoods(db, player2.ID, player1.ID, 10, 500); err == nil {
        panic("there shouldn't be success")
    }

    // So player 1 has to reduce the incoming quantity to two.
    fmt.Println("\nbuyGoods:\n    => this trade will success")
    if err := buyGoods(db, player2.ID, player1.ID, 2, 100); err != nil {
        panic(err)
    }
}

func simpleExample(db *gorm.DB) {
    // Create a player, who has a coin and a goods.
    if err := db.Clauses(clause.OnConflict{UpdateAll: true}).
        Create(&Player{ID: "test", Coins: 1, Goods: 1}).Error; err != nil {
        panic(err)
    }

    // Get a player.
    var testPlayer Player
    db.Find(&testPlayer, "id = ?", "test")
    fmt.Printf("getPlayer: %+v\n", testPlayer)

    // Create players with bulk inserts. Insert 1919 players totally, with 114 players per batch.
    bulkInsertPlayers := make([]Player, 1919, 1919)
    total, batch := 1919, 114
    for i := 0; i < total; i++ {
        bulkInsertPlayers[i] = Player{
            ID:    uuid.New().String(),
            Coins: rand.Intn(10000),
            Goods: rand.Intn(10000),
        }
    }

    if err := db.Session(&gorm.Session{Logger: db.Logger.LogMode(logger.Error)}).
        CreateInBatches(bulkInsertPlayers, batch).Error; err != nil {
        panic(err)
    }

    // Count players amount.
    playersCount := int64(0)
    db.Model(&Player{}).Count(&playersCount)
    fmt.Printf("countPlayers: %d\n", playersCount)

    // Print 3 players.
    threePlayers := make([]Player, 3, 3)
    db.Limit(3).Find(&threePlayers)
    for index, player := range threePlayers {
        fmt.Printf("print %d player: %+v\n", index+1, player)
    }
}

func createDB() *gorm.DB {
    dsn := "root:@tcp(127.0.0.1:4000)/test?charset=utf8mb4"
    db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{
        Logger: logger.Default.LogMode(logger.Info),
    })
    if err != nil {
        panic(err)
    }

    return db
}

func buyGoods(db *gorm.DB, sellID, buyID string, amount, price int) error {
    return util.TiDBGormBegin(db, true, func(tx *gorm.DB) error {
        var sellPlayer, buyPlayer Player
        if err := tx.Clauses(clause.Locking{Strength: "UPDATE"}).
            Find(&sellPlayer, "id = ?", sellID).Error; err != nil {
            return err
        }

        if sellPlayer.ID != sellID || sellPlayer.Goods < amount {
            return fmt.Errorf("sell player %s goods not enough", sellID)
        }

        if err := tx.Clauses(clause.Locking{Strength: "UPDATE"}).
            Find(&buyPlayer, "id = ?", buyID).Error; err != nil {
            return err
        }

        if buyPlayer.ID != buyID || buyPlayer.Coins < price {
            return fmt.Errorf("buy player %s coins not enough", buyID)
        }

        updateSQL := "UPDATE player set goods = goods + ?, coins = coins + ? WHERE id = ?"
        if err := tx.Exec(updateSQL, -amount, price, sellID).Error; err != nil {
            return err
        }

        if err := tx.Exec(updateSQL, amount, -price, buyID).Error; err != nil {
            return err
        }

        fmt.Println("\n[buyGoods]:\n    'trade success'")
        return nil
    })
}
```

## Step 3. Run the code

The following content introduces how to run the code step by step.

### Step 3.1 Modify parameters for TiDB Cloud

If you are using a TiDB Serverless cluster, modify the value of the `dsn` in `gorm.go`:

```go
dsn := "root:@tcp(127.0.0.1:4000)/test?charset=utf8mb4"
```

Suppose that the password you set is `123456`, and the connection parameters you get from the cluster details page are the following:

- Endpoint: `xxx.tidbcloud.com`
- Port: `4000`
- User: `2aEp24QWEDLqRFs.root`

In this case, you can modify the `dsn` as follows:

```go
dsn := "2aEp24QWEDLqRFs.root:123456@tcp(xxx.tidbcloud.com:4000)/test?charset=utf8mb4&tls=true"
```

### Step 3.2 Run the code

To run the code, you can run `make build` and `make run` respectively:

```shell
make build # this command executes `go build -o bin/gorm-example`
make run # this command executes `./bin/gorm-example`
```

Or you can use the native commands:

```shell
go build -o bin/gorm-example
./bin/gorm-example
```

Or run the `make` command directly, which is a combination of `make build` and `make run`.

## Step 4. Expected output

[GORM Expected Output](https://github.com/pingcap-inc/tidb-example-golang/blob/main/Expected-Output.md#gorm)