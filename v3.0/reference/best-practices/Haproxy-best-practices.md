# HAProxy 介绍

HAProxy是一个使用C语言编写的自由及开放源代码软件，其提供高可用性、负载均衡，以及基于TCP和HTTP的应用程序代理。GitHub、Bitbucket、Stack Overflow、Reddit、Tumblr、Twitter和 Tuenti在内的知名网站，及亚马逊网络服务系统都使用了HAProxy。
HAProxy 提供了 L4(TCP) 和 L7(HTTP) 两种负载均衡能力，具备丰富的功能。HAProxy 的社区非常活跃，版本更新快速（最新稳定版 1.7.2 于 2017/01/13 推出）。最关键的是，HAProxy 具备媲美商用负载均衡器的性能和稳定性。因为 HAProxy 的上述优点，它当前不仅仅是免费负载均衡软件的首选，更几乎成为了唯一选择。

# HAProxy 的核心功能

- 负载均衡：L4 和 L7 两种模式，支持 RR/静态 RR/LC/IP Hash/URI Hash/URL_PARAM Hash/HTTP_HEADER Hash等丰富的负载均衡算法；
- 健康检查：支持 TCP 和 HTTP 两种健康检查模式；
- 会话保持：对于未实现会话共享的应用集群，可通过 Insert Cookie/Rewrite Cookie/Prefix Cookie，以及上述的多种 Hash 方式实现会话保持；
- SSL：HAProxy 可以解析HTTPS协议，并能够将请求解密为HTTP后向后端传输;
- HTTP 请求重写与重定向；
- 监控与统计：HAProxy 提供了基于 Web 的统计信息页面，展现健康状态和流量数据。基于此功能，使用者可以开发监控程序来监控 HAProxy 的状态。



# HAProxy 部署操作
![haproxy](/media/Haproxy.jpg)
## 硬件要求 

根据官方文档对 HAProxy 的服务器硬件配置有以下建议，也可以根据负载均衡环境进行实际推算，在此基础上提高服务器配置。

|硬件资源|最低配置|
|---|---|
|CPU|2 cores，3.5 GHz| 
|Memory| 16 GB|
|Storage| 50 GB（SATA）|
|Network Interface Card| 万兆网卡|


## 依赖软件
根据官方介绍对操作系统和依赖包有以下建议，如果是通过 yum 源部署安装 haproxy 软件，依赖包可以不需要单独安装。

## 操作系统
- Linux 2.4 on x86, x86_64, Alpha, Sparc, MIPS, PARISC
- Linux 2.6 / 3.x on x86, x86_64, ARM, Sparc, PPC64
- Solaris 8/9 on UltraSPARC 2 and 3
- Solaris 10 on Opteron and UltraSPARC
- FreeBSD 4.10 - 10 on x86
- OpenBSD 3.1 to -current on i386, amd64, macppc, alpha, sparc64 and VAX (check the ports)
- AIX 5.1 - 5.3 on Power™ architecture

## 依赖包
- epel-release
- gcc
- systemd-devel

## 版本迭代

