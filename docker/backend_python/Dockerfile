FROM python:3.14

RUN apt-get update
RUN apt-get install -y libldap2-dev libsasl2-dev libssl-dev

# Define container app directory
RUN mkdir /app
WORKDIR /app/

# Copy entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh \
    && sed -i 's/\r$//' /entrypoint.sh

EXPOSE 4000

# IMPORTANT: use entrypoint, not command
ENTRYPOINT ["/entrypoint.sh"]
# CMD ["python", "app.py"]