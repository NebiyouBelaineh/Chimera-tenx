# Project Chimera: Agent Skills Directory

**Version**: 1.0.0  
**Last Updated**: 2026-02-06  
**Status**: Active

This directory defines the **runtime Skills** that Chimera Agents use to perform their autonomous operations. Skills are reusable capability packages that Workers invoke during task execution. They differ from MCP Servers (which are external bridges) in that Skills are internal, composable functions that orchestrate MCP Tools and business logic.

**Meta**: `specs/_meta.md`  
**Technical**: `specs/technical.md`  
**Functional**: `specs/functional.md`  
**SRS**: `docs/project-chimera-srs-challenge/project-chimera-srs.md`

---

## Skills vs. MCP Tools

**Skills** are internal, reusable capability packages that:
- Encapsulate business logic and orchestration
- Compose multiple MCP Tools
- Handle error recovery and retries
- Enforce validation and governance rules
- Are invoked by Workers during task execution

**MCP Tools** are external, standardized interfaces that:
- Bridge to external services (Twitter, Weaviate, Coinbase AgentKit)
- Provide Resources (data sources) and Tools (executable functions)
- Are discovered and invoked through the MCP protocol
- Are defined in MCP Servers (external processes)

**Example**: `skill_generate_content` (Skill) orchestrates `generate_image` and `generate_text` (MCP Tools) to create multimodal content.

---

## Skill Categories

Skills are organized into functional categories:

1. **Perception & Data Ingestion** - Monitoring and filtering external data
2. **Memory & Persona Management** - Retrieving and assembling agent context
3. **Content Generation** - Creating multimodal content (text, image, video)
4. **Social Media Actions** - Publishing and engaging on platforms
5. **Agentic Commerce** - Financial transactions and wallet management
6. **Validation & Governance** - Quality assurance and safety checks

---

## 1. Perception & Data Ingestion Skills

### 1.1 `skill_monitor_resources`

**Purpose**: Continuously poll MCP Resources for updates and detect relevant changes.

**Invoked By**: Planner Agent (background polling loop)

**Input Contract**:

```json
{
  "agent_id": "string (UUID)",
  "resource_uris": [
    "string (MCP Resource URI)"
  ],
  "poll_interval_seconds": "number (default: 60)",
  "last_poll_timestamp": "string (ISO 8601, optional)"
}
```

**Output Contract**:

```json
{
  "success": "boolean",
  "updates": [
    {
      "resource_uri": "string",
      "content": "object (resource-specific)",
      "timestamp": "string (ISO 8601)",
      "change_detected": "boolean"
    }
  ],
  "poll_timestamp": "string (ISO 8601)",
  "error": "string (if success === false)"
}
```

**MCP Dependencies**: 
- `mcp-server-twitter` (Resource: `twitter://mentions/recent`)
- `mcp-server-news` (Resource: `news://ethiopia/fashion/trends`)
- `mcp-server-market` (Resource: `market://crypto/eth/price`)

**SRS Reference**: FR 2.0

---

### 1.2 `skill_semantic_filter`

**Purpose**: Score content relevance against active goals using lightweight LLM. Only content above threshold triggers task creation.

**Invoked By**: Planner Agent (after resource monitoring)

**Input Contract**:

```json
{
  "agent_id": "string (UUID)",
  "content": "object (resource content)",
  "active_goals": [
    {
      "goal_id": "string (UUID)",
      "description": "string",
      "priority": "string (high | medium | low)"
    }
  ],
  "relevance_threshold": "number (default: 0.75, range: 0.0-1.0)"
}
```

**Output Contract**:

```json
{
  "success": "boolean",
  "relevance_score": "number (0.0-1.0)",
  "matches_threshold": "boolean",
  "matched_goals": [
    {
      "goal_id": "string (UUID)",
      "match_score": "number (0.0-1.0)"
    }
  ],
  "reasoning": "string (optional LLM reasoning)",
  "error": "string (if success === false)"
}
```

