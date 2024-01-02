---
title: Import Data into TiDB Cloud via MySQL CLI
summary: Learn how to import Data into TiDB Cloud via MySQL CLI.
---

# Import Data into TiDB Cloud via MySQL CLI

This document describes how to import data into TiDB Cloud via the [MySQL Command-Line Client](https://dev.mysql.com/doc/refman/8.0/en/mysql.html). You can import data from an SQL file or a CSV file. The following sections provide step-by-step instructions for importing data from each type of file.

## Prerequisites

Before you can import data via MySQL CLI to TiDB Cloud, you need the following prerequisites:

- You have access to your TiDB Cloud cluster. If you do not have a TiDB cluster, create one following the instructions in [Build a TiDB Serverless Cluster](/develop/dev-guide-build-cluster-in-cloud.md).
- Install MySQL CLI on your local computer.

## Step 1. Connect to your TiDB Cloud cluster

Connect to your TiDB cluster depending on the TiDB deployment option you have selected.

<SimpleTab>
<div label="TiDB Serverless">

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Ensure the configurations in the connection dialog match your operating environment.

    - **Endpoint Type** is set to `Public`.
    - **Connect With** is set to `MySQL CLI`.
    - **Operating System** matches your environment.

4. Click **Generate Password** to create a random password.

    > **Tip:**
    >
    > If you have created a password before, either use the original password or click **Reset Password** to generate a new one.

</div>
<div label="TiDB Dedicated">

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Click **Allow Access from Anywhere**.

    For more details about how to obtain the connection string, see [Connect to TiDB Dedicated via Standard Connection](/tidb-cloud/connect-via-standard-connection.md).

</div>
</SimpleTab>

## Step 2. Define the table and insert sample data

Before importing data, you need to prepare the table structure and insert real sample data into it. The following is an example SQL file (`product_data.sql`) that you can use to create a table and insert sample data:

```sql
-- Create a table in your TiDB database
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255),
    price DECIMAL(10, 2)
);

-- Insert sample data into the table
INSERT INTO products (product_id, product_name, price) VALUES
    (1, 'Laptop', 999.99),
    (2, 'Smartphone', 499.99),
    (3, 'Tablet', 299.99);
```

## Step 3. Import data from a SQL or CSV file

You can import data from an SQL file or a CSV file. The following sections provide step-by-step instructions for importing data from each type.

<SimpleTab>
<div label="From an SQL file">

Do the following to import data from an SQL file:

1. Provide a real SQL file (for example, `product_data.sql`) that contains the data you want to import. This SQL file must contain `INSERT` statements with real data.

2. Use the following command to import data from the SQL file:

    ```bash
    mysql --comments --connect-timeout 150 -u '<your_username>' -h <your_cluster_host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=<your_ca_path> -p <your_password> < product_data.sql
    ```

> **Note:**
>
> The default database name used here is `test`, and you can either manually create your own database or use the `CREATE DATABASE` command in an SQL file.

</div>
<div label="From a CSV file">

Do the following to import data from a CSV file:

1. Create a database and schema in TiDB to match your data import needs.

2. Provide a sample CSV file (for example, `product_data.csv`) that contains the data you want to import. The following is an example of a CSV file:

    **product_data.csv:**

    ```csv
    product_id,product_name,price
    4,Laptop,999.99
    5,Smartphone,499.99
    6,Tablet,299.99
    ```

3. Use the following command to import data from the CSV file:

    ```bash
    mysql --comments --connect-timeout 150 -u '<your_username>' -h <your_host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=<your_ca_path> -p<your_password> -e "LOAD DATA LOCAL INFILE '<your_csv_path>' INTO TABLE products
    FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\n'
    IGNORE 1 LINES (product_id, product_name, price);"
    ```

4. Make sure to replace the paths, table name (`products` in this example), `<your_username>`, `<your_host>`, `<your_password>`, `<your_csv_path>`, `<your_ca_path>`, and other placeholders with your actual information, and replace the sample CSV data with your real dataset as needed.

> **Note:**
>
> For more syntax details about `LOAD DATA LOCAL INFILE`, see [`LOAD DATA`](/sql-statements/sql-statement-load-data.md).

</div>
</SimpleTab>
