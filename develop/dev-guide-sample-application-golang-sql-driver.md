---
title: TiDB 和 Go-MySQL-Driver 的简单 CRUD 应用程序
summary: 给出一个 TiDB 和 Go-MySQL-Driver 的简单 CRUD 应用程序示例。
aliases: ['/zh/tidb/v7.2/dev-guide-sample-application-golang']
---

<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD029 -->

# TiDB 和 Go-MySQL-Driver 的简单 CRUD 应用程序

本文档将展示如何使用 TiDB 和 [Go-MySQL-Driver](https://github.com/go-sql-driver/mysql) 来构造一个简单的 CRUD 应用程序。

> **注意：**
>
> 推荐使用 Golang 1.16 以上版本进行 TiDB 的应用程序的编写。

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

进入目录 `sqldriver`：

```shell
cd sqldriver
```

目录结构如下所示：

```
.
├── Makefile
├── dao.go
├── go.mod
├── go.sum
├── sql
│   └── dbinit.sql
├── sql.go
└── sqldriver.go
```

其中，`dbinit.sql` 为数据表初始化语句：

```sql
USE test;
DROP TABLE IF EXISTS player;

CREATE TABLE player (
    `id` VARCHAR(36),
    `coins` INTEGER,
    `goods` INTEGER,
   PRIMARY KEY (`id`)
);
```

`sqldriver.go` 是 `sqldriver` 这个示例程序的主体。与 GORM 对比，go-sql-driver/mysql 的实现方式并非最优体验。你需要自行编写错误处理逻辑，手动关闭 `*sql.Rows`，并且代码无法简单复用。这会使你的代码有些冗余。因为 TiDB 与 MySQL 协议兼容，因此，需要初始化一个 MySQL 协议的数据源 `db, err := sql.Open("mysql", dsn)`，以此连接到 TiDB。并在其后，调用 `dao.go` 中的一系列方法，用来管理数据对象，进行增删改查等操作。

```go
package main

import (
    "database/sql"
    "fmt"

    _ "github.com/go-sql-driver/mysql"
)

func main() {
    // 1. Configure the example database connection.
    dsn := "root:@tcp(127.0.0.1:4000)/test?charset=utf8mb4"
    openDB("mysql", dsn, func(db *sql.DB) {
        // 2. Run some simple examples.
        simpleExample(db)

        // 3. Explore more.
        tradeExample(db)
    })
}

func simpleExample(db *sql.DB) {
    // Create a player, who has a coin and a goods.
    err := createPlayer(db, Player{ID: "test", Coins: 1, Goods: 1})
    if err != nil {
        panic(err)
    }

    // Get a player.
    testPlayer, err := getPlayer(db, "test")
    if err != nil {
        panic(err)
    }
    fmt.Printf("getPlayer: %+v\n", testPlayer)

    // Create players with bulk inserts. Insert 1919 players totally, with 114 players per batch.

    err = bulkInsertPlayers(db, randomPlayers(1919), 114)
    if err != nil {
        panic(err)
    }

    // Count players amount.
    playersCount, err := getCount(db)
    if err != nil {
        panic(err)
    }
    fmt.Printf("countPlayers: %d\n", playersCount)

    // Print 3 players.
    threePlayers, err := getPlayerByLimit(db, 3)
    if err != nil {
        panic(err)
    }
    for index, player := range threePlayers {
        fmt.Printf("print %d player: %+v\n", index+1, player)
    }
}

func tradeExample(db *sql.DB) {
    // Player 1: id is "1", has only 100 coins.
    // Player 2: id is "2", has 114514 coins, and 20 goods.
    player1 := Player{ID: "1", Coins: 100}
    player2 := Player{ID: "2", Coins: 114514, Goods: 20}

    // Create two players "by hand", using the INSERT statement on the backend.
    if err := createPlayer(db, player1); err != nil {
        panic(err)
    }
    if err := createPlayer(db, player2); err != nil {
        panic(err)
    }

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

func openDB(driverName, dataSourceName string, runnable func(db *sql.DB)) {
    db, err := sql.Open(driverName, dataSourceName)
    if err != nil {
        panic(err)
    }
    defer db.Close()

    runnable(db)
}
```

随后，封装一个用于适配 TiDB 事务的工具包 [util](https://github.com/pingcap-inc/tidb-example-golang/tree/main/util)，编写以下代码备用：

```go
package util

import (
    "context"
    "database/sql"
)

type TiDBSqlTx struct {
    *sql.Tx
    conn        *sql.Conn
    pessimistic bool
}

func TiDBSqlBegin(db *sql.DB, pessimistic bool) (*TiDBSqlTx, error) {
    ctx := context.Background()
    conn, err := db.Conn(ctx)
    if err != nil {
        return nil, err
    }
    if pessimistic {
        _, err = conn.ExecContext(ctx, "set @@tidb_txn_mode=?", "pessimistic")
    } else {
        _, err = conn.ExecContext(ctx, "set @@tidb_txn_mode=?", "optimistic")
    }
    if err != nil {
        return nil, err
    }
    tx, err := conn.BeginTx(ctx, nil)
    if err != nil {
        return nil, err
    }
    return &TiDBSqlTx{
        conn:        conn,
        Tx:          tx,
        pessimistic: pessimistic,
    }, nil
}

func (tx *TiDBSqlTx) Commit() error {
    defer tx.conn.Close()
    return tx.Tx.Commit()
}

func (tx *TiDBSqlTx) Rollback() error {
    defer tx.conn.Close()
    return tx.Tx.Rollback()
}
```

在 `dao.go` 中定义一系列数据的操作方法，用来对提供数据的写入能力。这也是本例子中核心部分。

```go
package main

import (
    "database/sql"
    "fmt"
    "math/rand"
    "strings"

    "github.com/google/uuid"
    "github.com/pingcap-inc/tidb-example-golang/util"
)

type Player struct {
    ID    string
    Coins int
    Goods int
}

// createPlayer create a player
func createPlayer(db *sql.DB, player Player) error {
    _, err := db.Exec(CreatePlayerSQL, player.ID, player.Coins, player.Goods)
    return err
}

// getPlayer get a player
func getPlayer(db *sql.DB, id string) (Player, error) {
    var player Player

    rows, err := db.Query(GetPlayerSQL, id)
    if err != nil {
        return player, err
    }
    defer rows.Close()

    if rows.Next() {
        err = rows.Scan(&player.ID, &player.Coins, &player.Goods)
        if err == nil {
            return player, nil
        } else {
            return player, err
        }
    }

    return player, fmt.Errorf("can not found player")
}

// getPlayerByLimit get players by limit
func getPlayerByLimit(db *sql.DB, limit int) ([]Player, error) {
    var players []Player

    rows, err := db.Query(GetPlayerByLimitSQL, limit)
    if err != nil {
        return players, err
    }
    defer rows.Close()

    for rows.Next() {
        player := Player{}
        err = rows.Scan(&player.ID, &player.Coins, &player.Goods)
        if err == nil {
            players = append(players, player)
        } else {
            return players, err
        }
    }

    return players, nil
}

// bulk-insert players
func bulkInsertPlayers(db *sql.DB, players []Player, batchSize int) error {
    tx, err := util.TiDBSqlBegin(db, true)
    if err != nil {
        return err
    }

    stmt, err := tx.Prepare(buildBulkInsertSQL(batchSize))
    if err != nil {
        return err
    }

    defer stmt.Close()

    for len(players) > batchSize {
        if _, err := stmt.Exec(playerToArgs(players[:batchSize])...); err != nil {
            tx.Rollback()
            return err
        }

        players = players[batchSize:]
    }

    if len(players) != 0 {
        if _, err := tx.Exec(buildBulkInsertSQL(len(players)), playerToArgs(players)...); err != nil {
            tx.Rollback()
            return err
        }
    }

    if err := tx.Commit(); err != nil {
        tx.Rollback()
        return err
    }

    return nil
}

func getCount(db *sql.DB) (int, error) {
    count := 0

    rows, err := db.Query(GetCountSQL)
    if err != nil {
        return count, err
    }

    defer rows.Close()

    if rows.Next() {
        if err := rows.Scan(&count); err != nil {
            return count, err
        }
    }

    return count, nil
}

func buyGoods(db *sql.DB, sellID, buyID string, amount, price int) error {
    var sellPlayer, buyPlayer Player

    tx, err := util.TiDBSqlBegin(db, true)
    if err != nil {
        return err
    }

    buyExec := func() error {
        stmt, err := tx.Prepare(GetPlayerWithLockSQL)
        if err != nil {
            return err
        }
        defer stmt.Close()

        sellRows, err := stmt.Query(sellID)
        if err != nil {
            return err
        }
        defer sellRows.Close()

        if sellRows.Next() {
            if err := sellRows.Scan(&sellPlayer.ID, &sellPlayer.Coins, &sellPlayer.Goods); err != nil {
                return err
            }
        }
        sellRows.Close()

        if sellPlayer.ID != sellID || sellPlayer.Goods < amount {
            return fmt.Errorf("sell player %s goods not enough", sellID)
        }

        buyRows, err := stmt.Query(buyID)
        if err != nil {
            return err
        }
        defer buyRows.Close()

        if buyRows.Next() {
            if err := buyRows.Scan(&buyPlayer.ID, &buyPlayer.Coins, &buyPlayer.Goods); err != nil {
                return err
            }
        }
        buyRows.Close()

        if buyPlayer.ID != buyID || buyPlayer.Coins < price {
            return fmt.Errorf("buy player %s coins not enough", buyID)
        }

        updateStmt, err := tx.Prepare(UpdatePlayerSQL)
        if err != nil {
            return err
        }
        defer updateStmt.Close()

        if _, err := updateStmt.Exec(-amount, price, sellID); err != nil {
            return err
        }

        if _, err := updateStmt.Exec(amount, -price, buyID); err != nil {
            return err
        }

        return nil
    }

    err = buyExec()
    if err == nil {
        fmt.Println("\n[buyGoods]:\n    'trade success'")
        tx.Commit()
    } else {
        tx.Rollback()
    }

    return err
}

func playerToArgs(players []Player) []interface{} {
    var args []interface{}
    for _, player := range players {
        args = append(args, player.ID, player.Coins, player.Goods)
    }
    return args
}

func buildBulkInsertSQL(amount int) string {
    return CreatePlayerSQL + strings.Repeat(",(?,?,?)", amount-1)
}

func randomPlayers(amount int) []Player {
    players := make([]Player, amount, amount)
    for i := 0; i < amount; i++ {
        players[i] = Player{
            ID:    uuid.New().String(),
            Coins: rand.Intn(10000),
            Goods: rand.Intn(10000),
        }
    }

    return players
}
```

`sql.go` 中存放了 SQL 语句的常量。

```go
package main

const (
    CreatePlayerSQL      = "INSERT INTO player (id, coins, goods) VALUES (?, ?, ?)"
    GetPlayerSQL         = "SELECT id, coins, goods FROM player WHERE id = ?"
    GetCountSQL          = "SELECT count(*) FROM player"
    GetPlayerWithLockSQL = GetPlayerSQL + " FOR UPDATE"
    UpdatePlayerSQL      = "UPDATE player set goods = goods + ?, coins = coins + ? WHERE id = ?"
    GetPlayerByLimitSQL  = "SELECT id, coins, goods FROM player LIMIT ?"
)
```

## 第 3 步：运行代码

本节将逐步介绍代码的运行方法。

### 第 3 步第 1 部分：表初始化

使用 go-sql-driver/mysql 时，需手动初始化数据库表，若你本地已经安装了 `mysql-client`，且使用本地集群，可直接在 `sqldriver` 目录下运行：

```shell
make mysql
```

或直接执行：

```shell
mysql --host 127.0.0.1 --port 4000 -u root<sql/dbinit.sql
```

若你不使用本地集群，或未安装 **mysql-client**，请直接登录你的集群，并运行 `sql/dbinit.sql` 文件内的 SQL 语句。

### 第 3 步第 2 部分：TiDB Cloud 更改参数

若你使用 TiDB Serverless 集群，更改 `sqldriver.go` 内 `dsn` 参数的值：

```go
dsn := "root:@tcp(127.0.0.1:4000)/test?charset=utf8mb4"
```

若你设定的密码为 `123456`，而且从 TiDB Serverless 集群面板中得到的连接信息为：

- Endpoint: `xxx.tidbcloud.com`
- Port: `4000`
- User: `2aEp24QWEDLqRFs.root`

那么此处应将 `mysql.RegisterTLSConfig` 和 `dsn` 更改为：

```go
mysql.RegisterTLSConfig("register-tidb-tls", &tls.Config {
    MinVersion: tls.VersionTLS12,
    ServerName: "xxx.tidbcloud.com",
})

dsn := "2aEp24QWEDLqRFs.root:123456@tcp(xxx.tidbcloud.com:4000)/test?charset=utf8mb4&tls=register-tidb-tls"
```

### 第 3 步第 3 部分：运行

你可以分别运行 `make mysql`, `make build` 和 `make run` 以运行此代码：

```shell
make mysql # this command executes `mysql --host 127.0.0.1 --port 4000 -u root<sql/dbinit.sql`
make build # this command executes `go build -o bin/sql-driver-example`
make run # this command executes `./bin/sql-driver-example`
```

或者你也可以直接使用原生的命令：

```shell
mysql --host 127.0.0.1 --port 4000 -u root<sql/dbinit.sql
go build -o bin/sql-driver-example
./bin/sql-driver-example
```

再或者直接运行 `make all` 命令，这是 `make mysql`, `make build` 和 `make run` 的组合。

## 第 4 步：预期输出

[go-sql-driver/mysql 预期输出](https://github.com/pingcap-inc/tidb-example-golang/blob/main/Expected-Output.md#sqldriver)
