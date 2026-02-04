# Scripts
> 원본 데이터 **data/raw**를 AI Agent 서비스 평가 및 검증용 데이터셋을 변역/생성/검증하는 스크립트입니다.

---
## translator.py
> 다국어 데이터셋을 한국어로 변환하여 데이터를 가공하는 스크립트.

- ✅ **Azure Translator** 리소스가 필요합니다.

--
## tester.py
> 데이터셋을 기반으로 guardrail endpoint에 요청 및 테스트 결과를 저장하는 스크립트.

- ✅ **Guardrail Service Endpoint**가 필요합니다. (각자 검증할 에이전트/모델의 endpoint로 변경해주세요)

---
## /processer
> 각 원본 데이터셋을 검증 및 테스트용으로 가공하여 JSONL 형식으로 저장하는 스크립트입니다.

- 각 원하는 형식으로 변경하여 활용하세요.
- 원본 데이터 중 용량이 큰 데이터는 직접 **source link** 를 통해서 다운로드 받아 **/raw** 폴더에 넣어 주세요.