**MCP Dependencies**: 
- LLM inference (Gemini 3 Flash or Haiku 3.5)

**SRS Reference**: FR 2.1

---

### 1.3 `skill_detect_trends`

**Purpose**: Analyze aggregated data over time intervals to identify emerging topic clusters and generate Trend Alerts.

**Invoked By**: Trend Spotter Worker (background process)

**Input Contract**:

```json
{
  "agent_id": "string (UUID)",
  "time_window_hours": "number (default: 4)",
  "resource_uris": [
    "string (MCP Resource URI)"
  ],
  "min_cluster_size": "number (default: 5)",
  "window_start": "string (ISO 8601, optional)",
  "window_end": "string (ISO 8601, optional)"
}
```

**Output Contract**:

```json
{
  "success": "boolean",
  "trend_alerts": [
    {
      "alert_id": "string (UUID)",
      "topics": ["string"],
      "relevance_score": "number (0.0-1.0)",
      "source_resources": ["string (MCP Resource URI)"],
      "window_start": "string (ISO 8601)",
      "window_end": "string (ISO 8601)",
      "cluster_size": "number"
    }
  ],
  "analysis_timestamp": "string (ISO 8601)",
  "error": "string (if success === false)"
}
```

**MCP Dependencies**: 
- `mcp-server-news` (Resources)
- LLM inference for topic clustering

**SRS Reference**: FR 2.2  
**Technical Spec**: § 1.9 Trend Alert

---

## 2. Memory & Persona Management Skills

### 2.1 `skill_load_persona`

**Purpose**: Load and parse SOUL.md configuration file to instantiate agent persona (backstory, voice, beliefs, directives).

**Invoked By**: Cognitive Core (at agent startup and context assembly)

**Input Contract**:

```json
{
  "agent_id": "string (UUID)",
  "soul_file_path": "string (default: agents/{agent_id}/SOUL.md)"
}
```

**Output Contract**:

```json
{
  "success": "boolean",
  "persona": {
    "agent_id": "string (UUID)",
    "name": "string",
    "backstory": "string",
    "voice_traits": ["string"],
    "core_beliefs": ["string"],
    "directives": ["string"],
    "honesty_directive": "string (special directive for transparency)"
  },
  "loaded_at": "string (ISO 8601)",
  "error": "string (if success === false)"
}
```

**Dependencies**: File system access to SOUL.md

**SRS Reference**: FR 1.0

---

### 2.2 `skill_retrieve_episodic_memory`

**Purpose**: Fetch short-term episodic memory from Redis cache (last 1 hour window).

**Invoked By**: Cognitive Core (before each reasoning step)

**Input Contract**:

```json
{
  "agent_id": "string (UUID)",
  "window_hours": "number (default: 1)",
  "limit": "number (default: 50)"
}
```

**Output Contract**:

```json
{
  "success": "boolean",
  "memories": [
    {
      "memory_id": "string (UUID)",
      "timestamp": "string (ISO 8601)",
      "content": "string",
      "context": "object",
      "memory_type": "string (conversation | action | event)"
    }
  ],
  "window_start": "string (ISO 8601)",
  "window_end": "string (ISO 8601)",
  "count": "number",
  "error": "string (if success === false)"
}
```

**Dependencies**: Redis cache

**SRS Reference**: FR 1.1

---

### 2.3 `skill_retrieve_semantic_memory`

**Purpose**: Query Weaviate vector database for semantically relevant long-term memories based on current context.

**Invoked By**: Cognitive Core (before each reasoning step)

**Input Contract**:

```json
{
  "agent_id": "string (UUID)",
  "query_text": "string",
  "limit": "number (default: 5)",
  "similarity_threshold": "number (default: 0.7, range: 0.0-1.0)"
}
```

**Output Contract**:

