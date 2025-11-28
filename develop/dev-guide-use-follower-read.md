---
title: Follower Read
summary: 使用 Follower Read 在特定情况下加速查询。
aliases: ['/zh/tidb/dev/use-follower-read']
---

# Follower Read

本章将介绍使用 Follower Read 在特定情况下加速查询的方法。

## 简介

在 TiDB 当中，数据是以 [Region](/tidb-storage.md#region) 为单位，分散在集群中所有的节点上进行存储的。一个 Region 可以存在多个副本，副本又分为一个 leader 和多个 follower。当 leader 上的数据发生变化时，TiDB 会将数据同步更新到 follower。

默认情况下，TiDB 只会在同一个 Region 的 leader 上读写数据。当系统中存在读取热点 Region 导致 leader 资源紧张成为整个系统读取瓶颈时，启用 Follower Read 功能可明显降低 leader 的负担，并且通过在多个 follower 之间均衡负载，显著地提升整体系统的吞吐能力。

## 何时使用

### 优化读热点

你可以在 [TiDB Dashboard 流量可视化页面](/dashboard/dashboard-key-visualizer.md)当中通过可视化的方法分析你的应用程序是否存在热点 Region。你可以通过将「指标选择框」选择到 `Read (bytes)` 或 `Read (keys)` 查看是否存在读取热点 Region。

如果发现确实存在热点问题，你可以通过阅读 [TiDB 热点问题处理](/troubleshoot-hot-spot-issues.md)章节进行逐一排查，以便从应用程序层面上避免热点的产生。

如果读取热点的确无法避免或者改动的成本很大，你可以尝试通过 Follower Read 功能将读取请求更好的负载均衡到 follower region。

### 优化跨数据中心部署的延迟

如果 TiDB 集群是跨地区或跨数据中心部署的，一个 Region 的不同副本分布在不同的地区或数据中心，此时可以通过配置 Follower Read 为 `closest-adaptive` 或 `closest-replicas` 让 TiDB 优先从当前的数据中心执行读操作，这样可以大幅降低读操作的延迟和流量开销。具体原理可参考 [Follower Read](/follower-read.md)。

## 开启 Follower Read

<SimpleTab>
<div label="SQL">

在 SQL 中，你可以将变量 `tidb_replica_read` 的值（默认为 `leader`）设置为 `follower`、`leader-and-follower`、`prefer-leader`、`closest-replicas` 或 `closest-adaptive` 开启 TiDB 的 Follower Read 功能：

```sql
SET [GLOBAL] tidb_replica_read = 'follower';
```

你可以通过 [Follower Read 使用方式](/follower-read.md#使用方式)了解该变量的更多细节。

</div>
<div label="Java">

在 Java 语言当中，可以定义一个 `FollowerReadHelper` 类用于开启 Follower Read 功能：

```java
public enum FollowReadMode {
    LEADER("leader"),
    FOLLOWER("follower"),
    LEADER_AND_FOLLOWER("leader-and-follower"),
    CLOSEST_REPLICA("closest-replica"),
    CLOSEST_ADAPTIVE("closest-adaptive"),
    PREFER_LEADER("prefer-leader");

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

在需要使用从 Follower 节点读取数据时，通过 `setSessionReplicaRead(conn, FollowReadMode.LEADER_AND_FOLLOWER)` 方法在当前 Session 开启能够在 Leader 节点和 Follower 节点进行负载均衡的 Follower Read 功能，当连接断开时，会恢复到原来的模式。

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

## 扩展阅读

- [Follower Read](/follower-read.md)
- [TiDB 热点问题处理](/troubleshoot-hot-spot-issues.md)
- [TiDB Dashboard 流量可视化页面](/dashboard/dashboard-key-visualizer.md)
