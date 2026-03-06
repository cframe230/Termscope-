from __future__ import annotations

from textual.widgets import Static

from termscope.models import SystemMetrics
from termscope.utils.formatters import format_load, format_percent, format_rate


class MetricsPanel(Static):
    def update_metrics(self, metrics: SystemMetrics) -> None:
        text = "\n".join(
            [
                f"CPU     {format_percent(metrics.cpu_percent)}",
                f"Memory  {format_percent(metrics.memory_percent)}",
                f"Swap    {format_percent(metrics.swap_percent)}",
                f"Disk    {format_percent(metrics.disk_percent)}",
                f"Load    {format_load(metrics.load_avg_1, metrics.load_avg_5, metrics.load_avg_15)}",
                f"Net RX  {format_rate(metrics.net_rx_per_sec)}",
                f"Net TX  {format_rate(metrics.net_tx_per_sec)}",
            ]
        )
        self.update(text)
