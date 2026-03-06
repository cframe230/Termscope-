from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Middle
from textual.screen import ModalScreen
from textual.widgets import Static

from termscope.models import ProcessInfo
from termscope.utils.process_safety import get_process_risk_reasons, is_critical_process


class ConfirmKillScreen(ModalScreen[bool]):
    BINDINGS = [
        Binding("y,enter", "confirm", "Confirm"),
        Binding("n,escape", "cancel", "Cancel"),
    ]

    def __init__(self, process: ProcessInfo, signal_name: str) -> None:
        super().__init__()
        self.process = process
        self.signal_name = signal_name

    def compose(self) -> ComposeResult:
        critical = is_critical_process(self.process)
        reasons = get_process_risk_reasons(self.process)

        header = f"Send {self.signal_name} to PID {self.process.pid}?"
        details = f"{self.process.name} ({self.process.username})"
        footer = "Enter/Y confirm · Esc/N cancel"

        if critical:
            warning = "⚠ HIGH RISK TARGET\n" + "\n".join(f"- {reason}" for reason in reasons)
            message = f"{header}\n{details}\n\n{warning}\n\n{footer}"
            classes = "critical"
        else:
            message = f"{header}\n{details}\n\n{footer}"
            classes = ""

        with Center():
            with Middle():
                yield Static(message, id="confirm-kill-dialog", classes=classes)

    def action_confirm(self) -> None:
        self.dismiss(True)

    def action_cancel(self) -> None:
        self.dismiss(False)
