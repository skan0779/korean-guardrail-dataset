import json
from pathlib import Path
from typing import Any, Dict, List

# ====== Folder Setting ======
REPO_ROOT = Path(__file__).resolve().parents[1]
INPUT_TRAIN_PATH = REPO_ROOT / "data" / "raw" / "K-MHaS" / "kmhas_train.txt"
INPUT_VALID_PATH = REPO_ROOT / "data" / "raw" / "K-MHaS" / "kmhas_valid.txt"
INPUT_TEST_PATH  = REPO_ROOT / "data" / "raw" / "K-MHaS" / "kmhas_test.txt"
OUTPUT_PATH = REPO_ROOT / "data" / "processed" / "KMHaS.jsonl"

# ====== Meta Setting ======
LICENSE = "cc-by-sa-4.0"
TYPE = "moderation"

# ====== Label Mapping ======
LABEL_TEXT_MAP = {
    0: "출신차별",
    1: "외모차별",
    2: "정치성향차별",
    3: "혐오욕설",
    4: "연령차별",
    5: "성차별",
    6: "인종차별",
    7: "종교차별",
    8: "비혐오",  # topic에서 제외
}
NOT_HATE_ID = 8

# ====== Helpers ======
def parse_labels(label_str: str) -> List[int]:
    """예: '8', '2,3' -> [8], [2,3]"""
    s = label_str.strip()
    if not s:
        return []
    return [int(x.strip()) for x in s.split(",") if x.strip().isdigit()]

def labels_to_topic(labels: List[int]) -> List[str]:
    """8 제외 + 한글 매핑 + 중복 제거"""
    topics: List[str] = []
    for lb in labels:
        if lb == NOT_HATE_ID:
            continue
        topics.append(LABEL_TEXT_MAP.get(lb, str(lb)))
    return list(dict.fromkeys(topics))

def is_blocked(labels: List[int]) -> bool:
    """label==8만 있으면 False, 그 외 True"""
    return any(lb != NOT_HATE_ID for lb in labels)

def convert_file(in_path: Path, wf, idx_start: int) -> int:
    if not in_path.exists():
        raise FileNotFoundError(f"Input file not found: {in_path}")

    idx = idx_start
    with in_path.open("r", encoding="utf-8") as rf:
        header = rf.readline()

        for line in rf:
            line = line.rstrip("\n")
            if not line.strip():

                continue

            if "\t" not in line:
                continue

            document, label_str = line.split("\t", 1)
            query = document.strip().strip('"')
            labels = parse_labels(label_str)
            
            record: Dict[str, Any] = {
                "id": f"kmhas-{idx}",
                "query": query,
                "answer": [],
                "topic": labels_to_topic(labels),
                "blocked": is_blocked(labels),
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
    with OUTPUT_PATH.open("w", encoding="utf-8") as wf:
        idx = convert_file(INPUT_TRAIN_PATH, wf, idx)
        idx = convert_file(INPUT_VALID_PATH, wf, idx)
        idx = convert_file(INPUT_TEST_PATH, wf, idx)

    print(f"=== SUCCESS: {idx - 1} === -> {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