```json
{
  "success": "boolean",
  "memories": [
    {
      "memory_id": "string (UUID)",
      "content": "string",
      "similarity_score": "number (0.0-1.0)",
      "timestamp": "string (ISO 8601)",
      "metadata": "object"
    }
  ],
  "query_timestamp": "string (ISO 8601)",
  "count": "number",
  "error": "string (if success === false)"
}
```

**MCP Dependencies**: 
- `mcp-server-weaviate` (Tool: `search_memory`)

**SRS Reference**: FR 1.1

---

### 2.4 `skill_assemble_context`

**Purpose**: Dynamically construct system prompt from SOUL.md, episodic memory, and semantic memory for LLM context injection.

**Invoked By**: Cognitive Core (before each reasoning step)

**Input Contract**:

```json
{
  "agent_id": "string (UUID)",
  "input_query": "string",
  "episodic_memories": [
    {
      "memory_id": "string (UUID)",
      "timestamp": "string (ISO 8601)",
      "content": "string",
      "context": "object"
    }
  ],
  "semantic_memories": [
    {
      "memory_id": "string (UUID)",
      "content": "string",
      "similarity_score": "number",
      "timestamp": "string (ISO 8601)"
    }
  ],
  "persona": {
    "name": "string",
    "backstory": "string",
    "voice_traits": ["string"],
    "directives": ["string"]
  }
}
```

**Output Contract**:

```json
{
  "success": "boolean",
  "system_prompt": "string (formatted prompt with sections: Who You Are, What You Remember, Current Context)",
  "context_length": "number (token count estimate)",
  "assembled_at": "string (ISO 8601)",
  "error": "string (if success === false)"
}
```

**Dependencies**: 
- `skill_load_persona`
- `skill_retrieve_episodic_memory`
- `skill_retrieve_semantic_memory`

**SRS Reference**: FR 1.1

---

### 2.5 `skill_evolve_persona`

**Purpose**: Summarize high-engagement interactions and update long-term biography in Weaviate to enable persona learning.

**Invoked By**: Judge Agent (background process after successful high-engagement interactions)

**Input Contract**:

```json
{
  "agent_id": "string (UUID)",
  "interaction_id": "string (UUID)",
  "engagement_metrics": {
    "likes": "number",
    "comments": "number",
    "shares": "number",
    "engagement_score": "number (0.0-1.0)"
  },
  "interaction_content": "object",
  "timestamp": "string (ISO 8601)"
}
```

**Output Contract**:

```json
{
  "success": "boolean",
  "memory_id": "string (UUID)",
  "summary": "string (generated summary of interaction)",
  "written_to_weaviate": "boolean",
  "timestamp": "string (ISO 8601)",
  "error": "string (if success === false)"
}
```

**MCP Dependencies**: 
- `mcp-server-weaviate` (Tool: `write_memory`)
- LLM inference for summarization

**SRS Reference**: FR 1.2

---

## 3. Content Generation Skills

### 3.1 `skill_generate_text`

**Purpose**: Generate text content (captions, scripts, replies) using the Cognitive Core LLM with persona-aware context.

**Invoked By**: Worker Agent (for text generation tasks)

**Input Contract**:

```json
{
  "agent_id": "string (UUID)",
  "task_id": "string (UUID)",
  "prompt": "string",
  "content_type": "string (caption | script | reply | post)",
  "persona_constraints": ["string"],
  "max_length": "number (default: 500)",
  "temperature": "number (default: 0.7, range: 0.0-1.0)",
  "system_context": "string (from skill_assemble_context)"
}
```

**Output Contract**:

```json
{
  "success": "boolean",
  "text_content": "string",
  "confidence_score": "number (0.0-1.0)",
  "token_count": "number",
  "generated_at": "string (ISO 8601)",
  "error": "string (if success === false)"
}
```

**Dependencies**: 
- LLM inference (Gemini 3 Pro / Claude Opus 4.5)
- `skill_assemble_context` (for system prompt)

**SRS Reference**: FR 3.0  
**Technical Spec**: § 1.2 Worker Result (artifact.text_content)

