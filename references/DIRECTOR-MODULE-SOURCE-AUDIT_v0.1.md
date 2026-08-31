# Director Module Source Audit v0.1

> 文档状态：`RESEARCH_DRAFT`
> 审计日期：2026-08-31
> 对抗复核：2026-08-31，Codex 独立审查 + Claude Code Fabel 5 只读复核；本次只修研究文本，不提升规范效力。
> 适用对象：`professional-screenwriter` 的候选导演模块
> 规范效力：无。本文件不修改 `SKILL.md`、现行 reference、模板、验证器或生产基线。
> 权利说明：本文件是来源审计和方法比较，不构成法律意见；第三方许可证与平台能力仍应在实际吸收或分发前复核。

## 1. 审计问题

本次审计不以仓库热度、Prompt 数量或展示片播放量判断专业性，而回答五个问题：

1. 来源能否帮助把剧本因果转译为可见镜头叙事？
2. 它提供的是导演方法、模型适配、Prompt 语法、案例语料，还是执行 API？
3. 主张是否来自官方事实、可复现实验、作者经验或营销文案？
4. 许可证是否允许研究、改编、复制或分发？
5. 哪些内容应吸收为原则，哪些只能作为假设，哪些必须拒绝？

## 2. 第一性原理与证据层级

导演模块需要完成的核心转译是：

```text
剧本因果
→ 观众必须获得的信息与情绪变化
→ 镜头功能与 Coverage
→ 空间、调度、景别、切点和声音
→ 模型可执行输入
→ 可剪、可理解的成片证据
```

证据不能压成单一高低等级。必须先判断来源角色，再判断当前主张验证状态：

| 轴 | 标签 | 含义 |
|---|---|---|
| 来源角色 | `OFFICIAL_MODEL` | 模型开发方对模型目标或上限的第一方说明；不等于某平台入口已开放 |
| 来源角色 | `ACCOUNT_OBSERVATION` | 当前账户、当前日期和当前 UI 的可见能力；不等于模型通用上限 |
| 来源角色 | `PROJECT_OUTPUT` | 冻结输入对应的真实输出与审片结论；只证明该样本 |
| 来源角色 | `LICENSED_METHOD` / `ARCHITECTURE_REFERENCE` | 许可明确的方法或架构；不等于已在本项目验证有效 |
| 来源角色 | `COMMUNITY_CORPUS` / `USER_CORPUS` | 经验语料或本地采集资产；只能生成候选假设 |
| 来源角色 | `INTERNAL_CANDIDATE` / `EXECUTION_ADAPTER` | 本 Skill 的候选设计，或仅负责调用执行的外壳 |
| 验证状态 | `FACT_VERIFIED` | 当前表述可由可定位的一手来源直接支持 |
| 验证状态 | `SAMPLE_VERIFIED` | 输入、输出和结论可定位；仅限冻结样本 |
| 验证状态 | `PARTIAL` | 来源或部分事实已核验，但入口、效果或复现链仍不完整 |
| 验证状态 | `UNVERIFIED` | 尚无本项目结果或无法定位原始证据 |
| 验证状态 | `CONFLICTED` | 同源内部、与官方事实或与当前实测存在冲突 |

冲突时不互相覆盖：官方资料裁定“模型方声称什么”，账户观察裁定“当前入口显示什么”，项目输出裁定
“这一次实际发生什么”。一次真实输出可高强度证明单样本，不能证明稳定成功率。

### 2.2 处置标签

| 标签 | 允许动作 |
|---|---|
| `ADOPT_FACT` | 作为对应平台/版本的技术事实，但需保留适用范围和核验日期 |
| `ADAPT_METHOD` | 提取抽象机制，重新表达并进行本项目验证 |
| `SAMPLE_CORPUS` | 仅抽样研究输入—输出模式，不批量吸收 |
| `ARCHITECTURE_ONLY` | 只研究模块边界或流程，不复制代码/文本 |
| `EXECUTION_ONLY` | 只在未来需要 API/批处理时评估，不进入导演知识层 |
| `RESEARCH_ONLY` | 仅供内部研究，不复制受保护表达 |
| `REJECT` | 不进入规范、模板、Prompt 或能力声明 |

## 3. 来源总表

### 3.1 官方能力与项目实证

