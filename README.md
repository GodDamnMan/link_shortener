# link_shortenner

Сервис для сокращения ссылок

## Возможности

- Сокращение любой ссылки (`POST /shorten`)
- Использование своих кодов для сокращения ссылок
- Переход по короткой ссылке с редиректом 302 (`GET /{code}`)
- Конфигурация через `pyproject.toml`
- Логгирование каждого обращения к Api

## Примеры запросов
Обычное сокращение
```bash
curl -X POST http://127.0.0.1:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://google.com"}'
```

Сокращение с кастомным кодом
```bash
curl -X POST http://127.0.0.1:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://example.com", "custom_code": "test"}'
```

## Quick setup

```bash
git clone https://github.com/GodDamnMan/link_shortener.git
cd link_shortener
pip install -e .
uvicorn app.main:app --reload --port 8000
```


## Tests
Prerequirements
```bash
pip install pytest httpx
```

Run tests
```bash
pytest -v
```