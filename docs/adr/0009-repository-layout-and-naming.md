# ADR 0009: Repository layout and naming

- Status: Accepted
- Date: 2026-11-10

## Decision

| Item | Value | Reason |
|---|---|---|
| Repository | `gcp-certification-coach` (public) | Contains the search term "certification" |
| Plugin `name` | `gcp-cert-coach` | Permanent identity; short because it prefixes every command (`/gcp-cert-coach:quiz`) |
| Plugin `displayName` | GCP Certification Coach | Shown in plugin lists and directories |
| Skill names | `init`, `learn`, `quiz`, `challenge`, `mock`, `progress`, `sync`, `rebuild`, `reset` | Short, typed often; disambiguated by the plugin prefix and precise descriptions; no reserved words (`claude`, `anthropic`) |

Layout:

- Repository root = marketplace (`.claude-plugin/marketplace.json`).
- Plugin in `plugins/gcp-cert-coach/` containing only what users install: manifest, skills, README, LICENSE.
- `docs/`, `evals/`, `scripts/`, `.github/` stay outside the plugin folder.
- No top-level `bin/` directory anywhere in the plugin (it blocks installation on claude.ai and Cowork).

## Licensing

- Code: MIT (`LICENSE`).
- Content (packs, cheat sheets, docs): CC BY 4.0 (`LICENSE-CONTENT`).
- Non-affiliation disclaimer in README and plugin description.

## GitHub topics

`claude-code`, `claude-skills`, `claude-code-plugin`, `agent-skills`, `anthropic`, `gcp`, `google-cloud`, `google-cloud-platform`, `gcp-certification`, `google-cloud-certification`, `associate-cloud-engineer`, `google-cloud-skills-boost`, `certification`, `exam-prep`, `study-guide`, `practice-questions`, `spaced-repetition`, `coursera`.
