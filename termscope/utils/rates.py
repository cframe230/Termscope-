from __future__ import annotations

from dataclasses import dataclass
from time import monotonic


@dataclass(slots=True)
class RateSample:
    rx_bytes: int
    tx_bytes: int
    timestamp: float


class NetworkRateTracker:
    def __init__(self) -> None:
        self._previous: RateSample | None = None

    def update(self, rx_bytes: int, tx_bytes: int) -> tuple[float, float]:
        now = monotonic()
        current = RateSample(rx_bytes=rx_bytes, tx_bytes=tx_bytes, timestamp=now)
        previous = self._previous
        self._previous = current

        if previous is None:
            return 0.0, 0.0

        elapsed = max(current.timestamp - previous.timestamp, 1e-6)
        rx_rate = max(current.rx_bytes - previous.rx_bytes, 0) / elapsed
        tx_rate = max(current.tx_bytes - previous.tx_bytes, 0) / elapsed
        return rx_rate, tx_rate
