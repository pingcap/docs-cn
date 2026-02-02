---
title: TiDB 最佳实践
summary: 了解部署、配置和使用 TiDB 的最佳实践。
---

# TiDB 最佳实践

通过遵循 TiDB 在部署、配置和使用方面的最佳实践，你可以有效优化 TiDB 集群的性能、可靠性和可扩展性。本文档对 TiDB 的各类最佳实践进行了总体介绍，帮助你更高效地使用 TiDB。

## 使用概览

从使用 TiDB 的基本原则和通用建议入手，快速了解如何高效使用 TiDB。

| 最佳实践主题 | 说明 |
| ------------- | ---- |
| [TiDB 最佳实践](/best-practices/tidb-best-practices.md) | TiDB 使用最佳实践的整体概览。 |

## 库表设计

了解 TiDB 库表设计最佳实践，包括 DDL 管理、主键选择，以及索引的设计与维护，以兼顾系统的性能、可扩展性和可维护性。

| 最佳实践主题 | 说明 |
| ------------- | ---- |
| [DDL 最佳实践](/best-practices/ddl-introduction.md) | 在 TiDB 中管理数据定义语言 (DDL) 操作的最佳实践。 |
| [将 UUID 用作主键的最佳实践](/best-practices/uuid.md) | 使用 UUID（通用唯一标识符）作为主键时，高效存储和索引 UUID 的最佳实践。 |
| [多列索引优化最佳实践](/best-practices/multi-column-index-best-practices.md) | 通过合理设计和使用多列索引来提升 TiDB 查询性能的最佳实践。 |
| [管理索引和识别未使用索引的最佳实践](/best-practices/index-management-best-practices.md) | 管理和优化索引、识别并清理未使用索引，以提升 TiDB 性能的最佳实践。 |

## 集群部署

探索适用于不同场景的推荐部署模式，例如在公有云上部署和多数据中心部署，以确保高可用性和资源使用效率。

| 最佳实践主题 | 说明 |
| ------------- | ---- |
| [在公有云上部署 TiDB 的最佳实践](/best-practices/best-practices-on-public-cloud.md) | 在公有云环境中部署 TiDB 的最佳实践，以兼顾性能、成本、可靠性和可扩展性。 |
| [三节点混合部署的最佳实践](/best-practices/three-nodes-hybrid-deployment.md) | 在保证系统稳定性的前提下，实现高性价比、三节点混合部署的最佳实践。 |
| [在三数据中心下就近读取数据的最佳实践](/best-practices/three-dc-local-read.md) | 通过使用 Stale Read 减少跨数据中心访问延迟的最佳实践。 |

## 运维管理

掌握 TiDB 在生产环境中的运维最佳实践，包括流量路由、负载均衡和监控，以确保系统稳定性和可观测性。

| 最佳实践主题 | 说明 |
| ------------- | ---- |
| [HAProxy 最佳实践](/best-practices/haproxy-best-practices.md) | 配置 HAProxy 将应用流量分发到多个 TiDB 节点的最佳实践。 |
| [只读存储节点最佳实践](/best-practices/readonly-nodes.md) | 使用只读节点将分析型或重读负载与 OLTP 流量隔离的最佳实践。 |
| [Grafana 监控最佳实践](/best-practices/grafana-monitor-best-practices.md) | 通过关键指标和面板配置实现故障诊断的最佳实践。 |

## 性能调优

深入了解如何通过对 TiKV 和 PD 等 TiDB 核心组件进行调优，以及利用只读存储节点等特性，提升不同业务负载下的系统性能。

| 最佳实践主题 | 说明 |
| ------------- | ---- |
| [SaaS 多租户场景下处理百万张表的最佳实践](/best-practices/saas-best-practices.md) | TiDB 在 SaaS 多租户环境的最佳实践，尤其适用于单集群表数量超过百万级别的场景。 |
| [高并发写入场景最佳实践](/best-practices/high-concurrency-best-practices.md) | 在高并发写入场景下避免写入热点、优化 TiDB 性能的最佳实践。 |
| [海量 Region 集群调优最佳实践](/best-practices/massive-regions-best-practices.md) | 在管理百万级 Region 时，优化 TiKV 性能并降低心跳开销的最佳实践。 |
| [PD 调度策略最佳实践](/best-practices/pd-scheduling-best-practices.md) | 通过调整 PD 调度策略实现负载均衡并加快故障恢复的最佳实践。 |
