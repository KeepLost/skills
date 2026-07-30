---
name: project-workflow
description: Use only when an OpenCode task is orchestrated by OpenClaw, project-workflow is explicitly requested, or the project contains managed session/status files; loading it activates the kickoff, stop-the-line, status sync, notifier, local Git, and handoff contract.
---

# Local Project Management Workflow

## Routing Note

This is the managed-protocol entrypoint only for an OpenClaw-orchestrated OpenCode task, an explicit `project-workflow` request, or a project containing managed session/status files. Outside those conditions, it does not claim routing priority over ordinary development work.

## ⚠️ CRITICAL: Read This First

**This skill is MANDATORY only while the managed protocol is active.**

While the managed protocol is active, before starting the project, implementing a feature, or making changes, you MUST follow this workflow. It ensures:
- Proper project structure and version control
- Auditable progress tracking
- Effective communication between AI agents
- Reproducible and maintainable code
- Continuous alignment with top-level architecture intent
- Early stop-the-line reporting instead of silent architectural drift

---

## Part 0: Architecture Governance Model

The goal is not only to produce code that passes tests. The goal is to produce code that still serves the project's top-level architectural intent. Smooth progress can be dangerous when specs are incomplete: if you keep coding while confused, you may silently make architecture decisions on behalf of the designer.

### Normative Project Documents

For complex or architecture-affecting projects, recognize these documents as normative project knowledge:

```text
AGENTS.md
opencode.json
docs/CONTEXT_MANIFEST.md
docs/ARCHITECTURE_CONSTITUTION.md
docs/TECHNICAL_SPEC.md
docs/adr/INDEX.md
status/
```

Rules:
- `docs/` contains confirmed long-term project knowledge and should be versioned in git.
- `status/` contains current agent communication and should not be versioned in git.
- `status/archive/` may hold milestone snapshots, but current `status/` files must stay current, not become a chat log.
- If required normative docs are missing for a complex/architecture-affecting task, do not guess. Write `status/questions.md` and stop.

### Confusion Level Protocol

Classify uncertainty before implementation and whenever a new ambiguity appears:

```text
0 = completely clear
1 = minor question, does not affect implementation
2 = local implementation assumption, non-architectural
3 = design ambiguity may affect architecture
4 = task goal or architecture direction unclear
5 = continuing would create significant risk
```

Rules:
- Level 0-1: proceed normally.
- Level 2: proceed only if the assumption is non-architectural and documented in `status/kickoff.md` or `status/execution-report.md`.
- Level >= 3: stop, write `status/questions.md`, update progress as blocked, send notifier, and wait.

### Stop-the-Line Rules

Stop and report instead of continuing implementation if:

1. a required normative document is missing for a complex/architecture-affecting task;
2. the technical spec is ambiguous;
3. normative documents conflict;
4. the task requires violating the technical spec;
5. existing code violates the architecture constitution and the task depends on it;
6. implementation requires an undocumented architecture assumption;
7. continuing requires a workaround, bypass, or temporary path that affects architecture;
8. a security or permission boundary is unclear;
9. a feature can be implemented locally but does not clearly enter the main path;
10. confusion level is >= 3.

When stopped, write `status/questions.md` using the required format, update `status/latest.progress.md`, send notifier, and wait for clarification. Stop-the-line is valid productive work.

**Hard rule (no silent stop):** whenever execution is paused/stopped for any reason (blocked, waiting for clarification, process mismatch, or manual pause), OpenCode MUST proactively notify OpenClaw with the stop reason and the exact next required confirmation/action. Silent stopping is prohibited.

---

## Part 1: Project Initialization

### ⚠️ MANDATORY: Create TODO List FIRST

**Before executing ANY initialization steps, create a TODO list using todowrite:**

