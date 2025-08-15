# News Parser — сбор заголовков в CSV

Скрипт парсит заголовки новостей с нескольких сайтов (например, `lenta.ru`, `habr.com`) и сохраняет в `output.csv`.

> Важно: сайты могут менять верстку. При необходимости подправьте CSS‑селекторы в коде.

## Запуск
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python parser.py
```

Результат — файл `output.csv` с колонками: `source,title,url`.