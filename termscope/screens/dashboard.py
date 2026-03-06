from __future__ import annotations

from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen

from termscope.models import ProcessInfo, SystemInfo, SystemMetrics
from termscope.widgets.distro_panel import DistroPanel
from termscope.widgets.footer_bar import FooterBar
from termscope.widgets.header_bar import HeaderBar
from termscope.widgets.metrics_panel import MetricsPanel
from termscope.widgets.process_table import ProcessTable


class DashboardScreen(Screen):
    def compose(self):
        yield HeaderBar(id="header")
        with Horizontal(id="main"):
            with Container(id="metrics-pane"):
                with Vertical(id="metrics-stack"):
                    yield MetricsPanel(id="metrics")
                    yield DistroPanel(id="distro-art")
            yield Container(ProcessTable(id="top-processes"), id="process-pane")
        yield FooterBar(id="footer")

    def update_dashboard(
        self,
        system_info: SystemInfo,
        metrics: SystemMetrics,
        processes: list[ProcessInfo],
        status: str,
    ) -> None:
        self.query_one(HeaderBar).update_info(system_info)
        self.query_one(MetricsPanel).update_metrics(metrics)
        self.query_one(DistroPanel).update_info(system_info)
        self.query_one("#top-processes", ProcessTable).update_processes(processes)
        self.query_one(FooterBar).update_status(status)
