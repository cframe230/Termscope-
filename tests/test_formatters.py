from termscope.utils.formatters import format_bytes, format_uptime


def test_format_bytes() -> None:
    assert format_bytes(1024) == "1.0 KB"


def test_format_uptime() -> None:
    assert format_uptime(3661) == "1h 1m"
