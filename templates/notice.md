---
artifact_id: NOTICE-[[NNN]]
artifact_type: NOTICE
project_id: PROJECT-[[SLUG]]-001
project_baseline: PROJECT-[[SLUG]]-v1.0.0
artifact_version: v1.0.0
status: DRAFT
owner: [[OWNER]]
upstream_ids: ["[[CHANGED-UPSTREAM-ID]]"]
notice_status: DRAFT
affected_ids: []
affected_paths: []
coupling: []
change_level: L1 / L2 / L3 / L4
priority: P0 / P1 / P2
---

# 上游变更通知

## 使用与命名

- 每次受控变更复制本模板为一个独立文件，统一存放在 `governance/notices/`。
- 推荐文件名：`governance/notices/NOTICE-<scope>-<NNN>-<slug>.md`；项目内简写可用
  `governance/notices/NOTICE-<NNN>-<slug>.md`。
- 文件名必须以 frontmatter 的 `artifact_id` 开头，使用 ASCII 连字符 `-`，不得使用下划线。
- 一个文件只承载一个 Notice 事务；完成全部下游同步与复验后，才可进入 `VERIFIED` 或 `CLOSED`。

## 1. 变更前后

| 对象 ID | 旧事实/状态 | 新事实/状态 | 是否锁定事实 | 事实源 |
|---|---|---|---|---|
| BIBLE-[[ID]] |  |  | 是 / 否 |  |

## 2. 触发证据

| Evidence ID | 文件 | 位置 | 发现内容 | 发现人 |
|---|---|---|---|---|
| EVID-[[NNN]] |  |  |  |  |

## 3. 影响对象

| 下游 Artifact | 影响类型 | 必须动作 | 负责人 | 复验方式 | 状态 |
|---|---|---|---|---|---|
| SC-[[ID]] | 因果/连续性/制作 |  |  |  | OPEN |

## 4. 迁移与回滚

- 迁移任务：`MIG-[[NNN]]`
- 目标基线：
- 回滚方案：
- 失败阻断条件：
- 批准人：
