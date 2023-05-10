---
title: Build a Simple CRUD App with TiDB and mysqlclient
summary: Learn how to build a simple CRUD application with TiDB and mysqlclient.
---

<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD029 -->

# Build a Simple CRUD App with TiDB and mysqlclient

[mysqlclient](https://pypi.org/project/mysqlclient/) is a popular open-source driver for Python.

This document describes how to use TiDB and mysqlclient to build a simple CRUD application.

> **Note:**
>
> It is recommended to use Python 3.10 or a later Python version.

## Step 1. Launch your TiDB cluster

<CustomContent platform="tidb">

The following introduces how to start a TiDB cluster.

**Use a TiDB Cloud Serverless Tier cluster**

For detailed steps, see [Create a Serverless Tier cluster](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-serverless-tier-cluster).

**Use a local cluster**

For detailed steps, see [Deploy a local test cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) or [Deploy a TiDB cluster using TiUP](/production-deployment-using-tiup.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

See [Create a Serverless Tier cluster](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-serverless-tier-cluster).

</CustomContent>

## Step 2. Get the code

```shell
git clone https://github.com/pingcap-inc/tidb-example-python.git
```

The following uses mysqlclient 2.1.1 as an example. Drivers for Python are more convenient to use than other languages, but they do not shield the underlying implementation and require manual management of transactions. If there are not a lot of scenarios where SQL is required, it is recommended to use ORM, which can help reduce the coupling of your program.

```python
import uuid
from typing import List

import MySQLdb
from MySQLdb import Connection
from MySQLdb.cursors import Cursor

def get_connection(autocommit: bool = True) -> MySQLdb.Connection:
    return MySQLdb.connect(
        host="127.0.0.1",
        port=4000,
        user="root",
        password="",
        database="test",
        autocommit=autocommit
    )


def create_player(cursor: Cursor, player: tuple) -> None:
    cursor.execute("INSERT INTO player (id, coins, goods) VALUES (%s, %s, %s)", player)


def get_player(cursor: Cursor, player_id: str) -> tuple:
    cursor.execute("SELECT id, coins, goods FROM player WHERE id = %s", (player_id,))
    return cursor.fetchone()


def get_players_with_limit(cursor: Cursor, limit: int) -> List[tuple]:
    cursor.execute("SELECT id, coins, goods FROM player LIMIT %s", (limit,))
    return cursor.fetchall()


def random_player(amount: int) -> List[tuple]:
    players = []
    for _ in range(amount):
        players.append((uuid.uuid4(), 10000, 10000))

    return players


def bulk_create_player(cursor: Cursor, players: List[tuple]) -> None:
    cursor.executemany("INSERT INTO player (id, coins, goods) VALUES (%s, %s, %s)", players)


def get_count(cursor: Cursor) -> None:
    cursor.execute("SELECT count(*) FROM player")
    return cursor.fetchone()[0]


def trade_check(cursor: Cursor, sell_id: str, buy_id: str, amount: int, price: int) -> bool:
    get_player_with_lock_sql = "SELECT coins, goods FROM player WHERE id = %s FOR UPDATE"

    # sell player goods check
    cursor.execute(get_player_with_lock_sql, (sell_id,))
    _, sell_goods = cursor.fetchone()
    if sell_goods < amount:
        print(f'sell player {sell_id} goods not enough')
        return False

    # buy player coins check
    cursor.execute(get_player_with_lock_sql, (buy_id,))
    buy_coins, _ = cursor.fetchone()
    if buy_coins < price:
        print(f'buy player {buy_id} coins not enough')
        return False


def trade_update(cursor: Cursor, sell_id: str, buy_id: str, amount: int, price: int) -> None:
    update_player_sql = "UPDATE player set goods = goods + %s, coins = coins + %s WHERE id = %s"

    # deduct the goods of seller, and raise his/her the coins
    cursor.execute(update_player_sql, (-amount, price, sell_id))
    # deduct the coins of buyer, and raise his/her the goods
    cursor.execute(update_player_sql, (amount, -price, buy_id))


def trade(connection: Connection, sell_id: str, buy_id: str, amount: int, price: int) -> None:
    with connection.cursor() as cursor:
        if trade_check(cursor, sell_id, buy_id, amount, price) is False:
            connection.rollback()
            return

        try:
            trade_update(cursor, sell_id, buy_id, amount, price)
        except Exception as err:
            connection.rollback()
            print(f'something went wrong: {err}')
        else:
            connection.commit()
            print("trade success")


def simple_example() -> None:
    with get_connection(autocommit=True) as conn:
        with conn.cursor() as cur:
            # create a player, who has a coin and a goods.
            create_player(cur, ("test", 1, 1))

            # get this player, and print it.
            test_player = get_player(cur, "test")
            print(f'id:{test_player[0]}, coins:{test_player[1]}, goods:{test_player[2]}')

            # create players with bulk inserts.
            # insert 1919 players totally, with 114 players per batch.
            # each player has a random UUID
            player_list = random_player(1919)
            for idx in range(0, len(player_list), 114):
                bulk_create_player(cur, player_list[idx:idx + 114])

            # print the number of players
            count = get_count(cur)
            print(f'number of players: {count}')

            # print 3 players.
            three_players = get_players_with_limit(cur, 3)
            for player in three_players:
                print(f'id:{player[0]}, coins:{player[1]}, goods:{player[2]}')


def trade_example() -> None:
    with get_connection(autocommit=False) as conn:
        with conn.cursor() as cur:
            # create two players
            # player 1: id is "1", has only 100 coins.
            # player 2: id is "2", has 114514 coins, and 20 goods.
            create_player(cur, ("1", 100, 0))
            create_player(cur, ("2", 114514, 20))
            conn.commit()

        # player 1 wants to buy 10 goods from player 2.
        # it will cost 500 coins, but player 1 cannot afford it.
        # so this trade will fail, and nobody will lose their coins or goods
        trade(conn, sell_id="2", buy_id="1", amount=10, price=500)

        # then player 1 has to reduce the incoming quantity to 2.
        # this trade will be successful
        trade(conn, sell_id="2", buy_id="1", amount=2, price=100)

        # let's take a look for player 1 and player 2 currently
        with conn.cursor() as cur:
            _, player1_coin, player1_goods = get_player(cur, "1")
            print(f'id:1, coins:{player1_coin}, goods:{player1_goods}')
            _, player2_coin, player2_goods = get_player(cur, "2")
            print(f'id:2, coins:{player2_coin}, goods:{player2_goods}')


simple_example()
trade_example()
```

The driver has a lower level of encapsulation than ORM, so there are a lot of SQL statements in the program. Unlike ORM, there is no data object in drivers, so the `Player` queried by the driver is represented as a tuple.

For more information about how to use mysqlclient, refer to [mysqlclient documentation](https://mysqlclient.readthedocs.io/).

## Step 3. Run the code

The following content introduces how to run the code step by step.

### Step 3.1 Initialize table

Before running the code, you need to initialize the table manually. If you are using a local TiDB cluster, you can run the following command:

<SimpleTab groupId="cli">

<div label="MySQL CLI" value="mysql-client">

```shell
mysql --host 127.0.0.1 --port 4000 -u root < player_init.sql
```

</div>

<div label="MyCLI" value="mycli">

```shell
mycli --host 127.0.0.1 --port 4000 -u root --no-warn < player_init.sql
```

</div>

</SimpleTab>

If you are not using a local cluster, or have not installed a MySQL client, connect to your cluster using your preferred method (such as Navicat, DBeaver, or other GUI tools) and run the SQL statements in the `player_init.sql` file.

### Step 3.2 Modify parameters for TiDB Cloud

If you are using a TiDB Cloud Serverless Tier cluster, you need to provide your CA root path and replace `<ca_path>` in the following examples with your CA path. To get the CA root path on your system, refer to [Where is the CA root path on my system?](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-tier-clusters#where-is-the-ca-root-path-on-my-system).

If you are using a TiDB Cloud Serverless Tier cluster, change the `get_connection` function in `mysqlclient_example.py`:

```python
def get_connection(autocommit: bool = True) -> MySQLdb.Connection:
    return MySQLdb.connect(
        host="127.0.0.1",
        port=4000,
        user="root",
        password="",
        database="test",
        autocommit=autocommit
    )
```

Suppose that the password you set is `123456`, and the connection parameters you get from the cluster details page are the following:

- Endpoint: `xxx.tidbcloud.com`
- Port: `4000`
- User: `2aEp24QWEDLqRFs.root`

In this case, you can modify the `get_connection` as follows:

```python
def get_connection(autocommit: bool = True) -> MySQLdb.Connection:
    return MySQLdb.connect(
        host="xxx.tidbcloud.com",
        port=4000,
        user="2aEp24QWEDLqRFs.root",
        password="123456",
        database="test",
        autocommit=autocommit,
        ssl_mode="VERIFY_IDENTITY",
        ssl={
            "ca": "<ca_path>"
        }
    )
```

### Step 3.3 Run the code

Before running the code, use the following command to install dependencies:

```bash
pip3 install -r requirement.txt
```

If you need to run the script multiple times, follow the [Table initialization](#step-31-initialize-table) section to initialize the table again before each run.

```bash
python3 mysqlclient_example.py
```

## Step 4. Expected output

[mysqlclient Expected Output](https://github.com/pingcap-inc/tidb-example-python/blob/main/Expected-Output.md#mysqlclient)