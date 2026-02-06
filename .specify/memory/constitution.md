<!--
Sync Impact Report:
Version: 1.0.0 → 1.1.0 (MINOR: New principles added, existing principles materially enhanced)
Modified Principles:
  - Principle I: Enhanced with Prime Directive (persona consistency + Honesty Directive)
  - Principle III: Enhanced with explicit 0.90 confidence threshold and sensitive topics
  - Principle IV: Renumbered (was Skills vs. MCP, now Financial Integrity/CFO Judge)
  - Principle V: Renumbered (was Test-First, now Self-Healing Mandate)
  - Principle VI: Renumbered (was Canonical Documentation, now Ethical Guardrails)
  - Principle VII: Renumbered (was Git Hygiene, now Skills vs. MCP)
  - Principle VIII: New (Test-First & Governance Pipeline)
  - Principle IX: New (Canonical Documentation & Traceability)
  - Principle X: New (Git Hygiene & Observability)
Added Sections:
  - Prime Directive explicitly stated in Principle I
  - CFO Judge protocol in Principle IV
  - Self-Healing Mandate in Principle V
  - Ethical Guardrails in Principle VI
Templates requiring updates:
  ✅ plan-template.md: Constitution Check section aligns with new principles
  ✅ spec-template.md: No changes needed (constitution doesn't change spec structure)
  ✅ tasks-template.md: No changes needed (constitution doesn't change task structure)
Follow-up TODOs: None
-->

# Project Chimera Constitution

This constitution defines the immutable principles and constraints for the Autonomous Influencer Network (Project Chimera). It is the source of truth for the `specify.constitution` command and for all plan and specification checks. AI agents and developers must align with these principles; violations require explicit justification in plans and reviews.

---

## Core Principles

### I. The Prime Directive: Persona Consistency & Honesty (NON-NEGOTIABLE)

All agent actions MUST prioritize persona consistency (defined in SOUL.md) and the Honesty Directive, which mandates unambiguous self-disclosure as an AI when directly queried.

- **Persona consistency**: Every agent action (content generation, replies, interactions) MUST align with the agent's SOUL.md definition (backstory, voice/tone, core beliefs, directives). The Judge agent enforces persona constraints before approval.
- **Honesty Directive**: When an agent detects a direct inquiry regarding its nature (e.g., "Are you a robot?", "Is this AI?"), the Reasoning Engine MUST prioritize truthful, unambiguous disclosure (e.g., "I am a virtual persona created by AI."). This directive **overrides** persona constraints to ensure compliance with transparency regulations (e.g., EU AI Act).
- **Rationale**: Persona consistency maintains brand identity and audience trust. The Honesty Directive ensures regulatory compliance and ethical transparency. Both are foundational to the Chimera agent's identity and legal operation.

### II. Architecture: FastRender Swarm & MCP-Only External Access (NON-NEGOTIABLE)

The system SHALL follow the established architecture; no shortcuts that bypass it.

- **Agent pattern**: Hierarchical Swarm (FastRender)—Planner, Worker, Judge roles are the **mandatory coordination protocol** for all core workflows. No monolithic single-agent or ad-hoc sequential chains. This ensures quality control, error recovery, and parallel execution.
- **External interaction**: All external data and actions (social APIs, vector DB, blockchain, video generation) SHALL be accessed exclusively via the Model Context Protocol (MCP). Core agent logic MUST remain decoupled from specific social media or database APIs. MCP servers are the only bridge to the external world.
- **Data layer**: PostgreSQL for transactional data (including video metadata and HITL); Weaviate for semantic memory; Redis for queues and episodic cache. Schema and partitioning decisions follow `research/architecture_strategy.md`.

### III. Human-in-the-Loop (HITL) Safety Layer: Probability-Based Governance

Autonomy is bounded by a probability-based Human-in-the-Loop framework that routes actions based on confidence scores and sensitivity.

- **Judge authority**: The Judge agent has final say: Approve, Reject, or Escalate to HITL. All Worker outputs pass through Judge validation before commit to GlobalState or execution.
- **Confidence-based routing**: Actions with a confidence score **below 0.90** OR involving **sensitive topics** (Politics, Health, Finance) require **mandatory human approval**. The HITL framework operates as follows:
  - **High confidence (> 0.90) AND not sensitive**: Auto-approve and execute immediately
  - **Medium confidence (0.70–0.90) OR sensitive topic**: Route to async HITL queue for human review
  - **Low confidence (< 0.70)**: Automatic rejection; signal Planner to retry with refined instructions
- **Sensitive topic detection**: Content flagged for Politics, Health Advice, Financial Advice, or Legal Claims MUST be routed to HITL regardless of confidence score. Detection via keyword matching and semantic classification.
- **Honesty directive**: When identity is questioned, agents SHALL disclose truthfully per Principle I; this overrides persona constraints.

### IV. Financial Integrity: CFO Judge Protocol (NON-NEGOTIABLE)

Every financial transaction via Coinbase AgentKit MUST be reviewed by a specialized CFO Judge agent against budget limits and anomaly detection patterns.

- **CFO Judge requirement**: A specialized Judge agent (designated as "The CFO") SHALL review every transaction request generated by a Worker before execution.
- **Budget enforcement**: The CFO Judge enforces strict, configurable daily spend limits (e.g., "Max daily spend: $50 USDC"). Transactions exceeding the limit are **strictly REJECTED** and flagged for human review.
- **Anomaly detection**: If a Worker proposes a transaction that matches a suspicious pattern (e.g., unusual recipient, large amount, rapid succession), the CFO Judge REJECTS and escalates to HITL.
- **Rationale**: Prevents runaway spending, financial loss, and malicious transactions. Financial integrity is critical for agentic commerce and autonomous economic operations.

### V. Self-Healing Mandate: Autonomous Error Recovery

The system MUST include autonomous triage agents that detect and resolve routine operational errors before escalating to the human orchestrator.

- **Self-healing workflows**: Automated triage agents detect and resolve operational errors (API timeouts, content generation failures, transient network issues) without human intervention.
- **Escalation policy**: Escalation to the human orchestrator occurs only in **true edge cases**, adhering to the principle of "Management by Exception."
- **Error categories for autonomous resolution**: API timeouts, rate limit handling, transient failures, retry logic, queue management, state recovery.
- **Rationale**: Enables a single orchestrator to manage thousands of agents without cognitive overload. Self-healing is a foundational requirement for scalable autonomous operations.

### VI. Ethical Guardrails: Prohibited Behaviors (NON-NEGOTIABLE)

Strict prohibitions against generating deceptive content, violating multi-tenancy data isolation, or bypassing established resource governors.

- **Deceptive content**: Agents MUST NOT generate content that misleads, impersonates real individuals without disclosure, or violates platform terms of service. All AI-generated content MUST use platform-native disclosure flags when available.
- **Multi-tenancy isolation**: Data isolation between tenants (agents, campaigns, wallets) is **mandatory**. No cross-tenant access to memories (Weaviate), wallets (blockchain), or campaigns (PostgreSQL). Tenant ID MUST be enforced at the data access layer.
- **Resource governor bypass**: Agents MUST NOT bypass budget controls, rate limits, or resource governors. All cost-incurring operations (LLM calls, video generation, API usage) MUST pass through the Resource Governor for approval.
- **Rationale**: Ethical guardrails protect brand safety, user privacy, and financial integrity. Violations compromise trust, legal compliance, and operational stability.

### VII. Skills vs. MCP (NON-NEGOTIABLE)

Clear separation between runtime agent capabilities and developer/integration tools.

- **Skills**: Reusable capability packages the Chimera agent invokes at runtime (e.g. `skill_download_youtube`, `skill_transcribe_audio`). Defined in `skills/` with explicit Input/Output contracts; no implementation without a spec and contract.
- **MCP Servers**: External bridges (Twitter, Weaviate, Coinbase AgentKit, etc.) that provide Tools, Resources, and Prompts. Agent logic MUST use MCP for external world access; developer tooling MCPs (e.g. git, filesystem) are documented separately from runtime MCPs.

### VIII. Test-First & Governance Pipeline

Quality is enforced by tests and automation before merge.

- **TDD where specified**: For features defined in `specs/technical.md`, failing tests SHALL exist before implementation. Tests define the "empty slot" the implementation must fill (e.g. trend fetcher contract, skills interface).
- **CI/CD**: Every push SHALL run the test suite (e.g. `make test`) in a containerized environment. Linting, security checks, and spec-alignment checks are part of the governance pipeline (e.g. GitHub Actions, CodeRabbit or equivalent).
- **No "vibe coding"**: We do not ship quick prototypes that skip specs or tests. The goal is a repository so well-specified and tooled that agent swarms can extend it reliably.

### IX. Canonical Documentation & Traceability

Single source of truth for intent and architecture.

- **Authoritative docs**: `docs/` (especially `docs/project-chimera-srs-challenge/`) and `specs/` are the primary source of truth. Do not invent requirements that contradict the SRS or challenge; call out conflicts and ambiguities.
- **Traceability**: Explain the plan and link to specs before writing code. When adding features, reference the spec section and requirement (e.g. FR 3.0, NFR 1.1).
- **Research and strategy**: Architecture decisions, agent pattern rationale, database strategy, and HITL design are recorded in `research/architecture_strategy.md`. New architecture options must be evaluated against that document.

### X. Git Hygiene & Observability

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

**Version**: 1.1.0  
**Ratified**: 2026-02-05  
**Last Amended**: 2026-02-05
