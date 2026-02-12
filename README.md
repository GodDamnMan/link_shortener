# link_shortenner

Сервис для сокращения ссылок. Выполнено  

## Возможности

- Сокращение любой ссылки (`POST /shorten`)
- Переход по короткой ссылке с редиректом 302 (`GET /{code}`)
- Конфигурация через `pyproject.toml`

## Quick setup

```bash
git clone https://github.com/GodDamnMan/link_shortener.git
cd link_shortener
pip install -e .
uvicorn app.main:app --reload --port 8000
```
