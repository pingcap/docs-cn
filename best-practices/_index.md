---
title: TiDB 最佳实践
summary: 了解部署、配置和使用 TiDB 的最佳实践。
---

# TiDB 最佳实践

By following best practices for deploying, configuring, and using TiDB, you can optimize the performance, reliability, and scalability of your TiDB deployments. This document provides an overview of the best practices for using TiDB.

## 使用概览

Get started with basic principles and general recommendations for using TiDB effectively.

| Best practice topic | Description |
| ------------------- | ----------- |
| [Use TiDB](/best-practices/tidb-best-practices.md) | A comprehensive overview of best practices for using TiDB. |

## 库表设计

Learn best practices for designing schemas in TiDB, including managing DDL operations, choosing primary keys, and designing and maintaining indexes to balance performance, scalability, and maintainability.

| Best practice topic | Description |
| ------------------- | ----------- |
| [Manage DDL](/best-practices/ddl-introduction.md) | Best practices for managing Data Definition Language (DDL) operations in TiDB. |
| [Use UUIDs as Primary Keys](/best-practices/uuid.md) | Best practices for storing and indexing UUIDs (Universally Unique Identifiers) efficiently when using UUIDs as primary keys. |
| [Optimize Multi-Column Indexes](/best-practices/multi-column-index-best-practices.md) | Best practices for designing and using multi-column indexes in TiDB to improve query performance. |
| [Manage Indexes and Identify Unused Indexes](/best-practices/index-management-best-practices.md) | Best practices for managing and optimizing indexes, identifying and removing unused indexes in TiDB to optimize performance. |

## 集群部署

Explore recommended deployment patterns for different scenarios, such as small clusters and multi–data center setups, to ensure high availability and efficient resource usage.

| Best practice topic | Description |
| ------------------- | ----------- |
| [Deploy TiDB on Public Cloud](/best-practices/best-practices-on-public-cloud.md) | Best practices for deploying TiDB on public cloud to maximize performance, cost efficiency, reliability, and scalability of your TiDB deployment. |
| [Three-Node Hybrid Deployment](/best-practices/three-nodes-hybrid-deployment.md) | Best practices for a cost-effective, hybrid three-node deployment while maintaining stability. |
| [Local Reads in Three-Data-Center Deployments](/best-practices/three-dc-local-read.md) | Best practices for reducing cross-center latency by using Stale Read. |

## 运维管理

Find operational best practices for running TiDB in production, such as traffic routing, load balancing, and monitoring, to help you maintain system stability and observability.

| Best practice topic | Description |
| ------------------- | ----------- |
| [Use HAProxy for Load Balancing](/best-practices/haproxy-best-practices.md) | Best practices for configuring HAProxy to distribute application traffic across multiple TiDB nodes. |
| [Use Read-Only Storage Nodes](/best-practices/readonly-nodes.md) | Best practices for using read-only nodes to isolate analytical or heavy read workloads from OLTP traffic. |
| [Monitor TiDB Using Grafana](/best-practices/grafana-monitor-best-practices.md) | Best practices for using key metrics and dashboard configurations for proactive troubleshooting. |

## 性能调优

| Best practice topic | Description |
| ------------------- | ----------- |
| [Handle Millions of Tables in SaaS Multi-Tenant Scenarios](/best-practices/saas-best-practices.md) | Best practices for managing millions of tables and ensuring tenant isolation in SaaS applications. |
| [Handle High-Concurrency Writes](/best-practices/high-concurrency-best-practices.md) | Best practices for handling high-concurrency write-heavy workloads in TiDB to avoid write hotspots and optimize performance. |
| [Tune TiKV Performance with Massive Regions](/best-practices/massive-regions-best-practices.md) | Best practices for optimizing TiKV performance and reducing heartbeat overhead when managing millions of Regions. |
| [Tune PD Scheduling](/best-practices/pd-scheduling-best-practices.md) | Best practices for adjusting PD policies to balance load and speed up failure recovery. |
