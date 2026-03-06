from __future__ import annotations

DISTRO_THEME_MAP: dict[str, str] = {
    "arch": "theme-arch",
    "cachyos": "theme-cachyos",
    "ubuntu": "theme-ubuntu",
    "debian": "theme-debian",
    "fedora": "theme-fedora",
    "nixos": "theme-nixos",
    "alpine": "theme-alpine",
    "gentoo": "theme-gentoo",
}

DISTRO_LOGO_STYLE_MAP: dict[str, str] = {
    "arch": "bold #3ea0ff",
    "cachyos": "bold #b46bff",
    "ubuntu": "bold #e95420",
    "debian": "bold #d70a53",
    "fedora": "bold #51a2ff",
    "nixos": "bold #7ad9f5",
    "alpine": "bold #6ab7ff",
    "gentoo": "bold #b39ddb",
}

DISTRO_LABEL_STYLE_MAP: dict[str, str] = {
    "arch": "bold #6ab7ff",
    "cachyos": "bold #d8b4ff",
    "ubuntu": "bold #ff9b73",
    "debian": "bold #ff6e9d",
    "fedora": "bold #8cc0ff",
    "nixos": "bold #a8ecff",
    "alpine": "bold #8fd0ff",
    "gentoo": "bold #d1c4e9",
}

DISTRO_VALUE_STYLE_MAP: dict[str, str] = {
    "arch": "#e6f3ff",
    "cachyos": "#f0e6ff",
    "ubuntu": "#ffe7dd",
    "debian": "#ffe3ee",
    "fedora": "#e7f3ff",
    "nixos": "#e5fbff",
    "alpine": "#e8f6ff",
    "gentoo": "#f3edff",
}

THEME_CLASSES = tuple(sorted(set(DISTRO_THEME_MAP.values()) | {"theme-default"}))


def get_theme_class(distro_id: str) -> str:
    return DISTRO_THEME_MAP.get((distro_id or "").lower(), "theme-default")


def get_logo_style(distro_id: str) -> str:
    return DISTRO_LOGO_STYLE_MAP.get((distro_id or "").lower(), "bold #84a9d8")


def get_label_style(distro_id: str) -> str:
    return DISTRO_LABEL_STYLE_MAP.get((distro_id or "").lower(), "bold #84a9d8")


def get_value_style(distro_id: str) -> str:
    return DISTRO_VALUE_STYLE_MAP.get((distro_id or "").lower(), "#e6edf5")
