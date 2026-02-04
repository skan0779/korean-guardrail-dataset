import asyncio, json, httpx
from pathlib import Path
from typing import Any, Dict, Tuple

# ====== Folder Setting =======
REPO_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = REPO_ROOT / "data" / "processed" / "selectstar.jsonl"
OUTPUT_PATH = REPO_ROOT / "answer" / "selectstar_result.jsonl"

# ====== Range Setting ========
API_URL = "http://localhost:8000/guardrail/check"
START = 1
END = 10000
CONCURRENCY = 10

# ====== Main Setting =========
SLEEP_SEC = 0.0
TIMEOUT_SEC = 20
STOP_ON_ERROR = False
WRITE_REQUEST_ECHO = False

# ====== Helper Function ======
async def post_json(
    client: httpx.AsyncClient,
    url: str,
    payload: Dict[str, Any],
) -> Tuple[Dict[str, Any], bool]:
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    try:
        response = await client.post(url, headers=headers, json=payload)
    except httpx.RequestError as e:
        return {"status": "error", "error": f"Request failed: {str(e)}"}, True

    text = response.text
    try:
        data = response.json()
    except Exception:
        data = {
            "status": "error",
            "error": "Non-JSON response",
            "http_status": response.status_code,
            "raw": text,
        }
    if response.status_code >= 400 and isinstance(data, dict):
        data.setdefault("status", "error")
        data.setdefault("http_status", response.status_code)
    return data, False

# ====== Main Function ========
async def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Input not found: {INPUT_PATH}")

    def print_error(id_value: object) -> None:
        print(f"ERROR: {id_value}")

    total = 0
    error_count = 0
    status_keys = [
        "prompt_blocked",
        "blockword_blocked",
        "content_blocked",
        "pii_blocked",
        "success",
        "failed",
    ]
    status_counts = {k: 0 for k in status_keys}

    file_mode = "a" if OUTPUT_PATH.exists() else "w"

    timeout = httpx.Timeout(TIMEOUT_SEC)
    stop_requested = False
    in_flight = set()

    async def handle_task(task: asyncio.Task) -> None:
        nonlocal error_count, stop_requested
        resp, had_exception = await task
        if had_exception:
            error_count += 1
            if STOP_ON_ERROR:
                stop_requested = True
        if isinstance(resp, dict):
            status = resp.get("status")
            if status in status_counts:
                status_counts[status] += 1
        wf.write(json.dumps(resp, ensure_ascii=False) + "\n")

    async with httpx.AsyncClient(timeout=timeout) as client:
        with INPUT_PATH.open("r", encoding="utf-8") as rf, OUTPUT_PATH.open(file_mode, encoding="utf-8") as wf:
            for line_no, line in enumerate(rf, start=1):
                if line_no < START:
                    continue
                if line_no > END:
                    break

                line = line.strip()
                if not line:
                    continue

                total += 1

                try:
                    row = json.loads(line)
                except Exception:
                    error_count += 1
                    print_error(line_no)
                    if STOP_ON_ERROR:
                        stop_requested = True
                        break
                    continue

                query = row.get("query")
                _id = row.get("id")

                if not isinstance(query, str) or not isinstance(_id, str):
                    error_count += 1
                    print_error(_id if isinstance(_id, str) and _id else line_no)
                    if STOP_ON_ERROR:
                        stop_requested = True
                        break
                    continue

                payload = {"query": query, "id": _id}

                task = asyncio.create_task(post_json(client, API_URL, payload))
                in_flight.add(task)

                if len(in_flight) >= CONCURRENCY:
                    done, in_flight = await asyncio.wait(
                        in_flight, return_when=asyncio.FIRST_COMPLETED
                    )
                    for finished in done:
                        await handle_task(finished)
                    if stop_requested:
                        break

                if SLEEP_SEC > 0:
                    await asyncio.sleep(SLEEP_SEC)

            if stop_requested:
                for task in in_flight:
                    task.cancel()
                await asyncio.gather(*in_flight, return_exceptions=True)
            else:
                for task in asyncio.as_completed(in_flight):
                    await handle_task(task)

    print(
        f"MODE    : {'APPEND' if file_mode == 'a' else 'NEW'}\n"
        f"RANGE   : {START} ~ {END}\n"
        f"TOTAL   : {total}\n"
        f"- prompt_blocked={status_counts['prompt_blocked']}\n"
        f"- blockword_blocked={status_counts['blockword_blocked']}\n"
        f"- content_blocked={status_counts['content_blocked']}\n"
        f"- pii_blocked={status_counts['pii_blocked']}\n"
        f"- success={status_counts['success']}\n"
        f"- failed={status_counts['failed']}\n"
        f"- error={error_count}\n"
    )

if __name__ == "__main__":
    asyncio.run(main())
