---
title: Naming Conventions for Data Import
summary: Learn about the naming conventions for CSV, Parquet, Aurora Snapshot, and SQL files during data import.
---

# Naming Conventions for Data Import

You can import data into TiDB Cloud in the following file formats: CSV, Parquet, Aurora Snapshot, and SQL. To make sure that your data is imported successfully, you need to prepare the following two types of files:

- **Schema file**. Prepare the database schema file (optional) and the table schema file, both in SQL format (`.sql`). If the table schema file is not provided, you need to create the corresponding table manually in the target database in advance.
- **Data file**. Prepare a data file that conforms to the naming conventions for importing data. If the data file name can not meet the requirements, it is recommended to use [**File Pattern**](#file-pattern) to perform the import task. Otherwise, the import task cannot scan the data files you want to import.

## Naming conventions for schema files

This section describes the naming conventions for database and table schema files. The naming conventions for schema files are the same for all the following types of source files: CSV, Parquet, Aurora Snapshot, and SQL.

The naming conventions for schema files are as follows:

- Database schema file (optional): `${db_name}-schema-create.sql`
- Table schema file: `${db_name}.${table_name}-schema.sql`

The following is an example of a database schema file:

- Name: `import_db-schema-create.sql`
- File content:

    ```sql
    CREATE DATABASE import_db;
    ```

The following is an example of a table schema file:

- Name: `import_db.test_table-schema.sql`
- File content:

    ```sql
    CREATE TABLE test_table (
        id INTEGER PRIMARY KEY,
        val VARCHAR(255)
    );
    ```

## Naming conventions for data files

This section describes the naming conventions for data files. Depending on the type of source files, the naming conventions for data files are different.

### CSV

When you import CSV files, name the data files as follows:

`${db_name}.${table_name}${suffix}.csv.${compress}`

`${suffix}` is optional and can be one of the following formats, where *`xxx`* can be any number:

- *`.xxx`*, such as `.01`
- *`._xxx_xxx_xxx`*, such as `._0_0_01`
- *`_xxx_xxx_xxx`*, such as `_0_0_01`

`${compress}` is the compression format and it is optional. TiDB Cloud supports the following formats: `.gzip`, `.gz`, `.zstd`, `.zst` and `.snappy`.

For example, the target database and table of all the following files are `import_db` and `test_table`:

- `import_db.test_table.csv`
- `import_db.test_table.01.csv`
- `import_db.test_table._0_0_01.csv`
- `import_db.test_table_0_0_01.csv`
- `import_db.test_table_0_0_01.csv.gz`

### Parquet

When you import Parquet files, name the data files as follows:

`${db_name}.${table_name}${suffix}.parquet` (`${suffix}` is optional)

For example:

- `import_db.test_table.parquet`
- `import_db.test_table.01.parquet`

### Aurora Snapshot

For Aurora Snapshot files, all files with the `.parquet` suffix in the `${db_name}.${table_name}/` folder conform to the naming convention. A data file name can contain any prefix consisting of "a-z, 0-9, - , _ , ." and suffix ".parquet".

For example:

- `import_db.test_table/mydata.parquet`
- `import_db.test_table/part001/mydata.parquet`
- `import_db.test_table/part002/mydata-part002.parquet`

### SQL

When you import SQL files, name the data files as follows:

`${db_name}.${table_name}${suffix}.sql.${compress}`

`${suffix}` is optional and can be one of the following formats, where *`xxx`* can be any number:

- *`.xxx`*, such as `.01`
- *`._xxx_xxx_xxx`*, such as `._0_0_01`
- *`_xxx_xxx_xxx`*, such as `_0_0_01`

`${compress}` is the compression format and it is optional. TiDB Cloud supports the following formats: `.gzip`, `.gz`, `.zstd`, `.zst` and `.snappy`.

For example:

- `import_db.test_table.sql`
- `import_db.test_table.01.sql`
- `import_db.test_table.01.sql.gz`

If the SQL file is exported through TiDB Dumpling with the default configuration, it conforms to the naming convention by default.

## File pattern

If the source data file of CSV or Parquet does not conform to the naming convention, you can use the file pattern feature to establish the name mapping relationship between the source data file and the target table. This feature does not support Aurora Snapshot and SQL data files.

- For CSV files, see **File Pattern** in [Step 4. Import CSV files to TiDB Cloud](/tidb-cloud/import-csv-files.md#step-4-import-csv-files-to-tidb-cloud)
- For Parquet files, see **File Pattern** in [Step 4. Import Parquet files to TiDB Cloud](/tidb-cloud/import-parquet-files.md#step-4-import-parquet-files-to-tidb-cloud) 
