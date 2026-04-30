# Balanced Brackets

Начните с первого теста в `test_solution.py`.

После каждого зелёного теста меняйтесь ролями.

Порядок:
1. `driver` запускает `pytest -q`.
2. Пара видит красный тест.
3. `driver` пишет минимальный код в `solution.py`.
4. Пара запускает `pytest -q`.
5. Если тест зелёный, роли меняются.
6. `navigator` выбирает следующий тест-кейс.
7. Новый `driver` пишет следующий тест.

Команды:

```bash
cd lessons/easy_balanced_brackets_task
pytest -q
```

Финальная проверка:

```bash
pytest -q reference_tests.py
```

Подсказка: для решения обычно нужен стек.
