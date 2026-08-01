# Professional Screenwriter Skill

> 控制平面唯一规范源：`governance/control-plane-contract.md`。
> 本 README 负责导航和使用说明，不重新定义全局 ID、状态或门禁。

> 面向长片、系列剧、竖屏微短剧、剧本重写、对白重写、
> 故事审查与 AI/实拍制作交接的结构化编剧工作流。
>
> 核心原则：
>
> ```text
> 先建立可验证的故事发动机，
> 再写结构，
> 再写场景，
> 再写剧本，
> 再交接制作。
>
> 任何上游事实变化，
> 都必须识别、同步并复验其下游影响。
> ```

---

# 这是什么

`professional-screenwriter` 是一个用于协助专业编剧开发与管理项目的 Skill 目录。

它不是单一的“剧本生成器”，也不是一套固定三幕公式。它提供一条可追溯的工作链：

```text
项目约束与受众
→ 项目清单
→ 故事 Bible
→ 格式与结构
→ 分集/长片大纲
→ 场景卡
→ 剧本主源
→ 对抗式审查
→ 版本与变更管理
→ AI/实拍制作交接
```

它适合：

- 从零开发一部长片、短片、剧集或竖屏微短剧
- 建立和维护 Story Bible
- 将模糊想法转化为可写、可审、可制作的大纲
- 重写场景、人物弧、对白、钩子或付费点
- 审查因果、人物动机、信息管理、连续性与生产可行性
- 将剧本交接为 AI 视频、实拍、分镜、资产、声音和后期生产包
- 管理来源、版本、上游事实变化与下游同步

它不适合：

- 未经结构开发就直接索要“完整长篇剧本”
- 将真实医疗、法律、执法、安全或历史信息当作无需核验的剧情事实
- 复制受版权保护的剧本、台词、角色、镜头、视觉资产或受保护表达
- 用“更大反转”“更惨人物”替代因果、人物选择与主题兑现
- 把已生成资产、旧 PDF、聊天记忆或单一搜索结果当作项目事实源

---

# 快速开始

## 新建项目

建议为每一个独立影视项目创建独立项目根目录：

```text
[[project-root]]/
├── governance/
├── development/
├── script/
├── production/
├── assets/
└── archive/
```

复制并优先填写：

```text
1. governance/project-manifest.md
2. development/story-bible.md
3. development/[[项目形式]]-outline.md
4. governance/source-links.md（如涉及外部事实）
5. governance/review-report.md
```

最小起步顺序：

```text
项目定义
→ 受众与格式
→ Logline
→ 主角发动机
→ 对抗力量
→ 核心关系
→ 世界规则与代价
→ 因果脊柱
→ 结构大纲
→ 场景卡
→ 剧本
```

## 写长片

阅读并使用：

```text
references/film-series-format.md
references/screenplay-format-cn-en.md
references/story-bible-templates.md
references/adversarial-review-rubric.md

templates/story-bible.md
templates/episode-outline.md
templates/scene-card.md
templates/feature-screenplay.fountain
templates/review-report.md

examples/feature-outline-example.md
examples/dialogue-rewrite-example.md
```

推荐路径：

```text
project-manifest
→ Story Bible
→ 长片因果脊柱
→ 八序列/三幕大纲
→ 场景卡
→ Fountain 剧本
→ 对抗式审查
→ 制作交接
```

## 写竖屏微短剧

阅读并使用：

```text
references/short-drama-playbook.md
references/hook-paywall-engine.md
references/screenplay-format-cn-en.md
references/adversarial-review-rubric.md
references/ai-production-handoff.md

templates/story-bible.md
templates/vertical-episode.md
templates/scene-card.md
templates/review-report.md

examples/vertical-drama-example.md
```

推荐路径：

```text
project-manifest
→ Story Bible
→ 季级承诺与核心问题
→ 分集问题地图
→ 单集入口钩子
→ 升级、局部兑现与集尾钩子
→ 付费点与付费后兑现
→ 竖屏剧本
→ 连续性/钩子审查
→ AI/实拍交接
```

