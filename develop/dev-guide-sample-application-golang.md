---
title: Build a Simple CRUD App with TiDB and Golang
summary: Learn how to build a simple CRUD application with TiDB and Golang.
aliases: ['/tidb/dev/dev-guide-outdated-for-go-sql-driver-mysql','/tidb/dev/dev-guide-outdated-for-gorm']
---

<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD029 -->

# Build a Simple CRUD App with TiDB and Golang

This document describes how to use TiDB and Golang to build a simple CRUD application.

> **Note:**
>
> It is recommended to use Golang 1.16 or a later version.

## Step 1. Launch your TiDB cluster

The following introduces how to start a TiDB cluster.

### Use a TiDB Cloud free cluster

For detailed steps, see [Create a free cluster](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-free-cluster).

### Use a local cluster

For detailed steps, see [Deploy a local test cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) or [Deploy a TiDB Cluster Using TiUP](/production-deployment-using-tiup.md).

## Step 2. Get the code

{{< copyable "shell-regular" >}}

```shell
git clone https://github.com/pingcap-inc/tidb-example-golang.git
```

<SimpleTab>

<div label="Using go-sql-driver/mysql" href="get-code-sql-driver">

Change to the `sqldriver` directory:

{{< copyable "shell-regular" >}}

```shell
cd sqldriver
```

The structure of this directory is as follows:

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

You can find initialization statements for the table creation in `dbinit.sql`:

{{< copyable "sql" >}}

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

`sqldriver.go` is the main body of the `sqldriver`. TiDB is highly compatible with the MySQL protocol, so you need to initialize a MySQL source instance `db, err := sql.Open("mysql", dsn)` to connect to TiDB. Then, you can use `dao.go` to read, edit, add, and delete data.

{{< copyable "" >}}

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

To adapt TiDB transactions, write a toolkit [util](https://github.com/pingcap-inc/tidb-example-golang/tree/main/util) according to the following code:

{{< copyable "" >}}

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

`dao.go` defines a set of data manipulation methods to provide the ability to write data. This is also the core part of this example.

{{< copyable "" >}}

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

`sql.go` defines SQL statements as constants:

{{< copyable "" >}}

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

</div>

<div label="Using GORM (Recommended)" href="get-code-gorm">

Compared with GORM, the go-sql-driver/mysql implementation might be not a best practice, because you need to write error handling logic, close `*sql.Rows` manually and cannot reuse code easily, which makes your code slightly redundant.

GORM is a popular open-source ORM library for Golang. The following instructions take `v1.23.5` as an example.

To adapt TiDB transactions, write a toolkit [util](https://github.com/pingcap-inc/tidb-example-golang/tree/main/util) according to the following code:

{{< copyable "" >}}

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

Change to the `gorm` directory:

{{< copyable "shell-regular" >}}

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

{{< copyable "" >}}

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

</div>

</SimpleTab>

## Step 3. Run the code

The following content introduces how to run the code step by step.

### Step 3.1 Table initialization

<SimpleTab>

<div label="Using go-sql-driver/mysql" href="sql-driver-table-init-sql-driver">

When using go-sql-driver/mysql, you need to initialize the database tables manually. If you are using a local cluster, and MySQL client has been installed locally, you can run it directly in the `sqldriver` directory:

{{< copyable "shell-regular" >}}

```shell
make mysql
```

Or you can execute the following command:

{{< copyable "shell-regular" >}}

```shell
mysql --host 127.0.0.1 --port 4000 -u root<sql/dbinit.sql
```

If you are using a non-local cluster or MySQL client has not been installed, connect to your cluster and run the statement in the `sql/dbinit.sql` file.

</div>

<div label="Using GORM (Recommended)" href="sql-driver-table-init-gorm">

No need to initialize tables manually.

</div>

</SimpleTab>

### Step 3.2 Modify parameters for TiDB Cloud

<SimpleTab>

<div label="Using go-sql-driver/mysql" href="tidb-cloud-sql-driver">

If you are using a non-local default cluster, such as TiDB Cloud or other remote clusters, modify the value of the `dsn` in `sqldriver.go`:

{{< copyable "" >}}

```go
dsn := "root:@tcp(127.0.0.1:4000)/test?charset=utf8mb4"
```

Suppose that the password you set is `123456` and the connection string you get from TiDB Cloud is the following:

```
mysql --connect-timeout 15 -u root -h xxx.tidbcloud.com -P 4000 -p
```

In this case, you can modify the parameters as follows:

{{< copyable "" >}}

```go
dsn := "root:123456@tcp(xxx.tidbcloud.com:4000)/test?charset=utf8mb4"
```

</div>

<div label="Using GORM (Recommended)" href="tidb-cloud-gorm">

If you are using a non-local default cluster, such as TiDB Cloud or other remote clusters, modify the value of the `dsn` in `gorm.go`:

{{< copyable "" >}}

```go
dsn := "root:@tcp(127.0.0.1:4000)/test?charset=utf8mb4"
```

Suppose that the password you set is `123456` and the connection string you get from TiDB Cloud is the following:

```
mysql --connect-timeout 15 -u root -h xxx.tidbcloud.com -P 4000 -p
```

In this case, you can modify the parameters as follows:

{{< copyable "" >}}

```go
dsn := "root:123456@tcp(xxx.tidbcloud.com:4000)/test?charset=utf8mb4"
```

</div>

</SimpleTab>

### Step 3.3 Run

<SimpleTab>

<div label="Using go-sql-driver/mysql" href="run-sql-driver">

To run the code, you can run `make mysql`, `make build` and `make run` respectively:

{{< copyable "shell" >}}

```shell
make mysql # this command executes `mysql --host 127.0.0.1 --port 4000 -u root<sql/dbinit.sql`
make build # this command executes `go build -o bin/sql-driver-example`
make run # this command executes `./bin/sql-driver-example`
```

Or you can use the native commands:

{{< copyable "shell" >}}

```shell
mysql --host 127.0.0.1 --port 4000 -u root<sql/dbinit.sql
go build -o bin/sql-driver-example
./bin/sql-driver-example
```

Or run the `make all` command directly, which is a combination of `make mysql`, `make build` and `make run`.

</div>

<div label="Using GORM (Recommended)" href="run-gorm">

To run the code, you can run `make build` and `make run` respectively:

{{< copyable "shell" >}}

```shell
make build # this command executes `go build -o bin/gorm-example`
make run # this command executes `./bin/gorm-example`
```

Or you can use the native commands:

{{< copyable "shell" >}}

```shell
go build -o bin/gorm-example
./bin/gorm-example
```

Or run the `make` command directly, which is a combination of `make build` and `make run`.

</div>

</SimpleTab>

## Step 4. Expected output

<SimpleTab>

<div label="Using go-sql-driver/mysql" href="output-sql-driver">

[go-sql-driver/mysql Expected Output](https://github.com/pingcap-inc/tidb-example-golang/blob/main/Expected-Output.md#sqldriver)

</div>

<div label="Using GORM (Recommended)" href="output-gorm">

[GORM Expected Output](https://github.com/pingcap-inc/tidb-example-golang/blob/main/Expected-Output.md#gorm)

</div>

</SimpleTab>
