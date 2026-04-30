from solution import merge_intervals


def test_empty_list_returns_empty_list():
    assert merge_intervals([]) == []


def test_single_interval_returns_as_is():
    assert merge_intervals([(1, 3)]) == [(1, 3)]


def test_non_overlapping_intervals_stay_separate():
    assert merge_intervals([(1, 2), (5, 7)]) == [(1, 2), (5, 7)]


def test_overlapping_intervals_are_merged():
    assert merge_intervals([(1, 3), (2, 5)]) == [(1, 5)]


def test_unsorted_input_is_supported():
    assert merge_intervals([(5, 7), (1, 3), (2, 4)]) == [(1, 4), (5, 7)]


def test_touching_intervals_are_merged():
    assert merge_intervals([(1, 2), (2, 4), (4, 6)]) == [(1, 6)]


def test_several_groups_are_merged_independently():
    assert merge_intervals([(1, 4), (8, 10), (2, 6), (15, 18)]) == [(1, 6), (8, 10), (15, 18)]
