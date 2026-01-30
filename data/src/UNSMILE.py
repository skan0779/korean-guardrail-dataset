import csv
import json
from pathlib import Path
from typing import Any, Dict, List

# ====== Folder Setting ======
REPO_ROOT = Path(__file__).resolve().parents[1]
TRAIN_INPUT_PATH = REPO_ROOT / "data" / "raw" / "korean_unsmile_dataset" / "unsmile_train_v1.0.tsv"
VALID_INPUT_PATH = REPO_ROOT / "data" / "raw" / "korean_unsmile_dataset" / "unsmile_valid_v1.0.tsv"
OUTPUT_PATH = REPO_ROOT / "data" / "processed" / "UNSMILE.jsonl"

# ====== Meta Setting ======
LICENSE = "cc-by-nc-nd-4.0"
TYPE = "moderation"

# ====== Column Setting ======
TEXT_COL = "문장"
CLEAN_COL = "clean"
LABEL_COLS = [
    "여성/가족",
    "남성",
    "성소수자",
    "인종/국적",
    "연령",
    "지역",
    "종교",
    "기타 혐오",
    "악플/욕설",
    "개인지칭",
]

# ====== Helper ======
def to_int01(x: Any) -> int:
    return 1 if str(x).strip() == "1" else 0

def extract_topics(row: Dict[str, Any]) -> List[str]:
    """각 라벨 컬럼이 1인 것만 리스트로 반환 (topic: [...])"""
    topics: List[str] = []
    for col in LABEL_COLS:
        if to_int01(row.get(col, 0)) == 1:
            topics.append(col)
    return topics

def convert_one_file(in_path: Path, wf, start_idx: int) -> int:
    """TSV 하나를 읽어서 wf(JSONL writer)에 쓰고, 마지막 idx 반환"""
    if not in_path.exists():
        raise FileNotFoundError(f"Input file not found: {in_path}")

    idx = start_idx
    with in_path.open("r", encoding="utf-8", newline="") as rf:
        reader = csv.DictReader(rf, delimiter="\t")

        required = {TEXT_COL, CLEAN_COL, *LABEL_COLS}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}\nFound: {reader.fieldnames}")

        for row in reader:
            query = (row.get(TEXT_COL) or "").strip()
            clean = to_int01(row.get(CLEAN_COL, 0))
            blocked = False if clean == 1 else True

            record = {
                "id": f"unsmile-{idx}",
                "query": query,
                "answer": [],
                "topic": extract_topics(row),
                "blocked": blocked,
                "type": TYPE,
                "license": LICENSE,
            }

            wf.write(json.dumps(record, ensure_ascii=False) + "\n")
            idx += 1

    return idx

# ====== Main ======
def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    idx = 1
    written = 0

    with OUTPUT_PATH.open("w", encoding="utf-8") as wf:
        before = idx
        idx = convert_one_file(TRAIN_INPUT_PATH, wf, idx)
        written += (idx - before)

        before = idx
        idx = convert_one_file(VALID_INPUT_PATH, wf, idx)
        written += (idx - before)

    print(f"=== SUCCESS: {written} ===")

if __name__ == "__main__":
    main()
