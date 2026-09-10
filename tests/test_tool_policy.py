import pytest
from tool_policy import decide, validate_policy

POLICY = {"default": "deny", "rules": [
    {"id": "read-docs", "effect": "allow", "action": "document:read", "resource": "docs/*"},
    {"id": "protect-private", "effect": "deny", "action": "*", "resource": "docs/private/*"},
]}


def test_matching_allow_rule():
    result = decide(POLICY, {"request_id": "1", "action": "document:read", "resource": "docs/guide.txt"})
    assert result["decision"] == "allow"
    assert result["rule_id"] == "read-docs"


def test_explicit_deny_wins():
    result = decide(POLICY, {"action": "document:read", "resource": "docs/private/notes.txt"})
    assert result["decision"] == "deny"
    assert result["rule_id"] == "protect-private"


def test_unmatched_request_is_denied():
    assert decide(POLICY, {"action": "email:send", "resource": "mail/a"})["reason"] == "default deny"


def test_invalid_policy_is_rejected():
    with pytest.raises(ValueError, match="default=deny"):
        validate_policy({"default": "allow", "rules": []})
