# ADR 0002: Store progress in a tracker artifact database

- Status: Accepted
- Date: 2026-11-10

## Context

Progress must persist across chats, be visible as a dashboard, and be readable and writable by Claude in any conversation.

## Options

1. Claude Project knowledge files. Rejected: Claude can read them but cannot write to them from a chat.
2. Files in the chat sandbox (`/mnt/...`). Rejected: they do not persist across chats.
3. Claude memory. Rejected: designed for short facts, not logs; not a dashboard.
4. Google Sheets or GitHub. Possible, but requires connectors, is slower per answer and has no built-in UI.
5. A published Claude artifact with the `db` runtime capability. Persistent, private to the owner, live UI through `onSnapshot`, writable by Claude with the artifact data tool.

## Decision

Option 5. `init` publishes the tracker page from a template with `capabilities: {db: {}}` and seeds its database. All other skills read and write that database.

## Consequences

- Works on claude.ai chat, the desktop app and Cowork. Claude Code is not a learner surface in v1.
- One tracker per certification. A Project instructions line binds a Project to its tracker (see ARCHITECTURE §5.3).
- Database schema is versioned (`settings.schemaVersion`) so `rebuild` can migrate.
- Exporting a backup to Sheets or GitHub is possible later but not part of v1.