## 重写一个场景或对白

先不要直接“润色台词”。

依次检查：

```text
1. 这场是谁的 POV？
2. 该人物想从谁那里得到什么？
3. 对方想要什么不同的结果？
4. 双方争夺的具体资源、信息、空间、许可或选择权是什么？
5. 开场谁有权力？
6. 结尾谁失去或得到什么？
7. 这场如何迫使下一场发生？
```

使用：

```text
templates/scene-card.md
templates/review-report.md
examples/dialogue-rewrite-example.md
references/adversarial-review-rubric.md
```

原则：

```text
对白不是内心字幕。

人物说话是为了获得、阻止、试探、威胁、交换、
隐瞒、逼供、夺权、索取原谅或改变选择。

若台词没有改变谁能做什么，
它通常还不是有效场景行动。
```

---

# 目录导览

```text
professional-screenwriter/
├── SKILL.md
├── README.md
│
├── references/
├── templates/
├── examples/
├── governance/
└── LICENSES/
```

## `SKILL.md`

Skill 的执行入口与路由规则。

它应定义：

- 接到不同任务时优先读取哪些文件
- 长片、剧集、竖屏短剧、对白重写、审查和制作交接的工作路径
- 故事事实、版本、变更与锁定的优先级
- 何时必须进行来源核验、上游通知和对抗式审查
- 何时可进入剧本、生产、后期或发布阶段

> `SKILL.md` 是本 Skill 的行为协议。
>
> 本 README 是面向人类使用者的导航入口。

## `references/`

方法与规范参考。

| 文件 | 用途 |
|---|---|
| `short-drama-playbook.md` | 竖屏微短剧的总体创作、节奏、钩子、情绪与生产思维 |
| `film-series-format.md` | 长片、系列剧、分集与格式差异 |
| `screenplay-format-cn-en.md` | 中英文剧本格式、Fountain、术语与可读性规则 |
| `hook-paywall-engine.md` | 入口钩子、过程钩子、集尾钩子、付费点与兑现 |
| `story-bible-templates.md` | Story Bible 的结构、事实管理与使用原则 |
| `adversarial-review-rubric.md` | 因果、人物、信息、连续性、生产与风险审查标准 |
| `ai-production-handoff.md` | 剧本到 AI/实拍资产、镜头、声音、UI 和后期的交接规则 |

> 规则主源原则：
>
> ```text
> 一个规则应该有一个规范主源。
>
> 若多个参考文件出现相同规则，
> 必须在 SKILL.md 或对应文件中说明：
> 哪个是主源，哪个只是摘要或应用说明。
> ```

## `templates/`

可复制的项目文件骨架。

| 文件 | 何时使用 |
|---|---|
| `feature-screenplay.fountain` | 撰写长片或横屏剧本主源时 |
| `episode-outline.md` | 开发剧集、系列或长片序列级大纲时 |
| `vertical-episode.md` | 开发单集竖屏微短剧时 |
| `story-bible.md` | 建立和维护人物、世界、关系、信息与连续性事实时 |
| `scene-card.md` | 在写剧本前设计每一场的目标、阻碍、策略、转折和结果时 |
| `review-report.md` | 对项目、大纲、剧本、场景或生产包执行正式审查时 |

> 模板不是“填空后自动成故事”的机器。
>
> 若主角没有目标、对抗力量没有策略、规则没有代价、
> 场景没有状态变化，填满表格也不会产生戏剧。

## `examples/`

原创示例，用于展示模板如何落地。

| 文件 | 演示内容 |
|---|---|
| `vertical-drama-example.md` | 竖屏短剧的集级结构、钩子、局部兑现与付费逻辑 |
| `feature-outline-example.md` | 长片因果脊柱、八序列、人物弧、世界规则与对抗审查 |
| `dialogue-rewrite-example.md` | 从失败台词到有效场景对白：目标、潜台词、道具、权力和转折 |

使用原则：

```text
示例用于学习结构与流程，
不用于复制其中的人物、情节、台词、世界、视觉或表达。
```

