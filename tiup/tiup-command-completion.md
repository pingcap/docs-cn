---
title: tiup completion
---

# tiup completion

To reduce user costs, TiUP provides the `tiup completion` command to generate a configuration file for automatic command-line completion. Currently, TiUP supports completing `bash` and `zsh` commands.

If you want to complete `bash` commands, you need to install `bash-completion` first. See the following instructions:

- On macOS: If your bash version is earlier than 4.1, run `brew install bash-completion`; otherwise, run `brew install bash-completion@2`.
- On Linux: Use a package manager to install `bash-completion`. For example, run `yum install bash-completion` or `apt install bash-completion`.

## Syntax

```shell
tiup completion <shell>
```

`<shell>` is used to set the type of shell you use. Currently, `bash` and `zsh` are supported.

## Usage

### bash

Write the `tiup completion bash` command into a file and source the file in `.bash_profile`. See the following example:

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

[<< Back to the previous page - TiUP Reference command list](/tiup/tiup-reference.md#command-list)