---

### 3.2 `skill_generate_image`

**Purpose**: Generate images via MCP Tools with mandatory character consistency enforcement.

**Invoked By**: Worker Agent (for image generation tasks)

**Input Contract**:

```json
{
  "agent_id": "string (UUID)",
  "task_id": "string (UUID)",
  "prompt": "string",
  "character_reference_id": "string (UUID, REQUIRED)",
  "negative_prompt": "string (optional)",
  "aspect_ratio": "string (default: 1:1, e.g. 16:9, 4:3)",
  "style_guidance": "object (optional)"
}
```

**Output Contract**:

```json
{
  "success": "boolean",
  "image_url": "string",
  "asset_id": "string (UUID)",
  "character_reference_id": "string (UUID)",
  "generation_metadata": {
    "model_provider": "string",
    "model_version": "string",
    "cost_usd": "number"
  },
  "generated_at": "string (ISO 8601)",
  "error": "string (if success === false)"
}
```

**MCP Dependencies**: 
- `mcp-server-ideogram` or `mcp-server-midjourney` (Tool: `generate_image`)

**SRS Reference**: FR 3.0, FR 3.1  
**Technical Spec**: § 1.5 MCP Tool: generate_image

---

### 3.3 `skill_generate_video`

**Purpose**: Generate video content via MCP Tools with tiered strategy (Tier 1: cost-effective, Tier 2: premium).

**Invoked By**: Worker Agent (for video generation tasks)

**Input Contract**:

```json
{
  "agent_id": "string (UUID)",
  "task_id": "string (UUID)",
  "tier": "string (tier1 | tier2, REQUIRED)",
  "prompt_text": "string",
  "source_image_url": "string (REQUIRED for tier1)",
  "character_reference_id": "string (UUID, optional)",
  "duration_seconds": "number (default: 10)",
  "negative_prompt": "string (optional)"
}
```

**Output Contract**:

```json
{
  "success": "boolean",
  "video_url": "string",
  "job_id": "string",
  "tier": "string (tier1 | tier2)",
  "generation_metadata": {
    "model_provider": "string (runway | luma)",
    "model_version": "string",
    "cost_usd": "number",
    "duration_seconds": "number",
    "resolution": "string"
  },
  "generated_at": "string (ISO 8601)",
  "error": "string (if success === false)"
}
```

**MCP Dependencies**: 
- `mcp-server-runway` or `mcp-server-luma` (Tool: `generate_video`)

**SRS Reference**: FR 3.0, FR 3.2  
**Technical Spec**: § 1.6 MCP Tool: generate_video

---

### 3.4 `skill_validate_character_consistency`

**Purpose**: Validate that generated images match the agent's character reference using vision-capable models.

**Invoked By**: Judge Agent (before approving image content)

**Input Contract**:

```json
{
  "agent_id": "string (UUID)",
  "generated_image_url": "string",
  "reference_image_url": "string",
  "character_reference_id": "string (UUID)"
}
```

**Output Contract**:

```json
{
  "success": "boolean",
  "is_consistent": "boolean",
  "consistency_score": "number (0.0-1.0)",
  "reasoning": "string (model explanation)",
  "validated_at": "string (ISO 8601)",
  "error": "string (if success === false)"
}
```

**Dependencies**: 
- Vision-capable LLM (Gemini 3 Pro Vision / GPT-4o)

**SRS Reference**: FR 3.1 (Developer Notes)  
**Functional Spec**: US-3.6

---

## 4. Social Media Action Skills

### 4.1 `skill_post_content`

**Purpose**: Publish text and optional media to social platforms via MCP Tools with platform-agnostic interface.

**Invoked By**: Worker Agent (after Judge approval)

**Input Contract**:

```json
{
  "agent_id": "string (UUID)",
  "task_id": "string (UUID)",
  "platform": "string (twitter | instagram | threads, REQUIRED)",
  "text_content": "string (REQUIRED)",
  "media_urls": ["string"],
  "disclosure_level": "string (automated | assisted | none, default: automated)"
}
```

