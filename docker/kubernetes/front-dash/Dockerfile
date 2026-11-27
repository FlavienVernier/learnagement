FROM python:3.14-slim AS dependencies

WORKDIR /build
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"
COPY front_DashPlotly/requirements.txt ./requirements.txt
RUN python -m pip install --no-cache-dir \
        --index-url https://download.pytorch.org/whl/cpu \
        "torch==2.15.0+cpu" \
    && python -m pip install --no-cache-dir -r requirements.txt

FROM python:3.14-slim

ENV PATH="/opt/venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOME=/tmp

RUN apt-get update \
    && apt-get install -y --no-install-recommends graphviz libgl1 libglib2.0-0 libgomp1 \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /data \
    && chown 10001:10001 /data

WORKDIR /app
COPY --from=dependencies /opt/venv /opt/venv
COPY --chown=10001:10001 front_DashPlotly/ /app/

USER 10001:10001
EXPOSE 8050
STOPSIGNAL SIGTERM

CMD ["gunicorn", "--bind", "0.0.0.0:8050", "--workers", "2", "--access-logfile", "-", "--error-logfile", "-", "main:server"]
