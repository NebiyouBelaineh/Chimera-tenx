# Project Chimera: Specification Meta

**Version**: 1.0.0  
**Last Updated**: 2026-02-05  
**Status**: Active

---

## High-Level Vision

Project Chimera is an **Autonomous Influencer Network**—a scalable platform for creating, deploying, and managing persistent AI agents that operate as digital influencers. These agents are not static scripts but goal-directed digital entities capable of:

- **Perception**: Monitoring trends, social signals, and market conditions via MCP Resources
- **Reasoning**: Strategic planning and decision-making through hierarchical swarm architecture
- **Creative Expression**: Generating multimodal content (text, images, video) aligned with persona
- **Economic Agency**: Autonomous financial transactions via non-custodial crypto wallets
- **Social Engagement**: Bi-directional interaction with audiences across multiple platforms

### Strategic Objectives

1. **Scalability**: Support 1,000+ concurrent autonomous agents managed by a single orchestrator
2. **Autonomy**: Agents operate with significant independence, escalating to humans only for edge cases
3. **Reliability**: Self-healing workflows that detect and recover from failures automatically
4. **Economic Independence**: Agents manage their own P&L, transact on-chain, and operate as self-sustaining entities
5. **Brand Safety**: Confidence-based Human-in-the-Loop (HITL) ensures quality and compliance

### Business Models

The platform enables three distinct business models:

- **Digital Talent Agency**: AiQEM owns and operates proprietary AI influencer fleets
- **Platform-as-a-Service (PaaS)**: External brands license Chimera OS to run custom agents
- **Hybrid Ecosystem**: Flagship fleet demonstrates capabilities while enabling third-party developers

---

## Architectural Foundation

### Core Patterns

1. **FastRender Swarm Architecture**: Hierarchical role-based swarm (Planner → Worker → Judge)
   - Planner: Decomposes goals into task DAGs, monitors GlobalState, handles dynamic re-planning
   - Worker: Stateless, parallel execution of atomic tasks via MCP Tools
   - Judge: Quality assurance, confidence scoring, HITL routing, OCC state management

2. **Model Context Protocol (MCP)**: Universal interface for all external interactions
   - Resources: Passive data sources (news feeds, social mentions, market data)
   - Tools: Executable functions (generate content, post to social, execute transactions)
   - Prompts: Reusable templates for standardized reasoning

3. **Hybrid Data Architecture**:
   - PostgreSQL: Transactional data (video metadata, HITL reviews, campaigns, financial logs)
   - Weaviate: Semantic memory (agent memories, persona definitions, RAG pipeline)
   - Redis: Episodic cache (last 1 hour), task queues, rate limiting

### System Topology

- **Hub-and-Spoke**: Central Orchestrator (hub) manages Agent Swarms (spokes)
- **Multi-Tenancy**: Strict data isolation between tenants (agents, campaigns, wallets)
- **Cloud-Native**: Kubernetes-orchestrated, auto-scaling, distributed services

---

## Project Constraints

### Non-Negotiable Constraints

1. **Spec-Driven Development**: No implementation code without ratified specification
   - All features must be defined in `specs/` (functional, technical) before coding
   - API contracts, database schemas, and agent interfaces must be executable specs
   - Reference: `.specify/memory/constitution.md` Principle I

2. **MCP-Only External Access**: No direct API calls from agent core logic
   - All external data/actions via MCP Servers (Twitter, Instagram, Weaviate, Coinbase, Video APIs)
   - Agent logic decoupled from third-party API implementations
   - Reference: `.specify/memory/constitution.md` Principle II

3. **FastRender Swarm Pattern**: Core workflows use Planner-Worker-Judge architecture
   - No monolithic single-agent or ad-hoc sequential chains for core workflows
   - Workers are stateless, parallel, shared-nothing
   - Judge has absolute authority: Approve, Reject, Escalate
   - Reference: `docs/project-chimera-srs-challenge/project-chimera-srs.md` Section 3.1

4. **Skills vs. MCP Separation**: Clear distinction between runtime capabilities and integration tools
   - Skills: Runtime agent capabilities (defined in `skills/` with I/O contracts)
   - MCP Servers: External bridges (documented separately from runtime MCPs)
   - Reference: `.specify/memory/constitution.md` Principle IV

### Operational Constraints

5. **Regulatory Compliance**: AI transparency and disclosure requirements
   - EU AI Act compliance: Agents capable of self-disclosure
   - Platform-native AI labeling (Twitter/Instagram `is_generated` flags)
   - Honesty Directive: Truthful disclosure when identity is questioned
   - Reference: `docs/project-chimera-srs-challenge/project-chimera-srs.md` Section 2.4, 5.2

6. **Cost Management**: Budget controls prevent runaway spending
   - Resource Governor: Budget limits enforced at Orchestrator level
   - CFO Judge: Reviews all financial transactions, enforces daily limits
   - Tiered video generation: Tier 1 (cost-effective) vs Tier 2 (hero content)
   - Reference: `docs/project-chimera-srs-challenge/project-chimera-srs.md` Section 2.4, 4.2

