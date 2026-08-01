# Professional Screenwriter 非劣基准协议

## 0. 封存身份

| 字段 | 值 |
|---|---|
| protocol_id | `BENCH-PSW-v1.0.0` |
| protocol_status | `FROZEN_BEFORE_BASELINE_RUN` |
| frozen_plan | `v1.0.7` |
| frozen_plan_sha256 | `30C62DB7147B0F3A9CEF2343D471B970AC15478FCA1F4698C0CA0B1D495D2385` |
| baseline_ref | `v0-baseline` / `f807fcc232fd5c6dcdbd04be14fb672dbea690b3` |
| decision_evidence | `v1.0.7 §0.1`冻结快照（原始用户证据：`DEC-20260731-D1-001`、`DEC-20260731-D6-001`） |
| total_outputs | `24`（4任务 × 2版本 × 3次） |
| calibration_arm | `NONE`（选择 `E.4.1-C`） |

本文件必须在首个 baseline RUN 前提交。`protocol_digest` 由提交后的文件字节计算并记录在 Skill 目录外的执行台账；修改本文件会使既有比较失效，baseline 与 candidate 必须全部重跑。

## 1. 固定任务

### T1 新建长片

输入简报：

> 105分钟中文剧情片，主角是被停职的港口安全工程师，目标中国流媒体，预算有限。

必需交付：

1. project manifest；
2. Full Bible 核心域；
3. 因果脊柱；
4. 八序列大纲；
5. 三张关键 Scene Card。

### T2 存量剧本诊断

输入：`tests/feature-project-fixture/script/master/script.fountain`及请求“诊断结构问题”。

必需交付：

1. 反推的 Bible 核心事实；
2. 因果链诊断；
3. 九字段 Finding 列表。

### T3 竖屏短剧

输入简报：

> 60集 × 90秒、9:16复仇爱情，第8集设置付费点。

必需交付：

1. 季承诺；
2. 前三集完整内容，含钩子与兑现；
3. 第8集付费点设计。

### T4 AI生产交接

输入：`tests/feature-project-fixture/script/master/script.fountain`及请求“生成AI视频交接包”。

必需交付：

1. 镜头与关键帧清单；
2. 声音、字幕与UI清单；
3. 角色与场景连续性约束；
4. AI/实拍执行说明及失败降级；
5. 权利、来源与人工复核状态；
6. 子交付物规范ID或嵌入规则。

输入文件在首次运行前按SHA-256封存。两版本必须收到相同的原始输入、用户请求与必需交付范围。

## 2. 能力覆盖矩阵

| SKILL命令意图 | 任务/子场景 | 预期加载的主入口 | 最低断言 |
|---|---|---|---|
| `/start` | T1/T3 建立项目 | `SKILL.md`、manifest契约/模板 | 项目定义与约束可追溯 |
| `/discover` | T1 概念筛选 | `SKILL.md`、电影结构reference | 前提、反命题与制作边界明确 |
| `/bible` | T1/T2 | Bible reference/template | 核心域完整，空项有理由 |
| `/structure` | T1/T2/T3 | 对应结构reference | 输出因果链而非事件清单 |
| `/outline` | T1/T3 | 电影或竖屏reference/template | 八序列/分集承诺完整 |
| `/scene` | T1 | Scene Card模板 | 三张卡含目标、阻碍、策略、反转、代价 |
| `/draft` | T3 | 竖屏单集模板 | 三集均有行动、反制、状态变化与新问题 |
| `/review` | T2 | rubric与review模板 | Finding九字段齐全 |
| `/rewrite` | T2 | rubric与重写规则 | 修法按因果深度排序且可复验 |
| `/continuity` | T2/T4 | Bible、剧本、handoff reference | 时间、知识、道具与关系矛盾可定位 |
| `/production` | T4 | handoff reference/template | 六项交接结构全部出现 |
| `/status` | T1/T3/T4 | manifest与契约 | 基线、风险、门禁与未决项可见 |
| `/export` | T4 | handoff/export合同 | 导出范围和引用闭包明确 |

运行trace必须记录实际加载文件；“预期加载”不是已加载证明。十三项能力不得有空映射。

## 3. 运行隔离

1. baseline与candidate使用独立只读worktree或等价只读快照；baseline检出`v0-baseline`。
2. 每次重复使用全新输出目录与fresh session，前次输出、review、trace不可见。
3. 24次运行随机交错；实际顺序在首轮前生成并封存。
4. 每次记录模型ID/build、采样配置、可用seed、tokenizer版本、开始/结束时间。
5. 只传原始artifact与用户式请求，不传预期答案、修复目标或版本身份。
6. 每轮结束把匿名产物、trace、配置和hash移入Skill与生成项目之外的只读sealed evidence store；随后清理生成侧可见目录和session。
7. A/B与版本映射密钥单独封存；评分先落盘并计算摘要，再揭盲。

任一隔离条件不满足，该RUN作废，不得补写证明。

## 4. 记录字段

每个RUN至少记录：