**Output Contract**:

```json
{
  "success": "boolean",
  "post_id": "string",
  "url": "string",
  "platform": "string",
  "published_at": "string (ISO 8601)",
  "error": "string (if success === false)"
}
```

**MCP Dependencies**: 
- `mcp-server-twitter` (Tool: `post_tweet`)
- `mcp-server-instagram` (Tool: `publish_media`)
- `mcp-server-threads` (Tool: `post_content`)

**SRS Reference**: FR 4.0  
**Technical Spec**: § 1.3 MCP Tool: post_content

---

### 4.2 `skill_reply_comment`

**Purpose**: Generate context-aware reply and post it to a specific mention/comment using memory and persona.

**Invoked By**: Worker Agent (for reply tasks)

**Input Contract**:

```json
{
  "agent_id": "string (UUID)",
  "task_id": "string (UUID)",
  "platform": "string (twitter | instagram | threads, REQUIRED)",
  "parent_id": "string (REQUIRED)",
  "parent_content": "string",
  "parent_author": "string",
  "context_memories": {
    "episodic": ["object"],
    "semantic": ["object"]
  },
  "persona_constraints": ["string"]
}
```

**Output Contract**:

```json
{
  "success": "boolean",
  "reply_id": "string",
  "reply_text": "string",
  "confidence_score": "number (0.0-1.0)",
  "platform": "string",
  "published_at": "string (ISO 8601)",
  "error": "string (if success === false)"
}
```

**Dependencies**: 
- `skill_generate_text` (for reply generation)
- `skill_assemble_context` (for memory retrieval)
- MCP Tools: `reply_comment` (platform-specific)

**SRS Reference**: FR 4.1  
**Technical Spec**: § 1.4 MCP Tool: reply_comment

---

### 4.3 `skill_manage_engagement_loop`

**Purpose**: Orchestrate the full bi-directional interaction loop: ingest → plan → generate → act → verify.

**Invoked By**: Planner Agent (when mentions/comments detected)

**Input Contract**:

```json
{
  "agent_id": "string (UUID)",
  "mention_id": "string",
  "platform": "string",
  "mention_content": "string",
  "mention_author": "string",
  "mention_timestamp": "string (ISO 8601)"
}
```

**Output Contract**:

```json
{
  "success": "boolean",
  "task_id": "string (UUID)",
  "reply_id": "string",
  "workflow_steps": [
    {
      "step": "string (ingest | plan | generate | act | verify)",
      "status": "string (success | failure)",
      "timestamp": "string (ISO 8601)"
    }
  ],
  "completed_at": "string (ISO 8601)",
  "error": "string (if success === false)"
}
```

**Dependencies**: 
- `skill_semantic_filter` (relevance check)
- `skill_reply_comment` (reply generation and posting)
- Judge validation

**SRS Reference**: FR 4.1  
**Functional Spec**: US-4.4

---

## 5. Agentic Commerce Skills

### 5.1 `skill_get_wallet_balance`

**Purpose**: Check wallet balance (USDC/ETH) via Coinbase AgentKit. Planner MUST call before cost-incurring workflows.

**Invoked By**: Planner Agent (before starting cost-incurring tasks)

**Input Contract**:

```json
{
  "agent_id": "string (UUID)"
}
```

**Output Contract**:

```json
{
  "success": "boolean",
  "wallet_address": "string",
  "balances": {
    "USDC": "string (decimal)",
    "ETH": "string (decimal)"
  },
  "checked_at": "string (ISO 8601)",
  "error": "string (if success === false)"
}
```

**MCP Dependencies**: 
- `mcp-server-coinbase` (Tool: `get_balance`)

**SRS Reference**: FR 5.1  
**Technical Spec**: § 1.7 MCP Tool: get_balance

---

### 5.2 `skill_transfer_asset`

