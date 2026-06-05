> 以下命令必须逐字执行，不得合并、简化或替换参数。

# Step 7: 提交 PR

创建 PR（`<N>` 替换为 issue 号）：

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

---

# Step 8: 合并 PR

## 8.1 等待 CI 检查

```bash
gh pr checks <PR_NUMBER> --watch
```

**此步骤不可跳过。** `--watch` 会阻塞等待 CI 完成，不得以 `gh pr view` 或 `gh pr checks`（不带 `--watch`）替代。

## 8.2 检查合并状态

```bash
MERGEABLE=$(gh pr view <PR_NUMBER> --json mergeable --jq .mergeable)
```

## 8.3 执行合并

**如果 `MERGEABLE` 为 `MERGEABLE`：**

执行 squash merge，自行总结本次变更作为 body：

```bash
gh pr merge <PR_NUMBER> --squash --delete-branch --body "<总结>"
```

**如果存在冲突（`CONFLICTING`）：**

跳过自动合并，提示用户手动处理冲突。不要尝试任何自动解决。

## 8.4 验证 issue 已关闭

```bash
gh issue view <N> --json state --jq .state
```

输出应为 `CLOSED`。

---

# Step 9: 清理本地分支

合并成功后，切回主分支并清理：

```bash
git switch $DEFAULT_BRANCH && git pull origin $DEFAULT_BRANCH && (git branch -D $BRANCH 2>/dev/null || true) && git remote prune origin
```

> 注意：合并 PR 时可能已自动清理本地分支，为避免删除分支报错导致流程中断，**必须保留** `2>/dev/null || true` 忽略错误，以确保顺利执行过期远程分支的清理。
