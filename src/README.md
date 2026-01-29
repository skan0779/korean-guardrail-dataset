# Pre-processing Scripts
> 원본 데이터 **data/raw**를 AI Agent 서비스 평가 및 검증용 데이터셋을 생성하는 스크립트입니다.

---
## KDPII.py
> KDPII 데이터셋을 읽어와서 가공 후 JSONL 형식으로 저장하는 스크립트.

- id: "kdpii-[i]"
- query: "text" (sentence[i].form 값)
- answer: [{"form":"", "label":""}] (sentence[i].PNE[] 값: label이 PNE_LABEL에 포함되는 것만 남기고, 각 원소는 {form, label}만 유지)
- topic: []
- blocked: True/False (answer가 비어있으면 False, 아니면 True)
- type: "pii-filter"
- license: "cc-by-4.0"

---
## APEACH.py
> APEACH 데이터셋을 읽어와서 가공 후 JSONL 형식으로 저장하는 스크립트.

- id: "apeach-[i]"
- query: "text"
- answer: []
- topic: [""] ("text_topic_eng" 값)
- blocked: True/False (class == "Spoiled" 이면 True, "Default"면 False)
- type: "moderation"
- license: "cc-by-sa-4.0"

---
## KOLD.py
> KOLD 데이터셋을 읽어와서 가공 후 JSONL 형식으로 저장하는 스크립트.

- id: "kold-[i]"
- query: "comment"
- answer: [{"form":""}] ("OFF_span" 값)
- topic: []
- blocked: True/False ("OFF" 값)
- type: "moderation"
- license: "unknown"

---
## UNSIMILE.py
> korean-unsmile-dataset 데이터셋을 읽어와서 가공 후 JSONL 형식으로 저장하는 스크립트.

- id: "unsmile-[i]"
- query: "" ("문장" 값)
- answer: []
- topic: [""] (라벨 리스트)
- blocked: True/False ("clean"==1 이면 False, 그 외 True)
- type: "moderation"
- license: "cc-by-nc-nd-4.0"

---
## KMHaS.py
> K-MHaS 데이터셋을 읽어와서 가공 후 JSONL 형식으로 저장하는 스크립트.

- id: "kmhas-[i]"
- query: "" ("document" 값)
- answer: []
- topic: [""] ("label" 값 리스트, 단 "label"==8 제외)
- blocked: True/False ("label"==8 이면 False, 그 외 True)
- type: "moderation"
- license: "cc-by-sa-4.0"

---
## LoL.py
> league-of-legends_filtering_list 파일 금칙어들을 JSONL 형식으로 저장하는 스크립트.

- id: "lol-[i]"
- query: "" ("text" 값)
- answer: []
- topic: ["욕설"]
- blocked: True
- type: "rules-based-protections"
- license: "unknown"

---
## slang.py
> slang 파일 금칙어들을 JSONL 형식으로 저장하는 스크립트.

- id: "slang-[i]"
- query: "" ("text" 값)
- answer: []
- topic: ["욕설"]
- blocked: True
- type: "rules-based-protections"
- license: "unknown"

---
## salesforce-prompt-leakage.jsonl.py
> salesforce/prompt-leakage 데이터셋을 읽어와서 가공 후 JSONL 형식으로 저장하는 스크립트.

- id: "salesforce-[i]"
- query: "" ("text" 값)
- answer: []
- topic: ["욕설"]
- blocked: True
- type: "rules-based-protections"
- license: "unknown"

