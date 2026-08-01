---
artifact_id: NOTICE-CONTRACT-001
artifact_type: NOTICE
project_id: PROJECT-PROFESSIONAL-SCREENWRITER
project_baseline: CONTRACT-v0.2.0
artifact_version: v0.1.11
status: IN_REVIEW
owner: LaoYu-Professional-Screenwriter
upstream_ids: [CONTRACT-PROFESSIONAL-SCREENWRITER]
review_id: REVIEW-CONTRACT-001
review_decision: PENDING
evidence_refs: [PLAN-v1.0.7, PHASE-1-COMPLETE, PHASE-2-COMPLETE, WP3B-PLACEHOLDERS, WP3B-ENUMS, WP3B-PLACEHOLDER-REPAIR, WP3B-UPSTREAM, WP4A-OWNERSHIP-AUDIT, WP3A-FEATURE-SCENES, A2-HANDOFF-STRUCTURE, A3B-SKILL-DEDUP, A4-EVIDENCE-CHAIN, A5-LICENSE-BOUNDARY, WP5-SINGLE-SOURCES]
notice_status: IN_PROGRESS
affected_ids: [CONTRACT-PROFESSIONAL-SCREENWRITER, PROJECT-PROFESSIONAL-SCREENWRITER]
affected_paths: [governance/**, templates/**, scripts/**, tests/**, LICENSES/**, SKILL.md, references/**, examples/**]
coupling: [BASELINE, SCHEMA, UPSTREAM, RIGHTS, PRODUCTION]
migration_tasks: [MIG-CONTRACT-001, MIG-WP3B-PLACEHOLDERS, MIG-WP3B-ENUMS, MIG-WP3B-PLACEHOLDER-REPAIR, MIG-WP3B-UPSTREAM, MIG-WP4A-OWNERSHIP-AUDIT, MIG-WP3A-FEATURE-SCENES, MIG-A2-HANDOFF-STRUCTURE, MIG-A3B-SKILL-DEDUP, MIG-A4-EVIDENCE-CHAIN, MIG-A5-LICENSE-BOUNDARY, MIG-WP5-SINGLE-SOURCES]
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
- `MIG-WP3B-ENUMS`：`VERIFIED`。59 个候选逐处裁决见
  `governance/enum-migration-map.tsv`；37 个错误用法迁入 schema 枚举域，22 个
  `ACTIVE`/`ARCHIVED` 用法因属于来源、谜团、决策、权利或项目阶段而保留；
- `MIG-WP3B-PLACEHOLDER-REPAIR`：`VERIFIED`。上游核对发现旧扫描器漏掉列表末尾
  的四个嵌套 token；失败证据、四处修复与原因见
  `governance/placeholder-migration-repair-map.tsv`，规范占位符累计1203处；
- `MIG-WP3B-UPSTREAM`：`VERIFIED`。11类正式模板的默认`upstream_ids`由schema生成表
  定义并逐模板一致；只保留上游方向，下游依赖继续由验证器反向生成，未制造双向循环；
- `MIG-WP4A-OWNERSHIP-AUDIT`：`VERIFIED`。filesystem ownership、未跟踪内容、空目录、
  模板闭包与保留文件名审计已接入；12个模板全部登记，feature场景预先锁定Scene Card
  数量匹配策略，4个README如实报告。规则自重叠与宿主`.claude`文件另记B9/B10，
  audit阶段不阻断，也不伪装为已修复；
- `MIG-WP3A-FEATURE-SCENES`：`VERIFIED`。feature Fountain已补齐三项身份字段，
  28个正式场景逐场绑定唯一稳定`SC-*`；实例化场景同步生成28份Scene Card，
  `ORPHAN_SCRIPT_SCENE`与`SCENE_NOT_IN_SCRIPT`均为零；
- `MIG-A2-HANDOFF-STRUCTURE`：`VERIFIED`。制作交接模板已下沉镜头/关键帧、声音/字幕/UI、
  连续性、执行/降级、权利/来源/复核及子交付物ID六类必填结构；解释和失败模式仍只在
  `references/ai-production-handoff.md`维护；
- `MIG-A3B-SKILL-DEDUP`：`VERIFIED`。Full Bible、Scene Card与四角色三组重复已按逐条
  语义迁移表改为“SKILL决策入口 + 精确主源锚点”；人工判读记录为`RECOMMEND`，未用
  关键词消失代替职责等价判断；
- `MIG-A4-EVIDENCE-CHAIN`：`VERIFIED`。R-03两处措辞统一；feature fixture把不可证的
  “延续到高潮”收窄为当前两场，补可见动作及`claim→scene→review finding`结构链；
  两条Finding均具九字段，语义充分性由`HUMAN_REVIEWED`记录承担；
- `MIG-A5-LICENSE-BOUNDARY`：`VERIFIED`。实际许可与第三方通知事实保留在`LICENSES/`；
  空白登记表迁入`templates/governance/`，判断方法与历史示例迁入`references/`；
  `governance/a5-license-boundary-map.tsv`覆盖旧三份边界文件的每一行，真实Skill许可文本
  保持字节级不变；
- `MIG-WP5-SINGLE-SOURCES`：`VERIFIED`。规则冲突优先级、四角色审查、STRUCT-LAYERED、
  钩子/付费点、变更等级与 Notice 分别收敛到唯一规范源，并以逐项迁移表保留领域适配；
  过时控制文件映射已删除，Skill 触发词限定在编剧语境。四个 README 按冻结裁决完成迁移、
  导出、改名或删除，安装树不再含保留文档名；导出包使用说明明确以 schema + WP4b 实现为准，
  未提前伪造不存在的 CLI；
- 最高可在原子激活前推进至：`VERIFIED`；
- `CLOSED` 仅允许与 Manifest 切换、合同 `LOCKED`、activation RUN 和 change-log
  最终摘要在同一 staging 事务中发生；
- 当前不得写入 reviewer/approver 最终签署，不得宣称新基线已激活。

## 回滚

任一 candidate 门禁失败时，停止后续迁移并回到最近 Phase tag；active baseline 与
`v0-baseline` 保持可读，不以删除旧历史伪造迁移成功。
