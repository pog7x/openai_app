## Поменять переменную окружения в docker-compose.yml

```yml
OPENAI_API_KEY=
```

## Запустить docker-compose

```bash
docker-compose up -d
```

## Получить список записей

```bash
curl '0.0.0.0:5555/processed-texts?offset=1' \
--header 'username: super_secret' \
--header 'password: very_secret'
```

## Создать запрос

```bash
curl '0.0.0.0:5555/process-text' \
--header 'username: super_secret' \
--header 'password: very_secret' \
--header 'Content-Type: application/json' \
--data '{
    "event_id": "12345",
    "payload": {
        "text": "What are the benefits of using AI in software development?",
        "meta": {"priority": "high"}
    }
}'
```
