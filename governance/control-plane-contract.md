---
artifact_id: CONTRACT-PROFESSIONAL-SCREENWRITER
artifact_type: CONTROL_PLANE_CONTRACT
project_id: PROJECT-PROFESSIONAL-SCREENWRITER
project_baseline: CONTRACT-v0.2.0
artifact_version: v0.2.0
status: IN_REVIEW
owner: LaoYu-Professional-Screenwriter
maintainer: YuYingRay
license: CC BY 4.0
official_source: https://github.com/YuYingRay/LaoYu-Professional-Screenwriter
upstream_ids: []
review_id: REVIEW-CONTRACT-001
review_decision: PENDING
evidence_refs: [NOTICE-CONTRACT-001]
---

# Professional Screenwriter 控制平面契约

> 版本：`CONTRACT-v0.2.0`
> 许可方：`LaoYu-Professional-Screenwriter`  
> 官方来源：`https://github.com/YuYingRay/LaoYu-Professional-Screenwriter`  
> 许可：CC BY 4.0（Skill 原创内容；第三方材料另行标记）  
> 状态：IN_REVIEW

## 0. 契约目的

本契约定义 Professional Screenwriter 项目文件如何保持：

```text
身份明确 → 权威明确 → 依赖可追溯 → 变更可传播 → 门禁可验证
```

它不判断故事是否“好看”，也不替代编剧、导演、制片、法务或专业顾问的判断。

它只约束可观察的项目控制事实：文件身份、版本、状态、依赖、审查、风险、权利和放行条件。

## 1. 对象模型

| 对象 | 定义 | 最小问题 |
|---|---|---|
| Project | 一个拥有明确交付目标和基线的创作项目 | 这是哪个项目？ |
| Artifact | 一个可独立版本化的文件或文件包 | 这份文件是什么？ |
| Fact | 可影响人物选择、因果、连续性或制作的原子事实 | 哪个事实有效？ |
| Dependency | Artifact 对上游事实或文件的依赖 | 它依据什么？ |
| Review | 对 Artifact 或事实进行的人类审查 | 谁如何判断？ |
| Notice | 一次受控变更传播事件 | 变化影响什么？ |
| Test Run | 对结构和追溯规则的验证记录 | 机器检查了什么？ |

## 2. 一致性等级

| 等级 | 含义 | 主要证据 |
|---|---|---|
| `STRUCTURAL_CONFORMANCE` | 字段、ID、路径、状态和版本合法 | 自动验证报告 |
| `TRACEABILITY_CONFORMANCE` | 事实、结构、场景、剧本和交接可追溯 | 依赖图与基线检查 |
| `HUMAN_REVIEWED` | 已完成人类对抗式审查 | REVIEW 报告与批准记录 |
| `PRODUCTION_READY` | 下游制作包可基于当前基线执行 | 兼容性矩阵、权利记录、生产批准 |

低等级通过不得宣称高等级完成。

## 2.1 Schema 生成投影

<!-- GENERATED:schema START -->

> 生成源：`governance/control-schema.json`（`PSW-CONTROL-SCHEMA-v0.2.0`）。
> 本区块禁止手改；运行 `python -X utf8 scripts/gen_contract_tables.py . --check` 对账。

### 状态必填字段

