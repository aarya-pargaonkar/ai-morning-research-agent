# AI Morning Research Agent

## Goal
Find the five most important AI developments from the previous 24 hours and produce a concise, source-backed briefing.

## Architecture — Stage 1
User request -> LLM -> Web Search Tool -> observations -> LLM -> final briefing

## Planned progression
1. Basic tool-using agent
2. Research quality: multiple searches, deduplication, date/source checks
3. Reliability and guardrails
4. Morning automation
5. Architectural upgrades only when justified

## Principle
Every component should have a reason to exist. Avoid adding RAG, vector databases,
multi-agent systems, MCP, or orchestration frameworks until the project actually needs them.
