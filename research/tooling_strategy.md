# Developer Tools Strategy: MCP Servers Configuration

**Project:** Project Chimera  
**Date:** February 6, 2026  
**Task:** Sub-Task A - Developer Tools (MCP)  
**Status:** Configured

---

## Overview

This document outlines the selection and configuration of MCP (Model Context Protocol) servers that serve as **developer tools** for Project Chimera. These tools are distinct from runtime agent skills and are designed to assist developers during the development, testing, and maintenance phases of the project.

**Key Distinction:**  
- **Developer Tools (MCP)**: Tools that help **developers** build and maintain the codebase (this document)
- **Agent Skills (Runtime)**: Capabilities that the **Chimera agents** use at runtime (separate task)

---

## Selected MCP Servers

### 1. GitHub MCP Server
**Purpose:** Repository management, issue tracking, PR automation, and code analysis  
**Package:** `@modelcontextprotocol/server-github`  
**Use Cases:**
- Browse and search code repositories
- Create and manage GitHub Issues and Pull Requests
- Monitor GitHub Actions workflows and CI/CD pipelines
- Analyze code patterns and security findings
- Access repository discussions and notifications

**Configuration:**
- Requires GitHub Personal Access Token (PAT) with `repo` scope
- Connects via Docker or direct Node.js execution
- Provides Tools: `create_issue`, `create_pull_request`, `search_code`, `get_repository_info`
- Provides Resources: `github://repo/{owner}/{repo}/issues`, `github://repo/{owner}/{repo}/pulls`

**Rationale:** Essential for managing the Project Chimera repository, tracking issues, and automating PR workflows as specified in Task 3.3 (CI/CD & AI Governance).

---

### 2. Filesystem MCP Server
**Purpose:** Secure file operations and project structure management  
**Package:** `@modelcontextprotocol/server-filesystem`  
**Use Cases:**
- Read and write project files with configurable access controls
- Navigate project directory structure
- Manage configuration files
- Create and modify documentation

**Configuration:**
- Scoped to project root directory: `/home/neba/work/tenx-trp/tenx-day-3-5/Chimera-tenx`
- Provides Tools: `read_file`, `write_file`, `list_directory`, `create_directory`
- Provides Resources: `file://{path}` for reading file contents

**Rationale:** Core developer tool for file operations. Enables AI assistants to read specs, modify code, and manage project structure while maintaining security boundaries.

---

### 3. Git MCP Server
**Purpose:** Version control operations and repository history analysis  
**Package:** `mcp-server-git` (Python-based)  
**Use Cases:**
- Read Git repository history and commit information
- Search commits by message, author, or date
- Analyze branch structure and merge history
- Generate commit messages and manage branches

**Configuration:**
- Points to repository root: `/home/neba/work/tenx-trp/tenx-day-3-5/Chimera-tenx`
- Provides Tools: `git_log`, `git_diff`, `git_status`, `git_branch_info`
- Provides Resources: `git://commits`, `git://branches`

**Rationale:** Critical for maintaining Git hygiene as required by the project (Task 1.3). Enables AI assistants to understand commit history, track changes, and ensure atomic commits.

---

### 4. SQLite MCP Server
**Purpose:** Database operations for development and testing  
**Package:** `@modelcontextprotocol/server-sqlite`  
**Use Cases:**
- Query and inspect database schemas
- Execute SQL queries for testing
- Analyze data structures
- Validate database migrations

**Configuration:**
- Points to development database: `./data/chimera_dev.db` (to be created)
- Provides Tools: `query`, `execute`, `get_schema`
- Provides Resources: `sqlite://tables`, `sqlite://schema`

**Rationale:** While production uses PostgreSQL and Weaviate, SQLite is useful for local development, testing, and rapid prototyping. Aligns with the TDD approach (Task 3.1) by enabling database schema validation.

---

## Configuration File

The MCP servers are configured in `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-github"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/home/neba/work/tenx-trp/tenx-day-3-5/Chimera-tenx"
      ]
    },
    "git": {
      "command": "uvx",
      "args": [
        "mcp-server-git",
        "--repository",
        "/home/neba/work/tenx-trp/tenx-day-3-5/Chimera-tenx"
      ]
    },
    "sqlite": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-sqlite",
        "./data/chimera_dev.db"
      ]
    }
  }
}
```

---

## Environment Variables Required

Create a `.env` file (or set in your shell environment) with:

```bash
# GitHub MCP Server
GITHUB_TOKEN=your_github_personal_access_token_here
```

**Note:** The GitHub token requires `repo` scope for full functionality.

---

## Installation & Verification

### Prerequisites
- Node.js 18+ (for npm-based MCP servers)
- Python 3.11+ with `uv` (for Git MCP server)
- Docker (optional, for GitHub MCP server alternative setup)

### Verification Steps

1. **Verify GitHub MCP Server:**
   ```bash
   npx -y @modelcontextprotocol/server-github --help
   ```

2. **Verify Filesystem MCP Server:**
   ```bash
   npx -y @modelcontextprotocol/server-filesystem --help
   ```

3. **Verify Git MCP Server:**
   ```bash
   uvx mcp-server-git --help
   ```

4. **Verify SQLite MCP Server:**
   ```bash
   npx -y @modelcontextprotocol/server-sqlite --help
   ```

---

## Integration with Project Chimera Workflow

### Spec-Driven Development
- **Filesystem MCP**: Enables AI assistants to read `specs/` directory before generating code
- **Git MCP**: Tracks spec changes and ensures code aligns with versioned specifications

### CI/CD & Governance
- **GitHub MCP**: Automates PR creation, issue tracking, and workflow monitoring
- **Git MCP**: Validates commit message quality and branch hygiene

### Testing & Development
- **SQLite MCP**: Enables rapid database schema testing and validation
- **Filesystem MCP**: Manages test files and fixtures

---

## Security Considerations

1. **Filesystem Access:** Scoped to project root only, preventing access to system files
2. **GitHub Token:** Stored as environment variable, never committed to repository
3. **SQLite Database:** Development database only, separate from production data
4. **Git Operations:** Read-only by default; write operations require explicit configuration

---

## Future Enhancements

Potential additional MCP servers for consideration:
- **PostgreSQL MCP Server**: For production database operations (when needed)
- **Docker MCP Server**: For container management and orchestration
- **Kubernetes MCP Server**: For K8s cluster management (future deployment phase)

---

## References

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [GitHub MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/github)
- [MCP Servers Directory](https://mcpbased.com/)
- Project Chimera Challenge Document: `docs/project-chimera-srs-challenge/project-chimera-challenge.md`
- Project Chimera SRS: `docs/project-chimera-srs-challenge/project-chimera-srs.md`

---

**Next Steps:**  
- ✅ MCP servers selected and documented  
- ✅ Configuration file created  
- ⏭️ Sub-Task B: Agent Skills (Runtime) - Separate task
