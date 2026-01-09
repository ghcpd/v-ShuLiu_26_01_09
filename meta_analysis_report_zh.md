# 元分析：协作与运维模式——Todo API 服务

总结
- 简要结论：仓库在事故处理、热修与 API 版本管理方面有相对清晰、务实的文档，但在时间压力下，实际行为经常偏离这些流程（标签漂移、跳过事后复盘、临时热修直接合并等）。下面通过具体示例给出证据。✅

## 1）快速导览（给新后端工程师或 SRE）
- 首先阅读：`CONTRIBUTING.md`、`ops/oncall.md`、`ops/incidents.md`、`docs/api_versioning.md`。📚
- 基本故障分诊流程：新发生的故障需要创建一个带有 `incident` 标签的 issue，并添加严重级别标签（推荐使用 `sev1`）。具体可参考 `ops/oncall.md` 和 `CONTRIBUTING.md`。
- 常见的热修模式：创建分支 `hotfix/<incident-id>`；在故障期间，值班维护者有时会直接合并到 `main`（示例见 `.github/PULL_REQUESTS.md` 中汇总的若干 PR）。⚠️

## 2）主要的协作与治理模式（基于观察）
- 仓库存在较完整的正式文档：`CONTRIBUTING.md`（热修分支、标签）、`docs/api_versioning.md`（API 版本规则）、`ops/oncall.md` / `ops/incidents.md`（事故处理期望）。
  - 证据：`CONTRIBUTING.md` 中描述了热修工作流和 Sev1 事故必须打 `sev1` 的要求；`docs/api_versioning.md` 详细写了版本管理规则。
- 值班 SRE 在事故期间是主要响应人，并在操作层面拥有较大的自主权（调查、回滚、合并热修）。
  - 证据：`ops/oncall.md` 中对 oncall 职责的描述；`ops/incidents.md` 中 2024-10-01 事故时间线展示了值班 SRE 的行为；`.github/PULL_REQUESTS.md` 中也保存了若干 oncall/admin 直接合并的 PR 示例。
- 社区贡献者与 SRE 共同承担评审职责，但对“破坏性变更”的最终批准人缺乏清晰定义，往往临时决定。
  - 证据：`docs/api_versioning.md` 中直接写明“尚不清楚谁拥有最终决策权”；`.github/PULL_REQUESTS.md` 和 `.github/ISSUES.md` 中多次出现关于审批权的讨论。

## 3）事故与热修在实际中的处理方式（证据驱动）
- 预期流程：15 分钟内响应，创建 `incident` issue，打上 `sev1` + 对应功能域标签，并在事后安排复盘（参见 `ops/oncall.md`、`CONTRIBUTING.md`）。
- 实际偏差：
  - 标签不一致：issue 中 `sev1`、`sev-1`、`priority-high` 混用（参考 `ops/oncall.md`、`.github/ISSUES.md`、`.github/LABELS.md`）。例如：Issue #102 使用的是 `sev-1`，但事故日志中记录为 `Sev1`（见 `ops/incidents.md` / `.github/ISSUES.md`）。
  - 事后复盘缺失或非常简略：一些 Sev1 事故通过 PR 修复后，并没有在 `ops/incidents.md` 中留下完整复盘记录（如 PR #213、PR #215 以及 `.github/ISSUES.md` 中的备注）。
  - 热修快车道：维护者或值班同学有时会在测试不稳定（flaky）的情况下，使用管理员权限快速合并热修 PR（`.github/PULL_REQUESTS.md` 中 PR #210 的摘要和讨论有体现）。在故障情景下这被视为可接受做法，但文档并未统一记录这种例外策略。

## 4）破坏性 API / 数据库 / 基础设施变更的提出与批准
- 文档中的要求：破坏性 API 变更需要引入新版本路径（如 `/v2`），并在 `docs/api_versioning.md` 和发版说明中记录；部署/基础设施变更需要由 SRE/平台团队评审（`CONTRIBUTING.md`）。
  - 证据：`docs/api_versioning.md` 中的版本管理策略；`CONTRIBUTING.md` 中“Deployment/infra changes: reviewed by @sre or @platform”的说明。
- 实际行为与缺口：
  - 实际审批权模糊——讨论常常退化为“由当前 oncall 或当时在线的人拍板”（见 `.github/ISSUES.md`、`.github/PULL_REQUESTS.md`）。
  - 与版本管理相关的 ADR 以及指导文档还处于草稿状态，且在合并 PR 时有时被忽略（`.github/PULL_REQUESTS.md` 中有开发者提到“API versioning ADR 仍在草稿中，先合并再补文档”）。
  - 事故期间的 DB 迁移可能出现“只回滚基础设施、不回滚数据库”的情况——`.github/ISSUES.md` 中有记录，比如一次 K8s 回滚并没有同时回滚 DB 迁移，被标记为问题。

