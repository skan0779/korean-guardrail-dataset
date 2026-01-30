import csv
import json
from pathlib import Path
from typing import Any, Dict

# ====== Folder Setting ======
REPO_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = REPO_ROOT / "data" / "raw" / "llm-red-teaming-dataset" / "redteam_master_dataset.csv"
OUTPUT_PATH = REPO_ROOT / "data" / "processed" / "navirocker.jsonl"

# ====== Meta Setting ======
LICENSE = "mit-license"
CATEGORY_TO_TYPE = {
    "harmful_content": "safety-classifier",
    "misinformation": "output-validation",
    "privacy_violations": "pii-filter",
    "jailbreaking": "safety-classifier",
    "bias_stereotypes": "moderation",
    "illegal_activities": "safety-classifier",
    "sexual_content": "moderation",
    "manipulation": "safety-classifier",
}

# ====== Main Function ======
def main() -> None:
    out_path = Path(OUTPUT_PATH)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    idx = 1

    with Path(INPUT_PATH).open("r", encoding="utf-8", newline="") as rf, out_path.open("w", encoding="utf-8") as wf:
        reader = csv.DictReader(rf)

        for row in reader:
            prompt = (row.get("prompt") or "").strip()
            category = (row.get("category") or "").strip()

            if not prompt or not category:
                continue

            record_type = CATEGORY_TO_TYPE.get(category, "safety-classifier")

            record: Dict[str, Any] = {
                "id": f"navirocker-{idx}",
                "query": prompt,
                "answer": [],
                "topic": [category],
                "blocked": True,
                "type": record_type,
                "license": LICENSE,
            }

            wf.write(json.dumps(record, ensure_ascii=False) + "\n")
            idx += 1

    print(f"=== SUCCESS: {idx - 1} ===")

if __name__ == "__main__":
    main()
