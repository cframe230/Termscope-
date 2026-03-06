from __future__ import annotations

from pathlib import Path

from termscope.app import TermScopeApp


ROOT = Path(__file__).resolve().parents[1]


class ScreenshotApp(TermScopeApp):
    CSS_PATH = str(ROOT / "termscope" / "styles" / "app.tcss")

    def on_mount(self) -> None:
        super().on_mount()
        self.set_timer(1.0, self._capture)

    def _capture(self) -> None:
        assets = ROOT / "assets"
        assets.mkdir(exist_ok=True)
        self.save_screenshot(filename="termscope-dashboard.svg", path=str(assets))
        self.exit()


if __name__ == "__main__":
    ScreenshotApp().run()
