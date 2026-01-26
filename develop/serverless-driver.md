---
title: TiDB Cloud Serverless Driver (Beta)
summary: 了解如何从 serverless 和 edge 环境连接到 TiDB Cloud Starter 或 TiDB Cloud Essential。
aliases: ['/tidbcloud/serverless-driver-config']
---

# TiDB Cloud Serverless Driver (Beta) <!-- Draft translated by AI -->

> **注意：**
>
> serverless driver 目前为 beta 版本，仅适用于 TiDB Cloud Starter 或 TiDB Cloud Essential 集群。

## 为什么要使用 TiDB Cloud Serverless Driver (Beta)

传统的基于 TCP 的 MySQL driver 并不适用于 serverless 函数，因为它们期望建立长连接、持久的 TCP 连接，而这与 serverless 函数的短生命周期特性相矛盾。此外，在 [Vercel Edge Functions](https://vercel.com/docs/functions/edge-functions) 和 [Cloudflare Workers](https://workers.cloudflare.com/) 等 edge 环境中，可能缺乏对完整 TCP 支持和完整 Node.js 兼容性，这些 driver 可能根本无法工作。

[TiDB Cloud serverless driver (Beta)](https://github.com/tidbcloud/serverless-js) 针对 JavaScript，可以让你通过 HTTP 连接到 TiDB Cloud Starter 或 TiDB Cloud Essential 集群，而 HTTP 通常被 serverless 环境所支持。借助该 driver，你可以从 edge 环境连接到 TiDB Cloud Starter 或 TiDB Cloud Essential 集群，并减少 TCP 带来的连接开销，同时保持与传统基于 TCP 的 MySQL driver 类似的开发体验。

> **注意：**
>
> 如果你更喜欢使用 RESTful API 进行编程而不是 SQL 或 ORM，可以使用 [Data Service (beta)](/tidb-cloud/data-service-overview.md)。

## 安装 serverless driver

你可以通过 npm 安装该 driver：

```bash
npm install @tidbcloud/serverless
```

## 使用 serverless driver

你可以使用 serverless driver 查询 TiDB Cloud Starter 或 TiDB Cloud Essential 集群中的数据，或执行交互式事务。

### 查询

要从 TiDB Cloud Starter 或 TiDB Cloud Essential 集群查询数据，你需要先创建连接。然后可以使用该连接执行原生 SQL 查询。例如：

```ts
import { connect } from '@tidbcloud/serverless'

const conn = connect({url: 'mysql://[username]:[password]@[host]/[database]'})
const results = await conn.execute('select * from test where id = ?',[1])
```

### 事务（实验性）

你也可以使用 serverless driver 执行交互式事务。例如：

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

## Edge 环境示例

以下是在 edge 环境中使用 serverless driver 的一些示例。你也可以尝试这个完整的 [在线演示](https://github.com/tidbcloud/car-sales-insight)。

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

了解更多关于 [在 Vercel 中使用 TiDB Cloud serverless driver](/tidb-cloud/integrate-tidbcloud-with-vercel.md)。

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

了解更多关于 [在 Cloudflare Workers 中使用 TiDB Cloud serverless driver](/tidb-cloud/integrate-tidbcloud-with-cloudflare.md)。

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

了解更多关于 [在 Netlify 中使用 TiDB Cloud serverless driver](/tidb-cloud/integrate-tidbcloud-with-netlify.md#use-the-edge-function)。

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

## 配置 serverless driver

你可以在连接级别和 SQL 级别配置 TiDB Cloud serverless driver。

### 连接级别配置

在连接级别，你可以进行如下配置：

| 名称         | 类型     | 默认值         | 描述                                                                                                                                                                                                                                                                                                                                                  |
|--------------|----------|---------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `username`   | string   | N/A           | 集群的用户名。                                                                                                                                                                                                                                                                                                                                       |
| `password`   | string   | N/A           | 集群的密码。                                                                                                                                                                                                                                                                                                                                         |
| `host`       | string   | N/A           | 集群的主机名。                                                                                                                                                                                                                                                                                                                                       |
| `database`   | string   | `test`        | 集群的数据库。                                                                                                                                                                                                                                                                                                                                       |
| `url`        | string   | N/A           | 数据库的 URL，格式为 `mysql://[username]:[password]@[host]/[database]`，其中 `database` 可省略（如果你打算连接到默认数据库）。                                                                                                                                                                                 |
| `fetch`      | function | global fetch  | 自定义 fetch 函数。例如，你可以在 node.js 中使用 `undici` 的 fetch。                                                                                                                                                                                                                                          |
| `arrayMode`  | bool     | `false`       | 是否以数组而非对象的形式返回结果。为了获得更好的性能，可以设置为 `true`。                                                                                                                                                                                                                                     |
| `fullResult` | bool     | `false`       | 是否返回完整结果对象而不仅仅是行数据。为了获得更详细的结果，可以设置为 `true`。                                                                                                                                                                                                                               |
| `decoders`   | object   | `{}`          | 一组键值对，允许你自定义不同列类型的解码过程。在每个键值对中，你可以指定列类型作为 key，并指定相应的函数作为 value。该函数以 TiDB Cloud serverless driver 返回的原始字符串值为参数，并返回解码后的值。                                                                                                         |

**数据库 URL**

> **注意：**
>
> 如果你的用户名、密码或数据库名包含特殊字符，在通过 URL 传递时必须对这些字符进行 [百分号编码](https://en.wikipedia.org/wiki/Percent-encoding)。例如，密码 `password1@//?` 需要在 URL 中编码为 `password1%40%2F%2F%3F`。

当配置了 `url` 后，无需单独配置 `host`、`username`、`password` 和 `database`。以下代码是等价的：

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

在 SQL 级别，你可以配置如下选项：

| 选项         | 类型   | 默认值           | 描述                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|--------------|--------|------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `arrayMode`  | bool   | `false`          | 是否以数组而非对象的形式返回结果。为了获得更好的性能，可以设置为 `true`。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `fullResult` | bool   | `false`          | 是否返回完整结果对象而不仅仅是行数据。为了获得更详细的结果，可以设置为 `true`。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `isolation`  | string | `REPEATABLE READ`| 事务隔离级别，可设置为 `READ COMMITTED` 或 `REPEATABLE READ`。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `decoders`   | object | `{}`             | 一组键值对，允许你自定义不同列类型的解码过程。在每个键值对中，你可以指定列类型作为 key，并指定相应的函数作为 value。该函数以 TiDB Cloud serverless driver 返回的原始字符串值为参数，并返回解码后的值。如果你在连接级别和 SQL 级别都配置了 `decoders`，则连接级别中 key 不同的键值对会合并到 SQL 级别生效；如果同一个 key（即列类型）在两级都指定，则以 SQL 级别为准。 |

**arrayMode 和 fullResult**

如果你希望以数组形式返回完整结果对象，可以如下配置 `arrayMode` 和 `fullResult` 选项：

```ts
const conn = connect({url: process.env['DATABASE_URL'] || 'mysql://[username]:[password]@[host]/[database]'})
const results = await conn.execute('select * from test',null,{arrayMode:true,fullResult:true})
```

**isolation**

`isolation` 选项只能在 `begin` 方法中使用。

```ts
const conn = connect({url: 'mysql://[username]:[password]@[host]/[database]'})
const tx = await conn.begin({isolation:"READ COMMITTED"})
```

**decoders**

如果你想自定义返回列值的格式，可以在 `connect()` 方法中配置 `decoder` 选项，如下所示：

```ts
import { connect, ColumnType } from '@tidbcloud/serverless';

const conn = connect({
  url: 'mysql://[username]:[password]@[host]/[database]',
  decoders: {
    // 默认情况下，TiDB Cloud serverless driver 会将 BIGINT 类型作为文本值返回。此 decoder 将 BIGINT 转换为 JavaScript 内置的 BigInt 类型。
    [ColumnType.BIGINT]: (rawValue: string) => BigInt(rawValue),
    
    // 默认情况下，TiDB Cloud serverless driver 会将 DATETIME 类型以 'yyyy-MM-dd HH:mm:ss' 格式的文本值返回。此 decoder 将 DATETIME 文本转换为 JavaScript 原生 Date 对象。
    [ColumnType.DATETIME]: (rawValue: string) => new Date(rawValue),
  }
})

// 你也可以在 SQL 级别配置 decoder 选项，以覆盖连接级别相同 key 的 decoders。
conn.execute(`select ...`, [], {
  decoders: {
    // ...
  }
})
```

> **注意：**
>
> TiDB Cloud serverless driver 配置变更：
> 
> - v0.0.7：新增 SQL 级别选项 `isolation`。
> - v0.0.10：新增连接级别配置 `decoders` 和 SQL 级别选项 `decoders`。

## 功能特性

### 支持的 SQL 语句

支持 DDL，支持以下 SQL 语句：`SELECT`、`SHOW`、`EXPLAIN`、`USE`、`INSERT`、`UPDATE`、`DELETE`、`BEGIN`、`COMMIT`、`ROLLBACK` 和 `SET`。

### 数据类型映射

TiDB 与 Javascript 之间的类型映射如下：

| TiDB 数据类型 | Javascript 类型 |
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
> 请确保在 TiDB Cloud 中使用默认的 `utf8mb4` 字符集进行类型转换为 JavaScript 字符串，因为 TiDB Cloud serverless driver 使用 UTF-8 编码将其解码为字符串。

> **注意：**
>
> TiDB Cloud serverless driver 数据类型映射变更：
> 
> - v0.1.0：`BINARY`、`VARBINARY`、`TINYBLOB`、`BLOB`、`MEDIUMBLOB`、`LONGBLOB` 和 `BIT` 类型现在返回为 `Uint8Array`，而不是 `string`。

### ORM 集成

TiDB Cloud serverless driver 已集成以下 ORM：

- [TiDB Cloud serverless driver Kysely dialect](https://github.com/tidbcloud/kysely)。
- [TiDB Cloud serverless driver Prisma adapter](https://github.com/tidbcloud/prisma-adapter)。

## 计费

serverless driver 本身免费，但使用该 driver 访问数据会产生 [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit-ru) 和存储用量。

- 对于 TiDB Cloud Starter 集群，计费遵循 [TiDB Cloud Starter 计费](https://www.pingcap.com/tidb-cloud-starter-pricing-details/) 模型。
- 对于 TiDB Cloud Essential 集群，计费遵循 [TiDB Cloud Essential 计费](https://www.pingcap.com/tidb-cloud-essential-pricing-details/) 模型。

## 限制

目前，使用 serverless driver 有如下限制：

- 单次查询最多可获取 10,000 行数据。
- 每次只能执行一条 SQL 语句，不支持在一个查询中执行多条 SQL 语句。
- 暂不支持通过 [私有端点](/tidb-cloud/set-up-private-endpoint-connections-serverless.md) 连接。
- 为保护你的凭证，服务端会通过跨域资源共享（CORS）阻止来自未授权浏览器来源的请求。因此，你只能在后端服务中使用 serverless driver。

## 后续步骤

- 了解如何 [在本地 Node.js 项目中使用 TiDB Cloud serverless driver](/develop/serverless-driver-node-example.md)。