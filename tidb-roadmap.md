---
title: TiDB 路线图
summary: 了解 TiDB 未来的发展方向，包括新特性和改进提升。
---

# TiDB 路线图

TiDB 路线图展示了 TiDB 未来的计划。随着我们发布长期稳定版本 (LTS)，这个路线图将会持续更新。通过路线图，你可以预先了解 TiDB 的未来规划，以便你关注进度，了解关键里程碑，并对开发工作提出反馈。

在开发过程中，路线图可能会根据用户需求和反馈进行调整。越靠右侧的特性，其优先级越低。如果你有功能需求，或者想提高某个特性的优先级，请在 [GitHub](https://github.com/pingcap/tidb/issues) 上提交 issue。

## TiDB 重要特性规划

<table>
  <thead>
    <tr>
      <th>类别</th>
      <th>2023 年底 LTS 版本</th>
      <th>2024 年中 LTS 版本</th>
      <th>未来版本</th>
    </tr>
  </thead>
  <tbody valign="top">
    <tr>
      <td>
        <b>可扩展性与性能</b><br />增强性能
      </td>
      <td>
        <ul>
          <li>
            <b>Partitioned Raft KV 存储引擎 GA</b><br />支持 PB 级别的集群，提升写入速度、扩缩容操作速度，提升数据整理的稳定性
          </li>
          <br />
          <li>
            <b>增强副本读取功能</b><br />降低 TiKV 跨可用区的数据传输成本
          </li>
          <br />
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>引入性能优化框架，适用于所有相关后台任务，如 DDL、TTL 和集群分析操作</b><br />
            性能优化框架将这些后台任务的工作负载分散到整个集群中，从而提升性能，并减少各个节点上的资源消耗。该框架已经应用于 <code>ADD INDEX</code> 操作。
          </li>
          <br />
          <li>
            <b>TiFlash 存算分离架构、基于 S3 的 TiFlash 存储引擎等功能 GA</b><br />
            实现更具成本效益的弹性 HTAP
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>移除事务大小的限制</b>
          </li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>
        <b>稳定性与高可用</b>
        <br />提升可靠性
      </td>
      <td>
        <ul>
          <li>
            <b>后台任务支持资源管控</b><br />
            控制后台任务（如数据导入、DDL、TTL、自动分析、数据整理等操作）对前台流量的影响
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>多租户</b>
            <br />基于资源管控实现资源隔离
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>增强 TiDB 内存管理</b>
          </li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>
        <b>SQL 功能</b>
        <br />增强 SQL 功能和兼容性
      </td>
      <td>
        <ul>
          <li>
            <b>兼容 MySQL 8.0</b>
          </li>
          <br />
          <li>
            <b>为数据导入、备份恢复、PITR 提供统一的 SQL 接口</b>
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>优化器支持 Cascades 框架</b>
            <br />改进查询优化框架，让优化器更具可扩展性，适应未来的需求
          </li>
          <br />
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>联邦查询</b>
          </li>
          <br />
          <li>
            <b>全文搜索和 GIS 支持</b>
          </li>
          <br />
          <li>
            <b>用户自定义函数</b>
          </li>
          <br />
        </ul>
      </td>
    </tr>
    <tr>
      <td>
        <b>数据库管理与可观测性</b>
        <br />增强数据库可管理性及其生态系统
      </td>
      <td>
        <ul>
          <li>
            <b>TiCDC 支持分布式同步单表数据</b>
            <br />大幅提高 TiDB 到 TiDB 的数据吞吐量
          </li>
          <br />
          <li>
            <b>升级期间自动暂停/恢复 DDL</b>
            <br />提供平滑的升级体验
          </li>
          <br />
          <li>
            <b>TiCDC 原生集成大数据生态</b>
            <br />例如集成 Snowflake 和 Iceburg
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>TiCDC 支持多个上游数据源</b>
            <br />支持从多个 TiDB 集群到 TiCDC (N:1)
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>AI 索引</b>
          </li>
          <br />
          <li>
            <b>支持迁移异构数据库</b>
          </li>
          <br />
          <li>
            <b>使用 AI 赋能 SQL 性能优化</b>
          </li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>
        <b>安全</b>
        <br />增强数据安全与隐私保护
      </td>
      <td>
        <ul>
          <li>
            <b>通过 Azure Key Vault 进行密钥管理</b>
            <br />由 Azure Key Vault 管理的静态加密
          </li>
          <br />
          <li>
            <b>列级访问控制</b>
            <br />允许针对特定列来授予或限制访问权限
          </li>
          <br />
          <li>
            <b>数据库级别的加密</b>
            <br />支持配置数据库级别的静态加密
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>AWS IAM 身份验证</b>
            <br />将 TiDB 作为 AWS 第三方 ARN，用于 AWS IAM 访问
          </li>
          <br />
          <li>
            <b>统一的 TLS CA/密钥轮换策略</b>
            <br />统一管理所有 TiDB 组件的证书
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>基于标签的访问控制</b>
            <br />通过配置标签来授予访问权限
          </li>
          <li>
            <b>增强客户端加密</b>
          </li>
          <br />
          <li>
            <b>增强数据脱敏</b>
          </li>
          <br />
          <li>
            <b>增强数据生命周期管理</b>
          </li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>

上述表格中并未列出所有功能，当前规划可能会调整。不同的服务订阅版本中的功能可能有所不同。

## 已发布特性

以下是历史版本路线图中已交付的部分功能。更多详细信息，请参阅 [v7.1.0 Release Notes](/releases/release-7.1.0.md)。

- 多租户框架的基础：资源组的资源管控配额和调度
- TiCDC 支持对象存储 sink，包括 Amazon S3 和 Azure Blob Storage (GA)
- 最快的在线添加索引 `ADD INDEX` 操作 (GA)
- TiFlash 延迟物化 (GA)
- TiFlash 支持数据落盘 (GA)
- LDAP 身份认证
- SQL 审计日志增强（仅企业版可用）
- Partitioned Raft KV 存储引擎（实验特性）
- 通用的会话级别执行计划缓存（实验特性）
- TiCDC 支持以 Kafka 为下游的分布式表级别数据同步（实验特性）

## 已发布版本

- [TiDB 7.2.0 Release Notes](/releases/release-7.2.0.md)
- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)
- [TiDB 7.0.0 Release Notes](/releases/release-7.0.0.md)
- [TiDB 6.6.0 Release Notes](/releases/release-6.6.0.md)
- [TiDB 6.5.0 Release Notes](/releases/release-6.5.0.md)
