# bewise

ссылка на тестовое задание:
- https://docs.google.com/document/d/1czwq05-iQWTpQIylIJ8vembhVrPipDa0CBEayjW5ieM/edit?tab=t.0#heading=h.1tomk7wdi438

## Описание сервиса

Сервис предоставляет следующий функционал:
- Принимает заявки через REST API (FastAPI).
- Обрабатывает и записывает заявки в PostgreSQL.
- Публикует информацию о новых заявках в Kafka.
- Обеспечивает эндпоинт для получения списка заявок с фильтрацией и пагинацией.

## Стек технологий
- FastAPI
- PostgreSQL
- Kafka
- SQLAlchemy
- Pydantic
- Pytest

## Установка и запуск

- Клонируйте репозиторий
```
git clone git@github.com:amalshakov/bewise.git
```
- Создайте и активируйте виртуальное окружение
```
python -m venv venv
source venv/Scripts/activate
```
- Запустите docker-compose (контейнеры)
```
docker-compose up --build
```
- Документация доступна по адресу:
```
http://localhost:8000/docs
```
### Автор:
- Александр Мальшаков (ТГ [@amalshakov](https://t.me/amalshakov), GitHub [amalshakov](https://github.com/amalshakov/))

### PS:
- .env добавлен в репу (реальных секретных данных там нет)