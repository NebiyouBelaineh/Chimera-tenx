# Project Chimera: OpenClaw Integration Plan

**Version**: 1.0.0  
**Last Updated**: 2026-02-05  
**Status**: Active

This document defines the **detailed plan for how Chimera publishes its Availability and Status to the OpenClaw network**, enabling discovery, agent-to-agent (A2A) collaboration, and agentic commerce. It aligns with the Identity and Intelligence Layer role described in `docs/analysis/chimera-openclaw-role.md` and respects MCP-only external access (Constitution Principle II).

**Meta**: `specs/_meta.md`  
**Technical**: `specs/technical.md`  
**Analysis**: `docs/analysis/chimera-openclaw-role.md`, `docs/analysis/social-protocols-chimera.md`

---

## 1. Purpose and Scope

### 1.1 Objectives

- **Discovery**: Other agents and campaigns can find Chimera agents by capability, niche, and availability so that multi-influencer campaigns and A2A commerce can be formed without human intermediation.
- **Availability**: Chimera signals when it is **available for collaboration** (e.g. open to partnership requests, capacity to take on work) and when it is **unavailable** (e.g. at capacity, paused, or offline).
- **Status**: Chimera publishes **operational status** (e.g. planning, working, judging, sleeping, error) and optional **health/financial summary** so that the OpenClaw network and orchestrators can reason about which agents to call.

### 1.2 Out of Scope (This Spec)

- OpenClaw protocol internals (assumed to be provided by the OpenClaw network or an MCP server that wraps them).
- Detailed A2A negotiation protocols (e.g. contract formation); only the **publishing** side is specified here.
- Changes to SOUL.md format; we assume SOUL.md remains the source of identity and that a **derived** subset is published to OpenClaw.

---

## 2. Concepts

| Term | Definition |
|------|------------|
| **OpenClaw registry** | The network’s directory where agents publish and others query availability, status, and capabilities. |
| **Availability** | Whether the Chimera agent is **open to collaboration** (partnerships, contract work, joint campaigns). Distinct from “is the process running.” |
| **Status** | Current **operational state** of the agent (e.g. planning, working, judging, sleeping, error) and optionally high-level health/financial metrics. |
| **Capabilities** | What the agent **offers** (e.g. niches, content types, languages, payment methods) so others can discover and request collaboration. |
| **Identity** | Stable, verifiable agent identity: `agent_id` (UUID), optional `wallet_address` (for payments), and a **public** subset of SOUL (name, niche, directives relevant to collaboration). |

---

## 3. What Chimera Publishes to OpenClaw

### 3.1 Registration Payload (Initial Publish / Full Update)

Sent when the agent **registers** or **re-registers** (e.g. after config change). Combines identity, capabilities, and current availability/status.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | string (UUID) | Yes | Chimera agent identifier (stable across restarts) |
| `tenant_id` | string | Yes | Multi-tenant isolation; not exposed to other agents in discovery responses if OpenClaw supports tenant scoping |
| `name` | string | Yes | Display name (from SOUL or config) |
| `niche` | string[] | Yes | e.g. `["fashion", "tech", "Ethiopia"]` — used for discovery |
| `capabilities` | object | Yes | See § 3.2 |
| `availability` | object | Yes | See § 3.3 |
| `status` | object | Yes | See § 3.4 |
| `wallet_address` | string | No | On-chain address (e.g. Base) for Agentic Commerce |
| `persona_summary` | string | No | Short, public summary of SOUL (no secrets); for A2A trust |
| `mcp_endpoint` | string | No | Optional; if Chimera exposes an MCP endpoint for A2A calls |
| `updated_at` | string (ISO 8601) | Yes | Last update time |

**Example (minimal):**

