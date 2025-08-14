# DevOps Docker Blog

Простой блог-сервер на Python/FastAPI с поддержкой Docker и PostgreSQL.

## Структура проекта

```
.
├── app/ # исходники приложения
├── logs/ # монтирование для логов
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Как собрать и запустить проект локально

```bash
# Перейти в директорию проекта
cd /opt/blog/devops-docker

# Поднять контейнеры приложения и БД
docker compose up -d --build
```

Приложение доступно на http://localhost:8080.

Логи приложения и PostgreSQL сохраняются в папку ./logs.

Данные PostgreSQL сохраняются между перезапусками контейнеров через volume.

## API

### GET /posts

Возвращает список публикаций:

```json
[
  { "id": 1, "title": "Hello world", "content": "My first post!" }
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

- Python / FastAPI
- PostgreSQL
- Docker, docker-compose
- GitHub Actions (CI/CD)
- Self-hosted runner на CentOS

## Проверка работоспособности (smoke-test)

- Перейти на http://localhost:8080.
- Выполнить GET /posts — должен вернуть текущий список постов.
- Выполнить POST /posts с JSON — должен добавить новый пост.
- Проверить, что новые данные сохранились после перезапуска контейнера.

## CI/CD и деплой

### Что было изначально (SSH workflow)

Планировалось автоматическое развертывание через GitHub Actions по SSH.

**Проблема:** при использовании NAT и проброса портов на VM GitHub Actions не смог подключиться (i/o timeout), потому что внешнее соединение на IP хоста с порта 22/2222 не работало.

Поэтому условия задания с SSH-деплоем не были выполнены.

### Как сделано сейчас (self-hosted runner)

- На VM установлен self-hosted runner.
- Workflow запускается прямо на VM.
- Сборка Docker-образа и деплой выполняются локально.
- Нет необходимости указывать SSH_PRIVATE_KEY, SERVER_HOST, SERVER_USER и порт.
- Условия задания, связанные с push в main → автоматическим деплоем на сервере, выполнены через локальный runner.

### Настройка GitHub Actions для self-hosted runner

1. Установить runner на VM:

```bash
mkdir actions-runner && cd actions-runner
# Скопировать команду config.sh с GitHub репозитория → вставить и выполнить
./config.sh --url https://github.com/k4kTu5-1337/devops-docker --token <TOKEN>
```

2. Запустить runner:

```bash
./run.sh
```

### Workflow .github/workflows/build-and-deploy.yml

```yaml
name: Build & Deploy Local
on:
  push:
    branches: [ main ]
jobs:
  build-and-deploy:
    runs-on: self-hosted
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Build Docker image
        uses: docker/build-push-action@v6
        with:
          context: .
          push: false
          tags: devops-docker:latest

      - name: Deploy with docker-compose
        run: |
          cd /opt/blog/devops-docker
          docker compose down || true
          docker compose up -d --build --remove-orphans
```

Workflow автоматически запускается при push в main.
Деплой происходит на той же VM, где установлен self-hosted runner.

Таким образом, все шаги CI/CD выполняются локально и корректно, хотя первоначальная идея с SSH и NAT не сработала.