## `governance/`

项目治理、版本、来源与影响传播文件。

| 文件 | 唯一职责 |
|---|---|
| `project-manifest.md` | 项目当前身份、范围、约束、有效基线、锁定状态、负责人、风险与下一步 |
| `upstream-notices.md` | 单次上游事实变化的影响分析、同步任务、复验、审批与回滚 |
| `source-links.md` | 外部主张、来源、证据、限制、交叉验证、权利与复核 |
| `change-log.md` | 按版本汇总已确认的项目重要变化、废弃项、破坏性变更与迁移 |

它们的关系：

```text
外部来源发现或推翻一个事实
→ source-links.md

事实需要改变项目设定
→ upstream-notices.md

通知完成、下游同步并形成新基线
→ change-log.md

当前项目究竟使用哪个基线、文件和阶段
→ project-manifest.md
```

## `LICENSES/`

许可证、第三方声明与资产权利记录。

该目录只应存放：

```text
- 本 Skill 的许可证
- 第三方材料、工具、字体、模板或库的许可声明
- 素材授权、署名、使用范围与限制
- 权利相关说明
```

该目录不得存放：

```text
- Story Bible
- 剧本
- 场景卡
- 来源研究日志
- 上游变更通知
- 日常项目决策
```

---

# 推荐项目目录

本 Skill 是“可复用方法与模板库”；具体创作项目应位于独立项目根目录中。

```text
[[project-root]]/
├── README.md
│
├── governance/
│   ├── project-manifest.md
│   ├── source-links.md
│   ├── upstream-notices.md
│   ├── change-log.md
│   ├── continuity-log.md
│   └── rights-register.md
│
├── development/
│   ├── story-bible.md
│   ├── feature-outline.md
│   ├── season-outline.md
│   ├── episode-outlines/
│   ├── scene-cards/
│   ├── information-matrix.md
│   ├── timeline.md
│   └── review-reports/
│
├── script/
│   ├── master/
│   │   └── [[project]].fountain
│   ├── revisions/
│   └── exports/
│
├── production/
│   ├── handoff/
│   ├── breakdowns/
│   ├── shot-lists/
│   ├── storyboards/
│   ├── voice/
│   ├── subtitles/
│   └── ui/
│
├── assets/
│   ├── characters/
│   ├── locations/
│   ├── props/
│   ├── wardrobe/
│   └── references/
│
└── archive/
    ├── superseded/
    └── released/
```

> 项目文件夹可按规模简化。
>
> 但不得简化掉以下事实控制链：
>
> ```text
> 当前项目配置
> → 当前故事事实
> → 当前剧本
> → 变更记录
> → 来源与权利边界
> → 制作交接
> ```

---

# 工作流

## 第一阶段：定义问题

在任何大纲或剧本前，先回答：

```text
项目为谁而做？
它承诺什么体验？
采用什么格式、画幅、时长、语言和商业模式？
什么是不可协商约束？
什么明确不做？
什么成功结果可以被验证？
```

创建：

```text
governance/project-manifest.md
```

若项目依赖外部真实信息，同时创建：

```text
governance/source-links.md
```

## 第二阶段：建立故事发动机

不要从“发生很多事”开始。

先建立：

```text
主角：
想要什么？
为什么现在必须要？
最初采取什么错误或有限策略？
真正缺少什么？
失败会失去什么？

对抗力量：
想要什么？
有什么资源？
如何主动反制？
不能做什么？
它如何代表主题的对立命题？

世界：
有哪些规则？
规则的成本是什么？
规则如何限制简单解决方案？

关系：
谁试图控制谁？
谁掌握什么秘密？
每段关系会在什么选择上破裂或改变？
```

创建：

```text
development/story-bible.md
```

## 第三阶段：建立因果结构

结构不是页码填空，而是压力下的选择链。

```text
旧状态
→ 触发事件
→ 主角不可逆选择
→ 对手反制
→ 重大后果
→ 中点：问题或策略改写
→ 新策略
→ 第二次失败
→ 危机：轻易选项消失
→ 高潮：主角付出核心代价的选择
→ 新常态
```

