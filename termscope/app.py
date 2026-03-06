from __future__ import annotations

from datetime import datetime
import signal

import psutil
from textual.app import App
from textual.binding import Binding
from textual.timer import Timer

from termscope.collectors.metrics import get_system_metrics
from termscope.collectors.processes import get_processes, prime_process_cpu
from termscope.collectors.system_info import get_system_info
from termscope.constants import REFRESH_INTERVAL_SECONDS
from termscope.screens.confirm_kill import ConfirmKillScreen
from termscope.screens.dashboard import DashboardScreen
from termscope.screens.processes import ProcessesScreen
from termscope.utils.distro_theme import THEME_CLASSES, get_theme_class
from termscope.widgets.process_table import ProcessTable


class TermScopeApp(App[None]):
    CSS_PATH = "styles/app.tcss"
    SCREENS = {
        "dashboard": DashboardScreen,
        "processes": ProcessesScreen,
    }
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("r", "refresh_data", "Refresh"),
        Binding("space", "toggle_pause", "Pause/Resume"),
        Binding("d", "show_dashboard", "Dashboard", show=False),
        Binding("p", "show_processes", "Processes", show=False),
        Binding("k", "request_term", "Kill"),
        Binding("K", "request_kill", "Force Kill"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.paused = False
        self._refresh_timer: Timer | None = None
        self._message = ""

    def on_mount(self) -> None:
        psutil.cpu_percent(interval=None)
        prime_process_cpu()
        self.push_screen("dashboard")
        self.refresh_all()
        self._refresh_timer = self.set_interval(REFRESH_INTERVAL_SECONDS, self._tick_refresh)

    def _tick_refresh(self) -> None:
        if not self.paused:
            self.refresh_all()

    def action_refresh_data(self) -> None:
        self.refresh_all()

    def action_toggle_pause(self) -> None:
        self.paused = not self.paused
        self._message = "Paused" if self.paused else "Resumed"
        self.refresh_all()

    def action_show_dashboard(self) -> None:
        self.switch_screen("dashboard")
        self.refresh_all()

    def action_show_processes(self) -> None:
        self.switch_screen("processes")
        self.refresh_all()

    def action_request_term(self) -> None:
        self._request_signal(signal.SIGTERM, "SIGTERM")

    def action_request_kill(self) -> None:
        self._request_signal(signal.SIGKILL, "SIGKILL")

    def _apply_theme(self, distro_id: str) -> None:
        theme_class = get_theme_class(distro_id)
        for class_name in THEME_CLASSES:
            self.screen.remove_class(class_name)
        self.screen.add_class(theme_class)

    def _selected_process(self):
        table_id = "#processes-table" if self.screen.name == "processes" else "#top-processes"
        try:
            table = self.screen.query_one(table_id, ProcessTable)
        except Exception:
            return None
        return table.get_selected_process()

    def _request_signal(self, sig: signal.Signals, signal_name: str) -> None:
        process = self._selected_process()
        if process is None:
            self._message = "No process selected"
            self.refresh_all()
            return

        def after_confirm(confirmed: bool) -> None:
            if not confirmed:
                self._message = f"Cancelled {signal_name}"
                self.refresh_all()
                return
            self._send_signal(process.pid, process.name, sig, signal_name)

        self.push_screen(ConfirmKillScreen(process, signal_name), after_confirm)

    def _send_signal(self, pid: int, name: str, sig: signal.Signals, signal_name: str) -> None:
        try:
            psutil.Process(pid).send_signal(sig)
            self._message = f"Sent {signal_name} to PID {pid} ({name})"
        except psutil.NoSuchProcess:
            self._message = f"PID {pid} already exited"
        except psutil.AccessDenied:
            self._message = f"Permission denied for PID {pid}"
        except Exception as exc:
            self._message = f"Signal failed: {exc}"
        self.refresh_all()

    def _status_prefix(self) -> str:
        state = "PAUSED" if self.paused else "LIVE"
        base = f"[{state}] q Quit | r Refresh | space Pause | / Search | k Kill | K SIGKILL"
        if self._message:
            return f"{base} | {self._message}"
        return base

    def refresh_all(self) -> None:
        system_info = get_system_info()
        metrics = get_system_metrics()
        timestamp = datetime.now().strftime("%H:%M:%S")
        self._apply_theme(system_info.distro_id)

        if isinstance(self.screen, ProcessesScreen):
            processes_screen = self.screen
            sort_by = getattr(processes_screen, "sort_by", "cpu")
            sort_descending = getattr(processes_screen, "sort_descending", True)
            processes = get_processes(sort_by=sort_by, descending=sort_descending, limit=None)
            search_prefix = getattr(processes_screen, "search_prefix", "")
            search_mode = getattr(processes_screen, "search_mode", False)
            no_match_query = getattr(processes_screen, "no_match_query", "")
            tracked_pid = getattr(processes_screen, "tracked_pid", None)
            tracked_name = getattr(processes_screen, "tracked_name", "")
            cpu_label = "CPU↓*" if sort_by == "cpu" and sort_descending else "CPU↑*" if sort_by == "cpu" else "CPU"
            mem_label = "Memory↓*" if sort_by == "memory" and sort_descending else "Memory↑*" if sort_by == "memory" else "Memory"
            if search_mode:
                search_status = f" | SEARCH /{search_prefix}"
            elif search_prefix:
                search_status = f" | search '{search_prefix}'"
            else:
                search_status = " | type to search | / search mode"
            no_match_status = f" | no match '{no_match_query}'" if no_match_query else ""
            tracked_status = (
                f" | tracking {tracked_name} ({tracked_pid})" if tracked_pid is not None else ""
            )
            status = (
                f"{self._status_prefix()} | c {cpu_label} | "
                f"m {mem_label}{search_status}{no_match_status}{tracked_status} | Updated {timestamp}"
            )
            processes_screen.update_processes_view(system_info, processes, status)
            return

        if isinstance(self.screen, DashboardScreen):
            processes = get_processes(sort_by="cpu", limit=None)
            status = f"{self._status_prefix()} | Updated {timestamp}"
            self.screen.update_dashboard(system_info, metrics, processes, status)


def main() -> None:
    TermScopeApp().run()


if __name__ == "__main__":
    main()
