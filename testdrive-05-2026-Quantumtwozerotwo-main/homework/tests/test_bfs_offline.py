from wikigame.bfs import find_path_bfs


class DummyProvider:
    def __init__(self, g: dict[str, list[str]]):
        self.g = g
        self.calls = 0

    def get_links(self, title: str) -> list[str]:
        self.calls += 1
        return self.g.get(title, [])


def test_shortest_path():
    g = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["D"],
        "D": [],
    }
    p = DummyProvider(g)
    res = find_path_bfs("A", "D", p, max_depth=10, max_pages=100)
    assert res is not None
    assert res.path in (["A", "B", "D"], ["A", "C", "D"])
    assert len(res.path) == 3
    assert res.visited_pages <= 4


def test_start_equals_goal():
    p = DummyProvider({"A": ["B"], "B": []})
    res = find_path_bfs("A", "A", p, max_depth=10, max_pages=100)
    assert res is not None
    assert res.path == ["A"]
    assert res.visited_pages == 0
    assert p.calls == 0


def test_no_path():
    p = DummyProvider({"A": ["B"], "B": [], "C": []})
    res = find_path_bfs("A", "C", p, max_depth=10, max_pages=100)
    assert res is None


def test_bfs_handles_cycles_without_revisiting_pages():
    g = {
        "A": ["B", "C"],
        "B": ["A", "D"],
        "C": ["A", "D"],
        "D": ["E"],
        "E": [],
    }
    p = DummyProvider(g)

    res = find_path_bfs("A", "E", p, max_depth=10, max_pages=100)

    assert res is not None
    assert res.path in (["A", "B", "D", "E"], ["A", "C", "D", "E"])
    assert len(res.path) == len(set(res.path))
    assert p.calls <= len(g)


def test_bfs_normalizes_start_and_goal():
    p = DummyProvider({"A": ["B"], "B": ["C"], "C": []})

    res = find_path_bfs(" A ", " C ", p, max_depth=10, max_pages=100)

    assert res is not None
    assert res.path == ["A", "B", "C"]
