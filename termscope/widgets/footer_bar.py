from __future__ import annotations

from textual.widgets import Static


class FooterBar(Static):
    DEFAULT_TEXT = "q Quit | r Refresh | space Pause | / Search | k Kill"

    def update_status(self, message: str | None = None) -> None:
        self.update(message or self.DEFAULT_TEXT)
