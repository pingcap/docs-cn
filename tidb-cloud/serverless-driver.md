---
title: TiDB Cloud Serverless Driver (Beta)
summary: Learn how to connect to TiDB Serverless from serverless and edge environments.
aliases: ['/tidbcloud/serverless-driver-config']
---

# TiDB Cloud Serverless Driver (Beta)

## Why use TiDB Cloud Serverless Driver (Beta)

Traditional TCP-based MySQL drivers are not suitable for serverless functions due to their expectation of long-lived, persistent TCP connections, which contradict the short-lived nature of serverless functions. Moreover, in edge environments such as [Vercel Edge Functions](https://vercel.com/docs/functions/edge-functions) and [Cloudflare Workers](https://workers.cloudflare.com/), where comprehensive TCP support and full Node.js compatibility may be lacking, these drivers may not work at all.

[TiDB Cloud serverless driver (Beta)](https://github.com/tidbcloud/serverless-js) for JavaScript allows you to connect to your TiDB Serverless cluster over HTTP, which is generally supported by serverless environments. With it, it is now possible to connect to TiDB Serverless clusters from edge environments and reduce connection overhead with TCP while keeping the similar development experience of traditional TCP-based MySQL drivers. 

> **Note:**
>
> If you prefer programming with RESTful API rather than SQL or ORM, you can use [Data Service (beta)](/tidb-cloud/data-service-overview.md).

## Install the serverless driver

You can install the driver with npm:

```bash
npm install @tidbcloud/serverless
```

## Use the serverless driver

You can use the serverless driver to query data of a TiDB Serverless cluster or perform interactive transactions.

### Query

To query data from a TiDB Serverless cluster, you need to create a connection first. Then you can use the connection to execute raw SQL queries. For example:

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
}catch (err) {
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

Learn more about [using TiDB Cloud serverless driver in Vercel](/tidb-cloud/integrate-tidbcloud-with-vercel.md).

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

Learn more about [using TiDB Cloud serverless driver in Cloudflare Workers](/tidb-cloud/integrate-tidbcloud-with-cloudflare.md).

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

Learn more about [using TiDB Cloud serverless driver in Netlify](/tidb-cloud/integrate-tidbcloud-with-netlify.md#use-the-edge-function).

</div>

<div label="Deno">

```ts
import { connect } from "npm:@tidbcloud/serverless-js"

const conn = connect({url: Deno.env.get('DATABASE_URL')})
const result = await conn.execute('show tables')
```

</div>

<div label="Bun">

```ts
import { connect } from "@tidbcloud/serverless-js"

const conn = connect({url: Bun.env.DATABASE_URL})
const result = await conn.execute('show tables')
```

</div>

</SimpleTab>

## Configure the serverless driver

You can configure TiDB Cloud serverless driver at both the connection level and the SQL level.

### Connection level configurations

At the connection level, you can make the following configurations:

| Name         | Type       | Default value | Description                                                                                                                                                                  |
|--------------|------------|---------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `username`   | string     | N/A           | Username of TiDB Serverless                                                                                                                                                  |
| `password`   | string     | N/A           | Password of TiDB Serverless                                                                                                                                                  |
| `host`       | string     | N/A           | Hostname of TiDB Serverless                                                                                                                                                  |
| `database`   | string     | `test`        | Database of TiDB Serverless                                                                                                                                                  |
| `url`        | string     | N/A           | The URL for the database, in the `mysql://[username]:[password]@[host]/[database]` format, where `database` can be skipped if you intend to connect to the default database. |
| `fetch`      | function   | global fetch  | Custom fetch function. For example, you can use the `undici` fetch in node.js.                                                                                               |
| `arrayMode`  | bool       | `false`       | Whether to return results as arrays instead of objects. To get better performance, set it to `true`.                                                                         |
| `fullResult` | bool       | `false`       | Whether to return full result object instead of just rows. To get more detailed results, set it to `true`.                                                                   |

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

| Option       | Type | Default value | Description                                                                                                |
|--------------|------|---------------|------------------------------------------------------------------------------------------------------------|
| `arrayMode`  | bool | `false`       | Whether to return results as arrays instead of objects. To get better performance, set it to `true`.       |
| `fullResult` | bool | `false`       | Whether to return full result object instead of just rows. To get more detailed results, set it to `true`. |

For example:

```ts
const conn = connect({url: process.env['DATABASE_URL'] || 'mysql://[username]:[password]@[host]/[database]'})
const results = await conn.execute('select * from test',null,{arrayMode:true,fullResult:true})
```

Starting from TiDB Cloud serverless driver v0.0.7, you can also configure the following SQL level option when you use transactions:

| Option       | Type   | Default value     | Description                                                                        |
|--------------|--------|-------------------|------------------------------------------------------------------------------------|
| `isolation`  | string | `REPEATABLE READ` | The transaction isolation level, which can be set to `READ COMMITTED` or `REPEATABLE READ`.    |

The `isolation` option can only be used in the `begin` function. Here is an example:

```ts
const conn = connect({url: 'mysql://[username]:[password]@[host]/[database]'})
const tx = await conn.begin({isolation:"READ COMMITTED"})
```

## Features

### Supported SQL statements

DDL is supported and the following SQL statements are supported:  `SELECT`, `SHOW`, `EXPLAIN`, `USE`, `INSERT`, `UPDATE`, `DELETE`, `BEGIN`, `COMMIT`, `ROLLBACK`, and `SET`.

### Data type mapping

The type mapping between TiDB Serverless and Javascript is as follows:

| TiDB Serverless type | Javascript type |
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
| BINARY               | string          |
| VARBINARY            | string          |
| TINYTEXT             | string          |
| TEXT                 | string          |
| MEDIUMTEXT           | string          |
| LONGTEXT             | string          |
| TINYBLOB             | string          |
| BLOB                 | string          |
| MEDIUMBLOB           | string          |
| LONGBLOB             | string          |
| DATE                 | string          |
| TIME                 | string          |
| DATETIME             | string          |
| TIMESTAMP            | string          |
| ENUM                 | string          |
| SET                  | string          |
| BIT                  | string          |
| JSON                 | object          |
| NULL                 | null            |
| Others               | string          |

### ORM integrations

TiDB Cloud serverless driver has been integrated with the following ORMs:

- [TiDB Cloud serverless driver Kysely dialect](https://github.com/tidbcloud/kysely).
- [TiDB Cloud serverless driver Prisma adapter](https://github.com/tidbcloud/prisma-adapter).

## Pricing

The serverless driver itself is free, but accessing data with the driver generates [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit) and storage usage. The pricing follows the [TiDB Serverless pricing](https://www.pingcap.com/tidb-serverless-pricing-details/) model.

## Limitations

Currently, using serverless driver has the following limitations:

- Up to 10,000 rows can be fetched in a single query.
- You can execute only a single SQL statement at a time. Multiple SQL statements in one query are not supported yet.
- Connection with [private endpoints](/tidb-cloud/set-up-private-endpoint-connections-serverless.md) is not supported yet.

## What's next

- Learn how to [use TiDB Cloud serverless driver in a local Node.js project](/tidb-cloud/serverless-driver-node-example.md).