| 状态 | 基本字段 | 状态附加字段 |
|---|---|---|
| `DRAFT` | `artifact_id`, `artifact_type`, `project_id`, `project_baseline`, `artifact_version`, `status`, `owner`, `upstream_ids` | — |
| `IN_REVIEW` | `artifact_id`, `artifact_type`, `project_id`, `project_baseline`, `artifact_version`, `status`, `owner`, `upstream_ids` | `review_id`, `review_decision`, `evidence_refs` |
| `APPROVED` | `artifact_id`, `artifact_type`, `project_id`, `project_baseline`, `artifact_version`, `status`, `owner`, `upstream_ids` | `reviewer`, `approver`, `test_run_id`, `conformance_level` |
| `LOCKED` | `artifact_id`, `artifact_type`, `project_id`, `project_baseline`, `artifact_version`, `status`, `owner`, `upstream_ids` | `lock_scope`, `content_digest` |
| `SUPERSEDED` | `artifact_id`, `artifact_type`, `project_id`, `project_baseline`, `artifact_version`, `status`, `owner`, `upstream_ids` | `superseded_by` |
| `BLOCKED` | `artifact_id`, `artifact_type`, `project_id`, `project_baseline`, `artifact_version`, `status`, `owner`, `upstream_ids` | `blocked_reason` |

### 类型附加字段

| Artifact 类型 | 附加字段 |
|---|---|
| `NOTICE` | `notice_status`, `affected_ids`, `affected_paths`, `coupling` |
| `PRODUCTION_HANDOFF` | — |
| `REVIEW` | `findings` |

### ID 前缀

| 前缀 | Artifact 类型 | 示例 |
|---|---|---|
| `ARC-` | `CHARACTER_ARC` | `ARC-PROTAG-001` |
| `ASM-` | `ASSUMPTION` | `ASM-001` |
| `ASSET-` | `ASSET` | `ASSET-PROP-001` |
| `AUDIO-` | `AUDIO` | `AUDIO-001` |
| `BEAT-` | `BEAT` | `BEAT-001` |
| `BIBLE-` | `STORY_BIBLE` | `BIBLE-CHAR-001` |
| `CLM-` | `CLAIM` | `CLM-001` |
| `CON-` | `CONSTRAINT` | `CON-001` |
| `DEL-` | `OUTLINE` | `DEL-OUTLINE-001` |
| `DEL-` | `PRODUCTION_HANDOFF` | `DEL-HANDOFF-001` |
| `DEL-` | `SEASON_MAP` | `DEL-SEASON-001` |
| `EP-` | `VERTICAL_EPISODE` | `EP-001` |
| `LOCK-` | `LOCK` | `LOCK-001` |
| `MIG-` | `MIGRATION` | `MIG-001` |
| `NOTICE-` | `NOTICE` | `NOTICE-001` |
| `PROJECT-` | `PROJECT_MANIFEST` | `PROJECT-TIDELINE-001` |
| `REVIEW-` | `REVIEW` | `REVIEW-001` |
| `RGT-` | `RIGHTS_ITEM` | `RGT-001` |
| `SC-` | `SCENE_CARD` | `SC-001` |
| `SCRIPT-` | `SCRIPT_MASTER` | `SCRIPT-v1.0.0` |
| `SHOT-` | `SHOT` | `SHOT-001` |
| `SRC-` | `SOURCE` | `SRC-001` |
| `SUB-` | `SUBTITLE_UI` | `SUB-001` |
| `TP-` | `THIRD_PARTY_MATERIAL` | `TP-001` |

### Review Finding 九字段

`finding_id`, `severity`, `evidence_location`, `failure_mechanism`, `downstream_impact`, `minimum_fix`, `verification_method`, `owner`, `status`

### 领域枚举

