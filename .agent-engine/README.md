# Agent Engine

**This is the development orchestration tool that BUILDS the application.**  
**It is NOT part of the application itself.**

## Purpose

The Agent Engine is a local autonomous system that:
- Receives your project requirements
- Orchestrates specialized AI agents
- Builds the complete application structure
- Manages the development lifecycle
- Ensures quality and compliance
- Maintains audit trails

## Architecture

```
User Input (Project Idea/Scope)
        ↓
   AGENT ENGINE (This folder)
        ↓
   Overseer Agent
        ↓
   ┌─────────────────────────────────┐
   │  Specialized Agents (Parallel)  │
   ├─────────────────────────────────┤
   │  • PRD Generator                │
   │  • Researcher                   │
   │  • Scaffolder                   │
   │  • Implementation Agent         │
   │  • Compliance Agent             │
   │  • Test Engineer                │
   │  • Documentation Writer         │
   └─────────────────────────────────┘
        ↓
   APPLICATION CODE
   (frontend/, backend/, etc.)
```

## What Gets Created

The Agent Engine creates the **actual application** in the project root:

```
project-root/
├── .agent-engine/        ← THIS (orchestration tool)
├── frontend/             ← THE APPLICATION
├── backend/              ← THE APPLICATION
├── docs/                 ← Application documentation
├── .github/              ← CI/CD for the application
├── project_memory.md     ← Audit trail
└── README.md             ← Application README
```

## How It Works (Simple Terms)

1. **You give an instruction:**
   ```
   "Build a vehicle panel beating workflow management system with RBAC"
   ```

2. **Agent Engine activates:**
   - Overseer reads your request
   - Creates PRD (Product Requirements Document)
   - Researches domain and tech stack
   - Sets up folder structure
   - Generates application code
   - Writes tests
   - Validates everything
   - Documents the project

3. **You get a working project:**
   - Complete codebase
   - Documentation
   - Tests
   - CI/CD pipelines
   - Environment setup
   - Audit trail in project_memory.md

## Key Principle

**The Agent Engine is a TOOL that creates SOFTWARE.**

**Like using a compiler:**
- You don't deploy the compiler with your app
- You don't confuse the compiler with your code
- The compiler is a build tool

**Similarly:**
- You don't deploy .agent-engine/ with your app
- You don't confuse agents with app features
- The Agent Engine is a development tool

## Technology Stack

- **Orchestration:** LangGraph + CrewAI
- **Communication:** A2A Protocol (Agent-to-Agent)
- **LLM Backend:** GitHub Copilot (Claude 3.5, GPT-4, Gemini)
- **Tools Access:** MCP Server (Serper API, GitHub, File System)
- **Quality Gates:** ASOP Framework
- **Audit Trail:** project_memory.md

## Status

**Version:** 0.1.0-alpha  
**Status:** Initial POC implementation  
**Framework:** Vibing Agentic SDLC v1.1.0

## Next Steps

See `IMPLEMENTATION_PLAN.md` for detailed setup instructions.
