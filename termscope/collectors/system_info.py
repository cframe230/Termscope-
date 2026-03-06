from __future__ import annotations

import platform
import socket
from pathlib import Path

from termscope.models import SystemInfo
from termscope.utils.os_release import read_os_release


PROC_UPTIME_PATH = "/proc/uptime"


def _read_uptime_seconds(path: str = PROC_UPTIME_PATH) -> float:
    file_path = Path(path)
    if not file_path.exists():
        return 0.0
    try:
        first = file_path.read_text(encoding="utf-8").split()[0]
        return float(first)
    except (IndexError, ValueError, OSError):
        return 0.0


def get_system_info() -> SystemInfo:
    osr = read_os_release()
    uname = platform.uname()
    return SystemInfo(
        hostname=socket.gethostname(),
        distro_name=osr.get("NAME", "Linux"),
        distro_pretty_name=osr.get("PRETTY_NAME", osr.get("NAME", "Linux")),
        distro_version=osr.get("VERSION_ID", osr.get("VERSION", "")),
        distro_id=osr.get("ID", "linux"),
        kernel_version=uname.release,
        architecture=uname.machine,
        uptime_seconds=_read_uptime_seconds(),
    )
