
FROM python:3.11

ARG BUILD_ENVIRONMENT=local

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY ./backend/requirements .

RUN if [ "$BUILD_ENVIRONMENT" = "local" ]; then \
        echo ">>> Installing development requirements" && \
        pip install --no-cache-dir -r /app/${BUILD_ENVIRONMENT}.txt; \
    else \
        echo ">>> Installing production requirements" && \
        pip install --no-cache-dir -r /app/${BUILD_ENVIRONMENT}.txt; \
    fi

COPY . .

COPY backend/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
