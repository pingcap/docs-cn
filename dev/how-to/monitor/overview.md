---
title: TiDB Monitoring Framework Overview
summary: Use Prometheus and Grafana to build the TiDB monitoring framework.
category: how-to
aliases: ['/docs/op-guide/monitor-overview/']
---

# TiDB Monitoring Framework Overview

The TiDB monitoring framework adopts two open source projects: Prometheus and Grafana. TiDB uses [Prometheus](https://prometheus.io) to store the monitoring and performance metrics and [Grafana](https://grafana.com/grafana) to visualize these metrics.

## About Prometheus in TiDB

As a time series database, Prometheus has a multi-dimensional data model and flexible query language. As one of the most popular open source projects, many companies and organizations have adopted Prometheus, and the project has a very active community. PingCAP is one of the active developers and adopters of Prometheus for monitoring and alerting in TiDB, TiKV and PD.

Prometheus consists of multiple components. Currently, TiDB uses the following of them:

- The Prometheus Server to scrape and store time series data
- The client libraries to customize necessary metrics in the application
- An Alertmanager for the alerting mechanism

The diagram is as follows:

![diagram](/media/prometheus-in-tidb.png)

## About Grafana in TiDB

Grafana is an open source project for analyzing and visualizing metrics. TiDB uses Grafana to display the performance metrics as follows:

![screenshot](/media/grafana-screenshot.png)
