---
title: TiDB 和 GORM 的简单 CRUD 应用程序
summary: 给出一个 TiDB 和 GORM 的简单 CRUD 应用程序示例。
---

<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD029 -->

# TiDB 和 GORM 的简单 CRUD 应用程序

[GORM](https://gorm.io/) 为当前比较流行的 Golang 开源 ORM 之一。

本文档将展示如何使用 TiDB 和 GORM 来构造一个简单的 CRUD 应用程序。

> **注意：**
>
> 推荐使用 Golang 1.20 以上版本进行 TiDB 的应用程序的编写。

## 第 1 步：启动你的 TiDB 集群

本节将介绍 TiDB 集群的启动方法。

**使用 TiDB Serverless 集群**

详细步骤，请参考：[创建 TiDB Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md#第-1-步创建-tidb-serverless-集群)。

**使用本地集群**

详细步骤，请参考：[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#部署本地测试集群)或[部署正式 TiDB 集群](/production-deployment-using-tiup.md)。

## 第 2 步：获取代码

```shell
git clone https://github.com/pingcap-inc/tidb-example-golang.git
```

此处将以 GORM v1.23.5 版本进行说明。

封装一个用于适配 TiDB 事务的工具包 [util](https://github.com/pingcap-inc/tidb-example-golang/tree/main/util)，编写以下代码备用：

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

进入目录 `gorm`：

```shell
cd gorm
```

目录结构如下所示：

```
.
├── Makefile
├── go.mod
├── go.sum
└── gorm.go
```

其中，`gorm.go` 是 `gorm` 这个示例程序的主体。使用 gorm 时，相较于 go-sql-driver/mysql，gorm 屏蔽了创建数据库连接时，不同数据库差异的细节，其还封装了大量的操作，如 AutoMigrate、基本对象的 CRUD 等，极大地简化了代码量。

`Player` 是数据结构体，为数据库表在程序内的映射。`Player` 的每个属性都对应着 `player` 表的一个字段。相较于 go-sql-driver/mysql，gorm 的 `Player` 数据结构体为了给 gorm 提供更多的信息，加入了形如 `gorm:"primaryKey;type:VARCHAR(36);column:id"` 的注解，用来指示映射关系。

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

## 第 3 步：运行代码

本节将逐步介绍代码的运行方法。

### 第 3 步第 1 部分：TiDB Cloud 更改参数

若你使用 TiDB Serverless 集群，更改 `gorm.go` 内 `dsn` 参数值：

```go
dsn := "root:@tcp(127.0.0.1:4000)/test?charset=utf8mb4"
```

若你设定的密码为 `123456`，而且从 TiDB Serverless 集群面板中得到的连接信息为：

- Endpoint: `xxx.tidbcloud.com`
- Port: `4000`
- User: `2aEp24QWEDLqRFs.root`

那么此处应将 `dsn` 更改为：

```go
dsn := "2aEp24QWEDLqRFs.root:123456@tcp(xxx.tidbcloud.com:4000)/test?charset=utf8mb4&tls=true"
```

### 第 3 步第 2 部分：运行

你可以分别运行 `make build` 和 `make run` 以运行此代码：

```shell
make build # this command executes `go build -o bin/gorm-example`
make run # this command executes `./bin/gorm-example`
```

或者你也可以直接使用原生的命令：

```shell
go build -o bin/gorm-example
./bin/gorm-example
```

再或者直接运行 `make all` 命令，这是 `make build` 和 `make run` 的组合。

## 第 4 步：预期输出

[GORM 预期输出](https://github.com/pingcap-inc/tidb-example-golang/blob/main/Expected-Output.md#gorm)
