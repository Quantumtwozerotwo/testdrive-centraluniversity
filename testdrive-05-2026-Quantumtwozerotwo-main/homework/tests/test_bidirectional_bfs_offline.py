import wikigame.bfs as bfs


class DummyProvider:
    def __init__(self, g: dict[str, list[str]]):
        self.g = g
        self.backlinks = _build_backlinks(g)
        self.link_calls = 0
        self.backlink_calls = 0
        self.requested_links: list[str] = []
        self.requested_backlinks: list[str] = []

    def get_links(self, title: str) -> list[str]:
        self.link_calls += 1
        self.requested_links.append(title)
        return self.g.get(title, [])

    def get_backlinks(self, title: str) -> list[str]:
        self.backlink_calls += 1
        self.requested_backlinks.append(title)
        return self.backlinks.get(title, [])


def _build_backlinks(g: dict[str, list[str]]) -> dict[str, list[str]]:
    backlinks: dict[str, list[str]] = {}
    for source, targets in g.items():
        backlinks.setdefault(source, [])
        for target in targets:
            backlinks.setdefault(target, []).append(source)
    return backlinks


def _total_calls(provider: DummyProvider) -> int:
    return provider.link_calls + provider.backlink_calls


def find_path_bidirectional_bfs(*args, **kwargs):
    assert hasattr(bfs, "find_path_bidirectional_bfs"), (
        "wikigame.bfs должен экспортировать find_path_bidirectional_bfs"
    )
    return bfs.find_path_bidirectional_bfs(*args, **kwargs)


def test_bidirectional_bfs_finds_shortest_path():
    g = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["D"],
        "D": ["E"],
        "E": [],
    }
    p = DummyProvider(g)

    res = find_path_bidirectional_bfs("A", "E", p, max_depth=10, max_pages=100)

    assert res is not None
    assert res.path in (["A", "B", "D", "E"], ["A", "C", "D", "E"])
    assert len(res.path) == 4
    assert res.visited_pages <= 5
    assert p.link_calls > 0
    assert p.backlink_calls > 0


def test_bidirectional_bfs_start_equals_goal():
    p = DummyProvider({"A": ["B"], "B": []})

    res = find_path_bidirectional_bfs("A", "A", p, max_depth=10, max_pages=100)

    assert res is not None
    assert res.path == ["A"]
    assert res.visited_pages == 0
    assert _total_calls(p) == 0


def test_bidirectional_bfs_respects_max_depth():
    g = {
        "A": ["B"],
        "B": ["C"],
        "C": ["D"],
        "D": ["E"],
        "E": [],
    }
    p = DummyProvider(g)

    res = find_path_bidirectional_bfs("A", "E", p, max_depth=2, max_pages=100)

    assert res is None


def test_bidirectional_bfs_respects_max_pages():
    g = {"S": [f"X{i}" for i in range(100)], "Z": []}
    for i in range(100):
        g[f"X{i}"] = ["Z"] if i == 99 else []
    p = DummyProvider(g)

    res = find_path_bidirectional_bfs("S", "Z", p, max_depth=2, max_pages=1)

    assert res is None


def test_bidirectional_bfs_returns_none_when_no_path():
    p = DummyProvider({"A": ["B"], "B": [], "C": []})

    res = find_path_bidirectional_bfs("A", "C", p, max_depth=10, max_pages=100)

    assert res is None


def test_bidirectional_bfs_normalizes_start_and_goal():
    p = DummyProvider({"A": ["B"], "B": ["C"], "C": []})

    res = find_path_bidirectional_bfs(" A ", " C ", p, max_depth=10, max_pages=100)

    assert res is not None
    assert res.path == ["A", "B", "C"]


def test_bidirectional_bfs_expands_from_goal_side():
    g = {
        "S": [*(f"X{i}" for i in range(50)), "M"],
        "M": ["S", "G"],
        "G": ["M"],
    }
    for i in range(50):
        g[f"X{i}"] = ["S"]
    p = DummyProvider(g)

    res = find_path_bidirectional_bfs("S", "G", p, max_depth=2, max_pages=10)

    assert res is not None
    assert res.path == ["S", "M", "G"]
    assert "G" in p.requested_backlinks
    assert p.backlink_calls > 0
    assert _total_calls(p) <= 4


def test_bidirectional_bfs_uses_small_goal_frontier_instead_of_scanning_wide_start_layer():
    g = {
        "S": [*(f"X{i}" for i in range(100)), "A"],
        "A": ["S", "B"],
        "B": ["A", "C"],
        "C": ["B", "G"],
        "G": ["C"],
    }
    for i in range(100):
        g[f"X{i}"] = ["S"]
    p = DummyProvider(g)

    res = find_path_bidirectional_bfs("S", "G", p, max_depth=4, max_pages=20)

    assert res is not None
    assert res.path == ["S", "A", "B", "C", "G"]
    assert "G" in p.requested_backlinks
    assert p.backlink_calls > 0
    assert _total_calls(p) < 20
