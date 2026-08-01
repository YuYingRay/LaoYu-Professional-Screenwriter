---
artifact_id: NOTICE-CONTRACT-001
artifact_type: NOTICE
project_id: PROJECT-PROFESSIONAL-SCREENWRITER
project_baseline: CONTRACT-v0.2.0
artifact_version: v0.1.1
status: IN_REVIEW
owner: LaoYu-Professional-Screenwriter
upstream_ids: [CONTRACT-PROFESSIONAL-SCREENWRITER]
review_id: REVIEW-CONTRACT-001
review_decision: PENDING
evidence_refs: [PLAN-v1.0.7, PHASE-1-COMPLETE, PHASE-2-COMPLETE, WP3B-PLACEHOLDERS]
notice_status: IN_PROGRESS
affected_ids: [CONTRACT-PROFESSIONAL-SCREENWRITER, PROJECT-PROFESSIONAL-SCREENWRITER]
affected_paths: [governance/**, templates/**, scripts/**, tests/**, LICENSES/**, SKILL.md, references/**, examples/**]
coupling: [BASELINE, SCHEMA, UPSTREAM, RIGHTS, PRODUCTION]
migration_tasks: [MIG-CONTRACT-001, MIG-WP3B-PLACEHOLDERS]
---

# NOTICE-CONTRACT-001：控制契约 v0.2.0 迁移事务

## 变更

- active baseline：`CONTRACT-v0.1.0`；
- candidate baseline：`CONTRACT-v0.2.0`；
- schema 成为枚举、字段矩阵、ownership、RUN、export 与影响选择器的机器权威；
- 本轮按冻结计划 A1–A6、WP2–WP5 逐项迁移，不允许静默覆盖旧基线。

## 影响闭包

当前 `affected_ids` 只登记已存在且已直接进入事务的控制 Artifact。完整 affected set
必须在 Phase 3 由 `upstream_ids` 反向传递闭包与 baseline/schema 选择器联合推导；
缺少仅由 baseline 或 schema 影响的 Artifact 时不得进入 `VERIFIED`。

## 迁移状态

- 当前：`IN_PROGRESS`；
- `MIG-WP3B-PLACEHOLDERS`：`VERIFIED`。显式逐处映射见
  `governance/placeholder-migration-map.json`；1199 个可填写槽位已迁为 `[[…]]`，
  复选框、前置列表、Markdown 链接与 Fountain 非占位内容保持不变；
- 最高可在原子激活前推进至：`VERIFIED`；
- `CLOSED` 仅允许与 Manifest 切换、合同 `LOCKED`、activation RUN 和 change-log
  最终摘要在同一 staging 事务中发生；
- 当前不得写入 reviewer/approver 最终签署，不得宣称新基线已激活。

## 回滚

任一 candidate 门禁失败时，停止后续迁移并回到最近 Phase tag；active baseline 与
`v0-baseline` 保持可读，不以删除旧历史伪造迁移成功。
