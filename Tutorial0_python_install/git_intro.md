# Introduction to GIT

This repository is a basic introduction to GIT. It explains how you can create a repository, clone it to your local machine, and push your changes to the remote repository on github.com. There is also an introduction to creating a new branch and a pull request. At the end, there is an overview of the most essential git commands. 

## What is GitHub?

GitHub is a version control and collaboration platform built around Git, a distributed version control system. 
It allows multiple people to work on projects (code, documentation, etc.) simultaneously while keeping track of changes made over time. 
GitHub also acts as a repository where you can publish your code, collaborate with others, and manage project-related tasks.

## How to install GitHub?

GitHub is already installed on Climcal and generally on Linux/MacOS, but if it is not available on your local machine, install it following the steps below:

**For Windows:**
- Download Git from the official site: https://git-scm.com/download/win.
- Run the installer. During installation, you can keep most of the default options. Pay attention to the option "Use Git from the command line" to ensure that Git is accessible from your terminal.

**For macOS:**

You can install Git via the command line using Homebrew (if installed) or directly.
1. Open Terminal.
2. Run the following command to install Git via Homebrew:
```
brew install git
```
Alternatively, install Xcode Command Line Tools, which includes Git:
```
xcode-select --install
```

**For Linux (Debian/Ubuntu):**

1. Open a terminal.
2. Update your package list:
```
sudo apt update
```
3. Install Git:
```
sudo apt install git
```

After the installation, add your username and email to the configuration:
```
git config --global user.name {your username}
git config --global user.email {your email}
```

## How to get help?
In the [official documentaion](https://docs.github.com/en) or using command line tools:
```
man git
git help
git {command} -h
```

## How to create a repository?

Go to github.com and log in with your credentials. Go to your dashboard or the repository overview page and click on `New`:
1. Enter a name for your repo and an optional description
2. Choose between public and private. Anyone can see a public repository, but you choose who can commit changes. A private repository can only be seen by selected collaborators.
3. Add a readme file where you can add some description or guide for your repository.
4. Add a .gitignore file. Here, you can specify file names/types that **will not** be pushed to your GitHub repository.
5. Select a license.
6. Click on `create`

## How to clone a repository on your local machine?

With cloning a repository, you can create a local copy of the repository on GitHub. 

1. Got to your repository on github.com and under `Code` (green button) and then `HTTPS` copy the link ending on `.git`, as `https://github.com/username/myrepo.git`. 
2. In your terminal/command line, navigate to a directory of your choice.
3. Use the following command to clone your repository:
```
git clone https://github.com/username/myrepo.git
```

If you don't have permission to clone your repository, adding an SSH-key from your local machine to your GitHub account may solve the issue:
1. Create an SSH-key on your local machine if you have not done so before. For example, you can use `ssh-keygen -t rsa -b 4096 -C`.
2. Go to the directory where the key is stored, usually ~/.ssh/, and open the public key file: `cat id_rsa.pub`
3. Copy your public key
4. Go to your GitHub page, click on your account on the top right, and then `settings.` In `settings`, you should find the tab `SSH and GPG keys` where you can click on `New SSH key` to add your local key to your GitHub account.

## How to push changes to your remote repository on GitHub?

So, you have made some changes (created or modified some files) on your local repository. These changes are just present on your local machine and are not automatically transferred to your remote repo on GitHub. To push the changes to your remote repo, you have to create commits first. 

1. To list all the changes you have made since your last commit, you can use `git status` in your terminal/command line.
2. You can commit changes to a specific file to your local repository by using the following two commands:
```
git add </path/to/file>
git commit -m "<commit-message>"
```
3. Or to use one commit for all changed files, use `git add .`
4. Push your commits to the remote repository on github.com. Here, changes are committed to the main branch.
```
git push origin main
```

If you want to download the newest version of your remote repository, follow the steps below:
1. To fetch commits from your remote repository to your local machine, use
```
git fetch
```
 2. To actually update your local repository (here from the main branch), use
```
git pull origin main
```

## How to create new branches?

Branches can be used to implement and test new features without touching the main version of the project. When the new branch is finished, you can merge it with the main branch by creating a pull request. 

1. For creating a new branch, you can use the following command:
```
git branch <new-branch-name>
```
2. Switch to the new branch
```
git checkout <new-branch-name>
```
3. Push the new branch to your remote repository on GitHub
```
git push origin <new-branch-name>
```

Now, you are working on the new branch. To push changes to your remote repository, always use the correct branch name. To find out on which branch you are, use `git status`. 

## What are pull requests, and how do you create one?

Pull requests can be used to merge two different branches. Before creating a pull request, make sure that all changes have been pushed to your remote repository on github.com. To create a pull request, go to your repository on GitHub and select your new branch. Click on `New pull request` in the pull requests tab. Follow the steps in the menu. 

## What is a GitHub fork?

A GitHub fork is a personal copy of someone else's repository that is stored under your own GitHub account. It allows you to make changes to the code independently without affecting the original project. You can later propose changes (via pull requests) to the original repository or keep the modifications in your own fork.

## Summary of some important Git Commands

### 1. Git Configuration
- **`git config --global user.name "Your Name"`**  
  Set your name in Git configuration.
- **`git config --global user.email "your.email@example.com"`**  
  Set your email in Git configuration.
- **`git config --global core.editor your_editor`**  
  Set the default editor for Git.
- **`git config --list`**  
  View all configuration settings.

### 2. Basic Repository Commands
- **`git init`**  
  Initialize a new Git repository.
- **`git clone <repository>`**  
  Clone an existing repository from a remote source.

### 3. Working with Changes
- **`git fetch`**  
  Get changes from remote repository.
- **`git status`**  
  Check the status of your working directory.
- **`git diff <file>`**  
  Show differences in file local vs. remote
- **`git add <file>`**  
  Stage changes to be committed.
- **`git add .`**  
  Stage all changed files for commit.
- **`git commit -m "Commit message"`**  
  Commit the staged changes with a message.

### 4. Branching and Merging
- **`git branch`**  
  List all branches in the repository.
- **`git branch <branch-name>`**  
  Create a new branch.
- **`git checkout <branch-name>`**  
  Switch to a different branch.
- **`git merge <branch-name>`**  
  Merge changes from a branch into the current branch.
- **`git branch -d <branch-name>`**  
  Delete a branch that has been merged.

### 5. Viewing History
- **`git log`**  
  View the commit history.
- **`git log --oneline --graph`**  
  View a summarized graphical representation of the history.

### 6. Undoing Changes
- **`git reset <file>`**  
  Unstage a file without removing changes from the working directory.
- **`git checkout -- <file>`**  
  Discard changes in the working directory.
- **`git revert <commit>`**  
  Create a new commit that undoes a previous commit.

### 7. Remote Repositories
- **`git remote add origin <url>`**  
  Link the local repository to a remote repository.
- **`git push origin <branch-name>`**  
  Push changes to a remote repository.
- **`git pull origin <branch-name>`**  
  Pull changes from a remote repository.

### 8. Stashing Changes
- **`git stash`**  
  Temporarily save changes that are not ready to be committed.
- **`git stash pop`**  
  Reapply stashed changes and remove them from the stash.
- **`git stash list`**  
  List all stashed changes.

### 9. Tagging
- **`git tag <tag-name>`**  
  Create a new tag for marking a release or important version.
- **`git push origin <tag-name>`**  
  Push a tag to the remote repository.
