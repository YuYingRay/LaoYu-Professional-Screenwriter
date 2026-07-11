# 独立 Notice 目录

每次受控变更创建一个独立文件：

```text
NOTICE_[PROJECT]_[NOTICE-NNN]_[slug].md
```

文件必须使用 `templates/notice.md` 的字段，并在完成下游同步与复验后才可标记 `VERIFIED` 或 `CLOSED`。

`governance/upstream-notices.md` 只维护索引和流程说明，不承载所有变更记录。
