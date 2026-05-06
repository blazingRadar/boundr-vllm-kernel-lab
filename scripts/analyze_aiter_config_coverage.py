#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AITER = ROOT / "workspaces" / "aiter"
MODEL_SHAPES = (
    AITER
    / "op_tests"
    / "op_benchmarks"
    / "triton"
    / "model_benchmarking_tool"
    / "model_shapes.json"
)
MODEL_CONFIGS = AITER / "aiter" / "configs" / "model_configs"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open() as f:
        return list(csv.DictReader(f))


def summarize_csv(path: Path) -> dict[str, object]:
    rows = read_csv_rows(path)
    dims = set()
    for r in rows:
        if {"M", "N", "K"}.issubset(r):
            dims.add((r["M"], r["N"], r["K"]))
        elif {"token", "model_dim", "inter_dim"}.issubset(r):
            dims.add((r["token"], r["model_dim"], r["inter_dim"]))
    return {
        "rows": len(rows),
        "unique_dim_tuples": len(dims),
        "sample_dim_tuples": list(sorted(dims))[:8],
    }


def main() -> None:
    model_shapes = json.loads(MODEL_SHAPES.read_text())

    targets = {
        "DeepSeek-R1": "deepseek_r1",
        "Qwen3-235B-A22B": "qwen3_235b",
    }

    print("# AITER Coverage Summary")
    print()
    print("## Model-shape inventory")
    for display_name in targets:
        shape = model_shapes.get(display_name, {})
        print(f"- {display_name}:")
        for op_name, entries in shape.items():
            print(f"  - {op_name}: {len(entries)} shapes")

    print()
    print("## Tuned model-config CSV inventory")
    for path in sorted(MODEL_CONFIGS.glob("*.csv")):
        summary = summarize_csv(path)
        print(
            f"- {path.name}: rows={summary['rows']} unique_dim_tuples={summary['unique_dim_tuples']}"
        )

    print()
    print("## Family buckets")
    family = defaultdict(list)
    for path in sorted(MODEL_CONFIGS.glob("*.csv")):
        name = path.name.lower()
        if "dsv3" in name or "ds_v3" in name or "deepseek" in name:
            family["deepseek"].append(path.name)
        elif "kimik2" in name or "kimi" in name:
            family["kimi"].append(path.name)
        elif "qwen" in name:
            family["qwen"].append(path.name)
        else:
            family["other"].append(path.name)
    for fam, files in sorted(family.items()):
        print(f"- {fam}: {len(files)} files")
        for name in files[:10]:
            print(f"  - {name}")


if __name__ == "__main__":
    main()
