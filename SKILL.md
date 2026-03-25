---
name: solveit-cli
description: Use this skill when you need to inspect, search, edit, or execute SolveIt dialogs from the terminal with the `sic` CLI. It is for agent-driven dialog work, especially regex search, message reads, incremental edits, and code execution inside an existing SolveIt dialog.
---

# SolveIt CLI

Use `sic` for dialog work that should stay machine-readable and scriptable. Prefer it over ad hoc HTTP calls.

## Preconditions

- Ensure `sic` is installed and runnable.
- Set `SOLVEIT_TOKEN`. `SOLVEIT_URL` is optional; if omitted, `sic` defaults to `http://localhost:5001`.
- Default output is JSON. Add `--pretty` only when inspecting manually.
- Current `fastcore.script` flags use underscores, not hyphens, for command-specific options such as `--msg_type` and `--msg_id`.

## Default Workflow

Start read-only, then mutate incrementally.

1. Find the dialog area you need.
   Example: `sic --url http://localhost:6001 dialog find CRAFT '^# '`
2. Read the target message or list the dialog.
   Example: `sic --url http://localhost:6001 msg read CRAFT --msg_id _733cf1be`
   Example: `sic --url http://localhost:6001 dialog msgs CRAFT`
3. Apply one small edit at a time.
   Example: `sic --url http://localhost:6001 msg str-replace CRAFT _733cf1be 'old' 'new'`
   Example: `sic --url http://localhost:6001 msg replace-lines CRAFT _733cf1be 3 'print(x + y)'`
4. Re-read or execute immediately after each change.
   Example: `sic --url http://localhost:6001 msg exec CRAFT _733cf1be`

## High-Value Commands

- `dialog find`: primary discovery tool; use regex to jump to headings, sections, or known phrases.
- `dialog msgs`: best full-dialog snapshot.
- `msg read`: fetch one message by id or relative offset.
- `msg add`: add `note`, `code`, `prompt`, or `raw` messages.
- `msg insert-line`, `msg replace-lines`, `msg del-lines`, `msg str-replace`: preferred edit loop.
- `dialog xml`: compact context export when XML is easier to feed into another step.
- `raw`: escape hatch for unsupported routes.

## Guardrails

- Prefer `dialog find` before `msg read` when you do not already know the message id.
- Keep edits incremental; do not batch many unrelated changes into one command.
- Trust the returned `diff` after edit commands and the returned `output` after `msg exec`.
- Missing dialogs surface as `Dialog not found: <name>`.
- If you need completion for manual work, use `completion-sic --install`.
