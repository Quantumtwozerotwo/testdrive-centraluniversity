# WikiGame (homework)

Это шаблон проекта для участников: клиенты к `ru.wikipedia.org` готовы, ваша задача — реализовать алгоритм поиска пути.

## Быстрый старт

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

Тесты будут падать, пока не реализованы функции в `wikigame/bfs.py`.

## Задание

### 1. Обязательная часть: обычный BFS

Реализуйте функцию `find_path_bfs(...)` в `wikigame/bfs.py`.

Она должна искать кратчайший путь от статьи `start` до статьи `goal`.

Ожидаемое поведение:
- если путь найден, вернуть `SearchResult(path=..., visited_pages=...)`;
- если путь не найден, вернуть `None`;
- `path` должен содержать статьи от `start` до `goal`, включая границы;
- `visited_pages` — это количество вызовов `provider.get_links(...)`.

Дополнительные правила:
- если `start == goal`, нужно сразу вернуть путь из одной вершины;
- в этом случае `visited_pages == 0`;
- глубина считается в переходах по ссылкам;
- нужно соблюдать лимиты `max_depth` и `max_pages`;
- одну и ту же страницу нельзя разворачивать повторно;
- `start` и `goal` нужно нормализовать.

### 2. Дополнительная часть: двусторонний BFS

Реализуйте функцию `find_path_bidirectional_bfs(...)` в `wikigame/bfs.py`.

Ожидаемое поведение:
- поиск идёт одновременно от `start` и от `goal`;
- поиск от `start` использует `provider.get_links(...)`;
- поиск от `goal` использует `provider.get_backlinks(...)`;
- результат имеет тот же формат `SearchResult`;
- `visited_pages` считает развёрнутые страницы с обеих сторон поиска;
- путь должен быть кратчайшим;
- ограничения `max_depth` и `max_pages` тоже должны соблюдаться.

## Как устроено (коротко)
- `wikigame/bfs.py` — основное задание: BFS и двусторонний BFS.
- `wikigame/wiki_client_sync.py` — sync-клиент MediaWiki API.
- `wikigame/cli.py` — запуск из командной строки.
- `tests/` — офлайн-тесты без интернета.

## Что покрывают тесты
- поиск кратчайшего пути;
- случай `start == goal`;
- отсутствие пути;
- циклы в графе;
- `max_depth`;
- `max_pages`;
- нормализацию входа;
- контракт для двустороннего BFS.

В CI две отдельные проверки:
- `BFS` — обязательная часть;
- `Bidirectional BFS` — дополнительная часть.

Оценка:
- 1 балл — проходит job `BFS`;
- 2 балла — проходят jobs `BFS` и `Bidirectional BFS`.

## Запуск CLI (русская Википедия)

```bash
python -m wikigame --start "Питон" --goal "Гвидо ван Россум" --max-depth 4 --max-pages 300
```

## Если падает SSL (`SSLCertVerificationError`)
Правильный вариант — передать CA bundle: `--ca-bundle /path/to/ca.pem`, крайний — `--insecure` (не рекомендуется).