创建：

```text
development/feature-outline.md
或
development/season-outline.md
development/episode-outlines/
```

## 第四阶段：拆成场景

每场至少要能回答：

```text
谁的 POV？
他/她想得到什么？
谁或什么阻止？
采用什么策略？
策略怎样失败或升级？
发生了什么转折？
进入与退出状态如何不同？
下场为何必然发生？
```

创建：

```text
development/scene-cards/
```

## 第五阶段：写剧本

剧本主源应只在大纲、人物状态、信息状态与场景功能可追溯时进入。

```text
script/master/[[project]].fountain
```

写作要求：

- 动作描述可拍摄、可生成、可剪辑
- 对白是人物行动，不是作者说明
- 关键规则、危机条件、选择和后果在必要处清楚表达
- 每场必须至少改变目标、策略、资源、信息、权力或代价之一
- 任何新事实都必须回写到 Bible 或以正式变更流程处理

## 第六阶段：执行对抗式审查

使用：

```text
templates/review-report.md
references/adversarial-review-rubric.md
```

审查至少覆盖：

```text
- 因果是否成立
- 主角是否主动
- 对手是否有策略
- 人物是否按其知识行动
- 世界规则是否有成本且不临时变形
- 时间线、道具、服装、伤病、地点是否连续
- 钩子是否兑现
- 高潮是否来自主角选择
- 生产方案是否可行
- 是否存在权利、安全、敏感内容或事实风险
```

## 第七阶段：管理变化

当变化影响事实、结构、知识、时间线、资产、生产或权利时：

```text
1. 在 Story Bible 或权威事实源中定义新事实
2. 创建 governance/upstream-notices.md 条目
3. 枚举所有受影响下游文件
4. 更新大纲、场景卡、剧本、资产、声音、字幕和生产包
5. 运行连续性与对抗式审查
6. 更新 governance/change-log.md
7. 在 project-manifest.md 指向新的有效基线
```

不要：

```text
只改剧本中的一处台词，
却留下旧大纲、旧场景卡、旧资产和旧字幕。

这不是修订；
这是制造未来矛盾。
```

## 第八阶段：制作交接

进入 AI 或实拍制作前，确认：

```text
剧本基线已锁定或处于受控版本；
角色、地点、服装、伤病、道具状态明确；
镜头、分镜、声音、UI、字幕和资产包使用同一版本；
所有可见文字、屏幕、地图、UI 可后期合成；
AI 风险已处理：角色一致性、手部、道具、口型、复杂群像、画幅安全区；
实拍风险已处理：地点、演员、排期、天气、动作、安全、许可与保险；
所有第三方素材、品牌、肖像、音乐、字体和声音均已处理权利边界。
```

阅读：

```text
references/ai-production-handoff.md
```

---

# 事实、版本与变更

## 权威层级

```text
明确用户/制片约束
→ project-manifest.md
→ Story Bible
→ 大纲 / 场景卡
→ 剧本主源
→ 生产文件与资产
→ 历史草稿与旧资产
```

这不是说 `project-manifest.md` 替代 Story Bible。

它的职责是声明：

```text
当前哪个 Bible、哪个大纲、哪个剧本、哪个生产包有效；
项目处于什么阶段；
哪些内容已经锁定；
下一步可以做什么；
什么正在阻断项目。
```

## 四个治理文件

| 文件 | 用于什么 | 不用于什么 |
|---|---|---|
| `project-manifest.md` | 当前项目入口、范围、约束、基线、阶段与负责人 | 完整故事设定或逐次历史 |
| `source-links.md` | 外部来源、主张、证据、限制和复核 | 收藏随机 URL 或取代专业意见 |
| `upstream-notices.md` | 单次重大变更的影响分析与下游同步 | 版本摘要或随手修订 |
| `change-log.md` | 已确认版本之间的重要变化 | 原始 Git 提交或未批准想法 |

## 变更等级

