# ADR 0008: No subagents in v1

- Status: Accepted
- Date: 2026-11-10

## Context

A question-verification agent that has not seen how a question was written would catch wrong answer keys. Plugin agents load in Cowork and Claude Code but are ignored in claude.ai chat.

## Decision

v1 ships no agents. Quality is protected by mandatory documentation links and a "wrong question" feedback path. v2 adds a verifier agent for surfaces that support it.
