# 中英文剧本格式与导出手册

> 本文件是 `professional-screenwriter` 的按需参考资料。
>
> 当任务涉及中文影视剧本、英文 Screenplay、Fountain、Final Draft 兼容文本、剧本格式检查、剧本转分镜或跨语言导出时加载。
>
> 主 `SKILL.md` 的因果、人物、场景功能、对抗式审查和内容安全规则优先于本文件。
>
> 本文件规定“如何清晰、统一、可制作地表达已经成立的故事”；它不能修复故事本身。

## 快速目录

- `# 1. 第一性原理`
- `# 2. 总体输出规则`
- `# 3. 中文文学剧本格式`
- `# 4. 英文 Master Scene Format`
- `# 5. Fountain 格式`
- `# 6. 中文与英文的转写规则`
- `# 7. 面向 AI 制作的格式扩展`
- `# 8. 格式对抗式审查`
- `# 9. 常见错误与修复`
- `# 10. 最小模板`
- `# 11. 最终放行门禁`
- `# 12. 与主 Skill 的协作`

---

# 1. 第一性原理

## 1.1 格式的唯一目的

剧本格式不是文学排版比赛。

格式的目的，是让下游协作者能够快速、准确地知道：

```text
何时发生？
何地发生？
谁在场？
镜头能看见和听见什么？
谁说话？
此刻的行动、信息和关系如何变化？
```

因此，格式服务于：

- 阅读速度
- 制作沟通
- 场景拆分
- 演员表演
- 预算与资产统计
- 分镜和拍摄计划
- 翻译、版本管理和 AI 生成工作流

如果格式很“漂亮”，但读者无法判断动作、对白、时间、地点和角色状态，它就是失败格式。

---

## 1.2 格式不能替代戏剧

以下问题不能靠排版修复：

- 主角没有目标
- 场景没有冲突
- 人物没有动机
- 反转不合逻辑
- 台词只是在解释剧情
- 结局由巧合解决
- 世界规则前后矛盾

格式检查必须在结构检查之后，或至少并行进行。

禁止为了“像专业剧本”而加入大量：

- `CUT TO:`
- `CLOSE ON:`
- `WE SEE:`
- `MUSIC CUE:`
- 复杂镜头语言
- 演员情绪指令
- 剪辑说明

除非这些内容对理解、节奏、声音或制作交接不可缺少。

---

## 1.3 交付格式选择

| 交付目标 | 优先格式 | 原因 |
|---|---|---|
| 中文策划、网剧、短剧开发 | 中文文学剧本 Markdown | 便于协作、审读与版本管理 |
| 英文影视剧本投递 | 英文 Master Scene Screenplay | 国际读者最熟悉的阅读协议 |
| 纯文本、Git、AI 协作 | Fountain `.fountain` | 可读、可 diff、可转换 |
| Final Draft 工作流 | `.fdx` 或 Final Draft 导入文本 | 适合专业剧本软件与制作团队 |
| AI 视频生产 | Markdown + CSV/表格 | 便于拆场、资产、分镜与提示词 |
| 双语制作 | 中文开发稿 + 英文拍摄稿 | 避免直接逐句翻译造成表演失真 |

不要同时维护多个“真源”文件。

推荐：

```text
一个主源文件
→ 导出为阅读稿、Fountain、PDF、分镜表或制作表
```

---

# 2. 总体输出规则

## 2.1 默认顺序

任何标准剧本场景按此顺序输出：

```text
场景标题
动作描述
角色名
必要的表演提示
对白
下一段动作或下一个人物对白
```

## 2.2 可拍摄原则

动作描述只写镜头能够：

```text
看见
听见
合理推断
```

不要直接写不可见内心。

错误：

```text
林夏感到被背叛，也意识到自己终于不再爱他。
```

改写：

```text
林夏盯着手机上的转账记录。她把戒指摘下，放到桌上。
```

错误：

```text
周明很紧张，但假装镇定。
```

改写：

```text
周明端起水杯。杯沿碰到牙齿，发出一声轻响。
```

## 2.3 动作段长度