**Purpose**: Execute on-chain transfers (USDC or native assets) via Coinbase AgentKit with budget governance.

**Invoked By**: Worker Agent (for transaction tasks, after CFO Judge approval)

**Input Contract**:

```json
{
  "agent_id": "string (UUID)",
  "task_id": "string (UUID)",
  "to_address": "string (REQUIRED)",
  "amount_usdc": "number (optional, mutually exclusive with amount_native)",
  "amount_native": "string (optional, e.g. ETH amount)",
  "token_symbol": "string (default: USDC, e.g. USDC | ETH)"
}
```

**Output Contract**:

```json
{
  "success": "boolean",
  "tx_hash": "string",
  "amount": "string",
  "token_symbol": "string",
  "to_address": "string",
  "executed_at": "string (ISO 8601)",
  "error": "string (if success === false, e.g. BudgetExceededError)"
}
```

**MCP Dependencies**: 
- `mcp-server-coinbase` (Tool: `send_payment`)

**SRS Reference**: FR 5.1  
**Technical Spec**: § 1.8 MCP Tool: send_payment

---

### 5.3 `skill_deploy_token`

**Purpose**: Deploy ERC-20 tokens (e.g., for fan loyalty programs) via Coinbase AgentKit.

**Invoked By**: Worker Agent (for token deployment tasks, after CFO Judge approval)

**Input Contract**:

```json
{
  "agent_id": "string (UUID)",
  "task_id": "string (UUID)",
  "token_name": "string (REQUIRED)",
  "token_symbol": "string (REQUIRED)",
  "total_supply": "string (REQUIRED)",
  "metadata_uri": "string (optional)"
}
```

**Output Contract**:

```json
{
  "success": "boolean",
  "token_address": "string",
  "token_name": "string",
  "token_symbol": "string",
  "tx_hash": "string",
  "deployed_at": "string (ISO 8601)",
  "error": "string (if success === false)"
}
```

**MCP Dependencies**: 
- `mcp-server-coinbase` (Tool: `deploy_token`)

**SRS Reference**: FR 5.1

---

### 5.4 `skill_enforce_budget`

**Purpose**: CFO Judge skill to review transaction requests and enforce budget limits with anomaly detection.

**Invoked By**: Judge Agent (CFO role, before approving transactions)

**Input Contract**:

```json
{
  "agent_id": "string (UUID)",
  "transaction_request": {
    "action": "string (native_transfer | deploy_token)",
    "to_address": "string",
    "amount_usdc": "number",
    "token_symbol": "string"
  },
  "budget_config": {
    "max_daily_spend_usdc": "number",
    "max_single_transaction_usdc": "number",
    "daily_spend_usdc": "number (current day)"
  }
}
```

**Output Contract**:

```json
{
  "success": "boolean",
  "approved": "boolean",
  "reason": "string",
  "anomaly_detected": "boolean",
  "anomaly_type": "string (optional, e.g. exceeds_daily_limit | suspicious_pattern)",
  "requires_hitl": "boolean",
  "checked_at": "string (ISO 8601)",
  "error": "string (if success === false)"
}
```

**Dependencies**: 
- Redis (for daily spend tracking)
- Budget configuration

**SRS Reference**: FR 5.2  
**Functional Spec**: US-5.4, US-5.5

---

## 6. Validation & Governance Skills

### 6.1 `skill_score_confidence`

**Purpose**: Generate confidence scores (0.0-1.0) for all Worker outputs (text, image, transaction).

**Invoked By**: Worker Agent (after generating output)

**Input Contract**:

```json
{
  "agent_id": "string (UUID)",
  "output_type": "string (text | image | video | transaction)",
  "output_content": "object (type-specific)",
  "generation_metadata": "object (optional)"
}
```

**Output Contract**:

```json
{
  "success": "boolean",
  "confidence_score": "number (0.0-1.0)",
  "reasoning": "string (optional explanation)",
  "scored_at": "string (ISO 8601)",
  "error": "string (if success === false)"
}
```

