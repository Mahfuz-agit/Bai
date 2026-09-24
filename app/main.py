from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.core.pipeline import CognitivePipeline
from app.providers.mock import MockProvider
from app.schemas.contracts import InputCase


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="output/result.json")
    args = parser.parse_args()

    case = InputCase.model_validate_json(Path(args.input).read_text(encoding="utf-8"))
    result = CognitivePipeline(provider=MockProvider()).run(case)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(result.model_dump_json(indent=2), encoding="utf-8")
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
