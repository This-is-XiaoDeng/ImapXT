import json
from pathlib import Path

CACHE_PATH = Path(".cache")
CACHE_PATH.mkdir(exist_ok=True)

def get_read_emails(address: str) -> list[str]:
    if not (path := CACHE_PATH / f"{address}.json").exists():
        return []
    with open(path) as f:
        return json.load(f)

def add_read_emails(address: str, num: str) -> None:
    path = CACHE_PATH / f"{address}.json"
    origin = get_read_emails(address)
    origin.append(num)
    with open(path, "w") as f:
        f.write(json.dumps(origin))