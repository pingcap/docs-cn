---
title: Full-Text Search with Python
summary: Full-text search lets you retrieve documents for exact keywords. In Retrieval-Augmented Generation (RAG) scenarios, you can use full-text search together with vector search to improve the retrieval quality.
aliases: ['/tidb/stable/vector-search-full-text-search-python']
---

# Full-Text Search with Python

Unlike [Vector Search](/ai/vector-search-overview.md), which focuses on semantic similarity, full-text search lets you retrieve documents for exact keywords. In Retrieval-Augmented Generation (RAG) scenarios, you can use full-text search together with vector search to improve the retrieval quality.

The full-text search feature in TiDB provides the following capabilities:

- **Query text data directly**: you can search any string columns directly without the embedding process.

- **Support for multiple languages**: no need to specify the language for high-quality search. TiDB supports documents in multiple languages stored in the same table and automatically chooses the best text analyzer for each document.

- **Order by relevance**: the search result can be ordered by relevance using the widely adopted [BM25 ranking](https://en.wikipedia.org/wiki/Okapi_BM25) algorithm.

- **Fully compatible with SQL**: all SQL features, such as pre-filtering, post-filtering, grouping, and joining, can be used with full-text search.

> **Tip:**
>
> For SQL usage, see [Full-Text Search with SQL](/ai/vector-search-full-text-search-sql.md).
>
> To use full-text search and vector search together in your AI apps, see [Hybrid Search](/ai/vector-search-hybrid-search.md).

## Prerequisites

Full-text search is still in the early stages, and we are continuously rolling it out to more customers. Currently, Full-text search is only available on {{{ .starter }}} and {{{ .essential }}} in the following regions:

- AWS: `Frankfurt (eu-central-1)` and `Singapore (ap-southeast-1)`

To complete this tutorial, make sure you have a {{{ .starter }}} cluster in a supported region. If you don't have one, follow [Creating a {{{ .starter }}} cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create it.

## Get started

### Step 1. Install the [pytidb](https://github.com/pingcap/pytidb) Python SDK

[pytidb](https://github.com/pingcap/pytidb) is the official Python SDK for TiDB, designed to help developers build AI applications efficiently. It includes built-in support for vector search and full-text search.

To install the SDK, run the following command:

```shell
pip install pytidb

# (Alternative) To use the built-in embedding functions and rerankers:
# pip install "pytidb[models]"

# (Optional) To convert query results into pandas DataFrames:
# pip install pandas
```

### Step 2. Connect to TiDB

```python
from pytidb import TiDBClient

db = TiDBClient.connect(
    host="HOST_HERE",
    port=4000,
    username="USERNAME_HERE",
    password="PASSWORD_HERE",
    database="DATABASE_HERE",
)
```

You can get these connection parameters from the [TiDB Cloud console](https://tidbcloud.com):

1. Navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed, with connection parameters listed.

   For example, if the connection parameters are displayed as follows:

   ```text
   HOST:     gateway01.us-east-1.prod.shared.aws.tidbcloud.com
   PORT:     4000
   USERNAME: 4EfqPF23YKBxaQb.root
   PASSWORD: abcd1234
   DATABASE: test
   CA:       /etc/ssl/cert.pem
   ```

   The corresponding Python code to connect to the {{{ .starter }}} cluster would be as follows:

   ```python
   db = TiDBClient.connect(
       host="gateway01.us-east-1.prod.shared.aws.tidbcloud.com",
       port=4000,
       username="4EfqPF23YKBxaQb.root",
       password="abcd1234",
       database="test",
   )
   ```

   Note that the preceding example is for demonstration purposes only. You need to fill in the parameters with your own values and keep them secure.

### Step 3. Create a table and a full-text index

As an example, create a table named `chunks` with the following columns:

- `id` (int): the ID of the chunk.
- `text` (text): the text content of the chunk.
- `user_id` (int): the ID of the user who created the chunk.

```python
from pytidb.schema import TableModel, Field

class Chunk(TableModel, table=True):
    __tablename__ = "chunks"

    id: int = Field(primary_key=True)
    text: str = Field()
    user_id: int = Field()

table = db.create_table(schema=Chunk)

if not table.has_fts_index("text"):
    table.create_fts_index("text")   # 👈 Create a fulltext index on the text column.
```

### Step 4. Insert data

```python
table.bulk_insert(
    [
        Chunk(id=2, text="the quick brown", user_id=2),
        Chunk(id=3, text="fox jumps", user_id=3),
        Chunk(id=4, text="over the lazy dog", user_id=4),
    ]
)
```

### Step 5. Perform a full-text search

After inserting data, you can perform a full-text search as follows:

```python
df = (
  table.search("brown fox", search_type="fulltext")
    .limit(2)
    .to_pandas() # optional
)

#    id             text  user_id
# 0   3        fox jumps        3
# 1   2  the quick brown        2
```

For a complete example, see [pytidb full-text search demo](https://github.com/pingcap/pytidb/blob/main/examples/fulltext_search).

## See also

- [pytidb Python SDK Documentation](https://github.com/pingcap/pytidb)

- [Hybrid Search](/ai/vector-search-hybrid-search.md)

## Feedback & Help

Full-text search is still in the early stages with limited accessibility. If you would like to try full-text search in a region that is not yet available, or if you have feedback or need help, feel free to reach out to us:

- Ask the community on [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) or [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs).
- [Submit a support ticket for TiDB Cloud](https://tidb.support.pingcap.com/servicedesk/customer/portals)