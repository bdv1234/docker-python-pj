# -- builder ---
FROM python:3.11-slim AS builder
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN apt-get update && apt-get install -y build-essential libpq-dev \
    && pip install --upgrade pip \
    && pip wheel --no-cache-dir --no-deps --wheel-dir /wheels  -r requirements.txt \
    && apt-get remove -y build-essential libpq-dev \
    && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

# -- final image ---
FROM python:3.11-slim
WORKDIR /app
ENV PATH="/root/.local/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# --- create a non root user ---
RUN addgroup --system app && adduser --system --ingroup app app

COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/*

COPY . /app
RUN chown -R app:app /app
USER app


EXPOSE 5002
CMD ["gunicorn", "app.app:app", "-c", "gunicorn_conf.py"]
