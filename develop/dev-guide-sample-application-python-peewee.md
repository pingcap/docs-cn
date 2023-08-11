---
title: Build a Simple CRUD App with TiDB and peewee
summary: Learn how to build a simple CRUD application with TiDB and peewee.
---

<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD029 -->

# Build a Simple CRUD App with TiDB and peewee

[peewee](http://docs.peewee-orm.com/en/latest/) is a popular open-source ORM library for Python.

This document describes how to use TiDB and peewee to build a simple CRUD application.

> **Note:**
>
> It is recommended to use Python 3.10 or a later Python version.

## Step 1. Launch your TiDB cluster

<CustomContent platform="tidb">

The following introduces how to start a TiDB cluster.

**Use a TiDB Serverless cluster**

For detailed steps, see [Create a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-tidb-serverless-cluster).

**Use a local cluster**

For detailed steps, see [Deploy a local test cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) or [Deploy a TiDB cluster using TiUP](/production-deployment-using-tiup.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

See [Create a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-tidb-serverless-cluster).

</CustomContent>

## Step 2. Get the code

```shell
git clone https://github.com/pingcap-inc/tidb-example-python.git
```

The following uses peewee 3.15.4 as an example.

```python
import os
import uuid
from typing import List

from peewee import *

from playhouse.db_url import connect

db = connect('mysql://root:@127.0.0.1:4000/test')


class Player(Model):
    id = CharField(max_length=36, primary_key=True)
    coins = IntegerField()
    goods = IntegerField()

    class Meta:
        database = db
        table_name = "player"


def random_player(amount: int) -> List[Player]:
    players = []
    for _ in range(amount):
        players.append(Player(id=uuid.uuid4(), coins=10000, goods=10000))

    return players


def simple_example() -> None:
    # create a player, who has a coin and a goods.
    Player.create(id="test", coins=1, goods=1)

    # get this player, and print it.
    test_player = Player.select().where(Player.id == "test").get()
    print(f'id:{test_player.id}, coins:{test_player.coins}, goods:{test_player.goods}')

    # create players with bulk inserts.
    # insert 1919 players totally, with 114 players per batch.
    # each player has a random UUID
    player_list = random_player(1919)
    Player.bulk_create(player_list, 114)

    # print the number of players
    count = Player.select().count()
    print(f'number of players: {count}')
    
    # print 3 players.
    three_players = Player.select().limit(3)
    for player in three_players:
        print(f'id:{player.id}, coins:{player.coins}, goods:{player.goods}')


def trade_check(sell_id: str, buy_id: str, amount: int, price: int) -> bool:
    sell_goods = Player.select(Player.goods).where(Player.id == sell_id).get().goods
    if sell_goods < amount:
        print(f'sell player {sell_id} goods not enough')
        return False

    buy_coins = Player.select(Player.coins).where(Player.id == buy_id).get().coins
    if buy_coins < price:
        print(f'buy player {buy_id} coins not enough')
        return False

    return True


def trade(sell_id: str, buy_id: str, amount: int, price: int) -> None:
    with db.atomic() as txn:
        try:
            if trade_check(sell_id, buy_id, amount, price) is False:
                txn.rollback()
                return

            # deduct the goods of seller, and raise his/her the coins
            Player.update(goods=Player.goods - amount, coins=Player.coins + price).where(Player.id == sell_id).execute()
            # deduct the coins of buyer, and raise his/her the goods
            Player.update(goods=Player.goods + amount, coins=Player.coins - price).where(Player.id == buy_id).execute()

        except Exception as err:
            txn.rollback()
            print(f'something went wrong: {err}')
        else:
            txn.commit()
            print("trade success")


def trade_example() -> None:
    # create two players
    # player 1: id is "1", has only 100 coins.
    # player 2: id is "2", has 114514 coins, and 20 goods.
    Player.create(id="1", coins=100, goods=0)
    Player.create(id="2", coins=114514, goods=20)

    # player 1 wants to buy 10 goods from player 2.
    # it will cost 500 coins, but player 1 cannot afford it.
    # so this trade will fail, and nobody will lose their coins or goods
    trade(sell_id="2", buy_id="1", amount=10, price=500)

    # then player 1 has to reduce the incoming quantity to 2.
    # this trade will be successful
    trade(sell_id="2", buy_id="1", amount=2, price=100)

    # let's take a look for player 1 and player 2 currently
    after_trade_players = Player.select().where(Player.id.in_(["1", "2"]))
    for player in after_trade_players:
        print(f'id:{player.id}, coins:{player.coins}, goods:{player.goods}')


db.connect()

# recreate the player table
db.drop_tables([Player])
db.create_tables([Player])

simple_example()
trade_example()
```

Compared with using drivers directly, peewee provides an abstraction for the specific details of different databases when you create a database connection. In addition, peewee encapsulates some operations such as session management and CRUD of basic objects, which greatly simplifies the code.

The `Player` class is a mapping of a table to attributes in the application. Each attribute of `Player` corresponds to a field in the `player` table. To provide peewee with more information, the attribute is defined as `id = CharField(max_length=36, primary_key=True)` to indicate the field type and its additional attributes. For example, `id = CharField(max_length=36, primary_key=True)` indicates that the `id` attribute is `String` type, the corresponding field in database is `VARCHAR` type, the length is `36`, and it is a primary key.

For more information about how to use peewee, refer to [peewee documentation](http://docs.peewee-orm.com/en/latest/).

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

If you are using a TiDB Serverless cluster, you need to provide your CA root path and replace `<ca_path>` in the following examples with your CA path. To get the CA root path on your system, refer to [Where is the CA root path on my system?](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-tier-clusters#where-is-the-ca-root-path-on-my-system).

If you are using a TiDB Serverless cluster, modify the parameters of the `connect` function in `peewee_example.py`:

```python
db = connect('mysql://root:@127.0.0.1:4000/test')
```

Suppose that the password you set is `123456`, and the connection parameters you get from the cluster details page are the following:

- Endpoint: `xxx.tidbcloud.com`
- Port: `4000`
- User: `2aEp24QWEDLqRFs.root`

In this case, you can modify the `connect` as follows:

- When peewee uses PyMySQL as the driver:

    ```python
    db = connect('mysql://2aEp24QWEDLqRFs.root:123456@xxx.tidbcloud.com:4000/test', 
        ssl_verify_cert=True, ssl_ca="<ca_path>")
    ```

- When peewee uses mysqlclient as the driver:

    ```python
    db = connect('mysql://2aEp24QWEDLqRFs.root:123456@xxx.tidbcloud.com:4000/test',
        ssl_mode="VERIFY_IDENTITY", ssl={"ca": "<ca_path>"})
    ```

Because peewee will pass parameters to the driver, you need to pay attention to the usage type of the driver when using peewee.

### Step 3.3 Run the code

Before running the code, use the following command to install dependencies:

```bash
pip3 install -r requirement.txt
```

If you need to run the script multiple times, follow the [Table initialization](#step-31-initialize-table) section to initialize the table again before each run.

```bash
python3 peewee_example.py
```

## Step 4. Expected output

[peewee Expected Output](https://github.com/pingcap-inc/tidb-example-python/blob/main/Expected-Output.md#peewee)