```
todowrite([
  {"content": "创建项目目录结构", "status": "pending", "priority": "high"},
  {"content": "初始化 Git 仓库", "status": "pending", "priority": "high"},
  {"content": "创建 .gitignore 文件", "status": "pending", "priority": "high"},
  {"content": "初始化环境（Python/Node.js）", "status": "pending", "priority": "high"},
  {"content": "创建初始提交", "status": "pending", "priority": "high"},
  {"content": "更新 status/latest.progress.md", "status": "pending", "priority": "high"},
  {"content": "记录到 status/history.progress.md", "status": "pending", "priority": "high"}
])
```

**Mark each item `in_progress` before starting, `completed` immediately after finishing.**

If `todowrite` is unavailable in the current runtime, do not block or invent tool results. Instead maintain `status/todo.md` with the same pending/in_progress/completed structure and continue the workflow.

### When to Initialize
- ✅ Starting any new code project
- ✅ First time working on an existing project without proper structure
- ✅ Before writing any significant code

### Standard Setup Sequence

```bash
# 1. Create project structure
mkdir -p codes/<project-name>/status/tmp
cd codes/<project-name>

# 2. Initialize Git
git init
git branch -M main

# 3. Create .gitignore FIRST (before any commits)
cat > .gitignore << 'EOF'
# Status directory (agent communication, NOT versioned)
status/

# Python
.venv/
venv/
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.pytest_cache/
.coverage

# Node.js
node_modules/
package-lock.json

# Test data
data/
datasets/
*.csv
*.db
*.sqlite

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Secrets
.env
.env.local
*.key
*.pem
credentials.json

# Logs
*.log
logs/

# Temporary files (use status/tmp/ instead)
temp/
tmp/
EOF

# 4. Environment initialization
# For Python projects:
uv venv .venv
source .venv/bin/activate
uv init  # Creates pyproject.toml

# For Node.js projects:
npm init -y

# 5. Initial commit
git add .
git commit -m "Initial commit: Project structure and configuration"

# 6. Record git operation in status
tmp=$(mktemp status/tmp/oc_XXXXXXXXXX.md)
cat > "$tmp" << EOF
[$(date '+%Y-%m-%d %H:%M')] 状态: 进行中
当前: 项目初始化完成，已创建 git 仓库和基础配置
下一步: 开始实现功能
Git操作: git init + initial commit
EOF
mv "$tmp" status/latest.progress.md
echo "[$(date '+%Y-%m-%d %H:%M')] 项目初始化，git init + initial commit" >> status/history.progress.md

```

### Critical: status/ Directory

**Purpose**: Communication channel for agent status tracking

**Must NOT be in Git**: Already excluded in `.gitignore`

**Why separate from Git?**
- Git tracks code changes
- status/ tracks development progress and agent communication
- Git operations are recorded IN status/ for auditability