默认每段动作控制在 1–4 行。

长动作应按以下方式拆开：

- 新人物动作
- 新信息
- 新空间变化
- 新声音
- 新时间跳跃
- 新情绪可见反应

不要将一个 10 行段落塞满人物动作、镜头、历史背景、心理解释和摄影建议。

---

# 3. 中文文学剧本格式

## 3.1 适用场景

中文文学剧本适合：

- 中文电影、电视剧、网剧、竖屏短剧的开发
- 导演、制片、编剧、分镜师协作
- 剧情、场景、人物和台词的快速修改
- AI 视频前期拆解
- 内部审读与提案

中文文学剧本强调清楚、统一和可拍摄；不要求机械复刻英文好莱坞页边距。

## 3.2 中文场景标题

推荐写法：

```text
1. 内景  城市规划院会议室  日

2. 外景  湘江边步道  夜

3. 内外景  汽车内/高架桥  夜

4. 内景  老周家客厅  连续
```

也可使用缩写形式：

```text
1. 内·会议室·日
2. 外·江边步道·夜
3. 内外·汽车/高架桥·夜
```

选定一种格式后，全稿保持一致。

场景标题至少包含：

```text
场次编号（推荐）
内景/外景/内外景
具体地点
时间
```

## 3.3 中文动作描述

示例：

```text
会议室的灯只亮了一半。

林夏站在投影幕前。她的方案图上，一整片街区的夜景照明被标成红色。

门被推开。周明没有进来，只把一份停职通知放到桌上。
```

动作描述规则：

- 用现在时。
- 先写观众立即能看到的事情。
- 用具体名词和动词。
- 首次出现的重要人物，给一项可拍识别特征。
- 重要声音可用大写、加粗或单独一行强调，但全稿一致。
- 不用长段落解释人物过去。
- 不在动作中替演员规定复杂情绪过程。

## 3.4 中文人物首次出现

推荐：

```text
林夏，32 岁，城市照明设计师，衬衫袖口沾着蓝色油墨，快步穿过走廊。
```

避免：

```text
林夏，一个从小被家庭忽视、内心敏感脆弱但外表坚强、毕业于名校且拥有复杂爱情史的女孩，走了进来。
```

首次出现只提供当前可拍、与戏剧相关的识别信息。履历放入人物小传或 Story Bible。

## 3.5 中文对白格式

推荐：

```text
林夏
这份停职通知，谁签的？

周明
（避开她的目光）
你最好别再查那片区域。
```

也可加人物状态：

```text
林夏（压低声音）
你说过，系统不会记录个人身份。
```

规则：

- 角色名独占一行。
- 表演提示放在角色名后或对白前，短且必要。
- 台词以可表演的行动为单位，不以作者解释为单位。
- 不把所有停顿、哭泣、转身都写进括号。
- 一段对白过长时，检查它是否应被行动、对方反应或冲突打断。

## 3.6 中文画外音与旁白

推荐标记：

```text
林夏（画外音）
那天以后，整座城市的灯都像在盯着我。
```

```text
广播声（画外）
请所有人员立即撤离。
```

区分：

| 标记 | 使用场景 |
|---|---|
| 画外音 | 人物不在画面内，但声音来自同一现实空间或附近 |
| 旁白 | 人物声音跨越时间、空间或现实画面，用于叙述 |
| 电话音 | 电话、语音、对讲机传来的声音 |
| 广播音 | 公共广播、新闻、喇叭、系统播报 |

不要滥用旁白解释剧情。旁白必须提供画面无法提供的张力、反讽、时间跳跃或主观视角。

## 3.7 中文转场

默认不必写转场。

仅在时间、空间或结构理解明显需要时使用：

```text
切至：

转场至：

闪回：

回到现在：

蒙太奇：

黑场。
```

不要在每个场景之间都写“切换”“转场”“镜头切到”。

---

# 4. 英文 Master Scene Format

## 4.1 定义

英文影视剧本通常使用 Master Scene Format：以场景而非每个镜头为组织单位。场景标题写明内外景、地点和时间；动作写可见可听内容；角色名和对白单独排布。

