from __future__ import annotations

from rich.text import Text
from textual.widgets import DataTable

from termscope.models import ProcessInfo


class ProcessTable(DataTable):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._processes: list[ProcessInfo] = []
        self._highlight_prefix = ""

    def on_mount(self) -> None:
        self.cursor_type = "row"
        self.add_columns("PID", "Name", "User", "CPU%", "MEM%")

    def set_highlight_prefix(self, prefix: str) -> None:
        self._highlight_prefix = prefix.lower().strip()

    def format_process_name(self, name: str) -> Text | str:
        prefix = self._highlight_prefix
        if not prefix or not name.lower().startswith(prefix):
            return name

        highlighted = Text()
        highlighted.append(name[: len(prefix)], style="bold #111111 on #ffd866")
        highlighted.append(name[len(prefix) :])
        return highlighted

    def update_processes(self, processes: list[ProcessInfo]) -> None:
        previous = self.get_selected_process()
        previous_pid = previous.pid if previous else None
        self._processes = list(processes)
        self.clear(columns=False)
        target_index = 0

        for index, process in enumerate(processes):
            self.add_row(
                str(process.pid),
                self.format_process_name(process.name),
                process.username,
                f"{process.cpu_percent:.1f}",
                f"{process.memory_percent:.1f}",
            )
            if previous_pid is not None and process.pid == previous_pid:
                target_index = index

        if processes:
            self.move_cursor(row=target_index, column=0)
            self.scroll_to_row(target_index)

    def get_selected_process(self) -> ProcessInfo | None:
        row_index = self.cursor_row
        if row_index is None:
            return None
        if 0 <= row_index < len(self._processes):
            return self._processes[row_index]
        return None

    def jump_to_prefix(self, prefix: str) -> bool:
        normalized = prefix.strip().lower()
        if not normalized:
            return False

        for index, process in enumerate(self._processes):
            if process.name.lower().startswith(normalized):
                self.move_cursor(row=index, column=0)
                self.scroll_to_row(index)
                return True
        return False

    def cycle_prefix(self, prefix: str) -> bool:
        normalized = prefix.strip().lower()
        if not normalized:
            return False

        matches = [
            index for index, process in enumerate(self._processes) if process.name.lower().startswith(normalized)
        ]
        if not matches:
            return False

        current_row = self.cursor_row if self.cursor_row is not None else -1
        for index in matches:
            if index > current_row:
                self.move_cursor(row=index, column=0)
                self.scroll_to_row(index)
                return True

        first = matches[0]
        self.move_cursor(row=first, column=0)
        self.scroll_to_row(first)
        return True

    def scroll_to_row(self, row_index: int) -> None:
        get_region = getattr(self, "_get_row_region", None)
        if callable(get_region):
            self.scroll_to_region(get_region(row_index), animate=False)
