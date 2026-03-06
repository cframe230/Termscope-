from __future__ import annotations

from datetime import datetime

from textual.widgets import Static

from termscope.models import SystemInfo
from termscope.utils.formatters import format_uptime


class HeaderBar(Static):
    def update_info(self, info: SystemInfo) -> None:
        now = datetime.now().strftime("%H:%M:%S")
        text = (
            f"Host: {info.hostname} | {info.distro_pretty_name} | "
            f"Kernel: {info.kernel_version} | Arch: {info.architecture} | "
            f"Up: {format_uptime(info.uptime_seconds)} | {now}"
        )
        self.update(text)