**Files in status/**:

| File | Written By | Read By | Purpose | Size Limit |
|------|------------|---------|---------|------------|
| `task-spec.md` | External | OpenCode | Task specification and acceptance criteria | No hard limit (be concise) |
| `confirmed.items.md` | External | OpenCode | Latest confirmations and directives | 600 chars |
| `kickoff.md` | OpenCode | External | Proof of reading, understanding, assumptions, and go/no-go before source changes | concise but complete |
| `questions.md` | OpenCode | External | Stop-the-line questions and blocking ambiguities | concise |
| `latest.progress.md` | OpenCode | External | Current status snapshot | 500 chars |
| `history.progress.md` | OpenCode | External | Chronological progress log | ≤60 chars per append |
| `arch-self-review.md` | OpenCode | External | Architecture compliance self-review before completion | No hard limit (be concise) |
| `execution-report.md` | OpenCode | External | Final completion report | No hard limit (be concise) |
| `archive/` | External/OpenCode | External/OpenCode | Milestone snapshots, not active current state | as needed |

---

## Part 2: Development Iteration Workflow

### ⚠️ MANDATORY: Create TODO List FIRST

**Before starting ANY development work, create a TODO list using todowrite:**

```
todowrite([
  {"content": "读取 AGENTS.md 与项目治理文档", "status": "pending", "priority": "high"},
  {"content": "读取 status/task-spec.md 与 status/confirmed.items.md", "status": "pending", "priority": "high"},
  {"content": "写 status/kickoff.md 并完成 go/no-go 判断", "status": "pending", "priority": "high"},
  {"content": "实现功能 X", "status": "pending", "priority": "high"},
  {"content": "实现功能 Y", "status": "pending", "priority": "high"},
  {"content": "写 status/arch-self-review.md", "status": "pending", "priority": "high"},
  {"content": "更新 status/latest.progress.md", "status": "pending", "priority": "high"},
  {"content": "记录到 status/history.progress.md", "status": "pending", "priority": "high"},
  {"content": "提交 git commit", "status": "pending", "priority": "high"}
])
```

**Mark each item `in_progress` before starting, `completed` immediately after finishing.**

**CRITICAL: Break down user requirements into specific, actionable TODO items. Each TODO should be a concrete step you can mark complete.**

**Milestone TODO hard requirements (mandatory):**
- For milestone-based work (e.g., E2→E7), TODOs MUST enumerate **every milestone goal from start to finish** with no omissions.
- Each milestone TODO MUST include an explicit **OpenClaw reporting step** (start, milestone progress, complete/blocked).
- A milestone is not complete until code/test/report/commit **and** OpenClaw notification are all done.

### Before Starting Work

**ALWAYS perform the Mandatory Context Gate first. Read in this order when files exist:**

```bash
# Project-local instructions and normative docs
[ -f AGENTS.md ] && cat AGENTS.md
[ -f docs/CONTEXT_MANIFEST.md ] && cat docs/CONTEXT_MANIFEST.md
[ -f docs/ARCHITECTURE_CONSTITUTION.md ] && cat docs/ARCHITECTURE_CONSTITUTION.md
[ -f docs/TECHNICAL_SPEC.md ] && cat docs/TECHNICAL_SPEC.md
[ -f docs/adr/INDEX.md ] && cat docs/adr/INDEX.md

# Current task communication
cat status/task-spec.md
[ -f status/confirmed.items.md ] && cat status/confirmed.items.md
[ -f status/questions.md ] && cat status/questions.md
```

If this is a complex or architecture-affecting task and any required governance document is missing or conflicts with another document, do not silently continue. Write `status/questions.md`, update `status/latest.progress.md` as blocked, notify, and stop. For small non-architecture tasks, missing governance docs may be non-blocking only if you explicitly record the reason in `status/kickoff.md`.

**Before modifying source code, write `status/kickoff.md`:**

```markdown
# Kickoff Meeting

## Documents Read

## My Understanding of the Task

## Top-Level Intent

## Applicable Rules

## Implementation Plan

## Assumptions

## Ambiguities / Conflicts

## Blocking Questions

## Can Implementation Start?
```

`Can Implementation Start?` must be an explicit yes before touching source code. If blocking questions exist, write `status/questions.md` and stop.

**confirmed.items.md Format** (written externally, read by OpenCode):
```
[YYYY-MM-DD HH:MM] 确认: <已确认的进展或决策>
[YYYY-MM-DD HH:MM] 指示: <接下来需要 OpenCode 注意/调整的事项>
```

This file contains latest confirmations and directives from external sources. Read it before each progress update to stay aligned.

### During Development

**Dependency Management:**

For Python projects:
```bash
# Add dependency
uv add <package>

# Add dev dependency
uv add --dev <package>

# Install all dependencies
uv sync
```

Note: if there exists problems on running `uv sync`, you could also manually install packages via methods like like
```bash
# Activate virtual environment
source .venv/bin/activate

uv pip install <package>
```

You shall use commands like `uv run python <script-name.py>` to run the Python scripts in current workspace, which is equivalent to the following way:
```bash
source .venv/bin/activate

python <script-name.py>
```

For Node.js projects:
```bash
npm install <package>
```

**NEVER modify global environments** (`/root/venv/base` or global npm)

**Decision Points:**
- Minor technical choices: document in code comments or execution report.
- Local non-architectural assumptions (confusion level 2): document in `status/kickoff.md` or `status/execution-report.md`.
- Major architectural decisions: do **not** decide alone. Write `status/questions.md` before implementation and stop.
- **DO NOT make major changes beyond task spec without confirmation.**

**When Blocked or Need Decision:**

- 2+ failed attempts at solving a problem
- Architectural decision beyond task spec
- Ambiguity in requirements that blocks progress
- Security/performance tradeoffs requiring human judgment
- Confusion level >= 3
- A local implementation would not clearly enter the main path
- Continuing requires a workaround, bypass, or temporary architecture path

Write `status/questions.md` first:

```markdown
# Open Questions

## Q1
Type: architecture / requirement / implementation / security
Blocking: yes/no
Context:
Options:
Recommendation:
Risk if unresolved:
Need answer from:
```

Then update blocked status:

```bash
# Extract TASK_ID from status/task-spec.md if present. Never invent "unknown" as an ID.
TASK_ID=$(grep -oE '^task[_-]id:[[:space:]]*[^[:space:]]+' status/task-spec.md 2>/dev/null | awk '{print $2}' | head -n 1)

# Update status to reflect blockage
tmp=$(mktemp status/tmp/oc_XXXXXXXXXX.md)
cat > "$tmp" << 'EOF'
[YYYY-MM-DD HH:MM] 状态: 已阻塞
当前: <描述当前问题>
下一步: 等待进一步指示
需要确认: 详见 status/questions.md
EOF
mv "$tmp" status/latest.progress.md
```

### Updating Progress

**Every time you make meaningful progress:**

```bash
# 1. Read latest directives first
cat status/confirmed.items.md 2>/dev/null

# 2. Update latest progress (atomic write via temp file)
tmp=$(mktemp status/tmp/oc_XXXXXXXXXX.md)
cat > "$tmp" << 'EOF'
[YYYY-MM-DD HH:MM] 状态: <进行中|已完成|已阻塞>
当前: <一句话说明刚完成了什么>
下一步: <下一个要做的事>
需要确认: <有则填写，无则省略>
EOF
mv "$tmp" status/latest.progress.md

# 3. Append to history (one-line summary, ≤60 chars)
echo "[YYYY-MM-DD HH:MM] <简短摘要>" >> status/history.progress.md
```

**Size Constraints:**
- `latest.progress.md`: Keep under 500 chars total
- `history.progress.md`: Each append must be ≤60 chars (excluding timestamp)

**For large content writes that fail mid-stream:** split content into bounded chunks, verify each chunk, and write through `status/tmp/` before atomically moving it to the target.

### OpenCode Notifier Integration

**Purpose**: Proactive notification system for real-time progress updates to external systems (OpenClaw). This manual notification path complements the external notifier service, which may also watch OpenCode's event stream/SSE and automatically notify OpenClaw when the session becomes idle, times out, or needs attention. OpenCode should keep working after sending interim notifications; it must not wait for OpenClaw unless blocked or explicitly asking for a decision.

The notifier helper loads its URL and token from protected runtime configuration. Never place live credentials in the skill directory, task text, status files, logs, or generated archives.

#### Getting Session ID

OpenClaw writes a `.session-sid` file in the current working directory when starting an OpenCode session. Read this file to get the session ID:

```bash
# Read SID
MY_SID=$(cat .session-sid 2>/dev/null)
```

#### Sending Proactive Notifications

At key progress milestones, use the notifier script in this skill's `scripts/` directory to send proactive notifications. The script loads URL and token values from protected runtime configuration; callers provide only `sid` and `message`.

Before sending, derive `TASK_ID` from `status/task-spec.md` if present. Never invent one and never send the literal placeholder `{task_id}`:

```bash
MY_SID=$(cat .session-sid 2>/dev/null)
TASK_ID=$(grep -oE '^task_id:[[:space:]]*[^[:space:]]+' status/task-spec.md 2>/dev/null | awk '{print $2}' | head -n 1)
if [ -n "$MY_SID" ]; then
  MSG="<进度描述>"
  [ -n "$TASK_ID" ] && MSG="任务 ${TASK_ID}: ${MSG}"
  if ! bash /root/.config/opencode/skills/project-workflow/scripts/notifier-send.sh "$MY_SID" "$MSG"; then
    echo "[$(date '+%Y-%m-%d %H:%M')] notifier 发送失败，已记录但不声称成功" >> status/history.progress.md
  fi
else
  # No registered route. Silently skip notification and continue; do NOT claim a notification was sent.
  :
fi
```

**Notification Trigger Points:**
- **Starting Work**: After reading task-spec.md and confirmed.items.md, before any coding, send "开始执行/开始开发 <task summary>" (prefix with real `task_id` only if it exists in task-spec.md).
- **TODO Progress** (阶段性进展): After completing each meaningful TODO/subtask, update `status/latest.progress.md`, append `status/history.progress.md`, then send a brief progress notification. This is an interim report indicating work is still ongoing. OpenClaw will only record this notification without intervention, and OpenCode should continue pushing forward.
- **Blocked**: After 2+ failed attempts or when human decision is needed, send blockage reason and required help, then stop and wait.
- **Any Stop/Pause**: Even if not technically blocked, if you stop or pause execution for any reason, immediately send a notifier message explaining why execution stopped and what confirmation or action is required to resume.
- **Task Complete** (最终完成): After tests pass and execution-report.md is written, send "任务完成，详见 execution-report.md". This signals full task completion, and OpenClaw will proceed with acceptance and follow-up processing.

**Milestone TODO-Notification Binding (mandatory):**
- If a TODO represents a milestone, create paired TODO items for:
  1) milestone implementation/verification, and
  2) milestone OpenClaw reporting + status file updates.
- Do not mark milestone TODO `completed` until both paired items are completed.

#### Important Notes
- `/notify` only requires `sid` and `message` - notifier automatically adds route/task context when configured.
- If `.session-sid` file doesn't exist (OpenClaw hasn't registered route), silently skip and continue; **do not claim a notification was sent**.
- If notifier script exits non-zero, record the failure in `status/history.progress.md`; **do not claim success** and do not retry endlessly.
- Messages should be concise (≤500 characters), avoid large code blocks or logs.
- This notification supplements `status/` file writes, doesn't replace them.
- Never silently stop. A stop/pause without an OpenClaw notification is a process violation.
- **TODO/Significant Progress notifications are interim reports only** - they indicate work is ongoing and do not signal task completion. OpenClaw will record these notifications without intervention, and OpenCode should continue pushing forward. Only after sending a Task Complete notification will OpenClaw proceed with acceptance and follow-up processing.
- Do not dump long unfinished TODO lists into `status/latest.progress.md`; keep `latest.progress.md` as a concise current-state snapshot. Use todowrite (or `status/todo.md` only when todowrite is unavailable) for detailed TODO tracking.

### Committing Code

**After completing a meaningful unit of work:**

```bash
# 1. Stage and commit code (status/ is already gitignored)
git add .
git commit -m "Descriptive message about what changed"

# 2. IMMEDIATELY record git operation in status
tmp=$(mktemp status/tmp/oc_XXXXXXXXXX.md)
cat > "$tmp" << 'EOF'
[YYYY-MM-DD HH:MM] 状态: 进行中
当前: <刚完成的工作内容>
下一步: <下一步计划>
Git操作: git commit -m "<commit message>"
EOF
mv "$tmp" status/latest.progress.md

echo "[YYYY-MM-DD HH:MM] git commit: <commit message 摘要>" >> status/history.progress.md
```

**Good commit messages:**
- "Add user authentication module"
- "Fix memory leak in data processor"
- "Refactor database connection logic"

**Bad commit messages:**
- "update"
- "fix"
- "wip"

### Git Operations Auditability

**CRITICAL RULE: Every git operation MUST be recorded in status/**

This ensures:
- ✅ All git operations are auditable
- ✅ Other AI agents (external systems) can track version control activity
- ✅ Complete development history is visible outside of git
- ✅ Progress and code changes are synchronized

**Examples:**

```bash
# After git commit
echo "[$(date '+%Y-%m-%d %H:%M')] git commit: Add feature X" >> status/history.progress.md

# After creating a branch
git checkout -b feature-experiment
echo "[$(date '+%Y-%m-%d %H:%M')] git checkout -b feature-experiment" >> status/history.progress.md

# After switching branches
git checkout main
echo "[$(date '+%Y-%m-%d %H:%M')] git checkout main" >> status/history.progress.md

# After merging
git merge feature-experiment
echo "[$(date '+%Y-%m-%d %H:%M')] git merge feature-experiment" >> status/history.progress.md
```

---

## Part 3: Task Completion

### ⚠️ MANDATORY: Create Completion TODO List FIRST

**Before starting completion process, create a TODO list using todowrite:**

```
todowrite([
  {"content": "验证所有接受标准已满足", "status": "pending", "priority": "high"},
  {"content": "运行代码并验证输出", "status": "pending", "priority": "high"},
  {"content": "运行测试（如适用）", "status": "pending", "priority": "high"},
  {"content": "清理临时文件", "status": "pending", "priority": "high"},
  {"content": "编写 status/arch-self-review.md", "status": "pending", "priority": "high"},
  {"content": "提交所有有意义的更改到 git", "status": "pending", "priority": "high"},
  {"content": "编写 status/execution-report.md", "status": "pending", "priority": "high"},
  {"content": "更新 status/latest.progress.md（标记完成）", "status": "pending", "priority": "high"},
  {"content": "记录到 status/history.progress.md", "status": "pending", "priority": "high"}
])
```

**Mark each item `in_progress` before starting, `completed` immediately after finishing.**

### Verification Checklist

**Before claiming completion, verify against `status/task-spec.md`:**

- [ ] All acceptance criteria met
- [ ] Code compiles/runs without errors
- [ ] Tests pass (if applicable)
- [ ] Actually run the program and verify output
- [ ] No temporary files left in project directory
- [ ] All meaningful changes committed to git
- [ ] `status/arch-self-review.md` written, even for non-architecture tasks

### Write Architecture Self-Review

Before writing the final execution report or claiming completion, write `status/arch-self-review.md` even if the task is not architecture-affecting:

```bash
tmp=$(mktemp status/tmp/oc_XXXXXXXXXX.md)
cat > "$tmp" << 'EOF'
# Architecture Self Review

## Changed Modules

## New or Changed Dependencies

## Main Path Integration

## Permission / Security Path

## Plugin Registration / Lifecycle

## Dead Code or Decorative Architecture Risk

## Compliance with Architecture Constitution

## Compliance with Technical Spec

## Assumptions Made

## Remaining Risks
EOF
mv "$tmp" status/arch-self-review.md
```

If there were no architecture-affecting changes, explicitly say so and list what was checked. Do not omit this file.

### Write Execution Report

```bash
tmp=$(mktemp status/tmp/oc_XXXXXXXXXX.md)
cat > "$tmp" << 'EOF'
# 执行报告

## 完成情况
- [x] 验收标准 1: <说明完成情况>
- [x] 验收标准 2: <说明完成情况>
- [x] 验收标准 3: <说明完成情况>

## 技术决策记录
- 决策 1: <选择了什么，为什么>
- 决策 2: <选择了什么，为什么>

## Architecture Review Summary
- arch-self-review.md written: yes
- architecture-affecting changes: yes/no
- main-path integration checked: yes/no
- permission/security path checked: yes/no
- decorative architecture risk: <none / describe>
- known architecture risks: <none / describe>

## Git 提交历史
- <commit hash>: <commit message>
- <commit hash>: <commit message>

## 遗留问题 / 技术债
- 问题 1: <描述>
- 问题 2: <描述>
（若无则写"无"）

## 需要人工决策的问题
- 问题 1: <描述>
（若无则省略此节）

## 验证结果
<实际运行输出或测试结果>
EOF
mv "$tmp" status/execution-report.md
```

### Update Final Status

```bash
tmp=$(mktemp status/tmp/oc_XXXXXXXXXX.md)
cat > "$tmp" << 'EOF'
[YYYY-MM-DD HH:MM] 状态: 已完成
当前: 所有验收标准已满足，执行报告已提交
下一步: 等待审查
Git操作: 最终提交已完成
EOF
mv "$tmp" status/latest.progress.md

echo "[YYYY-MM-DD HH:MM] 任务完成，执行报告已提交" >> status/history.progress.md
```

### Final Commit

```bash
git add .
git commit -m "Complete: <task summary>"

# Record final commit
echo "[$(date '+%Y-%m-%d %H:%M')] git commit: Complete <task summary>" >> status/history.progress.md
```

### Send Final Notification

After tests pass, `arch-self-review.md` and `execution-report.md` are written, final status is updated, and final commit is complete (if applicable), send one final notifier message:

```bash
MY_SID=$(cat .session-sid 2>/dev/null)
TASK_ID=$(grep -oE '^task_id:[[:space:]]*[^[:space:]]+' status/task-spec.md 2>/dev/null | awk '{print $2}' | head -n 1)
if [ -n "$MY_SID" ]; then
  MSG="任务完成，详见 status/execution-report.md 和 status/arch-self-review.md"
  [ -n "$TASK_ID" ] && MSG="任务 ${TASK_ID}: ${MSG}"
  bash /root/.config/opencode/skills/project-workflow/scripts/notifier-send.sh "$MY_SID" "$MSG" || \
    echo "[$(date '+%Y-%m-%d %H:%M')] final notifier 发送失败，已记录但不声称成功" >> status/history.progress.md
fi
```

---

## Part 4: Prohibited Actions

### ❌ NEVER DO:

1. **Global environment modifications**
   - NO installing to `/root/venv/base`
   - NO global npm packages (for runtime dependencies)
   - Projects MUST use local `.venv` or `node_modules`

2. **Version control violations**
   - NO committing `status/` directory to git
   - NO committing `.venv/` or `node_modules/`
   - NO committing test data or secrets
   - NO committing temporary files

3. **File system violations**
   - NO creating temp files in project root (use `status/tmp/` for temp files)
   - ALWAYS use `status/tmp/` for temporary files
   - Use atomic writes: write to `status/tmp/`, then `mv`

4. **Verification violations**
   - NO claiming "complete" without actual verification
   - NO skipping acceptance criteria checks
   - MUST actually run the code and verify output

5. **Scope violations**
   - NO major architectural changes beyond task spec
   - NO making decisions that require human input
   - Document decision points in execution report

6. **Audit violations**
   - NO git operations without recording in status/
   - Every commit, branch, merge MUST be logged
   - Progress updates MUST include git operations

7. **TODO management violations**
   - NO starting work without creating TODO list first
   - NO skipping TODO list for "simple tasks"
   - MUST break down user requirements into specific TODO items
   - MUST mark items `in_progress` before starting, `completed` immediately after finishing
   - Each TODO must be a concrete, verifiable step

---

## Part 6: Local-Only Git Policy

**This is LOCAL version control:**

### ✅ Allowed:
- Local commits for tracking changes
- Local branches for experiments
- Local history for rollback
- Local merges and rebases

### ❌ Prohibited:
- NO `git push`
- NO `git pull`
- NO `git fetch`
- NO remote repository setup (`git remote add`)
- NO GitHub/GitLab interaction
- NO cloud synchronization

**Why local-only?**
- **Privacy**: Code stays on your machine
- **Simplicity**: No network dependencies
- **Focus**: Version control without deployment concerns
- **Security**: No accidental exposure of sensitive data

---

## Quick Reference

Use this section as an index, not a second copy of the workflow:

| Need | Authoritative Section |
|------|-----------------------|
| Project initialization, `status/`, `.gitignore`, first local commit | Part 1 |
| Development kickoff, milestone TODOs, progress files, OpenClaw reporting | Part 2 |
| Completion verification, architecture self-review, execution report | Part 3 |
| Prohibited actions and stop-the-line requirements | Part 4 |
| Local-only Git boundaries | Part 6 |

TODO lists must be concrete, verifiable, and scoped to the current phase. Do not copy generic templates; derive them from the user's actual task, the project status files, and the relevant section above.

---

## Rules Summary

### 🔴 CRITICAL - Project Structure
1. **Every project = codes/<name>/ + status/ + .git**
2. **status/ NEVER in Git** — must be in `.gitignore`
3. **Read task-spec.md before starting** — it's your source of truth
4. **Update progress regularly** — latest.progress.md + history.progress.md

### 🔴 CRITICAL - Git Auditability
5. **Every git operation MUST be recorded in status/**
6. **Commits, branches, merges → all logged** — for agent communication
7. **status/ is the audit trail** — git operations visible to all agents
8. **Local only** — no remote operations

### 🔴 CRITICAL - external system Communication
### Project Management
9. **Project-local dependencies** — .venv for Python, node_modules for JS
10. **No global environment changes** — isolation is mandatory
11. **Temp files in status/tmp/** — never in project directory
12. **Atomic writes** — always via status/tmp/ temp file, then mv

### Git Practices
13. **Commit frequently** — logical checkpoints
14. **Meaningful messages** — describe what and why
15. **Verify before claiming done** — run it, test it, confirm it

### Communication Protocol
16. **OpenCode writes** — kickoff.md, questions.md, latest.progress.md, history.progress.md, arch-self-review.md, execution-report.md
17. **OpenCode reads** — AGENTS.md, docs/CONTEXT_MANIFEST.md, docs/ARCHITECTURE_CONSTITUTION.md, docs/TECHNICAL_SPEC.md, docs/adr/INDEX.md, task-spec.md, confirmed.items.md
18. **All writes atomic** — via status/tmp/ temp file, then mv

### Architecture Governance
19. **Kickoff before source changes** — no coding before status/kickoff.md says implementation can start
20. **Stop-the-line is mandatory** — confusion level >= 3 or architecture/security ambiguity means write questions.md and stop
21. **Never stop silently** — every stop/pause must be reported to OpenClaw with reason + required next action
22. **Architecture self-review before completion** — arch-self-review.md is required for every implementation task
23. **No decorative architecture** — implemented mechanisms must enter the main path or be reported as risk
24. **Milestone TODOs must bind reporting** — each milestone TODO must explicitly include OpenClaw reporting and status-file updates
25. **End-to-end goals cannot be omitted** — TODO list must enumerate all requested milestones/goals from start to finish

---

## Managed Project Profiles

### Python Projects
Use a project-local `.venv` and maintain `pyproject.toml` with local `uv add` and `uv sync` commands.

### Full-Stack Projects
Keep frontend and backend inside the managed project structure and maintain separate local dependency files where needed.

### All Managed Projects
- **This skill defines the managed contract** — read it when the managed protocol is active
- Apply repository-specific domain and platform rules without weakening this contract
- This skill ensures proper structure and workflow
- All managed projects follow the same status/ communication protocol

---

## Example Workflow Shape

1. Initialize the project structure, local Git repository, `.gitignore`, dependency environment, and `status/` files.
2. Start each implementation phase by reading governance and status files, writing `status/kickoff.md`, creating phase-specific TODOs, and reporting progress through `status/latest.progress.md` and `status/history.progress.md`.
3. Complete work only after verification, `status/arch-self-review.md`, `status/execution-report.md`, local Git history updates, and final status notification.

---

## Summary

This workflow ensures:
- ✅ Proper project structure and isolation
- ✅ Complete version control history
- ✅ Auditable git operations
- ✅ Effective agent communication
- ✅ Reproducible environments
- ✅ Verifiable completion

**Remember: Read this skill first whenever the managed protocol is active.**
