---
title: tiup mirror init
---

# tiup mirror init

命令 `tiup mirror init` 用于初始化一个空的镜像。初始化的镜像不包含任何组件和组件管理员，仅生成以下文件：

```
+ <mirror-dir>                                  # 镜像根目录
|-- root.json                                   # 镜像根证书
|-- 1.index.json                                # 组件/用户索引
|-- snapshot.json                               # 镜像最新快照
|-- timestamp.json                              # 镜像最新时间戳                 
|--+ keys                                       # 镜像私钥（可移动到其他位置）
   |-- {hash1..hashN}-root.json                 # 根证书私钥
   |-- {hash}-index.json                        # 索引私钥
   |-- {hash}-snapshot.json                     # 快照私钥
   |-- {hash}-timestamp.json                    # 时间戳私钥
```

以上文件的具体作用及内容格式请参考[镜像说明](/tiup/tiup-mirror-reference.md)。

## 语法

```shell
tiup mirror init <path> [flags]
```

`<path>` 为本地目录路径，可以为相对路径。TiUP 会以此路径为镜像文件存放路径，在其中生成文件。若该目录已存在，则必须保证为空，若该目录不存在，则 TiUP 会自动创建。

## 选项

### -k, --key-dir（string，默认 {path}/keys）

指定生成私钥文件的目录。若指定的文件目录不存在，则会自动创建。

### 输出

- 若成功：无输出
- 若 `<path>` 不为空：`Error: the target path '%s' is not an empty directory`
- 若 `<path>` 不是目录：`Error: fdopendir: not a directory`

[<< 返回上一页 - TiUP Mirror 命令清单](/tiup/tiup-component-mirror.md#命令清单)