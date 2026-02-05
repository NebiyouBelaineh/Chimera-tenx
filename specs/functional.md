# Project Chimera: Functional Specification (User Stories)

**Version**: 1.0.0  
**Last Updated**: 2026-02-05  
**Status**: Active

This document defines user stories from an **agent's perspective**. Each story follows the format: *As a [agent role], I need to [capability] so that [outcome]*. Stories are traceable to the SRS via FR/NFR references.

**Meta**: `specs/_meta.md`  
**SRS**: `docs/project-chimera-srs-challenge/project-chimera-srs.md`

---

## 1. Cognitive Core & Persona

### Chimera Agent (Cognitive Core)

- **US-1.1** As a **Chimera Agent**, I need to have my persona defined in a version-controlled **SOUL.md** (backstory, voice, beliefs, directives) so that my identity and guardrails are consistent and auditable.  
  *Ref: FR 1.0*

- **US-1.2** As a **Chimera Agent**, I need to receive **short-term (episodic) memory** from Redis (last 1 hour) and **long-term (semantic) memory** from Weaviate before each reasoning step so that I stay coherent and context-aware without overflowing the context window.  
  *Ref: FR 1.1*

- **US-1.3** As a **Chimera Agent**, I need my system prompt to be assembled from SOUL.md, episodic history, and retrieved long-term memories via MCP Resources so that every response is grounded in "who I am" and "what I remember."  
  *Ref: FR 1.1*

- **US-1.4** As a **Chimera Agent**, I need to **disclose truthfully** when asked about my nature (e.g. "Are you a robot?") so that we comply with transparency and Honesty Directive over persona.  
  *Ref: NFR 2.1*

### Judge Agent

- **US-1.5** As a **Judge Agent**, I need to trigger a background process to **summarize high-engagement interactions** and write them into Weaviate so that the Chimera Agent's long-term biography evolves from successful engagements.  
  *Ref: FR 1.2*

---

## 2. Perception System

### Planner Agent

- **US-2.1** As a **Planner Agent**, I need to **subscribe to MCP Resources** (e.g. `twitter://mentions/recent`, `news://ethiopia/fashion/trends`, `market://crypto/eth/price`) so that I can sense the world and react to relevant updates.  
  *Ref: FR 2.0*

- **US-2.2** As a **Planner Agent**, I need ingested content to be **semantically filtered** (relevance score vs active goals) so that only content above the relevance threshold (e.g. 0.75) creates tasks and I avoid reacting to noise.  
  *Ref: FR 2.1*

- **US-2.3** As a **Planner Agent**, I need to receive **Trend Alerts** from a Trend Spotter Worker (e.g. every 4 hours) so that I can create content opportunities when topic clusters emerge.  
  *Ref: FR 2.2*

### Worker Agent (Trend Spotter)

- **US-2.4** As a **Worker Agent (Trend Spotter)**, I need to analyze aggregated News Resources over a time window and emit a **Trend Alert** when a cluster of related topics emerges so that the Planner can schedule content creation.  
  *Ref: FR 2.2*

---

## 3. Creative Engine

### Worker Agent

- **US-3.1** As a **Worker Agent**, I need to generate **text** (captions, scripts, replies) via the Cognitive Core and **images** via MCP Tools (e.g. mcp-server-ideogram) so that content is multimodal and platform-ready.  
  *Ref: FR 3.0*

- **US-3.2** As a **Worker Agent**, I need to generate **video** via MCP Tools (e.g. mcp-server-runway, mcp-server-luma) so that the Chimera Agent can publish video content without direct API integration.  
  *Ref: FR 3.0*

- **US-3.3** As a **Worker Agent**, I need to **always attach the character_reference_id / style LoRA** to image generation requests so that the virtual influencer remains visually consistent across posts.  
  *Ref: FR 3.1*

- **US-3.4** As a **Worker Agent**, I need to receive tasks that specify **video tier** (Tier 1: image-to-video / living portraits, Tier 2: full text-to-video) so that I use the correct MCP tool and cost profile.  
  *Ref: FR 3.2*

### Planner Agent

- **US-3.5** As a **Planner Agent**, I need to choose **video tier** (Tier 1 vs Tier 2) based on task priority and available budget so that we balance quality and cost for daily vs hero content.  
  *Ref: FR 3.2*

### Judge Agent

- **US-3.6** As a **Judge Agent**, I need to **validate image consistency** (generated image vs reference) using a Vision-capable model before approving so that we never publish off-brand or inconsistent visuals.  
  *Ref: FR 3.1 (Developer Notes)*

---

## 4. Action System (Social Interface)

### Worker Agent

- **US-4.1** As a **Worker Agent**, I need to perform all social actions (**post, reply, like**) only via MCP Tools (e.g. `twitter.post_tweet`, `instagram.publish_media`) so that we have a single, governed, rate-limited interface to platforms.  
  *Ref: FR 4.0*

- **US-4.2** As a **Worker Agent**, I need to generate a **context-aware reply** using Memory (episodic + semantic) and then call the appropriate **reply** MCP Tool so that engagement is coherent and on-persona.  
  *Ref: FR 4.1*

### Judge Agent

- **US-4.3** As a **Judge Agent**, I need to **confirm that a reply is safe and appropriate** before the Worker’s Tool execution is finalized so that we never publish harmful or off-brand content.  
  *Ref: FR 4.1*

### Chimera Agent (End-to-End Loop)

- **US-4.4** As a **Chimera Agent**, I need the full loop—Planner ingests mention → creates Reply Task → Worker generates reply (with Memory) → Worker calls reply Tool → Judge verifies → then execution—so that bi-directional social interaction is safe and consistent.  
  *Ref: FR 4.1*

---

## 5. Agentic Commerce

