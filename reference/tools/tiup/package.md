---
title: 组件打包
category: tools
---

# 组件打包

当想要新增一个组件，或者新增一个已有组件的版本时，需要用 tar 将相关文件打包然后传到镜像仓库中，用 tar 打包并不是一件困难的事情，麻烦在于需要更新仓库的元信息，要避免更新元信息的时候破坏已有组件的信息。因此 package 组件便承担了这个任务。

```bash
[root@localhost ~]# tiup package --help
Package a tiup component and generate package directory

Usage:
  tiup package target [flags]

Flags:
  -C, -- string          打 tar 包前先切换目录，等同于 tar 的 -C 参数
      --arch string      组件运行的处理器架构 (默认为当前的 GOARCH)
      --desc string      组件的描述信息
      --entry string     组件的二进制文件位于包中的位置
  -h, --help             帮助信息
      --hide tiup list   在 tiup list 中隐藏该组件
      --name string      组件名称
      --os string        组件运行的操作系统 (默认为当前的 GOOS)
      --release string   组件的版本
      --standalone       该组件是否可以独立运行（例如 PD 不能独立运行，但是 playground 可以）
```

## Hello World

本节我们开发并打包一个 hello 组件，它唯一的功能就是输出它自带配置文件的内容，该文件的内容为 "Hello World"。为了简单起见，我们采用 bash 脚本来开发该组件.

### 首先创建它的配置文件，该文件内容就只有 "Hello World"

{{< copyable "shell-regular" >}}

```shell
cat > config.txt << EOF
Hello World
EOF
```

### 然后创建可执行文件

{{< copyable "shell-regular" >}}

```shell
cat > hello.sh << EOF
#! /bin/sh
cat \${TIUP_COMPONENT_INSTALL_DIR}/config.txt
EOF

chmod 755 hello.sh
```

环境变量 `TIUP_COMPONENT_INSTALL_DIR` 会由 TiUP 在运行时传入，指向该组件的安装目录。

然后参考[搭建私有镜像](/reference/tools/tiup/mirrors.md) 搭建离线镜像或私有镜像（主要是因为官方镜像现在没开放 publish 功能，不能发布自己的包），搭建完之后确保 TIUP_MIRRORS 变量指向搭建的镜像。

### 打包

{{< copyable "shell-regular" >}}

```shell
tiup package hello.sh config.txt --name=hello --entry=hello.sh --release=v0.0.1
```

此步骤会创建一个 package 目录，里面会放置打包好的文件和元信息。

### 上传到仓库

由于目前官方仓库未开放上传，我们只能上传到第 3 步中自己搭建的镜像上，上传方式就是直接将 package 中的所有文件拷贝到第 3 步 tiup mirrors 的 ${target-dir} 中。

```bash
cp package/* path/to/mirror/
```

如果第 3 步创建的目录恰好在当前目录下，并且名字叫 package，那就不需要手动 copy 了。

### 执行

```bash
[root@localhost ~]# tiup list hello --refresh
Available versions for hello (Last Modified: 2020-04-23T16:45:53+08:00):
Version  Installed  Release:                   Platforms
-------  ---------  --------                   ---------
v0.0.1              2020-04-23T16:51:41+08:00  darwin/amd64

[root@localhost ~]# tiup hello
The component `hello` is not installed; downloading from repository.
Starting component `hello`: /Users/joshua/.tiup/components/hello/v0.0.1/hello.sh
Hello World
```