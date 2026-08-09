---
artifact_id: NOTICE-CONTRACT-001
artifact_type: NOTICE
project_id: PROJECT-PROFESSIONAL-SCREENWRITER
project_baseline: CONTRACT-v0.2.0
artifact_version: v0.1.15
status: IN_REVIEW
owner: LaoYu-Professional-Screenwriter
upstream_ids: [CONTRACT-PROFESSIONAL-SCREENWRITER]
review_id: REVIEW-CONTRACT-001
review_decision: PENDING
evidence_refs: [PLAN-v1.0.8, PHASE-1-COMPLETE, PHASE-2-COMPLETE, A1-VE-MAPPING, WP3B-PLACEHOLDERS, WP3B-ENUMS, WP3B-PLACEHOLDER-REPAIR, WP3B-UPSTREAM, WP4A-OWNERSHIP-AUDIT, WP3A-FEATURE-SCENES, A2-HANDOFF-STRUCTURE, A3B-SKILL-DEDUP, A4-EVIDENCE-CHAIN, A5-LICENSE-BOUNDARY, WP5-SINGLE-SOURCES, WP1B-STRICT-HYGIENE, A6-IDENTIFIER-BOUNDARIES, WP4B-FULL-VALIDATION, BENCH-PSW-v1.0.0-20260801]
notice_status: VERIFIED
affected_ids: [CONTRACT-PROFESSIONAL-SCREENWRITER, PROJECT-PROFESSIONAL-SCREENWRITER, DEL-OPEN-QUESTIONS-001, DEL-SOURCE-INDEX-001, DEL-NOTICE-INDEX-001, DEL-CHANGELOG-001]
affected_paths: [governance/**, templates/**, scripts/**, tests/**, LICENSES/**, SKILL.md, references/**, examples/**]
coupling: [BASELINE, SCHEMA, UPSTREAM, RIGHTS, PRODUCTION]
changed_baseline: CONTRACT-v0.2.0
changed_schema_sections: [all]
verification_refs: [WP4B-FULL-VALIDATION, ROOT-CANDIDATE-VALIDATION, PHASE4-QUALITY-GATE-FAIL]
change_records: [CHG-CONTRACT-001, CHG-MANIFEST-001, CHG-OPEN-QUESTIONS-001, CHG-SOURCE-INDEX-001, CHG-NOTICE-INDEX-001, CHG-CHANGELOG-001]
migration_tasks: [MIG-CONTRACT-001, MIG-A1-VE-MAPPING, MIG-WP3B-PLACEHOLDERS, MIG-WP3B-ENUMS, MIG-WP3B-PLACEHOLDER-REPAIR, MIG-WP3B-UPSTREAM, MIG-WP4A-OWNERSHIP-AUDIT, MIG-WP3A-FEATURE-SCENES, MIG-A2-HANDOFF-STRUCTURE, MIG-A3B-SKILL-DEDUP, MIG-A4-EVIDENCE-CHAIN, MIG-A5-LICENSE-BOUNDARY, MIG-WP5-SINGLE-SOURCES, MIG-WP1B-STRICT-HYGIENE, MIG-A6-IDENTIFIER-BOUNDARIES, MIG-WP4B-FULL-VALIDATION, MIG-PHASE4-CHANGELOG]
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

- 当前：`VERIFIED`；
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
  导出、改名或删除，安装树不再含保留文档名；导出包使用说明最初只声明 schema 边界，
  WP4b 实现落地后已同步为真实 exporter/verifier CLI；
- `MIG-WP1B-STRICT-HYGIENE`：`VERIFIED`。ownership 的排除规则先于普通 owner 匹配，
  Windows 下 Git ignore 查询改用 NUL 协议，消除 B9 缓存重叠与 B10 宿主锁文件误报；
  未增加 allowlist，也未删除宿主状态。schema enforcement 已切为 `strict`，真实安装树
  `lint_repo --mode strict` 无 Finding；
- `MIG-A1-VE-MAPPING`：`VERIFIED`。37 处 `VE*` 已按 24 个示例表格、8 个标题、3 个正文
  独立分类；canonical 字段保持 `EP-*`，展示别名保留并由合同定义单射映射，`EP-08` 已修正补零；
- `MIG-A6-IDENTIFIER-BOUNDARIES`：`VERIFIED`。场景 ID、legacy Notice ID 与 `TBD` 门禁均改用
  排除 ASCII 字母数字的左右断言；Python 正负参数化测试为唯一阻断门禁，`rg --pcre2` 本机诊断为
  `AGREE`，未把第二引擎升级为 CI 依赖；
- `MIG-WP4B-FULL-VALIDATION`：`VERIFIED`。RUN 九类突变、Notice 反向闭包与 baseline/schema
  选择器、未接受 P1、三夹具生产证据链、9 行真实 CLI E2E 不变量矩阵、确定性导出/独立验证器及
  双平台 Python 3.11/3.13 CI 合同均已落地；最终本地总门禁为 125 项单测、strict、E2E 与
  Skill Creator quick validator 全部通过；
- 根候选校验补充了历史 Notice 兼容边界与 Manifest `candidate_baseline` 选择器；旧许可
  Notice 保持原基线且只读，未完成的旧 Notice 仍然阻断；根项目 candidate strict 校验通过；
- `MIG-PHASE4-CHANGELOG`：`VERIFIED`。变更日志此前已发生候选占位符迁移却仍标旧基线，
  本轮补入影响闭包并升至 v0.2.0；24 份质量回归的 E.4/E.5 FAIL 已如实记录，
  `review_decision: HOLD`，没有把控制平面正确性改善用于覆盖质量或 token 回归；
- 原子激活前的最高状态 `VERIFIED` 已达到；
- `CLOSED` 仅允许与 Manifest 切换、合同 `LOCKED`、activation RUN 和 change-log
  最终摘要在同一 staging 事务中发生；
- 当前不得写入 reviewer/approver 最终签署，不得宣称新基线已激活。

## 回滚

任一 candidate 门禁失败时，停止后续迁移并回到最近 Phase tag；active baseline 与
`v0-baseline` 保持可读，不以删除旧历史伪造迁移成功。

## 结构化变更记录

```change-record
record_id: CHG-CONTRACT-001
artifact_id: CONTRACT-PROFESSIONAL-SCREENWRITER
old_version: v0.1.0
new_version: v0.2.0
old_digest: sha256:b4ba28e25856bb614d75261d68ff881a01968677ba3d0edf2651f71e9e77bb5c
new_digest: sha256:4fea5a585da548fcccf8b5a25e6f96794761d4196b8763a2213305c908446039
disposition: CONTENT_CHANGED
reason: 控制契约迁移到 v0.2.0，并纳入候选事务、Notice 兼容与影响闭包规则。
```

```change-record
record_id: CHG-MANIFEST-001
artifact_id: PROJECT-PROFESSIONAL-SCREENWRITER
old_version: v0.1.0
new_version: v0.2.0
old_digest: sha256:a0311a7cc3175dead528ce35b32c17a1406f2f885f5d428095cbb798a4a003b1
new_digest: sha256:5a94f1e571ff70131becb3b495fdcbbb19905994898189c3a06ae9f9edefb1d1
disposition: CONTENT_CHANGED
reason: Manifest 保持 active baseline，同时声明 candidate baseline 与当前迁移证据。
```

```change-record
record_id: CHG-OPEN-QUESTIONS-001
artifact_id: DEL-OPEN-QUESTIONS-001
old_version: v0.1.0
new_version: v0.2.0
old_digest: sha256:a650c0034830f6e4802417a35fb5b01119b3aecca2e7e224f63e451d6e9482cd
new_digest: sha256:46f668a1476a58305b3b9ea3a86cf9e68f2e8308ef81b562c89ddf2b85858769
disposition: CONTENT_CHANGED
reason: 候选事务建立后，架构悬题及已关闭实测根因已更新并迁入 v0.2.0。
```

```change-record
record_id: CHG-SOURCE-INDEX-001
artifact_id: DEL-SOURCE-INDEX-001
old_version: v0.1.0
new_version: v0.2.0
old_digest: sha256:ee14a7309e9c4ecceb504629cfb1cbcb83d9d4ff2f589b76b547d4854c7c065e
new_digest: sha256:0b6b7c70d152ba5d4d71c6d46eadaa46be68be1838367d34e5f5c2e50da8a9bc
disposition: CONTENT_CHANGED
reason: 来源与证据索引在候选事务中完成许可边界和方法论证据迁移。
```

```change-record
record_id: CHG-NOTICE-INDEX-001
artifact_id: DEL-NOTICE-INDEX-001
old_version: v0.1.0
new_version: v0.2.0
old_digest: sha256:5cfc171e52a121e2aef44f2bed7f8e08d1bce53ada476f4d14ebc43342399abe
new_digest: sha256:7a095957a85af809ca460971283158d08f228a6d4f1dbc8ae3d1db1701b9848c
disposition: CONTENT_CHANGED
reason: Notice 索引迁入 v0.2.0，并收敛状态、命名与影响传播的规范入口。
```

```change-record
record_id: CHG-CHANGELOG-001
artifact_id: DEL-CHANGELOG-001
old_version: v0.1.0
new_version: v0.2.0
old_digest: sha256:8c87a747ec02c8f31c0e9a2bc633c45833791cc7f7195c5854c31b7c87ea47c0
new_digest: sha256:aaad7837506cf78599a9842f695287ae4337d09f46851a23f1aa1711048f55d7
disposition: CONTENT_CHANGED
reason: 将既有候选占位符迁移与 Phase 4 质量门禁 FAIL 纳入 v0.2.0 影响闭包；active baseline 保持不变。
```
