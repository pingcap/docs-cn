---
title: Figma 快速上手教程
summary: 本文档介绍如何使用 Figma 绘制图片。
---

# Figma 快速上手教程

[Figma](https://www.figma.com/) 是一款免费的在线绘图工具，支持多人实时协作，简单实用、易于上手，Windows 和 macOS 等平台均可使用。本文档介绍如何使用 Figma 绘制图片。

## Figma 快速上手

执行以下步骤可使用 Figma 快速绘制图片。

> **注意：**
>
> 本文档中的快捷键仅适用于 macOS 平台用户。关于 macOS 及 Windows 平台的所有快捷键，参见 [Figma 快捷键](https://www.figma.com/file/ewSrIu24UagGV8JN4kQNNzMH/KEYBOARD-SHORTCUTS?node-id=0%3A1)。

### 第 1 步：创建账号

访问 [Figma 官网](https://www.figma.com/)，点击 **Sign up** 创建账号。

> **注意：**
>
> 如果已有 Google 账号，点击 **Sign up with Google** 即可使用已有账号登录。

![登录](/media/figma-guide/sign-up.png)

### 第 2 步：打开 tidb-sketch-book 文件

点击 [tidb-sketch-book](https://www.figma.com/file/hNoQeZdKbqQ6gwyOy5cmLz/tidb-sketch-book-2020-2.0) 查看该绘图模板文件。

> **注意：**
>
> - **tidb-sketch-book** 文件包含绘图时常用的各种图形。绘图时，建议使用该文件中的图形元素和配色，以保持图片风格统一。
> - 如果不能打开该文件，请联系 [Jingyi Chen](mailto:chenjingyi@pingcap.com)。

![tidb-sketch-book](/media/figma-guide/tidb-sketch-book.png)

### 第 3 步：创建 Frame

1. 点击 **Back to Files** 查看可浏览或可编辑的文件。

    ![Back to Files](/media/figma-guide/back-to-files.png)

    ![Recently viewed](/media/figma-guide/recently-viewed.png)

2. 右击 tidb-sketch-book，选择 **Duplicate**，可生成新文件 **tidb-sketch-book (Copy)**。

    ![Duplicate](/media/figma-guide/duplicate.png)

    ![tidb-sketch-book (Copy)](/media/figma-guide/tidb-sketch-book-copy.png)

3. 右击 **tidb-sketch-book (Copy)** 文件，选择 **Rename** 修改文件名称。本示例中，文件更名为 figma-test。

    ![Rename](/media/figma-guide/rename.png)

    ![figma-test](/media/figma-guide/figma-test.png)

4. 双击更名后的文件。选择 **Frame** 工具 (F)，在屏幕中拖动鼠标生成一个 Frame（画框）。本示例中，生成 Frame 19。

    选中一个 Frame，使用快捷键 <kbd>Shift</kbd>+<kbd>Command</kbd>+<kbd>G</kbd>，可删除该 Frame。

    ![Frame](/media/figma-guide/frame.png)

    ![新 Frame](/media/figma-guide/new-frame.png)

之后便可在这个 Frame 中开始绘图。

### 第 4 步：绘制图片

建议将其他 Frame 中已有的图形复制、粘贴到新的 Frame 中，以便快速绘制图片。

> **注意：**
>
> * 为确保图片风格统一，请**按照 tidb-sketch-book 文件中的图形和配色方案**绘制图片。
> * 除非特殊原因，**请勿使用中文字符**，以免产出英文文章时需重新绘图。
> * 英文字体：**Ubuntu**；中文字体：**思源雅黑**。

#### 取色

1. 选中图形，点击右侧属性栏中 Design 选项卡的 Fill 选项打开拾色器。

    ![Fill](/media/figma-guide/fill.png)

2. 为了准确取到某个像素点的颜色，点击 Fill 中的颜色小卡片，再点击弹出的颜色选择器中的吸管工具，即可调出吸管工具（快捷键：<kbd>I</kbd> 或者 <kbd>Ctrl</kbd>+<kbd>C</kbd>）。

    ![吸管工具](/media/figma-guide/eyedropper.png)

3. 使用吸管工具吸取对应像素色块的颜色，放大镜窗口会显示取样像素的颜色和 hex 编码。

    ![放大镜窗口](/media/figma-guide/magnifier-window.png)

#### 复制并粘贴对象

1. 选中待编辑的对象，使用快捷键 <kbd>Command</kbd>+<kbd>C</kbd> 复制对象。

2. 选中目标 Frame，使用快捷键 <kbd>Command</kbd>+<kbd>V</kbd> 粘贴对象。

#### 复制并粘贴多个对象

1. 在图层面板中选中待编辑的对象所在的图层，使用快捷键 <kbd>Command</kbd>+<kbd>C</kbd> 复制这些对象。

    ![Copy objects](/media/figma-guide/copy-objects.png)

2. 选中目标 Frame，使用快捷键 <kbd>Command</kbd>+<kbd>V</kbd> 将这些对象粘贴到当前 Frame。

#### 绘制圆角

选中待编辑的对象，在属性面板中调整 **Corner Radius** 值。

![Corner Radius](/media/figma-guide/corner-radius.png)

### 第 5 步：导出图片

1. 选中待导出的 Frame，点击 **Export** 一栏的 **+**。

    > **注意：**
    >
    > 可导出 Frame（推荐）、图层、一组对象，或多个图层。

    ![导出](/media/figma-guide/export.png)

2. 设置图片格式。可导出为 **PNG（推荐）**、JPG、SVG 或 PDF 格式。

    ![图片格式](/media/figma-guide/figure-format.png)

3. 点击 **Export Frame X** 按钮导出 Frame。

    ![Export Frame X](/media/figma-guide/export-frame-x.png)

4. 设置图片名称时，使用**描述性**名称。名称中可包含小写字母、数字及短连线 `-`。**请勿使用大写字母、空格、下划线**。

更多步骤见 Figma 官方文档。
