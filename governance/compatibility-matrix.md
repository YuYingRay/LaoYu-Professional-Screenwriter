# 项目兼容性矩阵

> 本文件记录交付物相对当前项目基线的兼容状态。
> 它不替代 Manifest、Review 或 Notice。

## 1. 当前基线

| 字段 | 内容 |
|---|---|
| 项目 ID | PROJECT-[SLUG]-001 |
| 当前项目基线 | PROJECT-[SLUG]-v1.0.0 |
| 生成日期 | YYYY-MM-DD |
| 生成方式 | `scripts/validate_project.py` |
| 总体结果 | PASS / CONDITIONAL_PASS / BLOCKED / FAIL |

## 2. 交付物兼容性

| Artifact ID | 类型 | Artifact 版本 | 依据基线 | 已验证基线 | 状态 | Test Run | 备注 |
|---|---|---|---|---|---|---|---|
| BIBLE-v1.0.0 | STORY_BIBLE | v1.0.0 | PROJECT-[SLUG]-v1.0.0 | PROJECT-[SLUG]-v1.0.0 | PASS | RUN-[ID] |  |
| SCRIPT-v1.0.0 | SCRIPT_MASTER | v1.0.0 | PROJECT-[SLUG]-v1.0.0 | PROJECT-[SLUG]-v1.0.0 | PASS | RUN-[ID] |  |
| DEL-[ID] | PRODUCTION_HANDOFF | v1.0.0 | PROJECT-[SLUG]-v1.0.0 | PROJECT-[SLUG]-v1.0.0 | PASS | RUN-[ID] |  |

## 3. 失效条件

以下任一情况将使受影响交付物变为 `BLOCKED`：

- 依据基线与当前项目基线不一致；
- 上游 Artifact 已 `SUPERSEDED`，但下游未重新验证；
- 依赖的 Notice 尚未 `VERIFIED`；
- Review 结论要求重写，但交付物仍标记为 LOCKED；
- 生产包缺少剧本、Bible、权利或连续性依赖。
