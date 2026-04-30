from solution import has_path


def test_start_next_to_goal():
    assert has_path(["SG"]) is True


def test_straight_path_exists():
    assert has_path(["S..G"]) is True


def test_path_with_turn_exists():
    grid = [
        "S..",
        "##.",
        "..G",
    ]

    assert has_path(grid) is True


def test_wall_blocks_path():
    grid = [
        "S#G",
    ]

    assert has_path(grid) is False


def test_no_path_returns_false():
    grid = [
        "S#.",
        "###",
        ".#G",
    ]

    assert has_path(grid) is False


def test_diagonal_move_is_not_allowed():
    grid = [
        "S#",
        "#G",
    ]

    assert has_path(grid) is False


def test_cycle_does_not_loop_forever():
    grid = [
        "S...",
        ".##.",
        "...G",
    ]

    assert has_path(grid) is True