除非用户明确要求导演分镜版，不要把普通 spec script 写成镜头脚本。

## 4.2 Slugline / Scene Heading

标准格式：

```text
INT. LOCATION - TIME

EXT. LOCATION - TIME

INT./EXT. VEHICLE - MOVING - NIGHT
```

示例：

```text
INT. CITY PLANNING OFFICE - NIGHT

EXT. XIANG RIVER PROMENADE - NIGHT

INT./EXT. LIN'S CAR - MOVING - CONTINUOUS
```

场景标题规则：

- `INT.`：室内。
- `EXT.`：室外。
- `INT./EXT.`：内外景同时重要，例如车内与行驶环境。
- 地点名称具体且可持续复用。
- 用连字符分隔地点与时间。
- 时间使用 `DAY`、`NIGHT`、`MORNING`、`EVENING`、`DAWN`、`DUSK`、`LATER`、`CONTINUOUS` 等。
- 同一地点名称前后一致；不要在同一个地点随意写成 `OFFICE`、`WORKPLACE`、`LIN'S ROOM`。
- 只有制作确实需要时才加入天气、年代、季节、闪回等额外信息。

推荐：

```text
INT. LIN'S APARTMENT - BEDROOM - NIGHT
```

可接受但应谨慎：

```text
EXT. XIANG RIVER PROMENADE - RAINY NIGHT - 2026
```

不要写成：

```text
INT. THE BEAUTIFUL, LONELY, EXPENSIVE APARTMENT THAT SHOWS HOW SUCCESSFUL LIN IS - NIGHT
```

## 4.3 Action

示例：

```text
The office lights flicker.

LIN XIA, 32, sleeves stained with blue ink, stands before a glowing city map.

The door opens. ZHOU MING leaves a suspension notice on the table and disappears.
```

规则：

- 现在时。
- 只写可见或可听内容。
- 每段尽量短。
- 重要人物首次出现时，姓名通常用全大写。
- 重要声音可用全大写强调，例如 `A GUNSHOT`, `THE POWER CUTS OUT`；不要全篇滥用。
- 不要描述摄影机无法确认的动机或内心。
- 不要写小说式环境散文，除非环境本身是剧情行动。

错误：

```text
Lin feels the weight of every compromise she has made in her life.
```

改写：

```text
Lin deletes the presentation. Her finger hovers over the final confirmation.
```

## 4.4 Character Cues

标准示例：

```text
LIN
We need to leave. Now.

ZHOU
You still think this is about the lights?
```

规则：

- 英文角色名通常使用全大写。
- 同一个角色名在全稿保持一致。
- 同名或易混淆角色要加区分，例如 `YOUNG LIN`、`OLDER LIN`、`LIN (V.O.)`。
- 群众角色应具体到可执行，例如 `SECURITY GUARD`、`NURSE`，避免大量 `MAN 1`、`WOMAN 2`，除非确实无身份功能。
- 不要在角色名里塞入长身份说明。

## 4.5 Dialogue

示例：

```text
LIN
Who signed this?

ZHOU
(avoiding her eyes)
You should stop looking at that district.
```

对白规则：

- 白话、可演、可打断。
- 对白应改变权力、信息、关系或下一步行动。
- 不把已知事实重复解释给观众。
- 长独白必须有明确策略与对象，不是作者借角色讲话。
- 避免所有角色拥有相同句长、机智和比喻习惯。
- 英文台词的自然性优先于中文逐字对应。

## 4.6 Parentheticals

Parenthetical 是括号中的简短表演或语义提示，应谨慎使用；过多会降低阅读性。

可用：

```text
LIN
(quietly)
You knew.

ZHOU
into phone
Lock the bridge.
```

不要用：

```text
LIN
(extremely sad, remembering her difficult childhood, trying not to cry but also angry and confused)
You knew.
```

判断标准：

- 删除后对白意思是否可能被误解？
- 是否对演员理解台词意图必不可少？
- 能否通过前后动作表现？
- 是否实际上在替导演或演员完成表演？

若不是必要，删除。

