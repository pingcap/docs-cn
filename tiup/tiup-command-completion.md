---
title: tiup completion
---

# tiup completion

为了降低使用成本，TiUP 提供了 `tiup completion` 命令用于生成命令行自动补全的配置文件。目前支持 `bash` 和 `zsh` 两种 shell 的命令补全。

如果是 bash，需要提前安装好 bash-completion：

- 在 macOS 上的安装方式为：如果 bash 版本小于 4.1，执行 `brew install bash-completion`；如果 bash 版本大于等于 4.1，则执行 `brew install bash-completion@2`。
- 在 Linux 上的安装方式为：使用包管理器安装 `bash-completion` 包，例如执行 `yum install bash-completion` 或者 `apt install bash-completion`。

## 语法

```shell
tiup completion <shell>
```

`<shell>` 为 shell 类型，目前支持 `bash` 和 `zsh`。

## 使用方式

### bash

将自动补全代码写入一个文件，并且在 `.bash_profile` 中对其执行 `source` 命令：

```shell
tiup completion bash > ~/.tiup.completion.bash

printf "
# tiup shell completion
source '$HOME/.tiup.completion.bash'
" >> $HOME/.bash_profile

source $HOME/.bash_profile
```

### zsh

```shell
tiup completion zsh > "${fpath[1]}/_tiup"
```
