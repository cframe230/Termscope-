from __future__ import annotations

from pathlib import Path


DEFAULT_OS_RELEASE_PATH = "/etc/os-release"


def _strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1]
    return value


def read_os_release(path: str = DEFAULT_OS_RELEASE_PATH) -> dict[str, str]:
    file_path = Path(path)
    if not file_path.exists():
        return {}

    data: dict[str, str] = {}
    for raw_line in file_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key] = _strip_quotes(value)
    return data