## 4.7 O.S.、V.O.、CONT'D

| 标记 | 含义 | 使用原则 |
|---|---|---|
| `(O.S.)` | Off Screen，角色在同一场景现实空间中，但不在画面内 | 例如门外、隔壁房间、画框外 |
| `(V.O.)` | Voice Over，跨越画面、时间或叙事层的声音 | 旁白、回忆、录音、非同步叙述 |
| `(CONT'D)` | 同一人物对白被动作或分页打断后继续 | 多数软件自动处理，手写时不要滥用 |
| `(ON PHONE)` | 电话中说话 | 需根据软件或团队规范统一 |
| `(FILTERED)` | 经设备或特殊介质处理的声音 | 仅当声音质感重要时使用 |

示例：

```text
ZHOU (O.S.)
Don't touch that file.

LIN (V.O.)
That was the first time I understood the city had chosen a side.
```

不要将所有不在画面内的声音一律写成 `(V.O.)`。

## 4.8 Transitions

常用转场：

```text
CUT TO:

SMASH CUT TO:

DISSOLVE TO:

FADE OUT.

FADE IN:
```

默认原则：

- 普通场景切换不写 `CUT TO:`。
- 只在转场本身承载节奏、反讽、时间跳跃或叙事意义时写。
- 不要每页写多个转场。
- Fountain 中，全大写且以 `TO:` 结尾的行可被识别为转场。

## 4.9 Special Sequences

### Flashback

```text
FLASHBACK - INT. SCHOOL HALLWAY - DAY

...

BACK TO PRESENT:
```

只在闪回对当前行动有明确新意义时使用。

### Montage

```text
MONTAGE - LIN BUILDS THE CASE

-- Lin photographs broken streetlights.
-- She compares maintenance logs.
-- Zhou deletes security footage.

END MONTAGE.
```

蒙太奇适合压缩重复劳动、时间流逝或并列对照；不适合跳过本应完整呈现的关键选择。

### Intercut

```text
INTERCUT - LIN AND ZHOU ON THE PHONE

LIN
Where are you?

ZHOU
Somewhere your system can't see.
```

适用于两个空间同步的电话或对话。若对话复杂且频繁切换，使用 `INTERCUT` 能减少重复场景标题。

### Super / On-screen Text

```text
SUPER: 48 HOURS EARLIER

ON SCREEN: ACCESS DENIED
```

屏幕文字必须让观众可读、可理解，且不应承载唯一关键信息。

---

# 5. Fountain 格式

## 5.1 为什么使用 Fountain

Fountain 是为剧本设计的纯文本标记格式，能在普通文本编辑器中保持可读，并可被兼容工具转换为格式化剧本。

适合：

- Git 版本控制
- Codex 与 AI 协作
- 文本 diff
- 自动拆场
- Markdown/脚本协同
- 后续转 PDF 或专业剧本软件

推荐扩展名：

```text
project-title.fountain
```

## 5.2 最小 Fountain 示例

```fountain
Title: CITY OF LIGHTS
Credit: Written by
Author: Xiao Yu
Draft date: 2026-07-10

INT. CITY PLANNING OFFICE - NIGHT

The office lights flicker.

LIN XIA, 32, studies a glowing city map.

ZHOU MING
You should stop looking at that district.

LIN
Who signed the order?
```

Fountain 的基本识别逻辑：

- 以 `INT.`、`EXT.`、`INT./EXT.` 等开头的行可被识别为场景标题。
- 全大写角色名行后紧跟的文字会形成对白。
- 括号中的行可识别为 Parenthetical。
- 以 `TO:` 结尾的全大写行可识别为转场。

## 5.3 Fountain 场景标题

```fountain
INT. COFFEE SHOP - DAY

EXT. PARK - NIGHT

INT./EXT. CAR - MOVING - CONTINUOUS
```

如需强制将任意行作为场景标题，在行首加句点：

```fountain
.BACK IN THE OFFICE

.THE NEXT MORNING
```

Fountain 支持以句点强制场景标题。

## 5.4 Fountain 角色与对白

```fountain
LIN
We need to leave.

ZHOU
(quietly)
Not yet.
```

