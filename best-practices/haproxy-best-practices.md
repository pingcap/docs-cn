---
title: HAProxy 在 TiDB 中的最佳实践
aliases: ['/docs-cn/dev/best-practices/haproxy-best-practices/','/docs-cn/dev/reference/best-practices/haproxy/']
---

# HAProxy 在 TiDB 中的最佳实践

本文介绍 [HAProxy](https://github.com/haproxy/haproxy) 在 TiDB 中的最佳配置和使用方法。HAProxy 提供 TCP 协议下的负载均衡能力，TiDB 客户端通过连接 HAProxy 提供的浮动 IP 即可对数据进行操作，实现 TiDB Server 层的负载均衡。

![HAProxy 在 TiDB 中的最佳实践](/media/haproxy.jpg)

## HAProxy 简介

HAProxy 是由 C 语言编写的自由开放源码的软件，为基于 TCP 和 HTTP 协议的应用程序提供高可用性、负载均衡和代理服务。因为 HAProxy 能够快速、高效使用 CPU 和内存，所以目前使用非常广泛，许多知名网站诸如 GitHub、Bitbucket、Stack Overflow、Reddit、Tumblr、Twitter 和 Tuenti 以及亚马逊网络服务系统都在使用 HAProxy。

HAProxy 由 Linux 内核的核心贡献者 Willy Tarreau 于 2000 年编写，他现在仍然负责该项目的维护，并在开源社区免费提供版本迭代。最新的稳定版本 2.0.0 于 2019 年 8 月 16 日发布，带来更多[优秀的特性](https://www.haproxy.com/blog/haproxy-2-0-and-beyond/)。

## HAProxy 部分核心功能介绍

- [高可用性](http://cbonte.github.io/haproxy-dconv/1.9/intro.html#3.3.4)：HAProxy 提供优雅关闭服务和无缝切换的高可用功能；
- [负载均衡](http://cbonte.github.io/haproxy-dconv/1.9/configuration.html#4.2-balance)：L4 (TCP) 和 L7 (HTTP) 两种负载均衡模式，至少 9 类均衡算法，比如 roundrobin，leastconn，random 等；
- [健康检查](http://cbonte.github.io/haproxy-dconv/1.9/configuration.html#5.2-check)：对 HAProxy 配置的 HTTP 或者 TCP 模式状态进行检查；
- [会话保持](http://cbonte.github.io/haproxy-dconv/1.9/intro.html#3.3.6)：在应用程序没有提供会话保持功能的情况下，HAProxy 可以提供该项功能；
- [SSL](http://cbonte.github.io/haproxy-dconv/1.9/intro.html#3.3.2)：支持 HTTPS 通信和解析；
- [监控与统计](http://cbonte.github.io/haproxy-dconv/1.9/intro.html#3.3.3)：通过 web 页面可以实时监控服务状态以及具体的流量信息。

## 准备环境

在部署 HAProxy 之前，需准备好以下环境。

### 硬件要求

根据官方文档，对 HAProxy 的服务器硬件配置有以下建议，也可以根据负载均衡环境进行推算，在此基础上提高服务器配置。

|硬件资源|最低配置|
|:---|:---|
|CPU|2 核，3.5 GHz|
|内存|16 GB|
|存储容量|50 GB（SATA 盘）|
|网卡|万兆网卡|

### 依赖软件

根据官方文档，对操作系统和依赖包有以下建议，如果通过 yum 源部署安装 HAProxy 软件，依赖包无需单独安装。

#### 操作系统

| 操作系统版本               | 架构                                       |
|:-------------------------|:------------------------------------------|
| Linux 2.4                | x86、x86_64、Alpha、SPARC、MIPS 和 PA-RISC  |
| Linux 2.6 或 3.x         | x86、x86_64、ARM、SPARC 和 PPC64            |
| Solaris 8 或 9           | UltraSPARC II 和 UltraSPARC III            |
| Solaris 10               | Opteron 和 UltraSPARC                      |
| FreeBSD 4.10 ~ 10        | x86                                        |
| OpenBSD 3.1 及以上版本     | i386、AMD64、macppc、Alpha 和 SPARC64       |
| AIX 5.1 ~ 5.3            | Power™                                     |

#### 依赖包

- epel-release
- gcc
- systemd-devel

执行如下命令安装依赖包：

{{< copyable "shell-regular" >}}

```bash
yum -y install epel-release gcc systemd-devel
```

## 部署 HAProxy

HAProxy 配置 Database 负载均衡场景操作简单，以下部署操作具有普遍性，不具有特殊性，建议根据实际场景，个性化配置相关的[配置文件](http://cbonte.github.io/haproxy-dconv/1.9/configuration.html)。

### 安装 HAProxy

1. 使用 yum 安装 HAProxy：

    {{< copyable "shell-regular" >}}

    ```bash
    yum -y install haproxy
    ```

2. 验证 HAProxy 安装是否成功：

    {{< copyable "shell-regular" >}}

    ```bash
    which haproxy
    ```

    ```
    /usr/sbin/haproxy
    ```

#### HAProxy 命令介绍

执行如下命令查看命令行参数及基本用法：

{{< copyable "shell-regular" >}}

```bash
haproxy --help
```

| 参数    | 说明       |
| :------- | :--------- |
| `-v` | 显示简略的版本信息。 |
| `-vv` | 显示详细的版本信息。 |
| `-d` | 开启 debug 模式。 |
| `-db` | 禁用后台模式和多进程模式。 |
| `-dM [<byte>]` | 执行分配内存。|
| `-V` | 启动过程显示配置和轮询信息。 |
| `-D` | 开启守护进程模式。 |
| `-C <dir>` | 在加载配置文件之前更改目录位置至 `<dir>`。 |
| `-W` | 主从模式。 |
| `-q` | 静默模式，不输出信息。 |
| `-c` | 只检查配置文件并在尝试绑定之前退出。 |
| `-n <limit>` | 设置每个进程的最大总连接数为 `<limit>`。 |
| `-m <limit>` | 设置所有进程的最大可用内存为 `<limit>`（单位：MB）。 |
| `-N <limit>` | 设置单点最大连接数为 `<limit>`，默认为 2000。 |
| `-L <name>` | 将本地实例对等名称改为 `<name>`，默认为本地主机名。 |
| `-p <file>` | 将 HAProxy 所有子进程的 PID 信息写入 `<file>`。 |
| `-de` | 禁止使用 epoll(7)，epoll(7) 仅在 Linux 2.6 和某些定制的 Linux 2.4 系统上可用。 |
| `-dp` | 禁止使用 epoll(2)，可改用 select(2)。 |
| `-dS` | 禁止使用 splice(2)，splice(2) 在一些旧版 Linux 内核上不可用。 |
| `-dR` | 禁止使用 SO_REUSEPORT。 |
| `-dr` | 忽略服务器地址解析失败。 |
| `-dV` | 禁止在服务器端使用 SSL。 |
| `-sf <pidlist>` | 启动后，向 pidlist 中的 PID 发送 `finish` 信号，收到此信号的进程在退出之前将等待所有会话完成，即优雅停止服务。此选项必须最后指定，后跟任意数量的 PID。从技术上讲，SIGTTOU 和 SIGUSR1 都被发送。 |
| `-st <pidlist>` | 启动后，向 pidlist 中的 PID 发送 `terminate` 信号，收到此信号的进程将立即终止，关闭所有活动会话。此选项必须最后指定，后跟任意数量的 PID。从技术上讲，SIGTTOU 和 SIGTERM 都被发送。 |
| `-x <unix_socket>` | 连接指定的 socket 并从旧进程中获取所有 listening socket，然后，使用这些 socket 而不是绑定新的。 |
| `-S <bind>[,<bind_options>...]` | 主从模式下，创建绑定到主进程的 socket，此 socket 可访问每个子进程的 socket。 |

更多有关 HAProxy 命令参数的信息，可参阅 [Management Guide of HAProxy](http://cbonte.github.io/haproxy-dconv/1.9/management.html) 和 [General Commands Manual of HAProxy](https://manpages.debian.org/buster-backports/haproxy/haproxy.1.en.html)。

### 配置 HAProxy

yum 安装过程中会生成配置模版，你也可以根据实际场景自定义配置如下配置项。

```yaml
global                                     # 全局配置。
   log         127.0.0.1 local2            # 定义全局的 syslog 服务器，最多可以定义两个。
   chroot      /var/lib/haproxy            # 更改当前目录并为启动进程设置超级用户权限，从而提高安全性。
   pidfile     /var/run/haproxy.pid        # 将 HAProxy 进程的 PID 写入 pidfile。
   maxconn     4000                        # 每个 HAProxy 进程所接受的最大并发连接数。
   user        haproxy                     # 同 UID 参数。
   group       haproxy                     # 同 GID 参数，建议使用专用用户组。
   nbproc      40                          # 在后台运行时创建的进程数。在启动多个进程转发请求时，确保该值足够大，保证 HAProxy 不会成为瓶颈。
   daemon                                  # 让 HAProxy 以守护进程的方式工作于后台，等同于命令行参数“-D”的功能。当然，也可以在命令行中用“-db”参数将其禁用。
   stats socket /var/lib/haproxy/stats     # 统计信息保存位置。

defaults                                   # 默认配置。
   log global                              # 日志继承全局配置段的设置。
   retries 2                               # 向上游服务器尝试连接的最大次数，超过此值便认为后端服务器不可用。
   timeout connect  2s                     # HAProxy 与后端服务器连接超时时间。如果在同一个局域网内，可设置成较短的时间。
   timeout client 30000s                   # 客户端与 HAProxy 连接后，数据传输完毕，即非活动连接的超时时间。
   timeout server 30000s                   # 服务器端非活动连接的超时时间。

listen admin_stats                         # frontend 和 backend 的组合体，此监控组的名称可按需进行自定义。
   bind 0.0.0.0:8080                       # 监听端口。
   mode http                               # 监控运行的模式，此处为 `http` 模式。
   option httplog                          # 开始启用记录 HTTP 请求的日志功能。
   maxconn 10                              # 最大并发连接数。
   stats refresh 30s                       # 每隔 30 秒自动刷新监控页面。
   stats uri /haproxy                      # 监控页面的 URL。
   stats realm HAProxy                     # 监控页面的提示信息。
   stats auth admin:pingcap123             # 监控页面的用户和密码，可设置多个用户名。
   stats hide-version                      # 隐藏监控页面上的 HAProxy 版本信息。
   stats  admin if TRUE                    # 手工启用或禁用后端服务器（HAProxy 1.4.9 及之后版本开始支持）。

listen tidb-cluster                        # 配置 database 负载均衡。
   bind 0.0.0.0:3390                       # 浮动 IP 和 监听端口。
   mode tcp                                # HAProxy 要使用第 4 层的传输层。
   balance leastconn                       # 连接数最少的服务器优先接收连接。`leastconn` 建议用于长会话服务，例如 LDAP、SQL、TSE 等，而不是短会话协议，如 HTTP。该算法是动态的，对于启动慢的服务器，服务器权重会在运行中作调整。
   server tidb-1 10.9.18.229:4000 check inter 2000 rise 2 fall 3       # 检测 4000 端口，检测频率为每 2000 毫秒一次。如果 2 次检测为成功，则认为服务器可用；如果 3 次检测为失败，则认为服务器不可用。
   server tidb-2 10.9.39.208:4000 check inter 2000 rise 2 fall 3
   server tidb-3 10.9.64.166:4000 check inter 2000 rise 2 fall 3
```

如要通过 show processlist 查看连接来源 IP，需要配置使用 [PROXY 协议](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt)连接 TiDB。

```yaml
   server tidb-1 10.9.18.229:4000 send-proxy check inter 2000 rise 2 fall 3       
   server tidb-2 10.9.39.208:4000 send-proxy check inter 2000 rise 2 fall 3
   server tidb-3 10.9.64.166:4000 send-proxy check inter 2000 rise 2 fall 3
```

> **注意：**
>
> 使用 PROXY 协议，需要对应地添加 tidb server 的 `proxy-protocol.networks` 配置文件参数。

### 启动 HAProxy

- 方法一：执行 `haproxy`，默认读取 `/etc/haproxy/haproxy.cfg`（推荐）。

    {{< copyable "shell-regular" >}}

    ```bash
    haproxy -f /etc/haproxy/haproxy.cfg
    ```

- 方法二：使用 `systemd` 启动 HAProxy。

    {{< copyable "shell-regular" >}}

    ```bash
    systemctl start haproxy.service
    ```

### 停止 HAProxy

- 方法一：使用 `kill -9`。

    1. 执行如下命令：

        {{< copyable "shell-regular" >}}

        ```bash
        ps -ef | grep haproxy
        ```

    2. 终止 HAProxy 相关的 PID 进程：

        {{< copyable "shell-regular" >}}

        ```bash
        kill -9 ${haproxy.pid}
        ```

- 方法二：使用 `systemd`。

    {{< copyable "shell-regular" >}}

    ```bash
    systemctl stop haproxy.service
    ```
