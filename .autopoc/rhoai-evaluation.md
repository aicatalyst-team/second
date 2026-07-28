# RHOAI Fitness Evaluation: Second

## Project Summary
Second is a platform for building custom internal software where AI agents and humans work side by side. It features a Next.js web frontend and a Hono-based worker that runs AI coding agents (Claude Code, Codex, OpenCode). Requires MongoDB replica set and Redis.

## Strategy Alignment: Agentic AI

### Impact Dimensions (0-20 each)

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| audience_value | 15 | Enterprise teams building internal tools with AI agents. Strong developer appeal but niche audience. |
| strategic_alignment | 14 | Aligns with agentic AI strategy area. Uses agent runtimes (Claude, Codex) but not Red Hat AI-specific runtimes (Llama Stack, MCP). |
| strategy_fit | 12 | Demonstrates multi-agent platform deployment but doesn't directly leverage Red Hat AI products (no InstructLab, no vLLM, no KServe). |
| platform_leverage | 16 | Multi-service architecture (web + worker + MongoDB + Redis) showcases OpenShift's orchestration strengths. |
| demo_potential | 15 | Interactive web UI for agent management. Visually compelling demo with real-time agent sessions. |

**Impact Score: (15 + 14 + 12 + 16 + 15) / 5 = 14.4 / 20 = 72%**

### Feasibility Dimensions (0-20 each)

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| container_readiness | 16 | Existing Dockerfiles and docker-compose.yml. Needs UBI conversion. |
| dependency_profile | 12 | Requires MongoDB replica set, Redis, and AI provider API keys. Non-trivial infrastructure. |
| reproduction_confidence | 14 | Self-hosting docs exist. Clear build/run instructions. |
| complexity_sweet_spot | 11 | 4-service architecture adds deployment complexity. MongoDB replica set is the main challenge. |

**Feasibility Score: (16 + 12 + 14 + 11) / 4 = 13.25 / 20 = 66%**

## Relationship
**validates-platform-story**: Second demonstrates a real multi-service agent platform deployment on OpenShift, validating the platform's ability to handle complex agentic AI workloads with multiple interconnected services.

## Strategy Areas
- agentic-ai

## Capability Labels
- agent-runtime, ai-hub, developer-experience

## Strengths
- Existing containerization (Dockerfiles + docker-compose)
- Apache-2.0 license (enterprise-friendly)
- Multi-service architecture demonstrates real OpenShift value
- Interactive web UI provides compelling demo
- Well-documented self-hosting instructions

## Risks
- MongoDB replica set requirement adds infrastructure complexity
- Requires external AI provider API keys (Anthropic/OpenAI)
- Worker installs large AI CLI tools (~300MB+)
- bubblewrap dependency may conflict with OpenShift security policies
