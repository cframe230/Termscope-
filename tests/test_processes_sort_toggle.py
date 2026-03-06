from termscope.screens.processes import ProcessesScreen


def test_cpu_sort_toggles_direction_on_repeat() -> None:
    screen = ProcessesScreen()
    screen._refresh_app = lambda: None

    assert screen.sort_by == "cpu"
    assert screen.sort_descending is True

    screen.action_sort_cpu()
    assert screen.sort_by == "cpu"
    assert screen.sort_descending is False

    screen.action_sort_cpu()
    assert screen.sort_descending is True


def test_memory_sort_switches_and_then_toggles() -> None:
    screen = ProcessesScreen()
    screen._refresh_app = lambda: None

    screen.action_sort_memory()
    assert screen.sort_by == "memory"
    assert screen.sort_descending is True

    screen.action_sort_memory()
    assert screen.sort_descending is False
