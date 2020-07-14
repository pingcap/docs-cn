---
title: TiUP Terminology and Concepts
summary: Explain the terms and concepts of TiUP.
aliases: ['/docs/dev/tiup/tiup-terminology-and-concepts/']
---

# TiUP Terminology and Concepts

This document explains important terms and concepts of TiUP.

## TiUP components

The TiUP program contains only a few commands for downloading, updating, and uninstalling components. TiUP expands its functions with various components. A **component** is a program or script that can be run. When running a component through `tiup <component>`, TiUP adds a set of environment variables, creates the data directory for the program, and then runs the program.

By running the `tiup <component>` command, you can run a component supported by TiUP. The running logic is:

+ If you specify a version of a component through `tiup <component>[:version]`:

    - If the component does not have any version installed locally, TiUP downloads the latest stable version from the mirror server.
    - If the component has one or more versions installed locally, but there is no version specified by you, TiUP downloads the specified version from the mirror server.
    - If the specified version of the component is installed locally, TiUP sets the environment variable to run the installed version.

+ If you run a component through `tiup <component>` and specify no version:

    - If the component does not have any version installed locally, TiUP downloads the latest stable version from the mirror server.
    - If one or more versions have been installed locally, TiUP sets the environment variable to run the latest installed version.

## TiUP mirrors

All components of TiUP are downloaded from the TiUP mirrors. TiUP mirrors contain the TAR package of each component and the corresponding meta information (version, entry startup file, checksum). TiUP uses PingCAP's official mirrors by default. You can customize the mirror source through the `TIUP_MIRRORS` environment variable.

TiUP mirrors can be a local file directory or an online HTTP server:

+ `TIUP_MIRRORS=/path/to/local tiup list`
+ `TIUP_MIRRORS=https://private-mirrors.example.com tiup list`