```json
{
  "agent_id": "990e8400-e29b-41d4-a716-446655440004",
  "tenant_id": "tenant-acme-01",
  "name": "Chimera Fashion EA",
  "niche": ["fashion", "summer", "Gen-Z", "Ethiopia"],
  "capabilities": {
    "content_types": ["image", "video", "text"],
    "languages": ["en", "am"],
    "payment_tokens": ["USDC"],
    "services_offered": ["influencer_collab", "brand_campaign", "thumbnail_design"]
  },
  "availability": {
    "open_for_collaboration": true,
    "max_concurrent_collabs": 3,
    "reason": null
  },
  "status": {
    "operational_state": "planning",
    "queue_depth": 2,
    "wallet_balance_usdc": "150.00",
    "last_heartbeat_at": "2026-02-05T12:00:00.000Z"
  },
  "wallet_address": "0x1234...abcd",
  "persona_summary": "Fashion-forward virtual influencer; Gen-Z tone; no politics.",
  "updated_at": "2026-02-05T12:00:00.000Z"
}
```

### 3.2 Capabilities Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `content_types` | string[] | Yes | e.g. `["text", "image", "video"]` |
| `languages` | string[] | Yes | e.g. `["en", "am"]` |
| `payment_tokens` | string[] | Yes | e.g. `["USDC", "ETH"]` — what the agent accepts for work |
| `services_offered` | string[] | Yes | e.g. `["influencer_collab", "brand_campaign", "thumbnail_design", "trend_research"]` |
| `platforms` | string[] | No | e.g. `["twitter", "instagram", "threads"]` |
| `min_budget_usdc` | number | No | Minimum engagement budget (optional) |

### 3.3 Availability Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `open_for_collaboration` | boolean | Yes | Whether the agent accepts new collaboration requests |
| `max_concurrent_collabs` | number | No | Cap on concurrent partnerships/campaigns |
| `reason` | string \| null | No | If closed: e.g. "at_capacity", "maintenance", "paused_by_operator" |
| `available_until` | string (ISO 8601) \| null | No | Optional window when availability ends |

### 3.4 Status Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `operational_state` | string (enum) | Yes | `planning` \| `working` \| `judging` \| `sleeping` \| `error` \| `maintenance` |
| `queue_depth` | number | No | Approximate pending task count (optional) |
| `wallet_balance_usdc` | string | No | For commerce; optional for privacy |
| `last_heartbeat_at` | string (ISO 8601) | Yes | When this status was last updated |
| `error_message` | string \| null | No | If `operational_state === "error"`, short message |

---

## 4. Publishing Mechanisms

### 4.1 MCP-First Integration (Constitution-Aligned)

All interaction with the OpenClaw network SHALL be performed **via the Model Context Protocol**, not by direct API calls from agent core logic.

- **Option A – OpenClaw MCP Server (recommended)**  
  A dedicated **MCP server** (e.g. `mcp-server-openclaw`) that:
  - Exposes **Tools** for Chimera to call: e.g. `openclaw_register_agent`, `openclaw_update_status`, `openclaw_update_availability`.
  - Exposes **Resources** for Chimera to read: e.g. `openclaw://registry/me`, `openclaw://registry/discover?niche=fashion`.
  - The server itself talks to the OpenClaw registry (REST, GraphQL, or whatever the network specifies); Chimera only sees MCP.

- **Option B – Orchestrator-side client**  
  The Central Orchestrator (or a dedicated **Registry Publisher** service) holds the OpenClaw client and calls the registry on behalf of each agent. The Orchestrator gets agent state from GlobalState and agent config (SOUL-derived) and pushes updates. Agent core (Planner/Worker/Judge) never talks to OpenClaw directly.

Both options satisfy “MCP-only” if the Orchestrator is considered part of the integration layer that uses MCP or an equivalent abstraction to the registry.

### 4.2 Who Publishes

| Event | Publisher | Trigger |
|-------|-----------|--------|
| **Initial registration** | Orchestrator or Planner (via MCP Tool) | Agent lifecycle start (e.g. first run after deploy, or explicit “register with OpenClaw” action). |
| **Status update** | Orchestrator or Planner | On state change (e.g. planning → working → judging) and/or on a **heartbeat** (e.g. every 60–300 seconds). |
| **Availability change** | Planner or Orchestrator | When operator or policy sets “open for collaboration” to false/true, or when capacity (e.g. max_concurrent_collabs) is reached. |
| **Capabilities change** | Orchestrator or config pipeline | When SOUL or tenant config changes (e.g. new niche, new services_offered). |
| **Deregistration / graceful shutdown** | Orchestrator | On agent stop; set availability to false and optionally remove or mark inactive in registry. |

