---
title: TiDB 和 peewee 的简单 CRUD 应用程序
summary: 给出一个 TiDB 和 peewee 的简单 CRUD 应用程序示例。
---

<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD029 -->

# TiDB 和 peewee 的简单 CRUD 应用程序

[peewee](http://docs.peewee-orm.com/en/latest/) 为当前比较流行的开源 Python ORM 之一。

本文档将展示如何使用 TiDB 和 peewee 来构造一个简单的 CRUD 应用程序。

> **注意：**
>
> 推荐使用 Python 3.10 及以上版本进行 TiDB 的应用程序的编写。

## 第 1 步：启动你的 TiDB 集群

本节将介绍 TiDB 集群的启动方法。

**使用 TiDB Serverless 集群**

详细步骤，请参考：[创建 TiDB Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md#第-1-步创建-tidb-serverless-集群)。

**使用本地集群**

详细步骤，请参考：[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#部署本地测试集群)或[部署正式 TiDB 集群](/production-deployment-using-tiup.md)。

## 第 2 步：获取代码

```shell
git clone https://github.com/pingcap-inc/tidb-example-python.git
```

此处将以 peewee **3.15.4** 版本进行说明。

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

相较于直接使用 Driver，peewee 屏蔽了创建数据库连接时，不同数据库差异的细节。peewee 还封装了大量的操作，如会话管理、基本对象的 CRUD 等，极大地简化了代码量。

`Player` 类为数据库表在程序内的映射。`Player` 的每个属性都对应着 `player` 表的一个字段。peewee 使用 `Player` 类为了给 peewee 提供更多的信息，使用了形如以上示例中的 `id = CharField(max_length=36, primary_key=True)` 的类型定义，用来指示字段类型和其附加属性。`id = CharField(max_length=36, primary_key=True)` 表示 `id` 字段为 `CharField` 类型，对应数据库类型为 `VARCHAR`，长度为 `36`，且为主键。

关于 peewee 的更多使用方法，你可以参考 [peewee 官网](http://docs.peewee-orm.com/en/latest/)。

## 第 3 步：运行代码

本节将逐步介绍代码的运行方法。

### 第 3 步第 1 部分：表初始化

本示例需手动初始化表，若你使用本地集群，可直接运行：

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

若不使用本地集群，或未安装命令行客户端，请用喜欢的方式（如 Navicat、DBeaver 等 GUI 工具）直接登录集群，并运行 `player_init.sql` 文件内的 SQL 语句。

### 第 3 步第 2 部分：TiDB Cloud 更改参数

若你使用了 TiDB Serverless 集群，此处需使用系统本地的 CA 证书，并将证书路径记为 `<ca_path>` 以供后续指代。你可以参考 [Where is the CA root path on my system?](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-tier-clusters#where-is-the-ca-root-path-on-my-system) 文档获取你所使用的操作系统的 CA 证书位置。

若你使用 TiDB Serverless 集群，更改 `peewee_example.py` 内 `connect` 函数的入参：

```python
db = connect('mysql://root:@127.0.0.1:4000/test')
```

若你设定的密码为 `123456`，而且从 TiDB Serverless 集群面板中得到的连接信息为：

- Endpoint: `xxx.tidbcloud.com`
- Port: `4000`
- User: `2aEp24QWEDLqRFs.root`

那么此处应将 `connect` 更改为：

- peewee 将 PyMySQL 作为 Driver 时：

    ```python
    db = connect('mysql://2aEp24QWEDLqRFs.root:123456@xxx.tidbcloud.com:4000/test', 
        ssl_verify_cert=True, ssl_ca="<ca_path>")
    ```

- peewee 将 mysqlclient 作为 Driver 时：

    ```python
    db = connect('mysql://2aEp24QWEDLqRFs.root:123456@xxx.tidbcloud.com:4000/test',
        ssl_mode="VERIFY_IDENTITY", ssl={"ca": "<ca_path>"})
    ```

由于 peewee 会将参数透传至 Driver 中，使用 peewee 时请注意 Driver 的使用类型。

### 第 3 步第 3 部分：运行

运行前请先安装依赖：

```bash
pip3 install -r requirement.txt
```

当以后需要多次运行脚本时，请在每次运行前先依照[表初始化](#第-3-步第-1-部分表初始化)一节再次进行表初始化。

```bash
python3 peewee_example.py
```

## 第 4 步：预期输出

[peewee 预期输出](https://github.com/pingcap-inc/tidb-example-python/blob/main/Expected-Output.md#peewee)