| ID | 来源 | 来源角色 | 验证状态 | 权利/使用边界 | 可吸收知识 | 拒绝项 | 处置 |
|---|---|---|---|---|---|---|---|
| SRC-DIR-001 | [ByteDance Seedance 2.0 官方发布](https://seed.bytedance.com/en/blog/seedance-2-0-%E6%AD%A3%E5%BC%8F%E5%8F%91%E5%B8%83) | OFFICIAL_MODEL | FACT_VERIFIED | 官方网页用于事实引用；不复制展示素材 | 最多 9 图、3 视频、3 音频；15 秒多镜头音画输出；可参考文本分镜、景别、运镜、构图和声音 | 把官方展示片当作普通用户每次都能达到的稳定结果 | ADOPT_FACT |
| SRC-DIR-002 | [ByteDance Seedance 2.5 官方页](https://seed.bytedance.com/en/seedance2_5) | OFFICIAL_MODEL | FACT_VERIFIED | 官方网页用于事实引用；平台入口能力需另验 | 最长 30 秒叙事、参考控制、摄影语言、表演调度和编辑能力的官方目标 | 推断豆包 App、第三方 API 或特定账户必然暴露全部功能 | ADOPT_FACT |
| SRC-DIR-003 | 余老师于 2026-08-31 对豆包 App 当前账户的 UI 观察与确认；仓库内尚无冻结截图/任务 ID | ACCOUNT_OBSERVATION | PARTIAL | 用户提供的内部项目证据；不公开分发账户信息 | 当前入口可选择 Seedance 2.0 Fast 的 9 图/15 秒，并可选择 Seedance 2.5 做15秒正片测试 | 将当前 UI 状态永久写死为模型通用上限；在补齐冻结截图前标作可复查实测 | ADOPT_FACT |
| SRC-DIR-004 | `F:/AI 人工智能/010 个人实践—AI项目案例/吉米 玲珑 海龟角色图/剧本项目/production/video/EP1/FULL-SEEDANCE25-15S/raw/P1A/SHOT-EP001-FULL-P1A_A01.mp4`；SHA-256 `02839097F0DCE310E1EE83909BB514F023CE6B1AA6901AE1F4E895CC3F47B793`；对应执行卡 `EXECUTION_CARD_SHOT-EP001-FULL-P1A_A01_v0.3.0.md` 与 Prompt SHA-256 `A657692DB77406FCFB32D63D3C3D2368173F4026D2395B6AE17714B52A7618C7` | PROJECT_OUTPUT | SAMPLE_VERIFIED | 项目原创/用户控制的生产证据；执行卡记录 2026-08-31、豆包 App Seedance 2.5、15秒、9:16、原生音频、5图 | 该样本保持了角色与连续运动，但未形成足够景别覆盖和切镜语言；它仍可作为原任务的历史候选，不作为导演模块多镜头能力证明 | 把一次持续镜头结果升级为“Seedance 2.5 不会多镜头”，或追溯改判其原生产门禁 | ADAPT_METHOD |

### 3.2 导演、Coverage 与制作方法

| ID | 来源 | 许可证/状态 | 来源角色 | 验证状态 | 可吸收知识 | 拒绝项 | 处置 |
|---|---|---|---|---|---|---|---|
| SRC-DIR-005 | [wuwangzhang1216/DirectorSKILL](https://github.com/wuwangzhang1216/DirectorSKILL) | MIT；保留版权与许可声明 | LICENSED_METHOD | PARTIAL | function-first 镜头设计；blocking；coverage；轴线；剪辑动机；镜头计划字段；风险与降级 | 复制具体导演风格表达、电影镜头、角色、台词或情节；把 named-director overlay 当成默认工作流 | ADAPT_METHOD |
| SRC-DIR-006 | [billpar/ai-cinematic-pipeline](https://github.com/billpar/ai-cinematic-pipeline) | MIT | LICENSED_METHOD | PARTIAL | beat-to-shot、关键帧链、角色/场景一致性、音频和后期流水线 | 以仓库的“production-tested”自述替代独立验证 | ADAPT_METHOD |
| SRC-DIR-007 | [LinHao-city/StoryMind](https://github.com/LinHao-city/StoryMind) | AGPL-3.0 | ARCHITECTURE_REFERENCE | PARTIAL | LLM 规划镜头表后再调用多供应商生成的系统边界 | 复制代码、提示词或紧耦合实现进入 CC BY Skill；把演示结果当作导演质量证明 | ARCHITECTURE_ONLY |

### 3.3 Seedance 专用方法与 Prompt 编译

| ID | 来源 | 许可证/状态 | 来源角色 | 验证状态 | 可吸收知识 | 拒绝项 | 处置 |
|---|---|---|---|---|---|---|---|
| SRC-DIR-008 | [AtlasCloudAI/awesome-seedance-2.5-prompts-skills](https://github.com/AtlasCloudAI/awesome-seedance-2.5-prompts-skills) | CC BY 4.0 | LICENSED_METHOD | PARTIAL | 先选创作路由；完整分镜图 R2V；角色/场景/道具角色绑定；Shot 1/2/3；硬切、匹配剪辑、遮挡和插入镜；阶段可见终态 | Atlas Cloud 执行、密钥、轮询、计费状态机；将其旧模型可用性描述当作当前豆包事实 | ADAPT_METHOD |
| SRC-DIR-009 | [dexhunter/seedance2-skill](https://github.com/dexhunter/seedance2-skill) | MIT | LICENSED_METHOD | PARTIAL | 多模态引用、提示词结构和操作路径的对照材料 | 未能追溯到官方原文的能力主张；把文档转述当成模型保证 | ADAPT_METHOD |
| SRC-DIR-010 | [jnMetaCode/ai-shortfilm-prompts](https://github.com/jnMetaCode/ai-shortfilm-prompts) | 混合许可；必须逐文件、逐片段确认。凡 Mx-Shell 引文、转录、原 Prompt 或可识别近似表达，无论位于 `prompts/`、methodology、FAQ 或其他路径，均按 All Rights Reserved 隔离 | LICENSED_METHOD | PARTIAL | 仅从许可明确且不含受限表达的片段干净重述：逐秒单镜头与逐 Shot 多镜头分流；景别、构图、运镜、动作四字段；多镜头前锁定角色和氛围；Prompt 编译结构 | 原始/近似 Prompt 批量复制；“呼吸式手持永远加入”；摄影机型号必然数量级提升；同源 LLM 自评冒充视频验证；已过时的豆包时长口径 | ADAPT_METHOD（经片段级许可核对）/ RESEARCH_ONLY（ARR 范围） |
| SRC-DIR-011 | [songguoxs/seedance-prompt-skill](https://github.com/songguoxs/seedance-prompt-skill) | GitHub 未识别 LICENSE 文件；README 的许可表述不足以消除分发风险 | COMMUNITY_CORPUS | UNVERIFIED | 时间段表达、`@图片`绑定、参考类型和中文 Prompt 示例 | 直接复制文本；将时间段自然语言误当作剪辑点；缺少 Coverage/剪辑因果仍宣称导演方法 | RESEARCH_ONLY |
| SRC-DIR-012 | [rich5000/seedance-prompt-guide](https://github.com/rich5000/seedance-prompt-guide) | MIT | COMMUNITY_CORPUS | UNVERIFIED | 轻量中文 Prompt 对照、产品/一镜到底/编辑场景词法 | 将小型指南升级为能力规范；缺少真实视频验证 | SAMPLE_CORPUS |
| SRC-DIR-013 | [YouMind-OpenLab/awesome-seedance-2-prompts](https://github.com/YouMind-OpenLab/awesome-seedance-2-prompts) | 仓库 LICENSE 为 CC BY 4.0；具体社区贡献仍需检查单项来源 | COMMUNITY_CORPUS | UNVERIFIED | 大规模案例可用于抽样归类：镜头、广告、动漫、UGC、meme 等 Prompt 模式 | 整库吸收；用 2,000+ 数量或热门案例证明方法有效；忽略幸存者偏差与失败样本 | SAMPLE_CORPUS |

### 3.4 执行适配器与产品外壳

这些来源的来源角色统一为 `EXECUTION_ADAPTER`。它们只解决请求提交、API 参数、队列或产品界面，
不解决镜头为什么存在、何时切换以及观众是否看懂；其许可证可核验也不构成导演效果验证。

| ID | 来源 | 许可证/状态 | 可研究内容 | 不进入导演模块的内容 | 处置 |
|---|---|---|---|---|---|
| SRC-DIR-014 | [Anil-matcha/seedance2-comfyui](https://github.com/Anil-matcha/seedance2-comfyui) | MIT | 未来 ComfyUI 接口形态 | MuAPI 参数、第三方能力口径 | EXECUTION_ONLY |
| SRC-DIR-015 | [Anil-matcha/Seedance-2-API](https://github.com/Anil-matcha/Seedance-2-API) | MIT | 未来批处理适配器形态 | 把 MuAPI 暴露能力等同 ByteDance 官方模型能力 | EXECUTION_ONLY |
| SRC-DIR-016 | [SamurAIGPT/Seedance-2.5-API](https://github.com/SamurAIGPT/Seedance-2.5-API) | MIT | 第三方 API 路由样例 | “早期接口数量”等营销口径；未经官方核验的能力参数 | EXECUTION_ONLY |
| SRC-DIR-017 | [Anil-matcha/awesome-seedance-2.5-api-prompts](https://github.com/Anil-matcha/awesome-seedance-2.5-api-prompts) | 未发现明确仓库许可证 | 只做不可复制的市场观察 | Prompt、文档和示例的吸收或分发 | REJECT |
| SRC-DIR-018 | [SamurAIGPT/seedance-2-generator](https://github.com/SamurAIGPT/seedance-2-generator) | 未发现明确仓库许可证 | SaaS 产品边界观察 | Next.js、支付、账户、额度与生成记录；不解决导演设计 | REJECT |
| SRC-DIR-019 | [FloyoAI/ComfyUI-Seed-API](https://github.com/FloyoAI/ComfyUI-Seed-API) | Apache-2.0 | BytePlus/ComfyUI 节点形态 | 把节点参数当成 Prompt 或镜头规范 | EXECUTION_ONLY |

### 3.5 用户提供的本地导演资产

| ID | 来源 | 权利/来源状态 | 来源角色 | 验证状态 | 可吸收知识 | 拒绝或纠正项 | 处置 |
|---|---|---|---|---|---|---|---|
| SRC-DIR-020 | `视频动态Prompt 提示词：.md` | 用户提供；原始采集来源与许可未确认 | USER_CORPUS | UNVERIFIED | 常见平移、推拉、旋转和转场词的检索入口 | 把词条名称当作导演意图；把“转场”与摄影运动混为一层 | RESEARCH_ONLY |
| SRC-DIR-021 | `视频动态Prompt 提示词(镜头运动方向-镜头视角层级-镜头动态运镜)：.md` | 用户提供；原始采集来源与许可未确认 | USER_CORPUS | CONFLICTED | 可识别词库中哪些术语需要纠错和分层 | “量子级细节”“焦点爆破”等伪技术控制；作品式指代；摄影、剪辑、VFX 混层 | RESEARCH_ONLY |
| SRC-DIR-022 | `YUYING-可灵图生视频1.6.txt` 的 `CinematographyReference/CameraStyles` | 用户提供；原始来源与许可未确认；XML 闭合标签异常 | USER_CORPUS | CONFLICTED | 基础术语候选、剪辑术语索引、连续性检查线索 | 30 度规则被写反；Pan/平移、Cutaway/Insert 等定义混淆；叙事术语混入镜头类型；不得复制整段 | RESEARCH_ONLY |
| SRC-DIR-023 | `YUYING-midjourney艺术风格1.4.txt` 的同名片段 | 与 SRC-DIR-022 内容重复；来源与许可未确认 | USER_CORPUS | CONFLICTED | 仅用于确认重复与误差，不形成第二份证据 | 重复计权；复制错误定义；将重复文本当作交叉验证 | REJECT（重复原文） |
| SRC-DIR-024 | 当前工作树 `references/cinematography-director.md` | 本 Skill 候选原创转化；当前为未跟踪工作树文件，不是冻结基线 | INTERNAL_CANDIDATE | PARTIAL | 已完成叙事优先、摄影/剪辑/VFX 分层、正确 30 度规则、空间轴、AI 执行语法、导演卡与有限停止 | 不能因文件存在就宣称运行行为已修复；尚缺显式 Coverage 编译、Segment/Shot 分层和序列级真实视频门禁 | ADAPT_METHOD |

## 4. 可吸收知识清单

以下是 Claim–Source 血缘矩阵。`独立组` 按共同上游合并计数；本 Skill 内部候选不算独立外部证据。
“多源支持”只用于至少两个独立组，其他项目保持单源候选或项目假设。

| 机制主张 | 支持来源 | 独立组 | 当前裁决 |
|---|---|---:|---|
| Function first | 005、006、024 | 2 | 多源方法；待前向验证 |
| Beat 与 Shot 分离 | 005、006、008、010、024 | 3 | 多源方法；待前向验证 |
| Coverage 选择 | 005、004（失败样本）、024 | 2 | 方法 + 项目反例；待正例 |
| Blocking 可见化 | 005、006、024 | 2 | 多源方法；待前向验证 |
| Cut motivation | 005、008、024 | 2 | 多源方法；待前向验证 |
| Segment packing | 008、010、024 | 1 个 Seedance 社区谱系 + 内部候选 | 单谱系候选，不宣称多源 |
| 角色化参考输入 | 008、009、010、004 | 1 个 Seedance 社区谱系 + 1 个单样本 | 项目候选，不证明稳定性 |
| Visible end state | 008、010、024 | 1 个外部谱系 + 内部候选 | 单谱系候选 |
| Model adapter 与导演层分离 | 001/002、005、014–019 | 3 | 多源边界原则 |
| 真实成片门禁 | 004、005、006 | 3 | 多源原则；阈值仍需校准 |

候选机制清单：

1. **Function first**：先写观众需要理解的变化，再选景别和运镜。
2. **Beat 与 Shot 分离**：剧情节拍不是镜头，时间段也不是自动切点。
3. **Coverage 选择**：定位、动作、信息、反应、后果按需要组合，不机械凑景别。
4. **Blocking 可见化**：人物和摄影机都要写起点、动作、终点与空间方向。
5. **Cut motivation**：每个切点绑定新信息、反应、视线、动作、空间、情绪或时空变化。
6. **Segment packing**：一个模型生成段可以包含一个镜头或一个有意设计的多镜头序列，二者必须显式声明。
7. **角色化参考输入**：每张图只承担身份、场景、道具、分镜、起始构图、结束状态或风格等明确角色。
8. **Visible end state**：阶段或镜头结束时必须写可见事实，不能只写抽象情绪。
9. **Model adapter 与导演层分离**：官方能力和平台入口是技术事实，不能反向决定人物选择。
10. **真实成片门禁**：Prompt 格式、LLM 自评和静态字段检查都不能代替视频中的镜头可读性。

## 5. 明确拒绝项

以下内容不得进入未来规范：

- 为了“高级”而随机拼接推、拉、摇、移、环绕、变焦和粒子词；
- 所有镜头默认手持呼吸、所有忧郁默认慢推、所有梦幻默认旋转；
- 把摄影机/镜头型号当作跨模型稳定控制参数；
- 把精确秒点写成模型必然执行的剪辑帧；
- 把 9 张图全部上传当作默认最佳实践；
- 把观察线、轴线、运动箭头、格栅和文字说明放入生产首帧；
- 把 API wrapper 的参数或第三方聚合服务能力写成 Seedance 官方事实；
- 把仓库星数、案例数量、作者赞誉或 LLM 自评当作成片质量证据；
- 复制 Mx-Shell 原始 Prompt、未许可社区文本或来源不清的本地词库表达；
- 将 P1A 单样本失败泛化为所有模型、所有15秒段落或所有一镜到底都失败。

## 6. 来源吸收条件

研究候选准入与正式默认规则准入必须分开。

进入研究候选至少满足：

```text
主张可定位
+ 许可或使用边界明确
+ 与现有规则无冲突
+ 能改变一个具体导演决策
+ 有可证伪的正例、负例或真实视频验证计划
+ 保留来源与修改说明
```

只有验证计划、尚无结果的内容必须保持 `HYPOTHESIS`，不得成为默认行为。进入正式 Skill 的默认规则还必须满足：

```text
已完成至少一项能直接检验该机制的正例、负例或真实视频验证
+ 结果与失败边界已记录
+ 未把单样本泛化为稳定成功率
```

若只满足“看起来专业”“案例很多”或“以后会测试”，不得吸收为正式规则。

## 7. 当前裁决

### A 级：作为核心研究输入

- ByteDance Seedance 2.0/2.5 官方资料；
- 本项目豆包 App 与生成视频实证；
- DirectorSKILL 的 function/coverage/editing 方法；
- Atlas 的 Seedance 多参考与 Storyboard 路由；
- ai-shortfilm-prompts 的 MIT Prompt 编译部分。

### B 级：补充和反例

- dexhunter、rich5000、ai-cinematic-pipeline；
- YouMind 抽样案例；
- 用户本地词库的术语发现与错误样本。

### C 级：暂不进入导演知识层

- ComfyUI、MuAPI、BytePlus 和 SaaS 外壳；
- 无许可证的 Prompt 库；
- AGPL 项目的代码/文本实现；
- Mx-Shell 的 All Rights Reserved 原始 Prompt。

## 8. 尚未证明的假设

1. 显式 `Shot 1/2/3` 与完整分镜图能否让当前豆包 Seedance 2.5 稳定产生可辨认的多镜头序列。
2. 同一15秒内的理想镜头数是否随动作复杂度、参考图数量和声音密度变化。
3. 多图角色绑定与完整 Storyboard 同时输入时，模型会优先遵循哪类信息。
4. Prompt 中的切点描述与参考分镜图相比，哪一个对镜头层级更有效。
5. 原生音频是否帮助镜头节奏，还是增加指令竞争。

这些假设必须通过冻结输入、有限生成和普通观众审片验证，不能在研究阶段升级为规则。
