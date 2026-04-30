from solution import has_path


def test_start_next_to_goal():
    grid = ["SG"]

    assert has_path(grid) is True
