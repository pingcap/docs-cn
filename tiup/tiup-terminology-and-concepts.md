---
title: TiUP 术语及核心概念
category: tools
---

# TiUP 术语及核心概念

本文主要说明 TiUP 的重要术语和核心概念。

## TiUP 组件

TiUP 程序只包含少数几个命令，用来下载、更新、卸载组件。TiUP 通过各种组件来扩展其功能。**组件**是一个可以运行的程序或脚本，通过 `tiup <component>` 运行组件时，TiUP 会添加一组环境变量，并为该程序创建好对应的数据目录，然后运行该程序。

通过运行 `tiup <component>` 命令，你可以运行支持的 TiUP 组件，其中运行的逻辑为：

1. 如果用户通过 `tiup <component>[:version]` 运行指定某个组件的特定版本：
    - 组件在本地未安装任何版本，则从镜像服务器下载最新稳定版本
    - 组件在本地安装有其他版本，但是没有用户指定的版本，则从镜像服务器下载用户指定版本
    - 如果本地已经安装指定版本，则设置环境变量来运行已经安装的版本
2. 如果用户通过 `tiup <component>` 运行某个组件，且未指定任何版本：
   - 组件在本地未安装任何版本，则从镜像服务器下载最新稳定版本
   - 如果本地已经安装部分版本，则设置环境变量来运行已经安装的版本中的最新版本

开发一个组件本质上和写一个脚本以及开发一个普通的程序没有任何差别，区别在于 TiUP 组件需要使用 [`tiup package`](/tiup/tiup-package.md) 进行打包，并生成对应的元信息，如果组件已经在运行时，TiUP 会负责指定运行时临时目录。

通过 TiUP 运行的组件会包含以下环境变量（环境变量都在 TiUP 项目中的 pkg/localmeta/constant.go 中定义）：

- `EnvNameInstanceDataDir = "TIUP_INSTANCE_DATA_DIR"` 表示当前实例运行的工作目录，通常应该是 `$TIUP_HOME/data/<subdir>`，其中 subdir 为用户指定的 tag，如果用户没有指定 tag，则为一个随机字符串。
- `EnvNameComponentDataDir = "TIUP_COMPONENT_DATA_DIR"` 表示当前组件的持久化目录，通常应该是 `$TIUP_HOME/storage/<component>`。
- `EnvNameComponentInstallDir = "TIUP_COMPONENT_INSTALL_DIR"` 表示当前组件的安装目录，通常应该是 `$TIUP_HOME/components/<component>/<version>`。
- `EnvNameWorkDir = "TIUP_WORK_DIR"` 表示 TiUP 的工作目录，如果组件参数包含路径，同时路径是一个相对路径，这个相对路径是相对于 TiUP 的工作目录，而不是组件的工作目录。
- `EnvNameHome = "TIUP_HOME"` 表示 TiUP 的 Profile 目录。
- `EnvTag = "TIUP_TAG"` 表示这个实例的 tag。
  
## TiUP 镜像仓库

TiUP 的所有组件都从镜像仓库 (mirrors) 下载，镜像仓库包含各个组件的 TAR 包以及对应的元信息（版本、入口启动文件、校验和）。TiUP 默认使用 PingCAP 官方的镜像仓库。用户可以通过 TIUP_MIRRORS 环境变量自定义镜像仓库。

镜像仓库可以是本地文件目录或在线 HTTP 服务器：

1. `TIUP_MIRRORS=/path/to/local tiup list --refresh`
2. `TIUP_MIRRORS=https://private-mirrors.example.com tiup list --refresh`
