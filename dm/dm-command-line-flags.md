---
title: TiDB Data Migration Command-line Flags
summary: Learn about the command-line flags in DM.
---

# TiDB Data Migration Command-line Flags

This document introduces DM's command-line flags.

## DM-master

### `--advertise-addr`

- The external address of DM-master used to receive client requests
- The default value is `"{master-addr}"`
- Optional flag. It can be in the form of `"domain-name:port"`

### `--advertise-peer-urls`

- The external address for communication between DM-master nodes
- The default value is `"{peer-urls}"`
- Optional flag. It can be in the form of `"http(s)://domain-name:port"`

### `--config`

- The configuration file path of DM-master
- The default value is `""`
- Optional flag

### `--data-dir`

- The directory used to store data of DM-master
- The default value is `"default.{name}"`
- Optional flag

### `--initial-cluster`

- The `"{node name}={external address}"` list used to bootstrap DM-master cluster
- The default value is `"{name}={advertise-peer-urls}"`
- This flag needs to be specified if the `join` flag is not specified. A configuration example of a 3-node cluster is `"dm-master-1=http://172.16.15.11:8291,dm-master-2=http://172.16.15.12:8291,dm-master-3=http://172.16.15.13:8291"`

### `--join`

- The existing cluster's `advertise-addr` list when a DM-master node joins this cluster
- The default value is `""`
- This flag needs to be specified if the `initial-cluster` flag is not specified. Suppose a new node joins a cluster that has 2 nodes, a configuration example is `"172.16.15.11:8261,172.16.15.12:8261"`

### `--log-file`

- The output file name of the log
- The default value is `""`
- Optional flag

### `-L`

- The log level
- The default value is `"info"`
- Optional flag

### `--master-addr`

- The address on which DM-master listens to the client's requests
- The default value is `""`
- Required flag

### `--name`

- The name of a DM-master node
- The default value is `"dm-master-{hostname}"`
- Required flag

### `--peer-urls`

- The listening address for communications between DM-master nodes
- The default value is `"http://127.0.0.1:8291"`
- Required flag

## DM-worker

### `--advertise-addr`

- The external address of DM-worker used to receive client requests
- The default value is `"{worker-addr}"`
- Optional flag. It can be in the form of `"domain-name:port"`

### `--config`

- The configuration file path of DM-worker
- The default value is `""`
- Optional flag

### `--join`

- The `{advertise-addr}` list of DM-master nodes in a cluster when a DM-worker registers to this cluster
- The default value is `""`
- Required flag. A configuration example of 3-node (DM-master node) cluster is `"172.16.15.11:8261,172.16.15.12:8261,172.16.15.13:8261"`

### `--log-file`

- The output file name of the log
- The default value is `""`
- Optional flag

### `-L`

- The log level
- The default value is `"info"`
- Optional flag

### `--name`

- The name of a DM-worker node
- The default value is `"{advertise-addr}"`
- Required flag

### `--worker-addr`

- The address on which DM-worker listens to the client's requests
- The default value is `""`
- Required flag

## dmctl

### `--config`

- The configuration file path of dmctl
- The default value is `""`
- Optional flag

### `--master-addr`

- The `{advertise-addr}` of any DM-master node in the cluster to be connected by dmctl
- The default value is `""`
- It is a required flag when dmctl interacts with DM-master

### `--encrypt`

- Encrypts the plaintext database password into ciphertext
- The default value is `""`
- When this flag is specified, it is only used to encrypt the plaintext without interacting with the DM-master

### `--decrypt`

- Decrypts ciphertext encrypted with dmctl into plaintext
- The default value is `""`
- When this flag is specified, it is only used to decrypt the ciphertext without interacting with the DM-master
