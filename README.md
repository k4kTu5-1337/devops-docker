# FastAPI minimal blog (Docker + PostgreSQL)

Простейший API блога с двумя эндпоинтами:
- `GET /posts` — список публикаций
- `POST /posts` — создание публикации

Данные хранятся в PostgreSQL. Логи приложения и БД пишутся в `./logs` на хосте.

## Быстрый старт (локально/на сервере)
```bash
mkdir -p logs
docker compose up -d --build
curl -s http://localhost:8080/posts
curl -s -X POST http://localhost:8080/posts -H "Content-Type: application/json" -d '{"title":"Hello","content":"World"}'
curl -s http://localhost:8080/posts
```

### Требования
- Docker Engine + Docker Compose v2
- Открыт порт 8080 (firewalld)
- На CentOS/SELinux: bind-mount с меткой `:Z` уже настроен в `docker-compose.yml`

## Структура
```
app/
  database.py
  models.py
  schemas.py
  main.py
logs/                # точка монтирования логов
Dockerfile
docker-compose.yml
requirements.txt
.github/workflows/deploy.yml
```

## API
**GET /posts** → `200 OK`
```json
[]
```

**POST /posts**
Request:
```json
{"title":"Hello","content":"World"}
```
Response:
```json
{"id":1,"title":"Hello","content":"World"}
```

## CI/CD (GitHub Actions)
Workflow собирает образ и деплоит по SSH на сервер (где уже есть этот репозиторий).

Необходимые секреты (Repository → Settings → Secrets and variables → Actions):
- `SSH_PRIVATE_KEY`
- `SERVER_HOST`
- `SERVER_USER`
- `SERVER_PORT` (опционально, по умолчанию 22)
- `REPO_DIR` (например, `/opt/blog`)

> Образ публикуется в GHCR как `ghcr.io/<owner>/<repo>:latest`. Сделайте пакет Public **или** добавьте шаг логина в GHCR (см. комментарии в workflow).
