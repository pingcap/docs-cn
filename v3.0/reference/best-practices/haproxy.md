---
title: HAProxy 最佳实践
category: reference
---

# HAProxy 最佳实践

在线上使用 TiDB 数据库的时候，会遇到业务方希望 TiDB Server 层具有负载均衡能力。HAProxy 提供 TCP 协议下的负载均衡功能，TiDB 客户端可以通过连接 HAProxy 提供的浮动 IP 到 TiDB 数据库中进行数据的操作。本文介绍 HAProxy 在 TiDB 中的最佳实践配置和使用方法。

## HAProxy 简介

[HAProxy](https://github.com/haproxy/haproxy) 是由 C 语言编写的自由开放源码的软件，为基于 TCP 和 HTTP 协议的应用程序提供高可用性、负载均衡和代理服务。因为 HAProxy 能够快速、高效使用 CPU 和内存，所以目前使用非常广泛，许多知名网站诸如 GitHub、Bitbucket、Stack Overflow、Reddit、Tumblr、Twitter 和 Tuenti 以及亚马逊网络服务系统都在使用 HAProxy。

HAProxy 由 Linux 内核的核心贡献者 Willy Tarreau 于 2000 年编写，他现在仍然负责该项目的维护，并在开源社区免费提供版本迭代。最新的稳定版本 2.0.0 于 2019 年 8 月 16 日发布，带来更多[优秀的特性](https://www.haproxy.com/blog/haproxy-2-0-and-beyond/)。

## HAProxy 部分核心功能介绍

- [高可用性](http://cbonte.github.io/haproxy-dconv/1.9/intro.html#3.3.4)：HAProxy 提供优雅关闭服务和无缝切换的高可用功能；
- [负载均衡](http://cbonte.github.io/haproxy-dconv/1.9/configuration.html#4.2-balance)：L4（TCP）和 L7（HTTP）负载均衡模式，至少 9 类均衡算法，比如 roundrobin，leastconn，random 等；
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
|处理器|2 cores, 3.5 GHz|
|内存| 16 GB|
|存储容量| 50 GB (SATA)|
|网卡| 万兆网卡|

### 依赖软件

根据官方文档，对操作系统和依赖包有以下建议，如果通过 yum 源部署安装 HAProxy 软件，依赖包无需单独安装。

#### 操作系统

- Linux 2.4 操作系统，x86, x86_64, Alpha, Sparc, MIPS, PARISC 架构。
- Linux 2.6 / 3.x 操作系统，x86, x86_64, ARM, Sparc, PPC64 架构。
- Solaris 8/9 操作系统，UltraSPARC 2 and 3 架构。
- Solaris 10 操作系统，Opteron and UltraSPARC 架构。
- FreeBSD 4.10 - 10 操作系统，x86 架构。
- OpenBSD 3.1 to -current 操作系统，i386, amd64, macppc, alpha, sparc64 and VAX (check the ports) 架构。
- AIX 5.1 - 5.3 操作系统， Power™ architecture 架构。

#### 依赖包

- epel-release
- gcc
- systemd-devel

{{< copyable "shell-regular" >}}

```bash
yum -y install epel-release gcc systemd-devel
```

## 部署 HAProxy

HAProxy 配置 Database 负载均衡场景操作简单，以下部署操作具有普遍性，不具有特殊性，建议根据实际场景，个性化配置相关的[配置文件](http://cbonte.github.io/haproxy-dconv/1.9/configuration.html)。

![HAProxy](/media/haproxy.jpg)

### 安装 HAProxy

1. 使用 yum 安装 HAProxy

    {{< copyable "shell-regular" >}}

    ```bash
    yum -y install haproxy
    ```

2. 验证 HAProxy 安装是否成功

    {{< copyable "shell-regular" >}}

    ```bash
    which haproxy
    ```

#### HAProxy 命令介绍

{{< copyable "shell-regular" >}}

```bash
haproxy --help
```

|参数|描述|
|:-----|:---|
|-v|显示简略的版本信息|
|-vv|显示详细的版本信息|
|-d|debug 模式开启|
| -db|仅禁止后台模式|
|-dM [\<byte>]|执行分配内存|
|-V|启动过程显示配置和轮询信息|
|-D|开启守护进程模式|
|-C \<dir>|在加载配置文件之前更改目录位置|
|-W|主从模式|
|-q|静默模式，不输出信息|
|-c|只检查配置文件并在尝试绑定之前退出|
|-n|设置最大总连接数为 2000 |
|-m|限制最大可用内存（单位：MB）|
|-N|设置单点最大连接数，默认为 2000 |
|-L|本地实例对等名称|
|-p|将 HAProxy 所有子进程的 PID 信息写入该文件 |
|-de|禁止使用 speculative epoll，epoll 仅在 Linux 2.6 和某些定制的 Linux 2.4 系统上可用。|
|-dp|禁止使用 epoll，epoll 仅在 Linux 2.6 和某些定制的 Linux 2.4 系统上可用。|
|-dS|禁止使用 speculative epoll，epoll 仅在 Linux 2.6 和某些定制的 Linux 2.4 系统上可用。|
|-dR|禁止使用 SO_REUSEPORT|
|-dr|忽略服务器地址解析失败|
|-dV|禁止在服务器端使用 SSL|
|-sf/-st \<unix_socket> |在启动后，在 pidlist 中发送 FINISH 信号给 PID。收到此信号的进程将等待所有会话在退出之前完成，即优雅停止服务。此选项必须最后指定，后跟任意数量的 PID，SIGTTOU 和 SIGUSR1 都被发送。|
|-x \<unix_socket>,[\<bind options>...]|获取 socket 信息|
|-S \<unix_socket>,[\<bind options>...]|分配新的 socket|

### 配置 HAProxy

yum 安装过程中会生成配置模版。

```yaml
global                                     # 全局配置
   log         127.0.0.1 local2            # 定义全局的 syslog 服务器，最多可以定义两个
   chroot      /var/lib/haproxy            # 将当前目录为指定目录，设置超级用户权限启动进程，提高安全性
   pidfile     /var/run/haproxy.pid        # 将 HAProxy 进程写入 PID 文件
   maxconn     4000                        # 设置每个 HAProxy 进程锁接受的最大并发连接数
   user        haproxy                     # 同 uid 参数，使用是用户名
   group       haproxy                     # 同 gid 参数，建议专用用户组
   nbproc      40                          # 启动多个进程来转发请求，需要调整到足够大的值来保证 HAProxy 本身不会成为瓶颈
   daemon                                  # 让 HAProxy 以守护进程的方式工作于后台，等同于“-D”选项的功能。当然，也可以在命令行中用“-db”选项将其禁用。
   stats socket /var/lib/haproxy/stats     # 定义统计信息保存位置

defaults                                   # 默认配置
   log global                              # 日志继承全局配置段的设置
   retries 2                               # 向上游服务器尝试连接的最大次数，超过此值就认为后端服务器不可用
   timeout connect  2s                     # HAProxy 与后端服务器连接超时时间，如果在同一个局域网内可设置成较短的时间
   timeout client 30000s                   # 定义客户端与 HAProxy 连接后，数据传输完毕，不再有数据传输，即非活动连接的超时时间
   timeout server 30000s                   # 定义 HAProxy 与上游服务器非活动连接的超时时间

listen admin_stats                         # frontend 和 backend 的组合体，监控组的名称，按需自定义名称
   bind 0.0.0.0:8080                       # 配置监听端口
   mode http                               # 配置监控运行的模式，此处为 `http` 模式
   option httplog                          # 表示开始启用记录 HTTP 请求的日志功能
   maxconn 10                              # 最大并发连接数
   stats refresh 30s                       # 配置每隔 30 秒自动刷新监控页面
   stats uri /haproxy                      # 配置监控页面的 URL
   stats realm HAProxy                     # 配置监控页面的提示信息
   stats auth admin:pingcap123             # 配置监控页面的用户和密码 admin，可以设置多个用户名
   stats hide-version                      # 配置隐藏统计页面上的 HAProxy 版本信息
   stats  admin if TRUE                    # 配置手工启用/禁用，后端服务器（HAProxy-1.4.9 以后版本）

listen tidb-cluster                        # 配置 database 负载均衡
   bind 0.0.0.0:3390                       # 配置浮动 IP 和 监听端口
   mode tcp                                # HAProxy 中要使用第四层的应用层
   balance leastconn                       # 连接数最少的服务器优先接收连接。`leastconn` 建议用于长会话服务，例如 LDAP、SQL、TSE 等，而不是短会话协议，如 HTTP。该算法是动态的，对于实例启动慢的服务器，权重会在运行中作调整。
   server tidb-1 10.9.18.229:4000 check inter 2000 rise 2 fall 3       # 检测 4000 端口，检测频率为 2000 毫秒。如果检测出 2 次正常就认定机器已恢复正常使用，如果检测出 3 次失败便认定该服务器不可用。
   server tidb-2 10.9.39.208:4000 check inter 2000 rise 2 fall 3
   server tidb-3 10.9.64.166:4000 check inter 2000 rise 2 fall 3
```

### 使用 `systemd` 启动 HAProxy

- 方法一：执行 `haproxy`

    {{< copyable "shell-regular" >}}

    ```bash
    haproxy -f /etc/haproxy/haproxy.cfg
    ```

- 方法二：使用 `systemd` 启动 HAProxy，默认读取 `/etc/haproxy/haproxy.cfg`（推荐）

    {{< copyable "shell-regular" >}}

    ```bash
    systemctl start haproxy.service
    ```

### 使用 `systemd` 停止 HAProxy

- 方法一：执行 `kill -9`

    {{< copyable "shell-regular" >}}

    ```bash
    ps -ef | grep haproxy
    ```

    终止 HAProxy 相关的 PID 进程：

    {{< copyable "shell-regular" >}}

    ```bash
    kill -9 ${haproxy.pid}
    ```

- 方法二：使用 `systemd` 停止 HAProxy

    {{< copyable "shell-regular" >}}

    ```bash
    systemctl stop haproxy.service
    ```
