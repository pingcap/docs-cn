---
title: 使用 SQL 进行全文检索
summary: 全文检索允许你根据精确关键词检索文档。在 RAG（检索增强生成）场景中，你可以将全文检索与向量检索结合使用，以提升检索质量。
aliases: ['/tidb/stable/vector-search-full-text-search-sql']
---

# 使用 SQL 进行全文检索 <!-- Draft translated by AI -->

与 [向量检索](/vector-search/vector-search-overview.md) 侧重于语义相似性不同，全文检索允许你根据精确关键词检索文档。在 RAG（检索增强生成）场景中，你可以将全文检索与向量检索结合使用，以提升检索质量。

TiDB 的全文检索功能提供以下能力：

- **直接查询文本数据**：你可以直接在任意字符串列上进行检索，无需进行嵌入处理。

- **支持多语言**：无需指定语言即可获得高质量检索。TiDB 的文本分析器支持同一张表中多种语言混合的文档，并会自动为每个文档选择最佳分析器。

- **按相关性排序**：检索结果可以通过广泛采用的 [BM25 排序](https://en.wikipedia.org/wiki/Okapi_BM25) 算法按相关性排序。

- **与 SQL 完全兼容**：所有 SQL 特性，如预过滤、后过滤、分组和关联查询等，都可以与全文检索结合使用。

> **提示：**
>
> 关于 Python 的用法，请参见 [使用 Python 进行全文检索](/ai/vector-search-full-text-search-python.md)。
>
> 如需在 AI 应用中同时使用全文检索和向量检索，请参见 [混合检索](/ai/vector-search-hybrid-search.md)。

## 快速开始

全文检索目前仍处于早期阶段，我们正在持续向更多用户开放。目前，全文检索仅在以下区域的 TiDB Cloud Starter 和 TiDB Cloud Essential 上可用：

- AWS：`法兰克福 (eu-central-1)` 和 `新加坡 (ap-southeast-1)`

在使用全文检索前，请确保你的 TiDB Cloud Starter 集群已创建在支持的区域。如果还没有，请按照 [创建 TiDB Cloud Starter 集群](/develop/dev-guide-build-cluster-in-cloud.md) 进行创建。

要执行全文检索，请按照以下步骤操作：

1. [**创建全文索引**](#创建全文索引)：创建带有全文索引的表，或为已有表添加全文索引。

2. [**插入文本数据**](#插入文本数据)：向表中插入文本数据。

3. [**执行全文检索**](#执行全文检索)：使用文本查询和全文检索函数进行全文检索。

### 创建全文索引

要进行全文检索，需要创建全文索引，它为高效检索和排序提供必要的数据结构。全文索引既可以在新表上创建，也可以添加到已有表中。

创建带有全文索引的表：

```sql
CREATE TABLE stock_items(
    id INT,
    title TEXT,
    FULLTEXT INDEX (title) WITH PARSER MULTILINGUAL
);
```

或者为已有表添加全文索引：

```sql
CREATE TABLE stock_items(
    id INT,
    title TEXT
);

-- 你可以在这里插入一些数据。
-- 即使表中已有数据，也可以创建全文索引。

ALTER TABLE stock_items ADD FULLTEXT INDEX (title) WITH PARSER MULTILINGUAL ADD_COLUMNAR_REPLICA_ON_DEMAND;
```

`WITH PARSER <PARSER_NAME>` 子句中支持以下解析器：

- `STANDARD`：速度快，适用于英文内容，通过空格和标点分词。

- `MULTILINGUAL`：支持多种语言，包括英文、中文、日文和韩文。

### 插入文本数据

向带有全文索引的表插入数据与向其他表插入数据完全相同。

例如，你可以执行以下 SQL 语句插入多语言数据。TiDB 的多语言解析器会自动处理这些文本。

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

### 执行全文检索

要执行全文检索，你可以使用 `FTS_MATCH_WORD()` 函数。

**示例：检索最相关的 10 个文档**

```sql
SELECT * FROM stock_items
    WHERE fts_match_word("bluetoothイヤホン", title)
    ORDER BY fts_match_word("bluetoothイヤホン", title)
    DESC LIMIT 10;

-- 结果按相关性排序，最相关的文档排在最前面。

+------+-----------------------------------------------------------------------------------------------------------+
| id   | title                                                                                                     |
+------+-----------------------------------------------------------------------------------------------------------+
|    1 | イヤホン bluetooth ワイヤレスイヤホン                                                                         |
|    6 | Lightweight Bluetooth Earbuds with 48 Hours Playtime                                                      |
|    2 | 完全ワイヤレスイヤホン/ウルトラノイズキャンセリング 2.0                                                           |
|    3 | ワイヤレス ヘッドホン Bluetooth 5.3 65時間再生 ヘッドホン 40mm HD                                               |
|    5 | ワイヤレスイヤホン ハイブリッドANC搭载 40dBまでアクティブノイズキャンセル                                            |
+------+-----------------------------------------------------------------------------------------------------------+

-- 尝试用另一种语言检索：
SELECT * FROM stock_items
    WHERE fts_match_word("蓝牙耳机", title)
    ORDER BY fts_match_word("蓝牙耳机", title)
    DESC LIMIT 10;

-- 结果按相关性排序，最相关的文档排在最前面。

+------+---------------------------------------------------------------------------------------------------------------+
| id   | title                                                                                                         |
+------+---------------------------------------------------------------------------------------------------------------+
|   14 | 无线蓝牙耳机超长续航42小时快速充电 流光金属耳机                                                                      |
|   11 | 无线消噪耳机-黑色 手势触控蓝牙降噪 主动降噪头戴式耳机（智能降噪 长久续航）                                                |
|   15 | 皎月银 国家补贴 心率血氧监测 蓝牙通话 智能手表 男女表                                                                 |
+------+---------------------------------------------------------------------------------------------------------------+
```

**示例：统计与用户查询匹配的文档数量**

```sql
SELECT COUNT(*) FROM stock_items
    WHERE fts_match_word("bluetoothイヤホン", title);

+----------+
| COUNT(*) |
+----------+
|        5 |
+----------+
```

## 进阶示例：与其他表联合检索

你可以将全文检索与其他 SQL 特性（如关联查询和子查询）结合使用。

假设你有一张 `users` 表和一张 `tickets` 表，并希望根据作者姓名的全文检索结果查找其创建的工单：

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

你可以通过子查询根据作者姓名检索匹配的用户 ID，然后在外层查询中使用这些 ID 进行关联，获取相关工单信息：

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

## 参见

- [混合检索](/ai/vector-search-hybrid-search.md)

## 反馈与帮助

全文检索目前仍处于早期阶段，开放范围有限。如果你希望在尚未开放的区域体验全文检索，或有任何反馈与帮助需求，欢迎联系我们：

<CustomContent platform="tidb">

- [加入我们的 Discord](https://discord.gg/zcqexutz2R)

</CustomContent>

<CustomContent platform="tidb-cloud">

- [加入我们的 Discord](https://discord.gg/zcqexutz2R)
- [访问我们的支持门户](https://tidb.support.pingcap.com/)

</CustomContent>