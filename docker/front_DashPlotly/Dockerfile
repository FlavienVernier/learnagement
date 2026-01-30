FROM python:3.13
# Or any preferred Python version.


# Define container app directory
RUN mkdir /app
WORKDIR /app

# Data directory
# ToDo must be remove so that data will accessed via db
#RUN mkdir /data/


# Copy entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh \
    && sed -i 's/\r$//' /entrypoint.sh


# Rum app
ENTRYPOINT ["/entrypoint.sh"]
