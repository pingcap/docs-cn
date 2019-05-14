---
title: LOAD DATA | TiDB SQL Statement Reference 
summary: An overview of the usage of LOAD DATA for the TiDB database.
category: reference
---

# LOAD DATA

The `LOAD DATA` statement batch loads data into a TiDB table.

## Synopsis

**LoadDataStmt:**

![LoadDataStmt](/media/sqlgram/LoadDataStmt.png)

## Examples

```sql
mysql> CREATE TABLE trips (
    ->  trip_id bigint NOT NULL PRIMARY KEY auto_increment,
    ->  duration integer not null,
    ->  start_date datetime,
    ->  end_date datetime,
    ->  start_station_number integer,
    ->  start_station varchar(255),
    ->  end_station_number integer,
    ->  end_station varchar(255),
    ->  bike_number varchar(255),
    ->  member_type varchar(255)
    -> );
Query OK, 0 rows affected (0.14 sec)

mysql> LOAD DATA LOCAL INFILE '/mnt/evo970/data-sets/bikeshare-data/2017Q4-capitalbikeshare-tripdata.csv' INTO TABLE trips FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (duration, start_date, end_date, start_station_number, start_station, end_station_number, end_station, bike_number, member_type);

Query OK, 815264 rows affected (39.63 sec)
Records: 815264  Deleted: 0  Skipped: 0  Warnings: 0
```

## MySQL compatibility

* TiDB will by default commit every 20 000 rows. This behavior is similar to MySQL NDB Cluster, but not the default configuration with the InnoDB storage engine.

## See also

* [INSERT](/dev/reference/sql/statements/insert.md)
* [Transaction Model](/dev/reference/transactions/transaction-model.md)
* [Import Example Database](/dev/how-to/get-started/import-example-database.md)
