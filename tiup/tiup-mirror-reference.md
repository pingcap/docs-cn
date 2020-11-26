---
title: tiup mirror reference
aliases: ['/docs-cn/dev/tiup/tiup-mirror-reference/']
---

# tiup mirror reference

## 介绍

TiUP 镜像是 TiUP 的组件仓库，存放了一些列的组件和这些组件的元信息。镜像可以以以下两种形式存在：
- 本地磁盘上的目录：用于服务本地的 TiUP 客户端，文档中将称之为本地镜像
- 基于远程的磁盘目录启动的 HTTP 镜像：服务远程的 TiUP 客户端，文档中将称之为远程镜像

## 镜像的创建与更新

镜像可以通过以下两种方式创建：
- 通过命令 `tiup mirror init` 从零生成
- 通过命令 `tiup mirrir clone` 从已有镜像克隆

在创建镜像之后，可以通过 `tiup mirror` 相关命令来给镜像添加组件或删除组件，无论是通过何种方式更新镜像，TiUP 都不会从镜像中删除任何文件，而是通过增加文件并分配新版本号的方式更新。

## 本地镜像

一个典型的镜像目录结构如下：

```
+ <mirror-dir>                                  # 镜像根目录
|-- root.json                                   # 镜像根证书
|-- {1..N}.root.json                            # 镜像根证书
|-- {1..N}.index.json                           # 组件/用户索引
|-- {1..N}.{component}.json                     # 组件元信息
|-- {component}-{version}-{os}-{arch}.tar.gz    # 组件二进制包
|-- snapshot.json                               # 镜像最新快照
|-- timestamp.json                              # 镜像最新时间戳
|--+ commits                                    # 镜像更新日志（可删除）
   |--+ commit-{ts1..tsN}
      |-- {N}.{component}.json
      |-- {N}.index.json
      |-- {component}-{version}-{os}-{arch}.tar.gz 
      |-- snapshot.json
      |-- timestamp.json                  
|--+ keys                                       # 镜像私钥（可移动到其他位置）
   |-- {hash1..hashN}-root.json                 # 根证书私钥
   |-- {hash}-index.json                        # 索引私钥
   |-- {hash}-snapshot.json                     # 快照私钥
   |-- {hash}-timestamp.json                    # 时间戳私钥
```

### 镜像根证书

在 TiUP 镜像中，根证书用于存放其他元信息文件的公钥，每次获取到任何元信息文件（*.json）都需要根据其文件类型（root，index，snapshot，timestamp）在当前已安装的 root.json 中找到对应的公钥，然后用公钥验证其签名是否合法。

根证书文件格式如下：

```
{
    "signatures": [                                             # 每个元信息文件有一些列的签名，签名由该文件对应的几个私钥签出
        {
            "keyid": "{id-of-root-key-1}",                      # 第一个参与签名私钥的 ID，该 ID 由私钥对应的公钥内容哈希得到
            "sig": "{signature-by-root-key-1}"                  # 该私钥对此文件 signed 部分签名的结果
        },
        ...
        {
            "keyid": "{id-of-root-key-N}",                      # 第 N 个参与签名私钥的 ID
            "sig": "{signature-by-root-key-N}"                  # 该私钥对此文件 signed 部分签名的结果
        }
    ],
    "signed": {                                                 # 被签名的部分
        "_type": "root",                                        # 该字段说明本文件的类型，root.json 的类型就是 root
        "expires": "{expiration-date-of-this-file}",            # 该文件的过期时间，过期后客户端会拒绝此文件
        "roles": {                                              # root.json 中的 roles 用来记录对各个元文件签名的密钥
            "{role:index,root,snapshot,timestamp}": {           # 涉及到的元文件由 index, root, snapshot, timestamp
                "keys": {                                       # 只有 keys 中记录的密钥签名才是合法的
                    "{id-of-the-key-1}": {                      # 用于签名 {role} 的第 1 个密钥 ID
                        "keytype": "rsa",                       # 密钥类型，目前固定为 rsa
                        "keyval": {                             # 密钥的 payload
                            "public": "{public-key-content}"    # 表示公钥内容
                        },
                        "scheme": "rsassa-pss-sha256"           # 目前固定为 rsassa-pss-sha256
                    },
                    "{id-of-the-key-N}": {                      # 用于签名 {role} 的第 N 个密钥 ID
                        "keytype": "rsa",
                        "keyval": {
                            "public": "{public-key-content}"
                        },
                        "scheme": "rsassa-pss-sha256"
                    }
                },
                "threshold": {N},                               # threshold 指示该元文件需要至少 N 个密钥签名
                "url": "/{role}.json"                           # url 是指该文件的获取地址，对于 index 文件，需要在前面加上版本号，即 /{N}.index.json
            }
        },
        "spec_version": "0.1.0",                                # 本文件遵循的规范版本，未来变更文件结构需要升级版本号，目前为 0.1.0
        "version": {N}                                          # 本文件的版本号，每次更新文件需要创建一个新的 {N+1}.root.json，并将其 version 设置为 N + 1
    }
}
```