规范定义、Notice 要求、最低复验与批准门槛统一见
[`governance/control-plane-contract.md` §7.2](governance/control-plane-contract.md#72-变更等级与最低门禁)。

---

# 对抗式审查

每次准备“写下一步”之前，先问：

## 故事

- 主角是否真的想要明确目标，而不是被事件推着走？
- 对抗者是否有独立目标、资源、限制和反制策略？
- 每个关键事件是否由前一事件导致，而非偶然发生？
- 中点是否改变主角理解问题或解决策略的方式？
- 危机是否剥夺轻易选项？
- 高潮是否迫使主角支付开场时不愿支付的代价？

## 人物

- 每个关键人物在当前场景知道什么、相信什么、害怕失去什么？
- 人物是否在按已知信息行动？
- 关系变化是否通过实际选择和后果发生，而非口头宣布？
- 若删除某个角色，是否会有功能缺失？若不会，该角色可能只是冗余。

## 对白

- 这段对白中，谁想让谁做什么？
- 是否有具体可争夺对象：信息、许可、道具、位置、沉默、信任或选择权？
- 台词是否只是作者解释？
- 角色是否说得过于完整，跳过了后续戏剧压力？
- 结尾是否真的改变权力、资源、关系或下一步行动？

## 连续性

- 谁在哪里？何时？带着什么？伤在哪里？知道什么？
- 道具是否无解释地复制、消失或易主？
- 时间、天气、服装、伤病、消息和移动是否可能？
- 已删除或改变的伏笔，后续是否仍在回收？

## 制作

- 这个段落是否能以当前预算、地点、演员、时间、实拍或 AI 能力完成？
- 是否依赖复杂手部、长口型、群像、可读小字、危险动作或不稳定环境？
- 是否可以通过局部镜头、声音、反应、剪辑或后期 UI 达到同等戏剧目的？
- 已生成或已拍资产若与新事实冲突，是否有明确处理决定？

## 风险与权利

- 这是事实、推论、创作选择，还是未验证假设？
- 是否有需要专业、法务、平台或安全审阅的内容？
- 是否把可访问的网页、图片、人物或品牌误当作可自由使用素材？
- 是否存在不必要、可模仿或高风险的操作性细节？

---

# 使用示例

## 示例 A：请求长片开发

输入：

```text
我想写一部 105 分钟的港口灾难悬疑片。
主角是一名被停职的安全工程师。
目标是中国普通流媒体观众，预算有限。
```

推荐产出顺序：

```text
1. project-manifest.md
2. story-bible.md
3. feature-outline-example.md 的同类长片大纲
4. scene-card.md 集合
5. feature-screenplay.fountain
6. review-report.md
7. AI/实拍 handoff
```

不应立刻产出：

```text
100 页完整剧本，
同时假定港口、救援、法律、工程和医疗细节全部正确。
```

## 示例 B：请求竖屏付费短剧

输入：

```text
写一部 60 集、每集 90 秒、9:16 的复仇爱情短剧。
第 8 集需要付费点。
```

推荐产出顺序：

```text
1. project-manifest.md：格式、时长、付费模型、受众、画幅
2. story-bible.md：身份、关系、秘密、世界边界
3. hook-paywall-engine.md：入口/过程/集尾/付费/兑现地图
4. vertical-episode.md：逐集开发
5. scene-card.md：关键付费点与高潮场景
6. review-report.md：钩子兑现与连续性审查
7. production handoff：9:16 构图、资产锚点、字幕与 UI
```

## 示例 C：请求对白重写

输入：

```text
把这场姐弟争吵写得更有潜台词。
```

先确认：

```text
- 这场发生在故事的哪个节点？
- 他们各自要得到什么？
- 谁掌握哪项信息？
- 他们争夺什么具体对象或决定？
- 该场结尾必须让谁失去/获得什么？
```

再使用：

```text
examples/dialogue-rewrite-example.md
templates/scene-card.md
```

不要只把直白台词改成谜语。

---

# 贡献与维护

## 修改原则

- 先确定文件的唯一职责，再增加内容
- 不复制粘贴规则到多个参考文件；指定规范主源
- 模板变化必须检查示例、README 与 SKILL 路由是否需要同步
- 结构、事实、格式、版本、生产或权利变化必须评估是否触发 `upstream-notices.md`
- 新增外部事实或专业规则必须记录到 `source-links.md`
- 删除或迁移文件必须更新链接、路径、目录树和 `change-log.md`
- 不用未授权受保护内容作为示例、模板、视觉资产或训练素材

## 新增模板的最低要求

每个新增模板应包含：

```text
- 用途
- 适用范围
- 不适用范围
- 输入要求
- 输出定义
- 版本与负责人字段
- 事实源或依赖说明
- 锁定/验收条件
- 对抗式审查清单
```

## 新增示例的最低要求

每个新增示例应：

```text
- 明确标记为原创示例；
- 不复用受版权保护的故事、角色、台词或镜头；
- 对应至少一个现有模板；
- 显示“为什么这样写”，而不是只给成品；
- 包含失败模式或对抗式审查；
- 说明不可直接复制的内容边界。
```

---

# 许可与权利

本 Skill 的正式公开许可方为 `LaoYu-Professional-Screenwriter`，由 GitHub 账户 `YuYingRay` 维护。

官方来源：[github.com/YuYingRay/LaoYu-Professional-Screenwriter](https://github.com/YuYingRay/LaoYu-Professional-Screenwriter)  
许可证：CC BY 4.0，详见 [`LICENSE`](LICENSE) 和 [`LICENSES/skill-license.md`](LICENSES/skill-license.md)。

许可证、第三方声明和资产授权记录位于：

```text
LICENSES/
```

使用者应在使用前确认：

```text
- 本 Skill 自身的许可范围；
- 第三方模板、工具、字体、素材和示例的许可；
- 图像、音乐、声音、地图、UI、品牌、人物肖像和文本的使用权；
- AI 生成材料的输入、输出、平台条款、模仿与肖像风险；
- 目标平台、地区和用途所需的法律、隐私、安全与分级要求。
```

本 Skill 不提供法律、医疗、工程、安全、金融、执法或心理健康专业意见。

---

# 当前架构状态

当前目录的核心能力已覆盖：

```text
格式定义
故事开发
结构设计
场景设计
剧本格式
对白重写
短剧钩子与付费逻辑
对抗式审查
来源与证据管理
上游变更传播
版本日志
项目清单
AI/实拍交接
```

在宣布该架构“稳定完成”前，建议确认：

- [ ] `SKILL.md` 已定义任务路由、事实优先级、锁定规则和强制审查条件
- [ ] `governance/` 已存在并包含 `project-manifest.md`、`source-links.md`、`upstream-notices.md`、`change-log.md`
- [ ] `LICENSES/` 不再存放研究、故事、变更或项目治理文件
- [ ] 每个 `references/` 文件具有单一职责和明确规范主源
- [ ] 至少存在一个长片端到端测试项目
- [ ] 至少存在一个竖屏短剧端到端测试项目
- [ ] 测试可证明：上游事实变化会同步影响 Bible、大纲、场景卡、剧本与生产交接
- [ ] 所有外部事实可追溯到来源、主张、限制与复核状态
- [ ] 所有 P0 架构问题已修复；开发阶段若接受风险，必须标记 `ACCEPTED_RISK`，不得放行生产或发布

---

# 最终原则

```text
专业编剧工作流的目标不是让文件越来越多。

它的目标是让每一份文件都承担一个明确职责：

项目清单知道当前要做什么；
Story Bible 知道什么是真的；
大纲知道为什么事件发生；
场景卡知道人物如何争取目标；
剧本知道观众实际看见什么；
审查报告知道哪里会失败；
来源日志知道事实凭什么成立；
变更通知知道改动会影响什么；
变更日志知道版本之间发生了什么；
生产包知道怎样把故事做出来。

当这些文件彼此一致时，
团队才能快速创作而不失去因果、连续性、权利边界与制作控制。
```
