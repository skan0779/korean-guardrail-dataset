import json
from pathlib import Path
from typing import Any, Dict
import csv

# ====== Folder Setting ======
REPO_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = REPO_ROOT / "data" / "raw" / "slang.csv"
OUTPUT_PATH = REPO_ROOT / "data" / "processed" / "slang.jsonl"

# ====== Meta Setting ======
LICENSE = "unknown"
TYPE = "rules-based-protections"

# ====== Main Function ======
def main() -> None:
    in_path = Path(INPUT_PATH)
    out_path = Path(OUTPUT_PATH)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if not in_path.exists():
        raise FileNotFoundError(f"Input file not found: {in_path}")

    idx = 1
    written = 0

    with in_path.open("r", encoding="utf-8", newline="") as rf, out_path.open("w", encoding="utf-8") as wf:
        reader = csv.reader(rf)
        header_skipped = False

        for row in reader:
            if not row:
                continue

            if not header_skipped:
                header_skipped = True
                continue

            text = (row[0] or "").strip()
            if not text:
                continue

            record: Dict[str, Any] = {
                "id": f"slang-{idx}",
                "query": text,
                "answer": [],
                "topic": ["욕설"],
                "blocked": True,
                "type": TYPE,
                "license": LICENSE,
            }

            wf.write(json.dumps(record, ensure_ascii=False) + "\n")
            idx += 1
            written += 1

    print(f"=== SUCCESS: {written} ===")

if __name__ == "__main__":
    main()
