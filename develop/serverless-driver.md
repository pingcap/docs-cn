---
title: TiDB Cloud Serverless Driver (Beta)
summary: Learn how to connect to {{{ .starter }}} or {{{ .essential }}} from serverless and edge environments.
aliases: ['/tidbcloud/serverless-driver-config']
---

# TiDB Cloud Serverless Driver (Beta)

> **Note:**
>
> The serverless driver is in beta and only applicable to {{{ .starter }}} or {{{ .essential }}} clusters.

## Why use TiDB Cloud Serverless Driver (Beta)

Traditional TCP-based MySQL drivers are not suitable for serverless functions due to their expectation of long-lived, persistent TCP connections, which contradict the short-lived nature of serverless functions. Moreover, in edge environments such as [Vercel Edge Functions](https://vercel.com/docs/functions/edge-functions) and [Cloudflare Workers](https://workers.cloudflare.com/), where comprehensive TCP support and full Node.js compatibility may be lacking, these drivers may not work at all.

[TiDB Cloud serverless driver (Beta)](https://github.com/tidbcloud/serverless-js) for JavaScript lets you connect to your {{{ .starter }}} or {{{ .essential }}} cluster over HTTP, which is generally supported by serverless environments. With it, it is now possible to connect to {{{ .starter }}} or {{{ .essential }}} clusters from edge environments and reduce connection overhead with TCP while keeping the similar development experience of traditional TCP-based MySQL drivers.

> **Note:**
>
> If you prefer programming with RESTful API rather than SQL or ORM, you can use [Data Service (beta)](https://docs.pingcap.com/tidbcloud/data-service-overview/).

## Install the serverless driver

You can install the driver with npm:

```bash
npm install @tidbcloud/serverless
```

## Use the serverless driver

You can use the serverless driver to query data of a {{{ .starter }}} or {{{ .essential }}} cluster or perform interactive transactions.

### Query

To query data from a {{{ .starter }}} or {{{ .essential }}} cluster, you need to create a connection first. Then you can use the connection to execute raw SQL queries. For example:

```ts
import { connect } from '@tidbcloud/serverless'

const conn = connect({url: 'mysql://[username]:[password]@[host]/[database]'})
const results = await conn.execute('select * from test where id = ?',[1])
```

### Transaction (experimental)

You can also perform interactive transactions with the serverless driver. For example:

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

## Edge examples

Here are some examples of using the serverless driver in edge environments. For a complete example, you can also try this [live demo](https://github.com/tidbcloud/car-sales-insight).

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

Learn more about [using TiDB Cloud serverless driver in Vercel](https://docs.pingcap.com/tidbcloud/integrate-tidbcloud-with-vercel).

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

Learn more about [using TiDB Cloud serverless driver in Cloudflare Workers](https://docs.pingcap.com/tidbcloud/integrate-tidbcloud-with-cloudflare).

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

Learn more about [using TiDB Cloud serverless driver in Netlify](https://docs.pingcap.com/tidbcloud/integrate-tidbcloud-with-netlify#use-the-edge-function).

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

## Configure the serverless driver

You can configure TiDB Cloud serverless driver at both the connection level and the SQL level.

### Connection level configurations

At the connection level, you can make the following configurations:

| Name         | Type     | Default value | Description                                                                                                                                                                                                                                                                                                                                                  |
|--------------|----------|---------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `username`   | string   | N/A           | Username of the cluster.                                                                                                                                                                                                                                                                                                                                     |
| `password`   | string   | N/A           | Password of the cluster.                                                                                                                                                                                                                                                                                                                                     |
| `host`       | string   | N/A           | Hostname of the cluster.                                                                                                                                                                                                                                                                                                                                     |
| `database`   | string   | `test`        | Database of the cluster.                                                                                                                                                                                                                                                                                                                                     |
| `url`        | string   | N/A           | The URL for the database, in the `mysql://[username]:[password]@[host]/[database]` format, where `database` can be skipped if you intend to connect to the default database.                                                                                                                                                                                 |
| `fetch`      | function | global fetch  | Custom fetch function. For example, you can use the `undici` fetch in node.js.                                                                                                                                                                                                                                                                               |
| `arrayMode`  | bool     | `false`       | Whether to return results as arrays instead of objects. To get better performance, set it to `true`.                                                                                                                                                                                                                                                         |
| `fullResult` | bool     | `false`       | Whether to return full result object instead of just rows. To get more detailed results, set it to `true`.                                                                                                                                                                                                                                                   |
| `decoders`   | object   | `{}`          | A collection of key-value pairs, which enables you to customize the decoding process for different column types. In each pair, you can specify a column type as the key and specify a corresponding function as the value. This function takes the raw string value received from TiDB Cloud serverless driver as an argument and returns the decoded value. |

**Database URL**

> **Note:**
>
> If your username, password, or database name contains special characters, you must [percentage-encode](https://en.wikipedia.org/wiki/Percent-encoding) these characters when passing them by the URL. For example, the password `password1@//?` needs to be encoded as `password1%40%2F%2F%3F` in the URL.

When `url` is configured, there is no need to configure `host`, `username`, `password`, and `database` separately. The following codes are equivalent:

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

### SQL level options

> **Note:**
>
> The SQL level options have a higher priority over connection level configurations.

At the SQL level, you can configure the following options:

| Option       | Type   | Default value     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|--------------|--------|-------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `arrayMode`  | bool   | `false`           | Whether to return results as arrays instead of objects. To get better performance, set it to `true`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `fullResult` | bool   | `false`           | Whether to return the full result object instead of just rows. To get more detailed results, set it to `true`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `isolation`  | string | `REPEATABLE READ` | The transaction isolation level, which can be set to `READ COMMITTED` or `REPEATABLE READ`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `decoders`   | object | `{}`              | A collection of key-value pairs, which enables you to customize the decoding process for different column types. In each pair, you can specify a column type as the key and specify a corresponding function as the value. This function takes the raw string value received from TiDB Cloud serverless driver as an argument and returns the decoded value. If you have configured `decoders` at both the connection and SQL levels, the key-value pairs with different keys configured at the connection level will be merged to the SQL level to take effect. If the same key (this is, column type) is specified at both levels, the value at the SQL level takes precedence. |

**arrayMode and fullResult**

To return the full result object as arrays, you can configure the `arrayMode` and `fullResult` options as follows:

```ts
const conn = connect({url: process.env['DATABASE_URL'] || 'mysql://[username]:[password]@[host]/[database]'})
const results = await conn.execute('select * from test',null,{arrayMode:true,fullResult:true})
```

**isolation**

The `isolation` option can only be used in the `begin` function.

```ts
const conn = connect({url: 'mysql://[username]:[password]@[host]/[database]'})
const tx = await conn.begin({isolation:"READ COMMITTED"})
```

**decoders**

To customize the format of returned column values, you can configure the `decoder` option in the `connect()` method as follows:

```ts
import { connect, ColumnType } from '@tidbcloud/serverless';

const conn = connect({
  url: 'mysql://[username]:[password]@[host]/[database]',
  decoders: {
    // By default, TiDB Cloud serverless driver returns the BIGINT type as text value. This decoder converts BIGINT to the JavaScript built-in BigInt type.
    [ColumnType.BIGINT]: (rawValue: string) => BigInt(rawValue),
    
    // By default, TiDB Cloud serverless driver returns the DATETIME type as the text value in the 'yyyy-MM-dd HH:mm:ss' format. This decoder converts the DATETIME text to the JavaScript native Date object.
    [ColumnType.DATETIME]: (rawValue: string) => new Date(rawValue),
  }
})

// You can also configure the decoder option at the SQL level to override the decoders with the same keys at the connection level.
conn.execute(`select ...`, [], {
  decoders: {
    // ...
  }
})
```

> **Note:**
>
> TiDB Cloud serverless driver configuration changes:
> 
> - v0.0.7: add the SQL level option `isolation`.
> - v0.0.10: add the connection level configuration `decoders` and the SQL level option `decoders`.

## Features

### Supported SQL statements

DDL is supported and the following SQL statements are supported:  `SELECT`, `SHOW`, `EXPLAIN`, `USE`, `INSERT`, `UPDATE`, `DELETE`, `BEGIN`, `COMMIT`, `ROLLBACK`, and `SET`.

### Data type mapping

The type mapping between TiDB and Javascript is as follows:

| TiDB data type | Javascript type |
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

> **Note:**
>
> Make sure to use the default `utf8mb4` character set in TiDB Cloud for the type conversion to JavaScript strings, because TiDB Cloud serverless driver uses the UTF-8 encoding to decode them to strings. 

> **Note:**
>
> TiDB Cloud serverless driver data type mapping changes:
> 
> - v0.1.0: the `BINARY`, `VARBINARY`, `TINYBLOB`, `BLOB`, `MEDIUMBLOB`, `LONGBLOB`, and `BIT` types are now returned as a `Uint8Array` instead of a `string`.

### ORM integrations

TiDB Cloud serverless driver has been integrated with the following ORMs:

- [TiDB Cloud serverless driver Kysely dialect](https://github.com/tidbcloud/kysely).
- [TiDB Cloud serverless driver Prisma adapter](https://github.com/tidbcloud/prisma-adapter).

## Pricing

The serverless driver itself is free, but accessing data with the driver generates [Request Units (RUs)](https://docs.pingcap.com/tidbcloud/tidb-cloud-glossary#request-unit-ru) and storage usage.

- For {{{ .starter }}} clusters, the pricing follows the [{{{ .starter }}} pricing](https://www.pingcap.com/tidb-cloud-starter-pricing-details/) model.
- For {{{ .essential }}} clusters, the pricing follows the [{{{ .essential }}} pricing](https://www.pingcap.com/tidb-cloud-essential-pricing-details/) model.

## Limitations

Currently, using serverless driver has the following limitations:

- Up to 10,000 rows can be fetched in a single query.
- You can execute only a single SQL statement at a time. Multiple SQL statements in one query are not supported yet.
- Connection with [private endpoints](https://docs.pingcap.com/tidbcloud/set-up-private-endpoint-connections-serverless.md) is not supported yet.
- The server blocks requests from unauthorized browser origins via Cross-Origin Resource Sharing (CORS) to protect your credentials. As a result, you can use the serverless driver only from backend services.

## What's next

- Learn how to [use TiDB Cloud serverless driver in a local Node.js project](/develop/serverless-driver-node-example.md).