## 索引

索引文件记录了镜像中所有的组件已经组件的所有者信息。

其格式如下：

```
{
    "signatures": [                                             # 该文件的签名
        {
            "keyid": "{id-of-index-key-1}",                     # 第一个参与签名的 key 的 ID
            "sig": "{signature-by-index-key-1}",                # 该私钥对此文件 signed 部分签名的结果
        },
        ...
        {
            "keyid": "{id-of-root-key-N}",                      # 第 N 个参与签名私钥的 ID
            "sig": "{signature-by-root-key-N}"                  # 该私钥对此文件 signed 部分签名的结果
        }
    ],
    "signed": {
        "_type": "index",                                       # 指示该文件类型
        "components": {                                         # 组件列表
            "{component1}": {                                   # 第一个组件的名称
                "hidden": {bool},                               # 是否是隐藏组件
                "owner": "{owner-id}",                          # 组件所有者 ID
                "standalone": {bool},                           # 该组件是否可独立运行
                "url": "/{component}.json",                     # 获取组件的地址，需要加上版本号：/{N}.{component}.json
                "yanked": {bool}                                # 该组件是否已被标记为删除 
            },
            ...
            "{componentN}": {                                   # 第 N 个组件的名称
                ...
            },
        },
        "default_components": ["{component1}".."{componentN}"], # 镜像必须包含的默认组件，该字段目前固定为空（未启用）
        "expires": "{expiration-date-of-this-file}",            # 该文件的过期时间，过期后客户端会拒绝此文件
        "owners": {
            "{owner1}": {                                       # 第一个属主的 ID
                "keys": {                                       # 只有 keys 中记录的密钥签名才是合法的
                    "{id-of-the-key-1}": {                      # 该属主的第一个密钥
                        "keytype": "rsa",                       # 密钥类型，目前固定为 rsa
                        "keyval": {                             # 密钥的 payload
                            "public": "{public-key-content}"    # 表示公钥内容
                        },
                        "scheme": "rsassa-pss-sha256"           # 目前固定为 rsassa-pss-sha256
                    },
                    ...
                    "{id-of-the-key-N}": {                      # 该属主的第 N 个密钥
                        ...
                    }
                },
                "name": "{owner-name}",                         # 该属主的名字
                "threshod": {N}                                 # 指示该属主拥有的组件必须含有至少 N 个合法签名
            },
            ...
            "{ownerN}": {                                       # 第 N 个属主的 ID
                ...
            }
        }
        "spec_version": "0.1.0",                                # 本文件遵循的规范版本，未来变更文件结构需要升级版本号，目前为 0.1.0
        "version": {N}                                          # 本文件的版本号，每次更新文件需要创建一个新的 {N+1}.index.json，并将其 version 设置为 N + 1
    }
}
```