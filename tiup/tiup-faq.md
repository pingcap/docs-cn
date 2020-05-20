---
title: TiUP FAQ
category: tools
---

# TiUP FAQ

## TiUP 是否可以不使用官方镜像源？

TiUP 支持通过环境变量 TIUP_MIRRORS 指定镜像源，镜像源的地址可以是一个本地目录或 HTTP 服务器地址。如果用户的环境不能访问网络，可以建立自己的离线镜像源使用 TiUP。

## 如何将自己编写的组件放入 TiUP 镜像仓库？

暂时 TiUP 还不能接受外部开发的组件，但是 TiUP Team 已经制定了 TiUP 组件开发规范，同时正在开发 tiup-publish 组件，完成 tiup-publish 组件后，开发者可以通过 `tiup publish <comp> <version>` 将自己开发的组件发布到 TiUP 的官方镜像仓库。

## tiup-playground 和 tiup-cluster 有什么区别？

TiUP Playground 组件主要定位是快速上手和搭建单机的开发环境，支持 Linux/MacOS，要运行一个指定版本的 TiUP 集群更加简单。TiUP Cluster 组件主要是部署生成环境集群，通常是一个大规模的集群，还包含运维相关操作。
