Setup (local)
--------------
1) Create and activate virtualenv, then install deps:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2) Environment variables (examples):

```bash
export DATABASE_URL=postgresql://user:pass@localhost:5432/taskify
export REDIS_URL=redis://localhost:6379/0
# or explicitly
# export CELERY_BROKER_URL=redis://localhost:6379/0
# export CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

Database migrations (Alembic)
-----------------------------
- Generate a migration (after changing models):

```bash
alembic revision -m "describe your change"
```

- Apply migrations:

```bash
alembic upgrade head
```

Run the API (Gunicorn)
----------------------
```bash
gunicorn -c gunicorn_conf.py app.app:app
```

Start Celery worker
-------------------
```bash
celery -A app.tasks.celery worker --loglevel=info
```

Endpoints
---------
- Health:

```bash
curl -s http://localhost:8000/health | jq
```

- List tasks:

```bash
curl -s http://localhost:8000/tasks | jq
```

- Create task (triggers background job via Celery):

```bash
curl -s -X POST http://localhost:8000/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Example","description":"Demo task"}' | jq
```

- Prometheus metrics:

```bash
curl -s http://localhost:8000/metrics | head
```

Notes
-----
- Ensure Postgres and Redis (containers above) are running before starting the app/worker.
- The app reads Celery URLs from `CELERY_BROKER_URL`/`CELERY_RESULT_BACKEND` or `REDIS_URL`.

Run everything with Docker
--------------------------
The following commands bring up Postgres, Redis, run DB migrations, start the API, and a Celery worker. Replace `taskify:latest` with your built image tag if different.

```bash
# 1) Create a dedicated network for service discovery
docker network create taskify-net

# 2) Start PostgreSQL
docker run -d \
  --name taskify-db \
  --network taskify-net \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=pass \
  -e POSTGRES_DB=taskify \
  -p 5432:5432 \
  -v taskify_pgdata:/var/lib/postgresql/data \
  postgres:14

# 3) Start Redis
docker run -d \
  --name redis-server \
  --network taskify-net \
  -p 6379:6379 \
  -v redis-data:/data \
  redis:latest

# 4) Run DB migrations (one-off)
docker run --rm \
  --network taskify-net \
  -e DATABASE_URL=postgresql://user:pass@taskify-db:5432/taskify \
  taskify:latest \
  alembic upgrade head

# 5) Start the API (Gunicorn) on port 5002
docker run -d \
  --name taskify-api \
  --network taskify-net \
  -p 5002:5002 \
  -e DATABASE_URL=postgresql://user:pass@taskify-db:5432/taskify \
  -e REDIS_URL=redis://redis-server:6379/0 \
  taskify:latest

# 6) Start the Celery worker
docker run -d \
  --name taskify-worker \
  --network taskify-net \
  -e DATABASE_URL=postgresql://user:pass@taskify-db:5432/taskify \
  -e REDIS_URL=redis://redis-server:6379/0 \
  taskify:latest \
  celery -A app.tasks.celery worker --loglevel=info
```

Quick checks:

```bash
curl http://localhost:5002/health
curl -X POST http://localhost:5002/tasks -H 'Content-Type: application/json' -d '{"title":"Example","description":"Demo"}'
```