## Поменять переменную окружения в docker-compose.yml

```yml
OPENAI_API_KEY=
```

## При изменении секретные переменные окружения должны соответствовать хэдерам username и password

```yml
SECRET_USERNAME=super_secret
SECRET_PASSWORD=very_secret
```

## Для изменения параметров рейт лимита необходимо поменять переменные окружения:

```yml
RATE_LIMIT=5
RATE_LIMIT_LIFETIME=50
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

### Ответ:

```json
[
	{
		"event_id": "12345",
		"request_text": "What are the benefits of using AI in software development?",
		"ai_response": "AI helps automate routine tasks, improve decision-making, and enhance code quality."
	},
    ...
]
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

### Ответ:

```json
{
	"event_id": "12345",
	"request_text": "What are the benefits of using AI in software development?",
	"ai_response": "AI helps automate routine tasks, improve decision-making, and enhance code quality."
}
```
