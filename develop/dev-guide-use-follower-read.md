---
title: Follower Read
summary: 了解如何使用 Follower Read 优化查询性能。
---

# Follower Read

本文档介绍如何使用 Follower Read 优化查询性能。

## 简介

TiDB 使用 [Region](/tidb-storage.md#region) 作为基本单位将数据分布到集群中的所有节点。一个 Region 可以有多个副本，这些副本分为一个 leader 和多个 follower。当 leader 上的数据发生变化时，TiDB 会同步更新数据到 follower。

默认情况下，TiDB 只在同一个 Region 的 leader 上读写数据。当 Region 出现读热点时，Region leader 可能成为整个系统的读取瓶颈。在这种情况下，启用 Follower Read 功能可以通过在多个 follower 之间平衡负载来显著减少 leader 的负载并提高整个系统的吞吐量。

## 使用场景

### 减少读热点

<CustomContent platform="tidb">

你可以在 [TiDB Dashboard 的 Key Visualizer 页面](/dashboard/dashboard-key-visualizer.md)上直观地分析你的应用程序是否存在热点 Region。你可以通过选择"指标选择框"为 `Read (bytes)` 或 `Read (keys)` 来检查是否出现读热点。

有关处理热点的更多信息，请参阅 [TiDB 热点问题处理](/troubleshoot-hot-spot-issues.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

你可以在 [TiDB Cloud 的 Key Visualizer 页面](/tidb-cloud/tune-performance.md#key-visualizer)上直观地分析你的应用程序是否存在热点 Region。你可以通过选择"指标选择框"为 `Read (bytes)` 或 `Read (keys)` 来检查是否出现读热点。

有关处理热点的更多信息，请参阅 [TiDB 热点问题处理](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues)。

</CustomContent>

如果读热点不可避免或更改成本很高，你可以尝试使用 Follower Read 功能，将读取请求更好地负载均衡到 follower Region。

### 减少地理分布部署的延迟

如果你的 TiDB 集群跨区域或数据中心部署，Region 的不同副本分布在不同的区域或数据中心。在这种情况下，你可以将 Follower Read 配置为 `closest-adaptive` 或 `closest-replicas`，允许 TiDB 优先从当前数据中心读取，这可以显著减少读取操作的延迟和流量开销。有关实现细节，请参阅 [Follower Read](/follower-read.md)。

## 启用 Follower Read

<SimpleTab groupId="language">
<div label="SQL" value="sql">

要启用 Follower Read，将变量 `tidb_replica_read`（默认值为 `leader`）设置为 `follower`、`leader-and-follower`、`prefer-leader`、`closest-replicas` 或 `closest-adaptive`：

```sql
SET [GLOBAL] tidb_replica_read = 'follower';
```

有关此变量的更多详细信息，请参阅 [Follower Read 使用方法](/follower-read.md#usage)。

</div>
<div label="Java" value="java">

在 Java 中，要启用 Follower Read，定义一个 `FollowerReadHelper` 类。

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

从 Follower 节点读取数据时，使用 `setSessionReplicaRead(conn, FollowReadMode.LEADER_AND_FOLLOWER)` 方法启用 Follower Read 功能，可以在当前会话中平衡 Leader 节点和 Follower 节点之间的负载。当连接断开时，它将恢复到原始模式。

```java
public static class AuthorDAO {

    // 省略实例变量的初始化...

    public void getAuthorsByFollowerRead() throws SQLException {
        try (Connection conn = ds.getConnection()) {
            // 启用 follower read 功能。
            FollowerReadHelper.setSessionReplicaRead(conn, FollowReadMode.LEADER_AND_FOLLOWER);

            // 读取作者列表 100000 次。
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

## 阅读更多

- [Follower Read](/follower-read.md)

<CustomContent platform="tidb">

- [热点问题处理](/troubleshoot-hot-spot-issues.md)
- [TiDB Dashboard - Key Visualizer 页面](/dashboard/dashboard-key-visualizer.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

- [热点问题处理](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues)
- [TiDB Cloud Key Visualizer 页面](/tidb-cloud/tune-performance.md#key-visualizer)

</CustomContent>

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
