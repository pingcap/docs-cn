# 如何在你的 GitHub 个人主页上添加 TiDB 文档挑战赛徽章

[GitHub 个人主页](https://docs.github.com/zh/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/about-your-profile)不仅仅是你的 GitHub 仓库的集合，更是你在编程领域中的专业身份标志。

本指南介绍如何在你的 GitHub 个人主页上添加 TiDB 文档挑战赛 (TiDB Docs Dash) 活动徽章的详细步骤。

## 第 1 步：创建一个仓库，存放个人主页 README

如果您已经配置了 GitHub 个人主页 README，请跳过以下步骤，直接进入[第二步：编辑您的个人资料 README](#step-2-edit-your-profile-readme)。

1. 在 GitHub 任一页面的右上角，点击 **+**，然后点击 **New repository**。

    <img src="https://docs.github.com/assets/cb-34248/mw-1440/images/help/repository/repo-create-global-nav-update.webp" width="350" />

2. 以你的 GitHub 用户名命名该仓库。例如，如果你的用户名为 `ilovetidb`，则仓库名必须为 `ilovetidb`。
3. 选择 **Public** 将该仓库设置为公共可见。
4. 在 **Initialize this repository with:** 下，选择 **Add a README file**。
5. 点击 **Create repository**。

## 第 2 步：编辑个人主页 README

1. 在你的 `<github_username>` 仓库的 GitHub 页面上，点击右侧边栏上方的 **Edit README**。
2. 在 README 文件中添加以下代码，并将 `{{github_username}}` 替换为你的用户名，然后提交更改。

    ```HTML
    <p>
      <img src="https://api.vaunt.dev/v1/github/entities/{{github_username}}/achievements?format=svg&limit=3" width="350" />
    </p>
    ```

 此时，刷新你的 GitHub 个人主页，即可看到 TiDB Docs Dash 徽章。关于如何管理个人主页 README 的更多信息，请参阅 [GitHub 文档](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme)。

## （可选）通过 Vaunt 添加其他展示

本次 TiDB 文档挑战赛的徽章是通过 [Vaunt](https://vaunt.dev/) 授予的。Vaunt 是一个开发者关系平台，旨在赋能和发展开发者社区。

通过 Vaunt 提供的以下功能，你还可以在你的个人主页 README 中展示你在其他开源项目中的贡献：

- 集成你的 developer card 到个人主页 README

    示例卡片:

    <p>
        <a href="https://vaunt.dev">
            <img src="https://api.vaunt.dev/v1/github/entities/jeff1010322/contributions?format=svg" width="350" />
        </a>
    </p>

    如需集成你的 developer card，请将以下代码添加到你的 README 文件中，并将 `{{github_username}}` 替换为你的用户名。


    ```HTML
    <p>
        <a href="https://vaunt.dev">
            <img src="https://api.vaunt.dev/v1/github/entities/{{github_username}}/contributions?format=svg" width="350" />
        </a>
    </p>
    ```

- 集成你的社区贡献看板到个人主页 README

    社区贡献看板可以通过视图综合展示你在 GitHub 的贡献统计数据。

    [![VauntCommunity](https://api.vaunt.dev/v1/github/entities/pingcap/badges/community)](https://community.vaunt.dev/board/pingcap)

    - 查看[你的社区看板](https://community.vaunt.dev/).
    - 如需集成你的社区看板，请将以下代码添加到你的 README 文件中，并将 `{{github_username}}` 替换为你的用户名：

    ```Markdown
    [![VauntCommunity](https://api.vaunt.dev/v1/github/entities/{{github_username}}/badges/community)](https://community.vaunt.dev/board/{{github_username}})
    ```
