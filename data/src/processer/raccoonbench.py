import json
from pathlib import Path
from typing import Any, Dict

# ====== Folder Setting ======
REPO_ROOT = Path(__file__).resolve().parents[2]
ATTACKS_PATH = REPO_ROOT / "data" / "raw" / "RaccoonBench" / "Data" / "attacks"
OUTPUT_PATH = REPO_ROOT / "data" / "processed" / "RaccoonBench.jsonl"

# ====== Meta Setting ======
LICENSE = "gpl-3.0-license"
TYPE = "safety-classifier"
TOPIC = ["prompt-injection"]

# ===== Main Function ======
def main() -> None:
    files = sorted([p for p in ATTACKS_PATH.rglob("*") if p.is_file() and p.name != ".DS_Store"])

    idx = 1
    with OUTPUT_PATH.open("w", encoding="utf-8") as wf:
        for fp in files:
            text = fp.read_text(encoding="utf-8").strip()
            if not text:
                continue

            record: Dict[str, Any] = {
                "id": f"raccoonbench-{idx}",
                "query": text,
                "answer": [],
                "topic": TOPIC,
                "blocked": True,
                "type": TYPE,
                "license": LICENSE,
            }
            wf.write(json.dumps(record, ensure_ascii=False) + "\n")
            idx += 1

    print(f"=== SUCCESS: {idx - 1} === -> {OUTPUT_PATH}")

if __name__ == "__main__":
    main()

