---
description: Use the solveit_client CLI (`sic`) to interact with SolveIt dialogs, messages, and the API client from the command line or scripts. Trigger when working with SolveIt automation, dialog management, or message manipulation outside of Python.
---

# solveit_client CLI (`sic`)

A CLI that maps directly to the `solveit_client` Python API. Every operation follows the pattern:

```bash
sic <namespace>.<method> [positional_args] [--kwarg value]
```

## Namespaces

| Namespace | Object | Required flags |
|-----------|--------|----------------|
| `client` | `SolveItClient` | (none beyond auth) |
| `dialog` | `Dialog` | `--name` or `SOLVEIT_DIALOG` |
| `message` | `Message` | `--name` + `--id` |

## Auth & env vars

Flags can be omitted if the corresponding env var is set:

| Flag | Env var | Purpose |
|------|---------|---------|
| `--url` | `SOLVEIT_URL` | Server URL (default: `http://localhost:5001`) |
| `--token` | `SOLVEIT_TOKEN` | Auth token (default: `dummy`, which works for localhost) |
| `--name` | `SOLVEIT_DIALOG` | Dialog name (for `dialog.*` and `message.*`) |

## Output

All command output is JSON (pipe to `jq` for formatting). Return types:

- **Dialog** → `{"name": "...", "mode": "..."}`
- **Message** → `{"id": "...", "msg_type": "...", "content": "...", "output": "..."}`
- **Messages** (list) → array of message objects
- **MsgDiff** (from update/replace ops) → message fields + `"diff": "..."`

## Message Types

Common `msg_type` values for `dialog.add_msg`:

- `code`: Python/code cells you want SolveIt to run. Add the message, then call `sic message.exec --name <dialog> --id <msg_id>` to execute it and populate `output`.
- `note`: Non-executable text for headings, instructions, scratch notes, or context you want saved in the dialog without being run.
- `prompt`: A request for SolveIt AI. Adding the message only creates the prompt cell; the AI does not answer until you explicitly run `sic message.exec --name <dialog> --id <msg_id>`.
- `raw`: Low-level/plain content when you want to avoid the usual code/note/prompt semantics.

Typical prompt flow:

```bash
sic dialog.add_msg 'Reply with a short hello.' --name myproject --msg_type prompt
sic message.exec --name myproject --id _abc123
```

Before `message.exec`, a prompt message may show a pending placeholder output. After `message.exec`, `output` contains the AI response.

## Help system

```bash
sic                          # list namespaces
sic dialog --help            # list all dialog methods
sic dialog.add_msg --help    # show method signature and param docs
```

## Examples

```bash
# Create a dialog
sic client.create_dialog --name myproject

# Add a note
sic dialog.add_msg 'Hello world' --name myproject --msg_type note

# List messages
sic dialog.messages --name myproject

# Execute a code cell
sic message.exec --name myproject --id _abc123

# Add a prompt, then execute it to get the AI response
sic dialog.add_msg 'Summarize this dialog so far.' --name myproject --msg_type prompt
sic message.exec --name myproject --id _prompt123

# Update message content
sic message.update --name myproject --id _abc123 --content 'new content'

# Delete a dialog
sic dialog.delete --name myproject

# With env vars set, much shorter:
export SOLVEIT_URL=http://localhost:6001
export SOLVEIT_TOKEN=mytoken
export SOLVEIT_DIALOG=myproject

sic dialog.add_msg '1+1'
sic dialog.messages
sic message.exec --id _abc123
```

## Gotchas

- `--help` are boolean flags (no value after them); all other `--flags` expect a value
- Properties like `dialog.messages` take no positional args — just namespace flags
- `message.*` operations always need both `--name` and `--id`
- `dialog.add_msg --msg_type prompt` does not itself trigger the AI; you must run `sic message.exec` on that prompt message to get a response
- Dialog names can contain `/` for folder structure (e.g. `myproject/notebooks/analysis`)
- The `--name` flag is consumed by object construction for `dialog.*`/`message.*`, but passed through as a method arg for `client.*` (e.g. `client.create_dialog --name foo`)
