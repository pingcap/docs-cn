---
title: Connect to TiDB with Rails framework and ActiveRecord ORM
summary: Learn how to connect to TiDB using the Rails framework. This tutorial gives Ruby sample code snippets that work with TiDB using the Rails framework and ActiveRecord ORM.
---

# Connect to TiDB with Rails Framework and ActiveRecord ORM

TiDB is a MySQL-compatible database, [Rails](https://github.com/rails/rails) is a popular web application framework written in Ruby, and [ActiveRecord ORM](https://github.com/rails/rails/tree/main/activerecord) is the object-relational mapping in Rails.

In this tutorial, you can learn how to use TiDB and Rails to accomplish the following tasks:

- Set up your environment.
- Connect to your TiDB cluster using Rails.
- Build and run your application. Optionally, you can find [sample code snippets](#sample-code-snippets) for basic CRUD operations using ActiveRecord ORM.

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
git clone https://github.com/tidb-samples/tidb-ruby-rails-quickstart.git
cd tidb-ruby-rails-quickstart
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

3. In the connection dialog, select `Rails` from the **Connect With** drop-down list and keep the default setting of the **Endpoint Type** as `Public`.

4. If you have not set a password yet, click **Create password** to generate a random password.

5. Run the following command to copy `.env.example` and rename it to `.env`:

    ```shell
    cp .env.example .env
    ```

6. Edit the `.env` file, set up the `DATABASE_URL` environment variable as follows, and copy the connection string from the connection dialog as the variable value.

    ```dotenv
    DATABASE_URL=mysql2://<user>:<password>@<host>:<port>/<database_name>?ssl_mode=verify_identity
    ```

   > **Note**
   >
   > For TiDB Serverless, TLS connection **MUST** be enabled with the `ssl_mode=verify_identity` query parameter when using public endpoint.

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

5. Edit the `.env` file, set up the `DATABASE_URL` environment variable as follows, copy the connection string from the connection dialog as the variable value, and set the `sslca` query parameter to the file path of the CA certificate downloaded from the connection dialog:

    ```dotenv
    DATABASE_URL=mysql2://<user>:<password>@<host>:<port>/<database>?ssl_mode=verify_identity&sslca=/path/to/ca.pem
    ```

   > **Note**
   >
   > It is recommended to enable TLS connection when using the public endpoint to connect to TiDB Dedicated.
   >
   > To enable TLS connection, modify the value of the `ssl_mode` query parameter to `verify_identity` and the value of  `sslca` to the file path of CA certificate downloaded from the connection dialog.

6. Save the `.env` file.

</div>
<div label="TiDB Self-Hosted">

1. Run the following command to copy `.env.example` and rename it to `.env`:

    ```shell
    cp .env.example .env
    ```

2. Edit the `.env` file, set up the `DATABASE_URL` environment variable as follows, and replace the `<user>`, `<password>`, `<host>`, `<port>`, and `<database>` with your own TiDB connection information:

    ```dotenv
    DATABASE_URL=mysql2://<user>:<password>@<host>:<port>/<database>
    ```

   If you are running TiDB locally, the default host address is `127.0.0.1`, and the password is empty.

3. Save the `.env` file.

</div>
</SimpleTab>

### Step 4: Run the code and check the result

1. Create the database and table:

    ```shell
    bundle exec rails db:create
    bundle exec rails db:migrate
    ```

2. Seed the sample data:

    ```shell
    bundle exec rails db:seed
    ```

3. Run the following command to execute the sample code:

    ```shell
    bundle exec rails runner ./quickstart.rb
    ```

If the connection is successful, the console will output the version of the TiDB cluster as follows:

```
🔌 Connected to TiDB cluster! (TiDB version: 5.7.25-TiDB-v7.1.0)
⏳ Loading sample game data...
✅ Loaded sample game data.

🆕 Created a new player with ID 12.
ℹ️ Got Player 12: Player { id: 12, coins: 100, goods: 100 }
🔢 Added 50 coins and 50 goods to player 12, updated 1 row.
🚮 Deleted 1 player data.
```

## Sample code snippets

You can refer to the following sample code snippets to complete your own application development.

For complete sample code and how to run it, check out the [tidb-samples/tidb-ruby-rails-quickstart](https://github.com/tidb-samples/tidb-ruby-rails-quickstart) repository.

### Connect to TiDB with connection options

The following code in `config/database.yml` establishes a connection to TiDB with options defined in the environment variables:

```yml
default: &default
  adapter: mysql2
  encoding: utf8mb4
  pool: <%= ENV.fetch("RAILS_MAX_THREADS") { 5 } %>
  url: <%= ENV["DATABASE_URL"] %>

development:
  <<: *default

test:
  <<: *default
  database: quickstart_test

production:
  <<: *default
```

> **Note**
>
> For TiDB Serverless, TLS connection **MUST** be enabled via setting the `ssl_mode` query parameter to `verify_identity` in `DATABASE_URL` when using public endpoint, but you **don't** have to specify an SSL CA certificate via `DATABASE_URL`, because mysql2 gem will search for existing CA certificates in a particular order until a file is discovered.

### Insert data

The following query creates a single Player with two fields and returns the created `Player` object:

```ruby
new_player = Player.create!(coins: 100, goods: 100)
```

For more information, refer to [Insert data](/develop/dev-guide-insert-data.md).

### Query data

The following query returns the record of a specific player by ID:

```ruby
player = Player.find_by(id: new_player.id)
```

For more information, refer to [Query data](/develop/dev-guide-get-data-from-single-table.md).

### Update data

The following query updates a `Player` object:

```ruby
player.update(coins: 50, goods: 50)
```

For more information, refer to [Update data](/develop/dev-guide-update-data.md).

### Delete data

The following query deletes a `Player` object:

```ruby
player.destroy
```

For more information, refer to [Delete data](/develop/dev-guide-delete-data.md).

## Best practices

By default, the mysql2 gem (used by ActiveRecord ORM to connect TiDB) will search for existing CA certificates in a particular order until a file is discovered.

1. /etc/ssl/certs/ca-certificates.crt # Debian / Ubuntu / Gentoo / Arch / Slackware
2. /etc/pki/tls/certs/ca-bundle.crt # RedHat / Fedora / CentOS / Mageia / Vercel / Netlify
3. /etc/ssl/ca-bundle.pem # OpenSUSE
4. /etc/ssl/cert.pem # MacOS / Alpine (docker container)

While it is possible to specify the CA certificate path manually, this approach may cause significant inconvenience in multi-environment deployment scenarios, as different machines and environments may store the CA certificate in varying locations. Therefore, setting `sslca` to `nil` is recommended for flexibility and ease of deployment across different environments.

## Next steps

- Learn more usage of ActiveRecord ORM from [the documentation of ActiveRecord](https://guides.rubyonrails.org/active_record_basics.html).
- Learn the best practices for TiDB application development with the chapters in the [Developer guide](/develop/dev-guide-overview.md), such as: [Insert data](/develop/dev-guide-insert-data.md), [Update data](/develop/dev-guide-update-data.md), [Delete data](/develop/dev-guide-delete-data.md), [Query data](/develop/dev-guide-get-data-from-single-table.md), [Transactions](/develop/dev-guide-transaction-overview.md), and [SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md).
- Learn through the professional [TiDB developer courses](https://www.pingcap.com/education/) and earn [TiDB certifications](https://www.pingcap.com/education/certification/) after passing the exam.

## Need help?

Ask questions on the [Discord](https://discord.gg/vYU9h56kAX) channel.