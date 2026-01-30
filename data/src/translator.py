import os, json
from pathlib import Path
import requests
from dotenv import load_dotenv

# ====== Folder Setting ======
REPO_ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = REPO_ROOT / "data" / "processed" / "qualifire.jsonl"
OUTPUT_PATH = REPO_ROOT / "data" / "processed" / "qualifire-kr.jsonl"

# ====== Range Setting ======
START = 4501
END = 5000

# ====== Translation Function ======
def translate_text(text: str, endpoint: str, key: str, region: str | None = None) -> str:
    url = f"{endpoint}/translate"
    params = {
        "api-version": "3.0",
        "to": "ko",
    }
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }
    if region:
        headers["Ocp-Apim-Subscription-Region"] = region

    body = [{"text": text}]
    r = requests.post(url, params=params, headers=headers, json=body, timeout=30)
    r.raise_for_status()
    data = r.json()
    return data[0]["translations"][0]["text"]

# ========= Main Function =========
def main():
    load_dotenv()

    t_key = os.environ.get("AZURE_TRANSLATOR_KEY")
    t_endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT")
    t_region = os.environ.get("AZURE_TRANSLATOR_REGION")

    file_mode = "a" if OUTPUT_PATH.exists() else "w"
    processed = 0
    translated_ok = 0
    failed = 0
    skipped = 0

    with open(INPUT_PATH, "r", encoding="utf-8") as fin, open(OUTPUT_PATH, file_mode, encoding="utf-8") as fout:
        for line_no, line in enumerate(fin, start=1):
            if line_no < START:
                continue
            if line_no > END:
                break

            line = line.rstrip("\n")
            if not line.strip():
                skipped += 1
                continue

            processed += 1

            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                failed += 1
                fout.write(json.dumps({"id": line_no, "error": f"json_parse_error: {e}"}, ensure_ascii=False) + "\n")
                continue

            q = obj.get("query")
            if isinstance(q, str) and q.strip():
                try:
                    obj["query"] = translate_text(q, t_endpoint, t_key, t_region)
                    translated_ok += 1
                except requests.HTTPError as e:
                    obj["translation_error"] = f"http_error: {str(e)}"
                    failed += 1
                except requests.RequestException as e:
                    obj["translation_error"] = f"request_error: {str(e)}"
                    failed += 1
            else:
                skipped += 1

            fout.write(json.dumps(obj, ensure_ascii=False) + "\n")

    print(
        f"MODE    : {'APPEND' if file_mode == 'a' else 'NEW'}\n"
        f"RANGE   : {START} ~ {END}\n"
        f"RESULT  : total={processed}, complete={translated_ok}, fail={failed}, skip={skipped}\n"
    )

if __name__ == "__main__":
    main()
