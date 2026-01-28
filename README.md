<p align="center">
  <img src="/docs/icons/guardrail.svg" width="100%"/>
</p>

<h1 align="center">Korean Guardrail Dataset</h1>

<p align="center">
  AI Agent 서비스에서 <strong>가드레일(Guardrail)<strong>을 학습·평가·검증할 때 활용할 수 있는 한국어 데이터셋·벤치마크를 정리한 저장소입니다.
</p>

> ⚠️ 주의: 본 저장소에 링크된 데이터셋·벤치마크에는 **혐오·욕설·성적·폭력·불법행위·프롬프트 인젝션** 등 유해 콘텐츠가 포함될 수 있습니다. 연구·보안·안전 목적 외 사용을 금합니다.


---


## 1. Guardrail Types
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


## 2. Datasets
> ⚠️ 각 데이터셋에 적용된 **License**들을 반드시 확인 후 활용해 주세요.

| Types | Language | Source | Detail | License |
|---|---|---|---|---|
| Rules-based protections | ko-KR | [league-of-legends_filtering_list_2020](https://github.com/skan0779/korean-guardrail-dataset/blob/main/datasets/league-of-legends_filtering_list_2020.txt) | 리그오브레전드 금칙어 리스트 | Unknown |



