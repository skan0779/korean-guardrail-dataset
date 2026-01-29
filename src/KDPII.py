import json
from pathlib import Path
from typing import Any, Dict, List

# ====== 전역 설정 ======
REPO_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = REPO_ROOT / "data" / "raw" / "KDPII DATASET REVISED" / "PII_dataset_V3.json"
OUTPUT_PATH = REPO_ROOT / "data" / "processed" / "KDPII.jsonl"

# ====== 개인 설정 ======
LICENSE = "cc-by-4.0"
TYPE = "pii-filter"
PNE_LABEL = [
    # 개인 식별 정보
    "PS_NAME", # 성명
    "PS_NICKNAME", # 별명/닉네임
    "PS_ID", # 개인 식별자(아이디/핸들 등)

    # 생체/신체 정보
    "DT_BIRTH", # 생년월일
    "QT_AGE", # 나이
    "CV_SEX", # 성별
    "QT_LENGTH", # 신장
    "QT_WEIGHT", # 체중
    "TM_BLOOD_TYPE", # 혈액형

    # 위치 정보
    "LCP_COUNTRY", # 국가
    "LC_ADDRESS", # 주소
    "LC_PLACE", # 장소

    # 연락처 정보
    "QT_MOBILE", # 휴대폰번호
    "QT_PHONE", # 전화번호
    "TMI_EMAIL", # 이메일

    # 식별 번호
    "QT_RESIDENT_NUMBER", # 주민등록번호
    "QT_ALIEN_NUMBER", # 외국인등록번호
    "QT_PASSPORT_NUMBER", # 여권번호
    "QT_DRIVER_NUMBER", # 운전면허번호
    "QT_CARD_NUMBER", # 카드번호
    "QT_ACCOUNT_NUMBER", # 계좌번호
    "QT_PLATE_NUMBER", # 차량번호

    # 직업/교육 정보
    "OG_WORKPLACE", # 직장
    "OG_DEPARTMENT", # 부서
    "CV_POSITION", # 직위
    "OGG_EDUCATION", # 학력
    "QT_GRADE", # 성적
    "FD_MAJOR", # 전공

    # 기타 정보
    "OGG_RELIGION", # 종교
    "OGG_CLUB", # 단체/클럽
    "TMI_SITE", # 웹사이트(URL)
    "QT_IP", # IP주소
    "CV_MILITARY_CAMP", # 병역
]



                                               
# ====== 메인 코드 ======
def filter_pne(pne_list: List[Dict[str, Any]], allowed_labels: List[str]) -> List[Dict[str, str]]:
    """PNE에서 allowed_labels에 해당하는 항목만 남기고, form/label만 추출."""
    out: List[Dict[str, str]] = []
    for pne in pne_list or []:
        label = pne.get("label")
        if label in allowed_labels:
            form = pne.get("form")
            if form is not None and label is not None:
                out.append({"form": str(form), "label": str(label)})
    return out


def main() -> None:
    in_path = Path(INPUT_PATH)
    out_path = Path(OUTPUT_PATH)

    if not in_path.exists():
        raise FileNotFoundError(f"Input file not found: {in_path}")

    with in_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    idx = 1
    written = 0

    with out_path.open("w", encoding="utf-8") as wf:
        for dialog in data:
            sentences = dialog.get("sentence", [])
            if not isinstance(sentences, list):
                continue

            for sent in sentences:
                query = sent.get("form", "")
                pne = sent.get("PNE", [])

                answer = filter_pne(pne, PNE_LABEL)
                blocked = bool(answer)

                record = {
                    "id": f"kdpii-{idx}",
                    "query": query,
                    "answer": answer,
                    "blocked": blocked,
                    "type": TYPE,
                    "license": LICENSE,
                }

                wf.write(json.dumps(record, ensure_ascii=False) + "\n")
                idx += 1
                written += 1

    print(f"Done. Wrote {written} lines to: {out_path}")


if __name__ == "__main__":
    main()