7. **HITL Safety Layer**: Confidence-based routing for autonomous actions
   - High confidence (> 0.90): Auto-approve (unless sensitive topic)
   - Medium confidence (0.70-0.90): Async approval queue
   - Low confidence (< 0.70): Reject and re-plan
   - Sensitive topics: Mandatory HITL review (Politics, Health, Financial Advice, Legal Claims)
   - Reference: `research/architecture_strategy.md` Section 2

8. **Scalability Targets**: System must support enterprise-scale operations
   - Agent fleet: 1,000+ concurrent agents
   - Video generation: 10,000+ videos per day
   - Database writes: 10,000+ inserts per minute (peak)
   - Reference: `research/architecture_strategy.md` Appendix B

9. **Data Isolation**: Multi-tenancy requires strict boundaries
   - No cross-tenant access to memories (Weaviate), wallets (blockchain), or campaigns (PostgreSQL)
   - Tenant ID enforced at data access layer
   - Reference: `docs/project-chimera-srs-challenge/project-chimera-srs.md` Section 2.1

10. **Platform Volatility**: Social media APIs change frequently
    - MCP Server layer absorbs API changes; agent logic remains stable
    - No hard-coded API endpoints in agent core
    - Reference: `docs/project-chimera-srs-challenge/project-chimera-srs.md` Section 2.4

### Technical Constraints

11. **Technology Stack** (as per architecture decisions):
    - Agent Runtime: Python 3.11+ (async/await, MCP SDK support)
    - Database: PostgreSQL 15+ (ACID, JSONB, partitioning)
    - Vector DB: Weaviate (semantic search, RAG)
    - Cache/Queue: Redis 7+ (episodic memory, task queues)
    - Orchestration: Kubernetes (container orchestration, auto-scaling)
    - LLM APIs: Gemini 3 Pro/Flash, Claude Opus (reasoning vs throughput)
    - Reference: `research/architecture_strategy.md` Appendix A

12. **Test-First Development**: TDD where specified
    - Failing tests define "empty slots" before implementation
    - CI/CD runs test suite on every push
    - Reference: `.specify/memory/constitution.md` Principle V

---

## Canonical Documentation

### Primary Sources of Truth

1. **SRS**: `docs/project-chimera-srs-challenge/project-chimera-srs.md`
   - Functional requirements (FR), Non-functional requirements (NFR)
   - System architecture, interface requirements
   - **Do not invent requirements that contradict the SRS**

2. **Architecture Strategy**: `research/architecture_strategy.md`
   - Agent pattern rationale (Hierarchical Swarm vs Sequential Chain)
   - Database strategy (PostgreSQL vs NoSQL)
   - HITL architecture and confidence routing
   - **New architecture options must be evaluated against this document**

3. **Constitution**: `.specify/memory/constitution.md`
   - Core principles and development workflow
   - **Supersedes ad-hoc practices; all PRs must comply**

4. **Challenge Document**: `docs/project-chimera-srs-challenge/project-chimera-challenge.md`
   - 3-day roadmap, submission requirements
   - Assessment rubric (Velocity vs Distance)

### Specification Structure

- `specs/_meta.md` (this file): High-level vision and constraints
- `specs/functional.md`: User stories, functional requirements (FR references)
- `specs/technical.md`: API contracts, database schemas, agent interfaces
- `specs/openclaw_integration.md`: OpenClaw network integration (optional)

---

## Success Criteria

### Phase 1: Core Swarm Infrastructure
- Planner-Worker-Judge services operational
- Redis task queues functional
- Basic PostgreSQL schema deployed
- MCP client integration working

### Phase 2: HITL Layer
- HITL review queue implemented
- Review dashboard UI functional
- Confidence scoring logic operational
- Sensitive topic classification working

### Phase 3: Database Optimization
- PostgreSQL partitioning active
- Read replicas configured
- Connection pooling (PgBouncer) operational
- Batch insert optimizations deployed

### Phase 4: Video Metadata Pipeline
- Video generation MCP server deployed
- Metadata schema implemented
- High-velocity write path optimized
- Analytics queries functional

### Ultimate Goal

A repository so well-architected, specified, and tooled that **a swarm of AI agents can enter the codebase and build the final features with minimal human conflict**.

---

## Governance

- **Specification Authority**: This meta spec, along with `specs/functional.md` and `specs/technical.md`, defines the "what" before implementation
- **Constitution Compliance**: All implementations must align with `.specify/memory/constitution.md`
- **Traceability**: Features must reference SRS requirements (e.g. FR 3.0, NFR 1.1) and architecture decisions
- **Amendments**: Changes to this meta spec require documentation of rationale and impact assessment

---

**Related Documents**:
- Constitution: `.specify/memory/constitution.md`
- SRS: `docs/project-chimera-srs-challenge/project-chimera-srs.md`
- Architecture: `research/architecture_strategy.md`
- Challenge: `docs/project-chimera-srs-challenge/project-chimera-challenge.md`
