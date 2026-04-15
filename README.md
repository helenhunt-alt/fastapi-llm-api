# llm-p

Учебный проект на FastAPI: защищённый API для работы с LLM через OpenRouter

## Стек
- Python 3.11+
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite
- Pydantic
- JWT
- OpenRouter
- uv
- ruff

## Запуск проекта

### 1. Установить uv
```bash
python3 -m pip install uv
```

### 2. Создать виртуальное окружение
```bash
uv venv
source .venv/bin/activate
```

### 3. Установить зависимости
```bash
uv pip install -r <(uv pip compile pyproject.toml)
```

### 4. Заполнить .env
Создайте файл .env на основе .env.example и укажите OPENROUTER_API_KEY.

5. Запустить приложение
```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Структура проекта
- `app/core` — конфиг, безопасность, ошибки
- `app/db/` — база данных и модели
- `app/schemas/` — Pydantic-схемы
- `app/repositories/` — доступ к данным
- `app/services/` — внешние сервисы
- `app/usecases/` — бизнес-логика
- `app/api/` — роуты и зависимости