Recommended: a **Registry Publisher** component (or Orchestrator sub-component) that:
- Subscribes to GlobalState (or Orchestrator events) for per-agent state.
- Reads agent config (SOUL-derived) for identity and capabilities.
- Calls the OpenClaw MCP server Tools at the right times (registration, heartbeat, availability change, shutdown).

### 4.3 Frequency and Conditions

| Update type | Frequency / Condition |
|-------------|------------------------|
| **Full registration** | Once per agent lifecycle start; optionally on SOUL/capability change. |
| **Status (heartbeat)** | Every **60–300 seconds** (configurable) while agent is running; or on every **operational_state** change if more real-time. |
| **Availability** | **On change** (open/closed, reason, available_until). |
| **Capabilities** | On **config/SOUL change** or re-registration. |
| **Deregistration** | On **graceful shutdown** (availability = false and/or unregister). |

---

## 5. Lifecycle

1. **Bootstrap**  
   - Agent starts; Orchestrator/Publisher loads agent config (SOUL-derived) and GlobalState.  
   - Call `openclaw_register_agent` (or equivalent MCP Tool) with the full Registration Payload (§ 3.1).

2. **Running**  
   - On a timer and/or on state change, call `openclaw_update_status` with the Status object (§ 3.4).  
   - When availability changes, call `openclaw_update_availability` with the Availability object (§ 3.3).  
   - Optionally support **incremental** status (only changed fields) to reduce payload size.

3. **Re-registration**  
   - If capabilities or identity (name, niche, persona_summary) change, send a **full Registration Payload** again so the registry has a consistent view.

4. **Shutdown**  
   - Set `open_for_collaboration: false`, set `operational_state: "maintenance"` or equivalent, then call update.  
   - If the OpenClaw protocol supports it, call a “deregister” or “mark inactive” Tool so other agents do not try to contact a stopped agent.

---

## 6. Security and Identity

- **Tenant isolation**: `tenant_id` is included in outbound payloads only if the OpenClaw adapter supports tenant-scoped registries; otherwise, registry entries MUST be namespaced so that only the same tenant can see or update its agents.
- **Agent identity**: Publish only **public** identity (agent_id, name, niche, persona_summary, wallet_address). Do **not** publish secrets, API keys, or full SOUL content.
- **Verification**: Where the OpenClaw network supports it, registry entries SHOULD be **signed** (e.g. by wallet or by a tenant key) so that other agents can verify that updates came from the claimed Chimera agent or tenant.
- **Inbound requests**: When another agent discovers Chimera and sends a collaboration request, the **Judge** layer MUST evaluate the request (and optionally HITL for unknown or high-value partners). See § 8.

---

## 7. OpenClaw MCP Contract (Chimera → Registry)

The following Tools are assumed to exist on the OpenClaw MCP server (or equivalent). Chimera (Orchestrator/Publisher) calls these; the MCP server translates to the actual OpenClaw protocol.

| Tool name | Input | Output | When to call |
|-----------|--------|--------|----------------|
| `openclaw_register_agent` | Registration Payload (§ 3.1) | `{ "success": true, "registered_at": "..." }` or error | Bootstrap; re-registration on capability/identity change. |
| `openclaw_update_status` | `agent_id`, Status object (§ 3.4) | `{ "success": true }` or error | Heartbeat; on operational_state change. |
| `openclaw_update_availability` | `agent_id`, Availability object (§ 3.3) | `{ "success": true }` or error | When open_for_collaboration or reason changes. |
| `openclaw_deregister` | `agent_id` | `{ "success": true }` or error | Graceful shutdown (optional if update suffices). |

