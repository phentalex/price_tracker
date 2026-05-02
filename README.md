# Price Tracker

Веб-приложение для отслеживания цен на товары с Wildberries и Ozon. Автоматически проверяет цены по расписанию и отправляет уведомление в Telegram, когда цена достигает целевого значения. Развёртывание — Docker Compose.

## Возможности

- Добавление товаров по ссылке с Wildberries и Ozon
- Автоматический парсинг цен через Playwright / camoufox
- История цен с отображением динамики
- Telegram-уведомление при достижении целевой цены
- Мультипользовательский режим — каждый видит только свои товары
- Периодическая проверка цен через Celery Beat

## Стек

- Python 3.12
- Django 5.1
- Celery + Redis
- camoufox (Firefox) — антидетект-парсер
- PostgreSQL
- Docker / Docker Compose

## Переменные окружения

Файл `.env` в корне проекта:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_URL=postgres://ПОЛЬЗОВАТЕЛЬ:ПАРОЛЬ@db:5432/НАЗВАНИЕ_БАЗЫ
POSTGRES_DB=price_tracker
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

REDIS_URL=redis://redis:6379

TELEGRAM_BOT_TOKEN=your-telegram-bot-token
```

## Запуск локально через Docker

```bash
git clone https://github.com/phentalex/price-tracker.git
cd price-tracker
docker compose up --build -d
```

Доступно здесь -> http://localhost:8000

## Запуск на сервере через Docker

```bash
mkdir price-tracker && cd price-tracker
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d
```

## Как получить Telegram Chat ID

1. Напишите боту [@userinfobot](https://t.me/userinfobot) любое сообщение
2. Он ответит вашим ID — скопируйте его сюда

> ⚠️ Также необходимо написать своему боту хотя бы одно сообщение — иначе он не сможет отправлять уведомления.

Указать полученный Chat ID в личном кабинете на сайте.

## Автор

**Александр Уваров** — [GitHub](https://github.com/phentalex)
