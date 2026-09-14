"""Validate RECOVERY.md frontmatter against the Agent Recovery JSON Schema."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema
import yaml


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "recovery-plan.schema.json"


def load_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("file must begin with YAML frontmatter")
    try:
        frontmatter = text.split("---\n", 2)[1]
    except IndexError as exc:
        raise ValueError("frontmatter must end with ---") from exc
    data = yaml.safe_load(frontmatter)
    if not isinstance(data, dict):
        raise ValueError("frontmatter must contain a YAML mapping")
    return data


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    plans = sorted((ROOT / "examples").glob("*/RECOVERY.md"))
    failures = 0

    for plan in plans:
        try:
            jsonschema.Draft202012Validator(schema).validate(load_frontmatter(plan))
            print(f"PASS {plan.relative_to(ROOT)}")
        except (ValueError, yaml.YAMLError, jsonschema.ValidationError) as exc:
            failures += 1
            print(f"FAIL {plan.relative_to(ROOT)}: {exc.message if hasattr(exc, 'message') else exc}")

    if not plans:
        print("FAIL no RECOVERY.md examples found")
        return 1

    print(f"\n{len(plans) - failures}/{len(plans)} plans valid")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