注意：

- 角色名与对白之间不能插入空行，否则可能被解析为普通动作文本。
- 中文角色名由于不具备英文大写特征，使用 `@` 强制角色元素。

中文示例：

```fountain
@林夏
我们得走了。

@周明
（低声）
还不行。
```

Fountain 支持以 `@` 强制角色名，适用于普通大写规则无法覆盖的语言。

## 5.5 Fountain 转场与强调

```fountain
CUT TO:

SMASH CUT TO:

FADE OUT.
```

强调可按兼容工具支持情况使用：

```fountain
*italic*
**bold**
_underline_
```

注意：不同 Fountain 工具对强调、注释、双栏对白、分页和导出细节的支持可能不同。对外正式交付前，必须用目标软件实际导出并检查 PDF。

## 5.6 Fountain 双人同时对白

第二位角色名后使用 `^`：

```fountain
LIN
I told you--

ZHOU ^
You told me nothing.
```

该语法常被 Fountain 工具识别为并行/重叠对白。

只在重叠本身具有节奏或表演意义时使用；不要把普通轮流对话排成双栏。

## 5.7 Fountain 场景编号

不同工具对自动编号支持不同。若项目需要稳定编号，可使用：

```fountain
INT. CITY PLANNING OFFICE - NIGHT #1#
```

但应避免在开发早期过早锁死编号。频繁插入、删除场景时，自动编号通常更安全。Fountain 参考实现可通过 `#编号#` 强制场景编号。

---

# 6. 中文与英文的转写规则

## 6.1 不做逐字翻译

中文文学剧本转英文 Screenplay 时，目标是：

```text
保留剧情功能
保留人物策略
保留情绪关系
保留可拍信息
适配英文表演与阅读习惯
```

不是逐句替换词汇。

错误：

```text
你不要敬酒不吃吃罚酒。
```

低质量直译：

```text
Don't refuse a toast only to drink a forfeit.
```

功能转写需要依据人物关系、威胁强度与语境决定，例如：

```text
Don't make this harder than it has to be.
```

或：

```text
Take the deal while it's still on the table.
```

## 6.2 人名、地点与制度

建立术语表：

```md
| 中文 | 英文标准写法 | 备注 |
|---|---|---|
| 林夏 | LIN XIA | 全稿一致 |
| 城市规划院 | City Planning Institute | 首次出现可补充性质 |
| 智慧照明系统 | Smart Lighting Network | 不随意改为多个叫法 |
| 停职通知 | Suspension Notice | 需结合目标市场制度核验 |
```

不要在同一英文剧本中混用：

```text
Planning Bureau
Urban Office
City Planning Institute
Municipal Design Department
```

除非它们是不同机构。

## 6.3 时间和文化信息

转写时区分：

- 必须保留的剧情事实；
- 可本地化的社会表达；
- 需要专业核验的法律、医疗、执法、教育、公司制度；
- 不适合直译的成语、敬语、网络用语和身份称谓。

若无法确认目标市场的专业流程，用中性叙事表达，或明确标为待顾问核验。

不要编造“美国警方一定会……”“英国法律规定……”等事实来服务剧情。

## 6.4 中英双语版本管理

推荐目录：

```text
project/
├── source/
│   ├── story-bible.zh.md
│   ├── screenplay.zh.md
│   └── terminology.md
├── screenplay/
│   ├── project.en.fountain
│   ├── project.en.pdf
│   └── project.zh.pdf
└── production/
    ├── scene-breakdown.csv
    └── continuity-log.md
```

版本规则：

- 一个语言版本为剧情事实源。
- 另一语言版本是表演和制作转写，不得悄悄改变剧情。
- 若英文版为自然表达而修改动作、关系或信息，应记录为剧情变更。
- 每次锁稿后更新术语表与连续性日志。

---

# 7. 面向 AI 制作的格式扩展

## 7.1 剧本与镜头表分离

普通剧本写：

```text
人物做什么、说什么、发生什么。
```

镜头表写：

```text
怎么拍、机位在哪、什么景别、如何运动、画面资产如何保持一致。
```

