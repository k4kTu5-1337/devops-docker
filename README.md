# DevOps Docker Blog

Простой блог-сервер на Python/FastAPI с PostgreSQL, работающий в Docker.

## Структура проекта

```
.
├── app/                  # исходники приложения
├── logs/                 # точка монтирования для логов
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Локальный запуск

1. Установите Docker и Docker Compose на вашей машине или ВМ.
2. Запустите командой:

```bash
docker compose up -d --build
```

3. Приложение будет доступно на `http://localhost:8080`.

Логи сохраняются в папку `logs/`, данные PostgreSQL сохраняются в volume.

## API

### GET /posts

Возвращает список публикаций:

```json
[
  { "id": 1, "title": "Hello", "content": "World" }
]
```

### POST /posts

Добавляет новую публикацию:

**Request:**

```json
{
  "title": "Another post",
  "content": "Some content here"
}
```

**Response:**

```json
{
  "id": 2,
  "title": "Another post",
  "content": "Some content here"
}
```

## Технологии

- Python 3.11
- FastAPI
- Docker & Docker Compose
- PostgreSQL
- GitHub Actions (CI/CD)
- Self-hosted GitHub Runner

## Автоматический деплой

В репозитории настроен self-hosted runner на вашей ВМ (CentOS).

### Настройка секретов GitHub:

- `SSH_PRIVATE_KEY` — приватный ключ для подключения к ВМ
- `SERVER_USER` — пользователь на ВМ (например, `test`)
- `SERVER_HOST` — IP ВМ (например, `192.168.x.x`)
- `SERVER_PORT` — порт SSH (если отличается от 22)
- `REPO_DIR` — директория, куда будет деплой (например, `/opt/blog/devops-docker`)
- `CR_PAT` — (опционально) токен для приватного GHCR, если образ приватный

### Workflow GitHub Actions

- Сборка Docker-образа и пуш в GHCR при `push` в ветку `main`.
- Деплой на self-hosted runner выполняется на той же ВМ, где запущен контейнер.

**Важно:** Ранее, при использовании workflow с удалённым SSH (через NAT и внешний IP), деплой не выполнялся корректно (i/o timeout). Использование self-hosted runner устраняет проблему, так как деплой происходит локально на ВМ.

### Проверка

1. Локально через `docker compose up`.
2. Через браузер или `curl` на `http://<VM_IP>:8080/posts`.
3. Логи приложения и базы находятся в `logs/`.

---

**Примечание:** Self-hosted runner работает под пользователем, у которого есть доступ к Docker сокету, иначе требуется добавить пользователя в `docker` группу или использовать sudo.

