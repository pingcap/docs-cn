---
title: 创建数据源
summary: 了解如何为 DM 创建数据源。
---

# 创建数据源

> **注意：**
>
> 在创建数据源之前，你需要先[使用 TiUP 部署 DM 集群](/dm/deploy-a-dm-cluster-using-tiup.md)。

本文档介绍如何为 TiDB Data Migration (DM) 的数据迁移任务创建数据源。

数据源包含了访问迁移任务上游所需的信息。数据迁移任务需要引用对应的数据源来获取访问配置信息。因此，在创建数据迁移任务之前，需要先创建任务的数据源。详细的数据源管理命令请参考[管理上游数据源](/dm/dm-manage-source.md)。

## 第一步：配置数据源

1. （可选）加密数据源密码

    在 DM 的配置文件中，推荐使用经 dmctl 加密后的密文密码。按照下面的示例可以获得数据源的密文密码，用于下一步编写数据源配置文件。

    {{< copyable "shell-regular" >}}

    ```bash
    tiup dmctl encrypt 'abc!@#123'
    ```

    ```
    MKxn0Qo3m3XOyjCnhEMtsUCm83EhGQDZ/T4=
    ```

2. 编写数据源配置文件

    每个数据源需要一个单独的配置文件来创建数据源。按照下面示例创建 ID 为 "mysql-01" 的数据源，创建数据源配置文件 `./source-mysql-01.yaml`：

    ```yaml
    source-id: "mysql-01"    # 数据源 ID，在数据迁移任务配置和 dmctl 命令行中引用该 source-id 可以关联到对应的数据源
    
    from:
      host: "127.0.0.1"
      port: 3306
      user: "root"
      password: "MKxn0Qo3m3XOyjCnhEMtsUCm83EhGQDZ/T4=" # 推荐使用 dmctl 对上游数据源的用户密码加密之后的密码
      security:                                        # 上游数据源 TLS 相关配置。如果没有需要则可以删除
        ssl-ca: "/path/to/ca.pem"
        ssl-cert: "/path/to/cert.pem"
        ssl-key: "/path/to/key.pem"
    ```

## 第二步：创建数据源

使用如下命令创建数据源：

{{< copyable "shell-regular" >}}

```bash
tiup dmctl --master-addr <master-addr> operate-source create ./source-mysql-01.yaml
```

数据源配置文件的其他配置参考[数据源配置文件介绍](/dm/dm-source-configuration-file.md)。

命令返回结果如下：

{{< copyable "" >}}

```
{
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "",
            "source": "mysql-01",
            "worker": "dm-worker-1"
        }
    ]
}
```

## 第三步：查询创建的数据源

创建数据源后，可以使用如下命令查看创建的数据源：

- 如果知道数据源的 `source-id`，可以通过 `dmctl config source <source-id>` 命令直接查看数据源配置：

    {{< copyable "shell-regular" >}}

    ```bash
    tiup dmctl --master-addr <master-addr> config source mysql-01
    ```
    
    ```
    {
      "result": true,
      "msg": "",
      "cfg": "enable-gtid: false
        flavor: mysql
        source-id: mysql-01
        from:
          host: 127.0.0.1
          port: 3306
          user: root
          password: '******'
    }
    ```

- 如果不知道数据源的 `source-id`，可以先通过 `dmctl operate-source show` 命令查看源数据库列表，从中可以找到对应的数据源。

    {{< copyable "shell-regular" >}}

    ```bash
    tiup dmctl --master-addr <master-addr> operate-source show
    ```

    ```
    {
        "result": true,
        "msg": "",
        "sources": [
            {
                "result": true,
                "msg": "source is added but there is no free worker to bound",
                "source": "mysql-02",
                "worker": ""
            },
            {
                "result": true,
                "msg": "",
                "source": "mysql-01",
                "worker": "dm-worker-1"
            }
        ]
    }
    ```
