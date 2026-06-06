---
name: github-issue
description: 规范化开发一个 GitHub issue，从理解需求到提交 PR 的完整工作流。当用户说 "开发 issue #N"、"实现 #N" 时触发。
---

# GitHub Issue 开发工作流

当用户要求开发某个 GitHub issue 时，遵循以下工作流：

## 全局约束

以下全局约束贯穿全部阶段，必须始终遵守。

- **禁止 force push、禁止 rebase**（除非用户明确要求）
- **禁止简化或改写以下任何 bash 命令**——命令经过验证，省略参数或合并步骤会导致不必要的错误
- 每个 commit 只包含一个逻辑变更
- 遵循项目中的编码规范
- 如果过程中发现 issue 描述与实际代码不符（如函数已改名、接口已变更），先向用户确认再继续

## 工作流

### Step 1: 切换/创建分支

首先获取当前 GitHub 用户名和主分支名（`main` 或 `master`）：

```bash
USERNAME=$(gh api user --jq .login)
DEFAULT_BRANCH=$(git remote show origin | grep "HEAD branch" | awk '{print $NF}')
BRANCH="$USERNAME/issue<N>"
```

然后按以下逻辑处理：

- **如果 `$BRANCH` 已存在**：`git switch $BRANCH`，然后 `git pull origin $BRANCH` 同步最新代码，同时 `git fetch origin $DEFAULT_BRANCH && git merge origin/$DEFAULT_BRANCH` 合入主分支最新代码
  - **合并冲突处理**：优先尝试自动解决（同文件不同区域的误报冲突、格式差异等）；无法确定的语义冲突或大规模冲突时，执行 `git merge --abort` 中止合并，列出冲突文件和冲突内容，等待用户手动介入
- **如果 `$BRANCH` 不存在**：先 `git switch $DEFAULT_BRANCH && git pull origin $DEFAULT_BRANCH`，再 `git switch -c $BRANCH`

统一使用 `git switch`（不用 `git checkout`）。

### Step 2: 获取 Issue 信息

- 使用 `gh issue view <N>` 获取 issue 的标题、描述、评论、labels。
- 使用 `gh api repos/{owner}/{repo}/issues/{N}/comments` 获取所有评论（如果需要更多上下文）。

### Step 3: 理解需求与范围

- 提取 issue 的核心需求和验收条件
- 如果需求不明确，向用户提出澄清问题
- 确认影响范围和涉及的模块

### Step 4: 制定计划

所有 issue 均需进入 plan mode，使用 EnterPlanMode 设计实现方案。

向用户展示计划内容，**必须等待用户确认后再进入 Step 5 开始开发**。用户提出修改意见的，调整计划后重新确认。

### Step 5: 实施

按 TaskCreate 创建的任务清单逐步实施：

1. **测试**：不强制要求全量测试
   - 对无副作用的工具函数编写单元测试
   - 业务功能或难以写测试代码的可以跳过，通过实际运行验证
2. **实现功能代码**——最小改动实现需求
3. **运行测试**——每次改动后执行项目静态检查和测试
4. **提交**——每个逻辑变更一个 commit，格式见下方「提交格式」

#### 提交格式

```bash
git commit -m "$(cat <<'EOF'
<type>(<scope>): <描述>

<变更说明>
EOF
)"
```

- **type** — `feat / fix / doc / refactor / perf / test / build / ci / chore`
- **scope** — 涉及的模块或功能区域；跨模块用 `*`
- **描述** — 简明扼要，中文优先
- **变更说明** — 本次变更详情。对于改动较小、<描述>就能说清楚的，可省略

### Step 6: 验证与确认

- 运行完整测试套件
- 确认变更范围符合预期
- 确认没有引入 lint 错误或类型错误
- **必须等待用户确认后**才能进入 Step 7。用户提出修改意见的，回到 Step 5 重新实施后再验证。

### Step 7: 提交 PR

```bash
gh pr create --title "<type>(<scope>): <描述>" --body "$(cat <<'EOF'
## Summary
- <bullet point 1>
- <bullet point 2>
- <bullet point 3>

Closes #<N>
EOF
)"
```

- PR 标题格式 `<type>(<scope>): <描述>`，与 commit message 一致
- PR body 以 `Closes #<N>` 结尾，确保合并后自动关闭 issue

### Step 8: 合并 PR

PR 提交后，检查是否存在冲突并尝试自动合并：

```bash
gh pr checks <PR_NUMBER> --watch  # 等待 CI 检查完成
# 检查合并状态
MERGEABLE=$(gh pr view <PR_NUMBER> --json mergeable --jq .mergeable)
```

- 如果 `MERGEABLE` 为 `MERGEABLE`：执行 squash merge，自行总结本次变更作为 body：
  ```bash
  gh pr merge <PR_NUMBER> --squash --delete-branch --body "<总结>"
  ```
- 如果存在冲突（`CONFLICTING`）：**跳过自动合并**，提示用户手动处理冲突

合并成功后，若 PR body 中包含 `Closes #N`，GitHub 会自动关闭对应 issue。可在合并后验证：

```bash
gh issue view <N> --json state --jq .state  # 应为 CLOSED
```

### Step 9: 清理本地分支

合并成功后，切回主分支并清理本地开发分支：

```bash
git switch $DEFAULT_BRANCH && git pull origin $DEFAULT_BRANCH && (git branch -D $BRANCH 2>/dev/null || true) && git remote prune origin
```

> 注意：合并 PR 时可能已自动清理本地分支，为避免报错导致流程中断，删除分支时**必须保留** `2>/dev/null || true` 忽略错误，以确保顺利执行过期远程分支的清理。
