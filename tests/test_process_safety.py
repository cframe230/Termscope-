from termscope.models import ProcessInfo
from termscope.utils.process_safety import get_process_risk_reasons, is_critical_process


def test_root_systemd_process_is_critical() -> None:
    process = ProcessInfo(pid=1, name="systemd", username="root", cpu_percent=0.0, memory_percent=0.1)
    assert is_critical_process(process)
    reasons = get_process_risk_reasons(process)
    assert any("PID 1" in reason for reason in reasons)
    assert any("root" in reason for reason in reasons)


def test_normal_user_process_is_not_critical() -> None:
    process = ProcessInfo(pid=12345, name="python", username="fc", cpu_percent=1.0, memory_percent=1.0)
    assert not is_critical_process(process)
