FROM python:3.11

ARG BUILD_ENVIRONMENT=prod
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

RUN apt-get update && apt-get install -y --no-install-recommends netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./backend/requirements ./requirements

RUN if [ "$BUILD_ENVIRONMENT" = "local" ]; then \
        echo ">>> Installing development requirements" && \
        pip install --no-cache-dir -r requirements/local.txt; \
    else \
        echo ">>> Installing production requirements" && \
        pip install --no-cache-dir -r requirements/prod.txt; \
    fi

COPY ./backend .

RUN chmod +x /app/entrypoints/*.sh

ENTRYPOINT ["/app/entrypoints/start.sh"]
