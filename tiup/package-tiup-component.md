---
title: Package a Component
summary: Learn how to package a component.
category: tools
aliases: ['/docs/dev/reference/tools/tiup/package-component/']
---

# Package a Component

If you want to add a new component or add a version of an existing component, use the `tar` command to package the component files and then upload these packaged files to the mirror repository. Packaging with `tar` is not difficult. However, it is not easy to update the meta information of the repository without destroying the information of existing components.

To make it easy, TiUP provides the `package` component, which is used to package the newly added TiUP component and generate the directory of this component.

## TiUP `package` overview

Execute the following command to get the help information of the `mirrors` component:

{{< copyable "shell-root" >}}

```bash
tiup package --help
```

```
Package a tiup component and generate package directory

Usage:
  tiup package target [flags]

Flags:
  -C, -- string          Change directory before compress
      --arch string      Target ARCH of the package (default "GOARCH")
      --desc string      Description of the package
      --entry string     Entry point of the package
  -h, --help             help for tiup
      --hide tiup list   Don't show the component in tiup list
      --name string      Name of the package
      --os string        Target OS of the package (default "GOOS")
      --release string   Version of the package
      --standalone       Can the component run standalone
```

## Usage example: Add the `Hello World` component

This section introduces the development and packaging process of the `Hello World` component. The only function of this component is to output the content of its configuration file. The content is "Hello World".

To make it simple, the bash script is used to develop this component. See the following steps for details:

1. Create the configuration file of the `Hello World` component. The content of this file is "Hello World".

    {{< copyable "shell-regular" >}}

    ```shell
    cat > config.txt << EOF
    Hello World
    EOF
    ```

2. Create an executable file:

    {{< copyable "shell-regular" >}}

    ```shell
    cat > hello.sh << EOF
    #! /bin/sh
    cat \${TIUP_COMPONENT_INSTALL_DIR}/config.txt
    EOF

    chmod 755 hello.sh
    ```

    The `TIUP_COMPONENT_INSTALL_DIR` environment variable is passed in when TiUP is running. This variable points to the installation directory of the component.

3. Refer to [Create a Private Mirror](/tiup/tiup-mirrors.md) and create an offline or a private mirror accordingly. Make sure the `TIUP_MIRRORS` variable points to the mirror after this mirror is created.

    > **Note:**
    >
    > You cannot publish your package, because the `publish` feature of the official mirror is currently unavailable.

4. Packaging:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup package hello.sh config.txt --name=hello --entry=hello.sh --release=v0.0.1
    ```

    A `package` directory is created in this step. The packaged files and the meta information are stored in this directory.

5. Upload the packaged files to the repository:

    You can upload the packaged files only to the mirror created by yourself in step 3, because currently you cannot publish the files to the official repository. Execute the following command to copy all files in the `package` directory into `<target-dir>`. For details of `<target-dir>`, refer to the [`mirrors` description](/tiup/tiup-mirrors.md#mirrors-description).

    {{< copyable "shell-regular" >}}

    ```bash
    cp package/* path/to/mirror/
    ```

    If the directory created in step 3 happens to be in the current directory and the directory name happens to be `package`, you do not need to copy the files manually.

6. Check whether the `Hello World` component is created successfully:

    {{< copyable "shell-root" >}}

    ```bash
    tiup list hello
    ```

    ```
    Available versions for hello (Last Modified: 2020-04-23T16:45:53+08:00):
    Version  Installed  Release:                   Platforms
    -------  ---------  --------                   ---------
    v0.0.1              2020-04-23T16:51:41+08:00  darwin/amd64
    ```

    {{< copyable "shell-root" >}}

    ```bash
    tiup hello
    ```

    ```
    The component `hello` is not installed; downloading from repository.
    Starting component `hello`: /Users/joshua/.tiup/components/hello/v0.0.1/hello.sh
    Hello World
    ```
