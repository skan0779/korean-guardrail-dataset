<p align="center">
  <img src="/docs/icons/guardrail.svg" width="100%"/>
</p>

<h1 align="center">Korean Guardrail Dataset</h1>

<p align="center">
  AI Agent 서비스에서 <strong>가드레일(Guardrail)<strong>을 학습·평가·검증할 때 활용할 수 있는 한국어 데이터셋·벤치마크를 정리한 저장소입니다.
</p>

> ⚠️ 주의: 본 저장소에 링크된 데이터셋·벤치마크에는 **혐오·욕설·성적·폭력·불법행위·프롬프트 인젝션** 등 유해 콘텐츠가 포함될 수 있습니다. 연구·보안·안전 목적 외 사용을 금합니다.

---

## 1. Guardrails
> OpenAI가 공개한 [“A practical guide to building agents”](https://github.com/skan0779/korean-guardrail-dataset/blob/main/docs/papers/a-practical-guide-to-building-agents.pdf)(2025-04-17)의 **Guardrails** 섹션에서 제시한 구성요소를 기준으로 AI Agent 서비스에서의 Guardrail 기능을 분류하였습니다.

| Types | Examples |
|---|---|
| **Relevance classifier** | Off-topic queries |
| **Safety classifier** | Jailbreaks, Prompt injections |
| **PII filter** | Personally identifiable information |
| **Moderation** | Hate speech, Harassment, Violence |
| **Tool safeguards** | High-risk functions |
| **Rules-based protections** | Blocklists, Input length limits, Regex filters |
| **Output validation** | Response validity |

---

## 2. Datasets (KR)
> ⚠️ 각 데이터셋에 적용된 **License**를 반드시 확인 후 활용해 주세요.

| Types | Language | Source | Detail | Records | License |
|---|---|---|---|---|---|
| Rules-based protections | ko-KR | [league-of-legends_filtering_list_2020](https://github.com/skan0779/korean-guardrail-dataset/blob/main/data/league-of-legends_filtering_list_2020.txt) | 한국어 금칙어 리스트 (리그오브레전드) | 3,272 | Unknown |
| Rules-based protections | ko-KR | [slang](https://github.com/skan0779/korean-guardrail-dataset/blob/main/data/slang.csv) | 한국어 금칙어 리스트 | 4,241 | Unknown |
| PII filter | ko-KR | [KDPII DATASET REVISED](https://zenodo.org/records/16759166) | 한국어 PII 비식별화 데이터셋 (대화 기반) | 4,981 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| Moderation | ko-KR | [kocohub/korean-hate-speech](https://github.com/kocohub/korean-hate-speech) | 한국어 혐오표현 데이터셋 (연예 뉴스 댓글 기반) | 9,381 | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) |
| Moderation | ko-KR | [jason9693/APEACH](https://github.com/jason9693/APEACH) | 한국어 혐오표현 벤치마크 (탐지 평가용 크라우드 생성) | 3,770 | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) |
| Moderation | ko-KR | [smilegate-ai/korean_unsmile_dataset](https://github.com/smilegate-ai/korean_unsmile_dataset) | 한국어 혐오표현 데이터셋 (Smilegate AI) | 18,742 | [CC-BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/) |
| Moderation | ko-KR | [sgunderscore/hatescore-korean-hate-speech](https://github.com/sgunderscore/hatescore-korean-hate-speech) | 한국어 혐오표현 데이터셋 (Wikipedia, Smilegate AI) | 11,107 | [Apache-2.0 license](https://www.apache.org/licenses/LICENSE-2.0) |
| Moderation | ko-KR | [2runo/Curse-detection-data](https://github.com/2runo/Curse-detection-data) | 한국어 문장 욕설 여부 분류 데이터셋 | 5,825 | [MIT license](https://opensource.org/licenses/MIT) |
| Moderation | ko-KR | [boychaboy/KOLD](https://github.com/boychaboy/KOLD) | 한국어 Offensive Language 데이터셋 | 40,429 | Unlicensed |
| Moderation | ko-KR | [tunib-ai/DKTC](https://github.com/tunib-ai/DKTC) | 한국어 댓글/대화 분류 데이터(악성/비속어 포함 가능) | 3,949 | [CC-BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) |
| Moderation | ko-KR | [adlnlp/K-MHaS](https://github.com/adlnlp/K-MHaS) | 한국어 뉴스 댓글 멀티라벨 혐오표현 | 109,692 | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) |
| Moderation | ko-KR | [korean-hate-chat-data](https://www.kaggle.com/datasets/tanat05/korean-hate-chat-data) | 한국어 채팅 욕설 분류 데이터 | 14,879,941 | [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) |





|  |  | []() |  |  | []() |
|  |  | []() |  |  | []() |
|  |  | []() |  |  | []() |

---

## 3. Datasets (non-KR)
> 🌎 다국어로 된 원본 데이터셋을 한국어로 변환한 데이터셋 모음입니다. ⚠️ 원본 데이터셋에 적용된 **License**를 반드시 확인 후 활용해 주세요.

| Types | Main Source | Raw Source | Detail | Records | License |
|---|---|---|---|---|---|
| PII filter |  | [gretelai/synthetic_pii_finance_multilingual](https://huggingface.co/datasets/gretelai/synthetic_pii_finance_multilingual) | 금융 도메인 중심의 합성 PII 데이터셋 | 55,940 | Apache 2.0 |
| PII filter |  | [ai4privacy/pii-masking-400k](https://huggingface.co/datasets/ai4privacy/pii-masking-400k) | PII 마스킹/비식별 학습용 대규모 데이터셋 | 406,896 | licensing@ai4privacy.com |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

