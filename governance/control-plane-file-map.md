# 控制契约与现有文件映射

> 本文件是迁移地图，不替代 `control-plane-contract.md`。唯一规范源是控制平面契约。

| 文件/目录 | 契约角色 | 迁移动作 | 权威级别 |
|---|---|---|---|
| `SKILL.md` | 运行时行为、故事原则、路由 | 保留核心原则；删除重复状态与字段定义 | 行为规范 |
| `README.md` | 导航、快速开始、架构说明 | 只做导航，引用控制契约 | 非规范 |
| `references/film-series-format.md` | 电影/剧集方法 | 保留载体规则 | 领域参考 |
| `references/short-drama-playbook.md` | 竖屏方法 | 保留短剧节奏规则 | 领域参考 |
| `references/hook-paywall-engine.md` | 钩子、兑现、付费点 | 接入 EP/承诺追踪 | 领域参考 |
| `references/screenplay-format-cn-en.md` | 剧本格式 | 保留格式规则 | 格式参考 |
| `references/story-bible-templates.md` | Bible 方法 | 与 Full Bible 模板去重 | 领域参考 |
| `references/adversarial-review-rubric.md` | 红队方法 | 保留人工审查标准 | 审查参考 |
| `references/ai-production-handoff.md` | AI/实拍交接方法 | 对接正式交接模板 | 领域参考 |
| `templates/story-bible.md` | Full Bible Artifact | 所有项目启用；字段状态化 | 模板 |
| `templates/scene-card.md` | Scene Card Artifact | 固定 `SC-*`，支持拆分/合并 lineage | 模板 |
| `templates/episode-outline.md` | 单集/结构 Artifact | 接入 EP/BEAT/SC 依赖 | 模板 |
| `templates/vertical-episode.md` | 竖屏单集 Artifact | 接入钩子、兑现、付费点 | 模板 |
| `templates/feature-screenplay.fountain` | 剧本主源 | 每场加入可解析 `SC-*` | 模板 |
| `templates/review-report.md` | Review Artifact | 分离 Review Decision 与 Test Result | 模板 |
| `templates/production-handoff.md` | Production Handoff Artifact | 新增正式交付模板 | 模板 |
| `governance/project-manifest.md` | 项目控制台 | 服从项目阶段与基线契约 | 项目控制 |
| `governance/upstream-notices.md` | Notice 索引 | `UN-*` 迁移为 `NOTICE-*` | 变更控制 |
| `governance/source-links.md` | 主张与证据 | 接入 `CLM-* / SRC-*` | 证据控制 |
| `governance/change-log.md` | 版本摘要 | 不承担逐次影响分析 | 历史摘要 |
| `LICENSES/skill-license.md` | Skill 许可证 | 与前置声明统一为 CC BY 4.0 | 权利规范 |
| `LICENSES/third-party-notices.md` | 第三方声明 | 与 Skill 原创内容分离 | 权利记录 |
| `LICENSES/asset-rights-register.md` | 资产权利 | 接入 `RGT-* / ASSET-*` | 权利记录 |
| `tests/README.md` | 测试运行说明 | 引用契约，不另定义状态 | 测试说明 |
| `tests/expected-deliverables.md` | 验收断言 | 成为契约的可验证投影 | 验收规范 |
| `tests/feature-project-fixture/` | 长片 E2E 实例 | 补齐最小完整链路与失败注入 | 测试实例 |
| `tests/vertical-project-fixture/` | 竖屏 E2E 实例 | 补齐季图、单集、钩子与付费链路 | 测试实例 |

## 迁移优先级

1. 控制契约、Skill frontmatter、状态/ID/权威冲突；
2. Manifest、Full Bible、Scene Card、Review、Notice；
3. Fountain 场景映射与 Production Handoff；
4. 测试夹具、验证器和失败注入；
5. README、示例和历史说明清理。
