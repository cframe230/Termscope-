from termscope.utils.distro_theme import (
    get_label_style,
    get_logo_style,
    get_theme_class,
    get_value_style,
)


def test_get_theme_class_for_known_distro() -> None:
    assert get_theme_class("ubuntu") == "theme-ubuntu"


def test_get_theme_class_fallback() -> None:
    assert get_theme_class("unknown") == "theme-default"


def test_get_logo_style_for_known_distro() -> None:
    assert get_logo_style("debian") == "bold #d70a53"


def test_get_logo_style_fallback() -> None:
    assert get_logo_style("unknown") == "bold #84a9d8"


def test_get_label_style_for_known_distro() -> None:
    assert get_label_style("fedora") == "bold #8cc0ff"


def test_get_value_style_fallback() -> None:
    assert get_value_style("unknown") == "#e6edf5"
