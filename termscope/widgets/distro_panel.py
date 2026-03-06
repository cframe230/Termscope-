from __future__ import annotations

from rich.text import Text
from textual.widgets import Static

from termscope.models import SystemInfo
from termscope.utils.distro_art import get_distro_art, get_distro_art_rich_lines
from termscope.utils.distro_theme import get_label_style, get_value_style
from termscope.utils.formatters import format_uptime


class DistroPanel(Static):
    def _append_color_blocks(self, render: Text, indent: int) -> None:
        block = "██"
        base_colors = [
            "#1d1f21",
            "#cc6666",
            "#b5bd68",
            "#f0c674",
            "#81a2be",
            "#b294bb",
            "#8abeb7",
            "#c5c8c6",
        ]
        bright_colors = [
            "#666666",
            "#ff6b6b",
            "#d9ef8b",
            "#ffd866",
            "#5fb3ff",
            "#c792ea",
            "#7fdbca",
            "#ffffff",
        ]

        render.append("\n\n")
        render.append(" " * indent)
        for color in base_colors:
            render.append(block, style=color)
            render.append(" ")
        render.append("\n")
        render.append(" " * indent)
        for color in bright_colors:
            render.append(block, style=color)
            render.append(" ")

    def update_info(self, info: SystemInfo) -> None:
        art_lines_plain = get_distro_art(info.distro_id).splitlines()
        art_lines_rich = get_distro_art_rich_lines(info.distro_id)
        info_lines = [
            ("OS", info.distro_pretty_name),
            ("Host", info.hostname),
            ("Kernel", info.kernel_version),
            ("Arch", info.architecture),
            ("Uptime", format_uptime(info.uptime_seconds)),
        ]

        art_width = max((len(line) for line in art_lines_plain), default=0)
        total_lines = max(len(art_lines_plain), len(info_lines))
        render = Text()
        label_style = get_label_style(info.distro_id)
        value_style = get_value_style(info.distro_id)
        info_indent = art_width + 4

        for index in range(total_lines):
            if index < len(art_lines_rich):
                render.append_text(art_lines_rich[index])
                render.append(" " * (art_width - len(art_lines_plain[index])))
            else:
                render.append(" " * art_width)

            render.append(" " * 4)
            if index < len(info_lines):
                label, value = info_lines[index]
                render.append(f"{label:<7}", style=label_style)
                render.append(value, style=value_style)
            if index < total_lines - 1:
                render.append("\n")

        self._append_color_blocks(render, info_indent)
        self.update(render)
