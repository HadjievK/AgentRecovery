"""Validate RECOVERY.yaml files against schema and core safety invariants."""

from __future__ import annotations

import json
import sys
from collections import deque
from pathlib import Path
from typing import Any, Iterable

import jsonschema
import yaml


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "recovery-machine.schema.json"


def load_machine(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("document must contain a YAML mapping")
    return data


def as_transitions(value: Any) -> list[dict[str, Any]]:
    return value if isinstance(value, list) else [value]


def actions_in(state: dict[str, Any]) -> Iterable[dict[str, Any]]:
    yield from state.get("entry", [])
    for transition_set in state.get("on", {}).values():
        for transition in as_transitions(transition_set):
            yield from transition.get("actions", [])


def semantic_errors(machine: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    states = machine["states"]
    initial = machine["initial"]

    if initial not in states:
        errors.append(f"initial state {initial!r} does not exist")

    final_states = [name for name, state in states.items() if state.get("type") == "final"]
    if not final_states:
        errors.append("machine must declare at least one final state")

    graph: dict[str, set[str]] = {name: set() for name in states}
    for state_name, state in states.items():
        for event, transition_set in state.get("on", {}).items():
            transitions = as_transitions(transition_set)
            unguarded = [index for index, transition in enumerate(transitions) if "guard" not in transition]
            if len(unguarded) > 1:
                errors.append(f"{state_name}.{event} has more than one default transition")
            if unguarded and unguarded[-1] != len(transitions) - 1:
                errors.append(f"{state_name}.{event} default transition must be last")

            for transition in transitions:
                target = transition["target"]
                if target not in states:
                    errors.append(f"{state_name}.{event} targets missing state {target!r}")
                else:
                    graph[state_name].add(target)

        retry_actions = [action for action in actions_in(state) if action["kind"] == "retry"]
        if retry_actions and state["classification"] != "retry-safe":
            errors.append(f"{state_name} invokes retry but is not classified retry-safe")
        if state["classification"] == "unknown" and retry_actions:
            errors.append(f"{state_name} retries directly from unknown state")

    if initial in states:
        reachable: set[str] = set()
        queue = deque([initial])
        while queue:
            state_name = queue.popleft()
            if state_name in reachable:
                continue
            reachable.add(state_name)
            queue.extend(graph[state_name] - reachable)
        for state_name in sorted(set(states) - reachable):
            errors.append(f"state {state_name!r} is unreachable from initial state")

    return errors


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator_class = jsonschema.validators.validator_for(schema)
    validator_class.check_schema(schema)
    validator = validator_class(schema)
    machines = sorted((ROOT / "examples").glob("*/RECOVERY.yaml"))
    failures = 0

    for path in machines:
        try:
            machine = load_machine(path)
            validator.validate(machine)
            errors = semantic_errors(machine)
            if errors:
                raise ValueError("; ".join(errors))
            print(f"PASS {path.relative_to(ROOT)}")
        except (ValueError, yaml.YAMLError, jsonschema.ValidationError) as exc:
            failures += 1
            message = exc.message if hasattr(exc, "message") else str(exc)
            print(f"FAIL {path.relative_to(ROOT)}: {message}")

    if not machines:
        print("FAIL no RECOVERY.yaml examples found")
        return 1

    print(f"\n{len(machines) - failures}/{len(machines)} machines valid")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
