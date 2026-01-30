import json
from pathlib import Path
from typing import Any, Dict

# ====== Folder Setting ======
REPO_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = REPO_ROOT / "data" / "raw" / "league-of-legends_filtering_list_2020.txt"
OUTPUT_PATH = REPO_ROOT / "data" / "processed" / "LoL.jsonl"

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

    with in_path.open("r", encoding="utf-8") as rf, out_path.open("w", encoding="utf-8") as wf:
        for line in rf:
            text = line.strip()
            if not text:
                continue

            record: Dict[str, Any] = {
                "id": f"lol-{idx}",
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
