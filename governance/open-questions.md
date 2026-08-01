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
| B7 | 安装根存在计划未记载的空目录`.agents/`与`.codex/`；二者不受Git跟踪或本地`.gitignore`忽略，且当前ownership规则未声明 | WP1b strict前 | 暂停删除/豁免；先确认其是否为宿主运行时目录，再决定排除或清理 |
| B8 | A1独立枚举总数为37，但示例内分类为“表格24/标题8/正文3”，与冻结计划“表格25/标题8/正文2”不一致 | A1继续前 | 触发冻结计划§3 A1停止条件；等待计划最小补丁升版与重新冻结 |

## B7实测证据

- 发现时间：2026-08-01，WP0只读盘点。
- `.agents/`与`.codex/`均为空目录、无Git跟踪文件、未命中本地`.gitignore`。
- 该发现不改变`v0-baseline`提交内容，因为Git不记录空目录；但若不处置，WP1b的`UNDECLARED_EMPTY_DIR`门禁将确定性失败。
- 在作出包边界决定前，不删除目录、不新增白名单、不把该项伪记为PASS。

## B8实测证据

- 使用冻结计划指定宽模式`(?<![0-9A-Za-z])VE\d+(?![0-9])`独立复算，全集仍为37处。
- `examples/vertical-drama-example.md`内35处实际分为：Markdown表格单元24处、ATX标题8处、代码块正文引用3处。
- 三处正文引用位于当前文件第439、444、476行；其中第476行以箭头开头的下一集兑现要求无法归入表格单元。
- 另两处仍为`templates/story-bible.md`空白表格1处、`templates/vertical-episode.md`文件名约定1处。
- 最小修复只需把冻结计划§15 D3的“25/2”改为“24/3”；不改变37处全集、D3-MAP选择、保护示例不改或三处规范映射的执行动作。
