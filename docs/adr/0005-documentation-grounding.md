# ADR 0005: Ground content in public Google Cloud documentation via web search; defer MCP

- Status: Accepted
- Date: 2026-11-10

## Context

Explanations and questions must be correct and current. Options for retrieving official documentation:

1. Web search and fetch restricted to official domains (`cloud.google.com`, `docs.cloud.google.com`, `skills.google`). No setup.
2. Google Developer Knowledge MCP server (`search_documents`, `get_documents`, `answer_query`). More precise, but requires each user to create an API key in their own Google Cloud project and configure a connector; quotas apply; billing terms were not confirmed.

## Decision

v1 uses option 1. Every factual claim and every quiz question carries at least one documentation URL. When the needed fact is not confirmed by a fetched page, Claude says so instead of guessing.

v2 may add the MCP server as an optional connector. If added, the README must recommend a dedicated Google Cloud project without a billing account and a key restricted to that API, and must never ship a key in `.mcp.json`.

## Consequences

- Zero setup for users.
- Slightly slower than MCP; acceptable.
- Course materials are never used as a source (copyright).
