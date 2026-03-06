from termscope.utils.distro_art import get_distro_art


def test_get_distro_art_returns_neofetch_like_arch_art() -> None:
    art = get_distro_art("arch")
    assert "-`" in art
    assert "ooo/" in art


def test_get_distro_art_falls_back() -> None:
    art = get_distro_art("unknown-distro")
    assert "o_o" in art
