"""Evaluate simple default-deny tool rules and explain each decision."""
from __future__ import annotations

import argparse
import fnmatch
import json
from pathlib import Path


def load_json(path: Path):
    return json.loads(path.read_text("utf-8"))


def validate_policy(policy: dict) -> None:
    if policy.get("default") != "deny" or not isinstance(policy.get("rules"), list):
        raise ValueError("policy needs default=deny and a rules list")
    for rule in policy["rules"]:
        if rule.get("effect") not in {"allow", "deny"}:
            raise ValueError("rule effect must be allow or deny")
        if not all(isinstance(rule.get(key), str) for key in ("id", "action", "resource")):
            raise ValueError("rules need string id, action and resource")


def decide(policy: dict, request: dict) -> dict:
    validate_policy(policy)
    action, resource = request.get("action"), request.get("resource")
    if not isinstance(action, str) or not isinstance(resource, str):
        raise ValueError("request needs string action and resource")
    matches = [rule for rule in policy["rules"]
               if fnmatch.fnmatchcase(action, rule["action"])
               and fnmatch.fnmatchcase(resource, rule["resource"])]
    denies = [rule for rule in matches if rule["effect"] == "deny"]
    allows = [rule for rule in matches if rule["effect"] == "allow"]
    chosen = denies[0] if denies else (allows[0] if allows else None)
    return {"request_id": request.get("request_id"),
            "decision": chosen["effect"] if chosen else "deny",
            "rule_id": chosen["id"] if chosen else None,
            "reason": "explicit rule" if chosen else "default deny"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("policy", type=Path)
    parser.add_argument("requests", type=Path, help="one JSON request per line")
    args = parser.parse_args()
    policy = load_json(args.policy)
    for number, line in enumerate(args.requests.read_text("utf-8").splitlines(), 1):
        try:
            request = json.loads(line)
            print(json.dumps(decide(policy, request)))
        except (json.JSONDecodeError, ValueError) as error:
            raise SystemExit(f"line {number}: {error}") from error
