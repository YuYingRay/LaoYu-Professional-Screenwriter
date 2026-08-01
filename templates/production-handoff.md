---
artifact_id: DEL-[[PROJECT_ID]]-[[NNN]]
artifact_type: PRODUCTION_HANDOFF
project_id: PROJECT-[[SLUG]]-001
project_baseline: PROJECT-v1.0.0
artifact_version: v1.0.0
status: DRAFT
owner: [[ROLE]]
upstream_ids: ["[[BIBLE-ID]]", "[[SCRIPT-ID]]", "[[REVIEW-ID]]"]
conformance_level: STRUCTURAL_CONFORMANCE
---

# 制作交接包

## 0. 交接控制

| 字段 | 内容 |
|---|---|
| 交接 ID | `HANDOFF-[[PROJECT_ID]]-[[NNN]]` |
| 项目基线 |  |
| 剧本版本 |  |
| Story Bible 版本 |  |
| 审查报告 |  |
| 交接负责人 |  |
| 制片批准人 |  |
| 目标生产方式 | 实拍 / AI / 混合 |
| 目标画幅 | 16:9 / 9:16 / 其他 |
| 交接状态 | DRAFT / IN_REVIEW / APPROVED / LOCKED / BLOCKED |

## 1. 不可改变的故事事实

| ID | 类型 | 不可改变内容 | 事实源 | 关联场景 |
|---|---|---|---|---|
| BIBLE-[[ID]] | 角色/规则/时间/道具 |  |  | SC-[[ID]] |

## 2. 场景与镜头接口

| Scene ID | 场景版本 | 镜头范围 | 角色 | 地点 | 关键动作 | 连续性锚点 |
|---|---|---|---|---|---|---|
| SC-[[ID]] |  | SHOT-[[ID]] |  |  |  |  |

## 3. 资产清单

| Asset ID | 类型 | 来源 | 版本 | 权利状态 | 生成/拍摄限制 | 责任人 |
|---|---|---|---|---|---|---|
| ASSET-[[ID]] | 角色/地点/道具/声音/UI |  |  | RGT-[[ID]] |  |  |

## 4. 角色一致性

| Character ID | 外形锚点 | 服装 | 伤病/污损 | 道具 | 禁止漂移项 |
|---|---|---|---|---|---|
| CHAR-[[ID]] |  |  |  |  |  |

## 5. 风险与降级

| 风险 ID | 风险 | 触发条件 | 最小降级方案 | 是否改变故事事实 | 批准人 |
|---|---|---|---|---|---|
| RISK-[[ID]] |  |  |  | 是 / 否 |  |

## 6. 交接门禁

- [ ] 剧本已锁定，且 `content_digest` 与交接记录一致
- [ ] 所有场景均映射到 Scene Card
- [ ] 角色、服装、伤病、道具和地点状态已核验
- [ ] 镜头、声音、字幕和 UI 使用同一项目基线
- [ ] 第三方素材具备独立权利记录
- [ ] 未关闭 P0 已阻断生产
- [ ] 制作降级不静默改变人物选择与因果结果
