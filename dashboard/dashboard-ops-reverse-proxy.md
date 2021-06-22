---
title: 通过反向代理使用 TiDB Dashboard
---

# 通过反向代理使用 TiDB Dashboard

你可以使用反向代理将 TiDB Dashboard 服务安全从内部网络提供给外部网络。

## 操作步骤

### 第 1 步：获取实际 TiDB Dashboard 地址

当集群中部署有多个 PD 实例时，其中仅有一个 PD 实例会真正运行 TiDB Dashboard，因此需要确保反向代理的上游 (Upstream) 指向了正确的地址。关于该机制的详情，可参阅 [TiDB Dashboard 多 PD 实例部署](/dashboard/dashboard-ops-deploy.md#多-pd-实例部署) 章节。

使用 TiUP 部署工具时，操作命令如下（将 `CLUSTER_NAME` 替换为集群名称）：

```shell
tiup cluster display CLUSTER_NAME --dashboard
```

输出即为实际 TiDB Dashboard 地址。样例如下：

```
http://192.168.0.123:2379/dashboard/
```

> **注意：**
>
> 该功能在 TiUP Cluster v1.0.3 或更高版本部署工具中提供。
>
> <details>
> <summary>升级 TiUP Cluster 步骤</summary>
>
> ```shell
> tiup update --self
> tiup update cluster --force
> ```
>
> </details>

### 第 2 步：配置反向代理

<details>
<summary>使用 HAProxy 反向代理</summary>

[HAProxy](https://www.haproxy.org/) 作为反向代理时，方法如下：

1. 以在 8033 端口反向代理 TiDB Dashboard 为例，在 HAProxy 配置文件中，新增如下配置：

   ```haproxy
   frontend tidb_dashboard_front
     bind *:8033
     use_backend tidb_dashboard_back if { path /dashboard } or { path_beg /dashboard/ }

   backend tidb_dashboard_back
     mode http
     server tidb_dashboard 192.168.0.123:2379
   ```

   其中 `192.168.0.123:2379` 需替换为[第 1 步：获取实际 TiDB Dashboard 地址](#第-1-步获取实际-tidb-dashboard-地址)中取得的 TiDB Dashboard 实际地址中的 IP 及端口部分。

   > **警告：**
   >
   > 请务必保留 `use_backend` 指令中的 `if` 部分，确保只有该路径下的服务会被反向代理，否则将引入安全风险。参见[提高 TiDB Dashboard 安全性](/dashboard/dashboard-ops-security.md)。

2. 重启 HAProxy，以使配置生效。

3. 测试反向代理是否生效：访问 HAProxy 所在机器的 8033 端口下 `/dashboard/` 地址，如 <http://example.com:8033/dashboard/> ，即可访问 TiDB Dashboard。

</details>

<details>
<summary>使用 NGINX 反向代理</summary>

[NGINX](https://nginx.org/) 作为反向代理时，方法如下：

1. 以在 8033 端口反向代理 TiDB Dashboard 为例，在 NGINX 配置文件中，新增如下配置：

   ```nginx
   server {
     listen 8033;
     location /dashboard/ {
       proxy_pass http://192.168.0.123:2379/dashboard/;
     }
   }
   ```

   其中 `http://192.168.0.123:2379/dashboard/` 需替换为[第 1 步：获取实际 TiDB Dashboard 地址](#第-1-步获取实际-tidb-dashboard-地址)中取得的 TiDB Dashboard 实际地址。

   > **警告：**
   >
   > 请务必保留 `proxy_pass` 指令中的 `/dashboard/` 路径，确保只有该路径下的服务会被反向代理，否则将引入安全风险。参见[提高 TiDB Dashboard 安全性](/dashboard/dashboard-ops-security.md)。

2. 重新载入 NGINX 以使配置生效：

   ```shell
   sudo nginx -s reload
   ```

3. 测试反向代理是否生效：访问 NGINX 所在机器的 8033 端口下 `/dashboard/` 地址，如 `http://example.com:8033/dashboard/` ，即可访问 TiDB Dashboard。

</details>

## 自定义路径前缀

TiDB Dashboard 默认在 `/dashboard/` 路径下提供服务，即使是反向代理也是如此，例如 `http://example.com:8033/dashboard/`。若要配置反向代理以非默认的路径提供 TiDB Dashboard 服务，例如 `http://example.com:8033/foo/` 或 `http://example.com:8033/`，可参考以下步骤。

### 第 1 步：修改 PD 配置指定 TiDB Dashboard 服务路径前缀

修改 PD 配置中 `[dashboard]` 类别的 `public-path-prefix` 配置项，可指定服务路径前缀。该配置修改后需要重启 PD 实例生效。

以 TiUP 部署且希望运行在 `http://example.com:8033/foo/` 为例，可指定以下配置：

```yaml
server_configs:
  pd:
    dashboard.public-path-prefix: /foo
```

<details>
  <summary>使用 TiUP 部署全新集群时修改配置</summary>

若要全新部署集群，可在 TiUP 拓扑文件 `topology.yaml` 中加入上述配置项后进行部署，具体步骤参阅 [TiUP 部署文档](/production-deployment-using-tiup.md#第-3-步初始化集群拓扑文件)。

</details>

<details>
  <summary>使用 TiUP 修改已部署集群的配置</summary>

1. 以编辑模式打开该集群的配置文件（将 `CLUSTER_NAME` 替换为集群名称）

   ```shell
   tiup cluster edit-config CLUSTER_NAME
   ```

2. 在 `server_configs` 的 `pd` 配置下修改或新增配置项，若没有 `server_configs` 请在最顶层新增：

   ```yaml
   server_configs:
     pd:
       dashboard.public-path-prefix: /foo
   ```

   修改完成后的配置文件类似于：

   ```yaml
   server_configs:
     pd:
       dashboard.public-path-prefix: /foo
   global:
     user: tidb
     ...
   ```

   或

   ```yaml
   monitored:
     ...
   server_configs:
     tidb: ...
     tikv: ...
     pd:
       dashboard.public-path-prefix: /foo
     ...
   ```

3. 滚动重启所有 PD 实例生效配置（将 `CLUSTER_NAME` 替换为集群名称）

   ```shell
   tiup cluster reload CLUSTER_NAME -R pd
   ```

   详情请参阅 [TiUP 常见运维操作 - 修改配置参数](/maintain-tidb-using-tiup.md#修改配置参数)。

</details>

若希望运行在根路径（如 `http://example.com:8033/`）下，相应的配置为：

```yaml
server_configs:
  pd:
    dashboard.public-path-prefix: /
```

> **警告：**
>
> 修改自定义路径前缀生效后，直接访问将不能正常使用 TiDB Dashboard，您只能通过和路径前缀匹配的反向代理访问。

### 第 2 步：修改反向代理配置

<details>
<summary>使用 HAProxy 反向代理</summary>

以 `http://example.com:8033/foo/` 为例，HAProxy 配置如下：

```haproxy
frontend tidb_dashboard_front
  bind *:8033
  use_backend tidb_dashboard_back if { path /foo } or { path_beg /foo/ }

backend tidb_dashboard_back
  mode http
  http-request set-path %[path,regsub(^/foo/?,/dashboard/)]
  server tidb_dashboard 192.168.0.123:2379
```

其中 `192.168.0.123:2379` 需替换为[第 1 步：获取实际 TiDB Dashboard 地址](#第-1-步获取实际-tidb-dashboard-地址)中取得的 TiDB Dashboard 实际地址中的 IP 及端口部分。

> **警告：**
>
> 请务必保留 `use_backend` 指令中的 `if` 部分，确保只有该路径下的服务会被反向代理，否则将引入安全风险。参见[提高 TiDB Dashboard 安全性](/dashboard/dashboard-ops-security.md)。

若希望运行在根路径（如 `http://example.com:8033/`），HAProxy 配置如下：

```nginx
frontend tidb_dashboard_front
  bind *:8033
  use_backend tidb_dashboard_back

backend tidb_dashboard_back
  mode http
  http-request set-path /dashboard%[path]
  server tidb_dashboard 192.168.0.123:2379
```

修改配置并重启 HAProxy 后即可生效。

</details>

<details>
<summary>使用 NGINX 反向代理</summary>

以 `http://example.com:8033/foo/` 为例，相应的 NGINX 配置为：

```nginx
server {
  listen 8033;
  location /foo/ {
    proxy_pass http://192.168.0.123:2379/dashboard/;
  }
}
```

其中 `http://192.168.0.123:2379/dashboard/` 需替换为[第 1 步：获取实际 TiDB Dashboard 地址](#第-1-步获取实际-tidb-dashboard-地址)中取得的 TiDB Dashboard 实际地址。

> **警告：**
>
> 请务必保留 `proxy_pass` 指令中的 `/dashboard/` 路径，确保只有该路径下的服务会被反向代理，否则将引入安全风险。参见 [提高 TiDB Dashboard 安全性](/dashboard/dashboard-ops-security.md)。

若希望运行在根路径（如 `http://example.com:8033/`），NGINX 配置为：

```nginx
server {
  listen 8033;
  location / {
    proxy_pass http://192.168.0.123:2379/dashboard/;
  }
}
```

修改配置并重启 NGINX 后即可生效：

```shell
sudo nginx -s reload
```

</details>

## 下一步

参阅[提高 TiDB Dashboard 安全性](/dashboard/dashboard-ops-security.md)文档了解如何增强 TiDB Dashboard 的安全性，如配置防火墙等。