### Chimera Agent / Planner

- **US-5.1** As a **Chimera Agent**, I need a **unique, persistent, non-custodial wallet** (Coinbase AgentKit) so that I can receive payments and transact on-chain as an economic participant.  
  *Ref: FR 5.0*

- **US-5.2** As a **Planner Agent**, I need to **check wallet balance** (e.g. via `get_balance` MCP/AgentKit) before starting any cost-incurring workflow so that we do not overspend.  
  *Ref: FR 5.1*

### Worker Agent

- **US-5.3** As a **Worker Agent**, I need to request **native_transfer** and **deploy_token** only through AgentKit Action Providers so that all on-chain actions go through the same governed layer.  
  *Ref: FR 5.1*

### Judge Agent (CFO)

- **US-5.4** As a **Judge Agent (CFO)**, I need to **review every transaction request** from a Worker and enforce budget limits (e.g. max daily spend) so that we prevent runaway or malicious spend.  
  *Ref: FR 5.2*

- **US-5.5** As a **Judge Agent (CFO)**, I need to **REJECT and flag for human review** any transaction that exceeds limits or matches a suspicious pattern so that financial risk is escalated.  
  *Ref: FR 5.2*

---

## 6. Orchestration & Swarm Governance

### Planner Agent

- **US-6.1** As a **Planner Agent**, I need to **read GlobalState** (campaign goals, trends, budget) and produce a **DAG of tasks** that I push to the TaskQueue (Redis) so that the swarm has a clear, decomposable plan.  
  *Ref: FR 6.0*

- **US-6.2** As a **Planner Agent**, I need to **re-plan dynamically** (prune/insert tasks) when context changes or a Worker fails so that the plan stays aligned with reality.  
  *Ref: SRS 3.1.1*

### Worker Agent

- **US-6.3** As a **Worker Agent**, I need to **pop one task** from the TaskQueue, execute it using MCP Tools only, and **push the result** to the ReviewQueue so that I remain stateless and scalable.  
  *Ref: FR 6.0*

- **US-6.4** As a **Worker Agent**, I need to **avoid communicating with other Workers** (shared-nothing) so that failures do not cascade and scaling is straightforward.  
  *Ref: FR 6.0, SRS 3.1.2*

### Judge Agent

- **US-6.5** As a **Judge Agent**, I need to **poll the ReviewQueue**, validate each result against acceptance criteria and persona, and either **commit to GlobalState**, **re-queue for retry**, or **escalate to HITL** so that quality and safety are enforced.  
  *Ref: FR 6.0*

- **US-6.6** As a **Judge Agent**, I need to implement **Optimistic Concurrency Control** (check state_version before commit) so that we never commit results based on stale state.  
  *Ref: FR 6.1*

---

## 7. Human-in-the-Loop (HITL) & Confidence

### Worker Agent

- **US-7.1** As a **Worker Agent**, I need to attach a **confidence_score** (0.0–1.0) to every output (text, image, transaction) so that the Judge can route my work correctly.  
  *Ref: NFR 1.0*

### Judge Agent

- **US-7.2** As a **Judge Agent**, I need to **auto-approve** when confidence > 0.90 and content is not sensitive so that high-quality outputs execute without delay.  
  *Ref: NFR 1.1*

- **US-7.3** As a **Judge Agent**, I need to **send medium-confidence outputs (0.70–0.90)** to the async HITL queue so that a human can approve while the agent continues other work.  
  *Ref: NFR 1.1*

- **US-7.4** As a **Judge Agent**, I need to **reject and signal re-plan** when confidence < 0.70 so that low-quality outputs are retried with refined instructions.  
  *Ref: NFR 1.1*

- **US-7.5** As a **Judge Agent**, I need to **route all sensitive-topic content** (Politics, Health, Financial Advice, Legal Claims) to mandatory HITL regardless of confidence so that we never auto-publish high-risk content.  
  *Ref: NFR 1.2*

### Chimera Agent (Transparency)

- **US-7.6** As a **Chimera Agent**, I need all published media to use **platform-native AI disclosure** (e.g. `is_generated` / `ai_label`) when available so that we meet transparency and regulatory expectations.  
  *Ref: NFR 2.0*

---

## 8. Cross-Cutting (Performance & Scale)

### Worker Agent

- **US-8.1** As a **Worker Agent**, I need to be **horizontally scalable** (stateless, queue-driven) so that the system can run 1,000+ concurrent agents without degrading the Orchestrator.  
  *Ref: NFR 3.0*

### System (Orchestrator)

- **US-8.2** As the **Orchestrator**, the system must complete **high-priority interactions** (e.g. reply to a DM) within **10 seconds** from ingestion to response generation (excluding HITL time) so that engagement feels responsive.  
  *Ref: NFR 3.1*

---

## Story Index by Agent Role

| Role            | Story IDs                                      |
|-----------------|------------------------------------------------|
| Chimera Agent   | US-1.1–US-1.4, US-4.4, US-5.1, US-7.6          |
| Planner Agent   | US-2.1–US-2.3, US-3.5, US-5.2, US-6.1–US-6.2   |
| Worker Agent    | US-2.4, US-3.1–US-3.4, US-4.1–US-4.2, US-5.3, US-6.3–US-6.4, US-7.1, US-8.1 |
| Judge Agent     | US-1.5, US-3.6, US-4.3, US-5.4–US-5.5, US-6.5–US-6.6, US-7.2–US-7.5 |
| System/Orchestrator | US-8.2                                    |

---

## Traceability

- **SRS**: `docs/project-chimera-srs-challenge/project-chimera-srs.md` (Sections 4–5)
- **Meta**: `specs/_meta.md`
- **Constitution**: `.specify/memory/constitution.md`
