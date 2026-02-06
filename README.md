# Project Chimera

**Autonomous Influencer Network** — A spec-driven repository for building AI agents that research trends, generate content, and manage engagement. The repository is designed so that intent lives in specifications and infrastructure (CI/CD, tests, Docker, linting) enforces reliability.

---

## What This Repository Is

Project Chimera is the **“Factory”** for **Autonomous Influencers**: digital entities with perception (MCP Resources), reasoning (FastRender Swarm: Planner / Worker / Judge), creative output (text, image, video), and economic agency (Coinbase AgentKit). The layout and tooling are intended to allow humans or AI agents to implement features against a single source of truth (`specs/`) with automated checks on every change.

**Core principles:**

- **Spec-Driven Development (SDD):** Implementation follows ratified specs in `specs/`; code is traceable to API contracts and schemas defined there.
- **MCP-only external access:** All external data and actions go through Model Context Protocol servers; the agent core does not call third-party APIs directly.
- **FastRender Swarm:** Core workflows use a Planner → Worker → Judge architecture.
- **Governance:** Linting (PEP 8), tests, and an AI review policy (CodeRabbit) run in CI on every push.

---

## Requirements and Constraints That Shaped This Repository

The structure and tooling reflect the following requirements and constraints used when building the repository:

- **Spec-first:** No implementation without a ratified specification; specs must include API contracts, data schemas, and agent interfaces where relevant.
- **Executable specs:** API inputs/outputs and database schema are defined in a way that supports contract tests and validation.
- **Separation of developer tooling vs runtime:** Developer MCPs (e.g. Git, filesystem, GitHub) are documented separately from runtime agent skills; skills define input/output contracts and depend on MCP servers for external capabilities.
- **TDD and “empty slots”:** Tests were written to assert data structures and interfaces from the technical spec before implementation, defining the contracts the implementation must satisfy.
- **Governance pipeline:** Linting, security-related checks, and testing run automatically (e.g. in CI and optionally in Docker), so every push is validated.
- **AI review policy:** Code review configuration (e.g. CodeRabbit) instructs reviewers to check for spec alignment and security vulnerabilities, in addition to standard tooling (linters, secret scanners).

These are reflected in the presence of `specs/`, contract tests in `tests/`, the Makefile and CI workflow, and `.coderabbit.yaml`.

---

## What’s in This Repository

### Specifications (`specs/`)

The single source of truth for vision, behavior, and technical contracts:

| Document | Purpose |
|----------|---------|
| `_meta.md` | Vision, constraints, FastRender + MCP patterns, hybrid data (PostgreSQL, Weaviate, Redis). |
| `functional.md` | User stories from the agent’s perspective (Cognitive Core, Perception, Creative Engine, Action, Agentic Commerce, HITL). |
| `technical.md` | API contracts (Agent Task, Worker Result, MCP tools), database schema/ERD, Trend Alert, HITL. |
| `openclaw_integration.md` | How Chimera publishes availability, status, and capabilities to the OpenClaw network. |
| `001-autonomous-influencer-agents/` | Focused spec and checklists for autonomous influencer agents. |

### Agent Skills (`skills/`)

`skills/README.md` defines **input/output contracts** for 20+ runtime skills (perception, memory, content generation, social actions, agentic commerce, validation). Skills are distinct from MCP servers: they are internal capability packages that orchestrate MCP tools; contracts are traceable to the SRS and technical spec.

### Research and Documentation (`research/`, `docs/`)

- **`research/tooling_strategy.md`** — Selection and configuration of MCP servers used for development (e.g. GitHub, Filesystem, Git, SQLite).
- **`docs/analysis/`** — Chimera’s role in the Agent Social Network (OpenClaw), social protocols for agent-to-agent interaction.
- **`docs/insights/`** — Architecture notes and agent infrastructure pattern; diagrams in `docs/images/`.
- **`docs/project-chimera-srs-challenge/`** — Full Software Requirements Specification (SRS) and challenge context for readers who want the full product and process background.

### IDE and Agent Context (`.cursor/`)

