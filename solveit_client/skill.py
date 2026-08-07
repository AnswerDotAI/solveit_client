r"""Drive SolveIt dialogs over HTTP from outside the instance: create dialogs, add and edit messages, and execute code and AI prompts. Use this to automate a SolveIt instance from a laptop, script, or agent session -- anywhere that isn't the dialog's own kernel (from inside a dialog, use dialoghelper instead).

## Connection and auth

`SolveItClient(url=None, token=None)` reads `SOLVEIT_URL` (default `http://localhost:5001`) and `SOLVEIT_TOKEN`. The token is the value of the `_solveit` session cookie, copied once from browser DevTools after logging in to SolveIt. The cookie is set on the parent domain and every instance you own accepts it, so one copy works for all your instances; the localhost default needs no token. The client is callable: `cli(path, **data)` POSTs form data to any server route and returns parsed JSON (or raw text), so routes without a wrapper method are still reachable.

## Core objects

- `SolveItClient.create_dialog(name)` is create-OR-open: the server creates the file only if missing, then loads the dialog and starts its kernel. Calling it on an existing dialog is the programmatic equivalent of opening it in the browser, and is the required first step for message work: the message routes only see dialogs currently open on the server.
- `Dialog`: `add_msg(content, msg_type='code', placement='at_end')` (types: code, note, prompt, raw), `messages`, `find_msgs(re_pattern)`, `read_msg(n|id)`, `to_xml()` (the dialog as one XML string, for LLM reading), `run_all()`, `stop()` (the kernel), `reset()`, `delete()`, and `link`.
- `Message`: `exec(timeout=30)` queues the message on the server's run queue and polls until done -- needed for code AND prompt messages alike (adding a prompt does not trigger the AI). `update(**fields)`, `delete()`, plus the line-edit family shared with the fastai editing toolkit: `str_replace`, `strs_replace`, `insert_line`, `replace_lines`, `del_lines`, and `num_content` for a line-numbered view.

`Dialog` and `Message` serve attribute access (`dlg.mode`, `msg.output`, ...) from a cached server snapshot; `exec` and the editors refresh it automatically.

## Things to know

- Dialog names are paths relative to the instance data root, `/`-separated for folders (`myproject/experiment`), no `.ipynb` extension.
- Message content and outputs are persisted into the dialog's .ipynb on the instance and visible to anyone with access to that dialog: don't embed secrets in messages.
- `exec` on a prompt message spends the instance's AI usage.
- The `sic` CLI exposes the same API from the shell (`sic dialog.add_msg '1+1' --name myproject`), reading the same env vars plus `SOLVEIT_DIALOG` for the default dialog.
"""

from solveit_client.core import *

__all__ = ['SolveItClient', 'Dialog', 'Message', 'Messages', 'MsgDiff']
