FROM python:3

# Define container app directory
RUN mkdir /app
WORKDIR /app/

# Copy entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh \
    && sed -i 's/\r$//' /entrypoint.sh

EXPOSE 8050

# IMPORTANT: use entrypoint, not command
ENTRYPOINT ["/entrypoint.sh"]
# CMD ["python", "main.py"]
