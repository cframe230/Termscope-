from __future__ import annotations

import psutil

from termscope.models import ProcessInfo


SAFE_NAME = "<unknown>"
SAFE_USER = "<unknown>"


class ProcessCollector:
    def __init__(self) -> None:
        self._primed = False

    def prime(self) -> None:
        if self._primed:
            return
        for proc in psutil.process_iter():
            try:
                proc.cpu_percent(interval=None)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        self._primed = True

    def _coerce_process(self, proc: psutil.Process) -> ProcessInfo | None:
        try:
            return ProcessInfo(
                pid=proc.pid,
                name=proc.name() or SAFE_NAME,
                username=proc.username() or SAFE_USER,
                cpu_percent=float(proc.cpu_percent(interval=None)),
                memory_percent=float(proc.memory_percent()),
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, ValueError, TypeError):
            return None

    def get_processes(
        self,
        sort_by: str = "cpu",
        descending: bool = True,
        limit: int | None = 20,
    ) -> list[ProcessInfo]:
        self.prime()
        processes: list[ProcessInfo] = []
        for proc in psutil.process_iter():
            item = self._coerce_process(proc)
            if item is not None:
                processes.append(item)

        key = (lambda p: p.memory_percent) if sort_by == "memory" else (lambda p: p.cpu_percent)
        sorted_processes = sorted(processes, key=key, reverse=descending)
        return sorted_processes if limit is None else sorted_processes[:limit]


_collector = ProcessCollector()


def prime_process_cpu() -> None:
    _collector.prime()


def get_processes(
    sort_by: str = "cpu",
    descending: bool = True,
    limit: int | None = 20,
) -> list[ProcessInfo]:
    return _collector.get_processes(sort_by=sort_by, descending=descending, limit=limit)


def get_top_processes_by_cpu(limit: int = 10) -> list[ProcessInfo]:
    return get_processes(sort_by="cpu", descending=True, limit=limit)


def get_top_processes_by_memory(limit: int = 10) -> list[ProcessInfo]:
    return get_processes(sort_by="memory", descending=True, limit=limit)
