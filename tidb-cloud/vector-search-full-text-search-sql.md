---
title: 使用 SQL 进行全文搜索
summary: 全文搜索允许您通过精确关键词检索文档。在检索增强生成（RAG）场景中，您可以将全文搜索与向量搜索结合使用，以提高检索质量。
---

# 使用 SQL 进行全文搜索

与专注于语义相似度的[向量搜索](/tidb-cloud/vector-search-overview.md)不同，全文搜索允许您通过精确关键词检索文档。在检索增强生成（RAG）场景中，您可以将全文搜索与向量搜索结合使用，以提高检索质量。

TiDB 的全文搜索功能提供以下能力：

- **直接查询文本数据**：您可以直接搜索任何字符串列，无需进行嵌入处理。

- **支持多种语言**：无需指定语言即可实现高质量搜索。TiDB 中的文本分析器支持在同一个表中混合使用多种语言的文档，并自动为每个文档选择最佳的分析器。

- **按相关性排序**：搜索结果可以使用广泛采用的 [BM25 排序](https://en.wikipedia.org/wiki/Okapi_BM25)算法按相关性排序。

- **完全兼容 SQL**：所有 SQL 功能，如预过滤、后过滤、分组和连接，都可以与全文搜索一起使用。

> **提示：**
>
> 关于 Python 用法，请参见[使用 Python 进行全文搜索](/tidb-cloud/vector-search-full-text-search-python.md)。
>
> 要在 AI 应用中同时使用全文搜索和向量搜索，请参见[混合搜索](/tidb-cloud/vector-search-hybrid-search.md)。

## 开始使用

全文搜索仍处于早期阶段，我们正在持续向更多客户推出。目前，全文搜索仅适用于以下产品选项和地区：

- TiDB Cloud Serverless：`法兰克福 (eu-central-1)` 和 `新加坡 (ap-southeast-1)`

在使用全文搜索之前，请确保您的 TiDB Cloud Serverless 集群创建在支持的地区。如果您还没有集群，请按照[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)的说明创建一个。

要执行全文搜索，请按照以下步骤操作：

1. [**创建全文索引**](#创建全文索引)：创建带有全文索引的表，或为现有表添加全文索引。

2. [**插入文本数据**](#插入文本数据)：向表中插入文本数据。

3. [**执行全文搜索**](#执行全文搜索)：使用文本查询和全文搜索函数执行全文搜索。

### 创建全文索引

要执行全文搜索，需要全文索引，因为它提供了高效搜索和排序所需的数据结构。全文索引可以在新表上创建，也可以添加到现有表中。

创建带有全文索引的表：

```sql
CREATE TABLE stock_items(
    id INT,
    title TEXT,
    FULLTEXT INDEX (title) WITH PARSER MULTILINGUAL
);
```

或为现有表添加全文索引：

```sql
CREATE TABLE stock_items(
    id INT,
    title TEXT
);

-- 您可能在这里插入一些数据。
-- 即使表中已经有数据，也可以创建全文索引。

ALTER TABLE stock_items ADD FULLTEXT INDEX (title) WITH PARSER MULTILINGUAL ADD_COLUMNAR_REPLICA_ON_DEMAND;
```

在 `WITH PARSER <PARSER_NAME>` 子句中可以使用以下解析器：

- `STANDARD`：快速，适用于英文内容，按空格和标点符号分词。

- `MULTILINGUAL`：支持多种语言，包括英语、中文、日语和韩语。

### 插入文本数据

向带有全文索引的表中插入数据与向其他表插入数据完全相同。

例如，您可以执行以下 SQL 语句来插入多种语言的数据。TiDB 的多语言解析器会自动处理文本。

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

### 执行全文搜索

要执行全文搜索，您可以使用 `FTS_MATCH_WORD()` 函数。

**示例：搜索最相关的 10 个文档**

```sql
SELECT * FROM stock_items
    WHERE fts_match_word("bluetoothイヤホン", title)
    ORDER BY fts_match_word("bluetoothイヤホン", title)
    DESC LIMIT 10;

-- 结果按相关性排序，最相关的文档排在前面。

+------+-----------------------------------------------------------------------------------------------------------+
| id   | title                                                                                                     |
+------+-----------------------------------------------------------------------------------------------------------+
|    1 | イヤホン bluetooth ワイヤレスイヤホン                                                                         |
|    6 | Lightweight Bluetooth Earbuds with 48 Hours Playtime                                                      |
|    2 | 完全ワイヤレスイヤホン/ウルトラノイズキャンセリング 2.0                                                           |
|    3 | ワイヤレス ヘッドホン Bluetooth 5.3 65時間再生 ヘッドホン 40mm HD                                               |
|    5 | ワイヤレスイヤホン ハイブリッドANC搭載 40dBまでアクティブノイズキャンセル                                            |
+------+-----------------------------------------------------------------------------------------------------------+

-- 尝试用另一种语言搜索：
SELECT * FROM stock_items
    WHERE fts_match_word("蓝牙耳机", title)
    ORDER BY fts_match_word("蓝牙耳机", title)
    DESC LIMIT 10;

-- 结果按相关性排序，最相关的文档排在前面。

+------+---------------------------------------------------------------------------------------------------------------+
| id   | title                                                                                                         |
+------+---------------------------------------------------------------------------------------------------------------+
|   14 | 无线蓝牙耳机超长续航42小时快速充电 流光金属耳机                                                                      |
|   11 | 无线消噪耳机-黑色 手势触控蓝牙降噪 主动降噪头戴式耳机（智能降噪 长久续航）                                                |
|   15 | 皎月银 国家补贴 心率血氧监测 蓝牙通话 智能手表 男女表                                                                 |
+------+---------------------------------------------------------------------------------------------------------------+
```

**示例：统计匹配用户查询的文档数量**

```sql
SELECT COUNT(*) FROM stock_items
    WHERE fts_match_word("bluetoothイヤホン", title);

+----------+
| COUNT(*) |
+----------+
|        5 |
+----------+
```

## 高级示例：连接搜索结果与其他表

您可以将全文搜索与其他 SQL 功能（如连接和子查询）结合使用。

假设您有一个 `users` 表和一个 `tickets` 表，想要根据作者姓名的全文搜索来查找他们创建的工单：

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

您可以使用子查询根据作者姓名查找匹配的用户 ID，然后在外部查询中使用这些 ID 来检索和连接相关的工单信息：

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

## 另请参阅

- [混合搜索](/tidb-cloud/vector-search-hybrid-search.md)

## 反馈与帮助

全文搜索仍处于早期阶段，可用性有限。如果您想在尚未开放的地区尝试全文搜索，或者如果您有反馈或需要帮助，请随时联系我们：

<CustomContent platform="tidb">

- [加入我们的 Discord](https://discord.gg/zcqexutz2R)

</CustomContent>

<CustomContent platform="tidb-cloud">

- [加入我们的 Discord](https://discord.gg/zcqexutz2R)
- [访问我们的支持门户](https://tidb.support.pingcap.com/)

</CustomContent>
