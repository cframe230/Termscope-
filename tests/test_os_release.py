from pathlib import Path

from termscope.utils.os_release import read_os_release


def test_read_os_release_parses_values(tmp_path: Path) -> None:
    path = tmp_path / "os-release"
    path.write_text('NAME="Ubuntu"\nPRETTY_NAME="Ubuntu 24.04 LTS"\n', encoding="utf-8")

    data = read_os_release(str(path))

    assert data["NAME"] == "Ubuntu"
    assert data["PRETTY_NAME"] == "Ubuntu 24.04 LTS"
