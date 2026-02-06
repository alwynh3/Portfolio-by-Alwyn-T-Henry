# How to Deploy Your Portfolio

To share your portfolio with the world, the best free option is **GitHub Pages**. Here is how to do it:

## Prerequisite: GitHub Account
If you don't have one, create an account at [github.com](https://github.com).

## Step 1: Create a New Repository
1.  Log in to GitHub.
2.  Click the **+** icon in the top right and select **New repository**.
3.  Name it `portfolio` (or anything you like).
4.  Make sure it is **Public**.
5.  **Do not** initialize with README, .gitignore, or License (we already have your files ready).
6.  Click **Create repository**.

## Step 2: Push Your Code
I have already initialized Git for you locally. Now you just need to connect it to GitHub.
Run these commands in your terminal (copy and paste the lines GitHub gives you under "…or push an existing repository from the command line"):

```bash
git remote add origin https://github.com/YOUR_USERNAME/portfolio.git
git branch -M main
git push -u origin main
```
*(Replace `YOUR_USERNAME` with your actual GitHub username)*

## Step 3: Activate GitHub Pages
1.  Go to your repository **Settings** tab.
2.  Scroll down to the **Pages** section (on the left sidebar).
3.  Under **Source**, select `Deploy from a branch`.
4.  Under **Branch**, select `main` and `/ (root)`.
5.  Click **Save**.

## Step 4: Share!
GitHub will take a minute to build your site. Once done, it will give you a link like:
`https://your-username.github.io/portfolio/`

You can send this link to anyone!
