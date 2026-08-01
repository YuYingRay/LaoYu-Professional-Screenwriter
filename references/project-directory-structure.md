# STRUCT-LAYERED 项目目录规范

## 快速目录

- `# 1. 唯一结构`
- `# 2. 合法子集`
- `# 3. 旧结构迁移`
- `# 4. 路径职责`

# 1. 唯一结构

项目采用 `STRUCT-LAYERED`：

```text
[[project-root]]/
├── governance/
│   ├── project-manifest.md
│   ├── source-links.md
│   ├── upstream-notices.md
│   ├── change-log.md
│   ├── continuity-log.md
│   └── rights-register.md
├── development/
│   ├── story-bible.md
│   ├── feature-outline.md
│   ├── season-outline.md
│   ├── episode-outlines/
│   ├── scene-cards/
│   ├── information-matrix.md
│   ├── timeline.md
│   └── review-reports/
├── script/
│   ├── master/
│   │   └── [[project]].fountain
│   ├── revisions/
│   └── exports/
├── production/
│   ├── handoff/
│   ├── breakdowns/
│   ├── shot-lists/
│   ├── storyboards/
│   ├── voice/
│   ├── subtitles/
│   └── ui/
├── assets/
│   ├── characters/
│   ├── locations/
│   ├── props/
│   ├── wardrobe/
│   └── references/
└── archive/
    ├── superseded/
    └── released/
```

# 2. 合法子集

项目只创建实际需要的目录；空目录不是完成证据。合法子集必须满足：

- 所有正式工件位于上述六个职责根之一；
- `governance/project-manifest.md`始终存在；
- Story Bible、大纲/分集、Scene Card 与 Review 位于 `development/`；
- 剧本主源位于 `script/master/`；制作交接位于 `production/handoff/`；
- 省略目录不改变 Manifest → Bible → 结构/场景 → 剧本 → 交接的事实控制链。

# 3. 旧结构迁移

| 旧路径族 | 新路径族 |
|---|---|
| `00_admin/` | `governance/` |
| `01_core/`、`02_characters/`、`03_structure/`、`04_continuity/` | `development/` |
| `05_scripts/` | `script/` |
| `06_production/` | `production/` |
| `02_assets/` | `assets/` |
| `99_archive/` | `archive/` |
| 根级 `story/`、`structure/`、`scenes/`、`episodes/`、`reviews/` | `development/` 对应子目录 |

# 4. 路径职责

目录只表达职责，不表达 Artifact 状态。权威身份、版本、状态与上游关系仍以工件元数据和
`governance/control-plane-contract.md`为准；移动文件不得改变其 `artifact_id`。
