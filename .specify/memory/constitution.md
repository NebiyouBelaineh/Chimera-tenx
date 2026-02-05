# Project Chimera Constitution

This constitution defines the immutable principles and constraints for the Autonomous Influencer Network (Project Chimera). It is the source of truth for the `specify.constitution` command and for all plan and specification checks. AI agents and developers must align with these principles; violations require explicit justification in plans and reviews.

---

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

We do not write implementation code until the specification is ratified.

- **Intent before implementation**: Specifications in `specs/` (e.g. `_meta.md`, `functional.md`, `technical.md`) define the "what"; code implements the "how".
- **Executable specs**: API contracts (JSON schemas), database ERDs, and agent interfaces must be defined and linked in specs before implementation.
- **Rationale**: Ambiguity is the enemy of AI. Vague specs lead to agent hallucination and inconsistent behavior. The repository must be architected so a swarm of AI agents can build features from specs with minimal human conflict.

### II. Architecture: FastRender Swarm & MCP-Only External Access

The system SHALL follow the established architecture; no shortcuts that bypass it.

- **Agent pattern**: Hierarchical Swarm (FastRender)—Planner, Worker, Judge roles. No monolithic single-agent or ad-hoc sequential chains for core workflows.
- **External interaction**: All external data and actions (social APIs, vector DB, blockchain, video generation) SHALL be accessed exclusively via the Model Context Protocol (MCP). No direct API calls from agent core logic; MCP servers are the only bridge.
- **Data layer**: PostgreSQL for transactional data (including video metadata and HITL); Weaviate for semantic memory; Redis for queues and episodic cache. Schema and partitioning decisions follow `research/architecture_strategy.md`.

### III. Human-in-the-Loop (HITL) Safety Layer

Autonomy is bounded by a confidence-based safety layer.

- **Judge authority**: The Judge agent has final say: Approve, Reject, or Escalate to HITL. All Worker outputs pass through Judge validation before commit to GlobalState or execution.
- **HITL routing**: Content or actions that are low-confidence (< 0.70), medium-confidence (0.70–0.90), or sensitive-topic-flagged MUST be routed per the HITL flow defined in the architecture (async queue or mandatory review). No auto-approval bypass for sensitive topics or financial transactions above threshold.
- **Honesty directive**: When identity is questioned ("Are you a robot?"), agents SHALL disclose truthfully per the SRS; this overrides persona constraints.

### IV. Skills vs. MCP (NON-NEGOTIABLE)

Clear separation between runtime agent capabilities and developer/integration tools.

- **Skills**: Reusable capability packages the Chimera agent invokes at runtime (e.g. `skill_download_youtube`, `skill_transcribe_audio`). Defined in `skills/` with explicit Input/Output contracts; no implementation without a spec and contract.
- **MCP Servers**: External bridges (Twitter, Weaviate, Coinbase AgentKit, etc.) that provide Tools, Resources, and Prompts. Agent logic MUST use MCP for external world access; developer tooling MCPs (e.g. git, filesystem) are documented separately from runtime MCPs.

### V. Test-First & Governance Pipeline

Quality is enforced by tests and automation before merge.

- **TDD where specified**: For features defined in `specs/technical.md`, failing tests SHALL exist before implementation. Tests define the "empty slot" the implementation must fill (e.g. trend fetcher contract, skills interface).
- **CI/CD**: Every push SHALL run the test suite (e.g. `make test`) in a containerized environment. Linting, security checks, and spec-alignment checks are part of the governance pipeline (e.g. GitHub Actions, CodeRabbit or equivalent).
- **No "vibe coding"**: We do not ship quick prototypes that skip specs or tests. The goal is a repository so well-specified and tooled that agent swarms can extend it reliably.

### VI. Canonical Documentation & Traceability

Single source of truth for intent and architecture.

- **Authoritative docs**: `docs/` (especially `docs/project-chimera-srs-challenge/`) and `specs/` are the primary source of truth. Do not invent requirements that contradict the SRS or challenge; call out conflicts and ambiguities.
- **Traceability**: Explain the plan and link to specs before writing code. When adding features, reference the spec section and requirement (e.g. FR 3.0, NFR 1.1).
- **Research and strategy**: Architecture decisions, agent pattern rationale, database strategy, and HITL design are recorded in `research/architecture_strategy.md`. New architecture options must be evaluated against that document.

### VII. Git Hygiene & Observability

The repository and tooling support collaboration and audit.

- **Commits**: Commit early and often (minimum 2x/day when active). Commit history should tell a story of evolving complexity; meaningful messages required.
- **MCP Sense**: When required by the program, keep the Tenx MCP Sense server connected to the IDE as the "flight recorder" for traceability and assessment.

---

## Additional Constraints

- **Regulatory & ethics**: Design for AI transparency (e.g. EU AI Act). Use platform-native AI disclosure where available; persona and Honesty Directive must be enforceable.
- **Cost & budget**: Budget controls (Resource Governor, CFO Judge) and tiered video generation (Tier 1 / Tier 2) are part of the design; do not introduce unbounded spend paths.
- **Multi-tenancy**: Data isolation between tenants (agents, campaigns) is mandatory; no cross-tenant access to memories or wallets.

---

## Development Workflow

1. **Plan**: Create or update a plan (e.g. via Specify) that references this constitution and the relevant specs.
2. **Constitution check**: Plans and PRs must pass a constitution check; any deviation must be justified and documented.
3. **Spec → Test → Code**: Ratify or update spec → add or update failing tests → implement → ensure tests pass and CI is green.
4. **Review**: Code review must verify spec alignment, constitution compliance, and security (e.g. no secrets in code, MCP-only external access).

---

## Governance

- This constitution **supersedes** ad-hoc practices and one-off decisions. When in doubt, the SRS and `research/architecture_strategy.md` clarify intent; this document defines **how** we work.
- **Amendments**: Changes to the constitution require documentation (rationale, impact), approval (e.g. lead architect / maintainer), and a short migration note if existing plans or code are affected.
- **Compliance**: All PRs and plan gates must verify alignment with these principles. Tools (e.g. `spec-check`, CodeRabbit config) should enforce spec alignment and constitution-related checks where feasible.

---

**Version**: 1.0.0  
**Ratified**: 2026-02-05  
**Last Amended**: 2026-02-05
