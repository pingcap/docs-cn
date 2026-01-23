---
title: Full-Text Search with SQL
summary: Full-text search lets you retrieve documents for exact keywords. In Retrieval-Augmented Generation (RAG) scenarios, you can use full-text search together with vector search to improve the retrieval quality.
aliases: ['/tidb/stable/vector-search-full-text-search-sql']
---

# Full-Text Search with SQL

Unlike [Vector Search](/ai/vector-search-overview.md), which focuses on semantic similarity, full-text search lets you retrieve documents for exact keywords. In Retrieval-Augmented Generation (RAG) scenarios, you can use full-text search together with vector search to improve the retrieval quality.

The full-text search feature in TiDB provides the following capabilities:

- **Query text data directly**: you can search any string columns directly without the embedding process.

- **Support for multiple languages**: no need to specify the language for high-quality search. The text analyzer in TiDB supports documents in multiple languages mixed in the same table and automatically chooses the best analyzer for each document.

- **Order by relevance**: the search result can be ordered by relevance using the widely adopted [BM25 ranking](https://en.wikipedia.org/wiki/Okapi_BM25) algorithm.

- **Fully compatible with SQL**: all SQL features, such as pre-filtering, post-filtering, grouping, and joining, can be used with full-text search.

> **Tip:**
>
> For Python usage, see [Full-Text Search with Python](/ai/vector-search-full-text-search-python.md).
>
> To use full-text search and vector search together in your AI apps, see [Hybrid Search](/ai/vector-search-hybrid-search.md).

## Get started

Full-text search is still in the early stages, and we are continuously rolling it out to more customers. Currently, Full-text search is only available on {{{ .starter }}} and {{{ .essential }}} in the following regions:

- AWS: `Frankfurt (eu-central-1)` and `Singapore (ap-southeast-1)`

Before using full-text search, make sure your {{{ .starter }}} cluster is created in a supported region. If you don't have one, follow [Creating a {{{ .starter }}} cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create it.

To perform a full-text search, follow these steps:

1. [**Create a full-text index**](#create-a-full-text-index): create a table with a full-text index, or add a full-text index to an existing table.

2. [**Insert text data**](#insert-text-data): insert text data into the table.

3. [**Perform a full-text search**](#perform-a-full-text-search): perform a full-text search using text queries and full-text search functions.

### Create a full-text index

To perform full-text search, a full-text index is required as it provides the necessary data structure for efficient searching and ranking. Full-text indexes can be created on new tables or added to existing tables.

Create a table with a full-text index:

```sql
CREATE TABLE stock_items(
    id INT,
    title TEXT,
    FULLTEXT INDEX (title) WITH PARSER MULTILINGUAL
);
```

Or add a full-text index to an existing table:

```sql
CREATE TABLE stock_items(
    id INT,
    title TEXT
);

-- You might insert some data here.
-- The full-text index can be created even if data is already in the table.

ALTER TABLE stock_items ADD FULLTEXT INDEX (title) WITH PARSER MULTILINGUAL ADD_COLUMNAR_REPLICA_ON_DEMAND;
```

The following parsers are accepted in the `WITH PARSER <PARSER_NAME>` clause:

- `STANDARD`: fast, works for English contents, splitting words by spaces and punctuation.

- `MULTILINGUAL`: supports multiple languages, including English, Chinese, Japanese, and Korean.

### Insert text data

Inserting data into a table with a full-text index is identical to inserting data into any other tables.

For example, you can execute the following SQL statements to insert data in multiple languages. The multilingual parser in TiDB automatically processes the text.

```sql
INSERT INTO stock_items VALUES (1, "イヤホン bluetooth ワイヤレスイヤホン ");
INSERT INTO stock_items VALUES (2, "完全ワイヤレスイヤホン/ウルトラノイズキャンセリング 2.0 ");
INSERT INTO stock_items VALUES (3, "ワイヤレス ヘッドホン Bluetooth 5.3 65時間再生 ヘッドホン 40mm HD ");
INSERT INTO stock_items VALUES (4, "楽器用 オンイヤーヘッドホン 密閉型【国内正規品】");
INSERT INTO stock_items VALUES (5, "ワイヤレスイヤホン ハイブリッドANC搭載 40dBまでアクティブノイズキャンセル");
INSERT INTO stock_items VALUES (6, "Lightweight Bluetooth Earbuds with 48 Hours Playtime");
INSERT INTO stock_items VALUES (7, "True Wireless Noise Cancelling Earbuds - Compatible with Apple & Android, Built-in Microphone");
INSERT INTO stock_items VALUES (8, "In-Ear Earbud Headphones with Mic, Black");
INSERT INTO stock_items VALUES (9, "Wired Headphones, HD Bass Driven Audio, Lightweight Aluminum Wired in Ear Earbud Headphones");
INSERT INTO stock_items VALUES (10, "LED Light Bar, Music Sync RGB Light Bar, USB Ambient Lamp");
INSERT INTO stock_items VALUES (11, "无线消噪耳机-黑色 手势触控蓝牙降噪 主动降噪头戴式耳机（智能降噪 长久续航）");
INSERT INTO stock_items VALUES (12, "专业版USB7.1声道游戏耳机电竞耳麦头戴式电脑网课办公麦克风带线控");
INSERT INTO stock_items VALUES (13, "投影仪家用智能投影机便携卧室手机投影");
INSERT INTO stock_items VALUES (14, "无线蓝牙耳机超长续航42小时快速充电 流光金属耳机");
INSERT INTO stock_items VALUES (15, "皎月银 国家补贴 心率血氧监测 蓝牙通话 智能手表 男女表");
```

### Perform a full-text search

To perform a full-text search, you can use the `FTS_MATCH_WORD()` function.

**Example: search for most relevant 10 documents**

```sql
SELECT * FROM stock_items
    WHERE fts_match_word("bluetoothイヤホン", title)
    ORDER BY fts_match_word("bluetoothイヤホン", title)
    DESC LIMIT 10;

-- Results are ordered by relevance, with the most relevant documents first.

+------+-----------------------------------------------------------------------------------------------------------+
| id   | title                                                                                                     |
+------+-----------------------------------------------------------------------------------------------------------+
|    1 | イヤホン bluetooth ワイヤレスイヤホン                                                                         |
|    6 | Lightweight Bluetooth Earbuds with 48 Hours Playtime                                                      |
|    2 | 完全ワイヤレスイヤホン/ウルトラノイズキャンセリング 2.0                                                           |
|    3 | ワイヤレス ヘッドホン Bluetooth 5.3 65時間再生 ヘッドホン 40mm HD                                               |
|    5 | ワイヤレスイヤホン ハイブリッドANC搭載 40dBまでアクティブノイズキャンセル                                            |
+------+-----------------------------------------------------------------------------------------------------------+

-- Try searching in another language:
SELECT * FROM stock_items
    WHERE fts_match_word("蓝牙耳机", title)
    ORDER BY fts_match_word("蓝牙耳机", title)
    DESC LIMIT 10;

-- Results are ordered by relevance, with the most relevant documents first.

+------+---------------------------------------------------------------------------------------------------------------+
| id   | title                                                                                                         |
+------+---------------------------------------------------------------------------------------------------------------+
|   14 | 无线蓝牙耳机超长续航42小时快速充电 流光金属耳机                                                                      |
|   11 | 无线消噪耳机-黑色 手势触控蓝牙降噪 主动降噪头戴式耳机（智能降噪 长久续航）                                                |
|   15 | 皎月银 国家补贴 心率血氧监测 蓝牙通话 智能手表 男女表                                                                 |
+------+---------------------------------------------------------------------------------------------------------------+
```

**Example: count the number of documents matching the user query**

```sql
SELECT COUNT(*) FROM stock_items
    WHERE fts_match_word("bluetoothイヤホン", title);

+----------+
| COUNT(*) |
+----------+
|        5 |
+----------+
```

## Advanced example: Join search results with other tables

You can combine full-text search with other SQL features such as joins and subqueries.

Assume you have a `users` table and a `tickets` table, and want to find tickets created by authors based on a full-text search of their names:

```sql
CREATE TABLE users(
    id INT,
    name TEXT,
    FULLTEXT INDEX (name) WITH PARSER STANDARD
);

INSERT INTO users VALUES (1, "Alice Smith");
INSERT INTO users VALUES (2, "Bob Johnson");

CREATE TABLE tickets(
    id INT,
    title TEXT,
    author_id INT
);

INSERT INTO tickets VALUES (1, "Ticket 1", 1);
INSERT INTO tickets VALUES (2, "Ticket 2", 1);
INSERT INTO tickets VALUES (3, "Ticket 3", 2);
```

You can use a subquery to find matching user IDs based on the author's name, and then use these IDs in the outer query to retrieve and join related ticket information:

```sql
SELECT t.title AS TICKET_TITLE, u.id AS AUTHOR_ID, u.name AS AUTHOR_NAME FROM tickets t
LEFT JOIN users u ON t.author_id = u.id
WHERE t.author_id IN
(
    SELECT id FROM users
    WHERE fts_match_word("Alice", name)
);

+--------------+-----------+-------------+
| TICKET_TITLE | AUTHOR_ID | AUTHOR_NAME |
+--------------+-----------+-------------+
| Ticket 1     |         1 | Alice Smith |
| Ticket 2     |         1 | Alice Smith |
+--------------+-----------+-------------+
```

## See also

- [Hybrid Search](/ai/vector-search-hybrid-search.md)

## Feedback & help

Full-text search is still in the early stages with limited accessibility. If you would like to try full-text search in a region that is not yet available, or if you have feedback or need help, feel free to reach out to us:

- Ask the community on [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) or [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs).
- [Submit a support ticket for TiDB Cloud](https://tidb.support.pingcap.com/servicedesk/customer/portals)
