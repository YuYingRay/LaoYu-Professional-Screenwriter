---
artifact_id: DEL-OPEN-QUESTIONS-001
artifact_type: OPEN_QUESTIONS
project_id: PROJECT-PROFESSIONAL-SCREENWRITER
project_baseline: CONTRACT-v0.1.0
artifact_version: v0.1.0
status: DRAFT
owner: LaoYu-Professional-Screenwriter
upstream_ids: []
---

# 架构悬题

本文件只记录Professional Screenwriter Skill领域内尚未进入当前基线的架构问题。计划审查过程和执行台账不写入Skill payload。

| ID | 问题 | 延后时点 | 当前处置 |
|---|---|---|---|
| B1 | 跨模板信息重复：信息矩阵、人物目标表、连续性表与付费点表多处并存 | 三层重组 | 本轮不做 |
| B2 | 模板过度工程化：长季短剧填充成本与重复评分卡 | 基准数据后 | 本轮不做 |
| B3 | `BIBLE-`前缀语义超载；artifact ID内嵌版本与逻辑ID稳定性冲突 | ID重设轮 | 本轮不做 |
| B4 | 存量剧本ingestion工作流缺失 | 基准任务暴露后 | 本轮不做 |
| B5 | 瀑布流程与迭代创作之间的工作流冲突 | 三层重组 | 本轮不做 |
| B6 | 跨集事实注入率尚无完备定义 | 下一轮 | 定义完成前不评分 |
| B7 | 安装根存在计划未记载的空目录`.agents/`与`.codex/`；二者不受Git跟踪或本地`.gitignore`忽略，且当前ownership规则未声明 | WP1b strict前 | **CLOSED（2026-08-01）**：用户授权条件删除；前置门禁全部通过后以非递归方式删除，删除后不存在且未产生新空目录 |
| B8 | A1独立枚举总数为37，但示例内分类为“表格24/标题8/正文3”，与冻结计划“表格25/标题8/正文2”不一致 | A1继续前 | **CLOSED（2026-08-01）**：v1.0.7 已按“表格24/标题8/正文3”重新冻结，37处全集与D3-MAP动作不变 |
| B9 | ownership第1条的`**/__pycache__/**`与`scripts/**`等业务路径必然重叠；按“计算全部匹配”算法，运行Python后会稳定产生`MULTI_OWNED_FILE` | WP1b strict前 | **CLOSED（2026-08-01）**：`OWN-EXCLUDED`先于普通 owner 匹配；非排除规则之间的真实重叠仍阻断，未用删除缓存规避 |
| B10 | 安装根存在`.claude/scheduled_tasks.lock`，旧文本管道把 Git ignore 结果末尾 CR 误当成路径字符 | WP1b strict前 | **CLOSED（2026-08-01）**：改用 NUL 输入/输出协议后确认该宿主锁已被 Git 排除；未删除文件、未加白名单 |

## B7实测证据

- 发现时间：2026-08-01，WP0只读盘点。
- `.agents/`与`.codex/`均为空目录、无Git跟踪文件、未命中本地`.gitignore`。
- 该发现不改变`v0-baseline`提交内容，因为Git不记录空目录；但若不处置，WP1b的`UNDECLARED_EMPTY_DIR`门禁将确定性失败。
- 在作出包边界决定前，不删除目录、不新增白名单、不把该项伪记为PASS。
- 关闭证据（2026-08-01）：用户明确授权；动作前复验二者均在安装根内、为空、无Git跟踪内容；排除本节历史证据后，精确根相对路径模式未发现运行依赖引用。
- 删除采用不带递归参数的`Remove-Item -LiteralPath`逐目录执行；删除后两路径均不存在，全仓未发现新增空目录。若后续重建，WP1b strict仍应失败。

## B8实测证据

- 使用冻结计划指定宽模式`(?<![0-9A-Za-z])VE\d+(?![0-9])`独立复算，全集仍为37处。
- `examples/vertical-drama-example.md`内35处实际分为：Markdown表格单元24处、ATX标题8处、代码块正文引用3处。
- 三处正文引用位于当前文件第439、444、476行；其中第476行以箭头开头的下一集兑现要求无法归入表格单元。
- 另两处仍为`templates/story-bible.md`空白表格1处、`templates/vertical-episode.md`文件名约定1处。
- 最小修复只需把冻结计划§15 D3的“25/2”改为“24/3”；不改变37处全集、D3-MAP选择、保护示例不改或三处规范映射的执行动作。
- 关闭证据（2026-08-01）：执行计划已升为`v1.0.7`，冻结身份为`30C62DB7147B0F3A9CEF2343D471B970AC15478FCA1F4698C0CA0B1D495D2385 + 713行`；独立复核仍为37处、24/8/3及其他模板2处。

## B9/B10实测证据

- 发现时间：2026-08-01，WP4a首次真实安装根ownership audit。
- 导入`ownership.py`后，Python在`scripts/__pycache__/`生成缓存；每个缓存同时命中
  `OWN-EXCLUDED`与`OWN-TOOLING`，稳定报告`MULTI_OWNED_FILE`。`.gitignore`确实命中缓存，
  因此问题是规则重叠，不是缓存未忽略。
- `.claude/scheduled_tasks.lock`为124字节，创建/修改时间均为2026-07-21 10:38:07；
  `git status --untracked-files=all`不显示它是因为父目录属于Git的默认隐藏机制，但
  filesystem ownership视图仍必须枚举并报告。
- 两项均处于audit发现阶段，不阻断WP4a；WP1b切strict前必须关闭。当前不把报告删除、
  缓存清理或临时白名单伪记为修复。
- 关闭证据：`20f148a` 修复排除优先级与 NUL 协议；`ab336d6` 记录 strict 迁移证据。
  100 项单测与真实安装树 `lint_repo --mode strict` 均通过，Finding 为 0。
