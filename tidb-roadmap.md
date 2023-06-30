---
title: TiDB 路线图
summary: 了解 TiDB 未来的发展方向，包括新特性和改进提升。
---

# TiDB 路线图

TiDB 路线图展示了 TiDB 未来的发展方向，包括新特性和改进提升。通过 TiDB 路线图，你可以预先了解 TiDB 的未来规划，跟踪进度，了解关键里程碑，并对开发工作提出反馈。在开发过程中，路线图可能会根据用户需求和反馈进行调整。如果你有功能需求，或者想提高某个特性的优先级，请在 [GitHub](https://github.com/pingcap/tidb/issues) 上提交 issue。

## TiDB 重要特性规划

<table>
  <thead>
    <tr>
      <th>类别</th>
      <th>年中 LTS 版本</th>
      <th>年底 LTS 版本</th>
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
            <b>通用执行计划缓存</b><br />提升通用的读性能
          </li>
          <br />
          <li>
            <b>分区 Raft KV 存储引擎</b><br />提供更快的写入速度、更快的扩缩容操作，支持更大的集群
          </li>
          <br />
          <li>
            <b>TiFlash 性能提升</b><br />优化 TiFlash，例如实现延迟物化和运行时过滤器
          </li>
          <br />
          <li>
            <b>最快的在线 DDL 分布式执行框架</b><br />发布 DDL 分布式执行框架，支持快速完成在线 DDL 操作
          </li>
          <br />
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>PB 级别的稳定性</b><br />
            为海量数据提供可靠且稳定的性能
          </li>
          <br />
          <li>
            <b>TiFlash 计算和存储分离架构 （自动缩放）</b><br />
            实现弹性利用 HTAP 资源
          </li>
          <br />
          <li>
            <b>基于 S3 的 TiFlash 存储引擎</b>
            <br />降低共享存储成本
          </li>
          <br />
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>更强大的下一代存储引擎</b>
          </li>
          <br />
          <li>
            <b>事务大小无限制</b>
          </li>
          <br />
          <li>
            <b>支持多模型</b>
          </li>
          <br />
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
            <b>资源控制：资源组和后台任务支持流控和优先级调度</b><br />
            稳定高效地管理共享集群的负载和业务
          </li>
          <br />
          <li>
            <b>增强 TiCDC 和 PITR 的恢复目标</b>
            <br />增加业务连续性，将系统故障的影响最小化
          </li>
          <br />
          <li>
            <b>TiProxy</b>
            <br />在集群升级、扩缩容时，保持应用与数据库的连接，避免影响业务
          </li>
          <br />
          <li>
            <b>端到端的数据正确性检查</b>
            <br />防止由 TiCDC 导致的数据错误或数据损坏
          </li>
          <br />
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>多租户</b>
            <br />提供细粒度的资源控制和隔离，降低成本
          </li>
          <br />
          <li>
            <b>提升集群级和节点级的容错能力</b>
            <br />增强集群的弹性
          </li>
          <br />
          <li>
            <b>TiFlash 支持数据落盘</b>
            <br />避免 TiFlash 内存溢出
          </li>
          <br />
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>增强 TiDB 内存管理</b>
          </li>
          <br />
          <li>
            <b>全局表</b>
          </li>
          <br />
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
            <b>生产环境可用的 TTL (time-to-live) 数据生命周期控制</b>
            <br />通过自动清除过期数据，管理数据库大小，提升性能
          </li>
          <br />
          <li>
            <b>表级别的闪回</b>
            <br />支持通过 SQL 将单个表回退到指定的时间点
          </li>
          <br />
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>物化视图</b>
            <br />支持预计算以提高查询性能
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
            <b>Cascades 优化器</b>
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
            <br />通过多个节点分布式执行同步负载，大幅提高 TiCDC 吞吐量
          </li>
          <br />
          <li>
            <b
              >TiCDC 支持将 Amazon S3 和 Azure 对象存储作为生产级别的 sink</b
            >
            <br />增强生态系统，更好地处理大数据
          </li>
          <br />
          <li>
            <b>TiDB Operator 支持快速缩容</b>
            <br />从逐一缩容到批量快速缩容
          </li>
          <br />
          <li>
            <b>基于 SQL 的数据导入</b>
            <br />优化运维操作，对用户更友好
          </li>
          <br />
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>数据导入性能大幅提升</b>
            <br />预计提升 3~4 倍
          </li>
          <br />
          <li>
            <b>TiCDC 支持多个上游数据源</b>
            <br />支持从多个 TiDB 集群到 TiCDC (N:1)
          </li>
          <br />
          <li>
            <b>支持基于 SQL 的数据管理</b>
            <br />优化 TiCDC、DM 和 BR 等工具的数据管理方式
          </li>
          <br />
          <li>
            <b>升级期间自动暂停/恢复 DDL</b>
            <br />提供平滑的升级体验
          </li>
          <br />
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
        <br />增强数据安全与隐私
      </td>
      <td>
        <ul>
          <li>
            <b>JWT 身份验证</b>
            <br />提供安全和标准的身份验证方式
          </li>
          <br />
          <li>
            <b>LDAP 集成</b>
            <br />通过 TLS 在 LDAP 服务器进行身份验证
          </li>
          <br />
          <li>
            <b>增强审计日志</b>
            <br />
            审计日志中提供更多细节
          </li>
          <br />
        </ul>
      </td>
      <td>
        <ul>
          <li>
            <b>行级或列级的访问控制</b>
            <br />
            更细粒度的权限控制
          </li>
          <br />
          <li>
            <b>统一的 TLS CA/密钥轮换策略</b>
            <br />提升所有 TiDB 组件的安全性和运维效率
          </li>
          <br />
        </ul>
      </td>
      <td>
        <ul>
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
          <br />
        </ul>
      </td>
    </tr>
  </tbody>
</table>

上述表格中并未列出所有功能，当前规划可能会调整。不同的服务订阅版本中的功能可能有所不同。

## 近期已发布特性

- [TiDB 7.2.0 Release Notes](/releases/release-7.2.0.md)
- [TiDB 7.1.0 Release Notes](/releases/release-7.1.0.md)
- [TiDB 7.0.0 Release Notes](/releases/release-7.0.0.md)
- [TiDB 6.6.0 Release Notes](/releases/release-6.6.0.md)
- [TiDB 6.5.0 Release Notes](/releases/release-6.5.0.md)