| 枚举域 | 合法值 |
|---|---|
| `project_stages` | `CONCEPT`, `DEVELOPMENT`, `OUTLINE`, `SCRIPT`, `PREP`, `PRODUCTION`, `POST`, `RELEASE`, `ARCHIVED` |
| `work_actions` | `DISCOVER`, `BUILD_BIBLE`, `STRUCTURE`, `OUTLINE`, `DRAFT`, `REVIEW`, `REWRITE`, `CONTINUITY_CHECK`, `BUILD_HANDOFF` |
| `finding_statuses` | `OPEN`, `IN_PROGRESS`, `FIXED`, `ACCEPTED_RISK`, `REGRESSED` |
| `source_statuses` | `ACTIVE`, `PENDING_REVIEW`, `PARTIALLY_VERIFIED`, `VERIFIED`, `DISPUTED`, `OUTDATED`, `PAYWALLED`, `MOVED`, `ARCHIVED`, `SUPERSEDED`, `DO_NOT_USE` |
| `mystery_statuses` | `PLANTED`, `ACTIVE`, `PARTIALLY_PAID`, `PAID`, `DROPPED`, `REPLACED` |
| `decision_statuses` | `ACTIVE`, `SUPERSEDED`, `REVISIT`, `REJECTED` |
| `deprecation_statuses` | `OPEN`, `IN_PROGRESS`, `VERIFIED`, `REMOVED` |
| `rights_statuses` | `CANDIDATE`, `INTERNAL_ONLY`, `RIGHTS_PENDING`, `LICENSE_REQUESTED`, `LICENSED_LIMITED`, `OPEN_LICENSE_VERIFIED`, `PUBLIC_DOMAIN_CONFIRMED`, `PROJECT_ORIGINAL`, `CLIENT_PROVIDED`, `TALENT_RELEASED`, `APPROVED_FOR_USE`, `RESTRICTED`, `EXPIRING`, `EXPIRED`, `DISPUTED`, `REPLACEMENT_REQUIRED`, `REMOVED`, `ARCHIVED`, `DO_NOT_USE` |

### Template upstream 默认值

> 这里只声明上游。下游关系由验证器反向生成，禁止模板手工维护反向清单。

| Artifact 类型 | `upstream_ids` 默认槽位 |
|---|---|
| `PROJECT_MANIFEST` | — |
| `SOURCE_REGISTER` | `[[PROJECT-ID]]` |
| `NOTICE_INDEX` | `[[PROJECT-ID]]` |
| `CHANGE_LOG` | `[[PROJECT-ID]]`, `[[NOTICE-INDEX-ID]]` |
| `STORY_BIBLE` | `[[PROJECT-ID]]` |
| `OUTLINE` | `[[BIBLE-ID]]` |
| `VERTICAL_EPISODE` | `[[BIBLE-ID]]`, `[[SEASON-MAP-ID]]` |
| `SCENE_CARD` | `[[BIBLE-ID]]`, `[[OUTLINE-OR-EPISODE-ID]]` |
| `REVIEW` | `[[BIBLE-ID]]`, `[[REVIEWED-ARTIFACT-ID]]` |
| `NOTICE` | `[[CHANGED-UPSTREAM-ID]]` |
| `PRODUCTION_HANDOFF` | `[[BIBLE-ID]]`, `[[SCRIPT-ID]]`, `[[REVIEW-ID]]` |

### Notice 状态与耦合

notice_status：`DRAFT`, `OPEN`, `IN_PROGRESS`, `VERIFIED`, `CLOSED`

coupling：`UPSTREAM`, `BASELINE`, `SCHEMA`, `RIGHTS`, `PRODUCTION`

| `notice_status` | 附加必填字段 |
|---|---|
| `DRAFT` | — |
| `OPEN` | `affected_ids`, `affected_paths`, `coupling` |
| `IN_PROGRESS` | `affected_ids`, `affected_paths`, `coupling`, `migration_tasks` |
| `VERIFIED` | `affected_ids`, `affected_paths`, `coupling`, `verification_refs` |
| `CLOSED` | `affected_ids`, `affected_paths`, `coupling`, `verification_refs`, `closed_by_run_id` |

<!-- GENERATED:schema END -->

## 3. ID 规则