根据官方建议，目前稳定版本的 HAProxy 为稳定版[2.0 特性](https://www.haproxy.com/blog/haproxy-2-0-and-beyond/)

## 部署操作

HAProxy 配置 Database 负载均衡场景操作简单，以下部署操作具有普遍性，不具有特殊性，建议根据实际场景，个性化配置相关的[配置文件](http://cbonte.github.io/haproxy-dconv/1.9/configuration.html)。

### 安装 haproxy
- yum 安装 (推荐)
#### yum 安装 haproxy
```bash
yum -y install haproxy
```
#### 验证 haproxy 安装是否成功
```bash
which haproxy
```
### haproxy 命令介绍
```bash
$ haproxy --help
HA-Proxy version 1.9.0 2018/12/19 - https://haproxy.org/
Usage : haproxy [-f <cfgfile|cfgdir>]* [ -vdVD ] [ -n <maxconn> ] [ -N <maxpconn> ]
        [ -p <pidfile> ] [ -m <max megs> ] [ -C <dir> ] [-- <cfgfile>*]
```

|参数|描述|详情|
|-----|---|---|
|-v|displays version|版本|
|-vv|shows known build options.|版本|
|-d|enters debug mode|debug 模式开启|
| -db|only disables background mode.|禁止后台模式|
|-dM|[\<byte>] poisons memory with \<byte> (defaults to 0x50)|执行分配内存|
|-V|enters verbose mode (disables quiet mode)|启动过程显示配置和轮询信息
|-D|goes daemon|开启守护进程模式||
|-C|changes to \<dir> before loading files.||
|-W|master-worker mode.|主从模式|
|-q|quiet mode : don't display messages|静默模式，不输出信息|
|-c|check mode : only check config files and exit|检查配置信息文件|
|-n|sets the maximum total # of connections (2000)|最大总连接数|
|-m|limits the usable amount of memory (in MB)|最大使用内存|
|-N|sets the default, per-proxy maximum # of connections (2000)|单点最大连接数|
|-L|set local peer name (default to hostname)|本地实例对等名称|
|-p|writes pids of all children to this file|haproxy 进程 pid 信息写入 file |
|-de|disables epoll() usage even when available|禁止使用speculative epoll。epoll仅在Linux 2.6和某些定制的Linux 2.4系统上可用。|
|-dp|disables poll() usage even when available|禁止使用epoll。epoll仅在Linux 2.6和某些定制的Linux 2.4系统上可用。|
|-dS|disables splice usage (broken on old kernels)|禁止使用speculativeepoll。epoll仅在Linux 2.6和某些定制的Linux 2.4系统上可用。|
|-dR|disables SO_REUSEPORT usage|禁止使用 SO_REUSEPORT|
|-dr|ignores server address resolution failures|忽略失败的 server|
|-dV|disables SSL verify on servers side|禁止使用 SSL 在 servers 端|
|-sf/-st|\<unix_socket> get listening sockets from a unix socket|在启动后，在pidlist中发送FINISH信号给pid。收到此信号的进程将等待所有会话在退出之前完成。此选项必须最后指定，后跟任意数量的PID。 从技术上讲，SIGTTOU和SIGUSR1都被发送。|
|-x|\<unix_socket>[,<bind options>...] new stats socket for the master|获取 socket 信息|
|-S|\<unix_socket>[,\<bind options>...] new stats socket for the master|分配新的 socket|


#### 配置 haproxy configuration

> yum 安装过程中会生成配置模版
```yaml
global  # 全局配置
   log         127.0.0.1 local2       # 定义全局的 syslog 服务器，最多可以定义两个
   chroot      /var/lib/haproxy      # 将当前目录为指定目录，设置超级用户权限启动进程，提高安全性
   pidfile     /var/run/haproxy.pid  # 将 haproxy 进程写入 pid 文件
   maxconn     4000                     # 设置每个 haproxy 进程锁接受的最大并发连接数
   user        haproxy                     # 同 uid 参数，使用是用户名
   group       haproxy                    # 同 gid 参数，建议专用用户组
   nbproc      40                            # 启动多个进程来转发请求，需要调整到足够大的值来保证 haproxy 本身不会成为瓶颈
   daemon                                    # 让haproxy以守护进程的方式工作于后台，其等同于“-D”选项的功能。当然，也可以在命令行中以“-db”选项将其禁用。
   stats socket /var/lib/haproxy/stats  # 定义统计信息保存位置
 
defaults                                        # 默认配置
   log global                                  # 日志继承全局配置段的设置
   retries 2                                     # 向上游服务器尝试连接的最大次数，超过此值就认为后端服务器不可用
   timeout connect  2s                   # haproxy与后端服务器连接超时时间，如果在同一个局域网可设置较小的时间
   timeout client 30000s                # 定义客户端与haproxy连接后，数据传输完毕，不再有数据传输，即非活动连接的超时时间
   timeout server 30000s               # 定义haproxy与上游服务器非活动连接的超时时间
 
listen admin_stats                         # frontend和backend的组合体,监控组的名称，按需自定义名称
   bind 0.0.0.0:8080                       # 配置监听端口
   mode http                                   # 配置监控运行的模式，在这为http模式
   option httplog                              # 表示开始打开记录http请求的日志功能
   maxconn 10                                # 最大并发连接数
   stats refresh 30s                         # 配置每隔 30 秒自动刷新监控页面
   stats uri /haproxy                        # 配置监控页面的url
   stats realm Haproxy                   # 配置监控页面的提示信息 
   stats auth admin:pingcap123     # 配置监控页面的用户和密码admin,可以设置多个用户名       
   stats hide-version                        # 配置隐藏统计页面上的HAproxy版本信息
   stats  admin if TRUE                   # 配置手工启用/禁用,后端服务器(haproxy-1.4.9以后版本)  
 
listen tidb-cluster                           # 配置 database 负载均衡                   
   bind 0.0.0.0:3390                       # 配置浮动 IP 和 监听端口         
   mode tcp                                    # haproxy中还要使用4层的应用
   balance leastconn                      # 连接数最少的服务器优先接收连接。leastconn建议用于长会话服务，例如LDAP、SQL、TSE等，而不适合短会话协议。如HTTP.该算法是动态的，对于实例启动慢的服务器权重会在运行中调整。 
   server tidb-1 10.9.18.229:4000 check inter 2000 rise 2 fall 3       # 这是检测 4000 端口，检测频率是2000毫秒，检测 2 次正常就认为机器又可用了，失败 3 次认为此服务器就不可用               
   server tidb-2 10.9.39.208:4000 check inter 2000 rise 2 fall 3                      
   server tidb-3 10.9.64.166:4000 check inter 2000 rise 2 fall 3                      
```

#### systemd 启动  haproxy
- 方法一：执行 haproxy
```bash
haproxy -f /etc/haproxy/haproxy.cfg
```
- 方法二：systemd 启动 haproxy，默认读取 （推荐）/etc/haproxy/haproxy.cfg
```bash
systemctl start haproxy.service
```
#### systemd 停止  haproxy

- 方法一：kill -9
```bash
ps -ef |grep haproxy 
kill -9 haproxy.pid
```
- 方法二：systemd 停止 haproxy
```bash
systemctl stop haproxy.service
```

