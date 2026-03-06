from __future__ import annotations

DISTRO_ICON_MAP: dict[str, str] = {
    "arch": "",
    "cachyos": "",
    "ubuntu": "",
    "debian": "",
    "fedora": "",
    "rhel": "",
    "centos": "",
    "opensuse": "",
    "sles": "",
    "nixos": "",
    "gentoo": "",
    "alpine": "",
    "void": "",
    "manjaro": "",
    "linuxmint": "󰣭",
    "pop": "",
    "zorin": "󰣨",
}


def get_distro_icon(distro_id: str) -> str:
    return DISTRO_ICON_MAP.get((distro_id or "").lower(), "🐧")
