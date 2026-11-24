#FROM python:3.14
#
#RUN apt-get update && apt-get install -y graphviz && rm -rf /var/lib/apt/lists/*
#
## Define container app directory
#RUN mkdir /app
#WORKDIR /app/
#
## Copy entrypoint
#COPY entrypoint.sh /entrypoint.sh
#RUN chmod +x /entrypoint.sh \
#    && sed -i 's/\r$//' /entrypoint.sh
#
#EXPOSE 8050
#
## IMPORTANT: use entrypoint, not command
#ENTRYPOINT ["/entrypoint.sh"]
## CMD ["python", "main.py"]

############## base : OS ##############
FROM python:3.14 AS base
# TODO : épingler (python:3.14.x@sha256:...)

RUN apt-get update \
 && apt-get install -y --no-install-recommends libldap2-dev libsasl2-dev libssl-dev \
 && rm -rf /var/lib/apt/lists/*

RUN groupadd --system --gid 10001 app \
 && useradd  --system --uid 10001 --gid app \
    --create-home --home-dir /home/app --shell /usr/sbin/nologin app

# venv HORS de l'app, appartenant à app
ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
RUN python -m venv /opt/venv && chown -R app:app /opt/venv

RUN mkdir /app && chown app:app /app
WORKDIR /app

# Entrypoint propriété de root : le process app ne peut pas le modifier
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN sed -i 's/\r$//' /usr/local/bin/entrypoint.sh \
 && chmod 755 /usr/local/bin/entrypoint.sh

EXPOSE 4000
USER app
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

############## dev : code monté en volume ##############
FROM base AS dev
ENV ENV=dev

############## prod : code et dépendances dans l'image ##############
FROM base AS prod
ENV ENV=prod
COPY --from=os --chown=app:app requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY --from=os --chown=app:app . /app