不要在每段普通剧本动作里混入：

```text
镜头推进
35mm 镜头
赛博朋克蓝紫色调
电影级景深
8K 画质
```

这些内容应进入分镜表或 AI 视频提示词表。

## 7.2 可选制作标记

如项目需要，可在中文开发稿使用非最终格式的制作标记：

```text
【资产】城市规划院会议室、投影幕、红色警示地图
【角色状态】林夏：蓝色衬衫、右手轻微擦伤
【连续性】停职通知已被林夏拿走
【声音】远处警报；荧光灯电流声
```

这些标记不应直接出现在正式投递版剧本中。

## 7.3 场景拆分字段

每场导出以下字段：

```md
| 场次 | 内外景 | 地点 | 日夜 | 角色 | 关键道具 | 服装状态 | 情绪状态 | 声音 | VFX | 连续性风险 |
```

剧本内的地点、人物名、道具名必须稳定，才能自动化或半自动化拆分。

---

# 8. 格式对抗式审查

## 8.1 第一轮：阅读阻力

逐项检查：

- 场景标题是否在 1 秒内回答地点和时间？
- 角色名是否稳定、无歧义？
- 动作段是否过长，导致读者难以扫描？
- 每句对白是否属于明确说话者？
- 表演提示是否过多？
- 是否把导演、演员、剪辑、摄影和编剧职责混在同一层文本？
- 同一种元素是否全稿保持同一种写法？

## 8.2 第二轮：可拍性

逐项检查：

- 是否出现不可见的内心说明？
- 是否存在未定义的空间跳跃？
- 道具、伤病、服装、时间、天气是否前后连续？
- 画外音、旁白、电话音、广播音的来源是否明确？
- 复杂动作是否能被清晰调度？
- 是否有必须呈现却只写在极小屏幕文字中的关键信息？

## 8.3 第三轮：格式噪声

删除或改写：

- 无必要的 `CUT TO:`
- 无必要的 `WE SEE`
- 无必要的镜头尺寸、焦段、机位
- 无必要的音乐指令
- 无必要的情绪副词，例如“极度愤怒地”“非常悲伤地”
- 无必要的括号表演提示
- 小说式背景段落
- 每场重复的时间、天气、角色履历

## 8.4 第四轮：导出验证

Fountain、PDF、Final Draft 兼容文本或中文 Word 导出前检查：

- [ ] 场景标题是否都被正确识别？
- [ ] 中文角色名是否在 Fountain 中使用 `@` 强制角色格式？
- [ ] 对白是否没有被错误识别为动作？
- [ ] 转场是否没有误识别？
- [ ] 场景编号是否稳定且符合当前版本？
- [ ] 双人对白在目标软件中是否显示正确？
- [ ] PDF 是否存在孤立角色名、孤立括号、跨页断裂或乱码？
- [ ] 字体、页边距和语言编码是否适配目标交付方？
- [ ] 导出稿是否仍与锁定剧情版本一致？

不得仅凭文本看起来正确，就假设导出文件正确。

---

# 9. 常见错误与修复

| 错误 | 为什么失败 | 修复 |
|---|---|---|
| 用小说语言写动作 | 降低扫描速度，混入不可拍内心 | 改为可见行动与反应 |
| 每场都写镜头指令 | 干扰阅读，越权且难维护 | 转移到导演版或镜头表 |
| 角色名不统一 | 无法拆场、统计和追踪关系 | 建立术语表并全局替换 |
| 场景标题不含时间 | 制作无法判断连续性 | 补充日、夜、连续、稍后等 |
| 场景标题地点太泛 | 无法拆场或复用资产 | 使用稳定具体地点名称 |
| 对白前堆满括号 | 替演员表演，阅读笨重 | 仅保留改变语义的提示 |
| 每句台词后都写动作 | 节奏碎裂 | 只在行为改变信息或关系时写 |
| 用旁白解释剧情 | 剥夺画面和行动 | 让人物选择、物件和冲突传递信息 |
| Fountain 中文名未强制 | 可能被识别为动作 | 使用 `@角色名` |
| 过早固定场景编号 | 重写后编号混乱 | 开发期自动编号，锁稿后再固定 |
| 把 Markdown 表格放进正式剧本 | 不符合剧本阅读习惯 | 表格留在拆场、圣经和制作包 |
| 直接机器翻译对白 | 不自然且失去人物策略 | 做功能转写并读 aloud 检验 |

