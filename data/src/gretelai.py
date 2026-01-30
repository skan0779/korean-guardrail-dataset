import json
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

# ====== Folder Setting ======
REPO_ROOT = Path(__file__).resolve().parents[1]
TRAIN_PATH = REPO_ROOT / "data" / "raw" / "synthetic_pii_finance_multilingual" / "train-00000-of-00001.parquet"
TEST_PATH  = REPO_ROOT / "data" / "raw" / "synthetic_pii_finance_multilingual" / "test-00000-of-00001.parquet"
OUTPUT_PATH = REPO_ROOT / "data" / "processed" / "gretelai.jsonl"

# ====== Meta Setting ======
LICENSE = "apache-2.0-license"
TYPE = "pii-filter"

# ====== Helper Functions ======
def ensure_spans(v: Any) -> List[Dict[str, Any]]:
    if v is None:
        return []
    if isinstance(v, list):
        return [x for x in v if isinstance(x, dict)]
    if isinstance(v, str):
        s = v.strip()
        if not s:
            return []
        try:
            p = json.loads(s)
            return [x for x in p if isinstance(x, dict)] if isinstance(p, list) else []
        except json.JSONDecodeError:
            return []
    return []

def iter_records(parquet_path: Path):
    df = pd.read_parquet(parquet_path)
    if "generated_text" not in df.columns or "pii_spans" not in df.columns:
        raise ValueError(f"Missing required columns in {parquet_path.name}: {list(df.columns)}")
    for _, row in df.iterrows():
        text = row.get("generated_text")
        if not isinstance(text, str) or not text.strip():
            continue

        spans = ensure_spans(row.get("pii_spans"))
        answer: List[Dict[str, str]] = []

        for sp in spans:
            start, end, label = sp.get("start"), sp.get("end"), sp.get("label")
            if not isinstance(start, int) or not isinstance(end, int) or not isinstance(label, str):
                continue
            if start < 0 or end > len(text) or start >= end:
                continue
            span_text = text[start:end]
            if span_text:
                answer.append({"form": span_text, "label": label})

        if answer:
            yield text, answer

# ====== Main Function ======
def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    idx = 1
    written = 0

    with OUTPUT_PATH.open("w", encoding="utf-8") as wf:
        for p in [TRAIN_PATH, TEST_PATH]:
            if not p.exists():
                continue

            for text, answer in iter_records(p):
                record: Dict[str, Any] = {
                    "id": f"gretelai-{idx}",
                    "query": text,
                    "answer": answer,
                    "topic": [],
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
