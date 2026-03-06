from rich.text import Text

from termscope.models import ProcessInfo
from termscope.widgets.process_table import ProcessTable


def test_jump_to_prefix_matches_process_name() -> None:
    table = ProcessTable()
    table._processes = [
        ProcessInfo(pid=1, name="systemd", username="root", cpu_percent=0.0, memory_percent=0.1),
        ProcessInfo(pid=2, name="python", username="fc", cpu_percent=0.0, memory_percent=0.1),
        ProcessInfo(pid=3, name="plasmashell", username="fc", cpu_percent=0.0, memory_percent=0.1),
    ]

    moved = []
    table.move_cursor = lambda row, column=0: moved.append((row, column))
    table.scroll_to_row = lambda row: None

    assert table.jump_to_prefix("py") is True
    assert moved[-1] == (1, 0)


def test_jump_to_prefix_returns_false_when_missing() -> None:
    table = ProcessTable()
    table._processes = [
        ProcessInfo(pid=1, name="systemd", username="root", cpu_percent=0.0, memory_percent=0.1),
    ]
    table.move_cursor = lambda row, column=0: None
    table.scroll_to_row = lambda row: None

    assert table.jump_to_prefix("zzz") is False


def test_cycle_prefix_wraps_between_matches() -> None:
    table = ProcessTable()
    table._processes = [
        ProcessInfo(pid=1, name="python", username="fc", cpu_percent=0.0, memory_percent=0.1),
        ProcessInfo(pid=2, name="pipewire", username="fc", cpu_percent=0.0, memory_percent=0.1),
        ProcessInfo(pid=3, name="systemd", username="root", cpu_percent=0.0, memory_percent=0.1),
    ]
    table.cursor_coordinate = (0, 0)

    moved = []
    table.move_cursor = lambda row, column=0: moved.append((row, column))
    table.scroll_to_row = lambda row: None

    assert table.cycle_prefix("p") is True
    assert moved[-1] == (1, 0)


def test_format_process_name_highlights_prefix() -> None:
    table = ProcessTable()
    table.set_highlight_prefix("py")
    rendered = table.format_process_name("python")

    assert isinstance(rendered, Text)
    assert rendered.plain == "python"
    assert rendered.spans
