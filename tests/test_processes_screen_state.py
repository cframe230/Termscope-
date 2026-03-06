from termscope.screens.processes import ProcessesScreen


def test_accept_search_turns_off_search_mode() -> None:
    screen = ProcessesScreen()
    screen.search_mode = True
    object.__setattr__(screen, "_app", type("AppStub", (), {"refresh_all": lambda self: None})())
    screen.action_accept_search()
    assert screen.search_mode is False


def test_apply_search_result_sets_no_match_query() -> None:
    screen = ProcessesScreen()
    table = type(
        "TableStub",
        (),
        {
            "set_highlight_prefix": lambda self, prefix: setattr(self, "prefix", prefix),
            "get_selected_process": lambda self: None,
        },
    )()
    screen.search_prefix = "zzz"
    object.__setattr__(screen, "_app", type("AppStub", (), {"refresh_all": lambda self: None})())
    screen.query_one = lambda *args, **kwargs: table
    screen._apply_search_result(False)
    assert screen.no_match_query == "zzz"
