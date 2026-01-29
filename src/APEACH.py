import json
from pathlib import Path
from typing import Any, Dict
import csv

# ====== Folder Setting ======
REPO_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = REPO_ROOT / "data" / "raw" / "APEACH" / "APEACH-dataset.tsv"
OUTPUT_PATH = REPO_ROOT / "data" / "processed" / "APEACH.jsonl"

# ====== Label / Meta Setting ======
LICENSE = "cc-by-sa-4.0"
TYPE = "moderation"


# ====== Helper Function ======
def class_to_blocked(cls: Any) -> bool:
    """Default -> False, Spoiled -> True"""
    c = str(cls).strip().lower()
    if c == "default":
        return False
    if c == "spoiled":
        return True
    return False

# ====== Main Code ======
def main() -> None:
    in_path = Path(INPUT_PATH)
    out_path = Path(OUTPUT_PATH)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if not in_path.exists():
        raise FileNotFoundError(f"Input file not found: {in_path}")

    idx = 1
    written = 0

    with in_path.open("r", encoding="utf-8", newline="") as rf, out_path.open("w", encoding="utf-8") as wf:
        reader = csv.DictReader(rf, delimiter="\t")
        required_cols = {"text", "text_topic_eng", "class"}
        missing = required_cols - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing required columns in CSV: {sorted(missing)}. Found: {reader.fieldnames}")

        for row in reader:
            query = (row.get("text") or "").strip()
            topic = (row.get("text_topic_eng") or "").strip()
            cls = row.get("class")

            record: Dict[str, Any] = {
                "id": f"apeach-{idx}",
                "query": query,
                "answer": [],
                "topic": topic,
                "blocked": class_to_blocked(cls),
                "type": TYPE,
                "license": LICENSE,
            }

            wf.write(json.dumps(record, ensure_ascii=False) + "\n")
            idx += 1
            written += 1

    print(f"=== SUCCESS: {written} ===")

if __name__ == "__main__":
    main()