**Dependencies**: 
- LLM inference (for self-assessment)

**SRS Reference**: NFR 1.0  
**Functional Spec**: US-7.1

---

### 6.2 `skill_route_hitl`

**Purpose**: Route tasks to Human-in-the-Loop based on confidence thresholds and sensitive topic detection.

**Invoked By**: Judge Agent (after validating Worker output)

**Input Contract**:

```json
{
  "agent_id": "string (UUID)",
  "task_id": "string (UUID)",
  "confidence_score": "number (0.0-1.0, REQUIRED)",
  "content_type": "string (text | image | video | transaction)",
  "content_data": "object",
  "sensitive_flags": ["string"],
  "hitl_config": {
    "high_threshold": "number (default: 0.90)",
    "medium_threshold": "number (default: 0.70)",
    "low_threshold": "number (default: 0.70)"
  }
}
```

**Output Contract**:

```json
{
  "success": "boolean",
  "routing_decision": "string (auto_approve | async_approval | reject_retry | mandatory_hitl)",
  "hitl_review_id": "string (UUID, if routed to HITL)",
  "reasoning": "string",
  "routed_at": "string (ISO 8601)",
  "error": "string (if success === false)"
}
```

**Dependencies**: 
- `skill_detect_sensitive_topics`
- HITL queue (Redis/Database)

**SRS Reference**: NFR 1.1  
**Functional Spec**: US-7.2, US-7.3, US-7.4, US-7.5  
**Technical Spec**: § 1.10 HITL Review API

---

### 6.3 `skill_detect_sensitive_topics`

**Purpose**: Detect sensitive topics (Politics, Health Advice, Financial Advice, Legal Claims) for mandatory HITL routing.

**Invoked By**: Judge Agent (before routing decisions)

**Input Contract**:

```json
{
  "agent_id": "string (UUID)",
  "content": "string | object",
  "content_type": "string (text | image | video)",
  "sensitive_categories": ["string (default: [politics, health_advice, financial_advice, legal_claims])"]
}
```

**Output Contract**:

```json
{
  "success": "boolean",
  "is_sensitive": "boolean",
  "detected_categories": ["string"],
  "confidence": "number (0.0-1.0)",
  "detected_at": "string (ISO 8601)",
  "error": "string (if success === false)"
}
```

**Dependencies**: 
- Keyword matching
- Semantic classification (LLM)

**SRS Reference**: NFR 1.2  
**Functional Spec**: US-7.5

---

### 6.4 `skill_enforce_disclosure`

**Purpose**: Ensure AI disclosure labels are set on published content using platform-native features.

**Invoked By**: Worker Agent (before publishing content)

**Input Contract**:

```json
{
  "agent_id": "string (UUID)",
  "platform": "string (twitter | instagram | threads)",
  "content_type": "string (text | image | video | multimodal)",
  "disclosure_level": "string (automated | assisted | none)"
}
```

**Output Contract**:

```json
{
  "success": "boolean",
  "disclosure_applied": "boolean",
  "platform_label": "string (platform-specific label, e.g. is_generated, ai_label)",
  "applied_at": "string (ISO 8601)",
  "error": "string (if success === false)"
}
```

**SRS Reference**: NFR 2.0  
**Functional Spec**: US-7.6

---

### 6.5 `skill_handle_honesty_directive`

**Purpose**: Detect direct inquiries about agent nature and enforce truthful disclosure, overriding persona constraints.

**Invoked By**: Cognitive Core (during conversation processing)

**Input Contract**:

```json
{
  "agent_id": "string (UUID)",
  "user_query": "string",
  "persona": "object"
}
```

**Output Contract**:

```json
{
  "success": "boolean",
  "requires_disclosure": "boolean",
  "disclosure_response": "string (if requires_disclosure === true)",
  "detected_at": "string (ISO 8601)",
  "error": "string (if success === false)"
}
```

**Dependencies**: 
- Query classification (LLM or keyword matching)