| 前缀 | 对象 | 示例 |
|---|---|---|
| `PROJECT-` | 项目 | `PROJECT-TIDELINE-001` |
| `CON-` | 项目约束 | `CON-001` |
| `ASM-` | 创作假设 | `ASM-001` |
| `CLM-` | 外部主张 | `CLM-001` |
| `SRC-` | 来源 | `SRC-001` |
| `RGT-` | 权利项 | `RGT-001` |
| `TP-` | 第三方材料 | `TP-001` |
| `BIBLE-` | Bible 事实 | `BIBLE-CHAR-001` |
| `ARC-` | 人物弧 | `ARC-PROTAG-001` |
| `BEAT-` | 结构节点 | `BEAT-001` |
| `EP-` | 集 | `EP-001` |
| `SC-` | 逻辑场景 | `SC-001` |
| `SCRIPT-` | 剧本版本 | `SCRIPT-v1.0.0` |
| `ASSET-` | 资产 | `ASSET-PROP-001` |
| `SHOT-` | 镜头 | `SHOT-001` |
| `AUDIO-` | 音频 | `AUDIO-001` |
| `SUB-` | 字幕/UI | `SUB-001` |
| `NOTICE-` | 上游变更通知 | `NOTICE-001` |
| `REVIEW-` | 审查报告 | `REVIEW-001` |
| `MIG-` | 迁移任务 | `MIG-001` |
| `LOCK-` | 锁定点 | `LOCK-001` |
| `DEL-` | 交付物 | `DEL-001` |

逻辑 ID 一旦创建不得因排序、删场或重排而复用或重编号。展示编号可以变化。

竖屏短剧允许用 `VE[[集数]]` 作为文件名与叙述层的展示别名，但集的 canonical ID
始终使用 `EP-[[NNN]]`。两者按相同集数建立一一映射，例如 `VE01 ↔ EP-001`；
同一集不得映射到多个别名或 canonical ID。`artifact_id`、
`upstream_ids` 以及 Notice 中承担规范引用职责的字段不得写入 `VE*`。

## 4. 通用 Artifact 元数据

正式 Artifact 必须声明：

```text
artifact_id
artifact_type
project_id
project_baseline
artifact_version
status
owner
upstream_ids
```

进入审查时必须增加：

```text
review_id
review_decision
evidence_refs
```

进入 LOCKED 或 PRODUCTION_READY 时必须增加：

```text
reviewer
approver
lock_scope
content_digest
test_run_id
conformance_level
```

只声明 `upstream_ids`。下游依赖由验证器根据上游关系生成，不允许人工维护两套相互矛盾的依赖清单。

单人项目中，`reviewer` 与 `approver` 可以是同一人；但两个字段、审查证据与批准
证据仍必须分别存在，不能因为角色由同一人承担就省略任一门禁。

## 5. 字段状态

```text
OPEN → PROPOSED → REVIEWED → LOCKED → SUPERSEDED
```

另有终止状态：`NOT_APPLICABLE`。

| 状态 | 含义 |
|---|---|
| `OPEN` | 尚未形成决定 |
| `PROPOSED` | 已有候选方案但未批准 |
| `REVIEWED` | 已检查但未锁定 |
| `LOCKED` | 当前基线中的有效事实 |
| `SUPERSEDED` | 已由新事实替代 |
| `NOT_APPLICABLE` | 对本项目明确不适用，必须附理由 |

空白、`TBD`、`待定`、`以后再说`、`见最新版本`不是合法正式状态。

## 6. 生命周期枚举

### 项目阶段

```text
CONCEPT → DEVELOPMENT → OUTLINE → SCRIPT → PREP → PRODUCTION → POST → RELEASE → ARCHIVED
```

### Artifact 状态

```text
DRAFT → IN_REVIEW → APPROVED → LOCKED → SUPERSEDED
```

`BLOCKED` 可以从任意状态进入。

### Review 决策

```text
RECOMMEND
CONDITIONAL_RECOMMEND
REWRITE
HOLD
REJECT
```

### Test Result

```text
PASS
CONDITIONAL_PASS
BLOCKED
FAIL
NOT_APPLICABLE
```

### 风险状态

```text
OPEN → MITIGATING → MITIGATED → ACCEPTED → CLOSED
```

