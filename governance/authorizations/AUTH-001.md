---
artifact_id: AUTH-001
artifact_type: AUTHORIZATION
project_id: PROJECT-PROFESSIONAL-SCREENWRITER
project_baseline: CONTRACT-v0.2.0
artifact_version: v0.1.0
status: APPROVED
owner: LaoYu-Professional-Screenwriter
reviewer: YuYingRay
approver: YuYingRay
test_run_id: RUN-ACTIVATION-20260821-001
conformance_level: HUMAN_REVIEWED
upstream_ids: [CONTRACT-PROFESSIONAL-SCREENWRITER, NOTICE-CONTRACT-001]
evidence_refs: [PLAN-v1.0.9, PLAN-FREEZE-V109-20260821-001, MANIFEST-VIEW-ANCHOR-20260821-001]
authorization_scope: PREPARE_ONLY_STAGING
authorization_date: 2026-08-21
---

# AUTH-001：拟签 staging 准备授权

## 授权范围

余老师授权按冻结计划 `v1.0.9 +
200171F5EA4CC76F21FB03719F2E19345D3091EEE51E95E360628C7859FFC0F8 + 757 行`：

- 建立隔离的 prepare-only staging；
- 按 `MANIFEST-VIEW-ANCHOR-20260821-001` 构造拟激活最终 payload；
- 运行只读 preflight、白名单、剩余原始字节与 diff 排他验证；
- 计算并向用户呈交精确 canonical digest。

本授权不允许运行 activation RUN，不允许提交、切换 active baseline 或发布；也不等于用户已经
确认拟签 digest。

## ACT-TRUST-001 披露

四任务实测读取过 `governance/control-plane-contract.md`，其中六份 trace 还读取过
`governance/project-manifest.md`。因此，本次七个合同状态/签署字段与 Manifest 两个基线字段的
变化不会影响模型产出，只是一个**未经 A/B 因果验证、可被未来证据推翻的治理信任假设**，不是
已证明的测量等价。

该假设不改变 `E.4.1-C` 或 `E.5`，不把 T2-D4、T4-D5、T1 Token、T4 Token 的正式 FAIL 改成
PASS，也不构成以后候选的先例。若路由或 trace 显示这些字段参与模型可见材料选择、白名单扩展、
冻结 benchmark 集合改变、候选行为或交付范围改变，ACT-TRUST-001 立即失效并触发受影响任务重测。

## 接受与生效边界

本文件只记录 prepare-only 授权来源与假设披露，**不记录用户已经接受 ACT-TRUST-001，也不保留
任何拟回填的确认槽位**。用户接受必须与最终精确 digest 的确认一起，以单独事件写入 skill 外
execution ledger，并绑定 `manifest_final_sha`。该事件不存在时，staging 不得激活。