**SRS Reference**: NFR 2.1  
**Functional Spec**: US-1.4

---

## Implementation Notes

### Skill Invocation Pattern

Skills are invoked by Workers during task execution. The typical flow:

1. **Planner** creates Task → pushes to TaskQueue
2. **Worker** pops Task → invokes appropriate Skill(s)
3. **Worker** generates Result → pushes to ReviewQueue
4. **Judge** validates Result → approves/rejects/escalates

### Error Handling

All Skills return a `success` boolean and an optional `error` string. Workers should:
- Retry transient errors (with exponential backoff)
- Escalate persistent errors to Planner for re-planning
- Log all errors for telemetry

### MCP Integration

Skills compose MCP Tools but do not directly implement MCP protocol. The MCP Client (in the agent runtime) handles:
- Server discovery
- Transport (Stdio/SSE)
- JSON-RPC protocol
- Tool invocation

### Testing Strategy

Each Skill should have:
- Unit tests (mock MCP dependencies)
- Integration tests (real MCP servers in test environment)
- Contract tests (validate Input/Output schemas)

See `tests/test_skills_interface.py` for contract validation tests.

---

## Traceability

| Skill | SRS Reference | Technical Spec | Functional Spec |
|-------|---------------|----------------|-----------------|
| `skill_monitor_resources` | FR 2.0 | - | US-2.1 |
| `skill_semantic_filter` | FR 2.1 | - | US-2.2 |
| `skill_detect_trends` | FR 2.2 | § 1.9 | US-2.3, US-2.4 |
| `skill_load_persona` | FR 1.0 | - | US-1.1 |
| `skill_retrieve_episodic_memory` | FR 1.1 | - | US-1.2 |
| `skill_retrieve_semantic_memory` | FR 1.1 | - | US-1.2 |
| `skill_assemble_context` | FR 1.1 | - | US-1.3 |
| `skill_evolve_persona` | FR 1.2 | - | US-1.5 |
| `skill_generate_text` | FR 3.0 | § 1.2 | US-3.1 |
| `skill_generate_image` | FR 3.0, FR 3.1 | § 1.5 | US-3.1, US-3.3 |
| `skill_generate_video` | FR 3.0, FR 3.2 | § 1.6 | US-3.2, US-3.4 |
| `skill_validate_character_consistency` | FR 3.1 | - | US-3.6 |
| `skill_post_content` | FR 4.0 | § 1.3 | US-4.1 |
| `skill_reply_comment` | FR 4.1 | § 1.4 | US-4.2 |
| `skill_manage_engagement_loop` | FR 4.1 | - | US-4.4 |
| `skill_get_wallet_balance` | FR 5.1 | § 1.7 | US-5.2 |
| `skill_transfer_asset` | FR 5.1 | § 1.8 | US-5.3 |
| `skill_deploy_token` | FR 5.1 | - | US-5.3 |
| `skill_enforce_budget` | FR 5.2 | - | US-5.4, US-5.5 |
| `skill_score_confidence` | NFR 1.0 | § 1.2 | US-7.1 |
| `skill_route_hitl` | NFR 1.1 | § 1.10 | US-7.2-7.5 |
| `skill_detect_sensitive_topics` | NFR 1.2 | - | US-7.5 |
| `skill_enforce_disclosure` | NFR 2.0 | - | US-7.6 |
| `skill_handle_honesty_directive` | NFR 2.1 | - | US-1.4 |

---

## Next Steps

1. **Implementation**: Create Python modules for each skill (e.g., `skills/perception/monitor_resources.py`)
2. **Contract Validation**: Implement Pydantic models for Input/Output schemas
3. **MCP Integration**: Wire Skills to MCP Client for Tool invocation
4. **Testing**: Write failing tests per TDD approach (Task 3.1)
5. **Documentation**: Add usage examples and error handling patterns

---

**Status**: Structure defined, contracts specified. Ready for implementation phase.
