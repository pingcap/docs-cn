---
title: UUID Best Practices
summary: Learn best practice and strategy for using UUIDs with TiDB.
---

# UUID Best Practices

## Overview of UUIDs

When used as a primary key, instead of an `AUTO_INCREMENT` integer value, a universally unique identifier (UUID) delivers the following benefits:

- UUIDs can be generated on multiple systems without risking conflicts. In some cases, this means that the number of network trips to TiDB can be reduced, leading to improved performance.
- UUIDs are supported by most programming languages and database systems.
- When used as a part of a URL, a UUID is not vulnerable to enumeration attacks. In comparison, with an `auto_increment` number, it is possible to guess the invoice IDs or user IDs.

## Best practices

### Store as binary

The textual UUID format looks like this: `ab06f63e-8fe7-11ec-a514-5405db7aad56`, which is a string of 36 characters. By using `UUID_TO_BIN()`, the textual format can be converted into a binary format of 16 bytes. This allows you to store the text in a `BINARY(16)` column. When retrieving the UUID, you can use the `BIN_TO_UUID()` function to get back to the textual format.

### UUID format binary order and a clustered PK

The `UUID_TO_BIN()` function can be used with one argument, the UUID or with two arguments where the second argument is a `swap_flag`.

<CustomContent platform="tidb">

It is recommended to not set the `swap_flag` with TiDB to avoid [hotspots](/best-practices/high-concurrency-best-practices.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

It is recommended to not set the `swap_flag` with TiDB to avoid hotspots.

</CustomContent>

You can also explicitly set the [`CLUSTERED` option](/clustered-indexes.md) for UUID based primary keys to avoid hotspots.

To demonstrate the effect of the `swap_flag`, here are two tables with an identical structure. The difference is that the data inserted into `uuid_demo_1` uses `UUID_TO_BIN(?, 0)` and `uuid_demo_2` uses `UUID_TO_BIN(?, 1)`.

<CustomContent platform="tidb">

In the screenshot of the [Key Visualizer](/dashboard/dashboard-key-visualizer.md) below, you can see that writes are concentrated in a single region of the `uuid_demo_2` table that has the order of the fields swapped in the binary format.

</CustomContent>

<CustomContent platform="tidb-cloud">

In the screenshot of the [Key Visualizer](/tidb-cloud/tune-performance.md#key-visualizer) below, you can see that writes are concentrated in a single region of the `uuid_demo_2` table that has the order of the fields swapped in the binary format.

</CustomContent>

![Key Visualizer](/media/best-practices/uuid_keyviz.png)

```sql
CREATE TABLE `uuid_demo_1` (
  `uuid` varbinary(16) NOT NULL,
  `c1` varchar(255) NOT NULL,
  PRIMARY KEY (`uuid`) CLUSTERED
)
```

```sql
CREATE TABLE `uuid_demo_2` (
  `uuid` varbinary(16) NOT NULL,
  `c1` varchar(255) NOT NULL,
  PRIMARY KEY (`uuid`) CLUSTERED
)
```

## MySQL compatibility

UUIDs can be used in MySQL as well. The `BIN_TO_UUID()` and `UUID_TO_BIN()` functions were introduced in MySQL 8.0. The `UUID()` function is available in earlier MySQL versions as well.
