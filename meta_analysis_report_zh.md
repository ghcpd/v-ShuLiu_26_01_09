# 元分析：Todo API 服务的协作与运维

## 摘要
仓库中在 `CONTRIBUTING.md`、`docs/api_versioning.md`、`ops/oncall.md` 等文件中定义了较为清晰的目标流程，但在实际操作中经常出现偏离：很多事故是通过紧急热修和 Slack 协同解决，而不是完全按照“先 GitHub、再按流程”的方式执行。本报告梳理规则在哪里被写下、实际是如何被执行的，以及一名新加入的后端工程师或 SRE 需要掌握的关键点。

## 文档中宣称的流程
- 贡献与评审规则在 `CONTRIBUTING.md` 中：
  - 分支命名（如 feature 分支、hotfix 分支等）
  - 由 `@backend-core` 进行审批
  - 合并前必须通过 CI
- 事故与值班期望在 `ops/oncall.md` 和 `ops/incidents.md` 中：
  - 响应 SLA
  - 创建带有 `incident` 标签的 issue
  - 进行事后复盘
- API 版本管理指导草案在 `docs/api_versioning.md` 中：
  - 引入 `/v2` 路径
  - 保留 `/v1` 一段弃用期
- 标签约定在 `.github/LABELS.md` 中：
  - area、severity、status 等标签命名与推荐用法。

## 实际观察到的实践（带证据）
- 热修与紧急合并：
  - PR #213 作为热修 PR 被合并，说明中明确提到在 CI 部分失败的情况下使用了“admin override”（见 `.github/PULL_REQUESTS.md` 中对 PR #213 的记录）。
  - PR #215 是另一例针对后台 worker 问题的热修。
- 事故记录不一致：
  - `ops/incidents.md` 记录了 2024-10-01 `GET /todos` 的 Sev1 故障，将其与 PR #210 和后续的 PR #213 关联，但同时注明“部分讨论发生在 Slack，未完全拷贝到此处”。
  - 2024-11-12 worker stall 事件在 Issue #102 中跟踪，并由 PR #215 修复，但 postmortem 记录并不完整。
- 标签与严重级别使用不统一：
  - 仓库中混用了 `sev1`、`sev-1`、`priority-high` 等多种形式，`.github/LABELS.md` 与 `ops/incidents.md` 中对相关事件的描述也反映了这种不一致（例如：worker stall 在 notes 中写为“Sev1”，而 GitHub issue 使用 `sev-1`）。
- 破坏性 API 变更先于治理机制落地：
  - PR #220 引入了 `/v2/todos`，而此时 `docs/api_versioning.md` 仍然保留“谁来授权破坏性变更”的未决问题。
- 项目维护里程碑：
  - `.github/MILESTONES.md` 尝试将事件与 issue（如 #101、#102）关联，但从 PR → incident → 正式 postmortem 的链路经常不完整（例如 PR #210 → Issue #101，当时并没有单独的 postmortem issue）。

## 关键不一致与风险点
- Sev1 文化偏向“先把问题解决”：
  - 紧急修复（admin merge、hotfix 分支）被高度优先，仓库经常跳过完整的 GitHub 事故流程与复盘闭环，降低了长期可追溯性（PR #213、`ops/incidents.md` 中的备注）。
- 元数据漂移：
  - 多套标签/严重级别并行存在，让自动化分流与筛选变得脆弱（`.github/LABELS.md`、`ops/oncall.md`）。
- 破坏性变更的签核不清晰：
  - `docs/api_versioning.md` 明确承认尚未定义破坏性变更的批准人，但 PR #220 中仍然推进了新的主要 API surface。
- 值班期望 vs 实际：
  - `ops/oncall.md` 中要求创建事故 issue 并进行复盘，但事故记录与 PR 讨论显示实际执行中更多依赖 Slack 升级、且部分事件缺乏完整 postmortem。

## 新的后端工程师或 SRE 必须了解的事项 ✅
- 预期“高压下的紧急节奏”：
  - Sev1 通常通过 hotfix 分支和快速合并解决（参见 PR #213、PR #215），需要在第一时间与值班 oncall 协同，Slack 会是关键沟通渠道。
- 不要盲目信任元数据：
  - 严重级别标签混用 `sev1` / `sev-1` / `priority-high`，需要结合 issue 文本和 incident 记录进行人工判断。
- 在遵循既有流程的同时，保证“轨迹可追溯”：
  - 处理故障时要确保创建或关联带有 `incident` 标签的 issue，将后续笔记补充进 `ops/incidents.md`，并尽量把热修 PR 和事故 issue 对应起来（这是 `CONTRIBUTING.md` 与 `ops/incidents.md` 的设计初衷）。
- 对提出破坏性 API/DB/infra 变更时的注意事项：
  - 在 `docs/api_versioning.md` / RELEASE_NOTES 中记录变更，并在 PR 中明确期望的审批人——仓库目前没有单一清晰的最终审批角色，一些决策是以相对非正式的方式做出的（见 PR #220 及 `docs/api_versioning.md`）。

## 面向上手的简短建议（实战导向）
- 响应事故时：
  - 即使主要协调发生在 Slack 里，也要创建 GitHub incident issue，并将相关热修 PR 关联上，这样时间线才可保留（`ops/incidents.md` 中就提到过缺失 Slack 历史的问题）。
- 使用标签时：
  - 尽量采用更新的 `area:*` 和 `sev*` 形式；同时留意 `.github/LABELS.md` 所记录的旧标签或混用情况，以免误判历史数据。

---
本报告基于以下仓库文件与档案生成：`CONTRIBUTING.md`、`.github/LABELS.md`、`.github/PULL_REQUESTS.md`、`.github/MILESTONES.md`、`docs/api_versioning.md`、`ops/incidents.md`、`ops/oncall.md` 等（文中所引事件与示例均来源于这些资料）。
