---
title: TiDB Cloud Serverless 驱动（Beta）
summary: 了解如何从 serverless 和边缘环境连接到 TiDB Cloud Serverless。
aliases: ['/tidbcloud/serverless-driver-config']
---

# TiDB Cloud Serverless 驱动（Beta）

## 为什么使用 TiDB Cloud Serverless 驱动（Beta）

传统的基于 TCP 的 MySQL 驱动程序不适合 serverless 函数，因为它们需要长期存在的持久 TCP 连接，这与 serverless 函数的短暂特性相矛盾。此外，在边缘环境中，如 [Vercel Edge Functions](https://vercel.com/docs/functions/edge-functions) 和 [Cloudflare Workers](https://workers.cloudflare.com/)，由于可能缺乏完整的 TCP 支持和完整的 Node.js 兼容性，这些驱动程序可能完全无法工作。

JavaScript 版本的 [TiDB Cloud serverless 驱动（Beta）](https://github.com/tidbcloud/serverless-js) 允许你通过 HTTP 连接到 TiDB Cloud Serverless 集群，这通常在 serverless 环境中都支持。有了它，现在可以从边缘环境连接到 TiDB Cloud Serverless 集群，并减少 TCP 的连接开销，同时保持与传统基于 TCP 的 MySQL 驱动程序类似的开发体验。

> **注意：**
>
> 如果你更喜欢使用 RESTful API 而不是 SQL 或 ORM 进行编程，可以使用 [Data Service (beta)](/tidb-cloud/data-service-overview.md)。

## 安装 serverless 驱动

你可以使用 npm 安装驱动：

```bash
npm install @tidbcloud/serverless
```

## 使用 serverless 驱动

你可以使用 serverless 驱动查询 TiDB Cloud Serverless 集群的数据或执行交互式事务。

### 查询

要从 TiDB Cloud Serverless 集群查询数据，你需要先创建一个连接。然后你可以使用该连接执行原始 SQL 查询。例如：

```ts
import { connect } from '@tidbcloud/serverless'

const conn = connect({url: 'mysql://[username]:[password]@[host]/[database]'})
const results = await conn.execute('select * from test where id = ?',[1])
```

### 事务（实验性）

你也可以使用 serverless 驱动执行交互式事务。例如：

```ts
import { connect } from '@tidbcloud/serverless'

const conn = connect({url: 'mysql://[username]:[password]@[host]/[database]'})
const tx = await conn.begin()

try {
  await tx.execute('insert into test values (1)')
  await tx.execute('select * from test')
  await tx.commit()
} catch (err) {
  await tx.rollback()
  throw err
}
```

## 边缘环境示例

以下是在边缘环境中使用 serverless 驱动的一些示例。完整示例可以尝试这个[在线演示](https://github.com/tidbcloud/car-sales-insight)。

<SimpleTab>

<div label="Vercel Edge Function">

```ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { connect } from '@tidbcloud/serverless'
export const runtime = 'edge'

export async function GET(request: NextRequest) {
  const conn = connect({url: process.env.DATABASE_URL})
  const result = await conn.execute('show tables')
  return NextResponse.json({result});
}
```

了解更多关于[在 Vercel 中使用 TiDB Cloud serverless 驱动](/tidb-cloud/integrate-tidbcloud-with-vercel.md)。

</div>

<div label="Cloudflare Workers">

```ts
import { connect } from '@tidbcloud/serverless'
export interface Env {
  DATABASE_URL: string;
}
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const conn = connect({url: env.DATABASE_URL})
    const result = await conn.execute('show tables')
    return new Response(JSON.stringify(result));
  },
};
```

了解更多关于[在 Cloudflare Workers 中使用 TiDB Cloud serverless 驱动](/tidb-cloud/integrate-tidbcloud-with-cloudflare.md)。

</div>

<div label="Netlify Edge Function">

```ts
import { connect } from 'https://esm.sh/@tidbcloud/serverless'

export default async () => {
  const conn = connect({url: Netlify.env.get('DATABASE_URL')})
  const result = await conn.execute('show tables')
  return new Response(JSON.stringify(result));
}
```

了解更多关于[在 Netlify 中使用 TiDB Cloud serverless 驱动](/tidb-cloud/integrate-tidbcloud-with-netlify.md#use-the-edge-function)。

</div>

<div label="Deno">

```ts
import { connect } from "npm:@tidbcloud/serverless"

const conn = connect({url: Deno.env.get('DATABASE_URL')})
const result = await conn.execute('show tables')
```

</div>

<div label="Bun">

```ts
import { connect } from "@tidbcloud/serverless"

const conn = connect({url: Bun.env.DATABASE_URL})
const result = await conn.execute('show tables')
```

</div>

</SimpleTab>

## 配置 serverless 驱动

你可以在连接级别和 SQL 级别配置 TiDB Cloud serverless 驱动。

### 连接级别配置

在连接级别，你可以进行以下配置：

| 名称         | 类型     | 默认值 | 描述                                                                                                                                                                                                                                                                                                                                                  |
|--------------|----------|---------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `username`   | string   | N/A     | TiDB Cloud Serverless 的用户名                                                                                                                                                                                                                                                                                                                                  |
| `password`   | string   | N/A     | TiDB Cloud Serverless 的密码                                                                                                                                                                                                                                                                                                                                  |
| `host`       | string   | N/A     | TiDB Cloud Serverless 的主机名                                                                                                                                                                                                                                                                                                                                  |
| `database`   | string   | `test`  | TiDB Cloud Serverless 的数据库                                                                                                                                                                                                                                                                                                                                  |
| `url`        | string   | N/A     | 数据库的 URL，格式为 `mysql://[username]:[password]@[host]/[database]`，如果你打算连接到默认数据库，可以省略 `database`。                                                                                                                                                                                                                                                                                 |
| `fetch`      | function | global fetch | 自定义 fetch 函数。例如，你可以在 node.js 中使用 `undici` fetch。                                                                                                                                                                                                                                                                               |
| `arrayMode`  | bool     | `false` | 是否将结果以数组而不是对象形式返回。要获得更好的性能，请设置为 `true`。                                                                                                                                                                                                                                                                         |
| `fullResult` | bool     | `false` | 是否返回完整的结果对象而不是仅返回行。要获得更详细的结果，请设置为 `true`。                                                                                                                                                                                                                                                                   |
| `decoders`   | object   | `{}`    | 一组键值对，使你能够自定义不同列类型的解码过程。在每个键值对中，你可以指定一个列类型作为键，并指定一个相应的函数作为值。这个函数接收从 TiDB Cloud serverless 驱动接收到的原始字符串值作为参数，并返回解码后的值。 |

**数据库 URL**

> **注意：**
>
> 如果你的用户名、密码或数据库名称包含特殊字符，在通过 URL 传递时必须对这些字符进行[百分比编码](https://en.wikipedia.org/wiki/Percent-encoding)。例如，密码 `password1@//?` 需要在 URL 中编码为 `password1%40%2F%2F%3F`。

当配置了 `url` 时，就不需要单独配置 `host`、`username`、`password` 和 `database`。以下代码是等效的：

```ts
const config = {
  host: '<host>',
  username: '<user>',
  password: '<password>',
  database: '<database>',
  arrayMode: true,
}

const conn = connect(config)
```

```ts
const config = {
  url: process.env['DATABASE_URL'] || 'mysql://[username]:[password]@[host]/[database]',
  arrayMode: true
}

const conn = connect(config)
```

### SQL 级别选项

> **注意：**
>
> SQL 级别选项的优先级高于连接级别配置。

在 SQL 级别，你可以配置以下选项：

| 选项         | 类型   | 默认值            | 描述                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|--------------|--------|-------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `arrayMode`  | bool   | `false`          | 是否将结果以数组而不是对象形式返回。要获得更好的性能，请设置为 `true`。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `fullResult` | bool   | `false`          | 是否返回完整的结果对象而不是仅返回行。要获得更详细的结果，请设置为 `true`。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `isolation`  | string | `REPEATABLE READ`| 事务隔离级别，可以设置为 `READ COMMITTED` 或 `REPEATABLE READ`。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `decoders`   | object | `{}`             | 一组键值对，使你能够自定义不同列类型的解码过程。在每个键值对中，你可以指定一个列类型作为键，并指定一个相应的函数作为值。这个函数接收从 TiDB Cloud serverless 驱动接收到的原始字符串值作为参数，并返回解码后的值。如果你在连接级别和 SQL 级别都配置了 `decoders`，连接级别配置的具有不同键的键值对将合并到 SQL 级别生效。如果在两个级别都指定了相同的键（即列类型），SQL 级别的值优先。 |

**arrayMode 和 fullResult**

要将完整的结果对象以数组形式返回，你可以按如下方式配置 `arrayMode` 和 `fullResult` 选项：

```ts
const conn = connect({url: process.env['DATABASE_URL'] || 'mysql://[username]:[password]@[host]/[database]'})
const results = await conn.execute('select * from test',null,{arrayMode:true,fullResult:true})
```

**isolation**

`isolation` 选项只能在 `begin` 函数中使用。

```ts
const conn = connect({url: 'mysql://[username]:[password]@[host]/[database]'})
const tx = await conn.begin({isolation:"READ COMMITTED"})
```

**decoders**

要自定义返回的列值格式，你可以在 `connect()` 方法中按如下方式配置 `decoder` 选项：

```ts
import { connect, ColumnType } from '@tidbcloud/serverless';

const conn = connect({
  url: 'mysql://[username]:[password]@[host]/[database]',
  decoders: {
    // 默认情况下，TiDB Cloud serverless 驱动将 BIGINT 类型作为文本值返回。这个解码器将 BIGINT 转换为 JavaScript 内置的 BigInt 类型。
    [ColumnType.BIGINT]: (rawValue: string) => BigInt(rawValue),
    
    // 默认情况下，TiDB Cloud serverless 驱动将 DATETIME 类型作为 'yyyy-MM-dd HH:mm:ss' 格式的文本值返回。这个解码器将 DATETIME 文本转换为 JavaScript 原生 Date 对象。
    [ColumnType.DATETIME]: (rawValue: string) => new Date(rawValue),
  }
})

// 你也可以在 SQL 级别配置 decoder 选项来覆盖连接级别具有相同键的解码器。
conn.execute(`select ...`, [], {
  decoders: {
    // ...
  }
})
```

> **注意：**
>
> TiDB Cloud serverless 驱动配置变更：
> 
> - v0.0.7：添加 SQL 级别选项 `isolation`。
> - v0.0.10：添加连接级别配置 `decoders` 和 SQL 级别选项 `decoders`。

## 功能特性

### 支持的 SQL 语句

支持 DDL 和以下 SQL 语句：`SELECT`、`SHOW`、`EXPLAIN`、`USE`、`INSERT`、`UPDATE`、`DELETE`、`BEGIN`、`COMMIT`、`ROLLBACK` 和 `SET`。

### 数据类型映射

TiDB Cloud Serverless 和 Javascript 之间的类型映射如下：

| TiDB Cloud Serverless 类型 | Javascript 类型 |
|----------------------|-----------------|
| TINYINT              | number          |
| UNSIGNED TINYINT     | number          |
| BOOL                 | number          |
| SMALLINT             | number          |
| UNSIGNED SMALLINT    | number          |
| MEDIUMINT            | number          |
| INT                  | number          |
| UNSIGNED INT         | number          |
| YEAR                 | number          |
| FLOAT                | number          |
| DOUBLE               | number          |
| BIGINT               | string          |
| UNSIGNED BIGINT      | string          |
| DECIMAL              | string          |
| CHAR                 | string          |
| VARCHAR              | string          |
| BINARY               | Uint8Array      |
| VARBINARY            | Uint8Array      |
| TINYTEXT             | string          |
| TEXT                 | string          |
| MEDIUMTEXT           | string          |
| LONGTEXT             | string          |
| TINYBLOB             | Uint8Array      |
| BLOB                 | Uint8Array      |
| MEDIUMBLOB           | Uint8Array      |
| LONGBLOB             | Uint8Array      |
| DATE                 | string          |
| TIME                 | string          |
| DATETIME             | string          |
| TIMESTAMP            | string          |
| ENUM                 | string          |
| SET                  | string          |
| BIT                  | Uint8Array      |
| JSON                 | object          |
| NULL                 | null            |
| Others               | string          |

> **注意：**
>
> 确保在 TiDB Cloud Serverless 中使用默认的 `utf8mb4` 字符集进行 JavaScript 字符串的类型转换，因为 TiDB Cloud serverless 驱动使用 UTF-8 编码将它们解码为字符串。

> **注意：**
>
> TiDB Cloud serverless 驱动数据类型映射变更：
> 
> - v0.1.0：`BINARY`、`VARBINARY`、`TINYBLOB`、`BLOB`、`MEDIUMBLOB`、`LONGBLOB` 和 `BIT` 类型现在返回 `Uint8Array` 而不是 `string`。

### ORM 集成

TiDB Cloud serverless 驱动已经与以下 ORM 集成：

- [TiDB Cloud serverless 驱动 Kysely 方言](https://github.com/tidbcloud/kysely)。
- [TiDB Cloud serverless 驱动 Prisma 适配器](https://github.com/tidbcloud/prisma-adapter)。

## 定价

serverless 驱动本身是免费的，但使用驱动访问数据会产生 [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit) 和存储使用量。定价遵循 [TiDB Cloud Serverless 定价](https://www.pingcap.com/tidb-serverless-pricing-details/) 模型。

## 限制

目前，使用 serverless 驱动有以下限制：

- 单个查询最多可以获取 10,000 行数据。
- 一次只能执行一条 SQL 语句。目前不支持在一个查询中执行多条 SQL 语句。
- 尚不支持通过[私有端点](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)连接。

## 下一步

- 了解如何[在本地 Node.js 项目中使用 TiDB Cloud serverless 驱动](/tidb-cloud/serverless-driver-node-example.md)。
