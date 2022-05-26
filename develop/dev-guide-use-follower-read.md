---
title: Follower Read
summary: Learn how to use Follower Read to optimize query performance.
---

# Follower Read

This document introduces how to use Follower Read to optimize query performance.

## Introduction

TiDB uses [Region](/tidb-storage.md#region) as the basic unit to distribute data to all nodes in the cluster. A Region can have multiple replicas, and the replicas are divided into a leader and multiple followers. When the data on the leader changes, TiDB will update the data to the followers synchronously.

By default, TiDB only reads and writes data on the leader of the same Region. When a read hotspot occurs in a Region, the Region leader can become a read bottleneck for the entire system. In this situation, enabling the Follower Read feature can significantly reduce the load of the leader and improve the throughput of the whole system by balancing the load among multiple followers.

## When to use

You can visually analyze whether your application has a hotspot Region on the [TiDB Dashboard Key Visualizer Page](/dashboard/dashboard-key-visualizer.md). You can check whether a read hotspot occurs by selecting the "metrics selection box" to `Read (bytes)` or `Read (keys)`.

For more information about handling hotspot, see [TiDB Hotspot Problem Handling](/troubleshoot-hot-spot-issues.md).

If read hotspots are unavoidable or the changing cost is very high, you can try using the Follower Read feature to better load the balance of reading requests to the follower Region.

## Enable Follower Read

<SimpleTab>
<div label="SQL">

To enable Follower Read, set the variable `tidb_replica_read` (default value is `leader`) to `follower` or `leader-and-follower`:

{{< copyable "sql" >}}

```sql
SET [GLOBAL] tidb_replica_read = 'follower';
```

For more details about this variable, see [Follower Read Usage](/follower-read.md#usage).

</div>
<div label="Java">

In Java, to enable Follower Read, define a `FollowerReadHelper` class.

{{< copyable "" >}}

```java
public enum FollowReadMode {
    LEADER("leader"),
    FOLLOWER("follower"),
    LEADER_AND_FOLLOWER("leader-and-follower");

    private final String mode;

    FollowReadMode(String mode) {
        this.mode = mode;
    }

    public String getMode() {
        return mode;
    }
}

public class FollowerReadHelper {

    public static void setSessionReplicaRead(Connection conn, FollowReadMode mode) throws SQLException {
        if (mode == null) mode = FollowReadMode.LEADER;
        PreparedStatement stmt = conn.prepareStatement(
            "SET @@tidb_replica_read = ?;"
        );
        stmt.setString(1, mode.getMode());
        stmt.execute();
    }

    public static void setGlobalReplicaRead(Connection conn, FollowReadMode mode) throws SQLException {
        if (mode == null) mode = FollowReadMode.LEADER;
        PreparedStatement stmt = conn.prepareStatement(
            "SET GLOBAL @@tidb_replica_read = ?;"
        );
        stmt.setString(1, mode.getMode());
        stmt.execute();
    }

}
```

When reading data from the Follower node, use the `setSessionReplicaRead(conn, FollowReadMode.LEADER_AND_FOLLOWER)` method to enable the Follower Read feature, which can balance the load between the Leader node and the Follower node in the current session. When the connection is disconnected, it will be restored to the original mode.

{{< copyable "" >}}

```java
public static class AuthorDAO {

    // Omit initialization of instance variables...

    public void getAuthorsByFollowerRead() throws SQLException {
        try (Connection conn = ds.getConnection()) {
            // Enable the follower read feature.
            FollowerReadHelper.setSessionReplicaRead(conn, FollowReadMode.LEADER_AND_FOLLOWER);

            // Read the authors list for 100000 times.
            Random random = new Random();
            for (int i = 0; i < 100000; i++) {
                Integer birthYear = 1920 + random.nextInt(100);
                List<Author> authors = this.getAuthorsByBirthYear(birthYear);
                System.out.println(authors.size());
            }
        }
    }

    public List<Author> getAuthorsByBirthYear(Integer birthYear) throws SQLException {
        List<Author> authors = new ArrayList<>();
        try (Connection conn = ds.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement("SELECT id, name FROM authors WHERE birth_year = ?");
            stmt.setInt(1, birthYear);
            ResultSet rs = stmt.executeQuery();
            while (rs.next()) {
                Author author = new Author();
                author.setId( rs.getLong("id"));
                author.setName(rs.getString("name"));
                authors.add(author);
            }
        }
        return authors;
    }
}
```

</div>
</SimpleTab>

## Read more

- [Follower Read](/follower-read.md)
- [Troubleshoot Hotspot Issues](/troubleshoot-hot-spot-issues.md)
- [TiDB Dashboard - Key Visualizer Page](/dashboard/dashboard-key-visualizer.md)
