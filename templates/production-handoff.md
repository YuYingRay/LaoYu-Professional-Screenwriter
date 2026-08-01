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

## 2. 镜头与关键帧清单

| Shot ID | Scene ID | 场景版本 | 时长 | 景别 / 机位 | 关键动作 | 起始 / 结束状态 | 关键帧 / 输入资产 | 连续性锚点 | 执行方式 | QC 状态 |
|---|---|---|---:|---|---|---|---|---|---|---|
| SHOT-[[ID]] | SC-[[ID]] |  |  |  |  |  | ASSET-[[ID]] |  | AI / 实拍 / 混合 | DRAFT / APPROVED |

## 3. 资产清单

| Asset ID | 类型 | Source ID | 版本 | Rights ID / 状态 | 生成/拍摄限制 | 责任人 |
|---|---|---|---|---|---|---|
| ASSET-[[ID]] | 角色 / 地点 / 道具 / 关键帧 | SRC-[[ID]] |  | RGT-[[ID]] / [[RIGHTS-STATUS]] |  |  |

## 4. 角色与场景连续性约束

| 约束 ID | 对象 ID | 类型 | 进入状态 | 离开状态 | 服装 / 伤病 / 污损 | 道具 / 空间位置 | 禁止漂移项 | 证据场景 |
|---|---|---|---|---|---|---|---|---|
| CON-[[ID]] | CHAR-[[ID]] / SC-[[ID]] / ASSET-[[ID]] | 角色 / 场景 |  |  |  |  |  | SC-[[ID]] |

## 5. 声音、字幕与 UI 清单

| 规范 ID | 类型 | 关联 Shot / Scene | 内容或来源 | 语言 / 版本 | 时间码 / 同步点 | Rights ID | 人工复核人 | 批准决定 |
|---|---|---|---|---|---|---|---|---|
| AUDIO-[[ID]] | 对白 / 旁白 / 音效 / 音乐 | SHOT-[[ID]] | SRC-[[ID]] |  |  | RGT-[[ID]] |  | PENDING / APPROVED / REJECTED |
| SUB-[[ID]] | 字幕 / 屏幕文字 / UI | SHOT-[[ID]] | [[文本或设计稿路径]] |  |  | RGT-[[ID]] |  | PENDING / APPROVED / REJECTED |

## 6. AI / 实拍执行说明与失败降级

| Shot ID | 执行方式 / 工具版本 | 关键帧 / 输入资产 | 执行说明或 Prompt ID / 嵌入块 | 失败触发 | 最小降级方案 | 是否改变故事事实 | 批准人 |
|---|---|---|---|---|---|---|---|
| SHOT-[[ID]] | AI / 实拍 / 混合 | ASSET-[[ID]] | [[PROMPT-ID 或本表内说明]] |  |  | 是 / 否 |  |

## 7. 权利、来源与人工复核

| 规范 ID | 交付对象 | Source ID | Rights ID / 状态 | 证据路径 | 人工复核人 | 批准决定 | 复核日期 |
|---|---|---|---|---|---|---|---|
| RGT-[[ID]] | ASSET-[[ID]] / AUDIO-[[ID]] / SUB-[[ID]] | SRC-[[ID]] | RGT-[[ID]] / [[RIGHTS-STATUS]] | [[许可、来源或授权证据路径]] |  | PENDING / APPROVED / REJECTED |  |

## 8. 子交付物 ID 与嵌入规则

| 子交付物 | 规范 ID | 存储方式 | 路径或嵌入位置 | 上游 ID | 当前状态 |
|---|---|---|---|---|---|
| 镜头 | SHOT-[[ID]] | 独立文件 / 本表嵌入 |  | SC-[[ID]] |  |
| 声音 | AUDIO-[[ID]] | 独立文件 / 本表嵌入 |  | SHOT-[[ID]] |  |
| 字幕 / UI | SUB-[[ID]] | 独立文件 / 本表嵌入 |  | SHOT-[[ID]] |  |
| 资产 | ASSET-[[ID]] | 独立文件 / 本表嵌入 |  | BIBLE-[[ID]] |  |
| 权利 / 来源 | RGT-[[ID]] / SRC-[[ID]] | 独立登记 / 本表引用 |  | ASSET-[[ID]] |  |

## 9. 交接门禁

- [ ] 剧本已锁定，且 `content_digest` 与交接记录一致
- [ ] 所有场景均映射到 Scene Card
- [ ] 角色、服装、伤病、道具和地点状态已核验
- [ ] 镜头、声音、字幕和 UI 使用同一项目基线
- [ ] 第三方素材具备独立权利记录
- [ ] 未关闭 P0 已阻断生产
- [ ] 制作降级不静默改变人物选择与因果结果
