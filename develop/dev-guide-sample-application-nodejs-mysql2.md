---
title: TiDB 和 node-mysql2 的简单 CRUD 应用程序
summary: 给出一个 TiDB 和 node-mysql2 的简单 CRUD 应用程序示例。
---

<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD029 -->

# TiDB 和 Node.js 的简单 CRUD 应用程序

[node-mysql2](https://github.com/sidorares/node-mysql2) 为当前比较流行的开源 Node.js Driver 之一。此处将以 node-mysql2 **3.5.2** 版本进行说明。

本文档将展示如何使用 TiDB 和 node-mysql2 来构造一个简单的 CRUD 应用程序。

> **注意：**
> 推荐使用 Node.js 18.x 及以上版本进行 TiDB 的应用程序的编写。

## 第 1 步：启动你的 TiDB 集群

本节将介绍 TiDB 集群的启动方法。

<SimpleTab groupId="cluster">

<div label="TiDB Cloud" value="serverless-cluster">

[创建 TiDB Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md#第-1-步创建-tidb-serverless-集群)。

</div>

<div label="本地集群" value="local-cluster">

你可以部署一个本地测试的 TiDB 集群或正式的 TiDB 集群。详细步骤，请参考：

- [部署本地测试 TiDB 集群](/quick-start-with-tidb.md#部署本地测试集群)
- [部署正式 TiDB 集群](/production-deployment-using-tiup.md)

</div>

</SimpleTab>

## 第 2 步：获取代码

通过 Git 命令将示例代码拉取到本地：

```shell
git clone https://github.com/pingcap/tidb-example-nodejs.git --depth=1
cd tidb-example-nodejs
```

该示例的代码位于代码仓库中的 `node_mysql2/src/sample/index.js` 文件中，内容如下：

```javascript
import {createConnection} from 'mysql2/promise';
import dotenv from "dotenv";
import {loadSampleData} from "../helper.js";
import path from "path";

// Main function.

async function main() {
    // Load environment variables from .env file.
    dotenv.config();

    // Load sample data.
    const conn = await createConnection(process.env.DATABASE_URL);
    try {
        await loadSampleData(conn, path.join(process.cwd(), 'sql/players.init.sql'));
    } finally {
        await conn.end();
    }

    // Run examples.
    console.log('[Simple Example Output]\n');
    await simple_example();

    console.log('\n[Bulk Example Output]\n');
    await  bulk_example();

    console.log('\n[Trade Example Output]\n');
    await  trade_example();
}

void main();

// Common functions.

async function getConnection() {
    return createConnection(process.env.DATABASE_URL);
}

// Simple example.

async function simple_example() {
    const conn = await getConnection();

    try {
        // Create player.
        const newPlayerID = await createPlayer(conn, {
            coins: 1,
            goods: 1,
        });
        console.log(`Created new player with ID ${newPlayerID}.`);

        // Get player by ID.
        const player = await getPlayerByID(conn, 3);
        console.log(`Get player by ID 3: Player { id:${player.id}, coins:${player.coins}, goods:${player.goods} }`);

        // Delete player by ID.
        await deletePlayerByID(conn, 3);
        console.log(`Deleted player with ID 3.`);

        // Count players.
        const playerTotal = await countPlayers(conn);
        console.log(`The total number of players: ${playerTotal}`);

        // List players with limit.
        console.log('List players with limit 3:')
        const players = await listPlayersWithLimit(conn, 3);
        players.forEach(p => {
            console.log(`- Player { id:${p.id}, coins:${p.coins}, goods:${p.goods} }`);
        });
    } finally {
        await conn.end();
    }
}

async function createPlayer(conn, player) {
    const [rsh] = await conn.execute(
        'INSERT INTO players (id, coins, goods) VALUES (?, ?, ?);',
        [player.id || null, player.coins, player.goods]
    );
    return rsh.insertId;
}

async function getPlayerByID(conn, playerId) {
    const [rows] = await conn.execute(
        'SELECT id, coins, goods FROM players WHERE id = ?;',
        [playerId]
    );
    return rows[0];
}

async function deletePlayerByID(conn, playerId) {
    const [rsh] = await conn.execute(
        'DELETE FROM players WHERE id = ?;',
        [playerId]
    );
    return rsh.affectedRows === 1;
}

async function listPlayersWithLimit(conn, limit) {
    const [rows] = await conn.query('SELECT id, coins, goods FROM players LIMIT ?;', [limit]);
    return rows;
}

async function countPlayers(conn) {
    const [rows] = await conn.execute('SELECT COUNT(*) AS cnt FROM players;');
    return rows[0]?.cnt || null;
}

// Bulk operations example.

async function bulk_example() {
    const conn = await getConnection();
    try {
        // Bulk create players.
        const players = [];
        for (let i = 1000; i < 2000; i++) {
            players.push([i, 10000, 10000]);
        }

        for (let i = 0; i < players.length; i += 200) {
            const chunk = players.slice(i, i + 200);
            const insertedRows = await bulkCreatePlayer(conn, chunk);
            console.log(`Bulk inserted ${insertedRows} rows.`);
        }
    } finally {
        await conn.end();
    }
}

async function bulkCreatePlayer(conn, players) {
    const [rsh] = await conn.query('INSERT INTO players (id, coins, goods) VALUES ?;', [players]);
    return rsh.affectedRows;
}

// Transaction example.

async function trade_example() {
    const conn = await getConnection();

    try {
        // Create players.
        await createPlayer(conn, { id: 101, coins: 100, goods: 0 });
        await createPlayer(conn, { id: 102, coins: 2000, goods: 20 });

        // Trade attempt 1.
        await trade(1, conn, 102, 101, 10, 500);

        // Trade attempt 2.
        await trade(2, conn, 102, 101, 2, 100);

        // Get player status.
        console.log('\nPlayer status after trade:');

        const player1 = await getPlayerByID(conn, 101);
        console.log(`- Player { id:101, coins:${player1.coins}, goods:${player1.goods} }`);

        const player2 = await getPlayerByID(conn, 102);
        console.log(`- Player { id:102, coins:${player2.coins}, goods:${player2.goods} }`);
    } finally {
        await conn.end();
    }
}

async function trade(tradeSeq, conn, sellId, buyId, amount, price) {
    console.log(`[Trade ${tradeSeq}] Doing trade ${amount} goods from player ${sellId} to player ${buyId} for ${price} coins.`)

    // Start transaction.
    await conn.beginTransaction();
    try {
        // Lock rows and check.
        const getPlayerSql = 'SELECT coins, goods FROM players WHERE id = ? FOR UPDATE;';

        const [sellRows] = await conn.execute(getPlayerSql, [sellId]);
        const sellGoods = sellRows[0].goods;
        const sellCoins = sellRows[0].coins;
        if (sellGoods < amount) {
            throw new Error(`The goods of sell player ${sellId} are not enough.`);
        }

        const [buyRows] = await conn.execute(getPlayerSql, [buyId]);
        const buyGoods = buyRows[0].goods;
        const buyCoins = buyRows[0].coins;
        if (buyCoins < price) {
            throw new Error(`The coins of buy player ${buyId} is not enough.`);
        }

        // Update if checks passed.
        const updatePlayerSql = 'UPDATE players SET goods = ?, coins = ? WHERE id = ?;';
        await conn.execute(updatePlayerSql, [sellGoods - amount, sellCoins + price, sellId]);
        await conn.execute(updatePlayerSql, [buyGoods + amount, buyCoins - price, buyId]);

        // Commit transaction.
        await conn.commit();
        console.log(`[Trade ${tradeSeq}] Trade success!`);
    } catch (error) {
        // Rollback transaction.
        await conn.rollback();
        console.error(`[Trade ${tradeSeq}] Trade failed (rollback the transaction): ${error.message}\n`);
    }
}
```

关于 node-mysql2 的更多使用方法，你可以参考 [node-mysql2 官方仓库](https://github.com/sidorares/node-mysql2#mysql-2)。

## 第 3 步：运行代码

本节将逐步介绍代码的运行方法。

### 3.1 配置环境变量

在 `node_mysql2` 目录下新建一个 `.env` 文件，在该文件当中添加环境变量 `DATABASE_URL`。

> **⚠️ 注意：**
> 避免使用生产环境的集群运行代码，示例程序在初始化表结构是会删除已有的 `players` 表。

#### 环境变量 `DATABASE_URL`

<SimpleTab groupId="cluster">

<div label="本地/自托管集群" value="local-cluster">

如果你使用的是本地或者自部署的 TiDB 集群（默认不开启 SSL）你可以按照如下格式填写 `DATABASE_URL`：

```dotenv
DATABASE_URL=mysql://<USERNAME>:<PASSWORD>@<HOST>:<PORT>/<DB_NAME>
```

<details>
<summary>连接 TiUP Playground 集群的 <code>DATABASE_URL</code> 示例</summary>

```dotenv
DATABASE_URL=mysql://root:password@127.0.0.1:4000/test
```

</details>

</div>

<div label="TiDB Cloud Serverless 集群" value="serverless-cluster">

如果你使用的是 TiDB Cloud Serverless 集群，你必须通过 SSL 连接到 TiDB 集群, 因此你需要在 `DATABASE_URL` 中添加 `ssl` 参数，格式如下：

```dotenv
DATABASE_URL=mysql://<USERNAME>:<PASSWORD>@<HOST>:<PORT>/<DB_NAME>?ssl={"minVersion":"TLSv1.2","rejectUnauthorized":true}
```

<details>
<summary>连接 TiDB Serverless 集群的 <code>DATABASE_URL</code> 示例</summary>

```dotenv
DATABASE_URL=mysql://xxxxx.root:password@gateway01.us-west-2.prod.aws.tidbcloud.com:4000/test?ssl={"minVersion":"TLSv1.2","rejectUnauthorized":true}
```

</details>

</div>

</SimpleTab>

### 3.2 安装依赖

在 `node_mysql2` 目录下执行以下命令安装示例代码所需的依赖：

```shell
npm install
```

在你的项目代码当中你可以通过 `npm install mysql2@3.5.2` 命令安装推荐版本的 `mysql2` Driver。

### 3.4 启动示例程序

在 `node_mysql2` 目录下执行以下命令启动示例程序：

```shell
npm run demo:sample
```

## 第 4 步：预期输出

```
[Simple Example Output]

Created new player with ID 9.
Get player by ID 3: Player { id:3, coins:4, goods:256 }
Deleted player with ID 3.
The total number of players: 8
List players with limit 3:
- Player { id:1, coins:1, goods:1024 }
- Player { id:2, coins:2, goods:512 }
- Player { id:4, coins:8, goods:128 }

[Bulk Example Output]

Bulk inserted 200 rows.
Bulk inserted 200 rows.
Bulk inserted 200 rows.
Bulk inserted 200 rows.
Bulk inserted 200 rows.

[Trade Example Output]

[Trade 1] Doing trade 10 goods from player 102 to player 101 for 500 coins.
[Trade 1] Trade failed (rollback the transaction): The coins of buy player 101 is not enough.

[Trade 2] Doing trade 2 goods from player 102 to player 101 for 100 coins.
[Trade 2] Trade success!

Player status after trade:
- Player { id:101, coins:0, goods:2 }
- Player { id:102, coins:2100, goods:18 }
```

[node-mysql2 示例程序的预期输出](https://github.com/pingcap/tidb-example-nodejs/tree/main/node_mysql2/src/sample#expected-output)
