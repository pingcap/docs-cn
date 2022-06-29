---
title: TiDB 和 Golang 的简单 CRUD 应用程序
summary: 给出一个 TiDB 和 Golang 的简单 CRUD 应用程序示例。
---

<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD029 -->

# TiDB 和 Golang 的简单 CRUD 应用程序

本文档将展示如何使用 TiDB 和 Golang 来构造一个简单的 CRUD 应用程序。

> **注意：**
>
> 推荐使用 Golang 1.16 以上版本进行 TiDB 的应用程序的编写。

## 第 1 步：启动你的 TiDB 集群

本节将介绍 TiDB 集群的启动方法。

### 使用 TiDB Cloud 免费集群

[创建免费集群](/develop/dev-guide-build-cluster-in-cloud.md#第-1-步创建免费集群)。

### 使用本地集群

你可以部署一个本地测试的 TiDB 集群或正式的 TiDB 集群。详细步骤，请参考：

- [部署本地测试 TiDB 集群](/quick-start-with-tidb.md#部署本地测试集群)
- [部署正式 TiDB 集群](/production-deployment-using-tiup.md)。

### 使用云原生开发环境

基于 Git 的预配置的开发环境: [现在就试试](/develop/dev-guide-playground-gitpod.md)

该环境会自动克隆代码，并通过 TiUP 部署测试集群。

## 第 2 步：获取代码

{{< copyable "shell-regular" >}}

```shell
git clone https://github.com/pingcap-inc/tidb-example-golang.git
```

<SimpleTab>

<div label="使用 go-sql-driver/mysql" href="get-code-sql-driver">

进入目录 `sqldriver`：

{{< copyable "shell-regular" >}}

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

`sqldriver.go` 是 `sqldriver` 这个示例程序的主体。因为 TiDB 与 MySQL 协议兼容，因此，需要初始化一个 MySQL 协议的数据源 `db, err := sql.Open("mysql", dsn)`，以此连接到 TiDB。并在其后，调用 `dao.go` 中的一系列方法，用来管理数据对象，进行增删改查等操作。

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

随后，封装一个用于适配 TiDB 事务的工具包 [util](https://github.com/pingcap-inc/tidb-example-golang/tree/main/util)，编写以下代码备用：

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

在 `dao.go` 中定义一系列数据的操作方法，用来对提供数据的写入能力。这也是本例子中和核心部分。

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

`sql.go` 中存放了 SQL 语句的常量。

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

<div label="使用 gorm（推荐）" href="get-code-gorm">

可以看到，go-sql-driver/mysql 实现的代码略显冗余，需要自己管控错误处理逻辑，手动关闭 `*sql.Rows`，且不能很好的复用代码。并非最佳实践。

当前开源比较流行的 Golang ORM 为 gorm（推荐），此处将以 v1.23.5 版本进行说明。

封装一个用于适配 TiDB 事务的工具包 [util](https://github.com/pingcap-inc/tidb-example-golang/tree/main/util)，编写以下代码备用：

{{< copyable "" >}}

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

进入目录 `gorm` ：

{{< copyable "shell-regular" >}}

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

其中，`gorm.go` 是 `gorm` 这个示例程序的主体。使用 gorm 时，相较于 go-sql-driver/mysql，gorm 屏蔽了创建数据库连接时，不同数据库差异的细节，其还封装了大量的操作，如 AutoMigrate、基本对象的 CRUD 等，极大的简化了代码量。

`Player` 是数据结构体，为数据库表在程序内的映射。`Player` 的每个属性都对应着 `player` 表的一个字段。相较于 go-sql-driver/mysql，gorm 的 `Player` 数据结构体为了给 gorm 提供更多的信息，加入了形如 `` `gorm:"primaryKey;type:VARCHAR(36);column:id"` `` 的注解，用来指示映射关系。

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
    // Create a player, who has a coin and a goods..
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

## 第 3 步：运行代码

本节将逐步介绍代码的运行方法。

### 第 3 步第 1 部分：go-sql-driver/mysql 表初始化

<SimpleTab>

<div label="使用 go-sql-driver/mysql" href="sql-driver-table-init-sql-driver">

> 在 Gitpod Playground 中尝试 go-sql-driver/mysql: [现在就试试](https://gitpod.io/#targetMode=sqldriver/https://github.com/pingcap-inc/tidb-example-golang)

使用 go-sql-driver/mysql 时，需手动初始化数据库表，若你本地已经安装了 `mysql-client`，且使用本地集群，可直接在 `sqldriver` 目录下运行：

{{< copyable "shell-regular" >}}

```shell
make mysql
```

或直接执行：

{{< copyable "shell-regular" >}}

```shell
mysql --host 127.0.0.1 --port 4000 -u root<sql/dbinit.sql
```

若你不使用本地集群，或未安装 **mysql-client**，请直接登录你的集群，并运行 `sql/dbinit.sql` 文件内的 SQL 语句。

</div>

<div label="使用 gorm（推荐）" href="sql-driver-table-init-gorm">

> 在 Gitpod Playground 中尝试 gorm: [现在就试试](https://gitpod.io/#targetMode=gorm/https://github.com/pingcap-inc/tidb-example-golang)

无需手动初始化表。

</div>

</SimpleTab>

### 第 3 步第 2 部分：TiDB Cloud 更改参数

<SimpleTab>

<div label="使用 go-sql-driver/mysql" href="tidb-cloud-sql-driver">

若你使用非本地默认集群、TiDB Cloud 或其他远程集群，更改 `sqldriver.go` 内 `dsn` 参数的值：

{{< copyable "" >}}

```go
dsn := "root:@tcp(127.0.0.1:4000)/test?charset=utf8mb4"
```

若你设定的密码为 `123456`，而且从 TiDB Cloud 得到的连接字符串为：

```
mysql --connect-timeout 15 -u root -h xxx.tidbcloud.com -P 4000 -p
```

那么此处应将参数更改为：

{{< copyable "" >}}

```go
dsn := "root:123456@tcp(xxx.tidbcloud.com:4000)/test?charset=utf8mb4"
```

</div>

<div label="使用 gorm（推荐）" href="tidb-cloud-gorm">

若你使用非本地默认集群、TiDB Cloud 或其他远程集群，更改 `gorm.go` 内 `dsn` 参数值：

{{< copyable "" >}}

```go
dsn := "root:@tcp(127.0.0.1:4000)/test?charset=utf8mb4"
```

若你设定的密码为 `123456`，而且从 TiDB Cloud 得到的连接字符串为：

```
mysql --connect-timeout 15 -u root -h xxx.tidbcloud.com -P 4000 -p
```

那么此处应将参数更改为：

{{< copyable "" >}}

```go
dsn := "root:123456@tcp(xxx.tidbcloud.com:4000)/test?charset=utf8mb4"
```

</div>

</SimpleTab>

### 第 3 步第 3 部分：运行

<SimpleTab>

<div label="使用 go-sql-driver/mysql" href="run-sql-driver">

运行 `make all`，这是以下三个操作的组合：

- 创建表 (make mysql)：`mysql --host 127.0.0.1 --port 4000 -u root<sql/dbinit.sql`
- 构建二进制 (make build)： `go build -o bin/sql-driver-example`
- 运行 (make run)： `./bin/sql-driver-example`

你也可以单独运行这三个 make 命令或原生命令。

</div>

<div label="使用 gorm（推荐）" href="run-gorm">

运行 `make all`，这是以下两个操作的组合：

- 构建二进制 (make build)：`go build -o bin/gorm-example`
- 运行 (make run)：`./bin/gorm-example`

你也可以单独运行这两个 make 命令或原生命令。

</div>

</SimpleTab>

## 第 4 步：预期输出

<SimpleTab>

<div label="使用 go-sql-driver/mysql" href="output-sql-driver">

[go-sql-driver/mysql 预期输出](https://github.com/pingcap-inc/tidb-example-golang/blob/main/Expected-Output.md#sqldriver)

</div>

<div label="使用 gorm（推荐）" href="output-gorm">

[gorm 预期输出](https://github.com/pingcap-inc/tidb-example-golang/blob/main/Expected-Output.md#gorm)

</div>

</SimpleTab>
