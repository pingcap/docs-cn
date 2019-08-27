---
title: Kubernetes 上的集群初始化配置
category: how-to
---

# Kubernetes 上的集群初始化配置

本文介绍如何对 Kubernetes 上的集群进行初始化配置完成初始化账号和密码设置，以及批量自动执行 SQL 语句对数据库进行初始化。

> **注意：**
>
> 以下功能只在第一次创建集群时有作用，集群创建之后再设置或修改不会生效。

## 设置初始化账号和密码

集群创建时默认会创建 `root` 账号，但是密码为空，这会带来一些安全性问题。可以通过如下步骤为 `root` 账号设置初始密码：

1. 创建 `Secret`

    在部署集群前通过下面命令创建 [Secret](https://kubernetes.io/docs/concepts/configuration/secret/) 指定 root 账号密码：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl create secret generic tidb-secret --from-literal=root=<root-password> --namespace=<namespace>
    ```

    如果希望能自动创建其它用户，可以在上面命令里面再加上其他用户的 username 和 password，例如：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl create secret generic tidb-secret --from-literal=root=<root-password> --from-literal=developer=<developer-passowrd> --namespace=<namespace>
    ```

    该命令会创建 `root` 和 `developer` 两个用户的密码，存到 `tidb-secret` 的 Secret 里面。并且创建的普通用户`developer`默认只有`USAGE`权限，其他权限请在`tidb.initSql`中设置。

2. 设置允许访问 TiDB 的主机

    在部署集群前可以通过 `tidb.permitHost` 配置项来设置允许访问 TiDB 的主机 **host_name**。如果不设置，则允许所有主机访问。详情请参考 [Mysql GRANT host name](https://dev.mysql.com/doc/refman/5.7/en/grant.html)。

    ```
    tidb:
      passwordSecretName: tidb-secret
      permitHost: <mysql-client-host-name>
    ```

3. 部署集群

    创建 Secret 之后，通过下面命令部署集群：

    {{< copyable "shell-regular" >}}

    ```shell
    helm install pingcap/tidb-cluster --name=<release-name> --namespace=<namespace> --version=<chart-version> --set tidb.passwordSecretName=tidb-secret
    ```

    以上命令指定 `tidb.passwordSecretName` 之后，创建的集群会自动创建一个初始化的 Job，该 Job 在集群创建过程中会尝试利用提供的 secret 给 root 账号创建初始密码，并且创建其它账号和密码，如果指定了的话。注意由于 Job 创建时 TiDB 集群的 Pod 还没完全创建，所以可能会失败几次，初始化完成后 Pod 状态会变成 Completed。之后通过 MySQL 客户端登录时需要指定这里设置的密码。

## 批量执行初始化 SQL 语句

集群在初始化过程还可以自动执行 `tidb.initSql` 中的 SQL 语句用于初始化，该功能可以用于默认给集群创建一些 database 或者 table，并且执行一些用户权限管理类的操作。例如如下设置会在集群创建完成后自动创建名为 `app` 的 database，并且赋予 `developer` 账号对 `app` 的所有管理权限：

{{< copyable "yaml" >}}

```yaml
tidb:
  passwordSecretName: tidb-secret
  initSql: |-
    CREATE DATABASE app;
    GRANT ALL PRIVILEGES ON app.* TO 'developer'@'%';
```

将上述内容保存到 `values.yaml` 文件，然后执行下面命令部署集群：

{{< copyable "shell-regular" >}}

```bash
helm install pingcap/tidb-cluster -f values.yaml --name=<release-name> --namespace=<namespace> --version=<chart-version>
```

> **注意：**
>
> 目前没有对 initSql 做校验，尽管也可以在 initSql 里面创建账户和设置密码，但这种方式会将密码以明文形式存到 initializer Job 对象上，不建议这么做。
