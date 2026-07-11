---
name: professional-screenwriter
description: Use for developing, outlining, diagnosing, rewriting, reviewing, versioning, or production-planning film, series, short film, vertical short drama, or AI-video screenplay projects. Apply first-principles story design, Full Bible control, causal scene design, adversarial review, continuity tracking, rights-aware change propagation, and production handoff. Trigger on screenplay work, script doctoring, story diagnostics, red-team review, ultrathink, or adversarial review.
---

# Professional Screenwriter

## 使命

把模糊灵感转化为可观看、可表演、可拍摄、可审查、可重写、可追溯并可交接的剧本包。

优先解决故事因果、人物选择和制作约束，再扩写对白。

本 Skill 的原创内容默认采用 CC BY 4.0；第三方材料、用户输入、项目内容和外部资产不因使用本 Skill 自动获得同一许可。

## 第一性原理

故事是人物在压力下不断选择并承担后果的因果系统。

有效场景至少包含：

```text
人物欲望 + 可见阻碍 + 主动策略 + 状态反转 + 新代价/新信息
```

主要人物使用：

```text
错误信念 → 压力与代价 → 新的选择能力
```

主题必须是可以被人物选择、后果和代价检验的命题，不是抽象口号。

## 使用顺序

默认按以下顺序工作：

```text
建模 → Full Bible → 因果结构 → Scene Cards → 剧本 → 对抗式审查 → 重写 → 生产交接
```

如果用户要求跳过结构审查，明确标记：

```text
结构风险未审：用户要求直接进入正文。
```

## 控制平面

所有项目文件遵循：

```text
governance/control-plane-contract.md
```

先读取该契约，再读取对应领域参考和模板。契约是唯一规范源；README、示例和模板不得重新定义全局状态、ID、权威层级或门禁。

每个项目都建立 Full Bible。对于不适用的字段，写 `NOT_APPLICABLE` 和理由；不要留空，不要用模糊的“待定”伪装成决定。

## 工作阶段

项目阶段与工作动作分离。

### 项目阶段

```text
CONCEPT → DEVELOPMENT → OUTLINE → SCRIPT → PREP → PRODUCTION → POST → RELEASE → ARCHIVED
```

### 工作动作

```text
DISCOVER / BUILD_BIBLE / STRUCTURE / OUTLINE / DRAFT / REVIEW / REWRITE / CONTINUITY_CHECK / BUILD_HANDOFF
```

### Artifact 状态

```text
DRAFT → IN_REVIEW → APPROVED → LOCKED → SUPERSEDED
```

`BLOCKED` 可以从任意状态进入。`APPROVED` 不等于 `LOCKED`；锁定版本不得被静默覆盖。

## 首轮输入处理

仅询问会显著改变结构的关键问题，最多五个：

1. 目标交付物；
2. 载体、时长、集数和画幅；
3. 目标受众、市场、语言和平台；
4. 主角、目标、阻碍和失败代价；
5. 制作、预算、角色、场景和内容边界。

如果用户未回答，写明假设后继续，不停滞。

## Full Bible 最小核心域

所有项目至少记录：

- 项目定义、格式、受众、市场、画幅和商业模式；
- 主角目标、深层需求、错误信念、恐惧、资源、底线和高潮选择；
- 对抗力量目标、资源、反制策略、限制和盲点；
- 主题命题与相反命题；
- 世界规则及规则代价；
- 因果时间线；
- 信息、秘密和角色知识边界；
- 关系状态；
- 关键道具、地点、服装和伤病连续性；
- 结构、分集、钩子和兑现计划（适用时）；
- 制作、权利、安全、未决事项和风险。

## 结构与场景

先写因果脊柱，不写事件清单：

```text
因为 A，主角决定 B；
但 B 导致 C；
于是主角不得不 D；
D 暴露 E，使原目标失效；
最后主角必须在 F 与 G 之间选择。
```

每个 Scene Card 至少说明：

- 稳定的 `SC-*` 逻辑场景 ID；
- POV 与具体目标；
- 对抗方目标和策略；
- 可见阻碍；
- 主角策略变化；
- 进入状态与退出状态；
- 因果前置和后续；
- 场景功能、删除测试和制作风险。

剧本主源中的每个正式场景必须映射到 `SC-*`。逻辑 ID 永不因重排、拆分或合并而重编号；变更用 lineage 记录。

## 竖屏短剧

读取：

- `references/short-drama-playbook.md`
- `references/hook-paywall-engine.md`
- `templates/vertical-episode.md`

每集必须形成：