`ACCEPTED` 不等于 `CLOSED`。P0 风险即使被接受，也不能放行生产和发布。

### Notice 状态与耦合

```text
DRAFT → OPEN → IN_PROGRESS → VERIFIED → CLOSED
```

`status` 表示 Notice Artifact 本身的审查生命周期；`notice_status` 表示该变更传播
事务的推进状态，两者不得混用。`coupling` 必须从 `UPSTREAM`、`BASELINE`、
`SCHEMA`、`RIGHTS`、`PRODUCTION` 中选择，并按上方 schema 生成表满足对应状态的
附加必填字段。

## 7. 权威层级

```text
用户/制片/合同约束
        ↓
项目 Manifest
        ↓
Full Bible
        ↓
结构、大纲、Scene Cards
        ↓
剧本主源
        ↓
镜头、资产、声音、字幕、制作包
```

下游文件不得静默覆盖上游事实。若下游发现事实错误，必须建立 Notice，先修正权威事实源，再同步下游。

## 8. 版本与基线

- `project_baseline`：Artifact 所依据的项目基线。
- `artifact_version`：该 Artifact 自身版本。
- `content_digest`：锁定或生产交接时用于证明内容未被静默替换的摘要。
- `compatibility_matrix`：记录 Artifact 是否已经针对当前基线复验。

禁止只写“最终版”“最新版”“当前版”。必须写明相对哪个基线。

## 9. 锁定规则

锁定分为三种：

| 类型 | 含义 |
|---|---|
| Fact Lock | 某个事实或连续性状态不可静默改变 |
| Artifact Lock | 某个完整文件版本不可覆盖 |
| Production Lock | 下游制作只能基于指定基线执行 |

锁定内容发生变化时：

```text
新版本 → Notice → 影响分析 → 下游同步 → 复验 → 新基线
```

## 10. Review Finding 最小结构

每条发现必须包含：

```text
finding_id
severity
evidence_location
failure_mechanism
downstream_impact
minimum_fix
verification_method
owner
status
```

不能用“加强人物”“优化节奏”“提升质感”作为完整修复建议。

## 11. 门禁

| 门禁 | 最低要求 |
|---|---|
| Bible Ready | Full Bible 核心域完整；无关键空白；事实状态明确 |
| Outline Ready | 因果脊柱、结构节点、EP/SC 依赖完整 |
| Script Ready | 每个正式场景映射到 `SC-*`；无未登记关键事实 |
| Review Ready | 范围、证据、Finding、结论和修订路径完整 |
| Production Ready | 剧本锁定；生产包、权利、版本和基线兼容 |
| Release Ready | 无未处理 P0；发布包同一兼容基线；批准记录完整 |

## 12. 自动与人工边界

### 自动检查

- 必填字段和合法枚举；
- ID 唯一性与格式；
- 项目 ID、版本和基线一致性；
- 上游引用是否存在；
- 剧本 `SC-*` 是否有对应 Scene Card；
- 旧版本 Artifact 是否被标记；
- 锁定文件是否缺少审查、批准或摘要；
- 占位符是否残留在锁定文件；
- 旧 Notice ID、旧许可证、旧状态是否残留。

### 必须人工判断

- 因果链是否成立；
- 主角是否主动选择；
- 对手是否具有真实策略；
- 人物行为是否符合动机与知识边界；
- 钩子是否公平且有兑现；
- 对白是否具有策略和潜台词；
- 主题是否被人物选择检验；
- 生产降级是否保留戏剧结果；
- 权利、法律、医疗和安全结论是否充分。

## 13. 兼容与迁移

旧文件可以被迁移，但不得被当作新契约的规范源。

迁移必须记录：

```text
旧字段/旧状态
新字段/新状态
迁移原因
受影响文件
复验方法
```

未完成迁移的文件必须标记 `MIGRATION_REQUIRED`，不能伪装为 `LOCKED`。
