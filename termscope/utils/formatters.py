from __future__ import annotations


def format_bytes(value: float) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(value)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def format_rate(value: float) -> str:
    return f"{format_bytes(value)}/s"


def format_percent(value: float) -> str:
    return f"{value:.1f}%"


def format_uptime(seconds: float) -> str:
    total = int(seconds)
    days, remainder = divmod(total, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, _ = divmod(remainder, 60)
    parts: list[str] = []
    if days:
        parts.append(f"{days}d")
    if hours or days:
        parts.append(f"{hours}h")
    parts.append(f"{minutes}m")
    return " ".join(parts)


def format_load(a: float, b: float, c: float) -> str:
    return f"{a:.2f} {b:.2f} {c:.2f}"
