# Pre-processing Scripts
> 원본 데이터 **data/raw**를 AI Agent 서비스 평가 및 검증용 데이터셋을 생성하는 스크립트입니다.

---
## KDPII.py
> KDPII 데이터셋을 읽어와서 가공 후 JSONL 형식으로 저장하는 스크립트.

- id: "kdpii-[i]"
- query: sentence[i].form
- answer: sentence[i].PNE[] (label이 PNE_LABEL에 포함되는 것만 남기고, 각 원소는 {form, label}만 유지)
- blocked: True/False (answer가 비어있으면 False, 아니면 True)
- type: "pii-filter"
- license: "cc-by-4.0"

---



