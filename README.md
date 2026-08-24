# LaoYu Professional Screenwriter

面向电影、剧集、竖屏短剧和 AI 影视生产的专业编剧 Skill，覆盖故事开发、剧本诊断、连续性治理、权利清理与生产交接。

> 本 README 只用于 GitHub 仓库介绍与维护者导航。它不是 Skill 运行入口，不进入模型加载路由，不属于项目验证域，也不进入 `run_payload`。运行时规则以 [`SKILL.md`](SKILL.md) 及其按任务路由的规范文件为准。

## 仓库入口

- [`SKILL.md`](SKILL.md)：Skill 运行入口与任务路由。
- [`governance/control-plane-contract.md`](governance/control-plane-contract.md)：状态、权威层级与门禁的规范主源；变更等级见 [§7.2](governance/control-plane-contract.md#72-变更等级与最低门禁)。
- [`tests/testing-guide.md`](tests/testing-guide.md)：本地验证与测试说明。
- [`LICENSE`](LICENSE)：CC BY 4.0 许可文本；第三方与资产权利记录见 [`LICENSES/`](LICENSES/)。

## 本地验证

```powershell
python -X utf8 scripts/check_all.py . --mode strict
```