## 5）所有权与职责（后端 vs SRE/平台）
- 文档中宣称的划分：
  - 后端：API 实现、功能行为、维持 API 兼容性（见 `docs/api_versioning.md`、`CONTRIBUTING.md`）。
  - SRE/平台：部署、值班/oncall、基础设施变更、监控运维。
  - 证据：`CONTRIBUTING.md`、`ops/oncall.md` 中对职责的描述。
- 实际上的交叠与交接模式：
  - 值班 SRE 在事故期间做出绝大部分操作决策（包括紧急合并和回滚）。`.github/ISSUES.md` 中有明确表述“在事故情景下，由当前 oncall 决定”。
  - 理论上，平台团队应该评审所有 infra 变更，但在现实中，由于临时合并与审批权模糊，所有权往往退化为“谁在线谁负责”。

## 6）文档与行为之间的关键不一致（附证据的简表）
| 主题 | 文档中的规定 | 实际 / 观察到的情况 | 示例证据 |
|---|---:|---|---|
| 严重级别标签 | 使用 `sev1`/`sev2`/`sev3`（见 `.github/LABELS.md`） | 实际混用 `sev-1`、`priority-high` 等 | Issue #102；`.github/ISSUES.md`；`ops/oncall.md` 中对标签漂移的说明 |
| 事故复盘 | 要求在 `ops/incidents.md` 中撰写 postmortem | 一些 Sev1 事故没有正式复盘，只在评论中略有提及 | PR #213、PR #215；`.github/ISSUES.md` |
| 破坏性变更审批 | 需遵循 `docs/api_versioning.md` 并获得评审 | 实际审批权不清，部分变更在 ADR 完成前即被合并 | `.github/PULL_REQUESTS.md` 中的讨论；`docs/api_versioning.md` 的备注 |
| 紧急合并 / 测试要求 | 正常流程要求测试通过，走标准评审 | 事故期间允许 oncall/admin 在测试不稳定时直接合并 | `.github/PULL_REQUESTS.md`（PR #210 示例） |

## 7）新后端工程师或 SRE 需要了解的要点（实用清单）🔧
- 推荐阅读顺序：`CONTRIBUTING.md` → `ops/oncall.md` → `ops/incidents.md` → `docs/api_versioning.md`。✅
- 故障分诊：创建 `incident` issue，添加 `sev1`/`sev2`/`sev3`（推荐统一使用 `sevN` 形式），并根据影响面打上 `area:api|db|infra` 等标签（参考 `ops/oncall.md` 和 `.github/LABELS.md`）。
- 热修流程：为每个事故创建 `hotfix/<incident-id>` 分支；在故障期间预期 oncall 会走快速合并流程——事后要记得在 `ops/incidents.md` 中补充复盘链接（参见 `CONTRIBUTING.md` 与 `.github/PULL_REQUESTS.md` 中的实践）。
- 破坏性变更：默认假定需要同时获得后端和 SRE/平台评审；若有疑问，可以先开一个 ADR，并在 PR 中链接。`docs/api_versioning.md` 是期望行为的来源，但其内容偏草稿，如遇冲突要主动向维护者升级与确认最终决策。
- 沟通渠道：在 oncall 的即时沟通渠道（如 Slack）中及时升级问题——很多实际决策是在这些渠道完成的，并不会完全反映在文档中（`.github/ISSUES.md` 中也提到缺少公开升级路径的问题）。

## 8）项目可以进行的低成本改进（运维层面，而非功能层面）
- 统一严重级别标签（推荐统一用 `sev1`），并在 `CONTRIBUTING.md` 中增加简短的标签使用指南（证据：`ISSUES.md` / `LABELS.md` 中可以看到标签漂移）。
- 强制或自动化要求将热修 PR 与事故 issue / postmortem 关联，避免后续跟踪缺失（`.github/PULL_REQUESTS.md`、`ops/incidents.md` 中都有缺链示例）。
- 明确谁有权批准破坏性 DB/Schema 变更（产品 vs 后端 vs SRE），并在 `docs/api_versioning.md` 或专门的 ADR 中固化下来。

## 9）底线结论（一段话总结）
该仓库在协作与值班方面有一套合理且务实的文档，团队在实际 incident 处理中也采取了非常实用的做法（由 oncall 主导热修与快速回滚）。但标签漂移、事后复盘缺失，以及破坏性变更审批权不清，是反复出现的结构性问题——新同学应预期：关键决策大多由当班 oncall 拍板，并主动把“事故 → 热修 PR → postmortem”这条链条串起来。🔎

---
引用的主要资料（节选）：`CONTRIBUTING.md`、`ops/oncall.md`、`ops/incidents.md`、`docs/api_versioning.md`、`.github/LABELS.md`、`.github/PULL_REQUESTS.md`、`.github/ISSUES.md`、Issue #102、PR #210、PR #213、PR #215、PR #221。

（本报告基于仓库工件自动生成；如果需要，我可以起一个小 PR，统一标签并增加简短的“事故处理清单”。）
