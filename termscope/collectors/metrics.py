from __future__ import annotations

import os

import psutil

from termscope.constants import DEFAULT_DISK_PATH
from termscope.models import SystemMetrics
from termscope.utils.rates import NetworkRateTracker


_rate_tracker = NetworkRateTracker()


def get_system_metrics(disk_path: str = DEFAULT_DISK_PATH) -> SystemMetrics:
    vm = psutil.virtual_memory()
    swap = psutil.swap_memory()
    disk = psutil.disk_usage(disk_path)
    net = psutil.net_io_counters()
    rx_rate, tx_rate = _rate_tracker.update(net.bytes_recv, net.bytes_sent)

    try:
        load1, load5, load15 = os.getloadavg()
    except (AttributeError, OSError):
        load1 = load5 = load15 = 0.0

    return SystemMetrics(
        cpu_percent=psutil.cpu_percent(interval=None),
        memory_percent=vm.percent,
        swap_percent=swap.percent,
        disk_percent=disk.percent,
        load_avg_1=load1,
        load_avg_5=load5,
        load_avg_15=load15,
        net_rx_per_sec=rx_rate,
        net_tx_per_sec=tx_rate,
    )
