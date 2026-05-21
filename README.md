# ai-toolkit

AI 学习与使用过程中积累的工具、笔记、skill 集合。

## Skills

### `github-issue`

从 Issue 到 PR 合并的规范化开发工作流。

**安装**

```bash
npx skills add https://github.com/dan-kuroto/ai-toolkit/tree/master/skills/github-issue
```

---

## Hooks

### `send_notification.py`

发送系统桌面通知，依赖 [plyer](https://github.com/kivy/plyer) 实现跨平台通知推送。

配置 Claude Code hook：

```json
{
  "hooks": {
    "PermissionRequest": [
      {
        "hooks": [
          {
            "command": "uv run --with plyer C:/jsProjects/ai-toolkit/hooks/send_notification.py -t 'Claude Code' -m 'Permission Request'",
            "type": "command"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "command": "uv run --with plyer C:/jsProjects/ai-toolkit/hooks/send_notification.py -t 'Claude Code' -m 'Task Completed'",
            "type": "command"
          }
        ]
      }
    ]
  }
}
```
