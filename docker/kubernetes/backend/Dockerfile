# Purpose: build the non-root FastAPI Backend image used by the Kubernetes Deployment.
FROM python:3.14-slim AS dependencies

WORKDIR /build
COPY backend_python/requirements.txt ./requirements.txt
RUN python -m pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/usr/local/bin:${PATH}"

WORKDIR /app
COPY --from=dependencies /install /usr/local
COPY --chown=10001:10001 backend_python/ /app/

USER 10001:10001
EXPOSE 4000
STOPSIGNAL SIGTERM

CMD ["python", "app.py"]
