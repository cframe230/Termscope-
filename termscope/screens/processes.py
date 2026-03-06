from __future__ import annotations

from time import monotonic

from textual.binding import Binding
from textual.events import Key
from textual.screen import Screen
from textual.widgets import DataTable, Static

from termscope.models import ProcessInfo, SystemInfo
from termscope.widgets.footer_bar import FooterBar
from termscope.widgets.header_bar import HeaderBar
from termscope.widgets.process_table import ProcessTable


class ProcessesScreen(Screen):
    BINDINGS = [
        Binding("c", "sort_cpu", "Sort CPU"),
        Binding("m", "sort_memory", "Sort Memory"),
        Binding("slash", "enter_search_mode", "Search", show=False),
        Binding("enter", "accept_search", "Accept Search", show=False),
        Binding("backspace", "backspace_search", "Backspace Search", show=False),
        Binding("escape", "clear_search", "Clear Search", show=False),
    ]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.sort_by = "cpu"
        self.sort_descending = True
        self.search_prefix = ""
        self.search_mode = False
        self.no_match_query = ""
        self.tracked_pid: int | None = None
        self.tracked_name = ""
        self._last_search_at = 0.0
        self._search_timeout_seconds = 1.2

    def compose(self):
        yield HeaderBar(id="header")
        yield Static("Processes", id="processes-title")
        yield ProcessTable(id="processes-table")
        yield FooterBar(id="footer")

    def _sort_indicator(self) -> str:
        return "↓" if self.sort_descending else "↑"

    def _update_title(self) -> None:
        title = f"Processes — sort: {self.sort_by} {self._sort_indicator()}"
        if self.search_prefix:
            title += f" — search: {self.search_prefix}"
        if self.search_mode:
            title += " [SEARCH MODE]"
        if self.no_match_query:
            title += f" — no match: {self.no_match_query}"
        if self.tracked_pid is not None:
            title += f" — tracking: {self.tracked_name} ({self.tracked_pid})"
        self.query_one("#processes-title", Static).update(title)

    def _sync_tracked_process(self) -> None:
        selected = self.query_one(ProcessTable).get_selected_process()
        if selected is None:
            self.tracked_pid = None
            self.tracked_name = ""
        else:
            self.tracked_pid = selected.pid
            self.tracked_name = selected.name

    def _table(self) -> ProcessTable:
        return self.query_one(ProcessTable)

    def _refresh_app(self) -> None:
        try:
            self.app.refresh_all()
        except Exception:
            pass

    def _apply_search_result(self, matched: bool) -> None:
        self.no_match_query = "" if matched or not self.search_prefix else self.search_prefix
        self._table().set_highlight_prefix(self.search_prefix if matched else "")
        self._sync_tracked_process()
        self._refresh_app()

    def action_sort_cpu(self) -> None:
        if self.sort_by == "cpu":
            self.sort_descending = not self.sort_descending
        else:
            self.sort_by = "cpu"
            self.sort_descending = True
        self._refresh_app()

    def action_sort_memory(self) -> None:
        if self.sort_by == "memory":
            self.sort_descending = not self.sort_descending
        else:
            self.sort_by = "memory"
            self.sort_descending = True
        self._refresh_app()

    def action_enter_search_mode(self) -> None:
        self.search_mode = True
        self.no_match_query = ""
        self._refresh_app()

    def action_accept_search(self) -> None:
        if self.search_mode:
            self.search_mode = False
            self._refresh_app()

    def action_backspace_search(self) -> None:
        if self.search_prefix:
            self.search_prefix = self.search_prefix[:-1]
            self._last_search_at = monotonic()
            matched = True
            if self.search_prefix:
                matched = self._table().jump_to_prefix(self.search_prefix)
            self._apply_search_result(matched)
        elif self.search_mode:
            self.search_mode = False
            self._refresh_app()

    def action_clear_search(self) -> None:
        if self.search_prefix or self.search_mode or self.no_match_query:
            self.search_prefix = ""
            self.search_mode = False
            self.no_match_query = ""
            self._table().set_highlight_prefix("")
            self._refresh_app()

    def _handle_incremental_search(self, normalized: str) -> None:
        now = monotonic()
        timed_out = now - self._last_search_at > self._search_timeout_seconds
        table = self._table()

        if timed_out:
            self.search_prefix = ""

        if self.search_prefix == normalized and len(normalized) == 1 and not timed_out:
            matched = table.cycle_prefix(normalized)
        else:
            self.search_prefix += normalized
            matched = table.jump_to_prefix(self.search_prefix)
            if not matched and len(self.search_prefix) > 1:
                self.search_prefix = normalized
                matched = table.jump_to_prefix(self.search_prefix)

        self._last_search_at = now
        self._apply_search_result(matched)

    def _handle_search_mode_input(self, normalized: str) -> None:
        self.search_prefix += normalized
        matched = self._table().jump_to_prefix(self.search_prefix)
        self._apply_search_result(matched)

    def on_key(self, event: Key) -> None:
        if event.key == "slash":
            return

        if self.search_mode:
            if event.is_printable and event.character and event.character not in {"\n", "\r"}:
                self._handle_search_mode_input(event.character.lower())
                event.stop()
            return

        if len(event.key) != 1 or not event.character:
            return

        char = event.character
        if not char.isalnum():
            return

        self._handle_incremental_search(char.lower())
        event.stop()

    def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        if isinstance(event.data_table, ProcessTable):
            self._sync_tracked_process()
            self._update_title()

    def update_processes_view(
        self,
        system_info: SystemInfo,
        processes: list[ProcessInfo],
        status: str,
    ) -> None:
        self.query_one(HeaderBar).update_info(system_info)
        table = self.query_one("#processes-table", ProcessTable)
        table.set_highlight_prefix(self.search_prefix if not self.no_match_query else "")
        table.update_processes(processes)
        self._sync_tracked_process()
        self._update_title()
        self.query_one(FooterBar).update_status(status)
