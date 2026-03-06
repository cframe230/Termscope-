from termscope.collectors.system_info import get_system_info


def test_get_system_info_has_hostname() -> None:
    info = get_system_info()
    assert info.hostname