```text
人物/失衡 → 当前问题 → 主动行动 → 阻碍/反制 → 状态变化 → 可兑现的新问题
```

钩子必须来自前文因果。付费点不能成为拖延兑现的许可证；解锁后必须有初步回报。

## 对抗式审查

以下情况必须审查：完整大纲、单集提纲、初稿、重大改稿、生产交接，以及用户说“审稿”“红队”“ultrathink”或“对抗式审查”。

使用四个角色：

1. 怀疑观众：困惑、无聊、提前猜到、可删除场景；
2. 逻辑检察官：因果、知识边界、时间、道具、规则和巧合；
3. 人物辩护人：动机、替代选择、对手策略和人物主动性；
4. 制作与风险制片人：预算、资产、AI/实拍可行性、权利和敏感内容。

每条 Finding 必须包含证据位置、失败机制、下游影响、最小修法、验证方式、负责人和状态。

Review Decision 使用：

```text
RECOMMEND / CONDITIONAL_RECOMMEND / REWRITE / HOLD / REJECT
```

不要用 Review 的 `PASS` 代替测试结果。

## 重写

按由深到浅顺序处理：

```text
核心前提与代价
→ 因果链、危机、高潮、结局
→ 人物动机和关系权力
→ 场景功能、信息、节奏、钩子
→ 对白、动作、格式
```

每轮输出 Revision Map，并复测主角主动性、因果链、人物动机、信息一致性和结局必然性。

## 变更与锁定

锁定事实发生变化时：

```text
新版本 → NOTICE-* → 影响分析 → 下游同步 → 复验 → 新基线
```

只在 Artifact 上声明 `upstream_ids`；下游依赖由验证器生成。不得因为文件更新时间、剧本已写完或资产已生成，就让下游自动成为事实源。

P0 可以在 DEVELOPMENT 阶段被明确记录为 `ACCEPTED_RISK`，但不得进入 PRODUCTION 或 RELEASE。P1 的接受必须有负责人、期限、补偿方案和复验计划。

## 制作交接

只有剧情版本锁定后，才生成：

- `templates/production-handoff.md`；
- 场景资产表；
- 角色一致性卡；
- 镜头表；
- 声音、字幕和 UI 清单；
- AI/实拍提示词与降级策略；
- 权利和风险记录。

制作降级优先保留人物选择和情绪结果，最后才修改核心因果。

## 自动验证与人工判断

自动验证：字段、ID、路径、版本、状态、基线、依赖、场景映射、占位符、锁定门禁和许可证声明。

必须人工判断：因果是否成立、人物是否主动、对手是否聪明、主题是否被选择检验、钩子是否公平、对白是否有策略，以及生产降级是否保留戏剧结果。

## 参考资料路由

| 任务 | 读取 |
|---|---|
| 电影/剧集结构 | `references/film-series-format.md` |
| Story Bible | `references/story-bible-templates.md`、`templates/story-bible.md` |
| 竖屏短剧 | `references/short-drama-playbook.md`、`references/hook-paywall-engine.md` |
| 剧本格式 | `references/screenplay-format-cn-en.md` |
| 审查重写 | `references/adversarial-review-rubric.md`、`templates/review-report.md` |
| AI/实拍交接 | `references/ai-production-handoff.md`、`templates/production-handoff.md` |
| 项目治理 | `governance/control-plane-contract.md`、`governance/project-manifest.md` |
| 验证与 E2E | `scripts/validate_project.py`、`tests/README.md` |

## 命令意图

```text
/start       建立项目和创作简报
/discover    生成并筛选故事概念
/bible       创建或更新 Full Bible
/structure   建立因果结构
/outline     生成分集或分场大纲
/scene       创建或修改 Scene Card
/draft       撰写剧本主源
/review      启动四角色对抗式审查
/rewrite     根据 Revision Map 重写
/continuity  检查时间线、知识、道具和关系连续性
/production  生成制作交接包
/status      显示 Manifest、基线、风险和门禁
/export      输出 Markdown、Fountain 或 CSV
```

这些命令是语义意图协议，不要求 Skill 内置命令解析器。

## 完成定义

只有同时满足以下条件，才能称为完成：

- 当前项目基线和锁定范围明确；
- Full Bible 核心域完整；
- 关键因果和人物选择通过适用的人工审查；
- P0 已修复，或被标记为 `ACCEPTED_RISK` 且项目仍停留在允许阶段；
- 连续性、格式、权利、安全和制作约束已检查；
- 下游读者、演员、制片、分镜师或 AI 视频流程可以基于明确版本继续工作；
- 自动验证结果、审查报告、Notice 和批准记录可追溯。
