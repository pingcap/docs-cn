---
title: TiDB Operations Guide
category: operations
---

# TiDB Operations Guide

## Hardware and Software Requirements

  - [Hardware and Software Requirements](recommendation.md)

## Deploy

    - [Ansible Deployment (Recommended)](ansible-deployment.md)
    - [Docker Deployment](docker-deployment.md)
    - [Cross-Region Deployment](location-awareness.md)

## Configure

    - [Configuration Flags](configuration.md)

## Monitor

    - [Overview of the Monitoring Framework](monitor-overview.md)
    - [Key Metrics](dashboard-overview-info.md)
    - [Monitor a TiDB Cluster](monitoring-tidb.md)

## Scale

  - [Scale](horizontal-scale.md)

## Upgrade

  - [Upgrade](ansible-deployment.md#perform-rolling-update)

## Performance Tuning

    - [Performance Tuning for TiKV](tune-TiKV.md)

## Backup and Migrate

    - [Backup and Restore](backup-restore.md)
    + [Migrate Data from MySQL to TiDB](migration.md)
      - [Migrate All the Data](migration.md#using-the-mydumper--loader-tool-to-export-and-import-all-the-data)
      - [Migrate the Data Incrementally](migration.md#optional-using-the-syncer-tool-to-import-data-incrementally)

## Deploy TiDB Using the Binary

    - [Deploy TiDB Using the Binary](binary-deployment.md)