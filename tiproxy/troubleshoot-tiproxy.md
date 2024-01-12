---
title: Troubleshoot TiProxy
summary: Learn some common problems, causes, and solutions for TiProxy.
---

# Troubleshoot TiProxy

This document describes some common problems, causes, and solutions for TiProxy.

## Cannot connect to TiProxy

You can troubleshoot the issue by following these steps:

1. Check if the [connector version](/tiproxy/tiproxy-overview.md#supported-connectors) is supported. If the connector is not in the list, check if the connector supports [authentication plugins](https://dev.mysql.com/doc/refman/8.0/en/pluggable-authentication.html).
2. If the client reports `No available TiDB instances, please make sure TiDB is available`, check if there is a TiDB server and if the SQL port and HTTP status port of the TiDB server can be connected normally.
3. If the client reports `Require TLS enabled on TiProxy when require-backend-tls=true`, check if TiProxy is correctly configured with TLS certificates.
4. If the client reports `Verify TiDB capability failed, please upgrade TiDB`, check if the TiDB server version is v6.5.0 or later.
5. If the client reports `TiProxy fails to connect to TiDB, please make sure TiDB is available`, check if the TiProxy node can connect to the TiDB server.
6. If the client reports `Require TLS enabled on TiDB when require-backend-tls=true`, check if TiDB is correctly configured with TLS certificates.
7. If the client reports `TiProxy fails to connect to TiDB, please make sure TiDB proxy-protocol is set correctly`, check if [`proxy.proxy-protocol`](/tiproxy/tiproxy-configuration.md#proxy-protocol) is enabled on TiProxy and [`proxy-protocol`](/tidb-configuration-file.md#proxy-protocol) is not enabled on the TiDB server.
8. Check if TiProxy is configured with [`max-connections`](/tiproxy/tiproxy-configuration.md#max-connections) and if the number of connections on TiProxy exceeds the maximum connection limit.
9. Check the TiProxy log for error messages.

## TiProxy does not migrate connections

You can troubleshoot the issue by following these steps:

1. Whether the [TiProxy limitations](/tiproxy/tiproxy-overview.md#limitations) are not met. You can further confirm this by checking the TiProxy log.
2. Whether [`security.session-token-signing-cert`](/tidb-configuration-file.md#session-token-signing-cert-new-in-v640), [`security.session-token-signing-key`](/tidb-configuration-file.md#session-token-signing-key-new-in-v640), and [`graceful-wait-before-shutdown`](/tidb-configuration-file.md#graceful-wait-before-shutdown-new-in-v50) are correctly configured on TiDB.

## Unbalanced CPU usage on TiDB server

Check if the number of connections on TiDB server is balanced. If not, troubleshoot by following the [TiProxy does not migrate connections](#tiproxy-does-not-migrate-connections) section.

If the number of connections is balanced, it might be that some connections occupy a high CPU usage while other connections are relatively idle. TiProxy balances connections based on the number of connections on the TiDB server, not the actual load.

## Latency is significantly increased

You can troubleshoot the issue by following these steps:

1. Check the latency on TiProxy through Grafana. If the latency on TiProxy is not high, it means that the client load is high or the network latency between the client and TiProxy is high.
2. Check the latency on the TiDB server through Grafana. If the latency on the TiDB server is high, follow the steps in [Latency increases significantly](/tidb-troubleshooting-map.md#2-latency-increases-significantly) to troubleshoot.
3. Check the [network duration between TiProxy and TiDB server](/tiproxy/tiproxy-grafana.md#backend) through Grafana.
4. Check the CPU usage on TiProxy. If the CPU usage is over 90%, you need to scale out TiProxy.
