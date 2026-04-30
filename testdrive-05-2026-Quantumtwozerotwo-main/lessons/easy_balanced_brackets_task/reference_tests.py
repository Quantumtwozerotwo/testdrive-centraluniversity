from solution import is_balanced


def test_empty_string_is_balanced():
    assert is_balanced("") is True


def test_single_pair_is_balanced():
    assert is_balanced("()") is True


def test_nested_brackets_are_balanced():
    assert is_balanced("([]{})") is True


def test_missing_closing_bracket_is_not_balanced():
    assert is_balanced("(") is False


def test_missing_opening_bracket_is_not_balanced():
    assert is_balanced(")") is False


def test_wrong_pair_type_is_not_balanced():
    assert is_balanced("(]") is False


def test_wrong_order_is_not_balanced():
    assert is_balanced("([)]") is False


def test_ignores_non_bracket_characters():
    assert is_balanced("text { [ ok ] }") is True
