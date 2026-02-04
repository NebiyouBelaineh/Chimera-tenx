# Project Chimera: The Agentic Infrastructure Challenge

**Role:** Forward Deployed Engineer (FDE) Trainee  
**Duration:** February 4 - February 6, 2026

---

## Project Overview

Project Chimera is an engineering initiative to build a robust infrastructure for **Autonomous AI Influencers**. The system leverages **Spec-Driven Development (SDD)**, **Model Context Protocol (MCP)**, and **Agentic Commerce** to create digital entities capable of independent trend research, content creation, and financial management.

---

## 3-Day Roadmap

### Day 1: The Strategist (Research & Foundation)
**Focus:** Domain Mastery and Environment Setup

- **Task 1.1: Research Analysis**  
  Review the a16z Trillion Dollar AI Code Stack, OpenClaw protocols, MoltBook, and the Chimera SRS. Focus on inter-agent communication and sovereign digital identity.

- **Task 1.2: Architecture Strategy**  
  Document the agent pattern and infrastructure. Requirements include:
  - FastRender Swarm pattern (Planner/Worker/Judge)
  - Human-in-the-Loop safety triggers
  - Database selection (SQL for transactions vs NoSQL/Vector for metadata)

- **Task 1.3: Environment Initialization**  
  - Configure the Git repository using the **uv Python manager**  
  - Connect **Tenx MCP Sense** for activity telemetry  
  - Establish a `pyproject.toml`

---

### Day 2: The Architect (Specification & Context Engineering)
**Focus:** Translating Requirements into Executable Intent

- **Task 2.1: Master Specification**  
  Create a `specs/` directory using the GitHub Spec Kit framework:
  - `_meta.md`: Vision and constraints  
  - `functional.md`: User stories and agent behaviors  
  - `technical.md`: API contracts (JSON I/O) and Database ERDs

- **Task 2.2: Context Engineering**  
  Implement a `.cursor/rules` or `CLAUDE.md` file to govern IDE agents. Rules must:
  - Mandate spec-checking before code generation
  - Require plan explanation before execution

- **Task 2.3: Tooling & Skills**  
  - **Developer MCPs:** Configure `git-mcp` and `filesystem-mcp` for infrastructure management  
  - **Agent Skills:** Create a `skills/` directory with README-defined contracts for:
    - `skill_download_video`
    - `skill_transcribe_audio`
    - `skill_trend_fetcher`

---

### Day 3: The Governor (Infrastructure & Governance)
**Focus:** Safety, Testing, and Automation

- **Task 3.1: Test-Driven Development (TDD)**  
  Write failing unit tests in `tests/` based on technical specs. Focus on:
  - Data structure validation
  - Skill interface adherence

- **Task 3.2: Containerization**  
  - Develop a `Dockerfile` for environment encapsulation  
  - Create a `Makefile` with commands for setup and test

- **Task 3.3: CI/CD & Governance**  
  - Configure a GitHub Action (`.github/workflows/main.yml`) to execute the test suite on every push  
  - Implement a `.coderabbit.yaml` policy for AI-driven code reviews focusing on spec alignment and security

---

## Submission Checklist

### Day 1 Submission (Feb 4)
- **Google Drive Link:** A single PDF or Doc containing:
  - **Research Summary:** Key insights from required reading materials
  - **Architectural Approach:** Justification for agent patterns and infrastructure choices

### Day 3 Submission (Feb 6)
- **GitHub Repository:** Must include:
  - `specs/`, `tests/`, `skills/`
  - `Dockerfile`, `Makefile`
  - CI/CD workflows
- **Loom Video:** 5-minute walkthrough of:
  - Spec structure
  - Failing tests
  - IDE agent rule compliance
- **MCP Telemetry:** Verification of active Tenx MCP Sense connection during the challenge
