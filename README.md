# Tool Policy Playground

A small default-deny policy evaluator for understanding the host-side boundary
around tool-using agents. Rules match an action and resource; explicit deny
rules take precedence over allows.

```powershell
python tool_policy.py examples/policy.json examples/requests.jsonl
python -m pytest
```

The output records the selected rule or says `default deny`. This is a learning
project, not a production authorisation library. Glob patterns are easy to
misconfigure, rules use first-match order within the same effect, and there is
no identity, consent token, expiry or cryptographic authentication.

Main idea to explain: the model may request an action, but ordinary application
code makes the final decision. Deny-by-default limits what happens when a model
asks for an unknown tool or resource.

## Documentation

See [docs/SECURITY_MODEL.md](docs/SECURITY_MODEL.md) for the authorization flow,
matching and precedence rules, threat scenarios, limitations, production
hardening ideas and an interview walkthrough.
