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
             <b>分布式并行执行框架</b><br />
            TiDB v7.2.0 引入了用于后台任务（如 DDL 和 analyze）的分布式并行执行框架，为实现这些任务在计算节点间并行化提供了基础。v7.4.0 为分布式 reorg 任务（如 DDL 和 import）引入了全局排序，大幅减少了存储中额外资源的消耗。用户可以使用外部存储简化操作并节省成本
          </li>
          <br />
          <br />
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>增强执行计划缓存的性能和通用性</b><br />
          </li>
          <br />
          <li>
            <b>通过分布式并行执行框架实现动态节点扩缩容</b><br />
            动态调整节点分配，以满足后台任务的资源成本，同时保持稳定性和性能预期
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>移除事务大小的限制</b>
          </li>
          <li>
            <b>联邦查询</b>
            TiDB 查询 planner 支持 HTAP 场景中多个存储引擎
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
          <br />
          <li>
            <b>管控 Runaway Query</b><br />
              一种由运维人员控制的方式，显著提升了出现非预期的高成本查询时的性能稳定性
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>解耦 Placement Driver (PD)</b>
            <br />提升集群的可扩展性和弹性
          </li>
          <br />
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>多租户</b>
            <br />在资源管控基础上实现资源隔离
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
            <b>TiCDC 与数据仓库或数据湖系统的集成</b>
            <br />
          </li>
          <br />
          <li>
            <b>TiDB 节点标签</b>
            <br />将 DDL 操作分配到现有的或新添加的 TiDB 节点，以便将 DDL 任务与在线流量使用的计算资源隔离
          </li>
          <br />
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>SQL 执行计划管理</b>
            <br />控制 SQL 执行计划回归的机制
          </li>
          <br />
          <li>
            <b>Index Advisor</b>
            <br />基于工作负载、统计信息和执行计划，向用户提供索引建议
          </li>
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>物化视图</b>
            <br />存储预计算结果作为持久化数据视图，以提升查询性能
          </li>
          <br />
          <li>
            <b>支持迁移异构数据库</b>
          </li>
          <br />
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
          <li>
            <b>支持 AWS FIPS</b>
            <br />实现 FedRAMP 合规
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

- [TiDB 7.5.0 Release Notes](/releases/release-7.5.0.md)
- [TiDB 7.4.0 Release Notes](/releases/release-7.4.0.md)
- [TiDB 7.3.0 Release Notes](/releases/release-7.3.0.md)
- [TiDB 7.2.0 Release Notes](/releases/release-7.2.0.md)
- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)
- [TiDB 7.0.0 Release Notes](/releases/release-7.0.0.md)
- [TiDB 6.6.0 Release Notes](/releases/release-6.6.0.md)
- [TiDB 6.5.0 Release Notes](/releases/release-6.5.0.md)
