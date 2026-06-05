---
name: github-issue
description: 规范化开发一个 GitHub issue，从理解需求到提交 PR 的完整工作流。当用户说 "开发 issue #N"、"实现 #N" 时触发。
---

# GitHub Issue 开发工作流

本工作流分阶段渐进加载规则。

## 全局约束

以下全局约束贯穿全部阶段，必须始终遵守。

- **禁止 force push、禁止 rebase**（除非用户明确要求）
- **禁止简化或改写以下任何 bash 命令**——命令经过验证，省略参数或合并步骤会导致不必要的错误
- 每个 commit 只包含一个逻辑变更
- 遵循项目中的编码规范
- 如果过程中发现 issue 描述与实际代码不符（如函数已改名、接口已变更），先向用户确认再继续

---

## Step 1: 创建或切换到开发分支

首先获取 GitHub 用户名和仓库默认分支：

```bash
USERNAME=$(gh api user --jq .login)
DEFAULT_BRANCH=$(git remote show origin | grep "HEAD branch" | awk '{print $NF}')
BRANCH="$USERNAME/issue<N>"
```

然后按以下逻辑处理：

**如果 `$BRANCH` 已存在：**
```bash
git switch $BRANCH
git pull origin $BRANCH
git fetch origin $DEFAULT_BRANCH && git merge origin/$DEFAULT_BRANCH
```

**合并冲突处理：**
- 优先尝试自动解决（同文件不同区域的误报冲突、格式差异等）
- 无法确定的语义冲突或大规模冲突时，执行 `git merge --abort` 中止合并，列出冲突文件和冲突内容，等待用户手动介入

**如果 `$BRANCH` 不存在：**
```bash
git switch $DEFAULT_BRANCH && git pull origin $DEFAULT_BRANCH
git switch -c $BRANCH
```

> 统一使用 `git switch`，不用 `git checkout`。

## Step 2: 获取 Issue 信息

使用 `gh issue view <N>` 获取 issue 的标题、描述、评论、labels。

使用 `gh api repos/{owner}/{repo}/issues/{N}/comments` 获取所有评论（如果需要更多上下文）。

---

> **Step 2 完成后**：读取 `./PLAN.md` 进入需求分析与计划阶段。
