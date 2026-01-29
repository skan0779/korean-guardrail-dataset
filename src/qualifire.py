import csv
import json
from pathlib import Path
from typing import Any, Dict

# ====== Folder Setting ======
REPO_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = REPO_ROOT / "data" / "raw" / "prompt-injections-benchmark" / "test.csv"
OUTPUT_PATH = REPO_ROOT / "data" / "processed" / "qualifire.jsonl"

# ====== Meta Setting ======
LICENSE = "cc-by-nc-4.0"
TYPE = "safety-classifier"
TOPIC = ["jailbreak"]

# =====` Main Function ======
def main() -> None:
    idx = 1
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with INPUT_PATH.open("r", encoding="utf-8", newline="") as rf, OUTPUT_PATH.open("w", encoding="utf-8") as wf:
        reader = csv.DictReader(rf)

        for row in reader:
            text = (row.get("text") or "").strip()
            label = (row.get("label") or "").strip().lower()
            if not text or label not in {"jailbreak", "benign"}:
                continue

            record: Dict[str, Any] = {
                "id": f"qualifire-{idx}",
                "query": text,
                "answer": [],
                "topic": TOPIC,
                "blocked": (label == "jailbreak"),
                "type": TYPE,
                "license": LICENSE,
            }
            wf.write(json.dumps(record, ensure_ascii=False) + "\n")
            idx += 1

    print(f"=== SUCCESS: {idx - 1} ===")

if __name__ == "__main__":
    main()
