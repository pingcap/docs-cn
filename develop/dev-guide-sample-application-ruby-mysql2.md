---
title: Connect to TiDB with mysql2
summary: Learn how to connect to TiDB using Ruby mysql2. This tutorial gives Ruby sample code snippets that work with TiDB using mysql2 gem.
---

# Connect to TiDB with mysql2

TiDB is a MySQL-compatible database, and [mysql2](https://github.com/brianmario/mysql2) is one of the most popular MySQL drivers for Ruby.

In this tutorial, you can learn how to use TiDB and mysql2 to accomplish the following tasks:

- Set up your environment.
- Connect to your TiDB cluster using mysql2.
- Build and run your application. Optionally, you can find [sample code snippets](#sample-code-snippets) for basic CRUD operations.

> **Note:**
>
> This tutorial works with TiDB Serverless, TiDB Dedicated, and TiDB Self-Hosted.

## Prerequisites

To complete this tutorial, you need:

- [Ruby](https://www.ruby-lang.org/en/) >= 3.0 installed on your machine
- [Bundler](https://bundler.io/) installed on your machine
- [Git](https://git-scm.com/downloads) installed on your machine
- A TiDB cluster running

**If you don't have a TiDB cluster, you can create one as follows:**

<CustomContent platform="tidb">

- (Recommended) Follow [Creating a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster.
- Follow [Deploy a local test TiDB cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) or [Deploy a production TiDB cluster](/production-deployment-using-tiup.md) to create a local cluster.

</CustomContent>
<CustomContent platform="tidb-cloud">

- (Recommended) Follow [Creating a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster.
- Follow [Deploy a local test TiDB cluster](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) or [Deploy a production TiDB cluster](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) to create a local cluster.

</CustomContent>

## Run the sample app to connect to TiDB

This section demonstrates how to run the sample application code and connect to TiDB.

### Step 1: Clone the sample app repository

Run the following commands in your terminal window to clone the sample code repository:

```shell
git clone https://github.com/tidb-samples/tidb-ruby-mysql2-quickstart.git
cd tidb-ruby-mysql2-quickstart
```

### Step 2: Install dependencies

Run the following command to install the required packages (including `mysql2` and `dotenv`) for the sample app:

```shell
bundle install
```

<details>
<summary><b>Install dependencies for existing projects</b></summary>

For your existing project, run the following command to install the packages:

```shell
bundle add mysql2 dotenv
```

</details>

### Step 3: Configure connection information

Connect to your TiDB cluster depending on the TiDB deployment option you've selected.

<SimpleTab>
<div label="TiDB Serverless">

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Ensure the configurations in the connection dialog match your operating environment.

   - **Endpoint Type** is set to `Public`.
   - **Branch** is set to `main`.
   - **Connect With** is set to `General`.
   - **Operating System** matches the operating system where you run the application.

4. If you have not set a password yet, click **Generate Password** to generate a random password.

5. Run the following command to copy `.env.example` and rename it to `.env`:

    ```shell
    cp .env.example .env
    ```

6. Edit the `.env` file, set up the environment variables as follows, and replace the corresponding placeholders `<>` with connection parameters in the connection dialog:

    ```dotenv
   DATABASE_HOST=<host>
   DATABASE_PORT=4000
   DATABASE_USER=<user>
   DATABASE_PASSWORD=<password>
   DATABASE_NAME=test
   DATABASE_ENABLE_SSL=true
    ```

   > **Note**
   >
   > For TiDB Serverless, TLS connection **MUST** be enabled via `DATABASE_ENABLE_SSL` when using public endpoint.

7. Save the `.env` file.

</div>
<div label="TiDB Dedicated">

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Click **Allow Access from Anywhere** and then click **Download TiDB cluster CA** to download the CA certificate.

   For more details about how to obtain the connection string, refer to [TiDB Dedicated standard connection](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection).

4. Run the following command to copy `.env.example` and rename it to `.env`:

    ```shell
    cp .env.example .env
    ```

5. Edit the `.env` file, set up the environment variables as follows, and replace the corresponding placeholders `<>` with connection parameters in the connection dialog:

    ```dotenv
    DATABASE_HOST=<host>
    DATABASE_PORT=4000
    DATABASE_USER=<user>
    DATABASE_PASSWORD=<password>
    DATABASE_NAME=test
    DATABASE_ENABLE_SSL=true
    DATABASE_SSL_CA=<downloaded_ssl_ca_path>
    ```

   > **Note**
   >
   > It is recommended to enable TLS connection when using the public endpoint to connect to a TiDB Dedicated cluster.
   >
   > To enable TLS connection, modify `DATABASE_ENABLE_SSL` to `true` and use `DATABASE_SSL_CA` to specify the file path of CA certificate downloaded from the connection dialog.

6. Save the `.env` file.

</div>
<div label="TiDB Self-Hosted">

1. Run the following command to copy `.env.example` and rename it to `.env`:

    ```shell
    cp .env.example .env
    ```

2. Edit the `.env` file, set up the environment variables as follows, and replace the corresponding placeholders `<>` with your own TiDB connection information:

    ```dotenv
    DATABASE_HOST=<host>
    DATABASE_PORT=4000
    DATABASE_USER=<user>
    DATABASE_PASSWORD=<password>
    DATABASE_NAME=test
    ```

   If you are running TiDB locally, the default host address is `127.0.0.1`, and the password is empty.

3. Save the `.env` file.

</div>
</SimpleTab>

### Step 4: Run the code and check the result

Run the following command to execute the sample code:

```shell
ruby app.rb
```

If the connection is successful, the console will output the version of the TiDB cluster as follows:

```
🔌 Connected to TiDB cluster! (TiDB version: 8.0.11-TiDB-v7.5.0)
⏳ Loading sample game data...
✅ Loaded sample game data.

🆕 Created a new player with ID 12.
ℹ️ Got Player 12: Player { id: 12, coins: 100, goods: 100 }
🔢 Added 50 coins and 50 goods to player 12, updated 1 row.
🚮 Deleted 1 player data.
```

## Sample code snippets

You can refer to the following sample code snippets to complete your own application development.

For complete sample code and how to run it, check out the [tidb-samples/tidb-ruby-mysql2-quickstart](https://github.com/tidb-samples/tidb-ruby-mysql2-quickstart) repository.

### Connect to TiDB with connection options

The following code establishes a connection to TiDB with options defined in the environment variables:

```ruby
require 'dotenv/load'
require 'mysql2'
Dotenv.load # Load the environment variables from the .env file

options = {
  host: ENV['DATABASE_HOST'] || '127.0.0.1',
  port: ENV['DATABASE_PORT'] || 4000,
  username: ENV['DATABASE_USER'] || 'root',
  password: ENV['DATABASE_PASSWORD'] || '',
  database: ENV['DATABASE_NAME'] || 'test'
}
options.merge(ssl_mode: :verify_identity) unless ENV['DATABASE_ENABLE_SSL'] == 'false'
options.merge(sslca: ENV['DATABASE_SSL_CA']) if ENV['DATABASE_SSL_CA']
client = Mysql2::Client.new(options)
```

> **Note**
>
> For TiDB Serverless, TLS connection **MUST** be enabled via `DATABASE_ENABLE_SSL` when using public endpoint, but you **don't** have to specify an SSL CA certificate via `DATABASE_SSL_CA`, because mysql2 gem will search for existing CA certificates in a particular order until a file is discovered.

### Insert data

The following query creates a single player with two fields and returns the `last_insert_id`:

```ruby
def create_player(client, coins, goods)
  result = client.query(
    "INSERT INTO players (coins, goods) VALUES (#{coins}, #{goods});"
  )
  client.last_id
end
```

For more information, refer to [Insert data](/develop/dev-guide-insert-data.md).

### Query data

The following query returns the record of a specific player by ID:

```ruby
def get_player_by_id(client, id)
  result = client.query(
    "SELECT id, coins, goods FROM players WHERE id = #{id};"
  )
  result.first
end
```

For more information, refer to [Query data](/develop/dev-guide-get-data-from-single-table.md).

### Update data

The following query updated the record of a specific player by ID:

```ruby
def update_player(client, player_id, inc_coins, inc_goods)
  result = client.query(
    "UPDATE players SET coins = coins + #{inc_coins}, goods = goods + #{inc_goods} WHERE id = #{player_id};"
  )
  client.affected_rows
end
```

For more information, refer to [Update data](/develop/dev-guide-update-data.md).

### Delete data

The following query deletes the record of a specific player:

```ruby
def delete_player_by_id(client, id)
  result = client.query(
    "DELETE FROM players WHERE id = #{id};"
  )
  client.affected_rows
end
```

For more information, refer to [Delete data](/develop/dev-guide-delete-data.md).

## Best practices

By default, the mysql2 gem can search for existing CA certificates in a particular order until a file is discovered.

1. `/etc/ssl/certs/ca-certificates.crt` for Debian, Ubuntu, Gentoo, Arch, or Slackware
2. `/etc/pki/tls/certs/ca-bundle.crt` for RedHat, Fedora, CentOS, Mageia, Vercel, or Netlify
3. `/etc/ssl/ca-bundle.pem` for OpenSUSE
4. `/etc/ssl/cert.pem` for macOS or Alpine (docker container)

While it is possible to specify the CA certificate path manually, doing so might cause significant inconvenience in multi-environment deployment scenarios, because different machines and environments might store the CA certificate in different locations. Therefore, setting `sslca` to `nil` is recommended for flexibility and ease of deployment across different environments.

## Next steps

- Learn more usage of mysql2 driver from [the documentation of mysql2](https://github.com/brianmario/mysql2#readme).
- Learn the best practices for TiDB application development with the chapters in the [Developer guide](/develop/dev-guide-overview.md), such as: [Insert data](/develop/dev-guide-insert-data.md), [Update data](/develop/dev-guide-update-data.md), [Delete data](/develop/dev-guide-delete-data.md), [Query data](/develop/dev-guide-get-data-from-single-table.md), [Transactions](/develop/dev-guide-transaction-overview.md), and [SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md).
- Learn through the professional [TiDB developer courses](https://www.pingcap.com/education/) and earn [TiDB certifications](https://www.pingcap.com/education/certification/) after passing the exam.

## Need help?

Ask questions on the [Discord](https://discord.gg/vYU9h56kAX) channel.