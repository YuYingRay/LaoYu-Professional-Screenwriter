---
artifact_id: NOTICE-CONTRACT-001
artifact_type: NOTICE
project_id: PROJECT-PROFESSIONAL-SCREENWRITER
project_baseline: CONTRACT-v0.2.0
artifact_version: v0.1.23
status: IN_REVIEW
owner: LaoYu-Professional-Screenwriter
upstream_ids: [CONTRACT-PROFESSIONAL-SCREENWRITER]
review_id: REVIEW-CONTRACT-001
review_decision: CONDITIONAL_RECOMMEND
evidence_refs: [PLAN-v1.0.9, PHASE-1-COMPLETE, PHASE-2-COMPLETE, A1-VE-MAPPING, WP3B-PLACEHOLDERS, WP3B-ENUMS, WP3B-PLACEHOLDER-REPAIR, WP3B-UPSTREAM, WP4A-OWNERSHIP-AUDIT, WP3A-FEATURE-SCENES, A2-HANDOFF-STRUCTURE, A3B-SKILL-DEDUP, A4-EVIDENCE-CHAIN, A5-LICENSE-BOUNDARY, WP5-SINGLE-SOURCES, WP1B-STRICT-HYGIENE, A6-IDENTIFIER-BOUNDARIES, WP4B-FULL-VALIDATION, BENCH-PSW-v1.0.0-20260801, BENCH-PSW-E7-T2-R1-20260809, BENCH-PSW-E7-T2-R2-20260809, E7-CONTENT-ROLLBACK-20260812, BENCH-PSW-v1.0.0-20260812-ROLLBACK, E7-T4-RIGHTS-ROUTE-20260812, BENCH-PSW-v1.0.0-20260812-RIGHTS-ROUTE, USER-QUALITY-EXCEPTION-20260813-001, USER-TOKEN-EXCEPTION-20260814-001, PLAN-FREEZE-V109-20260821-001, MANIFEST-VIEW-ANCHOR-20260821-001, ACT-TRUST-001]
notice_status: CLOSED
affected_ids: [CONTRACT-PROFESSIONAL-SCREENWRITER, PROJECT-PROFESSIONAL-SCREENWRITER, DEL-OPEN-QUESTIONS-001, DEL-SOURCE-INDEX-001, DEL-NOTICE-INDEX-001, DEL-CHANGELOG-001, AUTH-001]
affected_paths: [governance/**, templates/**, scripts/**, tests/**, LICENSES/**, SKILL.md, references/**, examples/**]
coupling: [BASELINE, SCHEMA, UPSTREAM, RIGHTS, PRODUCTION]
changed_baseline: CONTRACT-v0.2.0
changed_schema_sections: [all]
verification_refs: [WP4B-FULL-VALIDATION, ROOT-CANDIDATE-VALIDATION, PHASE4-QUALITY-GATE-FAIL, E7-T2-R1-FAIL, E7-T2-R2-FAIL, E7-CONTENT-ROLLBACK-CONTROL-GATE, PHASE4-ROLLBACK-RETEST-FAIL, E7-T4-RIGHTS-ROUTE-UNIT, BENCH-PSW-v1.0.0-20260812-RIGHTS-ROUTE, V109-O1-PREPARE-VERIFIER]
change_records: [CHG-CONTRACT-001, CHG-MANIFEST-001, CHG-OPEN-QUESTIONS-001, CHG-SOURCE-INDEX-001, CHG-NOTICE-INDEX-001, CHG-CHANGELOG-001, CHG-ACTIVATION-001]
migration_tasks: [MIG-CONTRACT-001, MIG-A1-VE-MAPPING, MIG-WP3B-PLACEHOLDERS, MIG-WP3B-ENUMS, MIG-WP3B-PLACEHOLDER-REPAIR, MIG-WP3B-UPSTREAM, MIG-WP4A-OWNERSHIP-AUDIT, MIG-WP3A-FEATURE-SCENES, MIG-A2-HANDOFF-STRUCTURE, MIG-A3B-SKILL-DEDUP, MIG-A4-EVIDENCE-CHAIN, MIG-A5-LICENSE-BOUNDARY, MIG-WP5-SINGLE-SOURCES, MIG-WP1B-STRICT-HYGIENE, MIG-A6-IDENTIFIER-BOUNDARIES, MIG-WP4B-FULL-VALIDATION, MIG-PHASE4-CHANGELOG, MIG-PHASE4-E7-T2, MIG-E7-CONTENT-ROLLBACK, MIG-PHASE4-ROLLBACK-RETEST, MIG-E7-T4-RIGHTS-ROUTE, MIG-ACTIVATION-001]
closed_by_run_id: RUN-ACTIVATION-20260821-001
---

# NOTICE-CONTRACT-001：控制契约 v0.2.0 迁移事务

## 变更

- active baseline：`CONTRACT-v0.1.0`；
- candidate baseline：`CONTRACT-v0.2.0`；
- schema 成为枚举、字段矩阵、ownership、RUN、export 与影响选择器的机器权威；
- 本轮按冻结计划 A1–A6、WP2–WP5 逐项迁移，不允许静默覆盖旧基线；E.7 用户裁决 B
  已撤销其中会改变模型创作判断的内容子集，控制迁移继续保留。

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
- `MIG-A2-HANDOFF-STRUCTURE`：`REVERTED_BY_E7_B`。制作交接模板的内容扩张已撤销；旧结构
  证据只作为历史记录，不再代表当前候选能力；
- `MIG-A3B-SKILL-DEDUP`：`REVERTED_BY_E7_B`。SKILL 的内容语义去重已撤销，相应迁移表与
  专用门禁退役；这不是控制契约回退；
- `MIG-A4-EVIDENCE-CHAIN`：`CONTROL_SUBSET_VERIFIED / CONTENT_SUBSET_REVERTED`。
  R-03 的模型可见示例措辞恢复至内容基线；通用 `claim→scene→review finding` 连续性验证、
  fixture 结构及九字段 Finding 控制继续保留；
- `MIG-A5-LICENSE-BOUNDARY`：`VERIFIED`。实际许可与第三方通知事实保留在`LICENSES/`；
  空白登记表迁入`templates/governance/`，判断方法与历史示例迁入`references/`；
  `governance/a5-license-boundary-map.tsv`覆盖旧三份边界文件的每一行，真实Skill许可文本
  保持字节级不变；
- `MIG-WP5-SINGLE-SOURCES`：`CONTROL_SUBSET_VERIFIED / CONTENT_SUBSET_REVERTED`。
  规则冲突优先级、STRUCT-LAYERED、变更等级、Notice、README 处置、导出边界与 Skill 编剧
  触发词继续由控制层约束；四角色审查和钩子/付费点的内容单源化已撤销，相应两份迁移表与
  专用门禁退役；
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
  双平台 Python 3.11/3.13 CI 合同均已落地；内容层专用断言退役后，当前控制门禁为 113 项
  单测、strict、E2E 与 Skill Creator quick validator；
- 根候选校验补充了历史 Notice 兼容边界与 Manifest `candidate_baseline` 选择器；旧许可
  Notice 保持原基线且只读，未完成的旧 Notice 仍然阻断；根项目 candidate strict 校验通过；
- `MIG-PHASE4-CHANGELOG`：`VERIFIED`。变更日志此前已发生候选占位符迁移却仍标旧基线，
  本轮补入影响闭包并升至 v0.2.0；24 份质量回归的 E.4/E.5 FAIL 已如实记录，
  `review_decision: HOLD`，没有把控制平面正确性改善用于覆盖质量或 token 回归；
- `MIG-PHASE4-E7-T2`：`REVERTED_BY_E7_B`。两轮定向修复及其模型可见内容均已撤销；R1/R2
  结果只保留为历史失败证据，不得代表回退后候选；
- `MIG-E7-CONTENT-ROLLBACK`：`VERIFIED`。按用户裁决 B 对 13 个模型可见文件执行语义回退，
  保留机器契约、schema、ID、占位符、STRUCT-LAYERED、Notice、RUN、ownership、export、CI
  与通用连续性验证；三份只服务于已撤销内容的迁移表及 15 项专用断言退役，当前 113 项单测
  与 strict 门禁通过；
- `MIG-PHASE4-ROLLBACK-RETEST`：`FAILED / HOLD`。回退后候选已完整重跑 T1–T4；T1 的
  D1/D2 触发 E.4.1-C 方向一致下降，T3/T4 触发 E.5 零容差 FAIL。生成、评分、预揭盲与
  验证器证据完整性 PASS 不能覆盖目的层失败；完整结果与归因已写入 `governance/change-log.md`；
- `MIG-E7-T4-RIGHTS-ROUTE`：`IMPLEMENTED_PENDING_FULL_RETEST / HOLD`。权利清理默认只加载
  `rights-clearance-guide.md`，两份专项方法改为依据输入或既有资产清单中的具体类别按需选读；
  回归测试与 A5 迁移边界测试通过。因共享 `SKILL.md` 改动使旧四任务成绩失效，须绑定新候选
  从零完整重跑 T1–T4 后才能更新目的层结论；
- Notice 的控制迁移状态保持 `VERIFIED`，但原子激活质量门禁仍未通过；旧 `f8a1626`、R1、R2
  与本轮 `23704af` 的候选成绩分别绑定各自加载集，加载集变化后不得交叉复用；
- `CLOSED` 仅允许与 Manifest 切换、合同 `LOCKED`、activation RUN 和 change-log
  最终摘要在同一 staging 事务中发生；
- 当前不得写入 reviewer/approver 最终签署，不得宣称新基线已激活。

## 回滚

任一 candidate 门禁失败时，停止后续迁移并回到最近 Phase tag；active baseline 与
`v0-baseline` 保持可读，不以删除旧历史伪造迁移成功。E.7 用户已选择 B：内容层回退完成，
控制层保留；candidate 继续 `IN_REVIEW/HOLD`，Manifest 未切换，Notice 不得 `CLOSED`。

## 结构化变更记录

```change-record
record_id: CHG-CONTRACT-001
artifact_id: CONTRACT-PROFESSIONAL-SCREENWRITER
old_version: v0.1.0
new_version: v0.2.0
old_digest: sha256:b4ba28e25856bb614d75261d68ff881a01968677ba3d0edf2651f71e9e77bb5c
new_digest: sha256:79c539029a53fb18d0ac93d595735a6b6844eed072fe29830ce8e9f7615cf132
disposition: CONTENT_CHANGED
reason: 控制契约迁移到 v0.2.0，并纳入候选事务、Notice 兼容与影响闭包规则。
```

```change-record
record_id: CHG-MANIFEST-001
artifact_id: PROJECT-PROFESSIONAL-SCREENWRITER
old_version: v0.1.0
new_version: v0.2.0
old_digest: sha256:a0311a7cc3175dead528ce35b32c17a1406f2f885f5d428095cbb798a4a003b1
new_digest: sha256:2ac1634100526a35c388e1616df1668ff95937953a86e60d816201c8b31ca5bf
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
old_version: v0.2.7
new_version: v0.2.8
old_digest: sha256:e1dc77a401fd5ee83f8eecffbec8f4dbc96f0c8af979456c7265dc6ac9e27a31
new_digest: sha256:01b8e4725dead2413c174fd8623073bf34f2fff02983cefe7d85223b5a3a2ab9
disposition: CONTENT_CHANGED
reason: 将权利资料按输入事实选读的候选修复、旧四任务成绩失效与完整重跑停止条件纳入 v0.2.4；active baseline 保持不变。
```

---

## v1.0.9 终局事务记录（条件生效）

- 被测 candidate：`cd14ba43aefd272f8b63399cc0d68a6178c391a6`；baseline：
  `f807fcc232fd5c6dcdbd04be14fb672dbea690b3`；冻结计划：
  `v1.0.9 + 200171F5EA4CC76F21FB03719F2E19345D3091EEE51E95E360628C7859FFC0F8 + 757 行`；
- 最终全量复测保持正式结论：T2-D4、T4-D5 按 `E.4.1-C` FAIL；T1 `+7,326`、
  T4 `+12,163` 按 `E.5` FAIL。用户已分别接受只绑定当前测量身份的质量与 Token 残余风险；
  FAIL 不改为 PASS，不跨任务抵消，不构成先例；
- `ACT-TRUST-001` 只是假设：七个合同状态/签署字段与 Manifest 两个基线字段不改变模型产出，
  未经本轮 A/B 因果验证；用户须在 skill 外 ledger 中随精确 digest 明确接受，否则本事务不生效；
- 已知语义债：合同 frontmatter 拟切换为 `LOCKED`，但不在白名单内的
  `review_decision: PENDING` 与正文 `> 状态：IN_REVIEW` 保持被测原字节。此处只如实披露，
  不得据此宣称审查已完成；后续若要统一显示，必须另行解冻并重测受影响任务；
- 本文件的 `notice_status: CLOSED` 只在外部 ledger 同时存在用户最终 digest/ACT-TRUST-001
  接受事件，且 `RUN-ACTIVATION-20260821-001` final PASS 并与同一 canonical digest 一致时生效；
  条件未满足时，本 worktree 仅为 prepare-only staging，不是已激活基线。

```change-record
record_id: CHG-ACTIVATION-001
artifact_id: AUTH-001
old_version: v0.0.0
new_version: v0.1.0
old_digest: sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
new_digest: sha256:27c29401b6df5bfbb0c305694b53508cfe7be9c04703e3136a7e5ffcf1614877
disposition: CONTENT_CHANGED
reason: 新增拟签 staging 准备授权；空内容摘要只表示该 Artifact 在旧基线中不存在，不表示曾有空文件。
```
