# WikiGame: шаблон для участников

Это репозиторий-заготовка: сетевые клиенты к `ru.wikipedia.org` уже есть, а алгоритм поиска пути нужно реализовать самостоятельно.

## Что нужно сделать

### Обязательная часть. Обычный BFS

Реализуйте функцию `find_path_bfs(...)` в `homework/wikigame/bfs.py`.

Она должна искать кратчайший путь от статьи `start` до статьи `goal` по ссылкам Википедии.

Функция должна:
- вернуть `SearchResult(path=..., visited_pages=...)`, если путь найден;
- вернуть `None`, если путь не найден;
- учитывать ограничения `max_depth` и `max_pages`.

Что означают поля результата:
- `path` — список статей от `start` до `goal`, включая обе границы;
- `visited_pages` — количество вызовов `provider.get_links(...)`.

Правила:
- если `start == goal`, нужно сразу вернуть путь из одной статьи;
- в этом случае `visited_pages` должен быть равен `0`;
- глубина — это число переходов по ссылкам;
- повторно разворачивать одну и ту же страницу нельзя;
- перед поиском нужно нормализовать `start` и `goal`.

### Дополнительная часть. Двусторонний BFS

Реализуйте функцию `find_path_bidirectional_bfs(...)` в `homework/wikigame/bfs.py`.

Она должна:
- искать путь одновременно со стороны `start` и со стороны `goal`;
- поиск от `start` использует `provider.get_links(...)`;
- поиск от `goal` использует `provider.get_backlinks(...)`;
- возвращать результат в том же формате `SearchResult`;
- `visited_pages` считает развёрнутые страницы с обеих сторон поиска;
- находить кратчайший путь;
- учитывать те же ограничения `max_depth` и `max_pages`.

## Навигация
- `homework/wikigame/bfs.py` — основное задание: BFS и двусторонний BFS.
- `homework/wikigame/wiki_client_sync.py` — sync-клиент MediaWiki API.
- `homework/wikigame/cli.py` — CLI для обычного BFS.
- `homework/tests/` — офлайн-тесты без интернета.
- `lessons/` — задания для урока по TDD и парному программированию.

## Быстрый старт

```bash
cd homework
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
pytest -q
```

Тесты будут падать, пока не реализованы функции в `homework/wikigame/bfs.py`.

Что проверяют тесты:
- поиск кратчайшего пути;
- случай `start == goal`;
- отсутствие пути;
- графы с циклами;
- ограничения `max_depth` и `max_pages`;
- нормализацию входа;
- контракт для двустороннего BFS.

В GitHub Actions эти части видны отдельно:
- `BFS` — обязательная часть;
- `Bidirectional BFS` — дополнительная часть.

Оценка:
- 1 балл — проходит job `BFS`;
- 2 балла — проходят jobs `BFS` и `Bidirectional BFS`.

## Запуск CLI (после реализации BFS)

```bash
cd homework
python -m wikigame --start "Питон" --goal "Гвидо ван Россум" --max-depth 4 --max-pages 300
```

## Если падает SSL (`SSLCertVerificationError`)
Правильный вариант — передать свой CA bundle:

```bash
cd homework
python -m wikigame --ca-bundle /path/to/ca.pem --start "Питон" --goal "Гвидо ван Россум"
```

Крайний вариант (только для локальной отладки):

```bash
cd homework
python -m wikigame --insecure --start "Питон" --goal "Гвидо ван Россум"
```
