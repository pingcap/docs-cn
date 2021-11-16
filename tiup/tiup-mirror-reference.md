---
title: TiUP 镜像参考指南
---

# TiUP 镜像参考指南

TiUP 镜像是 TiUP 的组件仓库，存放了一系列的组件和这些组件的元信息。镜像有两种存在形式：

- 本地磁盘上的目录：用于服务本地的 TiUP 客户端，文档中将称之为本地镜像
- 基于远程的磁盘目录启动的 HTTP 镜像：服务远程的 TiUP 客户端，文档中将称之为远程镜像

## 镜像的创建与更新

镜像可以通过以下两种方式创建：

- 通过命令 `tiup mirror init` 从零生成
- 通过命令 `tiup mirror clone` 从已有镜像克隆

在创建镜像之后，可以通过 `tiup mirror` 相关命令来给镜像添加组件或删除组件，无论是通过何种方式更新镜像，TiUP 都不会从镜像中删除任何文件，而是通过增加文件并分配新版本号的方式更新。

## 镜像结构

一个典型的镜像目录结构如下：

```
+ <mirror-dir>                                  # 镜像根目录
|-- root.json                                   # 镜像根证书
|-- {2..N}.root.json                            # 镜像根证书
|-- {1..N}.index.json                           # 组件/用户索引
|-- {1..N}.{component}.json                     # 组件元信息
|-- {component}-{version}-{os}-{arch}.tar.gz    # 组件二进制包
|-- snapshot.json                               # 镜像最新快照
|-- timestamp.json                              # 镜像最新时间戳
|--+ commits                                    # 镜像更新日志（可删除）
   |--+ commit-{ts1..tsN}
      |-- {N}.root.json
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

> **注意：**
>
> + commits 目录是在更新镜像过程中产生的日志，用于回滚镜像，磁盘空间不足时可以定期删除旧的文件夹
> + keys 文件夹中存放的私钥较敏感，建议单独妥善保管

### 根证书

在 TiUP 镜像中，根证书用于存放其他元信息文件的公钥，每次获取到任何元信息文件（*.json）都需要根据其文件类型（root，index，snapshot，timestamp）在当前已安装的 root.json 中找到对应的公钥，然后用公钥验证其签名是否合法。

根证书文件格式如下：

```
{
    "signatures": [                                             # 每个元信息文件有一系列的签名，签名由该文件对应的几个私钥签出
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
            "{role:index,root,snapshot,timestamp}": {           # 涉及的元文件类型包括 index, root, snapshot, timestamp
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

### 索引

索引文件记录了镜像中所有的组件以及组件的所有者信息。

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
                "owner": "{owner-id}",                          # 组件管理员 ID
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

### 组件

组件元信息文件记录了特定组件的平台以及版本信息。

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
        "_type": "component",                                   # 指示该文件类型
        "description": "{description-of-the-component}",        # 该组件的描述信息
        "expires": "{expiration-date-of-this-file}",            # 该文件的过期时间，过期后客户端会拒绝此文件
        "id": "{component-id}",                                 # 该组件的 ID，具有全局唯一性
        "nightly": "{nightly-cursor}",                          # nightly 游标，值为最新的 nightly 的版本号（如 v5.0.0-nightly-20201209）
        "platforms": {                                          # 该组件支持的平台（如 darwin/amd64，linux/arm64 等）
            "{platform-pair-1}": {
                "{version-1}": {                                # Semantic Version 版本号（如 v1.0.0 等）
                    "dependencies": null,                       # 用于约定组件之间的依赖关系，该字段尚未使用，固定为 null
                    "entry": "{entry}",                         # 入口二进制文件位于 tar 包的相对路径
                    "hashs": {                                  # tar 包的 checksum，我们使用 sha256 和 sha512
                        "sha256": "{sum-of-sha256}",
                        "sha512": "{sum-of-sha512}",
                    },
                    "length": {length-of-tar},                  # tar 包的长度
                    "released": "{release-time}",               # 该版本的 release 时间
                    "url": "{url-of-tar}",                      # tar 包的下载地址
                    "yanked": {bool}                            # 该版本是否已被禁用
                }
            },
            ...
            "{platform-pair-N}": {
                ...
            }
        },
        "spec_version": "0.1.0",                                # 本文件遵循的规范版本，未来变更文件结构需要升级版本号，目前为 0.1.0
        "version": {N}                                          # 本文件的版本号，每次更新文件需要创建一个新的 {N+1}.{component}.json，并将其 version 设置为 N + 1
}
```

### 快照

快照文件记录了各个元文件当前的版本号。

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
        "_type": "snapshot",                                    # 指示该文件类型
        "expires": "{expiration-date-of-this-file}",            # 该文件的过期时间，过期后客户端会拒绝此文件
        "meta": {                                               # 其他元文件的信息
            "/root.json": {
                "length": {length-of-json-file},                # root.json 的长度
                "version": {version-of-json-file}               # root.json 的 version
            },
            "/index.json": {
                "length": {length-of-json-file},
                "version": {version-of-json-file}
            },
            "/{component-1}.json": {
                "length": {length-of-json-file},
                "version": {version-of-json-file}
            },
            ...
            "/{component-N}.json": {
                ...
            }
        },
        "spec_version": "0.1.0",                                # 本文件遵循的规范版本，未来变更文件结构需要升级版本号，目前为 0.1.0
        "version": 0                                            # 本文件的版本号，固定为 0
    }
```

### 时间戳

时间戳文件记录了当前快照 checksum。

其文件格式如下：

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
        "_type": "timestamp",                                   # 指示该文件类型
        "expires": "{expiration-date-of-this-file}",            # 该文件的过期时间，过期后客户端会拒绝此文件
        "meta": {                                               # snapshot.json 的信息
            "/snapshot.json": {
                "hashes": {
                    "sha256": "{sum-of-sha256}"                 # snapshot.json 的 sha256
                },
                "length": {length-of-json-file}                 # snapshot.json 的长度
            }
        },
        "spec_version": "0.1.0",                                # 本文件遵循的规范版本，未来变更文件结构需要升级版本号，目前为 0.1.0
        "version": {N}                                          # 本文件的版本号，每次更新文件需要覆盖 timestamp.json，并将其 version 设置为 N + 1
```

## 客户端工作流程

客户端通过以下逻辑保证从镜像下载到的文件是安全的：

+ 客户端安装时随 binary 附带了一个 root.json
+ 客户端运行时以已有的 root.json 为基础，做如下操作：
    1. 获取 root.json 中的 version，记为 N
    2. 向镜像请求 {N+1}.root.json，若成功，使用 root.json 中记录的公钥验证该文件是否合法
+ 向镜像请求 timestamp.json，并使用 root.json 中记录的公钥验证该文件是否合法
+ 检查 timestamp.json 中记录的 snapshot.json 的 checksum 和本地的 snapshot.json 的 checksum 是否吻合
    - 若不吻合，则向镜像请求最新的 snapshot.json 并使用 root.json 中记录的公钥验证该文件是否合法
+ 对于 index.json 文件，从 snapshot.json 中获取其版本号 N，并请求 {N}.index.json，然后使用 root.json 中记录的公钥验证该文件是否合法
+ 对于组件（如 tidb.json，tikv.json），从 snapshot.json 中获取其版本号 N，并请求 {N}.{component}.json，然后使用 index.json 中记录的公钥验证该文件是否合法
+ 对于组件 tar 文件，从 {component}.json 中获取其 url 及 checksum，请求 url 得到 tar 包，并验证 checksum 是否正确
