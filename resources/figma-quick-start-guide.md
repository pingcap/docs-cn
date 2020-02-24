---
title: Figma Quick Start Guide
summary: This guide introduces how to use Figma to design a figure.
---

# Figma Quick Start Guide

[Figma](https://www.figma.com/) is a collaborative interface design tool that runs in a browser. This guide introduces how to use Figma to design a figure.

## The Figma interface

For details, see the [Figma tutorial](https://help.figma.com/article/12-getting-familiar-with-figma).

## Get started with Figma

Perform the following steps to get started with Figma.

> **Note:**
>
> The keyboard shortcuts demonstrated in this document are only for macOS users. For more keyboard shortcuts on macOS and Windows, see [Figma keyboard shortcuts](https://www.figma.com/file/ewSrIu24UagGV8JN4kQNNzMH/KEYBOARD-SHORTCUTS?node-id=0%3A1).

### Step 1: Create an account

Go to [https://www.figma.com/](https://www.figma.com/) and click **Sign up** to create an account.

> **Note:**
>
> If you have a Google account, you can click **Sign up with Google** to log in with the existing Google account.

![Sign up](/media/sign-up.png)

### Step 2: Open the tidb-sketch-book file

Click [tidb-sketch-book](https://www.figma.com/file/MOBwqkBtuA03agMjeGEGUT/tidb-sketch-book) to view the template.

> **Note:**
>
> - **tidb-sketch-book** is a Figma file that collects common shapes for figure designs. When creating a figure, you are recommended to use the objects and colors in this file to maintain a consistent style for figures.
> - If you cannot open this file, contact [Jingyi Chen](mailto:chenjingyi@pingcap.com) for help.

![tidb-sketch-book](/media/tidb-sketch-book.png)

### Step 3: Create a Frame

1. Click **Back to Files** to see the files you can view or edit.

    ![Back to Files](/media/back-to-files.png)

    ![Recently viewed](/media/recently-viewed.png)

2. Right-click on the file and select **Duplicate**. You will get a new file named **tidb-sketch-book (Copy)**.

    ![Duplicate](/media/duplicate.png)

    ![tidb-sketch-book (Copy)](/media/tidb-sketch-book-copy.png)

3. Right-click on the **tidb-sketch-book (Copy)** file and select **Rename** to alter its name. In this example, the file is renamed as figma-test.

    ![Rename](/media/rename.png)

    ![figma-test](/media/figma-test.png)

4. Double-click the file you renamed just now. Choose the **Frame** tool (F) and drag out an area of the screen to make a new Frame. In this example, Frame 19 is created.

    To delete a frame, choose the frame and then press <kbd>Shift</kbd>+<kbd>Command</kbd>+<kbd>G</kbd>.

    ![Frame](/media/frame.png)

    ![New Frame](/media/new-frame.png)

Within this Frame, you can begin your designs.

### Step 4: Design your figure

You are recommended to copy and paste the existing objects within other Frames into the new Frame.

> **Note:**
>
> * To ensure a consistent style for figures, design a figure **based on shapes and the color scheme in the tidb-sketch-book file**.
> * Set text fonts to **Ubuntu**.

#### Pick a color

1. Select an object and click the **Fill** value in the properties panel to open the color picker.

    ![Fill](/media/fill.png)

2. Click the eyedropper tool icon (keyboard shortcuts: <kbd>I</kbd> or <kbd>Ctrl</kbd>+<kbd>C</kbd>) next to the slider to open the eyedropper tool.

    ![Eyedropper](/media/eyedropper.png)

3. Use the eyedropper to hover over the color in the Frame you want to sample. The magnifier window will show you both the color and hex code of the sampled pixel.

    ![Magnifier window](/media/magnifier-window.png)

#### Copy and paste an object

1. Select the object you want to edit and press <kbd>Command</kbd>+<kbd>C</kbd> to copy it.

2. Select the target Frame and press <kbd>Command</kbd>+<kbd>V</kbd> to paste the object.

#### Copy and paste multiple objects

1. Select the layers you want to edit in the layers panel and press <kbd>Command</kbd>+<kbd>C</kbd> to copy these objects.

    ![Copy objects](/media/copy-objects.png)

2. Select the target Frame and press <kbd>Command</kbd>+<kbd>V</kbd> to paste the objects into the current Frame.

#### Round corners

Select the object you want to edit and adjust the **Corner Radius** value in the properties panel.

![Corner Radius](/media/corner-radius.png)

#### Other operations

See the [Figma user guide](https://help.figma.com/category/9-getting-started).

### Step 5: Export a figure

1. Select the Frame you want to export and click **+** next to the **Export** settings.

    > **Note:**
    >
    > You can export a Frame (recommended), a layer, a group, or multiple layers.

    ![Export](/media/export.png)

2. Set the figure format. You can export to **PNG (recommended)**, JPG, SVG, or PDF.

    ![Figure format](/media/figure-format.png)

3. Click the **Export Frame X** button below **PNG** to export your figure.

    ![Export Frame X](/media/export-frame-x.png)

4. Use a **descriptive** name for the figure. You can use lowercase characters, numbers, and hyphens `-` in the name. **Avoid using uppercase characters, spaces, and underscores**.
