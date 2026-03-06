from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class SystemInfo:
    hostname: str = "unknown"
    distro_name: str = "Linux"
    distro_pretty_name: str = "Linux"
    distro_version: str = ""
    distro_id: str = "linux"
    kernel_version: str = "unknown"
    architecture: str = "unknown"
    uptime_seconds: float = 0.0


@dataclass(slots=True)
class SystemMetrics:
    cpu_percent: float = 0.0
    memory_percent: float = 0.0
    swap_percent: float = 0.0
    disk_percent: float = 0.0
    load_avg_1: float = 0.0
    load_avg_5: float = 0.0
    load_avg_15: float = 0.0
    net_rx_per_sec: float = 0.0
    net_tx_per_sec: float = 0.0


@dataclass(slots=True)
class ProcessInfo:
    pid: int
    name: str
    username: str
    cpu_percent: float
    memory_percent: float


@dataclass(slots=True)
class DashboardSnapshot:
    system_info: SystemInfo
    metrics: SystemMetrics
    top_cpu_processes: list[ProcessInfo] = field(default_factory=list)
    top_memory_processes: list[ProcessInfo] = field(default_factory=list)
    captured_at: datetime = field(default_factory=datetime.now)
