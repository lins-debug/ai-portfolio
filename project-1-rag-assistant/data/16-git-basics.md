# Git 版本控制

## 基本工作流

工作区 → 暂存区（git add）→ 本地仓库（git commit）→ 远程仓库（git push）。
git status 查看状态，git log 查看提交历史。

## 分支管理

git branch 创建分支，git checkout/switch 切换分支，git merge 合并分支。
分支策略：main 主分支 + feature 功能分支 + hotfix 修复分支。

## 常用命令

git clone：克隆远程仓库
git pull：拉取并合并远程更新
git stash：暂存当前修改
git rebase：变基，保持提交历史线性
git reset：回退到指定版本
git revert：反向提交撤销变更

## 解决冲突

多人在同一文件同一位置修改时产生冲突。手动编辑冲突标记（<<<<<<< ======= >>>>>>>），选择保留的内容。解决后 git add + git commit。

## .gitignore

忽略不需要版本控制的文件：*.pyc、__pycache__/、.env、node_modules/、.DS_Store。