- **`.cursor/rules/`** — Rules for IDE and AI assistants: project context, **Prime Directive** (no code generation without consulting `specs/`), traceability, MCP/TDD/safety. Ensures contributors and agents check specs before implementing.
- **`.cursor/commands/`** — Spec Kit–style commands for specification workflow.
- **`.cursor/mcp.json`** — MCP server configuration (developer and telemetry-related servers).

### Tests (`tests/`)

Contract tests that assert behavior and data shapes from the technical spec:

- **`test_trend_fetcher.py`** — Trend Alert and trend data structure vs API contract in `specs/technical.md`.
- **`test_skills_interface.py`** — Skill interfaces (e.g. `skill_monitor_resources`, `skill_detect_trends`) accept the specified parameters and return the specified contract.

Tests are run in Docker via `make test` and are part of CI.

### Infrastructure

- **`Dockerfile`** — Python 3.13 and uv; default command runs the test suite.
- **`Makefile`** — `setup`, `test`, `lint`, `spec-check`, `clean`.
- **`.github/workflows/main.yml`** — On every push/PR: lint job (`make lint`) and test job (`make test`).
- **`.coderabbit.yaml`** — CodeRabbit configuration: path-based instructions for **spec alignment** (against `specs/`) and **security**; tools such as Gitleaks, Semgrep, and Ruff enabled.
- **`pyproject.toml`** — Project config and Ruff (PEP 8) lint/format configuration.

---

## Repository Structure

```
├── .cursor/           # IDE rules and MCP config
│   ├── rules/         # chimera-core, research-architecture, python_uv_dockerfile, agent
│   ├── commands/      # Spec Kit commands
│   └── mcp.json       # MCP server configuration
├── .github/
│   └── workflows/
│       └── main.yml   # CI: lint + test on push/PR
├── docs/              # Analysis, report, images, insights
│   ├── analysis/      # OpenClaw role, social protocols
│   ├── insights/      # Architecture and insights
│   ├── project-chimera-srs-challenge/  # SRS and context
│   └── Project-Chimera-Report.md
├── research/
│   └── tooling_strategy.md   # Developer MCP servers
├── specs/             # Single source of truth (SDD)
│   ├── _meta.md       # Vision, constraints, patterns
│   ├── functional.md  # User stories (agent perspective)
│   ├── technical.md   # API contracts, schema, ERD
│   ├── openclaw_integration.md
│   └── 001-autonomous-influencer-agents/
├── skills/
│   └── README.md      # Skill I/O contracts (20+ skills)
├── tests/             # Contract tests
│   ├── test_trend_fetcher.py
│   └── test_skills_interface.py
├── .coderabbit.yaml   # AI review: spec alignment + security
├── Dockerfile         # Python 3.13 + uv, run tests
├── Makefile           # setup, test, lint, spec-check, clean
├── pyproject.toml     # Project and Ruff config
└── README.md          # This file
```

---

## Getting Started

**Prerequisites:** Python 3.13+, [uv](https://docs.astral.sh/uv/), Docker (for `make test`).

```bash
git clone <repo-url>
cd Chimera-tenx
make setup      # Install dependencies (uv sync)
make test       # Run tests in Docker
make lint       # Run Ruff (PEP 8 check + format check)
make spec-check # Verify spec files and run contract tests in Docker
```

Before changing code, read the relevant specs in `specs/` (_meta, functional, technical). The `.cursor/rules` encode a **Prime Directive**: check specs first and keep implementation traceable to them.

---

## Key References

- **Specs:** [specs/](specs/) — _meta, functional, technical, openclaw_integration
- **Skills (contracts):** [skills/README.md](skills/README.md)
- **SRS and context:** [docs/project-chimera-srs-challenge/](docs/project-chimera-srs-challenge/)
- **Research and tooling:** [research/tooling_strategy.md](research/tooling_strategy.md), [docs/analysis/](docs/analysis/), [docs/insights/](docs/insights/)
- **IDE rules:** [.cursor/rules/](.cursor/rules/) — chimera-core (Prime Directive), research-architecture, python_uv_dockerfile
