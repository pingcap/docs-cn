---
title: 使用 SQL 进行全文搜索
summary: 全文搜索允许你根据精确关键字搜索文档。在检索增强生成（RAG）场景中，你可以将全文搜索与向量搜索结合使用，以提升搜索质量。
aliases: ['/zh/tidbcloud/vector-search-full-text-search-sql/']
---

# 使用 SQL 进行全文搜索

与关注语义相似度的 [向量搜索](/ai/concepts/vector-search-overview.md) 不同，全文搜索允许你根据精确关键字搜索文档。在检索增强生成（RAG）场景中，你可以将全文搜索与向量搜索结合使用，以提升搜索质量。

TiDB 的全文搜索功能提供以下能力：

- **直接查询文本数据**：你可以直接在任意 string 列上进行搜索，无需 embedding 过程。

- **支持多语言**：无需指定语言即可获得高质量搜索。TiDB 的文本分析器支持同一张表中多种语言混合的文档，并会自动为每个文档选择最佳分析器。

- **按相关性排序**：搜索结果可通过广泛采用的 [BM25 排序](https://en.wikipedia.org/wiki/Okapi_BM25) algorithm 按相关性排序。

- **完全兼容 SQL**：所有 SQL 功能，如预过滤、后过滤、分组和 join，都可与全文搜索结合使用。

> **提示：**
>
> 如需在 Python 中使用，请参见 [使用 Python 进行全文搜索](/ai/guides/vector-search-full-text-search-python.md)。
>
> 如需在 AI 应用中同时使用全文搜索和向量搜索，请参见 [混合搜索](/ai/guides/vector-search-hybrid-search.md)。

## 快速开始

全文搜索仍处于早期阶段，我们正在持续向更多用户开放。目前，全文搜索仅在以下区域的 TiDB Cloud Starter 上可用：

- AWS: `Oregon (us-west-2)`、`N. Virginia (us-east-1)`、`Tokyo (ap-northeast-1)`、`Frankfurt (eu-central-1)` 和 `Singapore (ap-southeast-1)`

在使用全文搜索前，请确保你的 TiDB Cloud Starter 实例已创建在支持的区域。如果还没有，请按照 [创建 TiDB Cloud Starter 实例](/develop/dev-guide-build-cluster-in-cloud.md) 进行创建。

要进行全文搜索，请按照以下步骤操作：

1. [**创建全文索引**](#创建全文索引)：创建带有全文索引的表，或为已有表添加全文索引。

2. [**插入文本数据**](#插入文本数据)：向表中插入文本数据。

3. [**执行全文搜索**](#执行全文搜索)：使用文本查询和全文搜索函数进行全文搜索。

### 创建全文索引

要进行全文搜索，需要创建全文索引，它为高效搜索和排序提供必要的数据结构。全文索引既可以在新表上创建，也可以添加到已有表上。

创建带有全文索引的表：

```sql
CREATE TABLE stock_items(
    id INT,
    title TEXT,
    FULLTEXT INDEX (title) WITH PARSER MULTILINGUAL
);
```

或为已有表添加全文索引：

```sql
CREATE TABLE stock_items(
    id INT,
    title TEXT
);

-- 你可以在这里插入一些数据。
-- 即使表中已有数据，也可以创建全文索引。

ALTER TABLE stock_items ADD FULLTEXT INDEX (title) WITH PARSER MULTILINGUAL ADD_COLUMNAR_REPLICA_ON_DEMAND;
```

`WITH PARSER <PARSER_NAME>` 子句中可用的 parser 包括：

- `STANDARD`：速度快，适用于英文内容，通过空格和标点切分单词。所有文本在建立索引和搜索时都会转换为小写（不区分大小写匹配）。

- `MULTILINGUAL`：支持多种语言，包括英文、中文、日文和韩文。

### 管理全文索引 {#manage-full-text-indexes}

创建全文索引时，指定索引名称是可选的。如果不指定，TiDB 默认使用第一个被索引列的名称作为索引名。

```sql
-- 不指定索引名称时，TiDB 使用第一个被索引列名（"title"）作为索引名
ALTER TABLE stock_items ADD FULLTEXT INDEX (title) WITH PARSER MULTILINGUAL;

-- 指定索引名称
ALTER TABLE stock_items ADD FULLTEXT INDEX ft_title (title) WITH PARSER MULTILINGUAL;
```

**查看现有索引名称：**

```sql
-- Key_name 列显示索引名称
SHOW INDEX FROM stock_items;

-- 或查询 INFORMATION_SCHEMA
SELECT INDEX_NAME, COLUMN_NAME, INDEX_TYPE
FROM INFORMATION_SCHEMA.STATISTICS
WHERE TABLE_SCHEMA = 'your_database' AND TABLE_NAME = 'stock_items';
```

**删除全文索引：**

```sql
-- 先使用 SHOW INDEX 确认索引名称
ALTER TABLE stock_items DROP INDEX title;
```

#### 指定索引名称 {#specify-an-index-name}

在 `CREATE TABLE` 和 `ALTER TABLE` 语句中，你都可以在 `FULLTEXT INDEX` 或 `FULLTEXT KEY` 后指定索引名称：

```sql
-- 在 CREATE TABLE 中指定名称
CREATE TABLE users (
    id INT,
    name TEXT,
    FULLTEXT INDEX ft_name (name) WITH PARSER STANDARD
);

-- 在 ALTER TABLE 中指定名称
ALTER TABLE users ADD FULLTEXT INDEX ft_name (name) WITH PARSER STANDARD;

-- 使用独立的 CREATE FULLTEXT INDEX（必须指定索引名称）
CREATE FULLTEXT INDEX ft_name ON users (name) WITH PARSER STANDARD;
```

### 插入文本数据

向带有全文索引的表插入数据，与向其他表插入数据完全相同。

例如，你可以执行以下 SQL 语句插入多语言数据。TiDB 的多语言 parser 会自动处理文本。

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

要执行全文搜索，可以使用 `FTS_MATCH_WORD()` function。

**示例：搜索最相关的 10 个文档**

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
|    5 | ワイヤレスイヤホン ハイブリッドANC搭載 40dBまでアクティブノイズキャンセル                                            |
+------+-----------------------------------------------------------------------------------------------------------+

-- 尝试用另一种语言搜索：
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

#### 多词搜索：分词与查询语义

使用 `fts_match_word()` 时，查询字符串会按照 parser 的规则进行分词，并且每个 token 都会被独立匹配。

STANDARD parser 使用空格和标点作为分隔符，将字符串切分为单词。MULTILINGUAL parser 则根据特定语言的分词规则对字符串进行切分。

```sql
-- 此查询会被切分为两个 token："Alice" 和 "Smith"
SELECT * FROM users WHERE fts_match_word('Alice Smith', name);
```

`fts_match_word()` 使用 **OR** 语义：如果文档包含任意一个 token，就会匹配；匹配到的 token 越多，相关性得分越高。

```sql
-- 以下查询返回 name 列中包含
-- "Alice" 或 "Smith" 或两者都包含的所有行
SELECT * FROM users WHERE fts_match_word('Alice Smith', name);
```

一个常见误解是，`fts_match_word('Alice X', name)` 会将 `"Alice X"` 视为一个单独实体来进行精确匹配。实际上，它会被切分为 `Alice` 和 `X`，并使用 OR 语义。由于 `X` 是一个非常短的查询词，它可能匹配许多不相关的文档。请避免使用非常短的查询词或单个字母。

> **注意：**
>
> TiDB 全文搜索不支持精确短语匹配，即不支持要求所有查询 token 按指定顺序连续出现的匹配方式。

#### 前缀搜索

**不支持。**

#### 重复词项对相关性得分的影响

`fts_match_word()` 返回的相关性得分基于 **BM25** 算法。如果查询字符串包含重复词项，则该词项的词频在评分中会加倍。

```sql
-- "Alice" 出现两次；在 BM25 评分中，Alice 的词频为 2
SELECT * FROM users WHERE fts_match_word('Alice alice bob', name);
```

在此示例中，匹配 `Alice` 的文档相比 `bob` 会获得两倍的权重贡献。这是 BM25 算法的预期行为，因为它基于词频（TF）来评估相关性。

#### 相关性评分算法

TiDB 全文搜索使用 **BM25Tantivy** 算法来计算相关性得分。该算法是经典 BM25（Okapi BM25）算法的一个变体，使用 Count-Min Sketch 来近似文档频率（DF），以提升性能。

**BM25 公式（标准形式）：**

```
score(D, Q) = sum_{t in Q} IDF(t) * TF(t, D) * (k1 + 1) / (TF(t, D) + k1 * (1 - b + b * |D| / avgdl))
```

其中：

- `t`：查询词项
- `Q`：查询字符串（分词后的所有 token）
- `D`：正在评估的文档
- `TF(t, D)`：词项 `t` 在文档中的词频
- `IDF(t)`：逆文档频率，用于衡量词项的稀有程度
- `|D|`：文档长度
- `avgdl`：所有文档的平均文档长度
- `k1`、`b`：BM25 调优参数

TiDB 的实现使用固定值 `k1 = 1.2` 和 `b = 0.75`，这是信息检索中 BM25 的标准默认值。

返回的得分是一个非负浮点数。值越高，表示与查询的相关性越高。不同数据集之间的得分不能直接比较。

## 高级示例：与其他表 join 搜索结果

你可以将全文搜索与其他 SQL 功能（如 join 和子查询）结合使用。

假设你有一张 `users` 表和一张 `tickets` 表，并希望基于作者姓名的全文搜索结果查找其创建的工单：

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

你可以使用子查询根据作者姓名查找匹配的用户 ID，然后在外层查询中使用这些 ID 搜索并 join 相关工单信息：

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

- [混合搜索](/ai/guides/vector-search-hybrid-search.md)

## 反馈与帮助

全文搜索仍处于早期阶段，开放区域有限。如果你希望在尚未开放的区域体验全文搜索，或有任何反馈与帮助需求，欢迎联系我们：

- 在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问。
- [提交 TiDB Cloud 支持工单](https://tidb.support.pingcap.com/servicedesk/customer/portals)
