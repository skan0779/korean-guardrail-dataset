import json
from pathlib import Path
from typing import Any, Dict, List

# ====== Folder Setting ======
REPO_ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = REPO_ROOT / "data" / "raw" / "KOLD" / "kold_v1.json"
OUTPUT_PATH = REPO_ROOT / "data" / "processed" / "KOLD.jsonl"

# ====== Meta Setting ======
LICENSE = "unknown"
TYPE = "moderation"

# ====== Helper Function ======
def build_answer(off_span: Any) -> List[Dict[str, str]]:
    """answer: [{"form": "<OFF_span>"}]"""
    span = "" if off_span is None else str(off_span).strip()
    return [{"form": span}] if span else []

# ====== Main Code ======
def main() -> None:
    in_path = Path(INPUT_PATH)
    out_path = Path(OUTPUT_PATH)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if not in_path.exists():
        raise FileNotFoundError(f"Input file not found: {in_path}")

    with in_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Unexpected JSON structure: top-level should be a list.")

    idx = 1
    written = 0

    with out_path.open("w", encoding="utf-8") as wf:
        for row in data:
            if not isinstance(row, dict):
                continue

            query = row.get("comment", "")
            blocked = row.get("OFF", False)
            answer = build_answer(row.get("OFF_span", "")) if blocked else []

            record: Dict[str, Any] = {
                "id": f"kold-{idx}",
                "query": query,
                "answer": answer,
                "topic": [],
                "blocked": blocked,
                "type": TYPE,
                "license": LICENSE,
            }

            wf.write(json.dumps(record, ensure_ascii=False) + "\n")
            idx += 1
            written += 1

    print(f"=== SUCCESS: {written} ===")

if __name__ == "__main__":
    main()