```text
run_id
task_id
anonymous_version_label
run_index
input_digest
protocol_digest
model_id_and_build
sampling_config
seed_if_available
tokenizer_version
fresh_session_ref
visible_root_listing
loaded_file_trace
loaded_char_count
loaded_token_count
output_digest
validator_results
started_at
finished_at
```

不得用仓库文件大小估算实际加载量。

## 5. 八个质量维度与评分锚点

所有任务均按八维度评分。采用1–5分整数制；2分、4分表示相邻锚点之间。评分必须引用产物中的具体证据。

| # | 维度 | 1分 | 3分 | 5分 |
|---:|---|---|---|---|
| 1 | 因果链成立度 | 关键转折靠巧合或省略 | 主链成立但局部跳步 | 每个关键选择均由压力、策略和后果推出 |
| 2 | 主角主动性 | 主角主要被事件推动 | 主角有行动但关键转折由外力完成 | 主角持续选择并承担升级代价，高潮由其选择完成 |
| 3 | 对手策略真实性 | 对手只为剧情犯错 | 策略基本合理但反制单一 | 目标、资源、限制与迭代反制均可信 |
| 4 | 知识边界一致性 | 角色无来源地知道关键信息 | 主体一致，少数信息来源模糊 | 关键知识均有获得时点、来源与后果 |
| 5 | 连续性一致性 | 时间、道具、关系或伤病互相冲突 | 无致命冲突但追溯不完整 | 连续性锚点完整且跨交付可追溯 |
| 6 | 对白策略性 | 对白只解释信息 | 部分对白有目的和潜台词 | 每段关键对白都有目标、攻防、转向与关系后果 |
| 7 | 钩子公平与兑现 | 钩子无铺垫或解锁后不兑现 | 有铺垫与初步兑现但因果较弱 | 钩子来自既有因果，及时兑现并产生更深问题 |
| 8 | 生产可行性与降级保真 | 无法执行或降级破坏核心因果 | 可执行但风险/降级不完整 | 资产、镜头、风险与降级明确且保留人物选择和情绪结果 |

关键维度固定为：

| 任务 | 关键维度 |
|---|---|
| T1 | 1 因果链、2 主角主动性 |
| T2 | 1 因果链、4 知识边界 |
| T3 | 1 因果链、7 钩子公平与兑现 |
| T4 | 5 连续性、8 生产可行性与降级保真 |

## 6. 评分者安排

- T1/T3：由用户对12份匿名产物进行盲评；执行者不得提前揭示版本。
- T2/T4：由三验证器记录结构违规，并由独立LLM fresh session按同一八维量表评分；独立LLM不得看到版本映射、修复目标或其他RUN结果。
- 验证器只判断结构；LLM或用户判断语义。验证器通过不得替代质量评分。

## 7. E.4.1-C质量门禁

每任务、每版本固定3次运行。对每个关键维度按预注册的`run_index`配对，计算：

```text
delta_i = candidate_i - baseline_i
```

若三个`delta_i`全部小于等于0，且至少一个严格小于0，则该关键维度构成“方向一致的下降”，该任务质量门禁FAIL。三个差值全为0不算下降。

其他情况不因该维度阻断。非关键维度、总分、单次大幅波动全部如实报告，但在`E.4.1-C`下不作为阻断条件。总分不得覆盖关键维度FAIL。

## 8. E.5实际加载量门禁

只比较同一任务、同一原始输入、同一必需交付范围的实际加载输入。每任务以3次RUN的实际加载token中位数为聚合值。

预注册容差为`0%`：

```text
candidate_comparable_median_tokens <= baseline_comparable_median_tokens
```

满足为PASS，超出为FAIL。字符数同时报告，用于发现tokenizer或trace异常，但token数是门禁指标。

若candidate完成了baseline缺失的必需交付，新增范围的加载量单列为`scope_expansion_tokens`；必须从两版都可比的`comparable_scope_tokens`中剥离，不得把多交付误判为低效，也不得用新增范围掩盖旧范围膨胀。无法可靠拆分时该任务token结论为`INVALID_COMPARISON`并要求重跑，不得判PASS。

## 9. 聚合放行与失败处置

全部四任务必须同时满足：

1. 运行隔离七条有效；
2. 三验证器结果完整；
3. 关键维度未触发方向一致下降；
4. E.5实际加载量门禁PASS。

任一任务FAIL时，不得激活候选契约。按以下固定顺序处理：

1. 定位失败任务与维度/指标；
2. 归因集 = 该任务实际加载文件 ∩ 本轮修改文件；
3. 仅修复或回退归因集并只重跑该任务；
4. 归因集为空时增加重复次数并标记采样噪声，不盲目回退；
5. 两轮定向修复仍FAIL时交用户裁决接受例外或回退内容层。

任何例外必须写入`governance/change-log.md`；执行者不得自行豁免。

## 10. 防泄漏与验收

- baseline与candidate RUN绑定相同`protocol_digest`。
- 匿名产物不含commit、tag、版本名、路径或修复措辞。
- 评分记录先于揭盲密钥落盘并单独取摘要。
- 被测量树之后若改动任何实际加载文件，受影响任务必须重跑。
- 最终按创作质量、成本、控制平面正确性分别报告；不得从单一维度推导“本轮无用户价值”。
