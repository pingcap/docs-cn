---
title: Initialize a TiDB Cluster in Kubernetes
summary: Learn how to initialize a TiDB cluster in K8s.
category: how-to
---

# Initialize a TiDB Cluster in Kubernetes

This document describes how to initialize a TiDB cluster in Kubernetes (K8s), specifically, how to configure the initial account and password and how to initialize the database by executing SQL statements automatically in batch.

> **Note:**
>
> The following steps only apply when you create a cluster for the first time. Further configuration or modification after the initial cluster creation is not valid.

## Set initial account and password

When a cluster is created, a default account `root` is created with no password. This might cause security issues. You can set a password for the `root` account in the following steps:

1. Create a `secret` object.

    Before creating a cluster, create a [`secret`](https://kubernetes.io/docs/concepts/configuration/secret/) to specify the password for `root`:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl create secret generic tidb-secret --from-literal=root=<root-password> --namespace=<namespace>
    ```

    If you also want to create users automatically, append the desired user name and the password, for example:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl create secret generic tidb-secret --from-literal=root=<root-password> --from-literal=developer=<developer-passowrd> --namespace=<namespace>
    ```

    This command creates users `root` and `developer` with their passwords, which are saved in the `tidb-secret` object.

2. Deploy the cluster.

    After creating the `secret`, deploy the cluster using the following command:

    {{< copyable "shell-regular" >}}

    ```shell
    helm install pingcap/tidb-cluster --name=<release-name> --namespace=<namespace> --version=<chart_version> --set tidb.passwordSecretName=tidb-secret
    ```

    After specifying `tidb.passwordSecretName`, the above command sets up a cluster with an initialization job created automatically. Using the available `secret`, this job creates the password for the `root` account, and creates other user accounts and passwords if specified. The password specified here is required when you login to the MySQL client.

    > **Note:**
    >
    > When the initialization job is created, the Pod for the TiDB cluster has not been created fully. There might be a few errors before initialization completes and Pod state becomes Completed.

## Initialize SQL statements in batch

You can also execute the SQL statements in batch in `tidb.initSql` for initialization. This function by default creates some databases or tables for the cluster and performs user privilege management operations. For example, the following configuration automatically creates a database named `app` after the cluster creation, and grants the `developer` account full management privileges on `app`.

{{< copyable "yaml" >}}

```yaml
tidb:
  passwordSecretName: tidb-secret
  initSql: |-
    CREATE DATABASE app;
    GRANT ALL PRIVILEGES ON app.* TO 'developer'@'%';
```

Save the above configuration to the `values.yaml` file and run the following command to deploy the cluster:

{{< copyable "shell-regular" >}}

```bash
helm install pingcap/tidb-cluster -f values.yaml --name=<release-name> --namespace=<namespace> --version=<chart_version>
```

> **Note:**
>
> Currently no verification has been implemented for `initSql`. You can create accounts and set passwords in `initSql`, but it is not recommended because passwords created this way are saved as plaintext in the initializer job object.