---

# 10. 最小模板

## 10.1 中文文学剧本模板

```text
片名：《暂定片名》
类型：
时长：
版本：
日期：

1. 内景  地点  日

动作描述：只写可见和可听内容。

人物甲
（必要提示）
对白。

人物乙
对白。

2. 外景  地点  夜

动作描述。
```

## 10.2 英文 Screenplay 模板

```text
TITLE: TEMPORARY TITLE
Written by
AUTHOR NAME
Draft: YYYY-MM-DD

INT. LOCATION - DAY

Visible, present-tense action.

CHARACTER
Dialogue.

OTHER CHARACTER
(only if needed)
Dialogue.

EXT. LOCATION - NIGHT

Visible action.
```

## 10.3 Fountain 模板

```fountain
Title: TEMPORARY TITLE
Credit: Written by
Author: AUTHOR NAME
Draft date: YYYY-MM-DD

INT. LOCATION - DAY

Visible, present-tense action.

CHARACTER
Dialogue.

OTHER CHARACTER
(quietly)
Dialogue.

EXT. LOCATION - NIGHT

Visible action.
```

## 10.4 中文 Fountain 模板

```fountain
Title: 暂定片名
Credit: 编剧
Author: 作者名
Draft date: YYYY-MM-DD

.内景 地点 - 日

可见、可听的动作描述。

@人物甲
对白。

@人物乙
（必要提示）
对白。

.外景 地点 - 夜

动作描述。
```

注意：中文 Fountain 的场景标题可使用行首 `.` 强制识别；角色名可使用行首 `@` 强制识别。

---

# 11. 最终放行门禁

在导出或交付前确认：

- [ ] 剧情已通过主 `SKILL.md` 的结构、人物与对抗审查
- [ ] 全稿只使用一种稳定的场景标题体系
- [ ] 每个场景都有明确地点和时间
- [ ] 人物名称、地点、机构、道具名称全稿一致
- [ ] 动作仅描述可见、可听或可合理推断的内容
- [ ] 首次角色出现简洁且可拍
- [ ] 对白说话者无歧义
- [ ] Parenthetical / 表演提示只在必要时使用
- [ ] O.S.、V.O.、电话、广播、闪回、蒙太奇标记明确
- [ ] 无必要的镜头、剪辑、音乐和表演控制指令已删除
- [ ] 中英双语版本已通过术语表与剧情一致性核对
- [ ] Fountain 中文角色名已使用 `@`，特殊场景标题已按需使用 `.`
- [ ] 已用目标软件或目标流程实际导出并检查呈现结果
- [ ] 剧本稿、分镜稿、资产表和连续性表指向同一锁定版本

---

# 12. 与主 Skill 的协作

加载本文件时：

1. 先确认交付目标：开发稿、阅读稿、投递稿、Fountain、Final Draft 兼容稿、分镜稿或 AI 制作稿。
2. 先读取主 `SKILL.md` 的工作流；格式工作应发生在结构明确之后。
3. 短剧的钩子、分集、付费点与竖屏规则，由 `short-drama-playbook.md` 管理。
4. 概念短片、叙事短片、电影和剧集的结构密度，由 `film-series-format.md` 管理。
5. AI 资产、镜头和视频提示词，由主 `SKILL.md` 的制作转译部分或 `ai-production-handoff.md` 管理。
6. 规则冲突统一按
   `governance/control-plane-contract.md#71-规则冲突优先级`处理；本文件属于“当前任务明确路由到的领域 reference”层，目标软件的实际导入/导出规范属于其适用范围内的技术事实。

7. 如果目标软件、制作方或平台提供了独立格式规范，必须以其最新官方规范为准，并在导出后验证实际结果。
