from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .models import LinkProvider
from .utils import normalize_title


@dataclass(frozen=True)
class SearchResult:
    path: list[str]
    visited_pages: int


def find_path_bfs(
        start: str,
        goal: str,
        provider: LinkProvider,
        *,
        max_depth: int = 5,
        max_pages: int = 500,
) -> Optional[SearchResult]:

    start = normalize_title(start)
    goal = normalize_title(goal)

    if start == goal:
        return SearchResult(path=[start], visited_pages=0)

    from collections import deque
    queue = deque([(start, [start])])
    visited = {start}
    visited_pages = 0

    while queue and visited_pages < max_pages:
        current, path = queue.popleft()
        current_depth = len(path) - 1

        if current_depth >= max_depth:
            continue

        links = provider.get_links(current)
        visited_pages += 1

        for link in links:
            if link == goal:
                return SearchResult(
                    path=path + [goal],
                    visited_pages=visited_pages
                )

            if link not in visited:
                visited.add(link)
                queue.append((link, path + [link]))

    return None


def find_path_bidirectional_bfs(
        start: str,
        goal: str,
        provider: LinkProvider,
        *,
        max_depth: int = 5,
        max_pages: int = 500,
) -> Optional[SearchResult]:

    start = normalize_title(start)
    goal = normalize_title(goal)

    if start == goal:
        return SearchResult(path=[start], visited_pages=0)

    from collections import deque

    forward_queue = deque([start])
    forward_visited = {start: [start]}
    backward_queue = deque([goal])
    backward_visited = {goal: [goal]}
    visited_pages = 0

    for depth in range(max_depth + 1):
        if visited_pages >= max_pages:
            break

        if depth <= max_depth:
            new_forward = set()
            for _ in range(len(forward_queue)):
                current = forward_queue.popleft()

                if current in backward_visited:
                    forward_path = forward_visited[current]
                    backward_path = backward_visited[current][::-1]
                    full_path = forward_path + backward_path[1:]
                    return SearchResult(path=full_path, visited_pages=visited_pages)

                links = provider.get_links(current)
                visited_pages += 1

                if visited_pages >= max_pages:
                    break

                for link in links:
                    if link not in forward_visited:
                        forward_visited[link] = forward_visited[current] + [link]
                        forward_queue.append(link)
                        new_forward.add(link)

            for page in new_forward:
                if page in backward_visited:
                    forward_path = forward_visited[page]
                    backward_path = backward_visited[page][::-1]
                    full_path = forward_path + backward_path[1:]
                    return SearchResult(path=full_path, visited_pages=visited_pages)

        if visited_pages >= max_pages:
            break

        if depth <= max_depth:
            new_backward = set()
            for _ in range(len(backward_queue)):
                current = backward_queue.popleft()

                if current in forward_visited:
                    forward_path = forward_visited[current]
                    backward_path = backward_visited[current][::-1]
                    full_path = forward_path + backward_path[1:]
                    return SearchResult(path=full_path, visited_pages=visited_pages)

                backlinks = provider.get_backlinks(current)
                visited_pages += 1

                if visited_pages >= max_pages:
                    break

                for backlink in backlinks:
                    if backlink not in backward_visited:
                        backward_visited[backlink] = backward_visited[current] + [backlink]
                        backward_queue.append(backlink)
                        new_backward.add(backlink)

            for page in new_backward:
                if page in forward_visited:
                    forward_path = forward_visited[page]
                    backward_path = backward_visited[page][::-1]
                    full_path = forward_path + backward_path[1:]
                    return SearchResult(path=full_path, visited_pages=visited_pages)

    return None