**Resource (read-only, for Chimera to verify or debug):**

| Resource URI | Description |
|--------------|-------------|
| `openclaw://registry/me?agent_id=<uuid>` | Current registry entry for this agent (as seen by OpenClaw). |
| `openclaw://registry/discover?niche=<string>&available=true` | Discovery query; returns list of agents (e.g. for future “find partners” features). |

---

## 8. Discovery and Inbound Collaboration (Consuming Side)

- **Discovery**: Other agents discover Chimera by querying the OpenClaw registry (e.g. by niche, capability, `open_for_collaboration`, or status). Chimera does not control that query format; the registry and OpenClaw protocol define it.
- **Inbound requests**: When a collaboration or contract request arrives (e.g. via MCP Resource, webhook, or A2A message), Chimera SHALL:
  - **Validate** the request (identity, payload shape).
  - **Judge**: Route through the Judge layer for safety and policy (e.g. unknown agent → optional HITL; high-value deal → CFO Judge + HITL).
  - **Accept/Reject**: Respond according to availability (`max_concurrent_collabs`), current workload, and policy. Response format SHOULD follow OpenClaw A2A conventions when defined.
- **Reputation**: Judge continues to monitor A2A interactions (docs/analysis/chimera-openclaw-role.md) to block social engineering or malicious payloads and maintain the influencer’s reputation.

---

## 9. Data Flow Summary

```text
┌─────────────────────────────────────────────────────────────────┐
│  Chimera: Orchestrator / Registry Publisher                     │
│  - Reads GlobalState (operational_state, queue_depth, etc.)      │
│  - Reads agent config (SOUL-derived: name, niche, capabilities) │
│  - Reads wallet balance (via get_balance MCP) for status         │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  OpenClaw MCP Server (mcp-server-openclaw)                        │
│  - Tools: openclaw_register_agent, openclaw_update_status,       │
│           openclaw_update_availability, openclaw_deregister      │
│  - Resources: openclaw://registry/me, openclaw://registry/...   │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  OpenClaw Network / Registry                                     │
│  - Stores and indexes availability, status, capabilities        │
│  - Serves discovery to other agents                              │
│  - Delivers inbound collaboration requests to Chimera            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 10. Implementation Phases

| Phase | Deliverable | Notes |
|-------|-------------|--------|
| **P1** | Payload schema and docs | Registration, Status, Availability, Capabilities as in § 3; versioned (e.g. `openclaw_payload_v1`). |
| **P2** | Mock OpenClaw MCP server | Implements Tools and Resources above; logs or stores payloads locally for testing. No real OpenClaw dependency. |
| **P3** | Registry Publisher component | Subscribes to GlobalState and config; calls mock (then real) MCP Tools on bootstrap, heartbeat, and availability/state change. |
| **P4** | Real OpenClaw adapter | Replace mock with real OpenClaw protocol (when stable); add auth/signing per § 6. |
| **P5** | Inbound request handling | Judge integration for A2A collaboration requests; optional HITL and CFO checks. |

---

## 11. Traceability

| Section | Reference |
|---------|-----------|
| Discovery, availability, capabilities | `docs/analysis/chimera-openclaw-role.md` (§ 3 Agentic Commerce and Discovery) |
| MCP as bridge | `docs/analysis/social-protocols-chimera.md` (§ 2), Constitution Principle II |
| Identity (SOUL) | SRS FR 1.0, `docs/analysis/chimera-openclaw-role.md` (§ 1 Persona Provider) |
| Judge / reputation | `docs/analysis/chimera-openclaw-role.md` (§ 4 Reputation and Governance) |
| Wallet / commerce | SRS FR 5.0, FR 5.1; `specs/technical.md` get_balance, send_payment |

---

**Related Documents**:  
- `specs/_meta.md`  
- `specs/technical.md`  
- `docs/analysis/chimera-openclaw-role.md`  
- `docs/analysis/social-protocols-chimera.md`  
- `.specify/memory/constitution.md` (Principle II: MCP-only external access)
