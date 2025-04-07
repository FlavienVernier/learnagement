FROM python:3.9 
# Or any preferred Python version.

# Install requirement,
#ToDo must be moved into requirement file of app
RUN pip install requests beautifulsoup4 python-dotenv dash dash_bootstrap_components dash_core_components dash_html_components pandas geopy networkx matplotlib mysql mysql-connector mysql_connector_repackaged plotly

# Define container app directory
RUN mkdir /app
WORKDIR /app

#RUN python -m venv /opt/venv
# Enable venv
#ENV PATH="/opt/venv/bin:$PATH"

#COPY ./requirements.txt /app/requirements.txt
#RUN pip install -Ur requirements.txt

# Data directory
# ToDo must be remove so that data will accessed via db
RUN mkdir /data/

# Rum app
CMD ["python", "./main.py"] 


# With venv
#FROM python:3.9-slim as compiler
#ENV PYTHONUNBUFFERED 1

#WORKDIR /app/

#RUN python -m venv /opt/venv
# Enable venv
#ENV PATH="/opt/venv/bin:$PATH"

#COPY ./requirements.txt /app/requirements.txt
#RUN pip install -Ur requirements.txt

#FROM python:3.9-slim as runner
#WORKDIR /app/
#COPY --from=compiler /opt/venv /opt/venv

# Enable venv
#ENV PATH="/opt/venv/bin:$PATH"
#COPY . /app/
#CMD ["python", "app.py", ]