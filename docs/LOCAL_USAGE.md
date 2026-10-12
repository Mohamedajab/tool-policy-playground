# Local usage and testing

Run these commands from the repository root with Python 3.11 or newer.
The evaluator uses the standard library and does not need a model provider,
API key or network service. `pytest` is the only dependency needed for tests.

## Set up and test

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install pytest
.\.venv\Scripts\python.exe -m pytest
```

macOS or Linux:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install pytest
.venv/bin/python -m pytest
```

No package installation or editable install is necessary to run the script
from this checkout. If the environment is not activated, substitute its Python
path for `python` below.

## Run the supplied example

```bash
python tool_policy.py examples/policy.json examples/requests.jsonl
```

The program writes one JSON decision per request to standard output:

```json
{"request_id": "r1", "decision": "allow", "rule_id": "read-project-docs", "reason": "explicit rule"}
{"request_id": "r2", "decision": "deny", "rule_id": "block-private", "reason": "explicit rule"}
{"request_id": "r3", "decision": "deny", "rule_id": null, "reason": "default deny"}
```

The second request overlaps both an allow and a deny; the explicit deny wins.
The third matches no rule. The evaluator reports decisions only: it does not
read the requested document, send mail or execute a tool.

## Use the CLI in another script

Use `python tool_policy.py --help` to inspect the two positional paths.
A successful evaluation exits with status 0 **even if requests were denied**.
Do not use process success as permission to execute a requested action. Read
each JSON record's `decision` and keep enforcement in the caller.

Malformed request lines stop processing with a nonzero exit status and a line
number. Earlier decisions may already have been printed, so partial output is
not evidence that the entire input was processed successfully. Invalid policy
files or missing files also fail rather than producing a complete decision set.

## Troubleshooting

- **File not found:** check the working directory; the example paths are relative
  to the repository root.
- **Request validation failure:** provide string `action` and `resource` fields,
  and one complete JSON object per line. Blank lines are not ignored.
- **Unexpected default deny:** action and resource matching is case-sensitive;
  both patterns must match. Compare your request to the supplied examples.
- **Unexpected rule selection:** explicit denies override allows. Within each
  effect, the first matching rule in the list is selected.

The [existing security-model guide](SECURITY_MODEL.md) documents the full
contract and limitations. This example is not a production authorisation engine.
