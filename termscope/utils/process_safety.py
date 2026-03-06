from __future__ import annotations

from termscope.models import ProcessInfo


CRITICAL_PROCESS_NAMES = {
    "init",
    "systemd",
    "kthreadd",
    "dbus-daemon",
    "dbus-broker",
    "systemd-journald",
    "systemd-logind",
    "systemd-udevd",
    "NetworkManager",
    "sshd",
    "cron",
    "crond",
    "agetty",
    "login",
    "dockerd",
    "containerd",
}


def get_process_risk_reasons(process: ProcessInfo) -> list[str]:
    reasons: list[str] = []
    if process.pid == 1:
        reasons.append("PID 1 may be the init/system manager process")
    if process.pid <= 2:
        reasons.append("Very low PID suggests a core system process")
    if process.username == "root":
        reasons.append("Owned by root")
    if process.name in CRITICAL_PROCESS_NAMES:
        reasons.append(f"Matches critical system process name: {process.name}")
    if process.name.startswith("[") and process.name.endswith("]"):
        reasons.append("Kernel worker / kernel thread style process")
    return reasons


def is_critical_process(process: ProcessInfo) -> bool:
    return bool(get_process_risk_reasons(process))
