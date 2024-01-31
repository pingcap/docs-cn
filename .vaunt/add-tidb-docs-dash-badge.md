# How to Add TiDB Docs Dash Badges to Your GitHub Profile

Your [GitHub profile](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/about-your-profile) is more than just a collection of repositories; it is your professional identity in the coding world.

This guide walks you through the steps of adding [TiDB Docs Dash 2024](https://www.pingcap.com/event/tidb-docs-dash/) badges to your GitHub profile.

## Step 1. Create a repository for your profile README

If you have already set up your GitHub profile README, skip the following and go to [Step 2. Edit your profile README](#step-2-edit-your-profile-readme).

1. In the upper-right corner of any GitHub page, click **+**, and then click **New repository**.

    <img src="https://docs.github.com/assets/cb-34248/mw-1440/images/help/repository/repo-create-global-nav-update.webp" width="350" />

2. Type a repository name that matches your GitHub username. For example, if your username is `ilovetidb`, the repository name must be `ilovetidb`.
3. Choose **Public** for the repository visibility.
4. Under **Initialize this repository with:**, select **Add a README file**.
5. Click **Create repository**.

## Step 2. Edit your profile README

1. On the GitHub page of your `<github_username>` repository, click **Edit README** above the right sidebar.
2. Add the following code to your README file, replace `{{github_username}}` with your username, and commit the changes directly.

    ```HTML
    <p>
      <img src="https://api.vaunt.dev/v1/github/entities/{{github_username}}/achievements?format=svg&limit=3" width="350" />
    </p>
    ```

 Your GitHub profile now displays your TiDB Docs Dash badge. For more information about managing your profile README, see [GitHub docs](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme).

## (Optional) Explore more with Vaunt

TiDB Docs Dash badges are granted via [Vaunt](https://vaunt.dev/), a developer relations platform that aims to empower and grow developer communities.

You can use additional Vaunt features to showcase your contributions to other open source projects as follows:

- Integrate your developer card

    Example card:

    <p>
        <a href="https://vaunt.dev">
            <img src="https://api.vaunt.dev/v1/github/entities/jeff1010322/contributions?format=svg" width="350" />
        </a>
    </p>

    To integrate your developer card, add the following code to your README file and replace `{{github_username}}` with your username.

    ```HTML
    <p>
        <a href="https://vaunt.dev">
            <img src="https://api.vaunt.dev/v1/github/entities/{{github_username}}/contributions?format=svg" width="350" />
        </a>
    </p>
    ```

- Integrate your community boards

    The community boards provide community statistics, repository insights, and a view into repository achievements.

    [![VauntCommunity](https://api.vaunt.dev/v1/github/entities/pingcap/badges/community)](https://community.vaunt.dev/board/pingcap)

    - Explore [your own community boards](https://community.vaunt.dev/).
    - Add the following code to your README file and replace `{{github_username}}` with your username:

    ```Markdown
    [![VauntCommunity](https://api.vaunt.dev/v1/github/entities/{{github_username}}/badges/community)](https://community.vaunt.dev/board/{{github_username}})
    ```
